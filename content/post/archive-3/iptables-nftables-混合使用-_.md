---
title: iptables nftables 混合使用 -_-
author: "-"
date: 2019-03-30T16:56:03+00:00
url: /?p=14037
categories:
  - network
tags:
  - reprint
---
## iptables nftables 混合使用 -_-
iptables 和 nftables 可以混合使用，但是规则要小心配置。
  
archlinux nftables 的默认规则 是禁止转发的  (forward) 
  
看 iptables 的 trace 日志 报文 会先经过 iptables 的 forward 链，再流到 nftables 的 forward 链。

### iptables trace

iptables调试， raw表， LOG
  
### nftables trace

    nftables trace
  


