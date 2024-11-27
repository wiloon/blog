---
title: iptables `nftables` 混合使用 -_-
author: "-"
date: 2019-03-30T16:56:03+00:00
url: "iptables/nftables"
categories:
  - network
tags:
  - Original
---
## iptables `nftables` 混合使用 -_-

iptables 和 `nftables` 可以混合使用，但是规则要小心配置。
  
archlinux `nftables` 的默认规则是禁止转发的 (forward)
  
看 iptables 的 trace 日志 报文会先经过 iptables 的 forward 链，再流到 `nftables` 的 forward 链。

nftables 默认在 forward 链抛掉所有数据。
如果启用了 nftables, 一定修改一下 nftables 的默认配置文件。否则报文在 iptables 的 forward 链 accept 之 后会被 nftables 规则抛掉。

### iptables trace

iptables 调试， raw 表， LOG
  
### `nftables` trace

`nftables trace`
  