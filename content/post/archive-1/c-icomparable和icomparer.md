---
title: 从JVM角度理解线程
author: "-"
date: 2013-07-27T06:54:08+00:00
url: /?p=5708
categories:
  - Uncategorized

tags:
  - reprint
---
## 从JVM角度理解线程
http://blog.csdn.net/iter_zc/article/details/41843595

这篇说说如何从JVM的角度来理解线程，可以对Java的线程模型有一个更加深入的理解，对GC的一些细节也会理解地更加深刻。本文基于HotSpot的OpenJDK7实现。

我们知道JVM主要是用C++实现的，JVM定义的Thread的类继承结构如下:

Class hierarchy
   
- Thread
- NamedThread 
- VMThread
       
- ConcurrentGCThread
       
- WorkerThread
         
- GangWorker
         
- GCTaskThread
     
- JavaThread
     
- WatcherThread
  
另外还有一个重要的类OSThread不在这个继承关系里，它以组合的方式被Thread类所使用

这些类构成了JVM的线程模型，其中最主要的是下面几个类: 

java.lang.Thread: 这个是Java语言里的线程类，由这个Java类创建的instance都会 1:1 映射到一个操作系统的 osthread

JavaThread: JVM中C++定义的类，一个JavaThread的instance代表了在JVM中的java.lang.Thread的instance, 它维护了线程的状态，并且维护一个指针指向java.lang.Thread创建的对象(oop)。它同时还维护了一个指针指向对应的OSThread，来获取底层操作系统创建的osthread的状态

OSThread: JVM中C++定义的类，代表了JVM中对底层操作系统的osthread的抽象，它维护着实际操作系统创建的线程句柄handle，可以获取底层osthread的状态

VMThread: JVM中C++定义的类，这个类和用户创建的线程无关，是JVM本身用来进行虚拟机操作的线程，比如GC。

有两种方式可以让用户在JVM中创建线程

  1. new java.lang.Thread().start() 
  2. 使用JNI将一个native thread attach到JVM中

针对 new java.lang.Thread().start()这种方式，只有调用start()方法的时候，才会真正的在JVM中去创建线程，主要的生命周期步骤有: 

  1. 创建对应的JavaThread的instance 
  2. 创建对应的OSThread的instance

  3. 创建实际的底层操作系统的native thread

  4. 准备相应的JVM状态，比如ThreadLocal存储空间分配等

  5. 底层的native thread开始运行，调用java.lang.Thread生成的Object的run()方法

  6. 当java.lang.Thread生成的Object的run()方法执行完毕返回后,或者抛出异常终止后，终止native thread

  7. 释放JVM相关的thread的资源，清除对应的JavaThread和OSThread

针对JNI将一个native thread attach到JVM中，主要的步骤有: 

  1. 通过JNI call AttachCurrentThread申请连接到执行的JVM实例 
  2. JVM创建相应的JavaThread和OSThread对象

  3. 创建相应的java.lang.Thread的对象

  4. 一旦java.lang.Thread的Object创建之后，JNI就可以调用Java代码了

  5. 当通过JNI call DetachCurrentThread之后，JNI就从JVM实例中断开连接

  6. JVM清除相应的JavaThread, OSThread, java.lang.Thread对象

从JVM的角度来看待线程状态的状态有以下几种:

其中主要的状态是这5种:

_thread_new: 新创建的线程

_thread_in_Java: 在运行Java代码

_thread_in_vm: 在运行JVM本身的代码

_thread_in_native: 在运行native代码

_thread_blocked: 线程被阻塞了，包括等待一个锁，等待一个条件，sleep，执行一个阻塞的IO等

从OSThread的角度，JVM还定义了一些线程状态给外部使用，比如用jstack输出的线程堆栈信息中线程的状态:

比较常见有:

Runnable: 可以运行或者正在运行的

MONITOR_WAIT: 等待锁

OBJECT_WAIT: 执行了Object.wait()之后在条件队列中等待的

SLEEPING: 执行了Thread.sleep()的

从JavaThread的角度，JVM定义了一些针对Java Thread对象的状态，基本类似，多了一个TIMED_WAITING的状态，用来表示定时阻塞的状态

最后来看一下JVM内部的VM Threads，主要由几类:

VMThread: 执行JVM本身的操作

Periodic task thread: JVM内部执行定时任务的线程

GC threads: GC相关的线程，比如单线程/多线程的GC收集器使用的线程

Compiler threads: JIT用来动态编译的线程

Signal dispatcher thread: Java解释器Interceptor用来辅助safepoint操作的线程

具体的VMThread的作用，会在讲safepoint的时候细说，就写到这里吧

参考: Hotspot JVM thread management