---
title: 禁止network manager 开机启动.
author: "-"
date: 2012-02-08T14:38:46+00:00
url: /?p=2278
categories:
  - Linux
tags:
  - reprint
---
## 禁止network manager 开机启动.
安装sysv-rc-conf

sudo apt-get install sysv-rc-conf

运行sysv-rc-conf

sudo sysv-rc-conf

把network-m对应的xx都点掉.