---
title: semaphore/信号量, mutex/互斥锁
author: "-"
date: 2014-10-31T02:46:50+00:00
url: /?p=6997
categories:
  - OS

---
Mutex是一把钥匙，一个人拿了就可进入一个房间，出来的时候把钥匙交给队列的第一个。一般的用法是用于串行化对critical section代码的访问，保证这段代码不会被并行的运行。

Semaphore是一件可以容纳N人的房间，如果人不满就可以进去，如果人满了，就要等待有人出来。对于N=1的情况，称为binary semaphore。一般的用法是，用于限制对于某一资源的同时访问。

Binary semaphore与 Mutex的差异：

在 有的系统中Binary semaphore与Mutex是没有差异的。在有的系统上，主要的差异是mutex一定要由获得锁的进程来释放。而semaphore可以由其它进程释 放（这时的semaphore实际就是个原子的变量，大家可以加或减），因此semaphore可以用于进程间同步。Semaphore的同步功能是所有 系统都支持的，而Mutex能否由其他进程释放则未定，因此建议mutex只用于保护critical section。而semaphore则用于保护某变量，或者同步。

关于semaphore和mutex的区别，网上有著名的厕所理论（http://koti.mbnet.fi/niclasw/MutexSemaphore.html）：

Mutex:Is a key to a toilet. One person can have the key - occupy the toilet - at the time. When finished, the person gives (frees) the key to the next person in the queue.Officially: “Mutexes are typically used to serialise access to a section of re-entrant code that cannot be executed concurrently by more than one thread. A mutex object only allows one thread into a controlled section, forcing other threads which attempt to gain access to that section to wait until the first thread has exited from that section.”
Ref: Symbian Developer Library(A mutex is really a semaphore with value 1.)

Semaphore:

Is the number of free identical toilet keys. Example, say we have four toilets with identical locks and keys. The semaphore count - the count of keys - is set to 4 at beginning (all four toilets are free), then the count value is decremented as people are coming in. If all toilets are full, ie. there are no free keys left, the semaphore count is 0. Now, when eq. one person leaves the toilet, semaphore is increased to 1 (one free key), and given to the next person in the queue.

Officially: “A semaphore restricts the number of simultaneous users of a shared resource up to a maximum number. Threads can request access to the resource (decrementing the semaphore), and can signal that they have finished using the resource (incrementing the semaphore).”
Ref: Symbian Developer Library

所以，mutex就是一个binary semaphore （值就是0或者1）。但是他们的区别又在哪里呢？主要有两个方面：

    * 初始状态不一样：mutex的初始值是1（表示锁available），而semaphore的初始值是0（表示unsignaled的状态）。随后的操 作基本一样。mutex_lock和sem_post都把值从0变成1，mutex_unlock和sem_wait都把值从1变成0（如果值是零就等 待）。初始值决定了：虽然mutex_lock和sem_wait都是执行V操作，但是sem_wait将立刻将当前线程block住，直到有其他线程 post；mutex_lock在初始状态下是可以进入的。
    * 用法不一样（对称 vs. 非对称）：这里说的是“用法”。Semaphore实现了signal，但是mutex也有signal（当一个线程lock后另外一个线程 unlock，lock住的线程将收到这个signal继续运行）。在mutex的使用中，模型是对称的。unlock的线程也要先lock。而 semaphore则是非对称的模型，对于一个semaphore，只有一方post，另外一方只wait。就拿上面的厕所理论来说，mutex是一个钥 匙不断重复的使用，传递在各个线程之间，而semaphore择是一方不断的制造钥匙，而供另外一方使用（另外一方不用归还）。

前面的实验证明，mutex确实能够做到post和wait的功能，只是大家不用而已，因为它是“mutex”不是semaphore。


下面给出一个例子：

要 让一个thread在背景不断的执行，最简单的方式就是在该thread执行无穷回圈，如while(1) {}，这种写法虽可行，却会让CPU飙高到100%，因为CPU一直死死的等，其实比较好的方法是，背景平时在Sleep状态，当前景呼叫背景时，背景马 上被唤醒，执行该做的事，做完马上Sleep，等待前景呼叫。当背景sem_wait()时，就是马上处于Sleep状态，当前景sem_post() 时，会马上换起背景执行，如此就可避免CPU 100%的情形了。


/**//*
    (C) OOMusou 2006 http://oomusou.cnblogs.com

     Filename : pthread_create_semaphore.cpp
     Compiler : gcc 4.10 on Fedora 5 / gcc 3.4 on Cygwin 1.5.21
     Description : Demo how to create thread with semaphore in Linux.
     Release : 12/03/2006
     Compile : g++ -lpthread pthread_create_semaphore.cpp
    */
#include <stdio.h> // printf(),
#include <stdlib.h> // exit(), EXIT_SUCCESS
#include <pthread.h> // pthread_create(), pthread_join()
#include <semaphore.h> // sem_init()

sem_t binSem;

void* helloWorld(void* arg);

int main() {
     // Result for System call
    int res = 0;

     // Initialize semaphore
     res = sem_init(&binSem, 0, 0);
    if (res) {
         printf("Semaphore initialization failed!!/n");
         exit(EXIT_FAILURE);
     }

     // Create thread
     pthread_t thdHelloWorld;
     res = pthread_create(&thdHelloWorld, NULL, helloWorld, NULL);
    if (res) {
         printf("Thread creation failed!!/n");
         exit(EXIT_FAILURE);
     }

    while(1) {
         // Post semaphore
         sem_post(&binSem);
         printf("In main, sleep several seconds./n");
        sleep(1);
     }

     // Wait for thread synchronization
     void *threadResult;
     res = pthread_join(thdHelloWorld, &threadResult);
    if (res) {
         printf("Thread join failed!!/n");
         exit(EXIT_FAILURE);
     }

     exit(EXIT_SUCCESS);
}

void* helloWorld(void* arg) {
    while(1) {
         // Wait semaphore
         sem_wait(&binSem);
         printf("Hello World/n");
     }
}


编译运行：


[root@localhost semaphore]# gcc semaphore.c -lpthread
[root@localhost semaphore]# ./a.out
In main, sleep several seconds.
Hello World
In main, sleep several seconds.
Hello World
In main, sleep several seconds.
Hello World
In main, sleep several seconds.
Hello World

 

semaphore
　　 信号量(Semaphore)，有时被称为信号灯，是在多线程环境下使用的一种设施, 它负责协调各个线程, 以保证它们能够正确、合理的使用公共资源。
　　什么是信号量(Semaphore0
　　Semaphore分为单值和多值两种，前者只能被一个线程获得，后者可以被若干个线程获得。
　　以一个停车场是运作为例。为了简单起见，假设停车场只有三个车位，一开始三个车位都是空的。这是如果同时来了五辆车，看门人允许其中三辆不受阻碍的进入，然后放下车拦，剩下的车则必须在入口等待，此后来的车也都不得不在入口处等待。这时，有一辆车离开停车场，看门人得知后，打开车拦，放入一辆，如果又离开两辆，则又可以放入两辆，如此往复。
　　在这个停车场系统中，车位是公共资源，每辆车好比一个线程，看门人起的就是信号量的作用。
　　更进一步，信号量的特性如下：信号量是一个非负整数（车位数），所有通过它的线程（车辆）都会将该整数减一（通过它当然是为了使用资源），当该整数值为零时，所有试图通过它的线程都将处于等待状态。在信号量上我们定义两种操作： Wait（等待） 和 Release（释放）。 当一个线程调用Wait等待）操作时，它要么通过然后将信号量减一，要么一自等下去，直到信号量大于一或超时。Release（释放）实际上是在信号量上执行加操作，对应于车辆离开停车场，该操作之所以叫做“释放”是应为加操作实际上是释放了由信号量守护的资源。
　　实现
　　大家都知道，.Net Framework类库中提供的线程同步设施包括：
　　Monitor， AutoResetEvent， ManualResetEvent，Mutex，ReadWriteLock和 InterLock。 其中 AutoResetEvent， ManualResetEvent，Mutex派生自WaitHandler，它们实际上是封装了操作系统提供的内核对象。而其它的应当是在.Net虚拟机中土生土长的。显然来自操作系统内核对象的设施使用起来效率要差一些。不过效率并不是我们这里要考虑的问题，我们将使用两个 Monitor 和 一个ManualResetEvent 对象来模拟一个信号量。
　　代码如下：
　　public class Semaphore
　　{
　    　private ManualResetEvent waitEvent = new ManualResetEvent(false);
　　    private object syncObjWait = new object();
　　    private int maxCount = 1; file://最大资源数
　　    private int currentCount = 0; file://当前资源数
　　    public Semaphore()
　　{
　　}
　　   public Semaphore( int maxCount )
　　{
　　   this.maxCount = maxCount;
　　}
　　public bool Wait()
　　{
　　   lock( syncObjWait ) file://只能一个线程进入下面代码
　　   {
　　       bool waitResult = this.waitEvent.WaitOne(); file://在此等待资源数大于零
　　       if( waitResult )
　　       {
　　         lock( this )
　　           {
　　             if( currentCount > 0 )
　　               {
　　                  currentCount--;
　　                  if( currentCount == 0 )
　　                   {
　　                       this.waitEvent.Reset();
　                   　}
　　               }
　　         else
　　          {
　　               System.Diagnostics.Debug.Assert( false, "Semaphore is not allow current count < 0" );
　　          }
　　      }
　　  }
　　   return waitResult;
　　 }
　　}
　　/** <summary>
　　/// 允许超时返回的 Wait 操作
　　/// </summary>
　　/// <param name="millisecondsTimeout"></param>
　　/// <returns></returns>
　　public bool Wait( int millisecondsTimeout )
　　{
　　     lock( syncObjWait ) // Monitor 确保该范围类代码在临界区内
　　        {
　　           bool waitResult = this.waitEvent.WaitOne(millisecondsTimeout,false);
　　          if( waitResult )
　　          {
　　             lock( this )
　　             {
　　                if( currentCount > 0 )
　　                {
　　                    currentCount--;
　　                    if( currentCount == 0 )
　　                     {
　　                        this.waitEvent.Reset();
　　                      }
　　                  }
　　               else
　　               {
　　                     System.Diagnostics.Debug.Assert( false, "Semaphore is not allow current count < 0" );
　                　}
　             　}
　　          }
　　      return waitResult;
　　     }
　　}
　　public bool Release()
　　{
　　        lock( this ) // Monitor 确保该范围类代码在临界区内
　　       {
　　           currentCount++;
　　           if( currentCount > this.maxCount )
　　          {
　　             currentCount = this.maxCount;
　　             return false;
　　          }
　           　this.waitEvent.Set(); file://允许调用Wait的线程进入
　　        }
　　      return true;
　　     }
　　}
 