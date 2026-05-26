---
title: Kubernetes PVC 访问模式：RWO 简介
author: "-"
date: 2026-05-26T11:51:03+08:00
lastmod: 2026-05-26T11:51:03+08:00
url: pvc-access-modes
categories:
  - cloud
tags:
  - k8s
  - pvc
  - longhorn
  - remix
  - AI-assisted
---

## 是什么

PVC 的 `accessModes` 描述的是**这块卷在集群里能被怎样挂载**，不是 Linux 文件权限里的 `rwx`。

Kubernetes 常见三种：

| 模式 | 全称 | 含义（简化） |
| ---- | ---- | ------------ |
| **RWO** | ReadWriteOnce | 同一时刻，**最多一个节点**以读写方式挂载 |
| **ROX** | ReadOnlyMany | 多个节点可同时**只读**挂载 |
| **RWX** | ReadWriteMany | 多个节点可同时**读写**挂载（需 NFS、CephFS、Longhorn RWX 等） |

日常自建集群里，Longhorn、本地盘、云厂商块存储（EBS 等）给 Pod 用的，几乎都是 **RWO**。

## RWO 不等于 Pod 不能换节点

很多人会把 RWO 理解成「Pod 永远绑死在一个节点上」。更准确的说法是：

- **同一时刻**只能有一个节点挂载读写；
- Pod 迁到另一节点时，流程是：**旧 Pod 退出 → 卷 detach → 新节点 attach → 新 Pod 启动**。

因此 RWO **不阻止** Pod 漂移，但**不允许**两个 Pod 同时挂同一块盘。

## 和 Longhorn 副本数的关系

Longhorn 的 `numberOfReplicas: 2` 表示**数据在多个节点各存一份**（容错、迁移时 attach 更快），与 RWX 无关：

- **2 副本**：备份/调度层面；
- **RWO**：运行时仍只有一个节点在挂载读写。

二者可以同时存在，例如 Nexus 在 k8s-50 / k8s-71 各有一份 replica，但 Pod 仍只有一个。

## 常见踩坑：RollingUpdate + RWO

Deployment 默认 `RollingUpdate` 会先起新 Pod、再删旧 Pod。对挂 RWO PVC 的单副本应用，会出现：

```text
Multi-Attach error: Volume is already used by pod ...
```

新 Pod 在节点 B，旧 Pod 在节点 A，两块都想挂同一块盘，第二个会失败。

### 处理方式

对有状态、**replicas: 1** 且使用 RWO 的 Deployment，建议：

```yaml
spec:
  strategy:
    type: Recreate
```

`Recreate` 会先删旧 Pod，再建新 Pod，避免短暂的双挂载冲突。代价是更新时会有**短时间的停服**。

## RWX 能替代 RWO 吗

技术上可以选支持 RWX 的 StorageClass，但：

- 应用本身若**不支持多写者**（如 Nexus、单实例数据库），仍应 `replicas: 1`；
- 两个 Pod 同时写同一目录可能损坏数据；
- RWX 往往更复杂、开销更高。

对单实例有状态服务，**RWO + Recreate** 通常是更简单的组合。

## 相关

- 集群命令与 PV/PVC 示例：[k8s-command](/k8s-command)
- Tekton Workspace 里的 RWO 示例：[tekton-kaniko](/tekton-kaniko)
- Pod 与存储卷概念：[k8s](/k8s)
