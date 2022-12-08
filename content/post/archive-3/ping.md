---
title: ping, fping
author: "-"
date: 2020-04-13T10:43:01+00:00
url: ping
categories:
  - network
tags:
  - reprint
---
## ping, fping

## install

```bash
# ubuntu
apt install iputils-ping

```

## archlinux install fping

```bash
pacman -S fping
```

## windows 长 ping

```bat
ping 192.168.1.100 -t
```

### 指定网络设备

```bash
ping -c 1 -I veth0 192.168.3.102
```

### 同时显示统计信息

```bash
fping -l google.com
```

### 什么是ping

PING (Packet Internet Grope)，因特网包探索器，用于测试网络连接量的程序。Ping发送一个ICMP回声请求消息给目的地并报告是否收到所希望的ICMP回声应答。

### 什么是TTL

TTL: 生存时间
指定数据包被路由器丢弃之前允许通过的网段数量。
TTL 是由发送主机设置的，以防止数据包不断在 IP 互联网络上永不终止地循环。转发 IP 数据包时，要求路由器至少将 TTL 减小 1。
使用PING时涉及到的 ICMP 报文类型
一个为ICMR请求回显 (ICMP Echo Request)
一个为ICMP回显应答 (ICMP Echo Reply)
TTL 字段值可以帮助我们识别操作系统类型。
UNIX 及类 UNIX 操作系统 ICMP 回显应答的 TTL 字段值为 255
Compaq Tru64 5.0 ICMP 回显应答的 TTL 字段值为 64
微软 Windows NT/2K操作系统 ICMP 回显应答的 TTL 字段值为 128
微软 Windows 95 操作系统 ICMP 回显应答的 TTL 字段值为 32
当然，返回的TTL值是相同的
但有些情况下有所特殊
LINUX Kernel 2.2.x & 2.4.x ICMP 回显应答的 TTL 字段值为 64
FreeBSD 4.1, 4.0, 3.4;
Sun Solaris 2.5.1, 2.6, 2.7, 2.8;
OpenBSD 2.6, 2.7,
NetBSD
HP UX 10.20
ICMP 回显应答的 TTL 字段值为 255
Windows 95/98/98SE
Windows ME
ICMP 回显应答的 TTL 字段值为 32
Windows NT4 WRKS
Windows NT4 Server
Windows 2000
Windows XP
ICMP 回显应答的 TTL 字段值为 128
这样，我们就可以通过这种方法来辨别操作系统

<https://unix.stackexchange.com/questions/329110/display-the-missing-icmp-seq-count-ping-command>

Ping命令返回的TTL值详解
  
转载dankanku 最后发布于2016-09-19 14:54:51 阅读数 17722 收藏
  
展开
  
转自: <http://429006.com/article/Technology/160.htm>

Time To Live (TTL) 域的信息很有趣。每一个被发送出的IP信息包都有一个TTL域，该域被设置为一个较高的数值 (在本例中ping信息包的TTL值为255)。当信息包在网络中被传输时，TTL的域值通过一个路由器时递减1；当TTL 递减到0时，信息包被路由器抛弃。

IP规范规定: TTL应该被设置为60 (尽管ping 信息包的TTL是255)。这样做主要是为了让一个信息包永远在为了中存在。担该信息对我们来说有特殊的含义。我们可以使用TTL大致确定该信息包经过了多少个路由器过渡段。在本例中，用255减去N，N是返回的回送答复的TTL。如果TTL值在连续几个ping中发生变化，这说明返回的信息包经过了不同的路由器。

time显示了信息包到达远程主机后返回的时间。计算定位为毫秒。通常网卡下，来回时间在200毫秒以下最好。信息包抵达目的地的时间叫做latency (等待时间) ，如果你看到来回时间变化很大 (叫做"jitter (抖动) ) ，这说明同主机之间的联接状况很差。但是如果在较大抽样范围 (50到100) 内出现几个这样的情况也不必担心。

要退出ping, 则键入control-c。这激昂中止该程序并打印总结: 有多少信息包被传输，有多少信息包被接收到，丢失的信息包的比例，以及信息包来回时间的最低、最高和平均值。

ping是测试为了联接状况以及信息包发送和接收状况非常有用的工具。

对应的TTL值有什么特别的含意呢？

ttl每经过一个ip子层就减少1

UNIX 及类 UNIX 操作系统 ICMP 回显应答的 TTL 字段值为 255

Compaq Tru64 5.0 ICMP 回显应答的 TTL 字段值为 64

微软 Windows NT/2K操作系统 ICMP 回显应答的 TTL 字段值为 128

微软 Windows 95 操作系统 ICMP 回显应答的 TTL 字段值为 32

当然，返回的TTL值是相同的

但有些情况下有所特殊

LINUX Kernel 2.2.x & 2.4.x ICMP 回显应答的 TTL 字段值为 64

FreeBSD 4.1, 4.0, 3.4;
  
Sun Solaris 2.5.1, 2.6, 2.7, 2.8;
  
OpenBSD 2.6, 2.7,
  
NetBSD
  
HP UX 10.20
  
ICMP 回显应答的 TTL 字段值为 255

Windows 95/98/98SE
  
Windows ME
  
ICMP 回显应答的 TTL 字段值为 32

Windows NT4 WRKS
  
Windows NT4 Server
  
Windows 2000
  
ICMP 回显应答的 TTL 字段值为 128

这样，我们就可以通过这种方法来辨别

操作系统 TTL
  
LINUX 64
  
WIN2K/NT 128
  
WINDOWS 系列 32
  
UNIX 系列 255
