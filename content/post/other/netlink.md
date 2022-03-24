---
title: netlink
author: "-"
date: 2012-02-15T04:34:49+00:00
url: netlink
categories:
  - OS
tags:
  - reprint
---
## netlink

什么是Netlink通信机制

　  Netlink套接字是用以实现用户进程与内核进程通信的一种特殊的进程间通信(IPC) ,也是网络应用程序与内核通信的最常用的接口。

    Netlink 是一种特殊的 socket，它是 Linux 所特有的，类似于 BSD 中的AF_ROUTE 但又远比它的功能强大，目前在Linux 内核中
    使用netlink 进行应用与内核通信的应用很多; 包括：路由 daemon（NETLINK_ROUTE），用户态 socket 协议（NETLINK_USERSOCK），
    防火墙（NETLINK_FIREWALL），netfilter 子系统（NETLINK_NETFILTER），内核事件向用户态通知（NETLINK_KOBJECT_UEVENT），
    通用 netlink（NETLINK_GENERIC）等。
    
    Netlink 是一种在内核与用户应用间进行双向数据传输的非常好的方式，用户态应用使用标准的 socket API 就可以使用 netlink 提供的强大功能，
    内核态需要使用专门的内核 API 来使用 netlink。
    Netlink 相对于系统调用，ioctl 以及 /proc文件系统而言具有以下优点：
    1，netlink使用简单，只需要在include/linux/netlink.h中增加一个新类型的 netlink 协议定义即可,(如 #define NETLINK_TEST 20 然后，内核和用户态应用就可以立即通过 socket API 使用该 netlink 协议类型进行数据交换);
    2. netlink是一种异步通信机制，在内核与用户态应用之间传递的消息保存在socket缓存队列中，发送消息只是把消息保存在接收者的socket的接收队列，而不需要等待接收者收到消息；
    3．使用 netlink 的内核部分可以采用模块的方式实现，使用 netlink 的应用部分和内核部分没有编译时依赖;
    4．netlink 支持多播，内核模块或应用可以把消息多播给一个netlink组，属于该neilink 组的任何内核模块或应用都能接收到该消息，内核事件向用户态的通知机制就使用了这一特性；
    5．内核可以使用 netlink 首先发起会话;

>https://www.cnblogs.com/wenqiang/p/6306727.html
