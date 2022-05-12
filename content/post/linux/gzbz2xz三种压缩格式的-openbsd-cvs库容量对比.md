---
title: gz,bz2,xz三种压缩格式的 OpenBSD CVS库容量对比
author: "-"
date: 2012-02-26T03:59:24+00:00
url: /?p=2451
categories:
  - Linux
tags:$
  - reprint
---
## gz,bz2,xz三种压缩格式的 OpenBSD CVS库容量对比

  gz,bz2,xz三种压缩格式的 OpenBSD CVS库容量对比

<hr size="1" />


  压缩gz格式速度最快，也是OpenBSD的常用格式，压缩bz2格式时间稍长一些，但似乎在好机器上还可以接受，xz格式的压缩效果确实不错，cvs.tar是打包的全部OpenBSD CVS库，原本大小有5G多，经过xz压缩后只有700多M，不得不说压缩算法确实强悍，不过压缩时间太长——在我的1300MHz主频的老机器上，将5G多的cvs打包文件压缩成xz格式用了两个小时左右，看来这种格式最好不作为日常采用的格式，但是如果作为放在服务器上供长期、大量下载的资源，使用这种压缩格式来进行压缩和解压尚可理解。 
  
    
      代码:
    
    
    # ls -la
total 14202000
drwxr-xr-x   3 root  wheel         512 Mar 25 21:18 .
drwxr-xr-x  15 root  wheel         512 Mar 25 16:35 ..
drwxr-xr-x  10 root  wheel         512 Mar 25 17:49 cvs
-rw-r--r--   1 root  wheel         387 Mar 25 16:40 cvs-supfile
-rw-r--r--   1 root  wheel  5208381440 Mar 25 21:18 cvs.tar
-rw-r--r--   1 root  wheel   898476333 Mar 25 21:03 cvs.tar.bz2
-rw-r--r--   1 root  wheel  1162675369 Mar 25 21:13 cvs.tar.gz
    
    
    
    http://www.jiarun.org/thread2600.html
  
