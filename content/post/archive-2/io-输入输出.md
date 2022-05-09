---
title: IO, 输入输出
author: "-"
date: 2018-07-04T06:39:14+00:00
url: /?p=12393
categories:
  - Inbox
tags:
  - reprint
---
## IO, 输入输出
https://my.oschina.net/u/1859679/blog/1839169

同步阻塞IO

同步非阻塞IO

异步非阻塞IO
  
针对某种IO模型,我们如何分类,可以基于POSIX对同步/异步的定义来判别:

  * A synchronous I/O operation causes the requesting process to be blocked until that I/O operation completes; 
  * An asynchronous I/O operation does not cause the requesting process to be blocked;
  
    那么从上我们可以看出:

阻塞: 是否阻塞主要体现在调用的线程是否可以干别的,关注的是程序的等待状态

同步: 是否同步体现在消息通信机制上 。

也就是说同步和异步说的是消息的通知机制,阻塞非阻塞说的是线程的状态 。

Unix 5种I/O模型
  
在《UNIX网络编程: 卷一》的第六章书中列出了五种IO模型: 

阻塞式I/O；

非阻塞式I/O；

I/O复用 (select,poll,epoll...) ；

信号驱动式I/O (SIGIO) ；

异步I/O (POSIX的 aio 系列函数