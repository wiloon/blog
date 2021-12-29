---
title:  页缓存, Page Cache
author: "-"
date: 2011-10-29T08:30:33+00:00
url: page-cache
categories:
  - OS
tags:
  - file

---
 我们知道文件一般存放在硬盘（机械硬盘或固态硬盘）中，CPU 并不能直接访问硬盘中的数据，而是需要先将硬盘中的数据读入到内存中，然后才能被 CPU 访问。

由于读写硬盘的速度比读写内存要慢很多（DDR4 内存读写速度是机械硬盘500倍，是固态硬盘的200倍），所以为了避免每次读写文件时，都需要对硬盘进行读写操作，Linux 内核使用 页缓存（Page Cache） 机制来对文件中的数据进行缓存。

本文使用的 Linux 内核版本为：Linux-2.6.23

什么是页缓存
为了提升对文件的读写效率，Linux 内核会以页大小（4KB）为单位，将文件划分为多数据块。当用户对文件中的某个数据块进行读写操作时，内核首先会申请一个内存页（称为 页缓存）与文件中的数据块进行绑定。

>https://cloud.tencent.com/developer/article/1848933
>https://qinglinmao8315.github.io/linux/2018/03/14/linux-page-cache.html
>https://zhuanlan.zhihu.com/p/35277219
