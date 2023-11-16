---
title: Linux单机TCP并发连接
author: "-"
date: 2015-08-31T07:14:35+00:00
url: /?p=8204
categories:
  - Inbox
tags:
  - reprint
---
## Linux单机 TCP 并发连接

[http://blog.csdn.net/kobejayandy/article/details/47127991](http://blog.csdn.net/kobejayandy/article/details/47127991)

总结下服务端对于tcp连接的限制与提高tcp连接数的方法,可能工作中永远不会用到,但对于网络知识理解会有帮助。1.服务端与16位的端口号 (最大65535) 没什么关系
  
服务端ip+port(监听端口) + 客户端ip+port 决定了一条连接,客户端连接服务器后,服务端并没有又分配一个物理端口与客户端连接。其实所有的数据还是通过监听端口接收与发送的 (不论全双工与半双工,反正都是双工的) ,只不过多了一个逻辑上的socket。这些都应该是网卡上的事情,当接收到一个字节流的时候,网卡就会回调给操作系统,回调的时候会告诉操作系统客户端ip+port,假如是epoll模型,那么这次可能只接收了几个字节,回调那个新的socket的特定方法。然后下一次从监听端口回调上来的数据可能是另外的一个逻辑上的socket,各自互不影响。

2.内存限制
  
系统为每个TCP 连接分配一个TCP 控制块(TCP control block or TCB)。一个tcb控制块大概要占用1k多的内存,假如百万连接,1个tcb占用1k内存,那么就需要1G的内存了,这还是理想情况,一般情况下tcb要大于1k内存。当每个连接上在有数据传输的时候,同时需要的内存就更大了。

另外需要设置的tcp参数有tcp的读写缓冲区,默认为86k,都可以改成4k。此外需要修改tcp_mem的值。

tcp_mem(3个INTEGER变量): low, pressure, high
  
low: 当TCP使用了低于该值的内存页面数时,TCP不会考虑释放内存。
  
pressure: 当TCP使用了超过该值的内存页面数量时,TCP试图稳定其内存使用,进入pressure模式,当内存消耗低于low值时则退出pressure状态。
  
high: 允许所有tcp sockets用于排队缓冲数据报的页面量,当内存占用超过此值,系统拒绝分配socket,后台日志输出"TCP:
  
too many of orphaned sockets"。
  
3.文件句柄限制
  
每个socket都是一个文件句柄,linux下文件句柄限制,包括linux允许的最大文件句柄,linux允许的最大同时活动的文件句柄。

4.网卡限制
  
千兆网卡,上限满负荷工作,大概有600兆左右,单位为b,除以8为75k/单个连接。这个一般可以满足。

参考[http://www.blogjava.net/yongboy/archive/2013/04/11/397677.html](http://www.blogjava.net/yongboy/archive/2013/04/11/397677.html) linux下需要修改的地方有:
  
echo "* - nofile 1048576" >> /etc/security/limits.conf   #open file resource limit 是linux中process可以打开的文件句柄数量。
  
echo "fs.file-max = 1048576" >> /etc/sysctl.conf    #系统最大允许的文件描述符
  
echo "net.ipv4.ip_local_port_range = 1024 65535" >> /etc/sysctl.conf   #可以使用的端口范围,主要为了测试时候使用
  
echo "net.ipv4.tcp_mem = 786432 2097152 3145728" >> /etc/sysctl.conf   #见上
  
echo "net.ipv4.tcp_rmem = 4096 4096 16777216" >> /etc/sysctl.conf
  
echo "net.ipv4.tcp_wmem = 4096 4096 16777216" >> /etc/sysctl.conf
  
在参考文章中,建立100w的连接,大概使用了7500M的内存,每个连接大概7.5k的内存 (主要是读写缓冲区,tcb的大小) 。

另外,通过修改系统配置达到100w连接并不难,但是要是真正实现并发100w业务的处理还是很困难的。
