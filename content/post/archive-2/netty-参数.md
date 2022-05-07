---
title: netty tcp 参数
author: "-"
date: 2015-12-19T13:19:28+00:00
url: /?p=8572
categories:
  - Inbox
tags:
  - reprint
---
## netty tcp 参数

### TCP_NODELAY

这个选项的作用就是禁用 Nagle's Algorithm
NAGLE算法通过将缓冲区内的小封包自动相连,组成较大的封包,阻止大量小封包的发送阻塞网络,从而提高网络应用效率。但是对于时延敏感的应用场景需要关闭该优化算法；

SO_RCVBUF 接收缓冲区

SO_SNDBUF 发送缓冲区

SO_KEEPALIVE 保持连接检测对方主机是否崩溃,避免 (服务器) 永远阻塞于TCP连接的输入。

设置该选项后, 如果2小时内在此 socket 的任一方向都没有数据交换, TCP就自动给对方发一个保持存活探测分节 (keepalive probe)。

SO_REUSEADDR

SO_BACKLOG

The `backlog` argument is the requested maximum number of pending connections on the socket.

## SO_RCVBUF ,SO_SNDBUF

每个TCP socket在内核中都有一个发送缓冲区和一个接收缓冲区,TCP的全双工的工作模式以及TCP的滑动窗口便是依赖于这两个独立的buffer以及此buffer的填充状态。接收缓冲区把数据缓存入内核,应用进程一直没有调用read进行读取的话,此数据会一直缓存在相应socket的接收缓冲区内。再啰嗦一点,不管进程是否读取socket,对端发来的数据都会经由内核接收并且缓存到socket的内核接收缓冲区之中。read所做的工作,就是把内核缓冲区中的数据拷贝到应用层用户的buffer里面,仅此而已。进程调用send发送的数据的时候,最简单情况 (也是一般情况) ,将数据拷贝进入socket的内核发送缓冲区之中,然后send便会在上层返回。换句话说,send返回之时,数据不一定会发送到对端去 (和write写文件有点类似) ,send仅仅是把应用层buffer的数据拷贝进socket的内核发送buffer中。后续我会专门用一篇文章介绍read和send所关联的内核动作。每个UDP socket都有一个接收缓冲区,没有发送缓冲区,从概念上来说就是只要有数据就发,不管对方是否可以正确接收,所以不缓冲,不需要发送缓冲区。

接收缓冲区被TCP和UDP用来缓存网络上来的数据,一直保存到应用进程读走为止。对于TCP,如果应用进程一直没有读取,buffer满了之后,发生的动作是: 通知对端TCP协议中的窗口关闭。这个便是滑动窗口的实现。保证TCP socket 接收缓冲区不会溢出,从而保证了TCP是可靠传输。因为对方不允许发出超过所通告窗口大小的数据。 这就是TCP的流量控制,如果对方无视窗口大小而发出了超过窗口大小的数据,则接收方TCP将丢弃它。 UDP: 当 socket 接收缓冲区满时,新来的数据报无法进入接收缓冲区,此数据报就被丢弃。UDP是没有流量控制的；快的发送者可以很容易地就淹没慢的接收者,导致接收方的UDP丢弃数据报。
  
以上便是TCP可靠,UDP不可靠的实现。
  
这两个选项就是来设置TCP连接的两个buffer尺寸的。

   /**

               * 100 Continue


               * 是这样的一种情况: HTTP客户端程序有一个实体的主体部分要发送给服务器,但希望在发送之前查看下服务器是否会


               * 接受这个实体,所以在发送实体之前先发送了一个携带100


               * Continue的Expect请求首部的请求。服务器在收到这样的请求后,应该用 100 Continue或一条错误码来进行响应。


               */

<http://www.cnblogs.com/qq78292959/archive/2013/01/18/2865926.html>

<http://elf8848.iteye.com/blog/1961192>

<http://blog.chinaunix.net/uid-29075379-id-3905006.html>

<http://blog.csdn.net/russell_tao/article/details/18711023>
