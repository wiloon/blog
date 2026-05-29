---
title: Proxmox VE 虚拟机内存热扩容（虚拟机内 Arch Linux）
author: "-"
date: 2026-05-29T10:59:18+08:00
lastmod: 2026-05-29T11:34:38+08:00
url: pve-vm-memory-hotplug
categories:
  - cloud
tags:
  - proxmox
  - linux
  - kubernetes
  - opentofu
  - remix
  - AI-assisted
---

## 背景

在 homelab 里用 OpenTofu 管理 PVE 上的 K8s 节点（例如 r86s 上的 **k8s-51** control-plane、**k8s-50** worker）。k8s-51 曾长期只分配 **4GiB** 内存，同时承担 API VIP、kube-apiserver 与 **etcd Leader**，容易出现 apiserver 访问本地 etcd 超时，进而导致其它节点因 **node lease 续租失败** 被标为 NotReady。

后续将 k8s-51 内存一度调到 **8GiB** 缓解压力；在 r86s 物理机仅 **16GB**、且 K8s 节点统一 **`balloon: 0`** 的前提下，又把 k8s-51 调回 **6GiB**，与 k8s-50 的 6GiB 合计约 12GiB，给宿主机留出缓冲。

本文记录：**内存热扩容**、**memory balloon**、以及 **`balloon: 0` 时如何规划 VM 内存**。

## 结论一览

| 问题 | 答案 |
| --- | --- |
| PVE 能否在线加大内存？ | 一般可以（只增不减时，多数情况无需先关机） |
| 虚拟机内 Linux 能否感知并用上？ | 可以，内核通过 ACPI 内存热插拔 online 新内存 |
| 虚拟机内要不要额外命令？ | 加内存通常**不需要**（不同于磁盘要 `growpart`） |
| 是否保证绝不重启？ | **不保证**；缩内存时更可能重启 |
| balloon 在哪配置？ | **PVE 每台 VM 的配置文件**，不是 Arch 里的设置 |
| K8s 节点建议开 balloon 吗？ | homelab 建议 **统一 `balloon: 0`**，靠给够 `memory` 而不是超卖 |

## PVE / QEMU 侧

### 只加不减

- 在 PVE 中增大 VM 的 `memory`（单位 **MiB**，6GiB = `6144`，8GiB = `8192`）时，通常可对**运行中**的虚拟机通过 QEMU **热插内存条（ACPI DIMM hotplug）** 完成。
- **缩小**内存：一般需要**关机**或会触发重启；运行中缩容既不安全，也基本不可行。

#### 开了 balloon，扩容还要不要 ACPI 热插拔？

**不能简单理解成「开了 balloon 就不用 ACPI 热插拔」**，要分清你在改什么：

| 你在做的操作 | 和 balloon 的关系 | 典型实现 |
| --- | --- | --- |
| **把 PVE 里的 `memory` 调大**（OpenTofu / `qm set`，例如 6G→8G） | 与 balloon **开或关无关** | 仍多为 **ACPI 热插拔**（或重启后生效）；这是在给 VM **多加物理内存条** |
| **宿主机紧张，从 VM 收回内存** | balloon **inflate** | 在**已有** `memory` 范围内腾给 PVE，**不**等于热插拔 |
| **宿主机空闲，让 VM 多用一点**（在已配置的 min～max 之间） | balloon **deflate** 或 PVE 自动调内存 | 在**已划给该 VM 的上限内**调节，**不是**你把 `memory` 从 6G 改成 8G 那种改配置 |

因此：

- 本文 / OpenTofu 改的 **`memory.dedicated`**：属于上表第一行 —— **就算启用了 balloon，把 `memory` 数值加大时，一般仍走 ACPI 热插拔**（Linux 里 `free` 总量上涨）。
- Balloon **不能替代**「给 VM 多分配 2GiB 物理 RAM」；它主要是在**已分配额度内**和宿主机来回借还，或配合 PVE 的 min/max 自动调节。

**`balloon: 0`** 时：没有借还机制，要加内存**只能**调大 `memory` → 热插拔或重启；逻辑更直白，也更适合 K8s。

### 什么是 memory balloon

**Balloon 不是 PVE 独有，也不是 Arch 独有**，而是 **QEMU/KVM 虚拟化栈**里的机制：

| 层级 | 角色 |
| --- | --- |
| **PVE** | 在 VM 配置里暴露 `balloon`、`memory`（`qm config` 可见） |
| **QEMU** | 给虚拟机挂 **virtio-balloon** 虚拟设备 |
| **虚拟机内的 Linux** | 内核 **virtio_balloon** 驱动与 hypervisor 配合 |

宿主机与虚拟机**协商**「这台 VM 暂时少用一点内存」，而不是在 PVE 里把 `memory` 字段改小那种硬改配置。

#### Balloon 解决什么问题？

主要给 **宿主机提高内存利用率 / 超卖（overcommit）** 用：

- 多台 VM 配置的内存之和可以大于物理 RAM（前提是并非同时吃满）。
- 宿主机紧张时，balloon **膨胀（inflate）**：在虚拟机内占走一部分页，把物理内存还给 PVE。
- 压力缓解后 **收缩（deflate）**，虚拟机再把内存要回来。

适合：大量轻量 VM、测试机。不适合：etcd、数据库、对延迟敏感的 control-plane。

#### 和「内存热扩容」不是一回事

| | Memory balloon | ACPI 内存热插拔（热加 RAM） |
| --- | --- | --- |
| **目的** | 在**已分配的 RAM 内**动态腾挪，方便宿主机复用 | **增加** VM 可见总内存 |
| **是否改 PVE `memory`** | 通常不靠手改 `memory` 来缩 | 需要把 `memory` 从 4096 调到 6144/8192 等 |
| **虚拟机内** | 需要 virtio_balloon 驱动 | 需要 memory hotplug |

**关掉 balloon 也可以热加内存**（改 `memory` 仍走 ACPI 热插拔）。**开着 balloon 改大 `memory`** 时，通常**同样**走热插拔；balloon 负责的是另一条「在额度内借还」的链路，两者不互相替代。

#### `balloon` 配置写在哪？

在 **对应 PVE 节点**上的 VM 配置文件（集群环境为共享存储路径）：

```text
/etc/pve/qemu-server/<VMID>.conf
```

查看：

```bash
# 在 PVE 宿主机（如 192.168.50.5）上
qm config 103
grep -E '^memory|^balloon' /etc/pve/qemu-server/103.conf
```

Web UI：**虚拟机 → 硬件 → 内存** 里的 Ballooning Device 勾选与否，效果等价。

当前 homelab 的 OpenTofu（`homelab/opentofu/pve`）只管理 `memory { dedicated = ... }`，**尚未纳管 `balloon`**；若在 UI 里改过 balloon，以 PVE 实际配置为准，避免 state drift。

#### PVE 里 `balloon` 各取值的含义

依据 [PVE `qm.conf` 文档](https://pve.proxmox.com/pve-docs/qm.conf.5.html)：

| 配置 | 含义 |
| --- | --- |
| **不写 `balloon` 行** | 默认 **启用** virtio balloon（固定 `memory` 时也常用于上报 guest 实际用量） |
| **`balloon: 0`** | **显式关闭** balloon 设备 |
| **`balloon: N`（N>0）** | 启用，且目标内存为 N MiB（配合自动扩缩等场景） |

示例（k8s-51 关闭 balloon）：

```text
memory: 6144
balloon: 0
```

- `memory`：分配给该 VM 的内存（MiB）。
- `balloon: 0`：不使用 balloon 从 guest 回收内存。

### K8s 节点：是否开 balloon？

| 节点类型 | 建议 | 说明 |
| --- | --- | --- |
| **control-plane**（如 k8s-51） | **`balloon: 0`** | 避免宿主机抽内存导致 API / etcd 超时、Node NotReady |
| **worker**（如 k8s-50） | homelab 也建议 **`balloon: 0`** | worker 上有 DaemonSet、Longhorn、监控等；同一台 PVE 上只抽 worker 仍可能拖垮集群 |

「CP 关 balloon、worker 开 balloon」在理论上说得通，但 **16GB 宿主机跑两台 K8s 时**，抽 worker 对宿主机帮助有限，却仍有 NotReady 风险。本环境 **r86s 上 k8s-50、k8s-51 均为 `balloon: 0`**。

### 统一 `balloon: 0` 时，VM 内存怎么分？

**不能**在 16GB 物理机上让两台跑着的 K8s VM 各配 8GiB 还长期稳定：`balloon: 0` 时，分给 VM 的内存会**实打实占住**，不会从 guest 里往回抽。

粗算：

```text
VM 合计上限 ≈ 宿主机物理内存 − PVE/系统预留（约 3～4GiB）
```

以 **r86s（192.168.50.5，约 16GB 物理内存）** 为例，长期同时运行 **k8s-50 + k8s-51**（win11 常关）：

| VM | 角色 | 内存（MiB） | 说明 |
| --- | --- | --- | --- |
| k8s-51 | control-plane | **6144（6GiB）** | OpenTofu `k8s_51_memory_mib` |
| k8s-50 | worker | **6144（6GiB）** | 与 51 合计约 12GiB，留给宿主机约 3～4GiB |
| win11-ltsc | 桌面 | 4096 | 若开机需再扣减或先停其它 VM |

| 方案 | k8s-51 | k8s-50 | 合计 | 评价 |
| --- | --- | --- | --- | --- |
| 两台各 8GiB | 8192 | 8192 | ~16GiB | 宿主机几乎无余地，不推荐 |
| 8 + 6（曾用） | 8192 | 6144 | ~14GiB | 偏紧 |
| **6 + 6（当前）** | 6144 | 6144 | ~12GiB | 更适合 16GB + `balloon: 0` |

缩 k8s-51 到 6GiB 后，r86s 宿主机 `available` 可从约 3GiB 提升到约 7GiB 量级（视当时负载而定）。

### 和磁盘扩容的区别

| 操作 | PVE 宿主机改配置 | 虚拟机内是否还要操作 |
| --- | --- | --- |
| **加内存** | 在线改 `memory` 即可 | 通常不用，内核自动 online |
| **扩磁盘** | 在线可改虚拟盘容量 | **需要** `growpart` + `resize2fs`（或等价工具） |

## 虚拟机内（Arch Linux）

Homelab 节点系统是 Arch Linux（例如 `6.18.x` LTS），具备 **memory hotplug**：

- `/sys/devices/system/memory/memory*/online`
- PVE 热加内存后，`free -h` 的 **total / available** 会变大

### 如何确认

```bash
# 虚拟机内（SSH 进 VM）
free -h
uptime -s

# PVE 宿主机
qm config <VMID> | grep -E '^memory|^balloon'
free -h
```

## 用 OpenTofu 改内存（示例）

变量 `k8s_51_memory_mib`（默认 **6144**）：

```hcl
variable "k8s_51_memory_mib" {
  type        = number
  description = "k8s-51 RAM in MiB (6GiB = 6144)"
  default     = 6144
}

resource "proxmox_virtual_environment_vm" "k8s_51" {
  # ...
  memory {
    dedicated = var.k8s_51_memory_mib
  }
}
```

应用：

```bash
cd homelab/opentofu/pve
tofu plan -target=proxmox_virtual_environment_vm.k8s_51
tofu apply -target=proxmox_virtual_environment_vm.k8s_51
```

`plan` 示例：`memory.dedicated = 8192 -> 6144`（缩容）或 `4096 -> 6144`（扩容）。

## 实践注意

1. **改完在虚拟机内看** `free -h`，在宿主机看 `free -h`，确认 guest 与 PVE 都合理。
2. **减内存**前：评估 CP/etcd；缩容后可能重启，观察 `kubectl get nodes`。
3. **K8s control-plane**：观察 VIP（如 `192.168.50.100`）、etcd、Grafana Node Readiness 看板。
4. **扩内存不要**对根分区执行 `growpart`（那是磁盘操作）。
5. **`balloon` 与 `memory` 分开管**：改内存用 OpenTofu；改 balloon 用 PVE UI / `qm set`，后续可再纳入 OpenTofu。

## 一次真实时间线（k8s-51 @ r86s）

1. 长期 **4GiB** + `balloon: 0` → CP 内存紧张，集群偶发 NotReady。
2. OpenTofu 调至 **8192**：虚拟机内约 7.7Gi，CP 压力缓解；r86s 上两台 K8s 合计约 14GiB，宿主机偏紧。
3. 统一 **`balloon: 0`** 前提下，将 k8s-51 调回 **6144**：与 k8s-50 各 6GiB，宿主机 available 明显改善。
4. 变更后可用 `uptime -s` 确认是否重启；持续用监控观察 NotReady / VIP 切换。

## 参考

- [PVE `qm.conf(5)` — balloon](https://pve.proxmox.com/pve-docs/qm.conf.5.html)
- Homelab：`homelab/opentofu/pve`（VM 内存纳管）
- Homelab：`homelab/k8s/RUNBOOK-k8s-51-recovery.md`（k8s-51 control-plane 恢复）
