---
title: 'raspberry pi 3B  disable ipv6'
author: "-"
date: 2018-12-23T15:35:18+00:00
url: /?p=13197
categories:
  - Raspberry-Pi
tags:
  - reprint
---
## 'raspberry pi 3B  disable ipv6'
Add ipv6.disable=1 to /boot/cmdline.txt

cat /etc/modprobe.d/ipv6.conf

# Don't load ipv6 by default

alias net-pf-10 off

# uncommented

alias ipv6 off

# added

options ipv6 disable_ipv6=1

# this is needed for not loading ipv6 driver

blacklist ipv6

https://www.raspberrypi.org/forums/viewtopic.php?t=138899