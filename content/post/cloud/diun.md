---
title: "Diun: Homelab 容器镜像更新通知"
author: "-"
date: 2026-09-14T09:55:04+08:00
lastmod: 2026-09-14T09:55:04+08:00
url: diun
categories:
  - cloud
tags:
  - homelab
  - k8s
  - diun
  - docker
  - remix
  - AI-assisted
---

## 背景

homelab 里不少服务钉在某个镜像 tag 上，上游发了新版本不会自动跟着走。以前靠偶尔看 GitHub Release，或者写脚本去打 `releases/latest`。后者对把每个版本都标成 pre-release 的项目几乎没用——接口长期停在旧版，等于没监控。

现在改成在 K8s 集群里跑 [Diun](https://crazymax.dev/diun/)（Docker Image Update Notifier）：盯 registry 里的镜像 tag，出现匹配规则的新稳定版就推 Telegram。它不负责滚动升级，只负责通知。它在服务清单里的位置见 [Homelab Services](../cs/homelab.md)；硬件与集群拓扑见 [Homelab 拓扑](./homelab-topology.md)。

## 它盯的是 registry，不是正在跑的容器

Diun 用 file provider 读一份 watch 列表，直接问 registry「这个仓库现在有哪些 tag」，不扫描集群里的 Pod。所以：

- 可以盯 homelab 里跑着的容器（例如 Vaultwarden）
- 也可以盯**并不在集群里跑**的软件：只要上游会在打 release 时构建官方镜像，tag 与版本号一一对应，就可以把镜像当发版探针

后者用来补 GitHub `releases/latest` 的坑。有些项目几乎每个 release 都标 pre-release，那个接口会一直停在旧稳定版；镜像 tag 没有这层过滤。

## homelab 部署

跑在独立 namespace `diun`，由 Argo CD 管（`w10n-config` 里的 `infra/homelab/k8s/diun/`）。要点：

| 项 | 现网 |
| -- | ---- |
| 镜像 | Nexus 代理后的 `crazymax/diun` |
| 检查频率 | 每 6 小时；启动时再跑一次 |
| 通知 | Telegram Bot；凭据在 `notifications` namespace，由 [Reflector](./kubernetes-reflector.md) 反射进 `diun` |
| 状态 | Longhorn PVC 记已经见过的 tag，重启不会把历史版本再推一遍 |
| UI | 没有。纯后台 + 推送 |

首次检查关掉通知（`DIUN_WATCH_FIRSTCHECKNOTIF=false`），只建基线。之后才对真正的新 tag 发消息。

## 当前监控目标

只匹配 `x.y.z` 形式的稳定 tag（`include_tags: ^\d+\.\d+\.\d+$`），按 semver 排序，每个仓库最多看最近 15 个 tag。

| 镜像 | 实际对应什么 | 收到通知后 |
| ---- | ------------ | ---------- |
| `docker.io/vaultwarden/server` | AWS EC2 上的自建密码服务 | 改 Ansible 里的镜像 tag，再跑对应 playbook |
| 上游官方容器镜像（二进制部署的服务） | 墙外 VPS 上用 Ansible 装的二进制，本身不跑容器；官方镜像 tag 与 GitHub release 一一对应，含 pre-release | 改 inventory 里的版本号，再走既有升级流程 |

Vaultwarden 这一条的写法大致如下：

```yaml
- name: docker.io/vaultwarden/server:latest
  watch_repo: true
  notify_on:
    - new
  sort_tags: semver
  max_tags: 15
  include_tags:
    - ^\d+\.\d+\.\d+$
```

改 watch 列表之后要让 Deployment 重新读 ConfigMap（`kubectl -n diun rollout restart deploy/diun`）。

## 和 Watchtower / 自动升级的区别

Watchtower、Keel 一类工具会在发现新镜像后直接改运行中的容器。Diun 只发通知，升级仍是手动、按各服务自己的流程走。homelab 里版本是钉死的（GitOps 或 Ansible inventory），自动拉 `latest` 不符合现有发布方式。
