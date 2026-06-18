---
title: Kubernetes Descheduler 与 Pod 重平衡
author: "-"
date: 2026-06-18T15:35:08+08:00
lastmod: 2026-06-18T15:35:08+08:00
url: kubernetes-descheduler
categories:
  - cloud
tags:
  - k8s
  - kubernetes
  - descheduler
  - remix
  - AI-assisted
---

## 背景

Kubernetes **默认调度器**只在 Pod **创建时**选一次节点。Pod 一旦跑起来，除非被删除、驱逐或所在节点不可用，否则**不会**因为目标节点变忙而自动迁走。

homelab 里曾出现 worker 节点（如 k8s-50）堆了三十多个 Pod，而另一节点几乎空闲的情况。当时节点内存压力指标仍为 `MemoryPressure=False`（kubelet 认为内存够用），但 CPU 争抢、有状态服务启动慢等问题已经很明显。手动 `kubectl drain` 后 Pod 能正常分散到其他节点，说明调度器本身没问题，缺的是**主动重平衡**机制。

[Descheduler](https://github.com/kubernetes-sigs/descheduler) 是 Kubernetes SIG 维护的组件，周期性检查集群，按策略**驱逐**部分 Pod，让它们被默认调度器重新分配到更合适的节点。

## 调度器与 Descheduler 的分工

| 组件 | 时机 | 作用 |
| ---- | ---- | ---- |
| **kube-scheduler** | Pod 创建 / 被驱逐后重建 | 为新 Pod 选节点 |
| **Descheduler** | 周期性（如每 10 分钟） | 发现「不均衡」或「违反策略」的 Pod，发起驱逐 |
| **kubelet eviction** | 节点资源真不足时 | 按优先级驱逐 Pod（OOM、磁盘满等） |

三者互补：调度器负责「进门放哪」，Descheduler 负责「住久了要不要换房」，kubelet 负责「房子快塌了先赶人」。

## 什么时候需要 Descheduler

适合考虑部署的场景：

- 多个 worker 长期负载不均，某些节点 Pod 特别多、另一些很空
- 扩过节点内存或新加 worker 后，希望存量 Pod 逐步分散（调度器不会自动做这件事）
- 配置了 `podAntiAffinity` / `topologySpreadConstraints`，但历史 Pod 是在规则加入之前创建的
- 希望低利用率节点上的 Pod 被迁走，便于维护或省电

**不能指望 Descheduler 单独解决的问题：**

- DaemonSet Pod（每个节点必须有一份，无法迁走）
- 绑定了 `nodeSelector` / `nodeAffinity` 的 Pod（如只允许在特定 Longhorn 节点上跑的服务）
- StatefulSet + RWO PVC：卷挂在哪个节点，Pod 通常只能跟过去（除非卷 detach 后再 attach 到新节点）
- control-plane 节点的 `NoSchedule` 污点：普通 Pod 本就不能上去

## homelab 里常见的调度限制（与 Descheduler 无关）

即使装了 Descheduler，以下因素仍会限制 Pod 能去哪些节点：

1. **control-plane 污点**：`node-role.kubernetes.io/control-plane:NoSchedule`，三个 control-plane 不接普通工作负载
2. **Longhorn 存储节点**：只有部分 worker 参与 Longhorn，带 PVC 的 Pod 受卷副本与 `volume.kubernetes.io/selected-node` 等约束
3. **显式 nodeAffinity**：例如 Nexus 限制在 `k8s-50` / `k8s-71`
4. **资源 requests**：Pod 未设 requests 时，调度器打分依据较弱，容易随机堆在一处

Descheduler 只能驱逐**允许**被调度到其他节点的 Pod；上述硬约束不变。

## 安装方式（Helm）

官方 chart 在 [kubernetes-sigs/descheduler](https://github.com/kubernetes-sigs/descheduler/tree/master/charts/descheduler)。

```bash
helm repo add descheduler https://kubernetes-sigs.github.io/descheduler/
helm repo update

helm upgrade --install descheduler descheduler/descheduler \
  --namespace kube-system \
  --create-namespace
```

默认以 **CronJob** 形式周期性运行（常见为每 10 分钟一次 Job），无需常驻 Deployment。

## 常用策略

通过 ConfigMap / Helm `values.yaml` 中的 `deschedulerPolicy` 配置。常见策略包括：

| 策略 | 作用 |
| ---- | ---- |
| `LowNodeUtilization` | 低利用率节点上的 Pod 迁到高利用率节点，缓解冷热不均 |
| `RemovePodsViolatingInterPodAntiAffinity` | 清理违反 Pod 间反亲和的 Pod |
| `RemovePodsViolatingTopologySpreadConstraint` | 清理违反拓扑分布约束的 Pod |
| `RemoveDuplicates` | 同一节点上运行了多个同 ReplicaSet 副本时驱逐多余的 |

`LowNodeUtilization` 示例（需根据集群调整阈值）：

```yaml
apiVersion: descheduler/v1alpha2
kind: DeschedulerPolicy
profiles:
  - name: default
    pluginConfig:
      - name: LowNodeUtilization
        args:
          thresholds:
            cpu: 20
            memory: 20
            pods: 20
          targetThresholds:
            cpu: 50
            memory: 50
            pods: 50
    plugins:
      deschedule:
        enabled:
          - LowNodeUtilization
```

阈值含义简述：`thresholds` 以下视为「低利用率节点」候选迁出；`targetThresholds` 以上视为「高利用率节点」不再迁入。

## 与 cordon / drain 的关系

| 操作 | 触发方 | 场景 |
| ---- | ------ | ---- |
| `kubectl cordon` + `drain` | 人工 | 节点维护、重启、换硬件前的一次性清空 |
| Descheduler | 自动、周期性 | 日常负载均衡，无需停机 |

维护窗口仍应使用 `drain`；Descheduler 不能替代有计划的下线流程。

## 部署前注意

1. **先设 Pod `resources.requests`**，否则利用率策略缺乏可靠依据
2. **有状态服务**驱逐会触发重建，确认 PVC 可在目标节点 attach（Longhorn 多副本卷通常可以，单副本需谨慎）
3. **PDB（PodDisruptionBudget）** 会限制同时驱逐的数量，避免一次赶走过多副本
4. **从保守策略开始**，观察几轮 CronJob 日志再逐步加大力度
5. homelab 若未安装 Descheduler，可先用 `kubectl top nodes` + `kubectl get pods -A -o wide --field-selector spec.nodeName=<node>` 人工巡检

## 相关阅读

- [k8s](./k8s.md) — cordon、drain、DaemonSet 等基础概念
- [PVC 访问模式：RWO 简介](./pvc-access-modes.md) — 有状态 Pod 与节点绑定
- [Proxmox VE 虚拟机内存热扩容](./pve-vm-memory-hotplug.md) — worker 节点内存规划
