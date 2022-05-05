---
title: 线程
author: "-"
date: 2015-06-30T02:52:35+00:00
url: thread
categories:
  - Java
tags:
  - reprint
---
## 线程

进程在各自独立的空间中运行，进程之间共享数据需要用 mmap 或者进程间通信机制 (IPC) 如何在一个进程空间中执行多个线程，有些情况需要在一个进程中同时执行多个控制流程，这时候线程就派上了用场，
线程是比进程更轻量级的调度执行单位，线程的引入可以把一个进程的资源分配和执行调度分开，各个线程既可以共享进程资源(内存地址，文件IO等)，又可以独立调度 (线程是CPU调度的基本单位) 。

### 线程共享以下进程的资源和环境

1. 文件描述符表 (重点)
2. 每种信号的处理方式 (SIG_IGN、SIG_DFL或者自定义的信号处理函数)
3. 当前工作目录
4. 用户id和组id

### 线程有自己的私有数据

1. 线程id
2. 上下文信息, 包括各种寄存器的值, 程序计数器, 栈指针
3. 栈空间 (临时变量存储在栈空间中) (重点)
4. errno变量
5. 信号屏蔽字
6. 调度优先级

Linux上线程位于libpthread共享库中，因此在编译时要加上-lpthread选项 (-l :指明所链接的库)

### 进程与线程的联系与区别

1. 线程是在进程内部运行的执行分支
2. 线程是为了资源共享 (共享地址空间) ，进程是为了资源独占 (私有地址空间) 
3. Linux下没有真正的线程，它是利用轻量级进程来代替实现的
4. 进程是分配资源 (资源管理) 的最小单元；而线程是调度资源 (程序执行) 的最小单元
5. 线程与线程之间是独立的

实现线程主要有三种方式: 使用内核线程实现，使用用户线程实现和使用用户线程加轻量级进程混合实现。

### java thread

### Thread Dump日志的线程信息

    "resin-22129" daemon prio=10 tid=0x00007fbe5c34e000 nid=0x4cb1 waiting on condition [0x00007fbe4ff7c000]
      java.lang.Thread.State: WAITING (parking)
        at sun.misc.Unsafe.park(Native Method)
        at java.util.concurrent.locks.LockSupport.park(LockSupport.java:315)
        at com.caucho.env.thread2.ResinThread2.park(ResinThread2.java:196)
        at com.caucho.env.thread2.ResinThread2.runTasks(ResinThread2.java:147)
        at com.caucho.env.thread2.ResinThread2.run(ResinThread2.java:118)

    "Timer-20" daemon prio=10 tid=0x00007fe3a4bfb800 nid=0x1a31 in Object.wait() [0x00007fe3a077a000]
      java.lang.Thread.State: TIMED_WAITING (on object monitor)
        at java.lang.Object.wait(Native Method)
        - waiting on <0x00000006f0620ff0> (a java.util.TaskQueue)
        at java.util.TimerThread.mainLoop(Timer.java:552)
        - locked <0x00000006f0620ff0> (a java.util.TaskQueue)
        at java.util.TimerThread.run(Timer.java:505)

以上依次是:

- "resin-22129" 线程名称: 如果使用 java.lang.Thread 类生成一个线程的时候，线程名称为 Thread-(数字) 的形式，这里是resin生成的线程；
- daemon 线程类型: 线程分为守护线程 (daemon) 和非守护线程 (non-daemon) 两种，通常都是守护线程；
- prio=10 线程优先级: 默认为5，数字越大优先级越高；
- tid=0x00007fbe5c34e000 JVM线程的id: JVM内部线程的唯一标识，通过 java.lang.Thread.getId()获取，通常用自增的方式实现；
- nid=0x4cb1 操作系统线程id: 对应的系统线程id (Native Thread ID)，可以通过 top 命令进行查看，现场id是十六进制的形式；
- waiting on condition 系统线程状态: 这里是系统的线程状态，具体的含义见下面 系统线程状态部分；
- [0x00007fbe4ff7c000] 起始栈地址: 线程堆栈调用的其实内存地址；
- java.lang.Thread.State: WAITING (parking) JVM线程状态: 这里标明了线程在代码级别的状态，详细的内容见下面的 JVM线程运行状态 部分。
- 线程调用栈信息: 下面就是当前线程调用的详细栈信息，用于代码的分析。堆栈信息应该从下向上解读，因为程序调用的顺序是从下向上的。

### java 线程创建

- 继承Thread类
- 实现 Runnable 接口
- 使用 Callable 和 Future 创建线程
- 使用线程池创建线程 Executors

---

在Java程序中，JVM负责线程的调度。线程调度是指按照特定的机制为多个线程分配CPU的使用权。
  
调度的模式有两种: 分时调度和抢占式调度。分时调度是所有线程轮流获得CPU使用权，并平均分配每个线程占用CPU的时间；抢占式调度是根据线程的优先级来获取CPU的使用权。JVM的线程调度模式采用了抢占式模式。

Thread类实际上也是实现了Runnable接口的类。
  
在启动的多线程的时候，需要先通过Thread类的构造方法Thread(Runnable target) 构造出对象，然后调用Thread对象的start()方法来运行多线程代码。
  
实际上所有的多线程代码都是通过运行Thread的start()方法来运行的。因此，不管是扩展Thread类还是实现Runnable接口来实现多线程，最终还是通过Thread的对象的API来控制线程的，熟悉Thread类的API是进行多线程编程的基础。

JAVA多线程涉及到2个问题，一个是线程的调度，另一个是线程的同步

线程的状态: new runnable、running、waiting、timed_waiting、blocked、dead

New

The thread is in new state if you create an instance of Thread class but before the invocation of start() method.
  
当执行new Thread(Runnable r)后，新创建出来的线程处于new状态

Runnable
  
The thread is in runnable state after invocation of start() method, but the thread scheduler has not selected it to be the running thread.
  
每个支持多线程的系统都有一个调度器，调度器会从线程池中选择一个线程并启动它。当一个线程处于可执行状态时，表示它可能正处于线程池中等待调度器启动它；也可能它已正在执行。如执行了一个线程对象的start()方法后，线程就处于可执行状态，但显而易见的是此时线程不一定正在执行中。

当执行thread.start()后，线程处于runnable状态，这种情况下只要得到CPU，就可以开始执行了。runnable状态的线程，会接受JVM的调度，进入running状态，但是具体何时会进入这个状态，是随机不可知的

Running
  
The thread is in running state if the thread scheduler has selected it.
  
running状态中的线程最为复杂，可能会进入runnable、waiting、timed_waiting、blocked、dead状态: 
  
如果CPU调度给了别的线程，或者执行了Thread.yield()方法，则进入runnable状态，但是也有可能立刻又进入running状态
  
如果执行了Thread.sleep(long)，或者thread.join(long)，或者在锁对象上调用object.wait(long)方法，则会进入timed_waiting状态
  
如果执行了thread.join()，或者在锁对象上调用了object.wait()方法，则会进入waiting状态
  
如果进入了同步方法或者同步代码块，没有获取锁对象的话，则会进入blocked状态

Timed waiting
  
Timed waiting is a thread state for a thread waiting with a specified waiting time. A thread is in the timed waiting state due to calling one of the following methods with a specified positive waiting time:
  
Thread.sleep(sleeptime)
  
Object.wait(timeout)
  
Thread.join(timeout)
  
LockSupport.parkNanos(timeout)
  
LockSupport.parkUntil(timeout)

处于waiting状态中的线程，如果是因为thread.join()方法进入等待的话，在目标thread执行完毕之后，会回到runnable状态；如果是因为object.wait()方法进入等待的话，在锁对象执行object.notify()或者object.notifyAll()之后会回到runnable状态

处于timed_waiting状态中的线程，和waiting状态中的差不多，只不过是设定时间到了，就会回到runnable状态

Dead/死亡
  
当一个线程正常结束，或者抛出了未捕获的异常之后，它便处于死亡状态。如一个线程的run()函数执行完毕后线程就进入死亡状态，该线程结束

Blocked/阻塞
  
BLOCKED是指线程正在等待获取锁；WAITING是指线程正在等待其他线程发来的通知 (notify) ，收到通知后，可能会顺序向后执行 (RUNNABLE) ，也可能会再次获取锁，进而被阻塞住 (BLOCKED) 。

当一个线程处于停滞状态时，系统调度器就会忽略它，不对它进行调度。当处于停滞状态的线程重新回到可执行状态时，它有可能重新执行。如通过对一个线程调用wait()函数后，线程就进入停滞状态，只有当再次对该线程调用notify或notifyAll后它才能两次回到可执行状态。
  
处于blocked状态中的线程，只有获取了锁之后，才会脱离阻塞状态
  
Thread state for a waiting thread.A thread is in the waiting state due to calling one of the following methods:
  
{@link Object#wait() Object.wait} with no timeout
  
{@link #join() Thread.join} with no timeout
  
{@link LockSupport#park() LockSupport.park}

Blocked vs. Waiting - Blocked是syncronized阻塞的，或者一个线程进入了sychronized,然后调用了wait,则进入等待状态，其他线程进入了同步块调用了Notify，等待进程被唤起，然后，重新等待synchronized的对象锁，这个时候也是Blocked的状态。也就是临界点阻塞或者回到临界点阻塞都是Blocked.
  
sleep, wait, wait(long), park, join等等都是等待waiting状态。

Thread下的常用函数函数
  
suspend()、resume()
  
通过suspend()函数，可使线程进入停滞状态。通过suspend()使线程进入停滞状态后，除非收到resume()消息，否则该线程不会变回可执行状态。
  
当调用suspend()函数后，线程不会释放它的"锁标志"。

5. 当线程池中线程都具有相同的优先级，调度程序的JVM实现自由选择它喜欢的线程。这时候调度程序的操作有两种可能: 一是选择一个线程运行，直到它阻塞或者运行完成为止。二是时间分片，为池内的每个线程提供均等的运行机会。

6. 设置线程的优先级: 线程默认的优先级是创建它的执行线程的优先级。可以更改线程的优先级。

JVM从不会改变一个线程的优先级。然而，1-10之间的值是没有保证的。一些JVM可能不能识别10个不同的值，而将这些优先级进行每两个或多个合并，变成少于10个的优先级，则两个或多个优先级的线程可能被映射为一个优先级。

7. Thread.yield()方法作用是: 暂停当前正在执行的线程对象，并执行其他线程。
  
yield()应该做的是让当前运行线程回到可运行状态，以允许具有相同优先级的其他线程获得运行机会。因此，使用yield()的目的是让相同优先级的线程之间能适当的轮转执行。但是，实际中无法保证yield()达到让步目的，因为让步的线程还有可能被线程调度程序再次选中。

结论: yield()从未导致线程转到等待/睡眠/阻塞状态。在大多数情况下，yield()将导致线程从运行状态转到可运行状态，但有可能没有效果。

8. 另一个问题是线程的同步，这个我感觉比调度更加复杂一些

Java中每个对象都有一个"内置锁"，也有一个内置的"线程表"

当程序运行到非静态的synchronized方法上时，会获得与正在执行代码类的当前实例 (this实例) 有关的锁；当运行到同步代码块时，获得与声明的对象有关的锁

释放锁是指持锁线程退出了synchronized方法或代码块。

当程序运行到synchronized同步方法或代码块时对象锁才起作用。

一个对象只有一个锁。所以，如果一个线程获得该锁，就没有其他线程可以获得锁，直到第一个线程释放 (或返回) 锁。这也意味着任何其他线程都不能进入该对象上的synchronized方法或代码块，直到该锁被释放。

9. 当提到同步 (锁定) 时，应该清楚是在哪个对象上同步 (锁定) ？

obj.wait()
  
obj.notify()
  
obj.notifyAll()

关于这3个方法，有一个关键问题是: 

必须从同步环境内调用wait()、notify()、notifyAll()方法。只有拥有该对象的锁的线程，才能调用该对象上的wait()、notify()、notifyAll()方法

与每个对象具有锁一样，每个对象也可以有一个线程列表，他们等待来自该对象的通知。线程通过执行对象上的wait()方法获得这个等待列表。从那时候起，它不再执行任何其他指令，直到调用对象的notify()方法为止。如果多个线程在同一个对象上等待，则将只选择一个线程 (不保证以何种顺序) 继续执行。如果没有线程等待，则不采取任何特殊操作。

Non-Runnable (Blocked)
  
This is the state when the thread is still alive, but is currently not eligible to run.

Terminated
  
A thread is in terminated or dead state when its run() method exits.

Parking
  
Disables the current thread for thread scheduling purposes unless the permit is available.

1，线程状态为"waiting for monitor entry": 
  
意味着它 在等待进入一个临界区 ，所以它在"Entry Set"队列中等待。
  
此时线程状态一般都是 Blocked: 
  
java.lang.Thread.State: BLOCKED (on object monitor)

### waiting on condition
说明它在等待另一个条件的发生，来把自己唤醒，或者干脆它是调用了 sleep(N)。  
此时线程状态大致为以下几种:   
java.lang.Thread.State: WAITING (parking): 一直等那个条件发生；
java.lang.Thread.State: TIMED_WAITING (parking或sleeping): 定时的，那个条件不到来，也将定时唤醒自己。
如果大量线程在"waiting on condition":   
可能是它们又跑去获取第三方资源，尤其是第三方网络资源，迟迟获取不到Response，导致大量线程进入等待状态。  
所以如果你发现有大量的线程都处在 Wait on condition，从线程堆栈看，正等待网络读写，这可能是一个网络瓶颈的征兆，因为网络阻塞导致线程无法执行。  

### waiting for monitor entry
可能是一个全局锁阻塞住了大量线程。  
如果短时间内打印的 thread dump 文件反映，随着时间流逝，waiting for monitor entry 的线程越来越多，没有减少的趋势，可能意味着某些线程在临界区里呆的时间太长了，以至于越来越多新线程迟迟无法进入临界区。  

线程状态为"in Object.wait()": 
  
说明它获得了监视器之后，又调用了 java.lang.Object.wait() 方法。
  
每个 Monitor在某个时刻，只能被一个线程拥有，该线程就是 "Active Thread"，而其它线程都是 "Waiting Thread"，分别在两个队列 " Entry Set"和 "Wait Set"里面等候。在 "Entry Set"中等待的线程状态是 "Waiting for monitor entry"，而在 "Wait Set"中等待的线程状态是 "in Object.wait()"。
  
当线程获得了 Monitor，如果发现线程继续运行的条件没有满足，它则调用对象 (一般就是被 synchronized 的对象) 的 wait() 方法，放弃了 Monitor，进入 "Wait Set"队列。
  
此时线程状态大致为以下几种: 
  
    java.lang.Thread.State: TIMED_WAITING (on object monitor)； 
    java.lang.Thread.State: WAITING (on object monitor)；

一般都是RMI相关线程 (RMI RenewClean、 GC Daemon、RMI Reaper) ，GC线程 (Finalizer) ，引用对象垃圾回收线程 (Reference Handler) 等系统线程处于这种状态。

### Java Monitor
示范一: 
  
下面这个线程在等待这个锁 0x00000000fe7e3b50，等待进入临界区: 
  
"RMI TCP Connection(64896)-172.16.52.118" daemon prio=10 tid=0x00000000405a6000 nid=0x68fe waiting for monitor entry [0x00007f2be65a3000]
     
java.lang.Thread.State: BLOCKED (on object monitor)
  
at com.xyz.goods.service.impl.GoodsServiceImpl.findChanellGoodsCountWithCache(GoodsServiceImpl.java:1734)
  
- waiting to lock <0x00000000fe7e3b50> (a java.lang.String)

那么谁持有这个锁呢？
  
是另一个先调用了 findChanellGoodsCountWithCache 函数的线程: 
  
"RMI TCP Connection(64878)-172.16.52.117" daemon prio=10 tid=0x0000000040822000 nid=0x6841 runnable [0x00007f2be76b3000]
     
java.lang.Thread.State: RUNNABLE
  
at java.net.SocketInputStream.socketRead0(Native Method)
  
at java.net.SocketInputStream.read(SocketInputStream.java:129)
  
at java.io.BufferedInputStream.fill(BufferedInputStream.java:218)
  
at java.io.BufferedInputStream.read1(BufferedInputStream.java:258)
  
at java.io.BufferedInputStream.read(BufferedInputStream.java:317)
  
- locked <0x00000000af4ed638> (a java.io.BufferedInputStream)
  
at org.bson.io.Bits.readFully(Bits.java:35)
  
at org.bson.io.Bits.readFully(Bits.java:28)
  
at com.mongodb.Response.<init>(Response.java:35)
  
at com.mongodb.DBPort.go(DBPort.java:110)
  
- locked <0x00000000af442d48> (a com.mongodb.DBPort)
  
at com.mongodb.DBPort.go(DBPort.java:75)
  
- locked <0x00000000af442d48> (a com.mongodb.DBPort)
  
at com.mongodb.DBPort.call(DBPort.java:65)
  
at com.mongodb.DBTCPConnector.call(DBTCPConnector.java:202)
  
at com.mongodb.DBApiLayer$MyCollection.__find(DBApiLayer.java:296)
  
at com.mongodb.DB.command(DB.java:152)
  
at com.mongodb.DBCollection.getCount(DBCollection.java:760)
  
at com.mongodb.DBCollection.getCount(DBCollection.java:731)
  
at com.mongodb.DBCollection.count(DBCollection.java:697)
  
at com.xyz.goods.manager.MongodbManager.count(MongodbManager.java:202)
  
at com.xyz.goods.service.impl.GoodsServiceImpl.findChanellGoodsCount(GoodsServiceImpl.java:1787)
  
at com.xyz.goods.service.impl.GoodsServiceImpl.findChanellGoodsCountWithCache(GoodsServiceImpl.java:1739)
  
- locked <0x00000000fe7e3b50> (a java.lang.String)
  
示范二: 
  
等待另一个条件发生来将自己唤醒: 
  
"RMI TCP Connection(idle)" daemon prio=10 tid=0x00007fd50834e800 nid=0x56b2 waiting on condition [0x00007fd4f1a59000]
     
java.lang.Thread.State: TIMED_WAITING (parking)
  
at sun.misc.Unsafe.park(Native Method)
  
- parking to wait for <0x00000000acd84de8> (a java.util.concurrent.SynchronousQueue$TransferStack)
  
at java.util.concurrent.locks.LockSupport.parkNanos(LockSupport.java:198)
  
at java.util.concurrent.SynchronousQueue$TransferStack.awaitFulfill(SynchronousQueue.java:424)
  
at java.util.concurrent.SynchronousQueue$TransferStack.transfer(SynchronousQueue.java:323)
  
at java.util.concurrent.SynchronousQueue.poll(SynchronousQueue.java:874)
  
at java.util.concurrent.ThreadPoolExecutor.getTask(ThreadPoolExecutor.java:945)
  
at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:907)
  
at java.lang.Thread.run(Thread.java:662)
  
1) "TIMED_WAITING (parking)"中的 timed_waiting 指等待状态，但这里指定了时间，到达指定的时间后自动退出等待状态；parking指线程处于挂起中。
  
2) "waiting on condition"需要与堆栈中的"parking to wait for <0x00000000acd84de8> (a java.util.concurrent.SynchronousQueue$TransferStack)" 结合来看。首先，本线程肯定是在等待某个条件的发生，来把自己唤醒。其次，SynchronousQueue 并不是一个队列，只是线程之间移交信息的机制，当我们把一个元素放入到 SynchronousQueue 中时必须有另一个线程正在等待接受移交的任务，因此这就是本线程在等待的条件。

示范三: 
  
"RMI RenewClean-[172.16.50.182:4888]" daemon prio=10 tid=0x0000000040d2c800 nid=0x97e in Object.wait() [0x00007f9ccafd0000]
     
java.lang.Thread.State: TIMED_WAITING (on object monitor)
  
at java.lang.Object.wait(Native Method)
  
- waiting on <0x0000000799b032d8> (a java.lang.ref.ReferenceQueue$Lock)
  
at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:118)
  
- locked <0x0000000799b032d8> (a java.lang.ref.ReferenceQueue$Lock)
  
at sun.rmi.transport.DGCClient$EndpointEntry$RenewCleanThread.run(DGCClient.java:516)
  
at java.lang.Thread.run(Thread.java:662)

参考资源: 
  
1) CUBRID，2012，How to Analyze Java Thread Dumps；
  
2) 郑昀，2013，三个实例演示Java THread Dump日志分析；

程序中必须同时满足以下四个条件才会引发死锁: 

1). 互斥 (Mutual exclusion) : 线程所使用的资源中至少有一个是不能共享的，它在同一时刻只能由一个线程使用。
  
2). 持有与等待 (Hold and wait) : 至少有一个线程已经持有了资源，并且正在等待获取其他的线程所持有的资源。
  
3). 非抢占式 (No pre-emption) : 如果一个线程已经持有了某个资源，那么在这个线程释放这个资源之前，别的线程不能把它抢夺过去使用。
  
4). 循环等待 (Circular wait) : 假设有N个线程在运行，第一个线程持有了一个资源，并且正在等待获取第二个线程持有的资源，而第二个线程正在等待获取第三个线程持有的资源，依此类推……第N个线程正在等待获取第一个线程持有的资源，由此形成一个循环等待。

避免死锁，1. 按顺序锁定资源 2. 可中断的，有时间限制的等待 3. 死锁检测

http://www.iteye.com/topic/1119957
  
https://stackoverflow.com/questions/27406200/visual-vm-thread-states/27406503

Linux系统日志–syslog

java 实现多线程编程的方式有两种，一种是继承 Thread 类，另一种是实现 Runnable 接口。使用继承 Thread 类创建线程，最大的局限就是不能多继承

Thread.java 类中的 start() 方法通知"线程规划器"此线程已经准备就绪，等待调用线程对象的 run() 方法。这个过程其实就是让系统安排一个时间来调用 Thread 中的 run() 方法，也就是使线程得到运行，多线程是异步的，线程在代码中启动的顺序不是线程被调用的顺序。

保证在某一时刻只有一个线程能访问数据的简便方法，在任意时刻只允许一个线程对资源进行访问。如果有多个线程试图同时访问临界区，那么在有一个线程进入后，其他所有试图访问临界区的线程将被挂起，并一直持续到进入临界区的线程离开。临界区在被释放后，其他线程可以继续抢占，并以此达到用原子方式操作共享资源的目的.

### 临界区
  
临界区指的是一个访问共用资源 (例如: 共用设备或是共用存储器) 的程序片段，而这些共用资源又无法同时被多个线程访问的特性。当有线程进入临界区段时，
  
其他线程或是进程必须等待 (例如: bounded waiting 等待法) ，有一些同步的机制必须在临界区段的进入点与离开点实现，以确保这些共用资源是被互斥获得使用，
  
例如: semaphore。只能被单一线程访问的设备，例如: 打印机。

### 互斥量

互斥量和临界区很相似，只能拥有互斥对象的线程才能具有访问资源的权限，由于互斥对象只有一个，因此就决定了任何情况下次共享资源都不会同时被多个线程所访问。当前占据资源的线程在任务处理完后应将拥有的互斥对象交出，以便其他线程在获得后可以访问资源。互斥量比临界区复杂，因为使用互斥不仅仅能够在同一应用程序不同线程中实现资源的安全共享，而且可以在不同应用程序的线程之间实现对资源的安全共享。
  
互斥量是一个可以处于两态之一的变量: 解锁和加锁。这样，只需要一个二进制位表示它，不过实际上，常常使用一个整型量，0表示解锁，而其他所有的值则表示加锁。互斥量使用两个过程。当一个线程 (或进程) 需要访问临界区时，它调用mutex_lock。如果该互斥量当前是解锁的 (即临界区可用) ，此调用成功，调用线程可以自由进入该临界区。
  
另一方面，如果该互斥量已经加锁，调用线程被阻塞，直到在临界区中的线程完成并调用mutex_unlock。如果多个线程被阻塞在该互斥量上，将随机选择一个线程并允许它获得锁。
  
互斥量与临界区的作用非常相似，但互斥量是可以命名的，也就是说它可以跨越进程使用。所以创建互斥量需要的资源更多，所以如果只为了在进程内部是用的话使用临界区会带来速度上的优势并能够减少资源占用量 。因为互斥量是跨进程的互斥量一旦被创建，就可以通过名字打开它。

>管程, wiloon.com/monitor

### 信号量 semaphore

信号量对象对线程的同步方式与前面几种方法不同，信号允许多个线程同时使用共享资源
  
信号量(Semaphore)，有时被称为信号灯，是在多线程环境下使用的一种设施，是可以用来保证两个或多个关键代码段不被并发调用。在进入一个关键代码段之前，线程必须获取一个信号量；一旦该关键代码段完成了，那么该线程必须释放信号量。其它想进入该关键代码段的线程必须等待直到第一个线程释放信号量。为了完成这个过程，需要创建一个信号量VI，然后将Acquire Semaphore VI以及Release Semaphore VI分别放置在每个关键代码段的首末端。确认这些信号量VI引用的是初始创建的信号量。

CAS操作 (Compare-and-Swap) 
  
CAS操作 (compare and swap) CAS有3个操作数，内存值V，旧的预期值A，要修改的新值B。当且仅当预期值A和内存值V相同时，将内存值V修改为B，否则返回V。这是一种乐观锁的思路，它相信在它修改之前，没有其它线程去修改它；而Synchronized是一种悲观锁，它认为在它修改之前，一定会有其它线程去修改它，悲观锁效率很低。

重排序: 
  
编译器和处理器"为了提高性能，而在程序执行时会对程序进行的重排序。它的出现是为了提高程序的并发度，从而提高性能！但是对于多线程程序，重排序可能会导致程序执行的结果不是我们需要的结果！重排序分为"编译器"和"处理器"两个方面，而"处理器"重排序又包括"指令级重排序"和"内存的重排序"。

线程与内存交互操作
  
所有的变量 (实例字段，静态字段，构成数组对象的 元素，不包括局部变量和方法参数) 都存储在主内存中，每个线程有自己的工作内存，线程的工作内存保存被线程使用到变量的主内存副本拷贝。线程对变量的所有操作都必须在工作内存中进行，而不能直接读写主内存的变量。不同线程之间也不能直接访问对方工作内存中的变量，线程间变量值的传递通过主内存来完成。

JAVA中线程安全相关关键字及类
  
主要包括: synchronized，Volitile，ThreadLocal，Lock，Condition

volatile: 
  
1) 保证了新值能立即存储到主内存，每次使用前立即从主内存中刷新。
  
2) 禁止指令重排序优化。
  
注: volatile关键字不能保证在多线程环境下对共享数据的操作的正确性。可以使用在自己状态改变之后需要立即通知所有线程的情况下。只保证可见性，不保证原子性。即通过刷新变量值确保可见性。

Java中synchronized和final也能保证可见性

2.2 synchronized
  
同步快通过变量锁定前必须清空工作内存中的变量值，重新从主内存中读取变量值，解锁前必须把变量值同步回主内存来确保可见性。
  
把代码块声明为synchronized，有俩个作用，通常是指改代码具有原子性和可见性。如果没有同步机制提供的这种可见性，线程看到的共享比那里可能是修改前的值或不一致的值，这将引发许多严重问题。

原理: 当对象获取锁是，必须清空工作内存中的变量值，这样就可以保证直接从主内存中装入变量，同样在对象释放锁之前，会刷新工作内存中的变量值，强制使已做的任何更改都出现在主内存中，这样会保证在同一个锁上同步的俩个线程看到在synchronized块内修改的变量的相同值。

synchronized释放由JVM自己管理。

存在的问题: 

1) 无法中断一个正在等待获得锁的线程

2) 无法通过投票得到锁，如果不想等待下去，也就没法得到锁

3) 同步还需要锁的释放只能在与获得锁所在的堆栈帧相同的堆栈中进行，多数情况下，这没问题 (而且与一场处理交互的很好) ，但是，确实存在一些非块结构的锁定更适合情况。

final
  
被final修饰的字段在构造器中一旦被初始化完成，并且构造器没有把this引用传递进去，那么在其他线程中就能看见final字段的值，无需同步就可以被其他线程正确访问。
  
对于final域，编译器和处理器要遵守两个重排序规则: 
  
在构造函数内对一个final域的写入，与随后把这个被构造对象的引用赋值给一个引用变量，这两个操作之间不能重排序。
  
初次读一个包含final域的对象的引用，与随后初次读这个final域，这两个操作之间不能重排序。
  
写final域的重排序规则

写final域的重排序规则禁止把final域的写重排序到构造函数之外。这个规则的实现包含下面2个方面: 

JMM禁止编译器把final域的写重排序到构造函数之外。
  
编译器会在final域的写之后，构造函数return之前，插入一个StoreStore屏障。这个屏障禁止处理器把final域的写重排序到构造函数之外。

2.3 Lock
  
Lock是有JAVA编写而成的，在java这个层面是无关JVM实现的。包括: ReentrantLock，ReadWriteLock。其本质都依赖于AbstractQueueSynchronized类。Lock提供了很多锁的方式，尝试锁，中断锁等。释放锁的过程由JAVA开发人员自己管理。

就性能而言，对于资源冲突不多的情况下synchronized更加合理，但如果资源访问冲突多的情况下，synchronized的性能会快速下降，而Lock可以保持平衡。

2.4 condition
  
Condition将Object监视器方法 (wait，notify,notifyall) 分解成截然不同的对象，以便通过这些对象与任意Lock实现组合使用，为每个对象提供多个等待set(wait-set),，其中Lock替代了synchronized方法和语句的使用，condition替代了Object监视器方法的使用。Condition实例实质上被你绑定到一个锁上。要为特定Lock实例获得Condition实例，请使用其newCondition () 方法。

ReentrantLock相比于synchronized的优势: 
  
等待可中断: 在持有锁的线程长时间不释放锁的时候,等待的线程可以选择放弃等待.
  
公平锁: 按照申请锁的顺序来一次获得锁称为公平锁.synchronized的是非公平锁,ReentrantLock可以通过构造函数实现公平锁. new RenentrantLock(boolean fair)
  
锁绑定多个条件: 通过多次newCondition可以获得多个Condition对象,可以简单的实现比较复杂的线程同步的功能.通过await(),signal();



并发的三个特性

原子性

    原子性是指不可再分的最小操作指令，即单条机器指令，原子性操作任意时刻只能有一个线程，因此是线程安全的。 
    

Java内存模型中通过read、load、assign、use、store和write这6个操作保证变量的原子性操作。

    long和double这两个64位长度的数据类型java虚拟机并没有强制规定他们的read、load、store和write操作的原子性，即所谓的非原子性协定，但是目前的各种商业java虚拟机都把long和double数据类型的4中非原子性协定操作实现为原子性。所以java中基本数据类型的访问读写是原子性操作。 
    
    对于大范围的原子性保证需要通过lock和unlock操作以及synchronized同步块来保证。 
    

可见性

    可见性是指当一个线程修改了共享变量的值，其他线程可以立即得知这个修改。 
    

Java内存模型是通过在变量修改后将新值同步回主内存，在变量读取前从主内存刷新变量值来实现可见性的。

Java中通过volatile、final和synchronized这三个关键字保证可见性: 
  
volatile: 通过刷新变量值确保可见性。
  
synchronized: 同步块通过变量lock锁定前必须清空工作内存中变量值，重新从主内存中读取变量值，unlock解锁前必须把变量值同步回主内存来确保可见性。
  
final: 被final修饰的字段在构造器中一旦被初始化完成，并且构造器没有把this引用传递进去，那么在其他线程中就能看见final字段的值，无需同步就可以被其他线程正确访问。

有序性

    线程的有序性是指: 在线程内部，所有的操作都是有序执行的，而在线程之间，因为工作内存和主内存同步的延迟，操作是乱序执行的。 
    
    Java通过volatile和synchronized关键字确保线程之间操作的有序性。 
    

volatile禁止指令重排序优化实现有序性。
  
synchronized通过一个变量在同一时刻只允许一个线程对其进行lock锁定操作来确保有序性。

## java线程的实现方式
  
Java线程在JDK1.2之前，是基于名为"绿色线程"的用户线程实现的，而在JDK1.2中，线程模型被替换为基于操作系统原生线程模型来实现。在 Sun JDK 中，它的 Windows 和 Linux 版本都是使用一对一的线程模型来实现的.
  
因此，在目前的JDK版本中，操作系统支持怎样的线程模型，在很大程度上就决定了Java虚拟机的线程是怎样映射的，这点在不同的平台上没有办法达成一致，虚拟机规范中也未限定Java线程需要使用哪种线程模型来实现。

### java线程调度
线程调度有两种方式
  
协同式: 线程的执行时间由线程本身来控制，线程任务执行完成之后主动通知系统切换到另一个线程去执行。 (不推荐) 
      
优点: 实现简单，线程切换操作对线程本身是可知的，不存在线程同步问题。
      
缺点: 线程执行时间不可控制，如果线程长时间执行不让出CPU执行时间可能导致系统崩溃。

抢占式: 每个线程的执行时间有操作系统来分配，操作系统给每个线程分配执行的时间片，抢到时间片的线程执行，时间片用完之后重新抢占执行时间，线程的切换不由线程本身来决定 (Java使用的线程调度方式就是抢占式调度) 。
      
优点: 线程执行时间可控制，不会因为一个线程阻塞问题导致系统崩溃。

java中的线程安全等级

不可变: 

    可以是基本类型的final；可以是final对象，但对象的行为不会对其状态产生任何影响，比如String的subString就是new一个String对象各种Number类型如BigInteger和BigDecimal等大数据类型都是不可变的，但是同为Number子类型的AtomicInteger和AtomicLong则并非不可变。原因与它里面状态对象是unsafe对象有关，所做的操作都是CAS操作，可以保证原子性。 
    

绝对线程安全: 

    不管运行时环境如何，调用者都不需要任何额外的同步措施。 
    

相对线程安全: 

    这是我们通常意义上的线程安全。需要保证对象单独的操作是线程安全的。比如Vector，HashTable，synchronizedCollection包装集合等。 
    

线程兼容: 

    对象本身不是线程安全的，但可以通过同步手段实现。一般我们说的不是线程安全的，绝大多数是指这个。比如ArrayList，HashMap等。 
    

线程对立: 

    不管调用端是否采用了同步的措施，都无法在并发中使用的代码。 
    

线程安全的实现方式

互斥同步
  
在多线程访问的时候，保证同一时间只有一个线程使用。
  
临界区(Critical Section)，互斥量(Mutex)，信号量(Semaphore)，管程都是同步的一种手段
  
java里最基本的互斥同步手段是synchronized，编译之后会形成monitorenter和monitorexit这两个字节码指令，这两个字节码都需要一个reference类型的参数来指明要锁定和解锁的对象，还有一个锁的计数器，来记录加锁的次数，加锁几次就要同样解锁几次才能恢复到无锁状态。

java的线程是映射到操作系统的原生线程之上的，不管阻塞还是唤醒都需要操作系统的帮忙完成，都需要从用户态转换到核心态，这是很耗费时间的，是java语言中的一个重量级(Heavyweight)操作，虽然虚拟机本身会做一点优化的操作，比如通知操作系统阻塞之前会加一段自旋等待的过程，避免频繁切换到核心态。

非阻塞同步
  
互斥和同步最主要的问题就是阻塞和唤醒所带来的性能问题，所以这通常叫阻塞同步(悲观的并发策略)。随着硬件指令集的发展，我们有另外的选择: 基于冲突检测的乐观并发策略，通俗讲就是先操作，如果没有其他线程争用共享的数据，操作就成功，如果有，则进行其他的补偿(最常见就是不断的重试)，这种乐观的并发策略许多实现都不需要把线程挂起，这种同步操作被称为非阻塞同步。

这类的指令有: 
      
1)测试并设置(test-and-set)
      
2)获取并增加
      
3)交换
      
4)比较并交换(CAS)
      
5)加载链接/条件储存(Load-Linked/Store-Conditional LL/SC)

    后面两条是现代处理器新增的处理器指令，在JDK1.5之后，java中才可以使用CAS操作，就是传说中的sun.misc.Unsafe类里面的compareAndSwapInt()和compareAndSwapLong()等几个方法的包装提供，虚拟机对这些方法做了特殊的处理，及时编译出来的结果就是一条平台相关的处理器CAS指令，没有方法调用的过程，可以认为是无条件的内联进去。 
    
    原来需要对i++进行同步，但现在有了这种CAS操作来保证原子性，比如用AtomicInteger。 但是CAS存在一个ABA的问题。可以通过AtomicStampedReference来解决 (鸡肋) 。 
    

无同步
      
有一些代码天生就是线程安全的，不需要同步。其中有如下两类: 
      
可重入代码 (Reentrant Code) : 纯代码，具有不依赖存储在堆上的数据和公用的系统资源，用到的状态量都由参数中传入，不调用非可重入的方法等特征，它的返回结果是可以预测的。
      
线程本地存储 (Thread Local Storage) : 把共享数据的可见范围限制在同一个线程之内，这样就无须同步也能保证线程之间不出现数据争用问题。可以通过java.lang.ThreadLocal类来实现线程本地存储的功能。

java中的锁机制

悲观锁

    假定会发生并发冲突，屏蔽一切可能违反数据完整性的操作。悲观锁假定其他线程企图访问或者改变你正在访问、更改的对象的概率是很高的，因此在悲观锁的环境中，在你开始改变此对象之前就将该对象锁住，并且直到你提交了所作的更改之后才释放锁。 
    

乐观锁

    假设不会发生并发冲突。轻易不加锁。 
    

自旋锁与自适应自旋

    线程挂起和恢复的操作都需要转入内核态中完成，这些操作给系统的并发性能带来了很大的压力，在许多应用中，共享数据的锁定状态只会持续很短的一段时间，为了这段时间去挂起和恢复线程并不值得，可以让后请求锁的线程等待一会儿，但不放弃处理器的执行时间，让线程执行一个忙循环 (自旋) 。 
    
    自旋锁默认的自旋次数值是10次，可以使用参数-XX:PreBlockSpin更改。 
    
    自适应自旋意味着自旋的时间不再固定，而是由前一次在同一个锁上的自旋时间及锁的拥有者的状态来决定。 
    

锁清除: 

    虚拟机即时编译器在运行时，对一些代码上要求同步，但是被检测到不可能存在共享数据竞争的锁进行消除。锁消除的主要判定依据来源于逃逸分析的数据支持。 
    

锁粗化: 

    如果虚拟机探测到有一系列连续操作都对同一个对象反复加锁和解锁，将会把加锁同步的范围扩展 (粗化) 到整个操作序列的外部。 
    

锁升级

    Java SE1.6为了减少获得锁和释放锁所带来的性能消耗，引入了"偏向锁"和"轻量级锁"，所以在Java SE1.6里锁一共有四种状态，无锁状态，偏向锁状态，轻量级锁状态和重量级锁状态，它会随着竞争情况逐渐升级。锁可以升级但不能降级，意味着偏向锁升级成轻量级锁后不能降级成偏向锁。这种锁升级却不能降级的策略，目的是为了提高获得锁和释放锁的效率。 
    

### 偏向锁
Hotspot的作者经过以往的研究发现大多数情况下锁不仅不存在多线程竞争，而且总是由同一线程多次获得，为了让线程获得锁的代价更低而引入了偏向锁。当一个线程访问同步块并获取锁时，会在对象头和栈帧中的锁记录里存储锁偏向的线程ID，以后该线程在进入和退出同步块时不需要花费CAS操作来加锁和解锁，而只需简单的测试一下对象头的Mark Word里是否存储着指向当前线程的偏向锁，如果测试成功，表示线程已经获得了锁，如果测试失败，则需要再测试下Mark Word中偏向锁的标识是否设置成1 (表示当前是偏向锁) ，如果没有设置，则使用CAS竞争锁，如果设置了，则尝试使用CAS将对象头的偏向锁指向当前线程。 
    
偏向锁的撤销: 偏向锁使用了一种等到竞争出现才释放锁的机制，所以当其他线程尝试竞争偏向锁时，持有偏向锁的线程才会释放锁。偏向锁的撤销，需要等待全局安全点 (在这个时间点上没有字节码正在执行) ，它会首先暂停拥有偏向锁的线程，然后检查持有偏向锁的线程是否活着，如果线程不处于活动状态，则将对象头设置成无锁状态，如果线程仍然活着，拥有偏向锁的栈会被执行，遍历偏向对象的锁记录，栈中的锁记录和对象头的Mark Word要么重新偏向于其他线程，要么恢复到无锁或者标记对象不适合作为偏向锁，最后唤醒暂停的线程。下图中的线程1演示了偏向锁初始化的流程，线程2演示了偏向锁撤销的流程。 
    

关闭偏向锁: 偏向锁在Java 6和Java 7里是默认启用的，但是它在应用程序启动几秒钟之后才激活，如有必要可以使用JVM参数来关闭延迟-XX: BiasedLockingStartupDelay = 0。如果你确定自己应用程序里所有的锁通常情况下处于竞争状态，可以通过JVM参数关闭偏向锁-XX:-UseBiasedLocking=false，那么默认会进入轻量级锁状态。

轻量级锁: 

    轻量级锁加锁: 线程在执行同步块之前，JVM会先在当前线程的栈桢中创建用于存储锁记录的空间，并将对象头中的Mark Word复制到锁记录中，官方称为Displaced Mark Word。然后线程尝试使用CAS将对象头中的Mark Word替换为指向锁记录的指针。如果成功，当前线程获得锁，如果失败，表示其他线程竞争锁，当前线程便尝试使用自旋来获取锁。 
    
    轻量级锁解锁: 轻量级解锁时，会使用原子的CAS操作来将Displaced Mark Word替换回到对象头，如果成功，则表示没有竞争发生。如果失败，表示当前锁存在竞争，锁就会膨胀成重量级锁。下图是两个线程同时争夺锁，导致锁膨胀的流程图。 
    

因为自旋会消耗CPU，为了避免无用的自旋 (比如获得锁的线程被阻塞住了) ，一旦锁升级成重量级锁，就不会再恢复到轻量级锁状态。当锁处于这个状态下，其他线程试图获取锁时，都会被阻塞住，当持有锁的线程释放锁之后会唤醒这些线程，被唤醒的线程就会进行新一轮的夺锁之争。
  
重量级锁: 

    重量锁在JVM中又叫对象监视器 (Monitor) ，它至少包含一个竞争锁的队列，和一个信号阻塞队列 (wait队列) ，前者负责做互斥，后一个用于做线程同步。 
    

Java内存模型定义了八种操作: 
  
lock (锁定) : 作用于主内存的变量，它把一个变量标识为一个线程独占的状态；
  
unlock (解锁) : 作用于主内存的变量，它把一个处于锁定状态的变量释放出来，释放后的变量才可以被其他线程锁定；
  
read (读取) : 作用于主内存的变量，它把一个变量的值从主内存传送到线程中的工作内存，以便随后的load动作使用；
  
load (载入) : 作用于工作内存的变量，它把read操作从主内存中得到的变量值放入工作内存的变量副本中；
  
use (使用) : 作用于工作内存的变量，它把工作内存中一个变量的值传递给执行引擎；
  
assign (赋值) : 作用于工作内存的变量，它把一个从执行引擎接收到的值赋值给工作内存中的变量；
  
store (存储) : 作用于工作内存的变量，它把工作内存中的一个变量的值传送到主内存中，以便随后的write操作；
  
write (写入) : 作用于主内存的变量，它把store操作从工作内存中得到的变量的值写入主内存的变量中。

https://www.infoq.cn/article/Jtv2XL3a0HvRE2xwrNFs
  
http://smallbug-vip.iteye.com/blog/2275743
  
https://www.idaima.com/article/8968
  
http://www.infoq.com/cn/articles/java-memory-model-6

https://www.javatang.com/archives/2017/10/25/36441958.html

————————————————
版权声明: 本文为CSDN博主「mm_hh」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/mm_hh/article/details/72587207


https://blog.csdn.net/nalanmingdian/article/details/77748326


https://www.huaweicloud.com/articles/c0553b1cde014350e91620af1ce89f68.html

