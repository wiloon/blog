---
title: FireFox
author: "-"
date: 2013-07-15T11:11:59+00:00
url: fireFox
categories:
  - Inbox
tags:
  - reprint
---
## Firefox

## Firefox socks proxy

firefox 稳定版没有 `about:config` 选项.

firefox beta 和 firefox nightly build 可以在地址栏输入 `about:config` 查找 proxy 关键字, 设置 socks5 proxy

需要设置三个key

- network.proxy.socks: 192.168.9.1
- network.proxy.socks_port: 1080
- network.proxy.socks_remote_dns: true
- network.proxy.type: 1
