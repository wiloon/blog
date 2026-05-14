---
title: Conflict Check Design Pattern
author: "-"
date: 2026-05-14T20:17:36+08:00
lastmod: 2026-05-14T22:43:32+08:00
url: conflict-check-design-pattern
categories:
  - Pattern
tags:
  - original
  - AI-assisted
  - nso
  - redis
  - firewall
---

## 背景

在一个网络自动化项目中，防火墙策略由 NSO 缓存在 Redis 中，主要有两种数据结构：

- **object**：地址对象，`key` 是名称，`value` 是一个数组，数组元素是实际的 IP 地址或 CIDR 网段
- **group_object**：地址组，有自己的 `name` 和 `value`，`value` 是一个数组，数组元素是 `object` 的 name 或另一个 `group_object` 的 name

group 和 object 形成嵌套结构：一个 group 的 value 列表里，既可以直接引用 object，也可以引用其他 group，形成递归树。

## 问题

冲突检测模块的目标是判断用户提交的网络策略是否已在设备缓存中存在，并决定后续操作：

| 情况 | 结果 |
| --- | --- |
| 用户策略在缓存中**不存在** | 在设备上新建策略 |
| 用户策略在缓存中**部分存在** | 更新设备上的策略数据 |
| 用户策略是缓存中某条策略的**超集 (superset)** | 更新设备上的策略数据 |
| 用户策略与缓存中某条策略**完全匹配** | 不需要做任何操作 |
| 用户策略是缓存中某条策略的**子集 (subset)** | 不需要做任何操作 |

设备上过期策略的删除由其它模块处理，不属于本模块的责任范围。

每条策略（用户输入或设备缓存）有以下几个关键属性：

- **src**：源地址数组，每个元素是 `object_name` 或 `group_name`（address_object）
- **dst**：目标地址数组，结构与 src 相同
- **service**：协议和端口数组，每个元素是 `service_object_name` 或 `service_group_name`

src 和 dst 属于 address_object，service 属于 service_object。两种类型都具备 group/object 嵌套结构，因此 `PolicyObject` 类可以同时表达这两种类型的对象。

如果直接操作 Redis 的原始数据结构，业务代码需要：

1. 知道 Redis key 的命名规则
2. 手动递归展开 group 的嵌套引用
3. 每次比较都重复展开逻辑

这让冲突检测逻辑和缓存数据结构强耦合，可读性和可测试性都很差。

## 设计：用 Composite Pattern 封装

将 object 和 group_object 统一抽象为 `PolicyObject`，形成树形结构：

| 角色 | 映射 |
| --- | --- |
| Component | `PolicyObject`（统一接口） |
| Leaf | `object`（IP/网段，没有子节点） |
| Composite | `group_object`（包含子节点的组） |

### PolicyObject 类设计

```python
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class PolicyObject:
    name: str

    # 直接子节点（对应 group_object 的 value 数组展开后的直接引用）
    # 对于叶子节点，此列表为空
    sub_objects: list[PolicyObject] = field(default_factory=list)

    # 递归展开后所有叶子节点（实际的 IP/网段 object）
    # 冲突检测时直接遍历此列表，无需关心层级结构
    leaf_objects: list[PolicyObject] = field(default_factory=list)

    # 仅叶子节点有值，存放实际的 IP 地址或 CIDR 网段列表
    value: list[str] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return len(self.sub_objects) == 0
```

### 构建树结构

加载 Redis 缓存后，将所有 object 和 group_object 解析为 `PolicyObject`，递归绑定引用关系：

```python
def build_policy_object(
    name: str,
    object_map: dict[str, list[str]],     # name -> [ip/cidr, ...]
    group_map: dict[str, list[str]],     # name -> [member_name, ...]
) -> PolicyObject:
    if name in object_map:
        # 叶子节点
        node = PolicyObject(name=name, value=object_map[name])
        node.leaf_objects = [node]
        return node

    if name in group_map:
        # 容器节点：递归构建子节点
        subs = [
            build_policy_object(member, object_map, group_map)
            for member in group_map[name]
        ]
        leaves = [
            leaf
            for sub in subs
            for leaf in sub.leaf_objects
        ]
        node = PolicyObject(name=name, sub_objects=subs, leaf_objects=leaves)
        return node

    raise ValueError(f"Unknown policy object: {name}")
```

### Policy 类设计

每条策略用 `Policy` 类表示，其中 src、dst、service 均为 `PolicyObject` 列表（已经展开成树结构）：

```python
@dataclass
class Policy:
    src: list[PolicyObject]      # 源地址（address_object）
    dst: list[PolicyObject]      # 目标地址（address_object）
    service: list[PolicyObject]  # 协议和端口（service_object）
```

## 效果

### 冲突检测逻辑

```python
import ipaddress
from enum import Enum


class ConflictResult(Enum):
    NO_MATCH = "no_match"       # 在缓存中不存在，需新建
    PARTIAL = "partial"         # 部分重叠，需更新
    SUPERSET = "superset"       # 是缓存策略的超集，需更新
    EXACT_MATCH = "exact_match" # 完全匹配，无需操作
    SUBSET = "subset"           # 是缓存策略的子集，无需操作


def ip_ranges_overlap(cidr_a: str, cidr_b: str) -> bool:
    net_a = ipaddress.ip_network(cidr_a, strict=False)
    net_b = ipaddress.ip_network(cidr_b, strict=False)
    return net_a.overlaps(net_b)


def get_leaf_cidrs(objects: list[PolicyObject]) -> set[str]:
    """展开 PolicyObject 列表，收集所有叶子节点的 CIDR 字符串集合"""
    return {
        cidr
        for obj in objects
        for leaf in obj.leaf_objects
        for cidr in leaf.value
    }


def check_conflict(user_policy: Policy, cached_policy: Policy) -> ConflictResult:
    user_src = get_leaf_cidrs(user_policy.src)
    user_dst = get_leaf_cidrs(user_policy.dst)
    cached_src = get_leaf_cidrs(cached_policy.src)
    cached_dst = get_leaf_cidrs(cached_policy.dst)

    src_match = user_src == cached_src
    dst_match = user_dst == cached_dst

    if src_match and dst_match:
        return ConflictResult.EXACT_MATCH

    src_subset = user_src.issubset(cached_src)
    dst_subset = user_dst.issubset(cached_dst)

    if src_subset and dst_subset:
        return ConflictResult.SUBSET

    src_superset = cached_src.issubset(user_src)
    dst_superset = cached_dst.issubset(user_dst)

    if src_superset and dst_superset:
        return ConflictResult.SUPERSET

    src_overlap = any(
        ip_ranges_overlap(a, b) for a in user_src for b in cached_src
    )
    dst_overlap = any(
        ip_ranges_overlap(a, b) for a in user_dst for b in cached_dst
    )

    if src_overlap or dst_overlap:
        return ConflictResult.PARTIAL

    return ConflictResult.NO_MATCH
```

业务代码层就可以直接基于 `ConflictResult` 决策，完全不需要感知 Redis 数据结构和 group 的嵌套层级。

## 小结

`sub_objects` 保留了原始的直接子节点关系，便于调试和展示树结构；`leaf_objects` 是为冲突检测场景专门缓存的展开结果，是对标准 Composite Pattern 的实用扩展——牺牲少量内存，换取检测时无需重复递归遍历。

---

> 相关：[Composite Pattern](/composite-pattern)
