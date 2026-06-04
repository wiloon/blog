---
title: Kubernetes Kustomize 基础
author: "-"
date: 2026-06-04T20:09:34+08:00
lastmod: 2026-06-04T20:09:34+08:00
url: kustomize
categories:
  - Cloud
tags:
  - k8s
  - kustomize
  - remix
  - AI-assisted
---

## Kustomize 是什么

[Kustomize](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/) 是 Kubernetes 自带的配置管理工具：在**不修改原始 YAML 文件**的前提下，用一个小文件 `kustomization.yaml` 声明「要部署哪些资源、统一加什么 namespace/标签、如何做补丁」，`kubectl` 会先合并再 apply。

和 Helm 的分工可以这样理解：

| 方式 | 特点 | 常见场景 |
| ---- | ---- | -------- |
| 纯 YAML + `kubectl apply -f` | 最直接，改多个文件时要自己记顺序 | 单文件、临时试验 |
| **Kustomize** | 无模板语言，补丁基于 YAML；`kubectl apply -k` 内置 | homelab 自写 manifest、按目录组织服务 |
| **Helm** | Chart + values，适合第三方发行版 | `kube-prometheus-stack`、Nexus 等上游 Chart |

Kustomize 从 Kubernetes 1.14 起并入 `kubectl`，一般**不需要**单独安装 `kustomize` 二进制（旧文档里的独立 CLI 仍可用，但日常 `kubectl apply -k` 即可）。

## 最小目录结构

一个可部署单元通常是一个目录，根上有 `kustomization.yaml`，旁边放各资源的 YAML：

```text
blog-stats/
├── kustomization.yaml
├── namespace.yaml
├── configmap.yaml
├── secret.yaml
└── cronjob.yaml
```

`kustomization.yaml` 只列出要包含的文件（路径相对本目录）：

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - namespace.yaml
  - configmap.yaml
  - secret.yaml
  - cronjob.yaml
```

部署：

```bash
kubectl apply -k homelab/k8s/blog-stats/
```

等价于对合并后的 manifest 执行一次 `kubectl apply`；Kustomize 负责生成那份合并结果。本地只想看合并结果、不写入集群时：

```bash
kubectl kustomize homelab/k8s/blog-stats/
```

## 常用字段

### `resources`

必填（或改用 `bases` / `components` 等高级写法）。列出的每个条目可以是单个 YAML 文件，也可以是**另一个**带 `kustomization.yaml` 的子目录（嵌套 base）。

### `namespace`

给本层所有资源统一设置 `metadata.namespace`，避免每个文件重复写：

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: kube-prometheus-stack

resources:
  - prometheus/additional-scrape-configs.yaml
  - prometheus/blackbox-exporter.yaml
  - ingress-prometheus-remote-write.yaml
```

适合「同一目录下多份清单都进同一个命名空间」的场景；若某资源 YAML 里已经写了 `namespace`，以 Kustomize 合并规则为准（通常由 `kustomization.yaml` 覆盖或补齐）。

### `commonLabels` / `labels`

给所有资源加上统一标签，便于筛选、配合 ServiceMonitor 等：

```yaml
commonLabels:
  app.kubernetes.io/part-of: observability
```

### `patches` / `patchesStrategicMerge`

在不复制整份 Deployment 的情况下改片段，例如改镜像 tag、加环境变量、改副本数。战略合并补丁（`patchesStrategicMerge`）适合小改动；复杂条件可用 JSON6902 / RFC6902 风格的 `patches`。

### `images`

批量替换镜像名与 tag，适合 CI 只改 tag、不改完整 Deployment：

```yaml
images:
  - name: my-app
    newTag: v1.2.3
```

### `configMapGenerator` / `secretGenerator`

从文件生成 ConfigMap/Secret，并自动加内容哈希后缀，减少「只改 ConfigMap 却未触发滚动」的问题（需与 Deployment 的 name 引用方式配合）。

## 与 `kubectl apply -f` 的区别

| 命令 | 行为 |
| ---- | ---- |
| `kubectl apply -f dir/` | 按文件名顺序 apply 目录下**所有** YAML，**不会**读 `kustomization.yaml` |
| `kubectl apply -k dir/` | 先执行 Kustomize build，再 apply **合并后的** 清单 |

若目录里有 `kustomization.yaml`，应使用 **`-k`**，否则 `namespace`、补丁、生成器都不会生效。

删除资源时也有对应写法：`kubectl delete -k <目录>` 会按当前 build 结果删除（仍受 `--prune` 等行为约束，生产前先在测试命名空间验证）。

## homelab 中的用法

配置仓库 `w10n-config` 里，不少服务按目录 + Kustomize 管理，例如：

- `homelab/k8s/blog-stats/`：CronJob + ConfigMap + Secret，每日拉取博客统计写入 PostgreSQL
- `homelab/k8s/observability/`：Prometheus 额外抓取、Blackbox、自写 `PrometheusRule`、Ingress 等，用顶层 `namespace: kube-prometheus-stack` 统一命名空间

日常变更流程通常是：改 YAML → `kubectl apply -k <目录>` → 用 `kubectl get` / `logs` 验证。这与 [Argo CD 与 GitOps 持续部署](./argocd.md) 里「Git 为事实来源」可以并存：Argo 同步的 path 也可以是 Kustomize 目录，由 Argo 在服务端执行 `kustomize build` 再 apply。

若资源已由 Argo CD 管理，长期用本机 `kubectl apply -k` 旁路修改会导致 **OutOfSync**，可能与 selfHeal 互相覆盖；应急与正路对比见 [Argo CD CLI 与 kubectl annotate 对比](./argocd-cli-vs-kubectl-annotate.md)。

## 和 Helm 如何配合

二者不必二选一。常见组合：

- **Helm 装上游栈**（监控、Ingress Controller），values 只覆盖必要项
- **Kustomize 管自写清单**（业务 Deployment、CronJob、自研告警规则），目录进 Git，用 `apply -k` 或 Argo 同步

不建议对**同一份** Deployment 既用 Helm 又用 Kustomize 叠加 patch，除非清楚 release 名与对象归属，否则升级 Chart 时容易覆盖手工补丁。

## 适用与不适用

**适合：**

- 清单数量适中、以静态 YAML 为主
- 需要按环境（dev/staging/prod）做少量差异（`overlays/` 目录是官方推荐模式）
- 希望 diff 直观、不引入 Helm 模板语法

**不太适合：**

- 强依赖第三方 Chart 的参数组合（直接用 Helm 更省事）
- 需要复杂模板逻辑（可考虑 Helm 或外部生成器写 YAML 再 kustomize）

## 延伸阅读

- 官方导读：[Introduction to Kustomize](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/)
- 多环境结构：[Bases and Overlays](https://kubectl.docs.kubernetes.io/guides/config_management/bases_and_variants/)
- 集群概念总览：[k8s](./k8s.md)；GitOps 部署：[Argo CD 与 GitOps 持续部署](./argocd.md)
