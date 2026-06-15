---
title: Kubernetes Reflector：跨 namespace 自动同步 Secret 和 ConfigMap
author: "-"
date: 2026-06-14T21:24:31+08:00
lastmod: 2026-06-14T21:24:31+08:00
url: kubernetes-reflector
categories:
  - cloud
tags:
  - k8s
  - cert-manager
  - tls
  - remix
  - AI-assisted
---

在多 namespace 的 Kubernetes 集群里，TLS Secret、镜像拉取凭据、配置文件等资源经常需要在多个 namespace 里保持相同的内容。Secret 不能直接跨 namespace 引用，传统做法是手动 `kubectl` 复制，或者写脚本定时同步——两种方式都有维护成本和容易遗漏的问题。

[Kubernetes Reflector](https://github.com/emberstack/kubernetes-reflector) 是一个轻量级的 controller，专门解决这个问题：在源资源（Secret 或 ConfigMap）上添加几个注解，它就会自动把资源同步到指定的 namespace，并在源资源更新时同步更新所有副本。

## 典型使用场景

### TLS 通配符证书跨 namespace 分发

cert-manager 只在一个 namespace 签发证书，但多个 namespace 的 Ingress 都需要引用同一份 TLS Secret。

```
default/wiloon-tls-secret  ──Reflector──▶  argocd/wiloon-tls-secret
                                       ──▶  nexus/wiloon-tls-secret
                                       ──▶  rssx/wiloon-tls-secret
                                       ──▶  ...
```

### 镜像拉取凭据（ImagePullSecret）

私有镜像仓库的登录凭据需要在所有运行业务 Pod 的 namespace 里都存在。

## 安装

```bash
helm repo add emberstack https://emberstack.github.io/helm-charts
helm repo update
helm upgrade --install reflector emberstack/reflector \
  --namespace kube-system
```

或者用 ArgoCD Application 管理：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: reflector
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://emberstack.github.io/helm-charts
    chart: reflector
    targetRevision: "8.x"
  destination:
    server: https://kubernetes.default.svc
    namespace: kube-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## 注解说明

在**源 Secret / ConfigMap** 上添加注解来控制同步行为：

```yaml
metadata:
  annotations:
    # 允许被反射（必填）
    reflector.v1.k8s.emberstack.com/reflection-allowed: "true"

    # 允许同步到哪些 namespace（逗号分隔，支持正则）
    reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "argocd,nexus,rssx"

    # 自动在目标 namespace 创建（无需目标 namespace 显式声明接收）
    reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true"

    # 自动同步到哪些 namespace（留空则同步到 reflection-allowed-namespaces）
    reflector.v1.k8s.emberstack.com/reflection-auto-namespaces: "argocd,nexus"
```

`reflection-auto-enabled: "true"` 时，Reflector 主动推送——目标 namespace 不需要做任何操作，Secret 自动出现。这是最省事的模式，适合通配符 TLS 证书这类"所有 namespace 都需要"的场景。

## 与 cert-manager 结合使用

在 `default` namespace 签发通配符证书，通过 Reflector 同步到其他 namespace：

```yaml
# Certificate（default namespace）
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: wildcard-cert
  namespace: default
spec:
  secretName: wiloon-tls-secret
  commonName: "*.wiloon.lab"
  dnsNames:
    - "*.wiloon.lab"
  duration: 8760h
  renewBefore: 720h
  issuerRef:
    kind: ClusterIssuer
    name: ca-issuer
```

cert-manager 签发后，Secret `wiloon-tls-secret` 会自动创建。推荐在 `Certificate` CR 的 `secretTemplate` 里预先定义注解，这样 cert-manager 在创建 Secret 时就带上注解，完全声明式，适合 ArgoCD 管理：

```yaml
spec:
  secretTemplate:
    annotations:
      reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
      reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "argocd,nexus,rssx,enx"
      reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true"
```

如果 Secret 已经存在（如从旧版迁移），也可以用 `kubectl annotate` 补打：

```bash
# 补打注解（已有 Secret 的迁移场景）
kubectl annotate secret wiloon-tls-secret -n default \
  reflector.v1.k8s.emberstack.com/reflection-allowed=true \
  reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces="argocd,nexus,rssx,enx" \
  reflector.v1.k8s.emberstack.com/reflection-auto-enabled=true
```

验证同步结果：

```bash
kubectl get secret wiloon-tls-secret -A
```

## 新增 namespace 的处理

开启 `reflection-auto-enabled` 后，新建 namespace 里也会自动出现 Secret，**无需任何额外操作**。

如果不想用 auto 模式，而是由目标 namespace 主动声明"我要接收这个 Secret"，可以在目标端创建一个同名的 Secret 并打上注解：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: wiloon-tls-secret
  namespace: new-namespace
  annotations:
    reflector.v1.k8s.emberstack.com/reflects: "default/wiloon-tls-secret"
```

这种方式更安全，能精确控制哪些 namespace 可以接收。

## 注意事项

- Reflector 异常时，**已同步的 Secret 不会消失**，只是不再自动更新；服务短期内不受影响
- 源 Secret 删除时，Reflector 会同步删除所有反射副本，需注意不要误删
- `reflection-allowed-namespaces` 支持正则表达式，如 `".*"` 表示所有 namespace（谨慎使用）
- cert-manager 续期后会更新源 Secret，Reflector 会自动把新证书同步到各 namespace

## 与 per-namespace Certificate CR 方案对比

| | per-namespace Certificate | Reflector |
| --- | --- | --- |
| **原理** | cert-manager 在每个 namespace 各自签发 | 只签发一次，controller 自动同步 |
| **新增 namespace** | 需在 manifests 里加 `certificate.yaml` | auto 模式下零操作 |
| **额外依赖** | 无 | 需部署 Reflector controller |
| **证书续期** | cert-manager 各自续期，相互独立 | 源续期后 Reflector 同步 |
| **GitOps 可见性** | 每个 namespace 的证书状态都在 git 里 | 副本由 Reflector 管理，不在 git 里 |

两种方案都是合理的选择。namespace 数量少、变动少时，per-namespace CR 更透明；namespace 数量多或经常新增时，Reflector 更省事。
