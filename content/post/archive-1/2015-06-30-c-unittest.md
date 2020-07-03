---
title: java 线程状态
author: wiloon
type: post
date: 2015-06-30T02:52:35+00:00
url: /?p=7991
categories:
  - Uncategorized

---
在Java程序中，JVM负责线程的调度。线程调度是指按照特定的机制为多个线程分配CPU的使用权。
  
调度的模式有两种：分时调度和抢占式调度。分时调度是所有线程轮流获得CPU使用权，并平均分配每个线程占用CPU的时间；抢占式调度是根据线程的优先级别来获取CPU的使用权。JVM的线程调度模式采用了抢占式模式。

Thread类实际上也是实现了Runnable接口的类。
  
在启动的多线程的时候，需要先通过Thread类的构造方法Thread(Runnable target) 构造出对象，然后调用Thread对象的start()方法来运行多线程代码。
  
实际上所有的多线程代码都是通过运行Thread的start()方法来运行的。因此，不管是扩展Thread类还是实现Runnable接口来实现多线程，最终还是通过Thread的对象的API来控制线程的，熟悉Thread类的API是进行多线程编程的基础。

JAVA多线程涉及到2个问题，一个是线程的调度，另一个是线程的同步

线程的状态：new、runnable、running、waiting、timed_waiting、blocked、dead

New
  
The thread is in new state if you create an instance of Thread class but before the invocation of start() method.
  
当执行new Thread(Runnable r)后，新创建出来的线程处于new状态

Runnable
  
The thread is in runnable state after invocation of start() method, but the thread scheduler has not selected it to be the running thread.
  
每个支持多线程的系统都有一个调度器，调度器会从线程池中选择一个线程并启动它。当一个线程处于可执行状态时，表示它可能正处于线程池中等待调度器启动它；也可能它已正在执行。如执行了一个线程对象的start()方法后，线程就处于可执行状态，但显而易见的是此时线程不一定正在执行中。

当执行thread.start()后，线程处于runnable状态，这种情况下只要得到CPU，就可以开始执行了。runnable状态的线程，会接受JVM的调度，进入running状态，但是具体何时会进入这个状态，是随机不可知的

Running
  
The thread is in running state if the thread scheduler has selected it.
  
running状态中的线程最为复杂，可能会进入runnable、waiting、timed_waiting、blocked、dead状态：
  
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
  
BLOCKED是指线程正在等待获取锁；WAITING是指线程正在等待其他线程发来的通知（notify），收到通知后，可能会顺序向后执行（RUNNABLE），也可能会再次获取锁，进而被阻塞住（BLOCKED）。

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
  
当调用suspend()函数后，线程不会释放它的“锁标志”。

5、当线程池中线程都具有相同的优先级，调度程序的JVM实现自由选择它喜欢的线程。这时候调度程序的操作有两种可能：一是选择一个线程运行，直到它阻塞或者运行完成为止。二是时间分片，为池内的每个线程提供均等的运行机会。

6、设置线程的优先级：线程默认的优先级是创建它的执行线程的优先级。可以更改线程的优先级。

JVM从不会改变一个线程的优先级。然而，1-10之间的值是没有保证的。一些JVM可能不能识别10个不同的值，而将这些优先级进行每两个或多个合并，变成少于10个的优先级，则两个或多个优先级的线程可能被映射为一个优先级。

7、Thread.yield()方法作用是：暂停当前正在执行的线程对象，并执行其他线程。
  
yield()应该做的是让当前运行线程回到可运行状态，以允许具有相同优先级的其他线程获得运行机会。因此，使用yield()的目的是让相同优先级的线程之间能适当的轮转执行。但是，实际中无法保证yield()达到让步目的，因为让步的线程还有可能被线程调度程序再次选中。

结论：yield()从未导致线程转到等待/睡眠/阻塞状态。在大多数情况下，yield()将导致线程从运行状态转到可运行状态，但有可能没有效果。

8、另一个问题是线程的同步，这个我感觉比调度更加复杂一些

Java中每个对象都有一个“内置锁”，也有一个内置的“线程表”

当程序运行到非静态的synchronized方法上时，会获得与正在执行代码类的当前实例（this实例）有关的锁；当运行到同步代码块时，获得与声明的对象有关的锁

释放锁是指持锁线程退出了synchronized方法或代码块。

当程序运行到synchronized同步方法或代码块时对象锁才起作用。

一个对象只有一个锁。所以，如果一个线程获得该锁，就没有其他线程可以获得锁，直到第一个线程释放（或返回）锁。这也意味着任何其他线程都不能进入该对象上的synchronized方法或代码块，直到该锁被释放。

9、当提到同步（锁定）时，应该清楚是在哪个对象上同步（锁定）？

obj.wait()
  
obj.notify()
  
obj.notifyAll()

关于这3个方法，有一个关键问题是：

必须从同步环境内调用wait()、notify()、notifyAll()方法。只有拥有该对象的锁的线程，才能调用该对象上的wait()、notify()、notifyAll()方法

与每个对象具有锁一样，每个对象也可以有一个线程列表，他们等待来自该对象的通知。线程通过执行对象上的wait()方法获得这个等待列表。从那时候起，它不再执行任何其他指令，直到调用对象的notify()方法为止。如果多个线程在同一个对象上等待，则将只选择一个线程（不保证以何种顺序）继续执行。如果没有线程等待，则不采取任何特殊操作。

Non-Runnable (Blocked)
  
This is the state when the thread is still alive, but is currently not eligible to run.

Terminated
  
A thread is in terminated or dead state when its run() method exits.

Parking
  
Disables the current thread for thread scheduling purposes unless the permit is available.

1，线程状态为“waiting for monitor entry”：
  
意味着它 在等待进入一个临界区 ，所以它在”Entry Set“队列中等待。
  
此时线程状态一般都是 Blocked：
  
java.lang.Thread.State: BLOCKED (on object monitor)

2，线程状态为“waiting on condition”：
  
说明它在等待另一个条件的发生，来把自己唤醒，或者干脆它是调用了 sleep(N)。
  
此时线程状态大致为以下几种：
  
java.lang.Thread.State: WAITING (parking)：一直等那个条件发生；
  
java.lang.Thread.State: TIMED_WAITING (parking或sleeping)：定时的，那个条件不到来，也将定时唤醒自己。

3，如果大量线程在“waiting for monitor entry”：
  
可能是一个全局锁阻塞住了大量线程。
  
如果短时间内打印的 thread dump 文件反映，随着时间流逝，waiting for monitor entry 的线程越来越多，没有减少的趋势，可能意味着某些线程在临界区里呆的时间太长了，以至于越来越多新线程迟迟无法进入临界区。

4，如果大量线程在“waiting on condition”：
  
可能是它们又跑去获取第三方资源，尤其是第三方网络资源，迟迟获取不到Response，导致大量线程进入等待状态。
  
所以如果你发现有大量的线程都处在 Wait on condition，从线程堆栈看，正等待网络读写，这可能是一个网络瓶颈的征兆，因为网络阻塞导致线程无法执行。

线程状态为“in Object.wait()”：
  
说明它获得了监视器之后，又调用了 java.lang.Object.wait() 方法。
  
每个 Monitor在某个时刻，只能被一个线程拥有，该线程就是 “Active Thread”，而其它线程都是 “Waiting Thread”，分别在两个队列 “ Entry Set”和 “Wait Set”里面等候。在 “Entry Set”中等待的线程状态是 “Waiting for monitor entry”，而在 “Wait Set”中等待的线程状态是 “in Object.wait()”。
  
当线程获得了 Monitor，如果发现线程继续运行的条件没有满足，它则调用对象（一般就是被 synchronized 的对象）的 wait() 方法，放弃了 Monitor，进入 “Wait Set”队列。
  
此时线程状态大致为以下几种：
  
java.lang.Thread.State: TIMED_WAITING (on object monitor)；
  
java.lang.Thread.State: WAITING (on object monitor)；
  
一般都是RMI相关线程（RMI RenewClean、 GC Daemon、RMI Reaper），GC线程（Finalizer），引用对象垃圾回收线程（Reference Handler）等系统线程处于这种状态。

Java Monitor

图1 A Java Monitor

示范一：
  
下面这个线程在等待这个锁 0x00000000fe7e3b50，等待进入临界区：
  
"RMI TCP Connection(64896)-172.16.52.118" daemon prio=10 tid=0x00000000405a6000 nid=0x68fe waiting for monitor entry [0x00007f2be65a3000]
     
java.lang.Thread.State: BLOCKED (on object monitor)
  
at com.xyz.goods.service.impl.GoodsServiceImpl.findChanellGoodsCountWithCache(GoodsServiceImpl.java:1734)
  
- waiting to lock <0x00000000fe7e3b50> (a java.lang.String)

那么谁持有这个锁呢？
  
是另一个先调用了 findChanellGoodsCountWithCache 函数的线程：
  
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
  
示范二：
  
等待另一个条件发生来将自己唤醒：
  
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
  
1）“TIMED\_WAITING (parking)”中的 timed\_waiting 指等待状态，但这里指定了时间，到达指定的时间后自动退出等待状态；parking指线程处于挂起中。
  
2）“waiting on condition”需要与堆栈中的“parking to wait for <0x00000000acd84de8> (a java.util.concurrent.SynchronousQueue$TransferStack)” 结合来看。首先，本线程肯定是在等待某个条件的发生，来把自己唤醒。其次，SynchronousQueue 并不是一个队列，只是线程之间移交信息的机制，当我们把一个元素放入到 SynchronousQueue 中时必须有另一个线程正在等待接受移交的任务，因此这就是本线程在等待的条件。

示范三：
  
"RMI RenewClean-[172.16.50.182:4888]" daemon prio=10 tid=0x0000000040d2c800 nid=0x97e in Object.wait() [0x00007f9ccafd0000]
     
java.lang.Thread.State: TIMED_WAITING (on object monitor)
  
at java.lang.Object.wait(Native Method)
  
- waiting on <0x0000000799b032d8> (a java.lang.ref.ReferenceQueue$Lock)
  
at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:118)
  
- locked <0x0000000799b032d8> (a java.lang.ref.ReferenceQueue$Lock)
  
at sun.rmi.transport.DGCClient$EndpointEntry$RenewCleanThread.run(DGCClient.java:516)
  
at java.lang.Thread.run(Thread.java:662)

参考资源：
  
1）CUBRID，2012，How to Analyze Java Thread Dumps；
  
2）郑昀，2013，三个实例演示Java THread Dump日志分析；

程序中必须同时满足以下四个条件才会引发死锁：

1). 互斥（Mutual exclusion）：线程所使用的资源中至少有一个是不能共享的，它在同一时刻只能由一个线程使用。
  
2). 持有与等待（Hold and wait）：至少有一个线程已经持有了资源，并且正在等待获取其他的线程所持有的资源。
  
3). 非抢占式（No pre-emption）：如果一个线程已经持有了某个资源，那么在这个线程释放这个资源之前，别的线程不能把它抢夺过去使用。
  
4). 循环等待（Circular wait）：假设有N个线程在运行，第一个线程持有了一个资源，并且正在等待获取第二个线程持有的资源，而第二个线程正在等待获取第三个线程持有的资源，依此类推……第N个线程正在等待获取第一个线程持有的资源，由此形成一个循环等待。

避免死锁，1. 按顺序锁定资源 2. 可中断的，有时间限制的等待 3. 死锁检测

![][1]

http://www.iteye.com/topic/1119957
  
https://stackoverflow.com/questions/27406200/visual-vm-thread-states/27406503

<blockquote data-secret="1A90iIEGUv" class="wp-embedded-content">
  
    <a href="http://www.wiloon.com/wordpress/?p=2057">Linux系统日志–syslog</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://www.wiloon.com/wordpress/?p=2057&embed=true#?secret=1A90iIEGUv" data-secret="1A90iIEGUv" width="600" height="338" title=""Linux系统日志–syslog" - w1100n" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

 [1]: http://orwbur8sk.bkt.clouddn.com/javaSE_%E5%A4%9A%E7%BA%BF%E7%A8%8B-%E6%96%B9%E6%B3%95%E4%B8%8E%E7%8A%B6%E6%80%81%E5%85%B3%E7%B3%BB%E7%A4%BA%E6%84%8F%E5%9B%BE.png