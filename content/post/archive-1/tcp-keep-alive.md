---
title: TCP Keep-Alives
author: "-"
date: 2013-10-20T05:48:51+00:00
url: /?p=5861
categories:
  - Uncategorized
tags:
  - linux
  - SSH

---
## TCP Keep-Alives

>https://zhuanlan.zhihu.com/p/28894266
>https://datatracker.ietf.org/doc/html/rfc1122#page-101

当客户端端等待超过一定时间后自动给服务端发送一个空的报文，如果对方回复了这个报文证明连接还存活着，如果对方没有报文返回且进行了多次尝试都是一样，那么就认为连接已经丢失，客户端就没必要继续保持连接了。如果没有这种机制就会有很多空闲的连接占用着系统资源。

KeepAlive并不是TCP协议规范的一部分，但在几乎所有的TCP/IP协议栈（不管是Linux还是Windows）中，都实现了KeepAlive功能。

如何设置它?
在设置之前我们先来看看KeepAlive都支持哪些设置项

KeepAlive默认情况下是关闭的，可以被上层应用开启和关闭
tcp_keepalive_time: KeepAlive的空闲时长，或者说每次正常发送心跳的周期，默认值为7200s（2小时）
tcp_keepalive_intvl: KeepAlive探测包的发送间隔，默认值为75s
tcp_keepalive_probes: 在tcp_keepalive_time之后，没有接收到对方确认，继续发送保活探测包次数，默认值为9（次）

在Linux内核设置
KeepAlive默认不是开启的，如果想使用KeepAlive，需要在你的应用中设置SO_KEEPALIVE才可以生效。

查看当前的配置：

cat /proc/sys/net/ipv4/tcp_keepalive_time
cat /proc/sys/net/ipv4/tcp_keepalive_intvl
cat /proc/sys/net/ipv4/tcp_keepalive_probes
在Linux中我们可以通过修改 /etc/sysctl.conf 的全局配置：

net.ipv4.tcp_keepalive_time=7200
net.ipv4.tcp_keepalive_intvl=75
net.ipv4.tcp_keepalive_probes=9
添加上面的配置后输入 sysctl -p 使其生效，你可以使用 sysctl -a | grep keepalive 命令来查看当前的默认配置

如果应用中已经设置SO_KEEPALIVE，程序不用重启，内核直接生效