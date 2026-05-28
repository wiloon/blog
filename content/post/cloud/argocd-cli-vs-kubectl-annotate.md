---
title: Argo CD CLI 与 kubectl annotate 对比
author: "-"
date: 2026-05-28T12:40:16+08:00
lastmod: 2026-05-28T12:40:16+08:00
url: argocd-cli-vs-kubectl-annotate
categories:
  - Cloud
tags:
  - k8s
  - argocd
  - gitops
  - remix
  - AI-assisted
---

## 背景

在 homelab 里用 Argo CD 管理 QuantDinger（`application-quantdinger.yaml`，`automated` + `selfHeal`）。把 MiniMax 相关配置 push 到 `w10n-config` 后，集群里的 ConfigMap 一度还是旧内容：Argo 显示 `Synced`，但 revision 仍停在旧 commit。

当时本机没有安装 `argocd` CLI，于是先用 `kubectl annotate` 触发 hard refresh，又用 `kubectl apply -k` 把 manifest 直接打进集群。事后整理一下两种「触发 Argo」方式的区别，避免下次混淆。

## 两种方式分别做什么

### `argocd` CLI

Argo CD 官方命令行，通过 Argo API Server 操作 Application，语义最完整。

常见用途：

- `argocd app get quantdinger`：查看同步状态、health、当前 revision
- `argocd app sync quantdinger`：**主动执行一次 Sync**，把 Git 目标 revision 应用到集群
- `argocd app diff quantdinger`：对比 Git 与集群 live 状态
- `argocd app rollback quantdinger`：回滚到历史 revision

`sync` 会走 Argo 的完整同步流水线（diff、apply、health 等待、hook 等），并在 Argo UI / `Application` 状态里留下明确的 operation 记录。

### `kubectl annotate`（hard refresh）

不安装 CLI 时，可以直接改集群里的 `Application` 对象，给 Argo 控制器发信号：

```bash
kubectl -n argocd annotate application quantdinger \
  argocd.argoproj.io/refresh=hard --overwrite
```

含义：

- 让 Argo **重新拉取 Git 仓库**并刷新 Application 的「期望状态」缓存
- `hard` 会连同 manifest 生成缓存一起刷新（比 `normal` 更彻底）
- **不等于**立刻执行 Sync；在 `syncPolicy.automated` 开启时，控制器发现 OutOfSync 后才会自动同步

因此：refresh 解决的是「Argo 还没看到最新 Git」；若已看到最新 Git 但集群未对齐，仍需要 **Sync**（自动或手动）。

## 对比

| 维度 | `argocd` CLI | `kubectl annotate`（refresh） |
| ---- | ------------ | ----------------------------- |
| 依赖 | 需安装 CLI，并 login 到 Argo Server | 只需 `kubectl` 与 RBAC |
| 主要动作 | 可 **Sync / Diff / Rollback** 等完整操作 | 仅触发 **刷新 Git 缓存** |
| 是否直接改工作负载 | 通过 Argo Sync 间接改 | 不直接改；需配合 automated sync 或另做 sync |
| 操作记录 | Argo operation 历史清晰 | 仅 annotation 变更，不如 CLI 直观 |
| 适用场景 | 日常 GitOps 运维、排障、回滚 | 机器未装 CLI、CI/脚本里快速「拉一把 Git」 |
| 与 `kubectl apply -k` 关系 | 正路：以 Git 为准经 Argo 下发 | 旁路：`apply -k` 绕过 Argo 改集群，易导致 **OutOfSync** |

## 实际排障时的组合

以 QuantDinger 为例，推荐顺序：

1. **确认 Git 已 push**，本地 `git log -1` 与 Argo `status.sync.revision` 一致
2. **刷新缓存**：`kubectl annotate ... refresh=hard`（或 `argocd app get` 后 UI 点 Refresh）
3. **等待 automated sync**，或 **`argocd app sync quantdinger`**
4. 验证业务配置是否进 Pod，例如：

```bash
kubectl -n quantdinger get configmap quantdinger-backend-config \
  -o jsonpath='{.data.LLM_PROVIDER}{"\n"}'
kubectl -n quantdinger exec deploy/backend -- sh -lc \
  'echo LLM_PROVIDER=$LLM_PROVIDER; [ -n "$MINIMAX_API_KEY" ] && echo MINIMAX_API_KEY=SET'
```

若赶时间、且接受 Argo 暂时 OutOfSync，可 **`kubectl apply -k homelab/k8s/quantdinger`** 应急，再 `rollout restart`。长期仍应以 Git + Argo Sync 收敛，避免 selfHeal 与手工 apply 打架。

## 安装 argocd CLI（可选）

```bash
# Arch Linux 示例
yay -S argocd-bin
# 或官方 install 脚本 / 下载二进制

argocd login argocd.wiloon.com --grpc-web
argocd app list
argocd app sync quantdinger
```

登录方式因 Ingress、gRPC-Web、SSO 配置而异，以集群实际 Argo 入口为准。

## 小结

- **`kubectl annotate` + `refresh=hard`**：轻量、无 CLI，适合「让 Argo 重新读 Git」
- **`argocd app sync`**：GitOps 正操，显式把 Git 状态应用到集群
- **`kubectl apply -k`**：绕过 Argo 的应急手段，易造成 OutOfSync，不宜作为常态

在 automated + selfHeal 的 homelab 里，日常改 manifest → push → 等 Argo 同步即可；只有「push 了但 revision 不动」时，再 refresh；需要立即对齐且不想等控制器时，用 `argocd app sync` 最干净。
