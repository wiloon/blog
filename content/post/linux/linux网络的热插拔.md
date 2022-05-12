---
title: linux网络的热插拔
author: "-"
date: 2011-12-06T13:07:16+00:00
url: /?p=1814
categories:
  - Linux
  - Network
tags:
  - reprint
---
## linux网络的热插拔
# auto eth0:开机自动启动eth0，不管有沒有插上网线.
  
    如果开机没有插上网线，系统也会让dhclient3去设定，这样只有等超时才能继续开机。
  
  
    如果设为allow-hotplug eth0就不会出现上述情况，先不插网线，开机后再插网线也可以。但是在debian 里用/etc/init.d/networking restart后会出现网卡不能启动，要用ifup eth0
  
  
    才行.
  
