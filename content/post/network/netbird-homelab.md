---
title: Netbird 自建：公共 WiFi UDP 受限时访问 homelab
author: "-"
date: 2026-06-15T18:00:00+08:00
lastmod: 2026-06-16T00:15:53+08:00
url: netbird-homelab
categories:
  - network
tags:
  - netbird
  - homelab
  - wireguard
  - remix
  - AI-assisted
---

## 背景

MacBook 在咖啡店等公共 WiFi 下，需要访问家里 homelab 内网（`192.168.50.0/24`）。平时外出用 WireGuard 连回家，但这类环境里 UDP 经常被限速或干脆不通——不连 WG 时网页很快，一连上就严重丢包，很像运营商或场所 WiFi 在限制 UDP。

这次的目标是：在 UDP 不通时仍能稳定访问 homelab 内网，同时 MacBook 的出口代理保持现状，不和 homelab 的魔法工具链路搅在一起。

## 为什么选 Netbird

试过换运营商热点、换连接方式之后，结论是需要一条能在 UDP 被封时自动回退的路径。Netbird 自建控制面的关键能力是：

1. P2P 优先，延迟低
2. P2P 不通时走 TURN relay，可走 TCP 443，公共 WiFi 很难彻底封死
3. Subnet Router：homelab 里只需一台节点宣告 `192.168.50.0/24`，不必给每台内网主机装 client

和纯 WireGuard 相比，多了一层控制面和 relay 回退，换来的是在「刁钻 WiFi」下的可用性。

## 架构概览

```
MacBook（Netbird client，split tunnel）
├── 192.168.50.0/24  →  Netbird
│                         ├── P2P（UDP 通时）
│                         └── TURN relay TCP/443（UDP 不通时）
│                         └── 控制面: nb.wiloon.com
└── 其余流量            →  本地出口代理（保持现状）

homelab
├── netbird-router（专用 VM，Subnet Router，通告 192.168.50.0/24）
└── OpenWrt 静态路由：100.64.0.0/10 → netbird-router
```

几个设计选择：

- 控制面部署在阿里云，management / signal / dashboard 经 nginx 反代到 443
- Subnet Router 放在独立 VM，不挂在现有魔法工具网关上，两条链路解耦
- OpenWrt 用静态路由而非 masquerade，保留 client 真实 Netbird IP，日志好查
- MacBook 只路由 homelab 网段，不设默认网关（split tunnel）

## MacBook 侧

macOS 用 Homebrew 安装 client，连接到自建控制面后，确认 `192.168.50.0/24` 走 Netbird 接口，`ping 192.168.50.1` 通，出口 IP 仍走本地代理。

UDP 被模拟封锁时（例如用 `pf` 临时挡出站 UDP），`netbird status` 会在几秒内切到 `Connected (relayed)`，homelab 仍可达——这正是选它的原因。

## 和出口代理的关系

Netbird 只负责 homelab 内网可达性，不替代出口代理。MacBook 上 Clash + 魔法工具继续管其余流量；Netbird 与代理并行，各管一段路由。

iOS 侧因系统只允许一个 VPN 同时激活，方案和 MacBook 不同（full tunnel 经 homelab tproxy 等），本次先解决 MacBook，手机方案留到 Mac 侧稳定后再做。

## 部署入口

实现细节、Ansible / OpenTofu 清单和分阶段验收见 homelab 仓库里的 Netbird Task Spec（`infra/TASK-SPEC-netbird.md`），不在此文展开。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-16 | 初版：背景、架构、MacBook split tunnel 要点 | 配合 W24 周报内链，记录咖啡店 UDP 受限后的方案选型 |
