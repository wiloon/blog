---
title: "Kubernetes Operator and CRD"
author: "-"
date: 2026-07-13T08:50:03+08:00
lastmod: 2026-07-13T08:50:03+08:00
url: operator-crd
categories:
  - Cloud
tags:
  - k8s
  - operator
  - crd
  - remix
  - AI-assisted
---

## 要解决什么问题

Kubernetes 内置资源（Pod、Deployment、Service、PVC 等）描述的是通用计算、网络和存储。很多平台组件有自己的领域对象，例如：

- 证书：Certificate、Issuer
- 监控规则：PrometheusRule、ServiceMonitor
- 存储卷内部状态：Longhorn 的 Volume、Replica
- GitOps 应用：Argo CD 的 Application
- CI 流水线：Tekton 的 Task、Pipeline、PipelineRun

这些概念没法用 Deployment 直接表达。Kubernetes 提供的扩展方式是：先用 **CRD** 注册新的资源类型，再用 **控制器（Controller）** 持续把这些对象驱动到期望状态。两者合在一起，就是常说的 **Operator 模式**。

## CRD 与 CR

| 概念 | 全称 | 角色 |
| ---- | ---- | ---- |
| CRD | CustomResourceDefinition | 类型定义：叫什么名字、属于哪个 API group、有哪些字段 |
| CR | Custom Resource | 按该类型创建的具体实例 |

类比：CRD 像 Go 里的 `type` / `struct` 定义，CR 是这个类型的一个值。

注意分工：

- Kubernetes **内置**资源（Pod、Deployment、PVC 等）不是用 CRD 实现的。
- CRD 是给**外部/第三方**（以及自己）注册新资源**类型**的扩展口。
- apply 一批 CRD 之后，API Server 只是「认识」这些类型，能接收、校验、存贮、查询对应对象；**不会**因此去调用 Operator。

安装 Longhorn、cert-manager、kube-prometheus-stack 等组件时，通常会先（或一并）把一批 CRD 注册进集群。之后就可以：

```bash
# 列出已注册的 CRD
kubectl get crd

# 按 API group 过滤（示例）
kubectl get crd | grep cert-manager.io
kubectl get crd | grep longhorn.io
kubectl get crd | grep monitoring.coreos.com

# 像内置资源一样操作 CR
kubectl get certificate -A
kubectl get application -n argocd
kubectl get prometheusrule -A
```

`kubectl api-resources` 里也能看到这些自定义类型，说明它们已经进入 Kubernetes API。

## 控制器与 reconcile

Kubernetes 自身大量使用控制器：Deployment Controller、StatefulSet Controller 等跑在 `kube-controller-manager` 里。核心循环是：

```text
observe current state
  → compare with desired state
  → act until they match
  → repeat
```

例如声明 Deployment `replicas: 3`，控制器发现只有 2 个 Pod，就会再创建一个。

Operator 把同一套思路用到**领域对象**上：你声明「我要一张证书 / 一条告警规则 / 一次流水线运行」，控制器负责创建底层 Pod、Secret、Service 等，并在失败时重试或自愈。

## Operator = CRD + Controller

更准确一点：

1. **CRD**：告诉 API Server「集群里多了一种资源」。
2. **Controller / Operator**：watch 这类资源，执行运维逻辑。
3. （可选）Webhook：校验或改写 CR 字段。

没有控制器的 CRD 只是存了一份 YAML 到 etcd，不会自动干活。没有 CRD 的控制器也可以写，但无法用 `kubectl apply` 声明领域对象，生态集成也差一截。

因果方向：

```text
CRD 定类型（模具）
  → 某条路径产出 CR（订单 / 实例）
  → Operator watch CR 的增删改并 reconcile
  → 落地真实资源（卷、副本、Secret……）
```

不是「k8s 读完 CRD 后调用 Operator」，而是 Operator **自己跑着订阅** API；有 CR（或 CR 变化）才干活。

创建 CR 的常见来源：

| 来源 | 例子 |
| ---- | ---- |
| 人直接 apply | `kubectl apply` 一份 `Certificate` / `Application` |
| 组件代写 CR | 建 Longhorn StorageClass 的 PVC → CSI provisioner 创建 Volume 等 CR |
| UI / 其它控制器 | Longhorn UI、上层平台写同一套 CR |

Operator 不止监听「创建」，**更新、删除**也会进入同一套 reconcile。

### 典型流程一：直接声明 CR（证书）

```text
kubectl apply -f my-certificate.yaml   # kind: Certificate
        ↓
cert-manager controller 看到新 CR
        ↓
向 Issuer 申请证书、写入 Secret、续期
```

用户面对的是领域语言（Certificate），底层 Secret 由 Operator 维护。

### 典型流程二：PVC → CSI → CR（Longhorn）

这是 homelab 里用 Longhorn 最常见的路径：

```text
1. 安装 Longhorn 时 apply 其 CRD
   → 集群注册 Volume、Replica 等类型

2. 用户创建 StorageClass 为 longhorn 的 PVC
   → Longhorn CSI provisioner 按 CRD 创建对应 CR（不是 API Server 自己 invent）

3. Longhorn Operator 监听到 CR 变化
   → 按 CR 落地卷 / 副本等

4. PVC Bound，Pod 可挂载
```

可以记成：**CRD = 模具；CR = 订单；Operator = 接单落地。**  
下单的不一定是 Longhorn 自己——PVC/CSI、人或 UI 都可以创建 CR。

## 最小例子：声明一张证书

下面是 cert-manager 风格的 CR（字段示意，具体以集群里的 Issuer 为准）：

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-tls
  namespace: default
spec:
  secretName: example-tls-secret
  issuerRef:
    name: ca-issuer
    kind: ClusterIssuer
  dnsNames:
    - example.wiloon.com
```

含义：

- `kind: Certificate` 不是内置资源，来自 `certificates.cert-manager.io` 这个 CRD。
- `spec` 写期望状态：证书写到哪个 Secret、用哪个 Issuer、覆盖哪些域名。
- cert-manager Operator 负责申请、写入 Secret、到期续期。

同类例子：

| CR | 谁在处理 | 结果 |
| -- | -------- | ---- |
| `Application`（Argo CD） | Argo CD controller | 按 Git 路径同步到集群，见 [Argo CD](./argocd.md) |
| `PipelineRun`（Tekton） | Tekton controller | 拉起一组 Task Pod 跑 CI，见 [Tekton 与 Kaniko](./tekton-kaniko.md) |
| `PrometheusRule` | Prometheus Operator | 生成/更新 Prometheus 告警规则 |
| `KongPlugin` | Kong Ingress Controller | 把插件配置挂到 Ingress / Service |

## 和「直接写 Deployment」的差别

| 方式 | 你写什么 | 谁保证状态 |
| ---- | -------- | ---------- |
| 普通应用 | Deployment、Service、Ingress | Deployment Controller 管副本；其它运维靠人或脚本 |
| Operator | 领域 CR（Certificate、Application…） | Operator 管申请证书、同步 Git、扩缩存储副本等 |

业务应用（例如 RSSX、ENX）通常仍用 Deployment + PVC + Ingress。平台组件则用 Operator 把复杂运维编码进控制器。两者常同时存在：业务 YAML 简单，证书、存储、监控、GitOps 交给 Operator。

## Homelab 里常见的对应关系

在 homelab 集群里，平台层大量依赖 Operator / CRD；业务应用多半不写自研 Operator，但会消费这些 CR：

| 组件 | 模式 | 常见 CR / 说明 |
| ---- | ---- | -------------- |
| Longhorn | 存储 Operator | Volume、Replica、Setting；常见路径是 PVC → CSI 写 CR → Operator 落地卷/副本 |
| cert-manager | 证书 Operator | Certificate、ClusterIssuer（如 `ca-issuer`） |
| kube-prometheus-stack | Prometheus Operator | Prometheus、PrometheusRule、ServiceMonitor |
| Tekton | CI Operator | Task、Pipeline、PipelineRun |
| Argo CD | GitOps 控制器 | Application |
| Kong Ingress Controller | Ingress 控制器 | KongPlugin、KongConsumer 等 |
| Calico / Tigera | 网络 | 网络策略与安装相关 CR |

业务侧常见写法：Deployment 管进程；PVC 用 Longhorn StorageClass；Ingress 走 Kong；需要证书时写 Certificate 或复用已有 TLS Secret；用 Argo CD Application 做 GitOps 同步。

## 运维时要注意的几点

### 删 CRD 会级联删 CR

卸载组件时如果删掉 CRD，该类型下的所有 CR 通常也会被删掉。数据面是否还在，取决于组件实现（有的卷数据仍在磁盘，有的配置只活在 CR 里）。升级或卸载前先确认 CRD 策略。

### Helm / Argo CD 常单独管 CRD

CRD 体积大、字段会被 API Server 注入很多（尤其 `.status`），容易造成持续 OutOfSync。常见做法：

- Helm / Argo CD：`skipCrds: true`，运行时资源交给 GitOps，CRD 首次安装或升级时手动 `kubectl apply`
- 升级顺序：先 apply 新版 CRD，再升 Operator / chart 版本

Longhorn、kube-prometheus-stack 在 Argo CD 里常见这种拆分。

### 看不懂时先分清「类型」和「实例」

```bash
# 类型在不在
kubectl get crd certificates.cert-manager.io

# 实例有哪些
kubectl get certificate -A

# 控制器是否在跑
kubectl get deploy -n cert-manager
kubectl get pods -n cert-manager
```

CR 一直 Pending / 无事件，优先查对应 namespace 里的 Operator Pod 日志，而不是只盯业务 Deployment。

## 和相关文章的关系

- Kubernetes 基础对象与控制器概览：[k8s](./k8s.md)
- Argo CD 的 Application CR：[Argo CD](./argocd.md)
- Tekton 用 CRD 描述流水线：[Tekton 与 Kaniko](./tekton-kaniko.md)
- Kong Ingress：[Kong](./kong.md)

## 小结

1. **CRD** 向集群注册外部资源**类型**；内置 Pod/Deployment 不是靠 CRD 实现的。
2. **CR** 是按该类型创建的**实例**；谁创建 CR，常见是人、UI 或 CSI 等组件，不是「读完 CRD 就自动生出来」。
3. **Operator** watch CR 的变化并 reconcile；k8s 不会在加载 CRD 后主动去「调用」Operator。
4. Longhorn 示例：`apply CRD` → 建 longhorn PVC → CSI 写 Volume 等 CR → Operator 落地卷/副本。
5. 业务应用可以继续用 Deployment；证书、存储、监控、CI、GitOps 等平台能力，多半已经以 Operator 形式跑在集群里。
