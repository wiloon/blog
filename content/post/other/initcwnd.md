---
title: initcwnd
author: "-"
date: 2011-11-22T00:45:33+00:00
url: initcwnd
categories:
  - network
tags:
  - reprint
---
## initcwnd
initial congestion window parameter (initcwnd)


Changing initcwnd
Adjusting the value of the initcwnd setting on Linux is simple. Assuming we want to set it to 10:

Step 1: check route settings.

sajal@sajal-desktop:~$ ip route show
192.168.1.0/24 dev eth0  proto kernel  scope link  src 192.168.1.100  metric 1 
169.254.0.0/16 dev eth0  scope link  metric 1000 
default via 192.168.1.1 dev eth0  proto static 
sajal@sajal-desktop:~$ 
Make a note of the line starting with default.

Step 2: Change the default settings.
Paste the current settings for default and add initcwnd 10 to it.

sajal@sajal-desktop:~$ sudo ip route change default via 192.168.1.1 dev eth0  proto static initcwnd 10
Step 3: Verify

sajal@sajal-desktop:~$ ip route show
192.168.1.0/24 dev eth0  proto kernel  scope link  src 192.168.1.100  metric 1 
169.254.0.0/16 dev eth0  scope link  metric 1000 
default via 192.168.1.1 dev eth0  proto static  initcwnd 10
sajal@sajal-desktop:~$ 

>https://www.cnblogs.com/ztguang/p/14480009.html
>https://www.cdnplanet.com/blog/tune-tcp-initcwnd-for-optimum-performance/#change-initcwnd
