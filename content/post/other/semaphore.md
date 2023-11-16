---
title: semaphore/信号量, mutex/互斥锁
author: "-"
date: 2014-10-31T02:46:50+00:00
url: semaphore
categories:
  - OS
tags:
  - reprint
---
## 信号量 Semaphore

信号量是 Edsger Dijkstra 发明的数据结构，在解决多种同步问题时很有用。其本质是一个整数，并关联两个操作：

申请 acquire（也称为 wait、decrement 或 P 操作）
释放 release（也称 signal、increment 或 V 操作）

acquire操作将信号量减 1，如果结果值为负则线程阻塞，且直到其他线程进行了信号量累加为正数才能恢复。如结果为正数，线程则继续执行。

release操作将信号量加 1，如存在被阻塞的线程，此时他们中的一个线程将解除阻塞。

Go 运行时提供的 runtime_SemacquireMutex 和runtime_Semrelease 函数可用来实现sync.RWMutex互斥锁。

## semaphore/信号量, mutex/互斥锁

Mutex 是一把钥匙，一个人拿了就可进入一个房间，出来的时候把钥匙交给队列的第一个。一般的用法是用于串行化对 critical section 代码的访问，保证这段代码不会被并行的运行。

Semaphore/信号量 是一件可以容纳 N 人的房间，如果人不满就可以进去，如果人满了, 就要等待有人出来. 对于N=1的情况，称为binary semaphore。一般的用法是，用于限制对于某一资源的同时访问。

### Binary semaphore 与 Mutex 的差异

在 有的系统中 Binary semaphore 与 Mutex 是没有差异的。在有的系统上，主要的差异是mutex一定要由获得锁的进程来释放。而semaphore可以由其它进程释放 (这时的semaphore实际就是个原子的变量，大家可以加或减) ，因此semaphore可以用于进程间同步。Semaphore的同步功能是所有系统都支持的，而Mutex能否由其他进程释放则未定，因此建议mutex只用于保护critical section。而semaphore则用于保护某变量，或者同步。

关于semaphore和mutex的区别，网上有著名的厕所理论 ([http://koti.mbnet.fi/niclasw/MutexSemaphore.html](http://koti.mbnet.fi/niclasw/MutexSemaphore.html)) :

#### Mutex

Mutex 的发音是 /mjuteks/ ，其含义为互斥(体)，这个词是Mutual Exclude的缩写。

Is a key to a toilet. One person can have the key - occupy the toilet - at the time. When finished, the person gives (frees) the key to the next person in the queue. Officially: "Mutexes are typically used to serialise access to a section of re-entrant code that cannot be executed concurrently by more than one thread. A mutex object only allows one thread into a controlled section, forcing other threads which attempt to gain access to that section to wait until the first thread has exited from that section."
Ref: Symbian Developer Library(A mutex is really a semaphore with value 1.)

#### Semaphore

Is the number of free identical toilet keys. Example, say we have four toilets with identical locks and keys. The semaphore count - the count of keys - is set to 4 at beginning (all four toilets are free), then the count value is decremented as people are coming in. If all toilets are full, ie. there are no free keys left, the semaphore count is 0. Now, when eq. one person leaves the toilet, semaphore is increased to 1 (one free key), and given to the next person in the queue.

Officially: “A semaphore restricts the number of simultaneous users of a shared resource up to a maximum number. Threads can request access to the resource (decrementing the semaphore), and can signal that they have finished using the resource (incrementing the semaphore).”
Ref: Symbian Developer Library

所以，mutex就是一个binary semaphore  (值就是0或者1) 。但是他们的区别又在哪里呢？主要有两个方面:

- 初始状态不一样: mutex的初始值是1 (表示锁available) ，而semaphore的初始值是0 (表示unsignaled的状态) 。随后的操 作基本一样。mutex_lock和sem_post都把值从0变成1，mutex_unlock和sem_wait都把值从1变成0 (如果值是零就等 待) 。初始值决定了: 虽然mutex_lock和sem_wait都是执行V操作，但是sem_wait将立刻将当前线程block住，直到有其他线程 post；mutex_lock在初始状态下是可以进入的。
- 用法不一样 (对称 vs. 非对称) : 这里说的是“用法”。Semaphore实现了signal，但是mutex也有signal (当一个线程lock后另外一个线程 unlock，lock住的线程将收到这个signal继续运行) 。在mutex的使用中，模型是对称的。unlock的线程也要先lock。而 semaphore则是非对称的模型，对于一个semaphore，只有一方post，另外一方只wait。就拿上面的厕所理论来说，mutex是一个钥 匙不断重复的使用，传递在各个线程之间，而semaphore择是一方不断的制造钥匙，而供另外一方使用 (另外一方不用归还) 。

前面的实验证明，mutex确实能够做到post和wait的功能，只是大家不用而已，因为它是“mutex”不是semaphore。

下面给出一个例子:

要 让一个thread在背景不断的执行，最简单的方式就是在该thread执行无穷回圈，如while(1) {}，这种写法虽可行，却会让CPU飙高到100%，因为CPU一直死死的等，其实比较好的方法是，背景平时在Sleep状态，当前景呼叫背景时，背景马 上被唤醒，执行该做的事，做完马上Sleep，等待前景呼叫。当背景sem_wait()时，就是马上处于Sleep状态，当前景sem_post() 时，会马上换起背景执行，如此就可避免CPU 100%的情形了。

```c
/**
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

```

编译运行:

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
更进一步，信号量的特性如下: 信号量是一个非负整数 (车位数) ，所有通过它的线程 (车辆) 都会将该整数减一 (通过它当然是为了使用资源) ，当该整数值为零时，所有试图通过它的线程都将处于等待状态。在信号量上我们定义两种操作:  Wait (等待)  和 Release (释放) 。 当一个线程调用Wait等待) 操作时，它要么通过然后将信号量减一，要么一自等下去，直到信号量大于一或超时。Release (释放) 实际上是在信号量上执行加操作，对应于车辆离开停车场，该操作之所以叫做“释放”是应为加操作实际上是释放了由信号量守护的资源。
实现
大家都知道，.Net Framework类库中提供的线程同步设施包括:
Monitor， AutoResetEvent， ManualResetEvent，Mutex，ReadWriteLock和 InterLock。 其中 AutoResetEvent， ManualResetEvent，Mutex派生自WaitHandler，它们实际上是封装了操作系统提供的内核对象。而其它的应当是在.Net虚拟机中土生土长的。显然来自操作系统内核对象的设施使用起来效率要差一些。不过效率并不是我们这里要考虑的问题，我们将使用两个 Monitor 和 一个ManualResetEvent 对象来模拟一个信号量。
代码如下:
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

 ---

 Mutex 的发音是 /mjuteks/ ，其含义为互斥(体)，这个词是Mutual Exclude的缩写。
Mutex在计算机中是互斥也就是排他持有的一种方式，和信号量-Semaphore有可以对比之处。有人做过如下类比:
    *Mutex是一把钥匙，一个人拿了就可进入一个房间，出来的时候把钥匙交给队列的第一个。一般的用法是用于串行化对critical section代码的访问，保证这段代码不会被并行的运行。
    * Semaphore是一件可以容纳N人的房间，如果人不满就可以进去，如果人满了，就要等待有人出来。对于N=1的情况，称为binary semaphore。一般的用法是，用于限制对于某一资源的同时访问。
对于Binary semaphore与Mutex，这两者之间就存在了很多相似之处:
    在有的系统中Binary semaphore与Mutex是没有差异的。在有的系统上，主要的差异是mutex一定要由获得锁的进程来释放。而semaphore可以由其它进程释放 (这时的semaphore实际就是个原子的变量，大家可以加或减) ，因此semaphore可以用于进程间同步。Semaphore的同步功能是所有系统都支持的，而Mutex能否由其他进程释放则未定，因此建议mutex只用于保护critical section。而semaphore则用于保护某变量，或者同步。

网摘2:  
mutex与semaphore的区别
＂互斥(mutext)和旗语(semaphore)之间有什么不同？＂这样的问题简短而有力，但要回答却相当困难．即使有经验的实时操作系统(RTOS)用户在区别如何正确使用mutex和semaphore时也存在着困难．
但这一点很不幸而且很危险，因为无任这两种原生RTOS中的哪一种被错误使用，都会导致嵌入式系统出现意想不到的错误，特别是这些系统为有关生命安全的产品时.
有关mutex和semaphore的荒诞说法是它们是相似的，甚至是可以互换的．正确的事实是尽管mutex和semaphore在它们的执行上有相似之处，但是我们还是应该在使用它们时加以区别对待．
最 普遍 (但也是不正确) 的答案是: mutex和semphore非常相似，它们只有一个区别，那就是semaphores的计数可以超过1. 差不多所有的工程师都能正确的理解: mutex是一个二进制标志，可以通过它来确保执行流在代码关键区(critical section of code)互相排斥,从而对共享资源加一保护．但当他们被要求进一步回答如何使用＂计算方法semaphore"的方式时，大部分工程师的回答就如同教科书书一般的刻板---semaphore用于保护多重同类资源．
通 过类比办法，我们很容易解释为什么"多重资源＂场景是有缺陷的.如果你认为一个 mutex是由操作系统拥有的关键值的话，我们可以很容易地将个别的mutex比喻是城市咖啡店中一间浴室的钥匙．如果你想使用浴室，却找不到钥匙，你就 必须在一个队列中等候．同样地，mutex则协串行化多项任务，以取得全域资源的共享，并且为等待队列中的任务分配一个静候其循序渐进的位置．
但这种简单的资源保护协议并不使用于两间相同浴室的情况．如果把一个semaphore概括为一个mutex，使其能保护两个或更多相同的资源，那么在我们的比喻中，它就象是放着两把相同钥匙的蓝子，你可以用任何一把打开任何一扇浴室的门．
因此，semaphore本身并不能解决多个相同资源的问题．咖啡店中的客人可能只知道有一把钥匙，但并不知道哪间浴室可用．如果你试图以此方式使用semaphore，你将会发现需要更多的状态信息---它们通常是由不同的mutex所保护的共享资源．
正确使用semaphore是为了使信号从一项任务传至另一项任务．mutex意味着取得与释放，使用受保护共享资源的每一次任务都是以这样的顺序进行．相比之下，使用semaphore的任务通常不是发送信号，就是进入等待状态，不可能同时发生．
例如，任务1可能包含程序代码，当按下＂电源＂(power)按钮时，即可提出(如发送信号或增量)一个特别的semaphore; 任务2则依据相同的semaphore而用于唤醒显示器. 在这种情况下，其中一项任务是信号的生产者，另一项任务是信号的消费者．

用一个例子来做总结，首先展示如何使用mutex:
/*Task 1*/
mutexWait(mutex_mens_room);
// Safely use shared resource
mutexRelease(mutex_mens_room);

/*Task 2*/
mutexWait(mutex_mens_room);
// Safely use shared resource
mutexRelease(mutex_mens_room);

相应地，你总是采用下列方法使用semaphore:
/*Task 1 - Producer*/
semPost(sem_power_btn); // Send the signal

/*Task 2 - Consumer*/
semPend(sem_power_btn); // Wait for signal

重 要的是，semaphores可以被interrupt service routine(ISR)中断服务程序用来向task发送信号．发送一个semaphore是一个非阻塞的RTOS行为，并且ISR安全．因为这种技术排 除了在task级别的为了是中断不使能而引起的错误的可能性，从ISR中发出信号是一种使嵌入式软件更加可靠的设计方式.

---

[https://blog.51cto.com/sddai/3106478](https://blog.51cto.com/sddai/3106478)
