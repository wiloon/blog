---
title: openwrt lan 改网段
author: w1100n
type: post
date: 2018-10-07T05:26:23+00:00
url: /?p=12761
categories:
  - Uncategorized

---
https://www.cnblogs.com/double-win/p/3841017.html

```bash
  
vim /etc/config/network

config 'interface' 'lan' #LAN口，用于路由器子网设置
          
option 'ifname' 'eth0'
          
option 'type' 'bridge'
          
option 'proto' 'static'
          
option 'ipaddr' '192.168.99.1'
          
option 'netmask' '255.255.255.0'

```