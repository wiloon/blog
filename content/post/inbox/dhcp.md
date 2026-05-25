---
title: DHCP 与 DNS（OpenWrt homelab）
author: "-"
date: 2020-08-28T10:00:55+08:00
lastmod: 2026-05-24T14:43:58+08:00
draft: true
url: dhcp-dns-openwrt
categories:
  - network
tags:
  - dhcp
  - dns
  - dnsmasq
  - OpenWrt
  - homelab
  - remix
  - AI-assisted
aliases:
  - /p12473/
---

## DHCP 是什么

DHCP（Dynamic Host Configuration Protocol）在客户端开机或接入网络时，自动下发一组网络参数，常见包括：

- IP 地址、子网掩码
- 默认网关
- DNS 服务器地址
- 租期（lease time）
- 可选：域名、search domain（搜索域）

要正常上网，客户端至少需要 IP、掩码、网关和 DNS；其中 DNS 地址往往也是 DHCP 一并下发的，所以很多人会感觉「DHCP 和 DNS 是一起的」——协议上它们仍是两件事，只是经常由同一台设备、同一份配置一起管。

参考：[鸟哥 DHCP 理论](http://cn.linux.vbird.org/linux_server/0340dhcp.php#theory)

## DNS 和 DHCP 有没有关联

有，但分工不同：

| 协议 | 回答的问题 |
| ---- | ---------- |
| DHCP | 这台设备用哪个 IP、网关、租期；DNS 问谁 |
| DNS  | 这个名字对应哪个 IP |

关联方式常见有三类：

1. DHCP 在选项里告诉客户端「DNS 服务器是 x.x.x.x」（OpenWrt 上经常是路由器自己）。
2. 内网 DNS 记录和 DHCP 租约/静态分配共用同一份「主机名 ↔ IP」数据（dnsmasq 典型做法）。
3. DHCP 下发 search domain（如 `lan`），客户端访问 `nas` 时会尝试解析 `nas.lan`。

公网域名（如 `example.com`）仍由上游 DNS 或转发解析；你在 homelab 里配的通常是内网名（`*.lan`、`*.home` 等）的本地解析。

## OpenWrt：DHCP 与 DNS 合体（dnsmasq）

在**默认的 OpenWrt 配置**里，IPv4 的 DHCP 和内网 DNS 都由 **dnsmasq** 提供，没有单独换过 DNS 方案时可以认为「就是它在管」：

- **DHCP 服务器**：给手机、NAS、电脑分配 IP，并在 DHCP 选项里告诉客户端「DNS 用路由器 LAN 地址」（例如 `192.168.1.1`）。
- **DNS 服务器**：dnsmasq 在路由器上监听 **UDP/TCP 53**，应答 LAN 设备的查询；内网域名本地解析，公网域名再转发到上游。

客户端从 DHCP 拿到的 DNS 地址就是路由器自己；设备访问内网域名时，实际是在问路由器 **53 端口**，默认由 dnsmasq 处理。

因此用 LuCI 或 `/etc/config/dhcp` 管 homelab 内网域名，本质上是：**DHCP 登记「谁是谁（IP + 主机名）」，DNS 负责「名字 → IP」**；在 dnsmasq 里这两份数据常常来自同一套静态租约或 hosts 配置。

### 默认之外的情况

并非所有 OpenWrt 都「永远只有 dnsmasq」，常见例外如下：

| 情况 | 说明 |
| ---- | ---- |
| 安装了其他 DNS 软件 | 如 Unbound、knot-resolver 单独做 DNS 时，53 端口可能由别的进程监听，dnsmasq 可能只做 DHCP 或只做转发 |
| IPv6 | 常见由 **odhcpd** 处理 IPv6 的 RA / DHCPv6，与 IPv4 的 dnsmasq 分工不同 |
| 自定义 `/etc/config/dhcp` | 可关闭 dnsmasq 的 DNS 或 DHCP 其中一项 |

在路由器上可确认谁在提供 DNS：

```sh
# 谁在监听 53 端口
ss -lunp | grep ':53'

# dnsmasq 是否在运行
ps | grep '[d]nsmasq'
```

若输出里看到 `dnsmasq` 占用 `0.0.0.0:53` 或 `192.168.x.1:53`，说明当前由内网 DNS 由它在应答。

典型访问路径：

```text
设备开机
  → DHCP 拿到 IP，以及「DNS = 192.168.x.1（路由器）」
  → 浏览器访问 nas.homelab
  → 向路由器 DNS 查询
  → dnsmasq 查本地记录 / 租约中的主机名
  → 返回内网 IP
```

## homelab 实践里要注意的几点

### 客户端真的在用路由器 DNS

若设备手动指定了 `8.8.8.8` 等公网 DNS，会绕开 OpenWrt 上的内网记录，表现为「内网域名解析不到」。应让客户端使用 DHCP 下发的 DNS（或手动设为路由器 LAN IP）。

### 静态 IP 与 DNS 记录对齐

服务若用 DHCP 动态地址，IP 一变，固定 DNS 记录就会失效。常见做法：

- 在 OpenWrt 为设备做 DHCP 静态租约（MAC 绑定固定 IP）；
- 同时在 DNS 里写 `address=/主机名.lan/192.168.x.x`，或依赖 dnsmasq 根据主机名自动生成记录。

### 域名后缀与 search domain

DHCP 可下发 domain / search domain。客户端访问短名 `nas` 时，系统可能自动尝试 `nas.lan`（具体行为因操作系统而异）。配置时保持「DHCP 域名后缀」与「DNS 记录后缀」一致，少踩坑。

### 内网解析与公网解析分工

- 内网：dnsmasq 本地 `address=`、`dhcp-host`、租约主机名等。
- 公网：dnsmasq `server=` 转发到运营商或 AdGuard、Pi-hole 等上游。

## 小结

DNS 和 DHCP 不是同一个协议；在 OpenWrt homelab 里它们通过 dnsmasq 紧耦合：DHCP 分配 IP 并指定「去问哪台 DNS」，DNS 用同一份主机/IP 信息回答内网名字。用 DHCP 管理 homelab 内网域名，管的是登记与下发；真正做「名字 → IP」查询的仍是 DNS，只是多数情况下和 DHCP 在同一台 OpenWrt、同一份配置里完成。
