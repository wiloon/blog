---
title: arp
author: "-"
date: 2018-08-15T16:15:42+00:00
url: /?p=12535
categories:
  - Inbox
tags:
  - reprint
---
## arp

ARP协议概述
  
IP数据包常通过以太网发送。以太网设备并不识别32位IP地址: 它们是以48位以太网地址传输以太网数据包的。因此,IP驱动器必须把IP目的地址转换成以太网网目的地址。在这两种地址之间存在着某种静态的或算法的映射,常常需要查看一张表。地址解析协议(Address Resolution Protocol,ARP)就是用来确定这些映象的协议。

ARP工作时,送出一个含有所希望的IP地址的以太网广播数据包。目的地主机,或另一个代表该主机的系统,以一个含有IP和以太网地址对的数据包作为应答。发送者将这个地址对高速缓存起来,以节约不必要的ARP通信。
  
<https://www.ibm.com/developerworks/cn/linux/l-arp/index.html>
