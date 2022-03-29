---
title: GC日志
author: "-"
date: 2013-06-27T08:24:58+00:00
url: /?p=5584
categories:
  - Uncategorized

tags:
  - reprint
---
## GC日志
本文是 Plumbr 发行的 Java垃圾收集指南 的部分内容。文中将介绍GC日志的输出格式, 以及如何解读GC日志, 从中提取有用的信息。我们通过 -XX:+UseSerialGC 选项,指定JVM使用串行垃圾收集器, 并使用下面的启动参数让 JVM 打印出详细的GC日志:

-XX:+PrintGCDetails
  
-XX:+PrintGCDateStamps
  
-XX:+PrintGCTimeStamps
  
这样配置以后，发生GC时输出的日志就类似于下面这种格式(为了显示方便,已手工折行):

2015-05-26T14:45:37.987-0200: 151.126:
    
[GC (Allocation Failure) 151.126:
      
[DefNew: 629119K->69888K(629120K), 0.0584157 secs]
      
1619346K->1273247K(2027264K), 0.0585007 secs]
    
[Times: user=0.06 sys=0.00, real=0.06 secs]

2015-05-26T14:45:59.690-0200: 172.829:
    
[GC (Allocation Failure) 172.829:
      
[DefNew: 629120K->629120K(629120K), 0.0000372 secs]
      
172.829: [Tenured: 1203359K->755802K(1398144K), 0.1855567 secs]
      
1832479K->755802K(2027264K),
      
[Metaspace: 6741K->6741K(1056768K)], 0.1856954 secs]
    
[Times: user=0.18 sys=0.00, real=0.18 secs]
  
上面的GC日志暴露了JVM中的一些信息。事实上，这个日志片段中发生了 2 次垃圾回收事件(Garbage Collection events)。其中一次清理的是年轻代(Young generation), 而第二次处理的是整个堆内存。下面我们来看，如何解读第一次GC事件，发生在年轻代中的小型GC(Minor GC):

2015-05-26T14:45:37.987-02001:151.1262:[GC3(Allocation Failure4)
  
151.126: [DefNew5:629119K->69888K6(629120K)7
  
, 0.0584157 secs]1619346K->1273247K8(2027264K)9,0.0585007 secs10]
  
[Times: user=0.06 sys=0.00, real=0.06 secs]11

2015-05-26T14:45:37.987-0200 – GC事件(GC event)开始的时间点.
  
151.126 – GC时间的开始时间,相对于JVM的启动时间,单位是秒(Measured in seconds).
  
GC – 用来区分(distinguish)是 Minor GC 还是 Full GC 的标志(Flag). 这里的 GC 表明本次发生的是 Minor GC.
  
Allocation Failure – 引起垃圾回收的原因. 本次GC是因为年轻代中没有任何合适的区域能够存放需要分配的数据结构而触发的.
  
DefNew – 使用的垃圾收集器的名字. DefNew 这个名字代表的是: 单线程(single-threaded), 采用标记复制(mark-copy)算法的, 使整个JVM暂停运行(stop-the-world)的年轻代(Young generation) 垃圾收集器(garbage collector).
  
629119K->69888K – 在本次垃圾收集之前和之后的年轻代内存使用情况(Usage).
  
(629120K) – 年轻代的总的大小(Total size).
  
1619346K->1273247K – 在本次垃圾收集之前和之后整个堆内存的使用情况(Total used heap).
  
(2027264K) – 总的可用的堆内存(Total available heap).
  
0.0585007 secs – GC事件的持续时间(Duration),单位是秒.
  
[Times: user=0.06 sys=0.00, real=0.06 secs] – GC事件的持续时间,通过多种分类来进行衡量:
  
user – 此次垃圾回收, 垃圾收集线程消耗的所有CPU时间(Total CPU time).
  
sys – 操作系统调用(OS call) 以及等待系统事件的时间(waiting for system event)
  
real – 应用程序暂停的时间(Clock time). 由于串行垃圾收集器(Serial Garbage Collector)只会使用单个线程, 所以 real time 等于 user 以及 system time 的总和.
  
通过上面的分析, 我们可以计算出在垃圾收集期间, JVM 中的内存使用情况。在垃圾收集之前, 堆内存总的使用了 1.54G (1,619,346K)。其中, 年轻代使用了 614M(629,119k)。可以算出老年代使用的内存为: 967M(990,227K)。

下一组数据( -> 右边)中蕴含了更重要的结论, 年轻代的内存使用在垃圾回收后下降了 546M(559,231k), 但总的堆内存使用(total heap usage)只减少了 337M(346,099k). 通过这一点,我们可以计算出, 有 208M(213,132K) 的年轻代对象被提升到老年代(Old)中。

这个GC事件可以用下面的示意图来表示, 上方表示GC之前的内存使用情况, 下方表示结束后的内存使用情况:

GC Ergonomics
  
In J2SE   1.5.0 release we added a new way of tuning the Java(tm) heap
  
which we call "garbage collector (GC) ergonomics". This was added
  
only to the parallel GC collector. You may also have seen it referred
  
to as "Smart Tuning" or "Simplified Tuning". GC ergonomics allows a
  
user to tune the Java heap by specifying a desired behavior for
  
the application. These behaviors are a maximum pause time goal and a
  
throughput goal.
  
https://blogs.oracle.com/jonthecollector/its-not-magic

http://blog.csdn.net/renfufei/article/details/49230943
  
<https://plumbr.eu/blog/garbage-collection/understanding-garbage-collection-logs>