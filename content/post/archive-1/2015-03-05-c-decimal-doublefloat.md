---
title: Java 轻量级锁 (Lightweight Locking)
author: wiloon
type: post
date: 2015-03-05T02:32:58+00:00
url: /?p=7381
categories:
  - Uncategorized

---
http://blog.csdn.net/hsuxu/article/details/9472389

Java的多线程安全是基于Lock机制实现的，而Lock的性能往往不如人意。
  
原因是，monitorenter与monitorexit这两个控制多线程同步的bytecode原语，是JVM依赖操作系统互斥(mutex)来实现的。
  
互斥是一种会导致线程挂起，并在较短的时间内又需要重新调度回原线程的，较为消耗资源的操作。

为了优化Java的Lock机制，从Java6开始引入了轻量级锁的概念。

轻量级锁（Lightweight Locking）本意是为了减少多线程进入互斥的几率，并不是要替代互斥。
  
它利用了CPU原语Compare-And-Swap(CAS，汇编指令CMPXCHG)，尝试在进入互斥前，进行补救。

本文将详细介绍JVM如何利用CAS，实现轻量级锁。

原理详解
  
Java Object Model中定义，Object Header是一个2字（1 word = 4 byte）长度的存储区域。
  
第一个字长度的区域用来标记同步，GC以及hash code等，官方称之为 mark word。第二个字长度的区域是指向到对象的Class。

在2个word中，mark word是轻量级锁实现的关键。它的结构见下表

从表中可以看到，state为lightweight locked的那行即为轻量级锁标记。bitfieds名为指向lock record的指针，这里的lock record，其实是一块分配在线程堆栈上的空间区域。
  
用于CAS前，拷贝object上的mark word(为什么要拷贝，请看下文)。
  
第三项是重量级锁标记。后面的状态单词很有趣，inflated，译为膨胀，在这里意思其实是锁已升级到OS-level。
  
在本文的范围内，我们只关注第二和第三项即可。

为了能直观的理解lock，unlock与mark word之间的联系，我画了一张流程图：

在图中，提到了拷贝object mark word，由于脱离了原始mark word，官方将它冠以displaced前缀，即displaced mark word(置换标记字)。
  
这个displaced mark word是整个轻量级锁实现的关键，在CAS中的compare就需要用它作为条件。

为什么要拷贝mark word？
  
其实很简单，原因是为了不想在lock与unlock这种底层操作上再加同步。

在拷贝完object mark word之后，JVM做了一步交换指针的操作，即流程中第一个橙色矩形框内容所述。
  
将object mark word里的轻量级锁指针指向lock record所在的stack指针，作用是让其他线程知道，该object monitor已被占用。
  
lock record里的owner指针指向object mark word的作用是为了在接下里的运行过程中，识别哪个对象被锁住了。

下图直观地描述了交换指针的操作。

exchange\_pointer\_1

最后一步unlock中，我们发现，JVM同样使用了CAS来验证object mark word在持有锁到释放锁之间，有无被其他线程访问。
  
如果其他线程在持有锁这段时间里，尝试获取过锁，则可能自身被挂起，而mark word的重量级锁指针也会被相应修改。
  
此时，unlock后就需要唤醒被挂起的线程。

转载请注明原文链接：http://kenwublog.com/theory-of-lightweight-locking-upon-cas