---
title: 'Juc中的同步辅助类,  CountDownLatch,CyclicBarrier,Semaphore'
author: "-"
date: 2016-11-18T01:23:59+00:00
url: /?p=9401
categories:
  - Uncategorized

tags:
  - reprint
---
## 'Juc中的同步辅助类,  CountDownLatch,CyclicBarrier,Semaphore'
CountDownLatch
  
CyclicBarrier
  
Semaphore
  
Phaser
  
Exchanger

CountDownLatch
  
在完成一组正在其他线程中执行的操作之前,它允许一个或多个线程一直等待/阻塞
  
Java的concurrent包里面的CountDownLatch其实可以把它看作一个计数器,只不过这个计数器的操作是原子操作,同时只能有一个线程去操作这个计数器,也就是同时只能有一个线程去减这个计数器里面的值。
  
你可以向CountDownLatch对象设置一个初始的数字作为计数值,任何调用这个对象上的await()方法都会阻塞,直到这个计数器的计数值被其他的线程减为0为止。
  
CountDownLatch的一个非常典型的应用场景是: 有一个任务想要往下执行,但必须要等到其他的任务执行完毕后才可以继续往下执行。假如我们这个想要继续往下执行的任务调用一个CountDownLatch对象的await()方法,其他的任务执行完自己的任务后调用同一个CountDownLatch对象上的countDown()方法,这个调用await()方法的任务将一直阻塞等待,直到这个CountDownLatch对象的计数值减到0为止。
  
<http://www.wiloon.com/?p=7869>

CyclicBarrier
  
一种可重置的多路同步点, 在某些并发编程场景很有用. 它允许一组线程互相等待, 直到到达某个公共的屏障点 (common barrier point). 在涉及一组固定大小的线程的程序中, 这些线程必须不时地互相等待, 此时 CyclicBarrier 很有用.因为该 barrier在释放等待线程后可以重用, 所以称它为循环的barrier.
  
CyclicBarrier类似于CountDownLatch也是个计数器, 不同的是CyclicBarrier数的是调用了CyclicBarrier.await()进入等待的线程数, 当线程数达到了CyclicBarrier初始时规定的数目时,所有进入等待状态的线程被唤醒并继续。 CyclicBarrier就象它名字的意思一样,可看成是个障碍, 所有的线程必须到齐后才能一起通过这个障碍。 CyclicBarrier初始时还可带一个Runnable的参数,此Runnable任务在CyclicBarrier的数目达到后,所有其它线程被唤醒前被执行。

Semaphore
  
信号量是一类经典的同步工具. 信号量通常用来限制线程可以同时访问的 (物理或逻辑) 资源数量.
  
一个计数信号量。从概念上讲,信号量维护了一个许可集。如有必要,在许可可用前会阻塞每一个 acquire(),然后再获取该许可。每个 release() 添加一个许可,从而可能释放一个正在阻塞的获取者。但是,不使用实际的许可对象,Semaphore 只对可用许可的号码进行计数,并采取相应的行动。拿到信号量的线程可以进入代码,否则就等待。通过acquire()和release()获取和释放访问许可。

Phaser
  
一种可重用的同步屏障, 功能上类似于CyclicBarrier和CountDownLatch, 但使用上更为灵活. 非常适用于在多线程环境下同步协调分阶段计算任务 (Fork/Join框架中的子任务之间需同步时, 优先使用Phaser) 
  
<http://www.wiloon.com/?p=11214>

Exchanger 允许两个线程在某个汇合点交换对象, 在某些管道设计时比较有用. Exchanger提供了一个同步点, 在这个同步点, 一对线程可以交换数据. 每个线程通过exchange()方法的入口提供数据给他的伙伴线程, 并接收他的伙伴线程提供的数据并返回. 当两个线程通过Exchanger交换了对象, 这个交换对于两个线程来说都是安全的. Exchanger可以认为是 SynchronousQueue 的双向形式, 在运用到遗传算法和管道设计的应用中比较有用.

http://zapldy.iteye.com/blog/746458
  
http://www.jianshu.com/p/d424d02ed9eb