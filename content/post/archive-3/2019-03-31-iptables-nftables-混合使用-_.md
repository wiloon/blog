---
title: iptables nftables 混合使用 -_-
author: "-"
type: post
date: 2019-03-30T16:56:03+00:00
url: /?p=14037
categories:
  - Uncategorized

---
# iptables nftables 混合使用 -_-
iptables 和 nftables 可以混合 使用，规则要小心配置。
  
archlinux nftables 默认规则 禁止转发 （forward) 
  
看iptables 的 trace日志 报文 会先经过 iptables 的forward 链，再流到nftables的 forward链。

### iptables trace


  
    iptables调试， raw表， LOG
  




### nftables trace


  
    nftables trace
  


