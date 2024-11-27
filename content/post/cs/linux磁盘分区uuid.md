---
title: Linux磁盘分区UUID, blkid
author: "-"
date: 2017-11-19T07:03:53+00:00
url: /?p=11448
categories:
  - Inbox
tags:
  - reprint
---
## Linux 磁盘分区 UUID, blkid

[http://tiger2020.blog.51cto.com/723949/1535774](http://tiger2020.blog.51cto.com/723949/1535774)

查看设备的 uuid 的三种方法, 总结如下:
  
1 命令查看: blkid
  
2 文件查看: ls -l /dev/disk/by-uuid
  
3 命令查看: vol_id /dev/sda1

UUID的作用及意义
  
1: 它是真正的唯一标志符
  
UUID为系统中的存储设备提供唯一的标识字符串,不管这个设备是什么类型的。如果你在系统中启动的时候,使用盘符挂载时,可能找不到设备而加载失败,而使用UUID挂载时,则不会有这样的问题。
  
2: 设备名并非总是不变的
  
自动分配的设备名称并非总是一致的,它们依赖于启动时内核加载模块的顺序。如果你在插入了USB盘时启动了系统,而下次启动时又把它拔掉了,就有可能导致设备名分配不一致。
  
使用UUID对于挂载移动设备也非常有好处,它支持各种各样的卡,而使用UUID总可以使同一块卡挂载在同一个地方。
  
3: Ubuntu中的许多关键功能现在开始依赖于UUID
