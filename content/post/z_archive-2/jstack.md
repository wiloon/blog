---
title: jstack
author: "-"
date: 2015-11-11T11:20:45+00:00
url: jstack
categories:
  - inbox
tags:
  - reprint
---
## jstack
jstack主要用来查看某个Java进程内的线程堆栈信息。语法格式如下: 
    jstack [option] PID  
    jstack [option] executable core  
    jstack [option] [server-id@]remote-hostname-or-ip  

```bash

可以显示所有的线程  
H 打印线程信息,p指定pid,这两个参数的作用是显示进行pid下的所有线程的资源占用情况。  

    top -Hp PID  

找到cpu占用最高的线程  

10进制转16进制 

    printf "%x\n" PID

#-l long listings,会打印出额外的锁信息,在发生死锁时可以用jstack -l pid来观察锁持有情况
  
#http://www.wiloon.com/?p=10225

#-m mixed mode,不仅会输出Java堆栈信息,还会输出C/C++堆栈信息 (比如Native方法) 
  
#-m prints mixed mode (both Java and native C/C++ frames) stack trace.

#-F Force a stack dump when 'jstack [-l] pid' does not respond.

```
jstack可以定位到线程堆栈,根据堆栈信息我们可以定位到具体代码,所以它在JVM性能调优中使用得非常多。下面我们来一个实例找出某个Java进程中最耗费CPU的Java线程并定位堆栈信息,用到的命令有ps、top、printf、jstack、grep。

第一步先找出Java进程ID,我部署在服务器上的Java应用名称为mrf-center: 

ps -ef | grep mrf-center | grep -v grep

root 21711 1 1 14:47 pts/3 00:02:10 java -jar mrf-center.jar
  
得到进程ID为21711,第二步找出该进程内最耗费CPU的线程,可以使用

ps -Lfp pid或者ps -mp pid -o THREAD, tid, time或者top -Hp pid
  
,我这里用第三个,输出如下: 

TIME列就是各个Java线程耗费的CPU时间,CPU时间最长的是线程ID为21742的线程,用
  
printf "%x\n" 21742
  
得到21742的十六进制值为54ee,下面会用到。

OK,下一步终于轮到jstack上场了,它用来输出进程21711的堆栈信息,然后根据线程ID的十六进制值grep,如下: 
  
root@ubuntu:/# jstack 21711 | grep 54ee
  
"PollIntervalRetrySchedulerThread" prio=10 tid=0x00007f950043e000 nid=0x54ee in Object.wait() [0x00007f94c6eda000]
  
可以看到CPU消耗在PollIntervalRetrySchedulerThread这个类的Object.wait(),我找了下我的代码,定位到下面的代码: 
  
// Idle wait
  
getLog().info("Thread [" + getName() + "] is idle waiting…");
  
schedulerThreadState = PollTaskSchedulerThreadState.IdleWaiting;
  
long now = System.currentTimeMillis();
  
long waitTime = now + getIdleWaitTime();
  
long timeUntilContinue = waitTime – now;
  
synchronized(sigLock) {
  
try {
  
if(!halted.get()) {
  
sigLock.wait(timeUntilContinue);
  
}
  
}
  
catch (InterruptedException ignore) {
  
}
  
}
  
它是轮询任务的空闲等待代码,上面的sigLock.wait(timeUntilContinue)就对应了前面的Object.wait()。

一: jstack

jstack命令的语法格式:  jstack <pid>。可以用jps查看java进程id。这里要注意的是: 
  
1. 不同的 JAVA虚机的线程 DUMP的创建方法和文件格式是不一样的,不同的 JVM版本, dump信息也有差别。本文中,只以 SUN的 hotspot JVM 5.0_06 为例。
  
2. 在实际运行中,往往一次 dump的信息,还不足以确认问题。建议产生三次 dump信息,如果每次 dump都指向同一个问题,我们才确定问题的典型性。
  
二: 线程分析
  
2.1. JVM 线程
  
在线程中,有一些 JVM内部的后台线程,来执行如垃圾回收,或者低内存的检测等等任务,这些线程往往在 JVM初始化的时候就存在,如下所示: 
  
"Low Memory Detector" daemon prio=10 tid=0x081465f8 nid=0x7 runnable [0x00000000..0x00000000]
  
"CompilerThread0" daemon prio=10 tid=0x08143c58 nid=0x6 waiting on condition [0x00000000..0xfb5fd798]
  
"Signal Dispatcher" daemon prio=10 tid=0x08142f08 nid=0x5 waiting on condition [0x00000000..0x00000000]
  
"Finalizer" daemon prio=10 tid=0x08137ca0 nid=0x4 in Object.wait() [0xfbeed000..0xfbeeddb8]

at java.lang.Object.wait(Native Method)

– waiting on <0xef600848> (a java.lang.ref.ReferenceQueue$Lock)

at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:116)

– locked <0xef600848> (a java.lang.ref.ReferenceQueue$Lock)

at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:132)

at java.lang.ref.Finalizer$FinalizerThread.run(Finalizer.java:159)

"Reference Handler" daemon prio=10 tid=0x081370f0 nid=0x3 in Object.wait() [0xfbf4a000..0xfbf4aa38]

at java.lang.Object.wait(Native Method)

– waiting on <0xef600758> (a java.lang.ref.Reference$Lock)

at java.lang.Object.wait(Object.java:474)

at java.lang.ref.Reference$ReferenceHandler.run(Reference.java:116)

– locked <0xef600758> (a java.lang.ref.Reference$Lock)

"VM Thread" prio=10 tid=0x08134878 nid=0x2 runnable

"VM Periodic Task Thread" prio=10 tid=0x08147768 nid=0x8 waiting on condition
  
我们更多的是要观察用户级别的线程,如下所示: 

    "Thread-1" prio=10 tid=0x08223860 nid=0xa waiting on condition [0xef47a000..0xef47ac38]
    at java.lang.Thread.sleep(Native Method)
    at testthread.MySleepingThread.method2(MySleepingThread.java:53)
    – locked <0xef63d600> (a testthread.MySleepingThread)
    at testthread.MySleepingThread.run(MySleepingThread.java:35)
    at java.lang.Thread.run(Thread.java:595) 
  
我们能看到:   
* 线程的状态:  waiting on condition
* 线程的调用栈
* 线程的当前锁住的资源:  <0xef63d600>

2.2. 线程的状态分析  
正如我们刚看到的那样,线程的状态是一个重要的指标,它会显示在线程 Stacktrace的头一行结尾的地方。那么线程常见的有哪些状态呢？线程在什么样的情况下会进入这种状态呢？我们能从中发现什么线索？< /span>
  
1.1 Runnable
  
该状态表示线程具备所有运行条件,在运行队列中准备操作系统的调度,或者正在运行。

1.2 Wait on condition
  
该状态出现在线程等待某个条件的发生。具体是什么原因,可以结合 stacktrace来分析。最常见的情况是线程在等待网络的读写,比如当网络数据没有准备好读时,线程处于这种等待状态,而一旦有数据准备好读之后,线程会重新激活,读取并处理数据。在 Java引入 NewIO之前,对于每个网络连接,都有一个对应的线程来处理网络的读写操作,即使没有可读写的数据,线程仍然阻塞在读写操作上,这样有可能造成资源浪费,而且给操作系统的线程调度也带来压力。在 NewIO里采用了新的机制,编写的服务器程序的性能和可扩展性都得到提高。
  
如果发现有大量的线程都在处在 Wait on condition,从线程 stack看, 正等待网络读写,这可能是一个网络瓶颈的征兆。因为网络阻塞导致线程无法执行。一种情况是网络非常忙,几 乎消耗了所有的带宽,仍然有大量数据等待网络读 写；另一种情况也可能是网络空闲,但由于路由等问题,导致包无法正常的到达。所以要结合系统的一些性能观察工具来综合分析,比如 netstat统计单位时间的发送包的数目,如果很明显超过了所在网络带宽的限制 ; 观察 cpu的利用率,如果系统态的 CPU时间,相对于用户态的 CPU时间比例较高；如果程序运行在 Solaris 10平台上,可以用 dtrace工具看系统调用的情况,如果观察到 read/write的系统调用的次数或者运行时间遥遥领先；这些都指向由于网络带宽所限导致的网络瓶颈。另外一种出现 Wait on condition的常见情况是该线程在 sleep,等待 sleep的时间到了时候,将被唤醒。

1.3 Waiting for monitor entry 和 in Object.wait()
  
在多线程的 JAVA程序中,实现线程之间的同步,就要说说 Monitor。 Monitor是 Java中用以实现线程之间的互斥与协作的主要手段,它可以看成是对象或者 Class的锁。每一个对象都有,也仅有一个 monitor。每个 Monitor在某个时刻,只能被一个线程拥有,该线程就是 "Active Thread",而其它线程都是 "Waiting Thread",分别在两个队列 " Entry Set"和 "Wait Set"里面等候。在 "Entry Set"中等待的线程状态是 "Waiting for monitor entry",而在 "Wait Set"中等待的线程状态是 "in Object.wait()"。
  
先看 "Entry Set"里面的线程。我们称被 synchronized保护起来的代码段为临界区。当一个线程申请进入临界区时,它就进入了 "Entry Set"队列。对应的 code就像: 
  
synchronized(obj) {
  
………

}

这时有两种可能性: 
  
该 monitor不被其它线程拥有, Entry Set里面也没有其它等待线程。本线程即成为相应类或者对象的 Monitor的 Owner,执行临界区的代码
  
该 monitor被其它线程拥有,本线程在 Entry Set队列中等待。

在第一种情况下,线程将处于 "Runnable"的状态,而第二种情况下,线程 DUMP会显示处于 "waiting for monitor entry"。如下所示: 
  
Html代码
  
"Thread-0" prio=10 tid=0x08222eb0 nid=0x9 waiting for monitor entry [0xf927b000..0xf927bdb8]

at testthread.WaitThread.run(WaitThread.java:39)

– waiting to lock <0xef63bf08> (a java.lang.Object)

– locked <0xef63beb8> (a java.util.ArrayList)

at java.lang.Thread.run(Thread.java:595)
  
临界区的设置,是为了保证其内部的代码执行的原子性和完整性。但是因为临界区在任何时间只允许线程串行通过,这 和我们多线程的程序的初衷是相反的。 如果在多线程的程序中,大量使用 synchronized,或者不适当的使用了它,会造成大量线程在临界区的入口等待,造成系统的性能大幅下降。如果在线程 DUMP中发现了这个情况,应该审查源码,改进程序。
  
现在我们再来看现在线程为什么会进入 "Wait Set"。当线程获得了 Monitor,进入了临界区之后,如果发现线程继续运行的条件没有满足,它则调用对象 (一般就是被 synchronized 的对象) 的 wait() 方法,放弃了 Monitor,进入 "Wait Set"队列。只有当别的线程在该对象上调用了 notify() 或者 notifyAll() , " Wait Set"队列中线程才得到机会去竞争,但是只有一个线程获得对象的 Monitor,恢复到运行态。在 "Wait Set"中的线程, DUMP中表现为:  in Object.wait(),类似于: 
  
Html代码
  
"Thread-1" prio=10 tid=0x08223250 nid=0xa in Object.wait() [0xef47a000..0xef47aa38]

at java.lang.Object.wait(Native Method)

– waiting on <0xef63beb8> (a java.util.ArrayList)

at java.lang.Object.wait(Object.java:474)

at testthread.MyWaitThread.run(MyWaitThread.java:40)

– locked <0xef63beb8> (a java.util.ArrayList)

at java.lang.Thread.run(Thread.java:595)
  
仔细观察上面的 DUMP信息,你会发现它有以下两行: 
  
– locked <0xef63beb8> (a java.util.ArrayList)
  
– waiting on <0xef63beb8> (a java.util.ArrayList)
  
这里需要解释一下,为什么先 lock了这个对象,然后又 waiting on同一个对象呢？让我们看看这个线程对应的代码: 
  
Java代码
  
synchronized(obj) {
  
………
  
obj.wait();
  
………
  
}
  
线程的执行中,先用 synchronized 获得了这个对象的 Monitor (对应于 locked <0xef63beb8> ) 。当执行到 obj.wait(), 线程即放弃了 Monitor的所有权,进入 "wait set"队列 (对应于 waiting on <0xef63beb8> ) 。
  
往往在你的程序中,会出现多个类似的线程,他们都有相似的 DUMP信息。这也可能是正常的。比如,在程序中,有多个服务线程,设计成从一个队列里面读取请求数据。这个队列就是 lock以及 waiting on的对象。当队列为空的时候,这些线程都会在这个队列上等待,直到队列有了数据,这些线程被 Notify,当然只有一个线程获得了 lock,继续执行,而其它线程继续等待。

  1. JDK 5.0 的 lock
  
    上面我们提到如果 synchronized和 monitor机制运用不当,可能会造成多线程程序的性能问题。在 JDK 5.0中,引入了 Lock机制,从而使开发者能更灵活的开发高性能的并发多线程程序,可以替代以往 JDK中的 synchronized和 Monitor的 机制。但是,要注意的是,因为 Lock类只是一个普通类, JVM无从得知 Lock对象的占用情况,所以在线程 DUMP中,也不会包含关于 Lock的信息, 关于死锁等问题,就不如用 synchronized的编程方式容易识别。

4.案例分析
  
1. 死锁
  
在多线程程序的编写中,如果不适当的运用同步机制,则有可能造成程序的死锁,经常表现为程序的停顿,或者不再响应用户的请求。比如在下面这个示例中,是个较为典型的死锁情况: 
  
Java代码
  
"Thread-1" prio=5 tid=0x00acc490 nid=0xe50 waiting for monitor entry [0x02d3f000

..0x02d3fd68]

at deadlockthreads.TestThread.run(TestThread.java:31)

– waiting to lock <0x22c19f18> (a java.lang.Object)

– locked <0x22c19f20> (a java.lang.Object)

"Thread-0" prio=5 tid=0x00accdb0 nid=0xdec waiting for monitor entry [0x02cff000

..0x02cff9e8]

at deadlockthreads.TestThread.run(TestThread.java:31)

– waiting to lock <0x22c19f20> (a java.lang.Object)

– locked <0x22c19f18> (a java.lang.Object)

在 JAVA 5中加强了对死锁的检测。线程 Dump中可以直接报告出 Java级别的死锁,如下所示: 
  
Java代码

# Found one Java-level deadlock:

"Thread-1":
  
waiting to lock monitor 0x0003f334 (object 0x22c19f18, a java.lang.Object),
  
which is held by "Thread-0"
  
"Thread-0":
  
waiting to lock monitor 0x0003f314 (object 0x22c19f20, a java.lang.Object),
  
which is held by "Thread-1"
  
2. 热锁
  
热锁,也往往是导致系统性能瓶颈的主要因素。其表现特征为,由于多个线程对临界区,或者锁的竞争,可能出现: 
  
* 频繁的线程的上下文切换: 从操作系统对线程的调度来看,当线程在等待资源而阻塞的时候,操作系统会将之切换出来,放到等待的队列,当线程获得资源之后,调度算法会将这个线程切换进去,放到执行队列中。
  
* 大量的系统调用: 因为线程的上下文切换,以及热锁的竞争,或 者临界区的频繁的进出,都可能导致大量的系统调用。
  
* 大部分 CPU开销用在 "系统态 ": 线程上下文切换,和系统调用,都会导致 CPU在 "系统态 "运行,换而言之,虽然系统很忙碌,但是 CPU用在 "用户态 "的比例较小,应用程序得不到充分的 CPU资源。
  
* 随着 CPU数目的增多,系统的性能反而下降。因为 CPU数目多,同 时运行的线程就越多,可能就会造成更频繁的线程上下文切换和系统态的 CPU开销,从而导致更糟糕的性能。
  
上面的描述,都是一个 scalability (可扩展性) 很差的系统的表现。从整体的性能指标看,由于线程热锁的存在,程序的响应时间会变长,吞吐量会降低。
  
那么,怎么去了解 "热锁 "出现在什么地方呢？一个重要的方法还是结合操作系统的各种工具观察系统资源使用状况,以及收集 Java线程的 DUMP信息,看线程都阻塞在什么方法上,了解原因,才能找到对应的解决方法。
  
我们曾经遇到过这样的例子,程序运行时,出现了以上指出的各种现象,通过观察操作系统的资源使用统计信息,以及线程 DUMP信息,确定了程序中热锁的存在,并发现大多数的线程状态都是 Waiting for monitor entry或者 Wait on monitor,且是阻塞在压缩和解压缩的方法上。后来采用第三方的压缩包 javalib替代 JDK自带的压缩包后,系统的性能提高了几倍。

---

http://my.oschina.net/feichexia/blog/196575
  
https://docs.oracle.com/javase/8/docs/technotes/tools/unix/jstack.html
  
http://jameswxx.iteye.com/blog/1041173