---
title: ConcurrentLinkedQueue
author: "-"
date: 2018-01-03T13:52:10+00:00
url: ConcurrentLinkedQueue
categories:
  - Java
tags:
  - reprint
---
## ConcurrentLinkedQueue

<http://www.infoq.com/cn/articles/ConcurrentLinkedQueue>

一个基于链接节点的无界线程安全队列。此队列按照 FIFO（先进先出）原则对元素进行排序。队列的头部 是队列中时间最长的元素。队列的尾部 是队列中时间最短的元素。
新的元素插入到队列的尾部，队列获取操作从队列头部获得元素。当多个线程共享访问一个公共 collection 时，ConcurrentLinkedQueue 是一个恰当的选择。此队列不允许使用 null 元素。

<https://www.cnblogs.com/yangzhenlong/p/8359875.html>

ConcurrentLinkedQueue是Queue的一个安全实现．Queue中元素按FIFO原则进行排序．采用CAS操作，来保证元素的一致性。

<https://blog.51cto.com/u_15259710/3193985>
<https://juejin.cn/post/6844903602427805704>
