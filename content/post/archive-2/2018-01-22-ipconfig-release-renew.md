---
title: 'IPconfig  release renew'
author: w1100n
type: post
date: 2018-01-22T02:19:13+00:00
url: /?p=11775
categories:
  - Uncategorized

---
在Windows系统下IPconfig命令，后面带/release和 /renew参数可以实现从DHCP服务器重新获取IP地址：

1、ipconfig /release 释放当前网卡获取的IP地址，使用该命令后，网卡（IPv4地址）此时IP地址为空。

2、ipconfig /renew 为网卡重新从DHCP服务器上面获取新的IP地址。