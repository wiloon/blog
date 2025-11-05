---
title: cpu 占用分析
author: "-"
date: 2013-12-10T01:17:00+00:00
url: /?p=6032
categories:
  - cs
tags:
  - reprint
---
## cpu瓶颈分析

```bash
#系统的平均负载
uptime
# 每个 CPU 的使用情况
mpstat
# 每个进程 CPU 的使用情况
pidstat

stress
```

* stress [https://www.hi-linux.com/posts/59095.html](https://www.hi-linux.com/posts/59095.html)
  
    [https://www.infoq.cn/article/5jjIdOPx12RWWvGX_H9J?utm_source=rss&utm_medium=article](https://www.infoq.cn/article/5jjIdOPx12RWWvGX_H9J?utm_source=rss&utm_medium=article)
  
    [http://9leg.com/java/2016/08/09/cpu-consumption-analysis.html](http://9leg.com/java/2016/08/09/cpu-consumption-analysis.html)

通常性能瓶颈的表现是资源消耗过多、外部处理系统的性能不足，或者资源消耗不多，但程序的响应速度却达不到要求。

资源主要消耗在cpu，io (又分文件io和网络io) ，内存方面，机器的资源是有限的，当某资源消耗过多时，通常会造成系统的响应速度变慢。

对于java应用而言，寻找性能瓶颈的方法通常为首先分析资源的消耗，然后结合java的一些工具来查找程序中造成资源消耗过多的代码。

今天先谈一谈cpu消耗如何分析，系统为linux，jdk为sun jdk。

在linux中，cpu主要用于中断、内核和用户进程的任务处理，优先级为中断>内核>用户进程，下面先讲述三个重要的概念。

### 上下文切换

每个cpu (多核cpu中的每个cpu) 在同一时间只能执行一个线程，linux采用的是抢占式调度。为每个线程分配一定的执行时间， 当到达执行时间、线程中有io阻塞或高优先级的线程要执行时，linux将切换执行的线程，在切换时要存储目前的线程的执行状态， 并恢复要执行的线程的状态，这个过程就是上下文切换。对于java应用而言，典型的是在进行文件io操作、网络io操作、锁等待或者线程sleep时， 当前线程会进入阻塞或休眠状态，从而触发上下文切换，上下文切换过多会造成内核占据较多的cpu使用，从而使应用响应速度变慢。

### 运行队列
  
每个cpu核都会维护一个可运行的线程队列，例如一个4核的cpu，java应用里启动了8个线程，且这8个线程都处于可运行状态， 那么在分配平均的情况下每个cpu中的运行队列就会有2个线程。通常而言，系统的load主要由cpu运行队列来决定。

利用率
  
cpu利用率为cpu在用户进程、内核、中断处理、io等待以及空闲5个部分使用的百分比，这5个值是用来分析cpu消耗的关键指标。 在linux中，可通过top或pidstat方式来查看进程中线程的cpu的消耗状况。

* top

输入top命令后既可查看cpu的消耗情况，cpu的信息在top视图的上面几行中

对于多个或多核cpu，上面的显示则会是多个cpu所占用的百分比总合。如需查看每个核的消耗情况，可在进入top视图后按1，就会按核来显示消耗情况。

cpu-top

默认情况下，top视图中显示的为进程的cpu消耗状况，在top视图中按shift + h后，可按线程查看cpu的消耗状况，此时的pid既为线程id。

* pidstat

### sy过高

当sy值过高时，表示linux花费了更多的时间在进行线程切换。java应用造成这种现象的主要原因是启动的线程比较多， 且这些线程多处于不断的阻塞 (例如锁等待，io等待) 和执行状态的变化过程中，这就导致了操作系统要不断的切换执行的线程， 产生大量的上下文切换。在这种情况下，对java应用而言，最重要的是找出不断切换状态的原因， 可采用的方法为通过kill -3 pid 或jstack -l pid的方法dump出java应用程序的线程信息，查看线程的状态信息以及锁信息， 找出等待状态或锁竞争过多的线程。

进程和线程的上下文切换都涉及进出系统内核和寄存器的保存和还原，这是它们的最大开销。但与进程的上下文切换相比，线程还是要轻量一些， 最大的区别是线程上下文切换时虚拟内存地址保持不变，所以像TLB等CPU缓存不会失效。但要注意的是另一份提问 What is the overhead of a context-switch?的中提到了: Intel和AMD在2008年引入的技术可能会使TLB不失效。

>[http://itindex.net/detail/54482-netty-%E5%BC%80%E5%8F%91-%E4%B8%AD%E9%97%B4%E4%BB%B6](http://itindex.net/detail/54482-netty-%E5%BC%80%E5%8F%91-%E4%B8%AD%E9%97%B4%E4%BB%B6)
>[http://www.infoq.com/cn/articles/netty-high-performance](http://www.infoq.com/cn/articles/netty-high-performance)
