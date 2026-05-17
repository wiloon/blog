---
title: IPv6 地址类型与配置
author: "-"
date: 2026-05-09T16:00:55+08:00
url: ipv6
categories:
  - network
tags:
  - ipv6
  - remix
  - AI-assisted
aliases:
  - /p11537/
---

## GUA（Global Unicast Address，全局单播地址）

GUA 是 IPv6 中可在公网上路由的地址类型，相当于 IPv4 的公网 IP。

**地址格式**

GUA 地址以 `2000::/3` 开头，即前 3 位为 `001`，实际分配中几乎所有 GUA 地址都以 `2` 或 `3` 开头。

```
| 48 位全局路由前缀 | 16 位子网 ID | 64 位接口 ID |
```

- **全局路由前缀（Global Routing Prefix）**：由 ISP 或 RIR 分配，用于全球路由
- **子网 ID（Subnet ID）**：由站点管理员划分子网
- **接口 ID（Interface ID）**：标识同一子网内的主机，通常通过 SLAAC（EUI-64）或随机生成

**典型示例**

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

其中 `2001:0db8::/32` 是文档示例专用前缀（RFC 3849），不会在公网上实际路由。

**与 IPv4 公网 IP 的对比**

| 特性 | IPv4 公网 IP | IPv6 GUA |
| ---- | ------------ | -------- |
| 全球可路由 | ✓ | ✓ |
| 地址数量 | 约 43 亿 | 约 $3.4 \times 10^{38}$ |
| NAT 需求 | 通常需要 | 通常不需要 |
| 分配方式 | ISP 分配（动态/静态） | ISP 分配前缀，设备自动生成 |

**常见 GUA 前缀段**

- `2001::/32` — IANA 分配给各 RIR
- `2400::/12`、`2401::/16` — APNIC（亚太地区）
- `2600::/12` — ARIN（北美）
- `2a00::/12` — RIPE NCC（欧洲）

## ULA（Unique Local Address，唯一本地地址）

ULA 是 IPv6 的私有地址，相当于 IPv4 的 `192.168.x.x`、`10.x.x.x`、`172.16.x.x`，**不在公网上路由**，用于组织内部通信。

**地址格式**

ULA 地址以 `fc00::/7` 开头，实际使用中几乎都以 `fd` 开头：

```
| 8 位前缀 fd | 40 位全局 ID（随机） | 16 位子网 ID | 64 位接口 ID |
```

- **前缀**：固定为 `fd00::/8`（`fc00::/8` 理论上预留，实际未使用）
- **全局 ID**：40 位随机生成，用于区分不同组织的内部网络，避免合并网络时冲突
- **子网 ID**：管理员自行划分

**典型示例**

```
fd12:3456:789a:0001::1
```

**与 IPv4 私有地址的对比**

| 特性 | IPv4 私有地址 | IPv6 ULA |
| ---- | ------------- | -------- |
| 公网可路由 | ✗ | ✗ |
| 地址段固定 | ✓（RFC 1918） | 全局 ID 随机，冲突概率极低 |
| 典型用途 | 局域网内部 | 局域网 / 数据中心内部 |

---

## Link-Local Address（链路本地地址）

这就是你在虚拟机网卡上看到的、由 MAC 地址生成的 IPv6 地址。它**只能在同一个二层网段（链路）内通信**，不会被路由器转发，相当于"同一交换机内可用"。

**地址格式**

Link-Local 地址固定前缀为 `fe80::/10`，接口 ID 通过 EUI-64 算法从 MAC 地址派生：

```
fe80::/64 + EUI-64 接口 ID
```

**EUI-64 生成过程**

以 MAC 地址 `52:54:00:ab:cd:ef` 为例：

1. 从中间插入 `ff:fe`：`52:54:00:ff:fe:ab:cd:ef`
2. 翻转第 7 位（U/L 位）：`52` → `0101 0010` → 翻转第 7 位 → `0101 0000` → `50`
3. 最终接口 ID：`5054:00ff:feab:cdef`
4. 完整地址：`fe80::5054:00ff:feab:cdef`

> 现代 Linux 内核默认使用随机生成的接口 ID（RFC 7217）而非 EUI-64，以保护隐私。

**特点**

- 每块网卡**自动生成**，无需 DHCP 或手动配置
- 只在本链路有效，**不可跨路由器**
- 用于邻居发现协议（NDP）、路由器发现（RA）等底层协议
- 可用 `ping6 fe80::xxxx%eth0` 测试（需指定网卡）

**三种地址类型对比**

| 类型 | 前缀 | 路由范围 | IPv4 类比 |
| ---- | ---- | -------- | --------- |
| GUA | `2000::/3` | 全球公网 | 公网 IP |
| ULA | `fc00::/7`（常用 `fd`） | 组织内部 | 私有 IP |
| Link-Local | `fe80::/10` | 同一链路 | 169.254.x.x |

---

## RA（Router Advertisement，路由器通告）

RA 是 IPv6 邻居发现协议（NDP，RFC 4861）的核心机制之一。路由器周期性地向链路上的所有主机广播 RA 消息，告知主机如何配置地址和默认路由。

**RA 的作用**

- **地址自动配置（SLAAC）**：路由器在 RA 中携带网络前缀（如 `2001:db8:1::/64`），主机收到后自动拼接接口 ID 生成 GUA 地址，无需 DHCPv6
- **默认网关**：主机将发送 RA 的路由器链路本地地址（`fe80::...`）作为默认网关
- **MTU 通告**：告知链路 MTU，避免分片
- **DNS 配置（RDNSS）**：RFC 8106 扩展允许 RA 携带 DNS 服务器地址

**RA 消息格式（关键字段）**

| 字段 | 含义 |
| ---- | ---- |
| Cur Hop Limit | 建议的 IP 跳数限制 |
| M 标志（Managed） | 置 1 时提示主机使用 DHCPv6 获取地址 |
| O 标志（Other） | 置 1 时提示主机通过 DHCPv6 获取其他配置（如 DNS） |
| Router Lifetime | 路由器作为默认网关的有效时间（秒） |
| Prefix Information | 网络前缀、前缀长度、有效期 |
| RDNSS | DNS 服务器地址（可选） |

**地址配置模式（由 M/O 标志决定）**

| M 标志 | O 标志 | 配置方式 |
| ------ | ------ | -------- |
| 0 | 0 | 纯 SLAAC，地址和 DNS 均由 RA 提供 |
| 0 | 1 | SLAAC 生成地址，DHCPv6 获取 DNS 等配置 |
| 1 | 1 | 完整 DHCPv6，地址和配置均由 DHCPv6 分配 |

**RA 工作流程**

```
主机上线
  │
  ├─→ 发送 RS（Router Solicitation）组播到 ff02::2（所有路由器）
  │
路由器收到 RS
  │
  └─→ 回复 RA（Router Advertisement）到 ff02::1（所有节点）
          包含：前缀、网关、MTU、DNS...
                │
主机收到 RA
  │
  └─→ 前缀 + 接口 ID → 生成 GUA 地址
      fe80::路由器地址 → 设为默认网关
```

**查看 RA 相关信息**

```bash
# 查看路由器通告接收到的前缀
ip -6 route show

# 抓包查看 RA 消息（ICMPv6 type 134）
tcpdump -i eth0 'icmp6 and ip6[40] == 134'

# Linux 上查看网卡接受 RA 的配置
cat /proc/sys/net/ipv6/conf/eth0/accept_ra
```

---

## 禁用 ipv6

```bash
vim /etc/sysctl.d/ipv6.conf

#disable ipv6
ipv6.disable=1

```
[https://wiki.archlinux.org/title/IPv6#Disable_IPv6](https://wiki.archlinux.org/title/IPv6#Disable_IPv6)
