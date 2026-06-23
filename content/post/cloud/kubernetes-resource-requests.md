---
title: Kubernetes Resource Requests: 调度与 Descheduler 在算什么
author: "-"
date: 2026-06-23T11:14:01+08:00
lastmod: 2026-06-23T11:14:01+08:00
url: kubernetes-resource-requests
categories:
  - cloud
tags:
  - k8s
  - kubernetes
  - descheduler
  - remix
  - AI-assisted
---

## 问题从哪来

homelab 里 k8s-50 在 Grafana 上 CPU 一度接近 80%，但 [Descheduler](./kubernetes-descheduler.md) 每 15 分钟跑一轮，日志里始终是 `evictedPods=0`。排查后发现：Grafana 看的是节点上**真实 CPU 占用**，而调度器和 Descheduler 的 `LowNodeUtilization` 看的是各 Pod 的 **`resources.requests` 之和**占节点可分配量的比例。两者不是同一套数。

本文说明 `requests` / `limits` 分别做什么、为什么没写 requests 会让 Descheduler「看不见」热点，以及 homelab 里我们补 requests 时在干什么。

## requests、limits、实际用量，三套数

| 概念 | 谁在用 | 含义 |
| ---- | ------ | ---- |
| **requests** | kube-scheduler、Descheduler `LowNodeUtilization` | Pod 向集群「预订」的 CPU/内存；调度时保证节点剩余可分配量 ≥ 各 Pod requests 之和 |
| **limits** | kubelet、cgroup | Pod 允许使用的上限；CPU 可被节流，内存超限可能 OOMKill |
| **实际用量** | `kubectl top`、node_exporter、Grafana | 进程此刻真正吃掉的资源 |

可以粗浅理解成：

- **requests**：订座（调度与重平衡的依据）
- **limits**：包厢上限（运行时保护）
- **实际用量**：现场人数（监控里看到的负载）

没写 `requests` 时，在调度器眼里该容器预订为 **0**；它仍可能把 CPU 跑满，但**不会**抬高节点在 Descheduler 中的「利用率」。

## 调度器怎么用 requests

Pod 创建时，kube-scheduler 会过滤掉「剩余可分配 CPU/内存不够装下这个 Pod requests」的节点，再在候选节点上打分。requests 越准，Pod 越不容易被随机堆到同一台 worker。

没 requests 的 Pod 对调度器几乎「零成本」，容易在创建时落到已有 Pod 较多的节点（尤其配合 `ScheduleAnyway` 的拓扑分布时），之后也不会因为节点变忙而自动迁走——除非装 [Descheduler](./kubernetes-descheduler.md) 且节点在 requests 维度上真的「超阈值」。

## Descheduler 怎么用 requests

`LowNodeUtilization` 对每个节点算：

```text
利用率% = 该节点所有 Pod 的 requests 之和 ÷ 节点 allocatable
```

（CPU、内存、Pod 个数各算一条，再与阈值比较。）

homelab 当前阈值（`infra/homelab/k8s/descheduler/values.yaml`）：

| 参数 | 值 | 含义 |
| ---- | -- | ---- |
| `thresholds` | 25% | 三项**都**低于此 → 低利用率节点，可接收迁来的 Pod |
| `targetThresholds` | 60% | **任一项**高于此 → 高利用率节点，可能被迁出 Pod |

2026-06-23 某轮日志里 k8s-50 在 Descheduler 眼中是 `cpu=42%, memory=33%, pods=31%`，归类为 **appropriately utilized**；而 Grafana 上同一时刻 CPU 实际已远高于此。原因就是大量 Pod 未声明 requests，或 requests 远低于真实负载（例如 Nexus 订了 500m CPU 但实际可跑 500m+）。

因此：**先补 requests，再指望 Descheduler 按负载重平衡**；顺序不能反。

## homelab 正在补什么

仓库里已用 `kubectl top` 对过一轮，优先给 **Git 管理的、常驻且缺 requests 的 workload** 补值，例如 Argo CD（`infra/homelab/k8s/argocd/resource-requests-patch.yaml`）：

| 组件 | requests（示例） | 依据 |
| ---- | ---------------- | ---- |
| `argocd-application-controller` | 200m CPU / 768Mi | 常态 ~700Mi 内存 |
| `argocd-repo-server` | 50m / 256Mi | helm 渲染与 git 操作 |
| `argocd-redis` | 50m / 64Mi | 轻量缓存 |
| 其他 Argo CD Deployment | 50m / 64–128Mi | 控制面余量 |

Prometheus / Grafana 等在 `kube-prometheus-stack/values.yaml` 里已有 requests 注释与取值。Kong、Tekton 等若由集群外 Helm 安装、未进本仓库，需在对应 values 里同样补上，否则 Descheduler 仍会把它们当 0。

补 requests 的目的不是限流，而是让 **调度与 Descheduler 的账本** 接近真实负载；补完后 k8s-50 在 Descheduler 里的 CPU requests 占比会上升，才更可能触发 `LowNodeUtilization` 迁出。

## 怎么设一个合理的 requests

实用做法：

1. 用 `kubectl top pods -n <ns>` 看常态 CPU/内存（避开刚启动的尖峰）。
2. requests 取常态的 **1.2–1.5 倍** 留余量，不必等于 limits。
3. CPU 可先用 `50m`、`100m`、`200m` 这类档位；内存按 `64Mi`、`128Mi`、`256Mi` 递增。
4. 改完后 `kubectl describe node <node>` 看 **Allocated resources** 是否与预期一致。
5. 等一两轮 Descheduler CronJob，查日志是否出现 `overutilized` 与 `evictedPods>0`。

示例：

```yaml
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    memory: 512Mi
```

limits 可以只设内存（CPU 不设 limit 时多为可突发），但 **requests 建议成对写上**。

## 与 Grafana / kubectl top 的对照

| 你想知道 | 看什么 |
| -------- | ------ |
| 节点现在忙不忙 | Grafana、`kubectl top nodes` |
| 调度器认为节点满不满 | `kubectl describe node` → Allocated resources |
| Descheduler 会不会动 | CronJob 日志里的 `usagePercentage` 与 `overutilized` |
| 哪个 Pod 该补 requests | `kubectl top pods` + 对比 manifest 里是否 `<none>` |

## 相关阅读

- [Kubernetes Descheduler 与 Pod 重平衡](./kubernetes-descheduler.md) — 策略、阈值、PVC 与 nodeAffinity 限制
- [k8s](./k8s.md) — cordon、drain、DaemonSet
- [PVC 访问模式：RWO 简介](./pvc-access-modes.md) — 有状态 Pod 与卷挂载
