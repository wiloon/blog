---
title: 磁盘性能测试
author: "-"
date: 2023-05-18 09:26:55
url: disk/performance
categories:
  - Hardware
tags:
  - reprint
  - remix
---
## 磁盘性能测试

[https://blog.csdn.net/zqtsx/article/details/25487185](https://blog.csdn.net/zqtsx/article/details/25487185)

linux 下测试磁盘的读写 IO 速度 (IO物理测速)

## hdparm

这是一个是用来获取 ATA/IDE 硬盘的参数的命令, 是由早期 Linux IDE 驱动的开发和维护人员 Mark Lord 开发编写的 (hdparm has been written by Mark Lord, the primary developer and maintainer of the (E)IDE driver for Linux, with suggestions from many netfolk). 该命令应该也是仅用于 Linux 系统, 对于 UNIX 系统, ATA/IDE 硬盘用的可能比较少, 一般大型的系统都是使用磁盘阵列的.

```bash
hdparm -Tt /dev/sda
```

### options

- -t 评估硬盘的读取效率。
- -T 评估硬盘快取的读取效率。

/dev/sda:
  
Timing cached reads: 6676 MB in 2.00 seconds = 3340.18 MB/sec
  
Timing buffered disk reads: 218 MB in 3.11 seconds = 70.11 MB/sec

可以看到, 2秒钟读取了6676MB的缓存, 约合 3340.18 MB/sec;
  
在 3.11 秒中读取了 218MB 磁盘(物理读), 读取速度约合 70.11 MB/sec

## dd

这不是一个专业的测试工具, 不过如果对于测试结果的要求不是很苛刻的话, 平时可以使用来对磁盘的读写速度作一个简单的评估.
  
另外由于这是一个免费软件, 基本上 ×NIX 系统上都有安装, 对于 Oracle 裸设备的复制迁移, dd 一般都是首选.

首先了解两个特殊设备

- /dev/null 伪设备, 回收站. 写该文件不会产生 IO
- /dev/zero 伪设备, 会产生空字符流, 对它不会产生 IO

测试方法:

### 测试磁盘的 IO 写速度

time dd if=/dev/zero of=test.dbf bs=8k count=300000 如果要测试实际速度 还要在末尾加上 oflag=direct测到的才是真实的IO速度

b.测试磁盘的IO读速度

dd if=test.dbf bs=8k count=300000 of=/dev/null

表示 每次写入/读取8k的数据,执行300000次

dd命令可以通用,但不够专业,也没有考虑到缓存和物理读的区分,测试的数据也是仅作参考,不能算是权威。
  
##########################

用这个方法测试我08年买的笔记本,写速度23M/s；读速度91M/s

##########################

dd命令解释

dd if= of= bs= skip= seek= conv=

一定不要搞混 source 和 target,不然数据会丢失。所以 dd 平时用着顺手就叫它 dd,但是不小心把数据弄没了就该哭着叫它 Data Destroyer 了。

一般它的常用参数有:

bs=n,block size,每次读取 n bytes 写入,可与 count 联用；
  
ibs=n,一次读入 bytes 个字节 (default is 512)；
  
obs=n,一次性写 n bytes 个字节 (default is 512)；
  
bs 可以同时设置上边两个参数；
  
cbs=n,一次转换 n 个 bytes,即转换缓冲区大小。；
  
count=n, bs 操作的次数,仅拷贝 n 个块,如 dvd: bs=1M count=4430；
  
skip=n,指 if 后面的原文件跳过 n bytes 再开始读取；
  
seek=n,指 of 后面的目标文件跳过 n bytes 再开始写入；

测试IO同时读和写的速度

time dd if=/dev/sda1 of=test.dbf bs=8k

13048+1 records in
  
13048+1 records out
  
3.73s real 0.04s user 2.39s system

du -sm test.dbf

500 test.dbf  (同事测试读写速度时生成一个大小500M的 test.dbf文件)

上面测试的数据量比较小,仅作为参考.

相比两种方法:
  
前者是 linux 上专业的测试 IDE/ATA 磁盘的工具, 但是使用范围有局限性; (此试验仅仅使用了测试磁盘 IO 的参数,对于其他参数及解释参考 man 手册)
  
后者可以通用,但不够专业,也没有考虑到缓存和物理读的区分,测试的数据也是仅作参考,不能算是权威.

如果用dd测试,需要加oflag＝direct,测到的才是真实的磁盘io
