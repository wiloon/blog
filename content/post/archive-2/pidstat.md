---
title: pidstat
author: "-"
date: 2018-03-22T01:26:36+00:00
url: pidstat
categories:
  - Linux
tags:
  - reprint
---
## pidstat
  
pidstat是sysstat中的工具，如需使用pidstat，要先安装sysstat，在这里就不说明了。

us过高
  
当us值过高时，表示运行的应用消耗了大部分的cpu。在这种情况下，对于java应用而言，最重要的是找到具体消耗cpu的线程所执行的代码，可以采用如下方法。

首先通过linux命令top命令查看us过高的pid值

通过top -Hp pid查看该pid进程下的线程的cpu消耗状况，得到具体pid值

将pid值转化为16进制，这个转化后的值对应nid值的线程

通过jstack pid grep -C 20 "16进制的值" 命令查看运行程序的线程信息

该线程就是消耗cpu的线程，在采样时须多执行几次上述的过程，以确保找到真实的消耗cpu的线程。

java应用造成us过高的原因主要是线程一直处于可运行的状态Runnable，通常是这些线程在执行无阻塞、循环、正则或纯粹的计算等动作造成。 另外一个可能会造成us过高的原因是频繁的gc。如每次请求都需要分配较多内存，当访问量高时就导致不断的进行gc，系统响应速度下降， 进而造成堆积的请求更多，消耗的内存严重不足，最严重的时候会导致系统不断进行FullGC，对于频繁的gc需要通过分析jvm内存的消耗来查找原因。

```bash
pidstat 1
pidstat PID -r 3
  
```

minflt/s
  
每秒次缺页错误次数(minor page faults),次缺页错误次数意即虚拟内存地址映射成物理内存地址产生的page fault次数

majflt/s
  
每秒主缺页错误次数(major page faults),当虚拟内存地址映射成物理内存地址时,相应的page在swap中,这样的page fault为major page fault,一般在内存使用紧张时产生

VSZ

Virtual Size: The virtual memory usage of entire task in kilobytes.
  
RSS

Resident Set Size: The non-swapped physical memory used by the task in kilobytes.

pidstat主要用于监控全部或指定进程占用系统资源的情况,如CPU,内存、设备IO、任务切换、线程等。pidstat首次运行时显示自系统启动开始的各项统计信息,之后运行pidstat将显示自上次运行该命令以后的统计信息。用户可以通过指定统计的次数和时间来获得所需的统计信息。

执行pidstat,将输出系统启动后所有活动进程的cpu统计信息:

复制代码
  
linux:~ # pidstat
  
Linux 2.6.32.12-0.7-default (linux) 06/18/12 _x86_64_

11:37:19 PID %usr %system %guest %CPU CPU Command
  
……
  
11:37:19 11452 0.00 0.00 0.00 0.00 2 bash
  
11:37:19 11509 0.00 0.00 0.00 0.00 3 dd
  
复制代码
  
指定采样周期和采样次数

pidstat命令指定采样周期和采样次数,命令形式为"pidstat [option] interval [count]",以下pidstat输出以2秒为采样周期,输出10次cpu使用统计信息:

pidstat 2 10

cpu使用情况统计(-u)

使用-u选项,pidstat将显示各活动进程的cpu使用统计,执行"pidstat -u"与单独执行"pidstat"的效果一样。

内存使用情况统计(-r)

使用-r选项,pidstat将显示各活动进程的内存使用统计:

复制代码
  
linux:~ # pidstat -r -p 13084 1
  
Linux 2.6.32.12-0.7-default (linux) 06/18/12 _x86_64_

15:08:18 PID minflt/s majflt/s VSZ RSS %MEM Command
  
15:08:19 13084 133835.00 0.00 15720284 15716896 96.26 mmmm
  
15:08:20 13084 35807.00 0.00 15863504 15849756 97.07 mmmm
  
15:08:21 13084 19273.87 0.00 15949040 15792944 96.72 mmmm
  
复制代码
  
以上各列输出的含义如下:

minflt/s: 每秒次缺页错误次数(minor page faults),次缺页错误次数意即虚拟内存地址映射成物理内存地址产生的page fault次数
  
majflt/s: 每秒主缺页错误次数(major page faults),当虚拟内存地址映射成物理内存地址时,相应的page在swap中,这样的page fault为major page fault,一般在内存使用紧张时产生
  
VSZ: 该进程使用的虚拟内存(以kB为单位)
  
RSS: 该进程使用的物理内存(以kB为单位)
  
%MEM: 该进程使用内存的百分比
  
Command: 拉起进程对应的命令

IO情况统计(-d)

使用-d选项,我们可以查看进程IO的统计信息:

复制代码
  
linux:~ # pidstat -d 1 2
  
Linux 2.6.32.12-0.7-default (linux) 06/18/12 _x86_64_

17:11:36 PID kB_rd/s kB_wr/s kB_ccwr/s Command
  
17:11:37 14579 124988.24 0.00 0.00 dd

17:11:37 PID kB_rd/s kB_wr/s kB_ccwr/s Command
  
17:11:38 14579 105441.58 0.00 0.00 dd
  
复制代码
  
输出信息含义

kB_rd/s: 每秒进程从磁盘读取的数据量(以kB为单位)
  
kB_wr/s: 每秒进程向磁盘写的数据量(以kB为单位)
  
Command: 拉起进程对应的命令

针对特定进程统计(-p)

使用-p选项,我们可以查看特定进程的系统资源使用情况:

复制代码
  
linux:~ # pidstat -r -p 1 1
  
Linux 2.6.32.12-0.7-default (linux) 06/18/12 _x86_64_

18:26:17 PID minflt/s majflt/s VSZ RSS %MEM Command
  
18:26:18 1 0.00 0.00 10380 640 0.00 init
  
18:26:19 1 0.00 0.00 10380 640 0.00 init
  
……
  
复制代码

pidstat常用命令
  
使用pidstat进行问题定位时,以下命令常被用到:

pidstat -u 1

pidstat -r 1

pidstat -d 1
  
以上命令以1秒为信息采集周期,分别获取cpu、内存和磁盘IO的统计信息。

转自 <http://www.cnblogs.com/bangerlee/articles/2555307.html>
