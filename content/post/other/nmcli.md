---
title: nmcli
author: "-"
date: 2015-09-09T14:55:34+00:00
url: /?p=8231
categories:
  - Inbox
tags:
  - reprint
---
## nmcli

跨树协议 (STP)

```Bash
nmcli con show
# 创建 br0 启用 stp
nmcli con add type bridge ifname br0
# 禁用 stp
nmcli con add type bridge ifname br0 stp no
# 把 enp0s20f0u2 加入 br0
nmcli con add type bridge-slave ifname enp0s20f0u2 master br0
nmcli connection show --active

nmcli connection down enp0s20f0u2
nmcli connection up bridge-br0
nmcli connection up bridge-slave-enp0s20f0u2
```