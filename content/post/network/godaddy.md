---
title: godaddy
author: "-"
date: "2006-01-02 15:04:05"
url: godaddy
categories:
  - Inbox
tags:
  - Remix
---
## godaddy

买域名

1. 在Godaddy搜索某个关键字, 比如 wiloon
2. 在列表里找一个喜欢的或者价格低的, 有很多首年1.x$的, 比如 wiloon.online
3. 购买并支付, 支付方式可以用 paypal.

cloudflare> add site> free> 添加解析记录

- type: A
- name: @
- ipv4 address: <vps ip>
- proxy: false (DNS only)

Save (保存设置然后等 DNS 生效)

4. 配置域名解析, 配置到某一个 vps, DNS> Nameservers> Change Nameservers
