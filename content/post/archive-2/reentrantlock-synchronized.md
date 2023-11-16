---
title: Java ReentrantLock, synchronized
author: "-"
date: 2017-03-26T03:00:39+00:00
url: /?p=9958
categories:
  - Inbox
tags:
  - reprint
---
## Java ReentrantLock, synchronized

[http://www.ibm.com/developerworks/cn/java/j-jtp10264/index.html](http://www.ibm.com/developerworks/cn/java/j-jtp10264/index.html)

多线程和并发性并不是什么新内容,但是 Java 语言设计中的创新之一就是,它是第一个直接把跨平台线程模型和正规的内存模型集成到语言中的主流语言。核心类库包含一个 Thread 类,可以用它来构建、启动和操纵线程,Java 语言包括了跨线程传达并发性约束的构造 - synchronized 和 volatile. 在简化与平台无关的并发类的开发的同时,它决没有使并发类的编写工作变得更繁琐,只是使它变得更容易了。

### synchronized 快速回顾

把代码块声明为 synchronized,有两个重要后果, 通常是指该代码具有 原子性 (atomicity) 和 可见性 (visibility) 。
  
原子性意味着一个线程一次只能执行由一个指定监控对象 (lock) 保护的代码,从而防止多个线程在更新共享状态时相互冲突。
  
可见性则更为微妙;它要对付内存缓存和编译器优化的各种反常行为。一般来说,线程以某种不必让其他线程立即可以看到的方式 (不管这些线程在寄存器中、在处理器特定的缓存中,还是通过指令重排或者其他编译器优化) ,不受缓存变量值的约束,但是如果开发人员使用了同步,如下面的代码所示,那么运行库将确保某一线程对变量所做的更新先于对现有synchronized 块所进行的更新,当进入由同一监控器 (lock) 保护的另一个 synchronized 块时,将立刻可以看到这些对变量所做的更新。类似的规则也存在于 volatile 变量上。

```java
synchronized (lockObject) {
// update object state
}
```

所以,实现同步操作需要考虑安全更新多个共享变量所需的一切,不能有争用条件, 不能破坏数据 (假设同步的边界位置正确) ,而且要保证正确同步的其他线程可以看到这些变量的最新值。通过定义一个清晰的、跨平台的内存模型 (该模型在 JDK 5.0 中做了修改,改正了原来定义中的某些错误) ,通过遵守下面这个简单规则,构建"一次编写,随处运行"的并发类是有可能的:

不论什么时候,只要您将编写的变量接下来可能被另一个线程读取,或者您将读取的变量最后是被另一个线程写入的,那么您必须进行同步。
  
不过现在好了一点,在最近的 JVM 中,没有争用的同步 (一个线程拥有锁的时候,没有其他线程企图获得锁) 的性能成本还是很低的。 (也不总是这样；早期 JVM 中的同步还没有优化,所以让很多人都这样认为,但是现在这变成了一种误解,人们认为不管是不是争用,同步都有很高的性能成本。)

对 synchronized 的改进
  
如此看来同步相当好了,是么？那么为什么 JSR 166 小组花了这么多时间来开发 java.util.concurrent.lock 框架呢？ 答案很简单－同步是不错,但它并不完美。它有一些功能性的限制 —— 它无法中断一个正在等候获得锁的线程,也无法通过投票得到锁,如果不想等下去,也就没法得到锁。同步还要求锁的释放只能在与获得锁所在的堆栈帧相同的堆栈帧中进行,多数情况下,这没问题 (而且与异常处理交互得很好) ,但是,确实存在一些非块结构的锁定更合适的情况。

### ReentrantLock/重入锁

ReentrantLock的实现不仅可以替代隐式的 synchronized 关键字,而且能够提供超过关键字本身的多种功能。
  
这里提到一个锁获取的公平性问题,如果在绝对时间上,先对锁进行获取的请求一定被先满足,那么这个锁是公平的,反之,是不公平的,也就是说等待时间最长的线程最有机会获取锁,也可以说锁的获取是有序的。ReentrantLock 这个锁提供了一个构造函数,能够控制这个锁是否是公平的。
  
而锁的名字也是说明了这个锁具备了重复进入的可能,也就是说能够让当前线程多次的进行对锁的获取操作, 这样的最大次数限制是Integer.MAX_VALUE,约21亿次左右。
  
事实上公平的锁机制往往没有非公平的效率高,因为公平的获取锁没有考虑到操作系统对线程的调度因素,这样造成JVM对于等待中的线程调度次序和操作系统对线程的调度之间的不匹配。对于锁的快速且重复的获取过程中,连续获取的概率是非常高的,而公平锁会压制这种情况,虽然公平性得以保障,但是响应比却下降了,但是并不是任何场景都是以TPS作为唯一指标的,因为公平锁能够减少"饥饿"发生的概率,等待越久的请求越是能够得到优先满足。

java.util.concurrent.lock 中的 Lock 框架是锁定的一个抽象,它允许把锁定的实现作为 Java 类,而不是作为语言的特性来实现。这就为 Lock 的多种实现留下了空间,各种实现可能有不同的调度算法、性能特性或者锁定语义。 ReentrantLock 类实现了 Lock ,它拥有与 synchronized 相同的并发性和内存语义,但是添加了类似锁投票、定时锁等候和可中断锁等候的一些特性。此外,它还提供了在激烈争用情况下更佳的性能。 (换句话说,当许多线程都想访问共享资源时,JVM 可以花更少的时候来调度线程,把更多时间用在执行线程上。)

reentrant 锁意味着什么呢？简单来说,它有一个与锁相关的获取计数器,如果拥有锁的某个线程再次得到锁,那么获取计数器就加1,然后锁需要被释放两次才能获得真正释放。这模仿了 synchronized 的语义；如果线程进入由线程已经拥有的监控器保护的 synchronized 块,就允许线程继续进行,当线程退出第二个 (或者后续)  synchronized 块的时候,不释放锁,只有线程退出它进入的监控器保护的第一个 synchronized 块时,才释放锁。

在查看清单 1 中的代码示例时,可以看到 Lock 和 synchronized 有一点明显的区别 —— lock 必须在 finally 块中释放。否则,如果受保护的代码将抛出异常,锁就有可能永远得不到释放！这一点区别看起来可能没什么,但是实际上,它极为重要。忘记在 finally 块中释放锁,可能会在程序中留下一个定时炸弹,当有一天炸弹爆炸时,您要花费很大力气才有找到源头在哪。而使用同步,JVM 将确保锁会获得自动释放。

清单 1. 用 ReentrantLock 保护代码块。
  
Lock lock = new ReentrantLock();
  
lock.lock();
  
try {
  
// update object state
  
}
  
finally {
  
lock.unlock();
  
}

除此之外,与目前的 synchronized 实现相比,争用下的 ReentrantLock 实现更具可伸缩性。 (在未来的 JVM 版本中,synchronized 的争用性能很有可能会获得提高。) 这意味着当许多线程都在争用同一个锁时,使用 ReentrantLock 的总体开支通常要比 synchronized 少得多。
  
比较 ReentrantLock 和 synchronized 的可伸缩性

Tim Peierls 用一个简单的线性全等伪随机数生成器 (PRNG) 构建了一个简单的评测,用它来测量 synchronized 和 Lock 之间相对的可伸缩性。这个示例很好,因为每次调用 nextRandom() 时,PRNG 都确实在做一些工作,所以这个基准程序实际上是在测量一个合理的、真实的 synchronized 和 Lock 应用程序,而不是测试纯粹纸上谈兵或者什么也不做的代码 (就像许多所谓的基准程序一样。)

在这个基准程序中,有一个 PseudoRandom 的接口,它只有一个方法 nextRandom(int bound) 。该接口与 java.util.Random 类的功能非常类似。因为在生成下一个随机数时,PRNG 用最新生成的数字作为输入,而且把最后生成的数字作为一个实例变量来维护,其重点在于让更新这个状态的代码段不被其他线程抢占,所以我要用某种形式的锁定来确保这一点。 ( java.util.Random 类也可以做到这点。) 我们为 PseudoRandom 构建了两个实现；一个使用 syncronized,另一个使用 java.util.concurrent.ReentrantLock 。驱动程序生成了大量线程,每个线程都疯狂地争夺时间片,然后计算不同版本每秒能执行多少轮。图 1 和 图 2 总结了不同线程数量的结果。这个评测并不完美,而且只在两个系统上运行了 (一个是双 Xeon 运行超线程 Linux,另一个是单处理器 Windows 系统) ,但是,应当足以表现 synchronized 与 ReentrantLock 相比所具有的伸缩性优势了。
  
图 1 和图 2 中的图表以每秒调用数为单位显示了吞吐率,把不同的实现调整到 1 线程 synchronized 的情况。每个实现都相对迅速地集中在某个稳定状态的吞吐率上,该状态通常要求处理器得到充分利用,把大多数的处理器时间都花在处理实际工作 (计算机随机数) 上,只有小部分时间花在了线程调度开支上。您会注意到,synchronized 版本在处理任何类型的争用时,表现都相当差,而 Lock 版本在调度的开支上花的时间相当少,从而为更高的吞吐率留下空间,实现了更有效的 CPU 利用。
  
条件变量

根类 Object 包含某些特殊的方法,用来在线程的 wait() 、 notify() 和 notifyAll() 之间进行通信。这些是高级的并发性特性,许多开发人员从来没有用过它们 —— 这可能是件好事,因为它们相当微妙,很容易使用不当。幸运的是,随着 JDK 5.0 中引入 java.util.concurrent ,开发人员几乎更加没有什么地方需要使用这些方法了。

通知与锁定之间有一个交互 —— 为了在对象上 wait 或 notify ,您必须持有该对象的锁。就像 Lock 是同步的概括一样, Lock 框架包含了对 wait 和 notify 的概括,这个概括叫作 条件 (Condition)  。 Lock 对象则充当绑定到这个锁的条件变量的工厂对象,与标准的 wait 和 notify 方法不同,对于指定的 Lock ,可以有不止一个条件变量与它关联。这样就简化了许多并发算法的开发。例如, 条件 (Condition)  的 Javadoc 显示了一个有界缓冲区实现的示例,该示例使用了两个条件变量,"not full"和"not empty",它比每个 lock 只用一个 wait 设置的实现方式可读性要好一些 (而且更有效) 。 Condition 的方法与 wait 、 notify 和 notifyAll 方法类似,分别命名为 await 、 signal 和 signalAll ,因为它们不能覆盖 Object 上的对应方法。
  
这不公平

如果查看 Javadoc,您会看到, ReentrantLock 构造器的一个参数是 boolean 值,它允许您选择想要一个 公平 (fair) 锁,还是一个 不公平 (unfair) 锁。公平锁使线程按照请求锁的顺序依次获得锁；而不公平锁则允许讨价还价,在这种情况下,线程有时可以比先请求锁的其他线程先得到锁。

为什么我们不让所有的锁都公平呢？毕竟,公平是好事,不公平是不好的,不是吗？ (当孩子们想要一个决定时,总会叫嚷"这不公平"。我们认为公平非常重要,孩子们也知道。) 在现实中,公平保证了锁是非常健壮的锁,有很大的性能成本。要确保公平所需要的记帐 (bookkeeping) 和同步,就意味着被争夺的公平锁要比不公平锁的吞吐率更低。作为默认设置,应当把公平设置为 false ,除非公平对您的算法至关重要,需要严格按照线程排队的顺序对其进行服务。

那么同步又如何呢？内置的监控器锁是公平的吗？答案令许多人感到大吃一惊,它们是不公平的,而且永远都是不公平的。但是没有人抱怨过线程饥渴,因为 JVM 保证了所有线程最终都会得到它们所等候的锁。确保统计上的公平性,对多数情况来说,这就已经足够了,而这花费的成本则要比绝对的公平保证的低得多。所以,默认情况下 ReentrantLock 是"不公平"的,这一事实只是把同步中一直是事件的东西表面化而已。如果您在同步的时候并不介意这一点,那么在 ReentrantLock 时也不必为它担心。

图 3 和图 4 包含与 图 1和 图 2 相同的数据,只是添加了一个数据集,用来进行随机数基准检测,这次检测使用了公平锁,而不是默认的协商锁。正如您能看到的,公平是有代价的。如果您需要公平,就必须付出代价,但是请不要把它作为您的默认选择。

处处都好？

看起来 ReentrantLock 无论在哪方面都比 synchronized 好 —— 所有 synchronized 能做的,它都能做,它拥有与 synchronized 相同的内存和并发性语义,还拥有 synchronized 所没有的特性,在负荷下还拥有更好的性能。那么,我们是不是应当忘记 synchronized ,不再把它当作已经已经得到优化的好主意呢？或者甚至用 ReentrantLock 重写我们现有的 synchronized 代码？实际上,几本 Java 编程方面介绍性的书籍在它们多线程的章节中就采用了这种方法,完全用 Lock 来做示例,只把 synchronized 当作历史。但我觉得这是把好事做得太过了。

还不要抛弃 synchronized

虽然 ReentrantLock 是个非常动人的实现,相对 synchronized 来说,它有一些重要的优势,但是我认为急于把 synchronized 视若敝屣,绝对是个严重的错误。 java.util.concurrent.lock 中的锁定类是用于高级用户和高级情况的工具 。一般来说,除非您对 Lock 的某个高级特性有明确的需要,或者有明确的证据 (而不是仅仅是怀疑) 表明在特定情况下,同步已经成为可伸缩性的瓶颈,否则还是应当继续使用 synchronized。

为什么我在一个显然"更好的"实现的使用上主张保守呢？因为对于 java.util.concurrent.lock 中的锁定类来说,synchronized 仍然有一些优势。比如,在使用 synchronized 的时候,不能忘记释放锁；在退出 synchronized 块时,JVM 会为您做这件事。您很容易忘记用 finally 块释放锁,这对程序非常有害。您的程序能够通过测试,但会在实际工作中出现死锁,那时会很难指出原因 (这也是为什么根本不让初级开发人员使用 Lock 的一个好理由。)

另一个原因是因为,当 JVM 用 synchronized 管理锁定请求和释放时,JVM 在生成线程转储时能够包括锁定信息。这些对调试非常有价值,因为它们能标识死锁或者其他异常行为的来源。 Lock 类只是普通的类,JVM 不知道具体哪个线程拥有 Lock 对象。而且,几乎每个开发人员都熟悉 synchronized,它可以在 JVM 的所有版本中工作。在 JDK 5.0 成为标准 (从现在开始可能需要两年) 之前,使用 Lock 类将意味着要利用的特性不是每个 JVM 都有的,而且不是每个开发人员都熟悉的。

什么时候选择用 ReentrantLock 代替 synchronized

既然如此,我们什么时候才应该使用 ReentrantLock 呢？答案非常简单 —— 在确实需要一些 synchronized 所没有的特性的时候,比如时间锁等候、可中断锁等候、无块结构锁、多个条件变量或者锁投票。 ReentrantLock 还具有可伸缩性的好处,应当在高度争用的情况下使用它,但是请记住,大多数 synchronized 块几乎从来没有出现过争用,所以可以把高度争用放在一边。我建议用 synchronized 开发,直到确实证明 synchronized 不合适,而不要仅仅是假设如果使用 ReentrantLock "性能会更好"。请记住,这些是供高级用户使用的高级工具。 (而且,真正的高级用户喜欢选择能够找到的最简单工具,直到他们认为简单的工具不适用为止。) 。一如既往,首先要把事情做好,然后再考虑是不是有必要做得更快。
  
Lock 框架是同步的兼容替代品,它提供了 synchronized 没有提供的许多特性,它的实现在争用下提供了更好的性能。但是,这些明显存在的好处,还不足以成为用 ReentrantLock 代替 synchronized 的理由。相反,应当根据您是否 需要 ReentrantLock 的能力来作出选择。大多数情况下,您不应当选择它 —— synchronized 工作得很好,可以在所有 JVM 上工作,更多的开发人员了解它,而且不太容易出错。只有在真正需要 Lock 的时候才用它。在这些情况下,您会很高兴拥有这款工具。

### ReentrantLock与synchronized的系统调用

背景
网上一大票文章都在说Java中的synchronized锁是重量级锁,因为使用了系统调用,会从用户态陷入内核态,开销很大, 性能影响大,而ReentrantLock使用的是CAS轻量级操作,性能开销小,虽然JDK1.6后对synchronized进行了锁升级的优化,但是还是避免不了人们synchronized性能比不上ReentrantLock的刻板映像！

究其原因就是synchronized很重！有系统调用,会从用户态陷入内核态,那ReentrantLock有没有系统调用呢？那么本文就从系统调用的角度分析一下两者

长文预警！！！

前置知识
ReentrantLock原理
一图胜前言,ReentrantLock从大局上看原理如下 (注意ReentrantLock继承自AbstractQueuedSynchronizer)

一个数字state表示资源,一个线程尝试CAS地去+1,操作成功即上锁,那么可以欢快的执行锁内的代码
另一个哥们(线程)也来尝试CAS地+1,不好意思锁别人占着,你乖乖排队去 (双向的CLH队列) 阻塞,后面的线程来抢锁,抢不到都排队去就完事
第一个线程执行完释放锁资源,此时只有它自己在执行,欢快的将state置0 (不用CAS) ,然后叫醒排在它后面的哥们 (即队列中第二个节点) 执行。
大体逻辑如上,其中涉及到很多对共享变量CAS自旋的细节操作,比如CAS入队、CAS操作state,不是文本重点,此处不细表

synchronized原理
synchronized由于是JDK自带的锁,是JVM层面去实现的 (因为JDK1.6后synchronized有锁升级的过程,此处只分析synchronized重量级锁) ,具体是用ObjectMonitor来实现,开局一张原理图

ObjectMonitor主要数据结构如下

ObjectMonitor() {
    _count        = 0;   // 记录个数
    ...
    _owner        = NULL;//持有锁线程
    _WaitSet      = NULL;// 处于wait状态的线程,会被加入到_WaitSet
    ...
    _EntryList    = NULL;// 处于等待锁block状态的线程,会被加入到该列表
  }
想要获取monitor (即锁) 的线程,首先会进入_EntryList队列。
当某个线程获取到对象的monitor后,进入_Owner区域,设置为当前线程,同时计数器_count+1
如果线程调用了Object#wait()方法,则会进入_WaitSet队列。它会释放monitor锁,即将_owner赋值为null,并且_count-1,进入_WaitSet队列阻塞等待。
如果其他线程调用 Object#notify() / notifyAll() ,会唤醒_WaitSet中的某个线程,该线程再次尝试获取monitor锁,成功即进入_Owner区域。
同步方法执行完毕了,线程退出临界区,会将monitor的_owner设为null,并释放监视锁。
系统调用
在电脑中,系统调用 (英语: system call) ,指运行在用户空间的程序向操作系统内核请求需要更高权限运行的服务。系统调用提供用户程序与操作系统之间的接口。大多数系统交互式操作需求在内核态运行。如设备IO操作或者进程间通信。
说人话就是操作系统像一个黑盒子,运行在计算机硬件之上,你自己写的软件需要调用硬件的某些功能比如从磁盘打开一部电影,你的软件没法和硬盘直接交互的,必须告诉这个黑盒子,让黑盒子去硬盘里面去取,为啥要这样设计？

安全性与稳定性: 操作系统的东西你一个应用层软件不能乱碰,碰坏了宕机谁负责？这个能靠应用层软件自觉遵守？那肯定不行,否则就没有那么多病毒程序了,因此操作系统干脆直接不让你碰,只开放了安全的接口 (系统调用) 提供给你调用。
屏蔽硬件的复杂性: 硬件千奇百怪,各种型号,需要各种匹配的驱动才能运行,一个应用层软件想从硬盘读取数据,如果没有操作系统这个黑盒子给你提供便利 (系统调用) ,那你要从硬盘驱动开始写？等你写好了塑料花儿都谢了。
所以,系统调用开销是很大的,因此在程序中尽量减少系统调用的次数,并且让每次系统调用完成尽可能多的工作,例如每次读写大量的数据而不是每次仅读写一个字符。

那么Linux有哪些系统调用？这里可以查(系统调用表): [http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64](http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64)

从系统调用的角度分析
就一个锁而言,那么关键的东西我认为是如何上锁以及如何让线程阻塞以及唤醒线程,那么就从这三个方面分析

ReentrantLock
如何上锁
所谓上锁在ReentrantLock就是给state变量+1,state声明如下,注意是volatile的,也就是在多线程环境下对每个线程都是可见的

private volatile int state;
那么很多线程都在抢这把锁,只有一个线程能抢到 (即能执行state+1成功) ,怎么保证线程安全？答案是CAS,CAS是啥？简单来说就是Compare And Swap,即比较并替换: 给一个预期值E和一个更新值U,如果当前值A和预期值E相等,则更新A为U。感觉是不是有点像乐观锁？

int c = getState();//c是state
if (c == 0) {//锁还没被别人抢
        if (compareAndSetState(0, acquires)) {//重点是这句,CAS方式设置state
        setExclusiveOwnerThread(current);
        return true;
    }
}
继续跟下去,调用了unsafe的compareAndSwapInt,在往下就是native方法了

protected final boolean compareAndSetState(int expect, int update) {
    // See below for intrinsics setup to support this
    return unsafe.compareAndSwapInt(this, stateOffset, expect, update);
}

/**

* 源码在[http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/687fd7c7986d/src/share/classes/sun/misc/Unsafe.java](http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/687fd7c7986d/src/share/classes/sun/misc/Unsafe.java)
* Unsafe.compareAndSwapInt
* Atomically update Java variable to x if it is currently
* holding expected
* @return true if successful
*/
public final native boolean compareAndSwapInt(Object o, long offset,
                                              int expected,
                                              int x);
继续跟踪在JVM中的实现,源码位置: [http://hg.openjdk.java.net/jdk8/jdk8/hotspot/file/tip/src/share/vm/prims/unsafe.cpp](http://hg.openjdk.java.net/jdk8/jdk8/hotspot/file/tip/src/share/vm/prims/unsafe.cpp)

UNSAFE_ENTRY(jboolean, Unsafe_CompareAndSwapInt(JNIEnv *env, jobject unsafe, jobject obj, jlong offset, jint e, jint x))
  UnsafeWrapper("Unsafe_CompareAndSwapInt");
  oop p = JNIHandles::resolve(obj);
  jint* addr = (jint *) index_oop_from_field_offset_long(p, offset);
  return (jint)(Atomic::cmpxchg(x, addr, e)) == e;//此处调用了Atomic::cmpxchg
UNSAFE_END
里面又调用了Atomic::cmpxchg,源码位置: [http://hg.openjdk.java.net/jdk8/jdk8/hotspot/file/87ee5ee27509/src/os_cpu/linux_x86/vm/atomic_linux_x86.inline.hpp](http://hg.openjdk.java.net/jdk8/jdk8/hotspot/file/87ee5ee27509/src/os_cpu/linux_x86/vm/atomic_linux_x86.inline.hpp)

inline jint     Atomic::cmpxchg    (jint     exchange_value, volatile jint*     dest, jint     compare_value) {
  int mp = os::is_MP();
  __asm__ volatile (LOCK_IF_MP(%4) "cmpxchgl %1,(%3)"
                    : "=a" (exchange_value)
                    : "r" (exchange_value), "a" (compare_value), "r" (dest), "r" (mp)
                    : "cc", "memory");
  return exchange_value;
}
__asm__表示是汇编指令
LOCK_IF_MP,是否是多核处理器,如果是加上lock指令
lock 和cmpxchgl是CPU指令,lock指令是个前缀,可以修饰其他指令,cmpxchgl即为CAS指令
这个lock才是主角,它才是实现CAS的原子性的关键 (因为现在基本都是多核处理器了,那么肯定会存在多个核心争抢资源的情况) ,在Intel® 64 and IA-32 Architectures Software Developer’s Manual 中的章节LOCK—Assert LOCK# Signal Prefix 中给出LOCK指令的详细解释

总线锁
LOCK#信号就是我们经常说到的总线锁,处理器使用LOCK#信号达到锁定总线,来解决原子性问题,当一个处理器往总线上输出LOCK#信号时,其它处理器的请求将被阻塞,此时该处理器此时独占共享内存；总线锁这种做法锁定的范围太大了,导致CPU利用率急剧下降,因为使用LOCK#是把CPU和内存之间的通信锁住了,这使得锁定时期间,其它处理器不能操作其内存地址的数据 ,所以总线锁的开销比较大。

缓存锁
如果访问的内存区域已经缓存在处理器的缓存行中,P6系统和之后系列的处理器则不会声明LOCK#信号,它会对CPU的缓存中的缓存行进行锁定,在锁定期间,其它 CPU 不能同时缓存此数据,在修改之后,通过缓存一致性协议 (在Intel CPU中,则体现为MESI协议) 来保证修改的原子性,这个操作被称为缓存锁

lock指令会产生总线锁也可能会产生缓存锁,看具体的条件,有下面几种情况只能使用总线锁

当操作的数据不能被缓存在处理器内部,这个必须得使用总线锁了
操作的数据跨多个缓存行 (cache line) ,缓存锁的前置条件是多个数据在一个缓存行里面
有些处理器不支持缓存锁定。对于Intel 486和奔腾处理器,就算锁定的内存区域在处理器的缓存行中也会调用总线锁定。
无论是总线锁还是缓存锁这都是CPU在硬件层面上提供的锁,肯定效率比软件层面的锁要高

再来总结一下ReentrantLock如何上锁？

compareAndSetState -> Unsafe.compareAndSwapInt -> JNI(JVM) -> Atomic::cmpxchg -> lock cmpxchg(CPU指令)
绕了一大圈,上锁过程使用了系统调用吗？答案是没有 (会在文末证明) ,在系统调用表里面都搜不到,总体说来上锁过程还算是非常高效的！

如何阻塞
线程抢不到锁会进入队列阻塞,那么到底是什么阻塞的？下面一步一步来看

首先是调用了LockSupport.park(),park直译为停车,线程停车即阻塞,线程就阻塞在这里一动不动了,不会网下执行, LockSupport.park调用了Unsafe.park,这又是一个native方法

private final boolean parkAndCheckInterrupt() {
    LockSupport.park(this);//阻塞
    return Thread.interrupted();
}

/**

* 源码在[http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/687fd7c7986d/src/share/classes/sun/misc/Unsafe.java](http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/687fd7c7986d/src/share/classes/sun/misc/Unsafe.java)
* Block current thread, returning when a balancing
* unpark occurs, or a balancing unpark has
* already occurred, or the thread is interrupted, or, if not
* absolute and time is not zero, the given time nanoseconds have
* elapsed, or if absolute, the given deadline in milliseconds
* since Epoch has passed, or spuriously (i.e., returning for no
* "reason"). Note: This operation is in the Unsafe class only
* because unpark is, so it would be strange to place it
* elsewhere.
 */
public native void park(boolean isAbsolute, long time);
看JVM中Unsafe.park的实现,源码在[http://hg.openjdk.java.net/jdk8/jdk8/hotspot/file/tip/src/share/vm/prims/unsafe.cpp](http://hg.openjdk.java.net/jdk8/jdk8/hotspot/file/tip/src/share/vm/prims/unsafe.cpp)

UNSAFE_ENTRY(void, Unsafe_Park(JNIEnv *env, jobject unsafe, jboolean isAbsolute, jlong time))
  ...省略
  thread->parker()->park(isAbsolute != 0, time);
  ...省略
UNSAFE_END
调用了parker()->park(),即Parker::park,看一下Parker的定义,源码在[http://hg.openjdk.java.net/jdk7/jdk7/hotspot/file/81d815b05abb/src/share/vm/runtime/park.hpp](http://hg.openjdk.java.net/jdk7/jdk7/hotspot/file/81d815b05abb/src/share/vm/runtime/park.hpp)

class Parker : public os::PlatformParker {
    public:
      // For simplicity of interface with Java, all forms of park (indefinite,
      // relative, and absolute) are multiplexed into one call.
      void park(bool isAbsolute, jlong time);
      void unpark();
}
继承自PlatformParker,而PlatformParker是与平台相关的实现,屏蔽了平台的区别,park具体的实现和平台相关,下面是Linux中的实现,windows的实现可以参考hotspot\src\os\windows\vm\os_windows.cpp

void Parker::park(bool isAbsolute, jlong time) {
    //  如果别的线程已经unblock了我.  
    //  这里并没有拿到mutex的锁, 需要Atomic::xchg和barrier保证lock-free代码的正确。
    // We depend on Atomic::xchg() having full barrier semantics
    // since we are doing a lock-free update to _counter.
    // 通过原子操作来提升性能,可以跳过 mutex 加锁
    if (Atomic::xchg(0, &_counter) > 0) return;
    // safepoint region相关
    ThreadBlockInVM tbivm(jt);
    // 如果别的线程正在unblock我, 而持有了mutex, 我先返回了,没有必要在_mutex上等
    if (Thread::is_interrupted(thread, false) || pthread_mutex_trylock(_mutex) != 0) {
        return;
    }
    // 如果别的线程已经unblock了我, no wait needed
    // 已经拿到了mutex, 检查 _counter 大于 0 说明其他线程执行过 unpark,这里就可以跳过等待过程
    int status;
    if (_counter > 0)  {
        _counter = 0;
        status = pthread_mutex_unlock(_mutex);
        OrderAccess::fence();
        return;
    }
    // 记录线程的状态
    OSThreadWaitState osts(thread->osthread(), false /*not Object.wait()*/);
    jt->set_suspend_equivalent();
    // cleared by handle_special_suspend_equivalent_condition() or java_suspend_self()
    if (time == 0) {
        _cur_index = REL_INDEX; // arbitrary choice when not timed
        // 进入等待并自动释放 mutex 锁,这里没有通过 while 包裹 wait 过程,所以会出现伪唤醒问题
        status = pthread_cond_wait(&_cond[_cur_index], _mutex);
    } else {
        _cur_index = isAbsolute ? ABS_INDEX : REL_INDEX;
        // 进入等待并自动释放 mutex 锁,这里没有通过 while 包裹 wait 过程,所以会出现伪唤醒问题
        status = pthread_cond_timedwait(&_cond[_cur_index],_mutex, &absTime);
    }
    _cur_index = -1;
    // 已经从block住状态中恢复返回了, 把_counter设0.
    _counter = 0;
    status = pthread_mutex_unlock(_mutex);
    // 要保证多线程的正确性要十二分小心
    // 这里的memory fence 是一个lock addl 指令, 加上compiler_barrier
    // 保证_counter = 0 是对其他线程是可见的.
    // Paranoia to ensure our locked and lock-free paths interact
    // correctly with each other and Java-level accesses.
    OrderAccess::fence();
    // 已经醒过来, 但如果有别人在suspend我,那么继续suspend自己.
    // If externally suspended while waiting, re-suspend
    if (jt->handle_special_suspend_equivalent_condition()) {
        jt->java_suspend_self();
    }
}
其实park方法内部也用了CAS！重点关注一下此调用: pthread_cond_wait,就是调用此函数让线程阻塞的,这是POSIX线程(pthread)函数库中一个函数,感兴趣的可以看下它的源码: [https://code.woboq.org/userspace/glibc/nptl/pthread_cond_wait.c.html](https://code.woboq.org/userspace/glibc/nptl/pthread_cond_wait.c.html)

pthread_cond_wait内部调用了futex,而futex里面进行了系统调用sys_futex！那么futex是啥？参考下man 2 futex

在Linux中,为了挂起线程,使用 futex,futex 即 Fast user space mutex
futex 通过用户态和内核配合,可以减小开销,并且线程灵活可控是否要进入睡眠等待还是spin等待。
futex 构成
futex 由一个32bit的futex word和一个系统调用sys_futex组成,futex word是进行互斥的变量,sys_futex 是通知内核对线程进行挂起和唤醒。
futex的使用模式
用户线程 通过 CAS 类原子指令尝试获取锁,如果成功,则获取锁成功。这种情况下无需调用系统调用,不需要进入内核。开销很小。
如果CAS失败,可以选择spin重试,也可以选择挂起自己等待唤醒。这里即调用系统调用,让内核操作挂起,为了保证锁原语,调用者将futex word的当前状态 (锁定状态) 作为参数传入内核,内核进行检查如果与futex word的当前一致,则挂起线程。否则返回失败。
为了唤醒等待线程,获取锁的线程在释放锁后,需要调用系统调用,来通知锁释放,内核会唤醒等待者进行竞争锁。
介绍说明futex不一定会进行系统调用,但是调用LockSupport.park()的时候线程确实阻塞了,没有在自旋 (spin重试) ,因为自旋会消耗很多CPU资源,但是阻塞不会消耗,文末会证明LockSupport.park()确实进行了系统调用。

总结:

LockSupport.park -> Unsafe.park -> JNI(JVM) -> Parker::park -> pthread_cond_wait -> futex -> sys_futex(系统调用)
如何唤醒
ReentrantLock中调用了LockSupport.unpark,同样unpark也是一个native实现

Node s = node.next;
...
if (s != null)
    LockSupport.unpark(s.thread);//叫醒后面一个

/**

* 源码在: [http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/687fd7c7986d/src/share/classes/sun/misc/Unsafe.java](http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/687fd7c7986d/src/share/classes/sun/misc/Unsafe.java)
* Unblock the given thread blocked on park, or, if it is
* not blocked, cause the subsequent call to park not to
* block.  Note: this operation is "unsafe" solely because the
* caller must somehow ensure that the thread has not been
* destroyed. Nothing special is usually required to ensure this
* when called from Java (in which there will ordinarily be a live
* reference to the thread) but this is not nearly-automatically
* so when calling from native code.
* @param thread the thread to unpark.

*
 */
public native void unpark(Object thread);
JVM中unpark的实现,调用了Parker::unpark

UNSAFE_ENTRY(void, Unsafe_Unpark(JNIEnv *env, jobject unsafe, jobject jthread))
  UnsafeWrapper("Unsafe_Unpark");
  Parker* p = NULL;
  if (jthread != NULL) {
     ...初始化p
  }
  if (p != NULL) {
      ...省略
    p->unpark();
  }
UNSAFE_END
Parker::unpark的实现

void Parker::unpark() {
    int s, status ;
    // 其实 unpark 这里也可以先通过一个 cas 判断是否 _counter 已经大于0,如果是就可以跳过 mutex 加锁过程,效率更高,稍后你会发现 ParkEvent 就是类似的做法
    status = pthread_mutex_lock(_mutex);
    assert (status == 0, "invariant") ;
    s = _counter;
    _counter = 1;
    if (s < 1) {
        // thread might be parked
        if (_cur_index != -1) {
            // thread is definitely parked
            if (WorkAroundNPTLTimedWaitHang) {
                status = pthread_cond_signal (&_cond[_cur_index]);
                assert (status == 0, "invariant");
                status = pthread_mutex_unlock(_mutex);
                assert (status == 0, "invariant");
            } else {
            // must capture correct index before unlocking
int index =_cur_index;
                status = pthread_mutex_unlock(_mutex);
                assert (status == 0, "invariant");
                status = pthread_cond_signal (&_cond[index]);
                assert (status == 0, "invariant");
            }
        } else {
            pthread_mutex_unlock(_mutex);
            assert (status == 0, "invariant") ;
        }
    } else {
        pthread_mutex_unlock(_mutex);
        assert (status == 0, "invariant") ;
    }
}
调用了pthread_cond_signal,pthread_cond_signal和pthread_cond_wait是一对,都调用了系统调用sys_futex,不过传参不一样而已,看看sys_futex的定义

int futex(int *uaddr, int op, int val, const struct timespec*timeout,
          int *uaddr2, int val3);
第二个参数op即operation有下面可选,参考: [https://linux.die.net/man/2/futex](https://linux.die.net/man/2/futex)

pthread_cond_wait传参为FUTEX_WAIT,而pthread_cond_signal传参为FUTEX_WAKE

FUTEX_WAIT
FUTEX_WAKE
FUTEX_FD (present up to and including Linux 2.6.25)
FUTEX_REQUEUE (since Linux 2.5.70)
FUTEX_CMP_REQUEUE (since Linux 2.6.7)
相应的,文末也会给出证明

总结

LockSupport.unpark -> Unsafe.unpark -> JNI(JVM) -> Parker::unpark -> pthread_cond_signal -> futex -> sys_futex(系统调用)
synchronized
从系统底层啃完了ReentrantLock这块骨头,synchronized就简单多了,无非CAS、队列、futex几大法宝,此处的synchronized我们只分析重量级锁

前置知识
java中每个对象都有个markword,里面包含了锁信息,当为重量级锁的时候markword的一部分会指向一个ObjectMonitor的数据结构,这个ObjectMonitor就是JVM用来实现重量级锁的,图示如下

ObjectMonitor结构如下

ObjectMonitor::ObjectMonitor() {  
  _header       = NULL;  
  _count       = 0;  
  _waiters      = 0,  
  _recursions   = 0;       //线程的重入次数
  _object       = NULL;  
  _owner        = NULL;    //标识拥有该monitor的线程
  _WaitSet      = NULL;    //等待线程组成的双向循环链表,_WaitSet是第一个节点
  _WaitSetLock  = 0 ;  
  _Responsible  = NULL ;  
  _succ         = NULL ;  
  _cxq          = NULL ;    //多线程竞争锁进入时的单向链表
  FreeNext      = NULL ;  
  _EntryList    = NULL ;    //_owner从该双向循环链表中唤醒线程结点,_EntryList是第一个节点
  _SpinFreq     = 0 ;  
  _SpinClock    = 0 ;  
  OwnerIsThread = 0 ;  
}
由于synchronized是JVM来实现的,所以下面代码都是c/c++的

如何上锁
由于我们省略了锁升级的过程,直接看重量级锁的进入,代码在[https://github.com/JetBrains/jdk8u_hotspot/blob/master/src/share/vm/runtime/objectMonitor.cpp](https://github.com/JetBrains/jdk8u_hotspot/blob/master/src/share/vm/runtime/objectMonitor.cpp)

注意看源码的方法,看源码顺着一条线索去看,比如如何上锁,不要在乎细节,因为看了也看不懂(笑),反而导致丧失了继续看下去的耐心,当以后能力提升了再来看这些细节

void ATTR ObjectMonitor::enter(TRAPS) {
  /*
  *省略部分代码
  */
    for (;;) {
      EnterI (THREAD) ;
      /**
      *省略了部分代码
      **/
  }
}
直接来看EnterI

void ATTR ObjectMonitor::EnterI (TRAPS) {
    Thread * Self = THREAD ;
    if (TryLock (Self) > 0) {
        //这下不自旋了,我就默默的TryLock一下
        return ;
    }

    DeferredInitialize () ;
    //此处又有自旋获取锁的操作
    if (TrySpin (Self) > 0) {
        return ;
    }
    /**
    *到此,自旋终于全失败了,要入队挂起了
    **/
    ObjectWaiter node(Self) ; //将Thread封装成ObjectWaiter结点
    Self->_ParkEvent->reset() ;
    node._prev   = (ObjectWaiter *) 0xBAD ; 
    node.TState  = ObjectWaiter::TS_CXQ ; 
    ObjectWaiter * nxt ;
    for (;;) { //循环,保证将node插入队列
        node._next = nxt = _cxq ;//将node插入到_cxq队列的首部
        //CAS修改_cxq指向node
        if (Atomic::cmpxchg_ptr (&node, &_cxq, nxt) == nxt) break ;
        if (TryLock (Self) > 0) {//我再默默的TryLock一下,真的是不想挂起呀！
            return ;
        }
    }
    if ((SyncFlags & 16) == 0 && nxt == NULL && _EntryList == NULL) {
        // Try to assume the role of responsible thread for the monitor.
        // CONSIDER:  ST vs CAS vs { if (Responsible==null) Responsible=Self }
        Atomic::cmpxchg_ptr (Self, &_Responsible, NULL) ;
    }
    TEVENT (Inflated enter - Contention) ;
    int nWakeups = 0 ;
    int RecheckInterval = 1 ;
 
    for (;;) {
        if (TryLock (Self) > 0) break ;//临死之前,我再TryLock下
 
        if ((SyncFlags & 2) && _Responsible == NULL) {
           Atomic::cmpxchg_ptr (Self, &_Responsible, NULL) ;
        }
        if (_Responsible == Self || (SyncFlags & 1)) {
            TEVENT (Inflated enter - park TIMED) ;
            Self->_ParkEvent->park ((jlong) RecheckInterval) ;
            RecheckInterval *= 8 ;
            if (RecheckInterval > 1000) RecheckInterval = 1000 ;
        } else {
            TEVENT (Inflated enter - park UNTIMED) ;
            Self->_ParkEvent->park() ; //终于挂起了
        }
 
        if (TryLock(Self) > 0) break ;
        /**
        *后面代码省略
        **/
}
看TryLock

int ObjectMonitor::TryLock (Thread *Self) {
   for (;;) {
void* own = _owner ;
      if (own != NULL) return 0 ;//如果有线程还拥有着重量级锁,退出
      //CAS操作将_owner修改为当前线程,操作成功return>0
      if (Atomic::cmpxchg_ptr (Self, &_owner, NULL) == NULL) {
         return 1 ;
      }
      //CAS更新失败return<0
      if (true) return -1 ;
   }
}
看Atomic::cmpxchg_ptr,看这名像啥？这不就是CAS么,所以又来到了熟悉的Atomic::cmpxchg,不明白的可以看上面ReentrantLock如何上锁

inline intptr_t Atomic::cmpxchg_ptr(intptr_t exchange_value, volatile intptr_t*dest, intptr_t compare_value) {
  return (intptr_t)cmpxchg((jlong)exchange_value, (volatile jlong*)dest, (jlong)compare_value);
}

inline jint     Atomic::cmpxchg    (jint     exchange_value, volatile jint*     dest, jint     compare_value) {
  int mp = os::is_MP();
  __asm__ volatile (LOCK_IF_MP(%4) "cmpxchgl %1,(%3)"
                    : "=a" (exchange_value)
                    : "r" (exchange_value), "a" (compare_value), "r" (dest), "r" (mp)
                    : "cc", "memory");
  return exchange_value;
}
总结:

所谓上锁就是给ObjectMonitor._owner设置为指向获得锁的线程

如何阻塞
看上面的ObjectMonitor::EnterI方法,获取不到锁的时候调用了ParkEvent::park()方法,看到这是不是想到Parker::park()？那么到底有啥区别,看一下ParkEvent的定义,源码在[https://github.com/JetBrains/jdk8u_hotspot/blob/master/src/share/vm/runtime/park.hpp](https://github.com/JetBrains/jdk8u_hotspot/blob/master/src/share/vm/runtime/park.hpp)

class ParkEvent : public os::PlatformEvent {
  public:
    // MCS-CLH list linkage and Native Mutex/Monitor
    ParkEvent *volatile ListNext ;
ParkEvent* volatile ListPrev ;
    volatile intptr_t OnList ;
    volatile int TState ;
    volatile int Notified ;             // for native monitor construct
    volatile int IsWaiting ;            // Enqueued on WaitSet
  public:
    static ParkEvent *Allocate (Thread* t) ;
    static void Release (ParkEvent * e) ;
} ;
发现没有park方法,因为ParkEvent继承自PlatformEvent,所以去父类找

int os::PlatformEvent::park(jlong millis) {
  ...
  while (_Event < 0) {  // 当令牌不足时,会循环进入等待状态
    status = os::Linux::safe_cond_timedwait(_cond, _mutex, &abst);
  ...
}
继续看os::Linux::safe_cond_timedwait

int os::Linux::safe_cond_timedwait(pthread_cond_t *_cond, pthread_mutex_t*_mutex, const struct timespec *_abstime)
{
   if (is_NPTL()) {
      return pthread_cond_timedwait(_cond,_mutex, _abstime);
   } else {
      // 6292965: LinuxThreads pthread_cond_timedwait() resets FPU control
      // word back to default 64bit precision if condvar is signaled. Java
      // wants 53bit precision.  Save and restore current value.
      int fpu = get_fpu_control_word();
      int status = pthread_cond_timedwait(_cond, _mutex,_abstime);
      set_fpu_control_word(fpu);
      return status;
   }
}
看到没有,调用了pthread_cond_timedwait,pthread_cond_timedwait和pthread_cond_wait的区别一个是有超时设置,一个没有

总结:

ObjectMonitor::enter -> os::PlatformEvent::park -> pthread_cond_timedwait -> futex -> sys_futex(系统调用)
如何唤醒
首先释放重量级锁

void ATTR ObjectMonitor::exit(TRAPS) {
   Thread * Self = THREAD ;
   //省略很多代码
   //省略很多代码
  ...  
      w = _EntryList  ;
      if (w != NULL) {
          ExitEpilog (Self, w) ; //从_EntryList中唤醒线程
          return ;
      }
   }
}
看ExitEpilog

void ObjectMonitor::ExitEpilog (Thread *Self, ObjectWaiter* Wakee) {
   _succ = Knob_SuccEnabled ? Wakee->_thread : NULL ;
   ParkEvent * Trigger = Wakee->_event ;
   ...
   Trigger->unpark() ; //唤醒线程
   ...
}
继续看ParkEvent::unpark(),找不到这个方法,找父类os::PlatformEvent::unpark

void os::PlatformEvent::unpark() {
  ...
  if (AnyWaiters != 0 && WorkAroundNPTLTimedWaitHang) {
    AnyWaiters = 0;
    pthread_cond_signal(_cond);
  }
  ...  
}
pthread_cond_signal这啥？上文已经分析过了

总结

ObjectMonitor::exit -> os::PlatformEvent::unpark -> pthread_cond_signal -> futex -> sys_futex(系统调用)
总结
经过上面的分析,有没有感觉ReentrantLock和synchronized本质上就是一个东西？不过一个是在Java层面实现的,一个是JVM层面实现的,但在具体用法上又有些不同,比如

ReentrantLock用LockSupport.park阻塞和LockSupport.unpark唤醒
synchronized用Object.wait阻塞和Object.notify/notifyAll唤醒
ReentrantLock支持更多自定义条件队列,将不同的线程分组放到不同的队列,这样可以更好的控制线程
synchronized队列是在JVM层面实现的,无法自定义
相同

上锁都用CAS操作
底层都用了相同的系统调用,不能单纯的说synchronized就比ReentrantLock更重,ReentrantLock就比synchronized更轻
不能简单的比较孰优孰劣,视场景而定,它们都有自己的用途。

证明
到了最后的证明环节,这里需要先了解一下在Linux中追踪系统调用的命令strace,测试环境为CentOS 7,没有该命令先安装

yum install -y strace
安装java环境,已安装则忽略

## 环境变量设置

cat > /etc/profile.d/java8.sh <<EOF
export JAVA_HOME=$(dirname $(dirname $(readlink $(readlink $(which javac)))))
export PATH=\$PATH:\$JAVA_HOME/bin
export CLASSPATH=.:\$JAVA_HOME/jre/lib:\$JAVA_HOME/lib:\$JAVA_HOME/lib/tools.jar
EOF
source /etc/profile.d/java8.sh
证明CAS没有系统调用
程序准备
随便找个目录,新建测试程序CASTest.java,并编译javac CASTest.java

程序很简单,就是一直循环CAS,注意不要调用Thread.sleep(),因为该方法会产生系统调用,影响我们观察结果

import sun.misc.Unsafe;

import java.lang.reflect.Field;

/**

* 证明cas操作没有调用系统调用
* strace -ff -o out java CASTest
* 然后观察输出
 */
public class CASTest {

    int i = 0;

    public static CASTest t = new CASTest();

    public static void main(String[] args) throws Exception {
        Unsafe unsafe = getUnsafe();

        Field f = CASTest.class.getDeclaredField("i");
        long offset = unsafe.objectFieldOffset(f);


        //CAS一定会失败
        while (!unsafe.compareAndSwapInt(t, offset, 1, 1)){
            System.out.println(System.currentTimeMillis() + " failed-------------------------");
        }
    }

    /**
  * 获取unsafe
  * @return
  * @throws IllegalAccessException
     */
    public static Unsafe getUnsafe() throws IllegalAccessException {
        //Unsafe unsafe = Unsafe.getUnsafe();

        /**
    * 为什么不直接通过Unsafe unsafe = Unsafe.getUnsafe();拿到unsafe实例 ?
    * 因为直接拿要抛异常,不信你可以试试看,原因在于直接拿Unsafe会检查当前类加载器是不是Bootstrap加载器
    * 如果不是就抛异常,当前类加载器是AppClassLoader,当然不是Bootstrap ClassLoader,
    * 也就是说,Unsafe只允许JVM的某些系统来拿,但是你非要用,也可以自己通过下面的骚操作拿
    * 参考: [https://blog.csdn.net/a7980718/article/details/83279728](https://blog.csdn.net/a7980718/article/details/83279728)
         */
        Field unsafeField = Unsafe.class.getDeclaredFields()[0];
        unsafeField.setAccessible(true);
        Unsafe unsafe = (Unsafe) unsafeField.get(null);
        return unsafe;
    }
}
追踪系统调用
-o 表示输出到当前文件夹的out文件中,后面的java CASTest表示运行该程序

strace -ff -o out java CASTest
此时程序疯狂输出,快速打开另外一个shell窗口,在该目录下查看文件ls -lh

-rw-r--r-- 1 root root 1.6K 2月  28 13:53 CASTest.class
-rw-r--r-- 1 root root 1.6K 2月  28 13:50 CASTest.java
-rw-r--r-- 1 root root  14K 2月  28 13:53 out.5278
-rw-r--r-- 1 root root 3.6M 2月  28 13:53 out.5279
-rw-r--r-- 1 root root  13K 2月  28 13:53 out.5280
...
发现一堆out.*,因为java本来就是多线程程序,JVM一启动就会产生很多线程,每一个out文件都是一个线程的系统调用输出,此处要找到主线程,最大的那个out.5279就是主线程,因为它最大而且一直在变大,看一眼内容,全是write...,这正是我们程序中输出的字符串,看一眼时间戳,和程序里面的是不是一样？这也能佐证这就是主线程的输出！

write(1, "\n", 1)                       = 1
write(1, "1614491601624 failed------------"..., 45) = 45
write(1, "\n", 1)                       = 1
write(1, "1614491601624 failed------------"..., 45) = 45
write(1, "\n", 1)                       = 1
write(1, "1614491601625 failed------------"..., 45) = 45
write(1, "\n", 1)                       = 1
write(1, "1614491601625 failed------------"..., 45) = 45
write(1, "\n", 1)                       = 1
write就是系统调用,但是这不是CAS产生的！而是System.out.println这句话产生的,所以证明了CAS本身并没有任何系统调用！

证明pthread_cond_wait和pthread_cond_signal有系统调用
程序准备
和上面证明CAS一样,先准备程序LockSupportTest.java,代码很简单,就是两个线程不停地去park然后unpark对方。

import java.io.IOException;
import java.util.concurrent.locks.LockSupport;

/**

* 证明park和unpark都调用了系统调用sys_futex
* strace -ff -o out java LockSupportTest
* 然后观察输出
 */
public class LockSupportTest {

    static Thread t1 = null,t2 = null;
    public static void main(String[] args) throws IOException, InterruptedException {

        t1 = new Thread(()->{
            while(true){
                String name = Thread.currentThread().getName();
                System.out.println(System.currentTimeMillis()+ " "+name+" prepare park!");
                //底层调用glibc函数库pthread_cond_wait
                LockSupport.park();
                //底层调用glibc函数库pthread_cond_signal
                LockSupport.unpark(t2);
            }
        },"thread 1");

        t2 = new Thread(()->{
            while(true){
                String name = Thread.currentThread().getName();
                System.out.println(System.currentTimeMillis()+ " "+name+" prepare park!");
                //底层调用glibc函数库pthread_cond_signal
                LockSupport.unpark(t1);
                //底层调用glibc函数库pthread_cond_wait
                LockSupport.park();
            }
        },"thread 2");

        t1.start();
        //此处睡确保线程1先启动
        Thread.sleep(10);
        t2.start();

        //阻塞主线程不退出
        System.in.read();

    }

}
追踪系统调用
strace -ff -o out java LockSupportTest
此时新开shell窗口看文件输出

-rw-r--r-- 1 root root 2.2K 2月  28 16:16 LockSupportTest.class
-rw-r--r-- 1 root root 1.1K 2月  28 16:16 LockSupportTest.java
-rw-r--r-- 1 root root  15K 2月  28 16:16 out.6398
-rw-r--r-- 1 root root 223K 2月  28 16:16 out.6399
-rw-r--r-- 1 root root  15K 2月  28 16:16 out.6400
-rw-r--r-- 1 root root 1.5K 2月  28 16:16 out.6401
-rw-r--r-- 1 root root 1.3K 2月  28 16:16 out.6402
-rw-r--r-- 1 root root 2.3K 2月  28 16:16 out.6403
-rw-r--r-- 1 root root  31K 2月  28 16:16 out.6404
-rw-r--r-- 1 root root  30K 2月  28 16:16 out.6405
-rw-r--r-- 1 root root 1.1K 2月  28 16:16 out.6406
-rw-r--r-- 1 root root  90K 2月  28 16:16 out.6407
-rw-r--r-- 1 root root 5.0M 2月  28 16:16 out.6408
-rw-r--r-- 1 root root 5.4M 2月  28 16:16 out.6409
-rw-r--r-- 1 root root 2.1K 2月  28 16:16 out.6416
这次我们不找主线程,找线程1和线程2,发现out.6409和out.6416在疯狂的变大,说明这是线程1或线程2的输出,打开out.6409看一眼

futex(0x7fdee81c0354, FUTEX_WAIT_BITSET_PRIVATE, 303, {tv_sec=9170827, tv_nsec=944125191}, 0xffffffff) = 0
futex(0x7fdee81c0328, FUTEX_WAKE_PRIVATE, 1) = 0
write(1, "1614501167372 thread 2 prepare p"..., 36) = 36
write(1, "\n", 1)                       = 1
futex(0x7fdee81bef54, FUTEX_WAKE_OP_PRIVATE, 1, 1, 0x7fdee81bef50, FUTEX_OP_SET<<28|0<<12|FUTEX_OP_CMP_GT<<24|0x1) = 1
futex(0x7fdee81c0c04, FUTEX_WAIT_PRIVATE, 541, NULL) = ?
exited with 130
这信息就很丰富了,看输出write(1, "1614501167372 thread 2 prepare p"..., 36) = 36可以知道这是线程2的系统调用,具体来解释一下

打印了输出

write(1, "1614501167372 thread 2 prepare p"..., 36) = 36

打印一个换行符,所以System.out.println其实调用了两次系统调用

write(1, "\n", 1)                       = 1

# 打印完开始叫醒线程1,这里就是系统调用sys_futex

# 打印完开始叫醒线程1,这里就是系统调用sys_futex

# 打印完开始叫醒线程1,这里就是系统调用sys_futex

futex(0x7fdee81bef54, FUTEX_WAKE_OP_PRIVATE, 1, 1, 0x7fdee81bef50, FUTEX_OP_SET<<28|0<<12|FUTEX_OP_CMP_GT<<24|0x1) = 1

# 然后开始自己阻塞住,这里也就是系统调用sys_futex

# 然后开始自己阻塞住,这里也就是系统调用sys_futex

# 然后开始自己阻塞住,这里也就是系统调用sys_futex

futex(0x7fdee81c0c04, FUTEX_WAIT_PRIVATE, 541, NULL) = ?
所以证明了pthread_cond_wait和pthread_cond_signal都调用了系统调用sys_futex

由于个人水平有限,有些细节难免有疏漏或错误,敬请指正。

参考
[https://juejin.cn/post/6844903918653145102#heading-15](https://juejin.cn/post/6844903918653145102#heading-15)
[https://albk.tech/%E8%81%8A%E8%81%8ACPU%E7%9A%84LOCK%E6%8C%87%E4%BB%A4.html](https://albk.tech/%E8%81%8A%E8%81%8ACPU%E7%9A%84LOCK%E6%8C%87%E4%BB%A4.html)
[https://www.beikejiedeliulangmao.top/java/concurrent/thread-park/](https://www.beikejiedeliulangmao.top/java/concurrent/thread-park/)
[https://blog.csdn.net/zwjyyy1203/article/details/106217887](https://blog.csdn.net/zwjyyy1203/article/details/106217887)
[https://zhuanlan.zhihu.com/p/151271009](https://zhuanlan.zhihu.com/p/151271009)

---

[https://zhuanlan.zhihu.com/p/353546643](https://zhuanlan.zhihu.com/p/353546643)
