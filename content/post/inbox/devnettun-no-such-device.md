---
title: '/dev/net/tun,No such device'
author: "-"
date: 2017-06-30T05:19:10+00:00
url: /?p=10724
categories:
  - Inbox
tags:
  - reprint
---
## '/dev/net/tun,No such device'
```bash
  
sudo pacman -Syu
  
sudo pacman -S linux

sudo modprobe tun
  
modprobe: FATAL: Module tun not found in directory /lib/modules/4.6.3-1-ARCH

sudo insmod /lib/modules/4.6.4-1-ARCH/kernel/drivers/net/tun.ko.gz
  
lsmod | grep tun
  
tun 28672 0
  
```

https://bbs.archlinux.org/viewtopic.php?id=184992