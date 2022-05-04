---
title: openwrt proxy
author: "-"
date: 2018-11-03T05:45:46+00:00
url: /?p=12846
categories:
  - network
tags:
  - reprint
---
## openwrt proxy
## 安装ipset

opkg install ipset

# 创建一个网络地址的"集合"

ipset create vlist hash:net

# gfwlist > ipset

https://github.com/cokebar/gfwlist2dnsmasq

## 配置dnsmasq

<http://blog.wiloon.com/?p=12638>