---
title: vmstat
author: "-"
date: 2017-03-31T01:31:46+00:00
url: vmstat
categories:
  - Linux
tags:
  - reprint
  - Command
---
## vmstat

```bash
vmstat -SM 1
vmstat 1 10
# vmstat每2秒采集数据,一直采集,直到结束程序
vmstat 2

# 2表示每两秒采集一次服务器状态,1表示只采集一次。
vmstat 2 1
```

vmstat命令是最常见的 Linux/Unix 监控工具, 可以展现给定时间间隔的服务器的状态值, 包括服务器的 CPU 使用率, 内存使用, 虚拟内存交换情况, IO读写情况。 相比 top, vmstat 可以看到整个机器的 CPU,内存,IO 的使用情况,而不是单单看到各个进程的 CPU 使用率和内存使用率(使用场景不一样)。

```bash
    -S: 输出信息的单位, (k: 1000, K:1024 , m: 1000000, M: 1048576) bytes, -S, --unit CHAR
    -a: 显示活动内页
    -f: 显示启动后创建的进程总数；
    -m: 显示slab信息；
    -n: 头信息仅显示一次
    -s: 以表格方式显示事件计数器和内存状态；
    -d: 报告磁盘状态；
    -p: 显示指定的硬盘分区状态;
```

一般vmstat工具的使用是通过两个数字参数来完成的,第一个参数是采样的时间间隔数,单位是秒,第二个参数是采样的次数,如:

### 输出的字段

### r

表示运行队列(就是说多少个进程真的分配到CPU),我测试的服务器目前CPU比较空闲,没什么程序在跑,当这个值超过了CPU数目,就会出现CPU瓶颈了。这个也和top的负载有关系,一般负载超过了3就比较高,超过了5就高,超过了10就不正常了,服务器的状态很危险。top的负载类似每秒的运行队列。如果运行队列过大,表示你的CPU很繁忙,一般会造成CPU使用率很高。

### b

表示阻塞的进程,这个不多说,进程阻塞,大家懂的。

### swpd

swap 的使用量  
虚拟内存已使用的大小, 如果大于0, 表示你的机器物理内存不足了, 如果不是程序内存泄露的原因, 那么你该升级内存了或者把耗内存的任务迁移到其他机器。

### free

空闲的物理内存的大小,我的机器内存总共8G,剩余3415M。

### buff

块设备 (block device) 所占用的缓存页, 包括: 直接读写块设备、以及文件系统元数据 (metadata) 比如 SuperBlock 所使用的缓存页；
  
buffers are only used for file metadata (inodes, etc) and data from raw block devices. It's accessed via block device and block number.

### cache

直接用来记忆我们打开的文件,给文件做缓冲,我本机大概占用300多M(这里是Linux/Unix的聪明之处,把空闲的物理内存的一部分拿来做文件和目录的缓存,是为了提高 程序执行的性能,当程序使用内存时,buffer/cached会很快地被使用。);表示普通文件数据所占用的缓存页。
  
Cache has file data blocks, and memory mapped information (i.e. files mapped with mmap() calls). It's accessed primarily via inode number.

### si

每秒从磁盘读入虚拟内存的大小,如果这个值大于0,表示物理内存不够用或者内存泄露了,要查找耗内存进程解决掉。我的机器内存充裕,一切正常。

- so
每秒虚拟内存写入磁盘的大小,如果这个值大于0,同上。

### bi (block input)

每秒读取的块数 (读磁盘）
bi 块设备每秒接收的块数量,这里的块设备是指系统上所有的磁盘和其他块设备,默认块大小是1024byte,我本机上没什么IO操作,所以一直是0,但是我曾在处理拷贝大量数据(2-3T)的机器上看过可以达到140000/s,磁盘写入速度差不多140M每秒

### bo (block output)

每秒写入的块数 (写磁盘）
bo 块设备每秒发送的块数量,例如我们读取文件,bo就要大于0。bi和bo一般都要接近0,不然就是IO过于频繁,需要调整。

### in 中断

in 每秒CPU的中断次数,包括时间中断

### cs 上下文切换

cs 每秒上下文切换次数, 例如我们调用系统函数,就要进行上下文切换,线程的切换,也要进程上下文切换,这个值要越小越好,太大了,要考虑调低线程或者进程的数目,例如在apache和nginx这种web服务器中,我们一般做性能测试时会进行几千并发甚至几万并发的测试,选择web服务器的进程可以由进程或者线程的峰值一直下调,压测,直到cs到一个比较小的值,这个进程和线程数就是比较合适的值了。系统调用也是,每次调用系统函数,我们的代码就会进入内核空间,导致上下文切换,这个是很耗资源,也要尽量避免频繁调用系统函数。上下文切换次数过多表示你的CPU大部分浪费在上下文切换,导致CPU干正经事的时间少了,CPU没有充分利用,是不可取的。

### us

us 用户CPU时间,我曾经在一个做加密解密很频繁的服务器上,可以看到us接近100,r运行队列达到80(机器在做压力测试,性能表现不佳)

### sy

sy 系统CPU时间,如果太高,表示系统调用时间长,例如是IO操作频繁。

### id

id 空闲 CPU时间,一般来说,id + us + sy = 100,一般我认为id是空闲CPU使用率,us是用户CPU使用率,sy是系统CPU使用率。

### wa

wa 等待IO CPU时间。

### st

虚拟机偷取的时间所占的百分比

-a, --active
    显示活跃和非活跃内存
-f, --forks
    显示从系统启动至今的 fork 数量 。这包括 fork、vfork 和 clone 系统调用，并相当于创建的任务总数。每个进程由一个或多个任务表示，这取决于线程的使用情况
-m, --slabs
    显示 slabinfo
-n, --one-header
    只在开始时显示一次各字段名称
-s, --stats
    显示各种事件计数器和内存统计信息的表
-D, --disk-sum
    报告一些有关磁盘活动的汇总统计数据
-d, --disk
    显示磁盘相关统计信息
-p, --partition DEVICE
    显示指定磁盘分区统计信息
-S, --unit CHAR
    使用指定单位显示。CHAR 可取值有 k (1000）、K (1024）、m (1000000） 、M (1048576）。默认单位为 K (1024 Bytes）
-t, --timestamp
    将时间戳附加到每行
-w, --wide
    宽输出模式，输出大于 80 个字符/行
-h, --help
    显示帮助信息并退出
-V, --version
    显示版本信息并退出

---

<http://www.cnblogs.com/ggjucheng/archive/2012/01/05/2312625.html>  
<http://man.linuxde.net/vmstat>  
<http://linuxperf.com/?p=32>  
<http://linuxperf.com/?p=32&embed=true#?secret=w2eizeWWHO>  
<http://netcome.iteye.com/blog/754548>
