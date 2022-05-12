---
title: linux 网络命令
author: "-"
date: 2011-12-03T13:58:11+00:00
url: /?p=1713
categories:
  - Linux
  - Network
tags:$
  - reprint
---
## linux 网络命令
iwconfig 和 iwpriv。iwconfig 用于配置一些比较 general 的功能，如 ESSID、AP 的 MAC 地址、mode、频道、速率等。和 ifconfig 类似，不加任何参数的时候显示 /proc/net/wireless 的内容；而 iwpriv 则配置比较 private 的内容，和各个网卡相关的东西，可以用 -a 获得所有可以执行的命令。下面是这些命令的说明: 

  * iwevent 显示 wireless 事件，主要是驱动程序或者配置更新的事件。
  * iwgetid 获得当前连接网络的信息，相对于 iwconfig 更适合写脚本使用。
  * iwlist 用于显示无线网络的各种信息，通过 scaning 网络中 AP 获得。
  * iwspy 用于获取无线网络某些节点上的统计信息。


1.查看网卡型号: 
  
# lsmod | grep iw

2.查看网卡信息: 
  
# iwconfig

查看附近可用的无线接入点 (AP) 
  
# iwlist wlan0 scan

ifconfig wlan0 up

ifconfig wlan0 down