---
title: partx
author: "-"
date: 2017-11-13T09:22:22+00:00
url: /?p=11418
categories:
  - Inbox
tags:
  - reprint
---
## partx
http://gulingzi.blog.51cto.com/2208376/1561403

/proc/partitions 记录了系统中所有硬盘及其上面的分区,包括已挂载和未挂载的。
  
有些硬盘没有记录分区信息,可能是没有分区,或者未记录

对于分区完成,但是尚未挂载的硬盘分区,partx告诉内核去做登记,以备挂载。
  
partx 告诉内核去识别、登记某个硬盘上的分区信息。并不是加载,只是识别并记录而已。
      
或者删除某个分区的记录。

-a 登记某块盘上的所有分区信息,如果某个分区信息已有记录,就会报错: 
    
BLKPG: Device or resource busy
    
error adding partition 4

如果某磁盘上的分区信息都没有被记录,则安静完成。

-d 删除内核中关于某磁盘上的所有分区的记录 (不是卸载) 
  
-d -nr m-n 删除从第m-n分区的记录

如果已经挂载,则无法删除,并报错: 
  
error deleting partition 5: BLKPG: Device or resource busy

如果都删除了,使用-a选项来重新登记,不会有报错。

一般分区完成后,系统会识别到。

-l 列出某磁盘上的分区情况。数据从磁盘上获取,并不是来源于/proc/partitions