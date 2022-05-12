---
title: java 线程 sleep, wait, join, yield
author: "-"
date: 2012-09-14T06:07:55+00:00
url: java/thread/sleep
categories:
  - Java
tags:$
  - reprint
---
## java 线程 sleep, wait, join, yield
### wait()    
调用该方法的线程进入 WAITING 状态，只有等待另外线程的通知或被中断才会返回，需要注意，

调用wait()方法后，会释放对象的锁。

wait(long)    超时等待一段时间，这里的参数是毫秒，也就是等待长达n毫秒，如果没有通知就超时返回。
wait(long, int)    对于超时时间更细粒度的控制，可以达到毫秒。

```java
Thread.sleep(3000);
TimeUnit.SECONDS.sleep(random.nextInt(10));
this.wait(2000);
```
### sleep
sleep 是 Thread 类的静态方法, sleep() 使当前线程进入停滞状态 (阻塞当前线程), 让出CUP的使用、目的是不让当前线程独自霸占该进程所获的CPU资源，以留一定时间给其他线程执行的机会;
  
Thread.sleep 不会导致锁行为的改变，如果当前线程是拥有锁的，那么Thread.sleep不会让线程释放锁。
  
所以当在一个 Synchronized 块中调用 Sleep() 方法时，线程虽然休眠了，但是对象的锁并没有被释放，其他线程无法访问这个对象 (即使睡着也持有对象锁) 。
  
在 sleep() 休眠时间期满后，该线程不一定会立即执行， 这是因为其它线程可能正在运行而且没有被调度为放弃执行，除非此线程具有更高的优先级。
  
如果能够帮助你记忆的话，可以简单认为和锁相关的方法都定义在 Object 类中，因此调用 Thread.sleep 是不会影响锁的相关行为。

wait() 方法是 Object 类里的方法； 当一个线程执行到 wait() 方法时，它就进入到一个和该对象相关的等待池中，同时失去 (释放) 了对象的锁 (暂时失去锁，wait(long timeout)超时时间到后还需要返还对象锁) 
  
wait() 使用 notify 或者 notifyAll 或者指定睡眠时间来唤醒当前等待池中的线程。
  
wiat() 必须放在 synchronized block 中，否则会在 program runtime 时扔出 "java.lang.IllegalMonitorStateException" 异常。

wait() 是从 Java 1.0 开始就存在的老牌"等待"函数，在 Java 1.5 以前是最主要的一类用于线程间进行同步的方法。

wait() 的使用方法相对比较 "怪异"。首先调用 wait() 的线程需要获得一个用于线程间共享的对象的 "锁"  (在 Java 术语中称为"监视器") ，然后调用 wait() 会首先**释放**这把锁，并将当前线程暂停，只有在其他进程通过调用共享对象的 notify() 或者 notifyAll() 时才会醒来。但是醒来之后也不是说立即就会得到执行，只是线程会重新加入对锁对象的竞争，只有竞争胜出之后才会获得运行权。

典型的使用 wait() 函数的代码是这样的
```java
// 等待者(Thread1)
synchronized (lock) {
while (condition != true) {
    lock.wait() 
}
  // do stuff
}

// 唤醒者(Thread2) 
synchronized (lock) {
condition = true;
lock.notify();
}
```
为什么 wait() 需要配合 synchronized 使用？

在 stackoverflow 上有个帖子对这个问题进行了讨论。我认为最主要的原因是为了防止以下这种情况
```java
// 等待者(Thread1)
while (condition != true) { // step.1
    lock.wait() // step.4
}

// 唤醒者(Thread2)
condition = true; // step.2
lock.notify(); // step.3
```

在对之前的代码去掉 synchronized 块之后，如果在等待者判断 condition != true 之后而调用 wait() 之前，唤醒者将 condition 修改成了 true 同时调用了 notify() 的话，那么等待者在调用了 wait() 之后就没有机会被唤醒了。

Thread.sleep 和 Object.wait 都会暂停当前的线程，对于CPU资源来说，不管是哪种方式暂停的线程，都表示它暂时不再需要CPU的执行时间。OS会将执行时间分配给其它线程。 区别是， 调用 wait 后， 需要别的线程执行 notify/notifyAll 才能够重新获得CPU执行时间。

线程的状态参考 Thread.State 的定义。 新创建的但是没有执行 (还没有调用start()) 的线程处于"新建"，或者说 Thread.State.NEW 状态。
  
Thread.State.BLOCKED  (阻塞)  表示线程正在获取锁时, 因为锁不能获取到而被迫暂停执行下面的指令, 一直等到这个锁被别的线程释放。 BLOCKED 状态下线程， OS 调度机制需要决定下一个能够获取锁的线程是哪个，这种情况下，就是产生锁的争用，无论如何这都是很耗时的操作。

从操作系统的角度讲，os 会维护一个 ready queue (就绪的线程队列) 。  并且在某一时刻 cpu 只 为ready queue 中位于队列头部的线程服务。
  
但是当前正在被服务的线程可能觉得 cpu 的服务质量不够好，于是提前退出，这就是 yield

sleep() 使当前线程进入停滞状态，所以执行 sleep() 的线程在指定的时间内肯定不会执行； yield() 只是使当前线程重新回到可执行状态，所以执行 yield() 的线程有可能在进入到可执行状态后马上又被执行。
  
sleep() 可使优先级低的线程得到执行的机会， 当然也可以让同优先级和高优先级的线程有执行的机会； yield() 只能使同优先级的线程有执行的机会。

但是 wait() 和 sleep() 都可以通过 interrupt() 方法打断线程的暂停状态，从而使线程立刻抛出 InterruptedException  (但不建议使用该方法) 。

### yield()
理论上，yield意味着放手，放弃，投降。一个调用 yield() 方法的线程告诉虚拟机它乐意让其他线程占用自己的位置。这表明该线程没有在做一些紧急的事情。注意，这仅是一个暗示，并不能保证不会产生任何影响。

在Thread.java中yield()定义如下: 
>A hint to the scheduler that the current thread is willing to yield its current use of a processor. The scheduler is free to ignore
>this hint. Yield is a heuristic(adj. 启发式的；探索的) attempt to improve relative progression between threads that would otherwise over-utilize a CPU.
>Its use should be combined with detailed profiling and benchmarking to ensure that it actually has the desired effect.

public static native void yield();
  
让我们列举一下关于以上定义重要的几点: 

Yield是一个静态的原生(native)方法
  
Yield告诉当前正在执行的线程把运行机会交给线程池中拥有相同优先级的线程。
  
Yield不能保证使得当前正在运行的线程迅速转换到可运行的状态
  
它仅能使一个线程从运行状态转到可运行状态，而不是等待或阻塞状态
  
yield()方法使用示例
  
在下面的示例程序中，我随意的创建了名为生产者和消费者的两个线程。生产者设定为最小优先级，消费者设定为最高优先级。在Thread.yield()注释和非注释的情况下我将分别运行该程序。没有调用yield()方法时，虽然输出有时改变，但是通常消费者行先打印出来，然后事生产者。

调用yield()方法时，两个线程依次打印，然后将执行机会交给对方，一直这样进行下去。
  
package test.core.threads;

public class YieldExample
  
{
  
public static void main(String[] args)
  
{
  
Thread producer = new Producer();
  
Thread consumer = new Consumer();

producer.setPriority(Thread.MIN_PRIORITY); //Min Priority
  
consumer.setPriority(Thread.MAX_PRIORITY); //Max Priority

producer.start();
  
consumer.start();
  
}
  
}

class Producer extends Thread
  
{
  
public void run()
  
{
  
for (int i = 0; i < 5; i++)
  
{
  
System.out.println("I am Producer : Produced Item " + i);
  
Thread.yield();
  
}
  
}
  
}

class Consumer extends Thread
  
{
  
public void run()
  
{
  
for (int i = 0; i < 5; i++)
  
{
  
System.out.println("I am Consumer : Consumed Item " + i);
  
Thread.yield();
  
}
  
}
  
}
  
上述程序在没有调用yield()方法情况下的输出: 

I am Consumer : Consumed Item 0
  
I am Consumer : Consumed Item 1
  
I am Consumer : Consumed Item 2
  
I am Consumer : Consumed Item 3
  
I am Consumer : Consumed Item 4
  
I am Producer : Produced Item 0
  
I am Producer : Produced Item 1
  
I am Producer : Produced Item 2
  
I am Producer : Produced Item 3
  
I am Producer : Produced Item 4
  
上述程序在调用yield()方法情况下的输出: 

I am Producer : Produced Item 0
  
I am Consumer : Consumed Item 0
  
I am Producer : Produced Item 1
  
I am Consumer : Consumed Item 1
  
I am Producer : Produced Item 2
  
I am Consumer : Consumed Item 2
  
I am Producer : Produced Item 3
  
I am Consumer : Consumed Item 3
  
I am Producer : Produced Item 4
  
I am Consumer : Consumed Item 4

### join()
join() 定义在 Thread.java 中  
join() 的作用: 让"主线程"等待"子线程" 结束之后才能继续运行。这句话可能有点晦涩，我们还是通过例子去理解:   
线程实例的方法 join()方法可以使得一个线程在另一个线程结束后再执行。如果join()方法在一个线程实例上调用，当前运行着的线程将阻塞直到这个线程实例完成了执行。
  
>wiloon.com/thread-join

#### 让线程停下来的方法
    函数                版本  消耗CPU   能否被Interrupt   核心方法  线程状态
    spinlock            1.0   是        否              native  RUNNABLE
    wait()              1.0   否        是              native  WAITING
    LockSupport.park()  1.5   否        是              native  WAITING
    sleep()             1.0   否        是              native  TIMED_WAITING
    join()              1.0   否        是              wait()  WAITING
    FutureTask.get()    1.5   否        是              park()  WAITING

suspend() 1.0 否 否 native WAITING 已弃用
  
ReentrantLock.lock() 1.5 部分是 否 park() WAITING 有可 Interrupt 版本 lockInterruptibly()
  
Condition.await() 1.5 否 是 park() WAITING 有不可 Interrupt 版本 awaitUninterruptibly()
  


Condition.await()
  
Condition 类也是在 Java 1.5 之后新加入的并发控制类。如果说 Lock 是用来替代 synchronized 的话，那么 Condition 就是用来替代 wait()、notify() 和 notifyAll() 的，相应的函数名分别是 await()、signal() 和 signalAll()。注意到因为 wait() 是 Object 下的函数，所以 Condition 自然也有它的 wait()，为了不重名只好把新的函数命名成为 await()，signal() 还有 signalAll() 也是基于同样的理由。

内部同样使用 park() 实现等待。

Future.get()
  
使用过 ExecutorService 或者 NIO 的话一定对 Future 不会陌生，而 Future 的 get() 是阻塞方法，内部也是使用 park() 来阻塞调用者的线程。

join()是Thread类的一个方法。根据jdk文档的定义: 

public final void join()throws InterruptedException: Waits for this thread to die.

join()方法的作用，是等待这个线程结束；但显然，这样的定义并不清晰。个人认为"Java 7 Concurrency Cookbook"的定义较为清晰: 

Waiting for the finalization of a thread

In some situations, we will have to wait for the finalization of a thread. For example, we may have a program that will begin initializing the resources it needs before proceeding with the rest of the execution. We can run the initialization tasks as threads and wait for its finalization before continuing with the rest of the program. For this purpose, we can use the join() method of the Thread class. When we call this method using a thread object, it suspends the execution of the calling thread until the object called finishes its execution.

解释一下，是主线程等待子线程的终止。也就是说主线程的代码块中，如果碰到了t.join()方法，此时主线程需要等待 (阻塞) ，等待子线程结束了(Waits for this thread to die.),才能继续执行t.join()之后的代码块。

 

 oin方法实现是通过wait (小提示: Object 提供的方法) 。 当main线程调用t.join时候，main线程会获得线程对象t的锁 (wait 意味着拿到该对象的锁),调用该对象的wait(等待时间)，直到该对象唤醒main线程 ，比如退出后。这就意味着main 线程调用t.join时，必须能够拿到线程t对象的锁。

join() 一共有三个重载版本，分别是无参、一个参数、两个参数: 


(1) 三个方法都被final修饰，无法被子类重写。

(2) join(long), join(long, long) 是synchronized method，同步的对象是当前线程实例。

(2) 无参版本和两个参数版本最终都调用了一个参数的版本。

(3) join() 和 join(0) 是等价的，表示一直等下去；join(非0)表示等待一段时间。

从源码可以看到 join(0) 调用了Object.wait(0)，其中Object.wait(0) 会一直等待，直到被notify/中断才返回。

while(isAlive())是为了防止子线程伪唤醒(spurious wakeup)，只要子线程没有TERMINATED的，父线程就需要继续等下去。

(4) join() 和 sleep() 一样，可以被中断 (被中断时，会抛出 InterrupptedException 异常) ；不同的是，join() 内部调用了 wait()，会出让锁，而 sleep() 会一直保持锁。

join使用时注意几点: 
1. join与start调用顺序问题

上面的讨论大概知道了join的作用了，那么，入股 join在start前调用，会出现什么后果呢？先看下面的测试结果


main线程没有等待[BThread]执行完再执行。join方法必须在线程start方法调用之后调用才有意义。这个也很容易理解: 如果一个线程都没有start，那它也就无法同步了。

2. join()与异常

在join()过程中，如果当前线程被中断，则当前线程出现异常。(注意是调用thread.join()的线程被中断才会进入异常，比如a线程调用b.join()，a中断会报异常而b中断不会异常)

如下:threadB中启动threadA，并且调用其方法等待threadA完成，此时向threadB发出中断信号，会进入中断异常代码。


http://blog.csdn.net/wbchn/article/details/2462112
  
http://www.zhihu.com/question/23328075
  
http://www.cnblogs.com/DreamSea/archive/2012/01/16/sleepandwaitdifferent.html
  
http://www.importnew.com/14958.html
  
http://www.cnblogs.com/dreamsea/archive/2012/01/16/2263844.html
  
http://blog.dyngr.com/blog/2016/09/09/how-to-make-a-thread-wait/

————————————————
版权声明: 本文为CSDN博主「DivineH」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/qq_38293564/article/details/80432875


