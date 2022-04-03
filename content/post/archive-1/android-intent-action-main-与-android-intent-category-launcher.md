---
title: 文件系统，block组，block，bmap，inode，inode table，imap
author: "-"
date: 2014-04-14T08:06:08+00:00
url: imap
categories:
  - Uncategorized

tags:
  - reprint
---
## 文件系统，block组，block，bmap，inode，inode table，imap

文件系统 imap：inode 节点位图(inodemap)管理空闲inode

摘取自骏马金龙的第4章ext文件系统机制原理剖析

在写文件(Linux中一切皆文件)时需要为其分配一个inode号。

其实，在格式化创建文件系统后，所有的inode号都已计算好（创建文件系统时会为每个块组计算好该块组拥有哪些inode号），因此产生了问题：要为文件分配哪一个inode号呢？又如何知道某一个inode号是否已经被分配了呢？

既然是"是否被占用"的问题，使用位图是最佳方案，像bmap记录block的占用情况一样。标识inode号是否被分配的位图称为inodemap简称为imap。这时要为一个文件分配inode号只需扫描imap即可知道哪一个inode号是空闲的。

这样理解更容易些，类似bmap块位图一样，inode号是预先规划好的。inode号分配后，文件删除也会释放inode号。分配和释放的inode号，像是在一个地图上挖掉一块，用完再补回来一样。

imap存在着和bmap和inode table一样需要解决的问题：如果文件系统比较大，imap本身就会很大，每次存储文件都要进行扫描，会导致效率不够高。同样，优化的方式是将文件系统占用的block划分成块组，每个块组有自己的imap范围。

>https://www.jianshu.com/p/4a07b2c26879