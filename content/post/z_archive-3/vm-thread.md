---
title: VM Thread
author: "-"
date: 2019-10-11T10:19:34+00:00
url: /?p=14988
categories:
  - Inbox
tags:
  - reprint
---
## VM Thread
VM Thread是JVM层面的一个线程，主要工作是对其他线程的创建，分配和对象的清理等工作的。
  
cpu 100% 通常的思路是查看runnable的线程，但如果发现是耗尽cpu的是vmthread

多半会伴随old区已满 (此时垃圾回收已停止) ，通常这是由于在并发下短时间内创建很多对象造成。

https://my.oschina.net/zhangxufeng/blog/1613808