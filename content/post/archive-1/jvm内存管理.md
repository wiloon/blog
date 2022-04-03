---
title: java JVM 内存问题 调查,调优
author: lcf
date: 2012-11-06T08:07:01+00:00
url: /?p=4618
categories:
  - Java

tags:
  - reprint
---
## java JVM 内存问题 调查,调优
https://my.oschina.net/u/3345762/blog/1784199
  
https://my.oschina.net/u/3345762/blog/1644973

http://www.infoq.com/cn/articles/Troubleshooting-Java-Memory-Issues?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global

http://www.importnew.com/14933.html
  
http://lovestblog.cn/blog/2015/08/21/rssxmx/

```bash
  
# set jdk path
  
export PATH=/usr/java/default/bin/:$PATH

# list java process
  
jcmd -l

# show jcmd command
  
jcmd PID help

#heap dump
  
jcmd PID GC.heap_dump /root/dump.hprof

```

Eclipse Memory Analyzer


  
    Eclipse Memory Analyzer
  




NMT, pmap
  
Max memory = [-Xmx] + [-XX:MaxPermSize] + number_of_threads * [-Xss]

init: represents the initial amount of memory (in bytes) that the Java virtual machine requests from the operating system for memory management during startup. The Java virtual machine may request additional memory from the operating system and may also release memory to the system over time. The value of init may be undefined.

used: represents the amount of memory currently used (in bytes).

committed: represents the amount of memory (in bytes) that is guaranteed to be available for use by the Java virtual machine. The amount of committed memory may change over time (increase or decrease). The Java virtual machine may release memory to the system and committed could be less than init. committed will always be greater than or equal to used.

max: represents the maximum amount of memory (in bytes) that can be used for memory management. Its value may be undefined. The maximum amount of memory may change over time if defined. The amount of used and committed memory will always be less than or equal to max if max is defined. A memory allocation may fail if it attempts to increase the used memory such that used > committed even if used <= max would still be true (for example, when the system is low on virtual memory).

reserved memory 是指JVM 通过mmap PROT_NONE 申请的虚拟地址空间,在页表中已经存在了记录 (entries) ,保证了其他进程不会被占用,会page faults, committed memory 是JVM向操做系统实际分配的内存 (malloc/mmap) ,mmaped PROT_READ | PROT_WRITE,仍然会page faults 但是跟 reserved 不同,完全内核处理像什么也没发生一样。 used memory 是JVM实际存储了数据 (Java对象) 的大小,当used~=committed的时候,heap就会grow up,-Xmx设置了上限。

PROT_NONE can be used to implement guard pages, Microsoft has the same concept (MSDN).

To quote the first link:

allocation of additional inaccessible memory during memory allocation operations is a technique for mitigating against exploitation of heap buffer overflows. These guard pages are unmapped pages placed between all memory allocations of one page or larger. The guard page causes a segmentation fault upon any access.
  
Thus useful in implementing protection for areas such as network interfacing, virtual machines, and interpreters. An example usage: pthread_attr_setguardsize, pthread_attr_getguardsize.

为了保证java内存不会溢出,java中有垃圾回收机制。垃圾回收机制是指jvm用于释放那些不再使用的对象所占用的内存。java语言并不要求jvm有gc,也没有规定gc如何工作。垃圾收集的目的在于清除不再使用的对象。gc通过确定对象是否被活动对象引用来确定是否收集该对象。

内存溢出就是你要求分配的java虚拟机内存超出了系统能给你的,系统不能满足需求,于是产生溢出。

内存泄漏是指你向系统申请分配内存进行使用(new),可是使用完了以后却不归还(delete),结果你申请到的那块内存你自己也不能再访问,该块已分配出来的内存也无法再使用,随着服务器内存的不断消耗,而无法使用的内存越来越多,系统也不能再次将它分配给需要的程序,产生泄露。一直下去,程序也逐渐无内存使用,就会溢出。 (内存泄露vs内存溢出) 

【内存空间的划分】

Sun JDK实现时遵照JVM规范,将内存空间划分为方法区、堆、JVM方法栈、本地方法栈及pc寄存器。

  * 方法区: 

存放要加载的类or接口的信息 (名称、修饰符等) 、类的static变量、final常量、Field信息、方法信息 (元数据) 。通过Class对象获取的相关数据就来自该区域。 -见 Class类

Sun JDK中这块区域对应Permanet Generation (持久代) ,默认最小值为16MB,最大值为64MB,可通过-XX:PermSize及-XX:MaxPermSize来设置最小值和最大值。

  * 堆 (Heap Memory) : 

存放对象实例及数组值,Heap中对象所占用的内存由GC进行回收,在32位系统上最大为2G,64位系统上无限制。可通过-Xms和-Xmx控制,-Xms为JVM启动时申请的最小Heap内存,-Xmx为JVM可申请的最大Heap内存。

  * 方法栈: 

每个线程均会创建PC寄存器和方法栈。方法栈中有栈帧。方法栈为线程私有。当方法运行完毕,该方法对应的栈帧所占用的空间自动释放。

-想到 ThreadLocal

方法栈空间不足时,抛出StackOverflowError错误 (如不合理的递归调用) ,在Sun JDK中可通过-Xss设置大小。


【Heap Memory详解】

{    [  (Eden)(S0)(S1)  ]     [ (          ) ]    }

|--New Gen--|    |-Old Gen-|

|-----heap--------|

-New Generation:新生代

大多数情况下java程序中新建的对象都从新生代分配内存,新生代由Eden Space和两块相同大小的Survivor Space构成。可通过-Xmn指定新生代的大小。

-Eden Space: 创建对象,依据的是方法区中存放的类的元数据。

-S0: 当Eden Space空间用完时,JVM的垃圾回收器对其进行回收,将Eden中不被其他对象使用的对象进行销毁,同时将Eden中还被其他对象引用的对象移到S0区,如果S0区也没有空间了则移动到S1区。

-S1

-Old Generation: 旧生代

存放新生代中经过多次垃圾回收仍然存活的对象,例如缓存对象。旧生代占用大小为-Xmx值减-Xmn对应的值。

--Shallow Heap

java.lang.OutOfMemoryError: GC overhead limit exceeded

这个是JDK6新添的错误类型。是发生在GC占用大量时间而很少的堆被恢复的时候发生的,是一种保护机制。解决方案是,关闭该功能,使用 -XX:-UseGCOverheadLimit

Sun官方解释: 

The parallel / concurrent collector will throw an OutOfMemoryError if too much time is being spent in garbage collection: if more than 98% of the total time is spent in garbage collection and less than 2% of the heap is recovered, an OutOfMemoryError will be thrown. This feature is designed to prevent applications from running for an extended period of time while making little or no progress because the heap is too small. If necessary, this feature can be disabled by adding the option -XX:-UseGCOverheadLimit to the command line

如何避免: 查看是否有使用大内存的代码或死循环。

【System.gc() 与 finalize()】

java.lang.System.gc()

java.lang.Runtime.getRuntime().gc()

java.lang.Object.finalize()

一个题目:
  
11. rbo = new ReallyBigObject();
  
12. // more code here
  
13. rbo = null;
  
14.
  
Which statement should be placed at line 14 to suggest that the virtual
  
machine expend effort toward recycling the memory used by the
  
object rbo?
  
A. System.gc();
  
B. Runtime.getRuntaime().gc();
  
C. System.freeMemory();
  
D. Runtime.getRuntime().growHeap();
  
E. Runtime.getRuntime().freeMemory();

gc()有何用？

调用 gc 方法暗示着 Java 虚拟机做了一些努力来回收未用对象,以便能够快速地重用这些对象当前占用的内存。当控制权从方法调用中返回时,虚拟机已经尽最大努力从所有丢弃的对象中回收了空间。
  
调用 System.gc() 等效于调用Runtime.getRuntime().gc()

finalize()有何用？

gc 只能清除在堆上分配的内存(纯java语言的所有对象都在堆上使用new分配内存),而不能清除栈上分配的内存 (当使用JNI技术时,可能会在栈上分配内存,例如java调用c程序,而该c程序使用malloc分配内存时) 。因此,如果某些对象被分配了栈上的内存区域,那gc就管不着了,对栈上的对象进行内存回收就要靠finalize()。
  
举个例子来说,当java 调用非java方法时 (这种方法可能是c或是c++的) ,在非java代码内部也许调用了c的malloc()函数来分配内存,而且除非调用那个了 free() 否则不会释放内存(因为free()是c的函数),这个时候要进行释放内存的工作,gc是不起作用的,因而需要在finalize()内部的一个固有方法调用free()。
  
finalize的工作原理应该是这样的: 一旦垃圾收集器准备好释放对象占用的存储空间,它首先调用finalize(),而且只有在下一次垃圾收集过程中,才会真正回收对象的内存.所以如果使用finalize(),就可以在垃圾收集期间进行一些重要的清除或清扫工作.

finalize()在什么时候被调用?
  
有三种情况
  
1.所有对象被Garbage Collection时自动调用,比如运行System.gc()后.
  
2.程序退出时为每个对象调用一次finalize方法。
  
3.显式的调用finalize方法
  
除此以外,正常情况下,当某个对象被系统收集为无用信息的时候,finalize()将被自动调用。但是jvm不保证finalize()一定被调用,也就是说,finalize()的调用是不确定的,这也就是为什么sun不提倡使用finalize()的原因. 简单来讲,finalize()是在对象被GC回收前会调用的方法,而System.gc()建议而非强制GC开始回收工作,具体执行要看GC的执行策略。

调用了 System.gc() 之后,java 在内存回收过程中就会调用那些要被回收的对象的 finalize() 方法。

【待看】

1.Calling System.gc() is a bad idea

2.System.gc() in Java

3.System.GC 算法

http://timyang.net/java/java_gc_tunning/

Java垃圾回收调优
  
Wednesday, Jan 7th, 2009 by Tim | Tags: GC, Java
  
在Java中,通常通讯类型的服务器对GC(Garbage Collection)比较敏感。通常通讯服务器每秒需要处理大量进出的数据包,需要解析,分解成不同的业务逻辑对象并做相关的业务处理,这样会导致大量的临时对象被创建和回收。同时服务器如果需要同时保存用户状态的话,又会产生很多永久的对象,比如用户session。业务越复杂的应用往往用户session包含的引用对象就越多。这样在极端情况下会发生两件事情,long gc pause time 或 out of memory。

一,要解决long pause time首先要了解JVM中heap的结构

java gc heap

Java Heap为什么要分成几个不同的代(generation)? 由于80%-98%的对象的生存周期很短,大部分新对象存放在young generation可以很高效的回收,避免遍历所有对象。
  
young与old中内存分配的算法完全不同。young generation中由于存活的很少,要mark, sweep 然后再 compact 剩余的对象比较耗时,干脆把 live object copy 到另外一个空间更高效。old generation完全相反,里面的 live object 变化较少。因此采用 mark-sweep-compact更合适。
  
二,Java中四种垃圾回收算法

Java中有四种不同的回收算法,对应的启动参数为
  
–XX:+UseSerialGC
  
–XX:+UseParallelGC
  
–XX:+UseParallelOldGC
  
–XX:+UseConcMarkSweepGC

  1. Serial Collector
  
    大部分平台或者强制 java -client 默认会使用这种。
  
    young generation算法 = serial
  
    old generation算法 = serial (mark-sweep-compact)
  
    这种方法的缺点很明显,stop-the-world, 速度慢。服务器应用不推荐使用。 
  2. Parallel Collector
  
    在linux x64上默认是这种,其他平台要加 java -server 参数才会默认选用这种。
  
    young = parallel,多个thread同时copy
  
    old = mark-sweep-compact = 1
  
    优点: 新生代回收更快。因为系统大部分时间做的gc都是新生代的,这样提高了throughput(cpu用于非gc时间)
  
    缺点: 当运行在8G/16G server上old generation live object太多时候pause time过长

  3. Parallel Compact Collector (ParallelOld)
  
    young = parallel = 2
  
    old = parallel,分成多个独立的单元,如果单元中live object少则回收,多则跳过
  
    优点: old old generation上性能较 parallel 方式有提高
  
    缺点: 大部分server系统old generation内存占用会达到60%-80%, 没有那么多理想的单元live object很少方便迅速回收,同时compact方面开销比起parallel并没明显减少。

  4. Concurent Mark-Sweep(CMS) Collector
  
    young generation = parallel collector = 2
  
    old = cms
  
    同时不做 compact 操作。
  
    优点: pause time会降低, pause敏感但CPU有空闲的场景需要建议使用策略4.
  
    缺点: cpu占用过多,cpu密集型服务器不适合。另外碎片太多,每个object的存储都要通过链表连续跳n个地方,空间浪费问题也会增大。

几条经验: 
  
1. java -server
  
2. 设置Xms=Xmx=3/4物理内存
  
3. 如果是CPU密集型服务器,使用–XX:+UseParallelOldGC, 否则–XX:+UseConcMarkSweepGC
  
4. 新生代,Parallel/ParallelOld可设大于Xmx1/4,CMS可设小,小于Xmx1/4
  
5. 优化程序,特别是每个用户的session中的集合类等。我们的一个模块中session中曾经为每个用户使用了一个ConcurrentHashMap, 里面通常只有几条记录,后来改成数组之后,每台机大概节约了1~2G内存。

不过总的说来,Java的GC算法感觉是业界最成熟的,目前很多其他语言或者框架也都支持GC了,但大多数都是只达到Java Serial gc这种层面,甚至分generation都未考虑。JDK7里面针对CMS又进行了一种改进,会采用一种G1(Garbage-First Garbage Collection)的算法。实际上Garbage-First paper(PDF) 2004年已经出来了,相信到JDK7已经可以用于严格生产环境,有时间也会进一步介绍一下G1。
  
另外在今年的Sun Tech Days上Joey Shen讲的Improving Java Performance(PDF)也是一个很好的Java GC调优的入门教程。

http://zhanjindong.com/2016/03/02/jvm-memory-tunning-notes
  
https://stackoverflow.com/questions/12916603/what-s-the-purpose-of-mmap-memory-protection-prot-none