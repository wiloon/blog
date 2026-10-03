---
title: "Helm Chart: Kubernetes 包管理"
author: "-"
date: 2018-11-24T11:27:20+00:00
lastmod: 2026-10-03T12:22:00+08:00
url: helm
categories:
  - Cloud
tags:
  - helm
  - k8s
  - argocd
  - remix
  - AI-assisted
---
## Helm 是什么

Helm 是 Kubernetes 的包管理器，地位类似 Linux 上的 pacman / apt。apt 安装的单位是 deb 包，Helm 安装的单位是 chart。

```bash
# archlinux
pacman -S helm

# macOS
brew install helm

# curl
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

## Chart 解决什么问题

在 K8s 里部署一个应用，需要的远不止一个镜像。以 Kong（API 网关 + Ingress Controller）为例，一次部署要创建这些资源：

- Deployment：跑 Kong 网关和 Ingress Controller 两个容器
- Service：proxy、admin、webhook 等多个
- ServiceAccount、ClusterRole、ClusterRoleBinding：Controller 要读集群里的 Ingress
- ValidatingWebhookConfiguration：校验用户提交的 Kong 资源
- Secret：webhook 用的 TLS 证书
- CRD：KongPlugin、KongConsumer 等自定义资源

手写这些 YAML 有几个问题：

1. 量大，资源之间互相引用（Service 的 selector 要对上 Pod 的 label，webhook 的 caBundle 要对上 Secret），手写容易错。
2. 每个用户的环境不一样：LoadBalancer IP、资源配额、是否开 TLS。直接改 YAML 的话，上游一更新就得重新合并一遍。
3. 升级、回滚没有统一的单位，只能一个个资源去改。

Chart 就是针对这几个问题的打包方式：上游维护者把这套 YAML 写成模板，把需要用户决定的部分抽成参数（values），打上版本号发布。用户只关心自己那几个参数。

## Chart 的结构

一个 chart 就是一个目录（发布时打成 `.tgz`）：

```text
kong/
├── Chart.yaml        # name, version, appVersion, dependencies
├── values.yaml       # default parameters
├── templates/        # Go templates that render to K8s manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ...
└── crds/             # CRDs, installed before templates
```

渲染过程是：`templates/` + 默认 `values.yaml` + 用户的 values 覆盖 → 一组普通的 K8s YAML。可以用 `helm template` 直接看渲染结果，不需要连集群：

```bash
helm repo add kong https://charts.konghq.com
helm template kong kong/kong --version 3.4.1 -n kong -f my-values.yaml
```

用户的 values 通常只有几十行，比如：

```yaml
proxy:
  loadBalancerIP: 192.0.2.10
resources:
  requests:
    cpu: 100m
    memory: 384Mi
```

## Chart 和镜像的关系

一个常见的误解是 chart 把几个镜像打包在一起。实际上 **chart 里不包含任何镜像**，它只是一堆 YAML 模板，镜像在模板里以 `image: 仓库:tag` 的形式被引用，运行时由节点自己去镜像仓库拉。

所以 chart 和镜像是两个独立发布、独立版本号的东西。`Chart.yaml` 里有两个版本字段：

| 字段 | 含义 | 例子 |
| ---- | ---- | ---- |
| `version` | chart 本身的版本，模板或默认值改了就升 | `3.4.1` |
| `appVersion` | 这个 chart 默认部署的应用版本，多数 chart 用它当默认镜像 tag | `3.9` |

几个推论：

1. 升级 chart 不一定升级镜像。Kong chart 从 2.52.0 升到 3.4.1，跨了一个大版本，但渲染出来的镜像仍然是 `kong:3.9` 和 `kong/kubernetes-ingress-controller:3.5`，变化的只是模板写法和 webhook 配置。
2. 反过来也成立：chart 的小版本升级可能只是把默认镜像换了。Loki chart 6.55.0 → 7.3.0 渲染结果的唯一实质差异是 `grafana/loki:3.6.7` → `3.6.11`。
3. 镜像版本可以和 chart 解耦：大多数 chart 允许在 values 里覆盖 `image.tag`，锁定镜像而单独升级 chart，或者反过来。
4. chart 的大版本号（major）表示模板或 values 有不兼容变化，不代表应用本身有大版本变化。升 major 前要看 chart 的 CHANGELOG / UPGRADE 文档，而不是应用的 release notes。

一个 chart 引用多个镜像很常见（Kong 引用两个，Loki 单机模式引用 Loki 本体和一个 sidecar）。chart 保证的是这几个镜像的版本组合经过上游测试、能配合工作；这也是一起升级省事的原因。但这个"组合"是写在模板里的引用关系，不是打包关系。

## Release：安装后的实例

chart 是模板，release 是用某组 values 安装到集群里的一个实例。同一个 chart 可以在不同 namespace 装多个 release。

```bash
helm install kong kong/kong -n kong -f my-values.yaml
helm upgrade kong kong/kong -n kong --version 3.4.1 -f my-values.yaml
helm list -n kong
helm history kong -n kong
helm rollback kong 3 -n kong   # back to revision 3
```

Helm 把每次安装或升级的渲染结果存成 namespace 里的一个 Secret（`sh.helm.release.v1.<name>.v<N>`），回滚就是把之前某个版本的渲染结果重新 apply。

## 与 Argo CD 搭配

用 Argo CD 部署 chart 时，Argo CD 只借用 Helm 的渲染能力：它内部执行相当于 `helm template` 的操作，把结果当普通 YAML 去同步，不会调用 `helm install`。因此：

- `helm list` 看不到这些应用，回滚走 Argo CD 或 git revert，而不是 `helm rollback`。
- chart 版本写在 Application 的 `targetRevision`，values 文件放在自己的 git 仓库里，两者都受版本控制。
- Renovate 这类工具可以监控 `targetRevision`，有新 chart 版本时自动开 PR。

```yaml
sources:
  - repoURL: https://charts.konghq.com
    chart: kong
    targetRevision: "3.4.1"
    helm:
      valueFiles:
        - $values/k8s/kong/values.yaml
```

更多见 [Argo CD 与 GitOps 持续部署](../cloud/argocd.md)。

## Chart 的维护者可以和应用不同

chart 是独立的发布物，维护者不一定是应用的开发者，也可能中途换人。一个例子是 Loki：2026 年 3 月起，面向开源用户的 Loki chart 从 `grafana/helm-charts` 迁到了社区维护的 `grafana-community/helm-charts`（从 chart 6.55.0 分叉），原仓库里的 `grafana/loki` chart 从 7.x 开始只为企业版 Grafana Enterprise Logs 维护。

这时 Loki 镜像本身仍然是同一个开源镜像，变化的只是"谁来维护模板"。如果继续跟着原仓库升级，渲染结果短期内可能没差别，但长期会偏向企业版的默认值。开源用户应当把 chart 来源（`repoURL`）换到社区仓库。

所以选 chart 时除了看版本，还要看 chart 仓库是谁在维护：应用官方、社区组织（如 grafana-community），还是个人。

## 升级 chart 前的检查

```bash
# list available chart versions
helm search repo grafana-community/loki --versions | head

# show default values of the target version
helm show values kong/kong --version 3.4.1

# render old and new with the same values, then diff
helm template kong kong/kong --version 2.52.0 -f values.yaml > old.yaml
helm template kong kong/kong --version 3.4.1  -f values.yaml > new.yaml
diff old.yaml new.yaml
```

diff 时重点看：

- `image:` 行，确认镜像有没有变
- StatefulSet 的 `selector`、`serviceName`、`volumeClaimTemplates`，这些字段不可修改，变了就要先删 StatefulSet 再重建
- CRD 变化，很多 chart（如 Longhorn）要求手动先 apply CRD
- 新增或删除的资源

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-03 | 标题改为 `Helm Chart: Kubernetes 包管理`；分类 Inbox → Cloud；补充 chart 结构、chart 与镜像的关系、release、Argo CD 搭配、chart 维护者变更、升级检查 | 原文只有安装命令，补充 chart 概念说明 |
