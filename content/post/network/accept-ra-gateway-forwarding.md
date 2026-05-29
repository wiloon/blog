---
title: Linux accept_ra 与网关转发场景
author: "-"
date: 2026-05-29T13:07:18+08:00
lastmod: 2026-05-29T13:27:10+08:00
url: accept-ra-gateway-forwarding
categories:
  - Network
tags:
  - linux
  - ipv6
  - networking
  - homelab
  - remix
  - AI-assisted
---

## 背景

`accept_ra` 是 Linux 内核里控制「是否接受路由器通告（Router Advertisement, RA）」的 sysctl。常见路径：

```text
/proc/sys/net/ipv6/conf/<interface>/accept_ra
```

取值含义（简化）：

| 值 | 行为 |
| --- | --- |
| `0` | 忽略 RA，不自动配置地址/默认路由 |
| `1` | 接受 RA（主机模式） |
| `2` | 接受 RA，即使接口已开启 `forwarding`（网关/路由器模式） |

默认情况下，一旦接口 `net.ipv6.conf.<iface>.forwarding=1`，内核会把 `accept_ra` 视为 `0`，不再接受 RA。这是 RFC 4861 的意图：路由器不应把 RA 当主机来用。

## 解决什么问题

典型场景：**一台 Linux 机器同时做网关转发，又需要从上游路由器拿 IPv6 前缀和默认路由**。

例如 homelab 里的 VPN 客户端 `192.168.50.61`：

1. 上游 OpenWrt 通过 RA 向 LAN 下发 ISP 委派的 `/60` GUA 前缀和 `::/0` 默认路由。
2. 50.61 运行 tproxy，需要 `ip_forward=1` 转发 LAN / WireGuard 流量。
3. 若 `accept_ra=0` 且 **没有** userspace 网络栈（如 systemd-networkd）代为处理 RA，本机 IPv6 直连（VPN `direct` 出站）可能 `Network is unreachable`。

`accept_ra=2` 的作用：**在开启 IP 转发的同时，仍接受上游 RA**，让网关主机也能获得 GUA 和默认路由。

## 与本次 IPv6 PD 故障的区别

2026-05-29 的 USTC 镜像 IPv6 失败，根因是 OpenWrt **丢失运营商 PD**，LAN 只剩 ULA、无 GUA。此时即使 50.61 设 `accept_ra=2` 也无效——上游根本没有可下发的公网前缀。

`accept_ra=2` 解决的是 **「上游 PD 正常，但网关因 forwarding 且仅靠内核收 RA 时被忽略」** 的配置问题，不能替代 OpenWrt PD 恢复。

## homelab 现网决策（50.61）

**结论：保持 `accept_ra=0`，不改为 `2`，也不持久化。**

| 项 | 说明 |
| --- | --- |
| 现网 | `ens18.accept_ra=0`，`forwarding=1` |
| RA 由谁处理 | **systemd-networkd**（`/etc/systemd/network/20-ethernet.network`），路由带 `proto ra` |
| 为何不改为 `2` | networkd 已在 userspace 处理 RA；改 `2` 与 networkd 重复，现网 IPv6 已通，无需动 |
| 前提 | 继续使用 systemd-networkd；若日后不用 networkd，再评估 `accept_ra=2` |

## 如何查看与设置

```bash
# 查看
sysctl net.ipv6.conf.ens18.accept_ra
sysctl net.ipv6.conf.ens18.forwarding

# 临时生效
sysctl -w net.ipv6.conf.ens18.accept_ra=2

# 持久化（systemd-networkd 示例）
# /etc/systemd/network/10-ens18.network
# [IPv6AcceptRA]
# UseRoutes=yes
# 并在 [Network] 段配合 Gateway 或路由策略；Arch 亦可用 /etc/sysctl.d/*.conf
```

持久化 `accept_ra=2` 适用于 **无 systemd-networkd 等 userspace 兜底** 的网关；若 networkd 已管理接口 RA，通常保持默认即可。

## 何时需要

- Linux 作为 **透明代理 / 软路由 / WireGuard 网关**，且 **本机** 需要 IPv6 公网出网（direct 出站）。
- 上游（OpenWrt 等）已通过 RA 下发 GUA + 默认路由。

不需要的情况：

- 纯主机，未开 `forwarding` → `accept_ra=1` 通常足够。
- **systemd-networkd 已处理 RA**（如 homelab 50.61）→ 保持 `accept_ra=0` 即可，不必改 `2`。
- 仅 IPv4 出网，或 VPN direct 强制 IPv4。
- 上游无 PD/GUA（应先修 OpenWrt WAN IPv6）。

## 相关

- homelab：WAN IPv6 PD 丢失时，VPN 全隧道下国内镜像 IPv6 直连失败（运维恢复 OpenWrt PD 即可）
- 透明代理：tproxy 启动与 RA 时序、ISP `/60` 前缀变更时的前缀监听与本机回包 RETURN 规则热更新
- 内核文档：`Documentation/networking/ip-sysctl.rst`（`accept_ra` 各比特含义）
