---
title: /proc
author: "-"
date: 2011-10-27T23:19:33+00:00
url: proc
categories:
  - OS
tags:
  - reprint
---
## /proc

在GUN/Linux操作系统中，/proc 是一个位于内存中的伪文件系统(in-memory pseudo-file system)。该目录下保存的不是真正的文件和目录，而是一些“运行时”信息，如系统内存、磁盘io、设备挂载信息和硬件配置信息等。proc目录是一个控制中心，用户可以通过更改其中某些文件来改变内核的运行状态。proc目录也是内核提供给我们的查询中心，我们可以通过这些文件查看有关系统硬件及当前正在运行进程的信息。在Linux系统中，许多工具的数据来源正是proc目录中的内容。例如，lsmod命令就是cat /proc/modules命令的别名，lspci命令是cat /proc/pci命令的别名。

### cat /proc/pagetypeinfo

查看内存碎片情况

cat / proc / pagetypeinfo

我看到三种types的内存区域;

DMA
DMA32
正常
Linux如何select一个内存区域来分配一个新的页面？

写入/读取受内存保护的进程的内存
我怎样才能减less最小的Linux进程的内存占用量
区分Java应用程序mmaped内存和Linux上的JVM mmapped内存
使用C用户空间代码读取Linux / proc接口的最佳方法是什么？
在Linux程序中跟踪积极使用的内存
找出一个进程在Linux上使用多less内存页面
OSError：无法从python subprocess.call分配内存
python subprocess.Popen错误与OSError：一段时间后不能分配内存
Shell脚本循环在CygWin下耗尽内存
在fork (）中重复的段？
这些内存区域仅为32位系统定义，而不在64位中定义。

记住这些是我们正在讨论的内核可访问的main memory 。 在32 bit  (4GB）系统中，内核与用户空间之间的分割为1:3 。 含义内核可以访问1GB和用户空间3GB。 内核的1GB分割如下：

Zone_DMA (0-16MB）： 永久映射到内核地址空间。
出于兼容性原因，较旧的ISA设备只能处理较低的16MB主内存。

Zone_Normal (16MB-896MB）： 永久映射到内核地址空间。
许多内核操作只能使用ZONE_NORMAL所以它是性能最关键的区域，并且是内核主要分配的内存。

ZONE_HIGH_MEM (896MB以上）： 没有永久映射到内核的地址空间。
内核可以访问整个4GB的主内存。 内核的1GB通过Zone_DMA ＆ Zone_Normal和用户的3GB通过ZONE_HIGH_MEM 。 使用英特尔的Physical Address Extension (PAE) ，可以获得4个额外的位来寻址主存储器，产生36位，总共可以访问64GB的内存。 增量地址空间 (36位地址 – 32位地址）是ZONE_HIGH_MEM用于映射到用户访问的主存储器 (即2GB – 4GB之间）的位置。

阅读更多：

<http://www.quora.com/Linux-coreel/Why-is-there-ZONE_HIGHMEM-in-the-x86-32-Linux-kernel-but-not-in-the-x86-64-kernel>
<http://www.quora.com/Linux-coreel/What-is-the-difference-between-high-memory-and-normal-memory>
Linux 3/1虚拟地址分割

<https://zhuanlan.zhihu.com/p/26923061>
