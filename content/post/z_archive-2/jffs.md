---
title: JFFS
author: "-"
date: 2018-04-06T02:08:48+00:00
url: /?p=12117
categories:
  - Inbox
tags:
  - reprint
---
## JFFS
JFFS 是一个特别针对闪存的文件系统
  
JFFS v1 最初是由瑞典的 Axis Communications AB 公司开发的,使用在他们的嵌入式设备中,并且在 1999 年末基于 GNU GPL 发布出来。最初的发布版本基于 Linux 内核 2.0,后来 RedHat 将它移植到 Linux 内核 2.2,做了大量的测试和 bug fix 的工作使它稳定下来,并且对签约客户提供商业支持。但是在使用的过程中,JFFS v1 设计中的局限被不断的暴露出来。于是在 2001 年初的时候,RedHat 决定实现一个新的闪存文件系统,这就是现在的 JFFS2。下面将详细介绍 JFFS2 设计中主要的思想,关键的数据结构和垃圾收集机制。这将为我们实现一个闪存上的文件系统提供很好的启示。 首先,JFFS2 是一个日志结构(log-structured)的文件系统,包含数据和原数据(meta-data)的节点在闪存上顺序的存储。JFFS2 之所以选择日志结构的存储方式,是因为对闪存的更新应该是 out-of-place 的更新方式,而不是对磁盘的 in-place 的更新方式。

JFFS3 简介
  
虽然不断有新的补丁程序来提高 JFFS2 的性能,但是不可扩展性是它最大的问题,但是这是它自身设计的先天缺陷,是没有办法靠后天来弥补的。因此我们需要一个全新的文件系统,而 JFFS3 就是这样的一个文件系统,JFFS3 的设计目标是支持大容量闪存(>1TB)的文件系统。JFFS3 与 JFFS2 在设计上根本的区别在于,JFFS3 将索引信息存放在闪存上,而 JFFS2将索引信息保存在内存中。比如说,由给定的文件内的偏移定位到存储介质上的物理偏移地址所需的信息,查找某个目录下所有的目录项所需的信息都是索引信息的一种。 JFFS3 现在还处于设计阶段,文件系统的基本结构借鉴了 Reiser4 的设计思想,整个文件系统就是一个 B+ 树。JFFS3 的发起者正工作于垃圾回收机制的设计,这是 JFFS3 中最复杂,也是最富有挑战性的部分。JFFS3 的设计文档可以在http://www.linux-mtd.infradead.org/doc/jffs3.html 得到

https://www.ibm.com/developerworks/cn/linux/l-jffs2/