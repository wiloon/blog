---
title: iptables nftables 混合使用 -_-
author: wiloon
type: post
date: 2019-03-30T16:56:03+00:00
url: /?p=14037
categories:
  - Uncategorized

---
iptables 和 nftables 可以混合 使用，规则要小心配置。
  
archlinux nftables 默认规则 禁止转发 （forward）
  
看iptables 的 trace日志 报文 会先经过 iptables 的forward 链，再流到nftables的 forward链。

### iptables trace

<blockquote class="wp-embedded-content" data-secret="iTzOKBoIhX">
  
    <a href="http://blog.wiloon.com/?p=12128">iptables调试， raw表， LOG</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://blog.wiloon.com/?p=12128&#038;embed=true#?secret=iTzOKBoIhX" data-secret="iTzOKBoIhX" width="600" height="338" title=""iptables调试， raw表， LOG" - w1100n" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

### nftables trace

<blockquote class="wp-embedded-content" data-secret="Qo3n5H6Ki8">
  
    <a href="http://blog.wiloon.com/?p=14030">nftables trace</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://blog.wiloon.com/?p=14030&#038;embed=true#?secret=Qo3n5H6Ki8" data-secret="Qo3n5H6Ki8" width="600" height="338" title=""nftables trace" - w1100n" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>