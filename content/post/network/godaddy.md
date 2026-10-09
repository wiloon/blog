---
title: godaddy
author: "-"
date: "2006-01-02 15:04:05"
lastmod: 2026-10-09T21:22:13+08:00
url: godaddy
categories:
  - Network
tags:
  - dns
  - remix
  - AI-assisted
---
## godaddy

买域名

1. 在Godaddy搜索某个关键字, 比如 wiloon
2. 在列表里找一个喜欢的或者价格低的, 有很多首年1.x$的, 比如 wiloon.online
3. 购买并支付, 支付方式可以用 paypal.

cloudflare> add site> free> 添加解析记录

- type: A
- name: @
- ipv4 address: `<vps ip>`
- proxy: false (DNS only)

Save (保存设置然后等 DNS 生效)

4. 配置域名解析, 配置到某一个 vps, DNS> Nameservers> Change Nameservers

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Network | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
