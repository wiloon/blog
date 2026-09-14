---
title: "Homelab Services: 部署了哪些服务"
author: "-"
date: 2017-02-20T07:37:42+00:00
lastmod: 2026-09-14T10:00:01+08:00
url: homelab
categories:
  - cloud
tags:
  - homelab
  - k8s
  - remix
  - AI-assisted
---

## 这篇写什么

本文只回答「集群里现在跑了哪些服务」。对外 HTTPS 走 Kong Ingress，持续部署走 [Argo CD](../cloud/argocd.md)。物理机、PVE 宿主机、K8s 节点和网段见 [Homelab 拓扑](../cloud/homelab-topology.md)。两篇分工：

| 问题 | 看哪篇 |
| ---- | ------ |
| 哪台物理机 → 哪个 PVE → 哪些 K8s 节点 | [Homelab 拓扑](../cloud/homelab-topology.md) |
| 集群里部署了哪些服务、怎么访问 | 本文 |

清单以 `w10n-config` 的 `infra/homelab/k8s/` 为准。域名由 OpenWrt 解析到 Kong Ingress VIP `192.168.50.101`。

## 平台层

集群自己用的组件，一般不直接当「业务应用」打开。

| 服务 | Namespace | 访问 | 说明 |
| ---- | --------- | ---- | ---- |
| kube-vip | kube-system | API `192.168.50.100`；Ingress `192.168.50.101` | control-plane 与 Kong LoadBalancer 各一个 VIP |
| Kong | kong | （所有 `*.wiloon.com` / `*.wiloon.lab` HTTPS） | Ingress Controller，TLS 在这一层终止 |
| Longhorn | longhorn-system | https://longhorn.wiloon.com | 集群存储 |
| cert-manager | cert-manager | （无独立 UI） | 通配符证书；Ingress 用已签发的 Secret，不用 cert-manager 注解 |
| Reflector | kube-system | （无独立 UI） | 跨 namespace 同步 TLS / Telegram 等 Secret，见 [Reflector](../cloud/kubernetes-reflector.md) |
| Argo CD | argocd | https://argocd.wiloon.com | GitOps，manifest 在 git 里改完即 sync |
| Descheduler | kube-system | （无独立 UI） | Pod 重平衡，见 [Descheduler](../cloud/kubernetes-descheduler.md) |
| Metrics Server | kube-system | `kubectl top` | 给 HPA 和排障用 |

## 应用

| 服务 | Namespace | 访问 | 说明 |
| ---- | --------- | ---- | ---- |
| RSSX | rssx | https://rssx-lab.wiloon.com | RSS 阅读器 |
| RSSHub | rsshub | https://rsshub.wiloon.lab | 把没有原生 RSS 的站点转成 feed，给 RSSX 订阅 |
| ENX | enx | UI https://enx.wiloon.lab ；API https://enx-api.wiloon.lab | 英语学习扩展的后端和 UI；CI/CD 见 [enx-api Homelab CI/CD](../cloud/enx-api-homelab-cicd.md) |
| Calibre | default | https://calibre.wiloon.com | 电子书 |
| QuantDinger | quantdinger | https://quantdinger.wiloon.com | 量化相关 backend + frontend |
| PM Toolkit | pm-toolkit | https://pm-toolkit.wiloon.lab | FastAPI + Next.js 内网工具 |
| Pomodoro | default | https://pomodoro-lab.wiloon.com | 番茄钟 |
| Nexus | nexus | UI https://nexus.wiloon.com ；Docker Hub 代理 https://docker-registry.wiloon.com | 镜像缓存；另有 GHCR / GCR / hosted 等子域 |
| ddns-go | ddns-go | https://ddns-go.wiloon.com | 家用出口 IP 变了之后更新 Cloudflare DNS |
| nettest | default | NodePort `192.168.50.100:30880` | whoami，用来测连通性 |

Pathfinder 已从集群下线，不在上表。

## 可观测与通知

| 服务 | Namespace | 访问 | 说明 |
| ---- | --------- | ---- | ---- |
| Grafana | kube-prometheus-stack | https://grafana.wiloon.com | 看板 |
| Prometheus | kube-prometheus-stack | https://prometheus.wiloon.com | 时序指标 |
| Loki | loki | （经 Grafana） | 日志 |
| Alloy | loki | （无 UI） | 节点侧采集，见 [可观测性工具](../cloud/observability-tools.md) |
| Diun | diun | 无 UI，Telegram 推送 | 盯 registry 里的新镜像 tag，见 [Diun](../cloud/diun.md) |
| notifications | notifications | （无 UI） | 共享 Telegram Bot 凭据，Reflector 反射给 Diun |

## 数据与 CI

| 服务 | Namespace | 访问 | 说明 |
| ---- | --------- | ---- | ---- |
| PostgreSQL | database | 集群内 `postgres.database.svc:5432`；NodePort `192.168.50.100:30432` | 共享库 |
| Redis | database | 集群内 `redis.database.svc:6379`；NodePort `192.168.50.100:30379` | 共享缓存（RSSHub 等） |
| Tekton | tekton-pipelines | https://tekton.wiloon.com | 构建镜像、改 GitOps tag |
| blog-stats | blog-stats | Grafana 看板 | 定期统计博客文章数和字数 |

## 站外服务（Kong 反代）

不跑在 K8s 里，只通过 Ingress 把内网主机暴露成域名。

| 服务 | 上游 | 访问 |
| ---- | ---- | ---- |
| NAS（威联通） | `192.168.50.227:5000` | https://nas.wiloon.com |
| OpenClaw | `192.168.50.72:18789` | https://openclaw.wiloon.com |

PVE 上的软路由、Windows 虚拟机、VPN 网关等不属于「集群服务」，记在 [Homelab 拓扑](../cloud/homelab-topology.md)。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-09-14 | 重写为现网服务清单；与 Homelab 拓扑互链 | 原文已过时 |
