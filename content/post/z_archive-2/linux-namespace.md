---
title: linux Namespace
author: "-"
date: 2018-07-31T08:40:02+00:00
url: /?p=12469
categories:
  - Inbox
tags:
  - reprint
---
## linux Namespace
https://lwn.net/Articles/531114/
  
https://coolshell.cn/articles/17010.html

Linux Namespace是Linux提供的一种内核级别环境隔离的方法。
  
chroot内部的文件系统无法访问外部的内容。Linux Namespace在此基础上,提供了对UTS、IPC、mount、PID、network、User等的隔离机制。
  
UTS Namespace
  
IPC全称 Inter-Process Communication, 是 Unix/Linux下进程间通信的一种方式, IPC 有共享内存、信号量、消息队列等方法。