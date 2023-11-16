---
title: Spinlock(自旋锁), Ticket Spinlock, MCS Spinlock
author: "-"
date: 2013-06-01T07:59:24+00:00
url: "spinlock"
categories:
  - Development
tags:
  - reprint
---
## Spinlock(自旋锁), Ticket Spinlock, MCS Spinlock

为什么要加锁
在 SMP 系统中,如果仅仅是需要串行地增加一个变量的值,那么使用原子操作的函数 (API) 就可以了。但现实中更多的场景并不会那么简单,比如需要将一个结构体A中的数据提取出来,然后格式化、解析,再添加到另一个结构体B中,这整个的过程都要求是「原子的」,也就是完成之前,不允许其他的代码来读/写这两个结构体中的任何一个。

这时,相对轻量级的原子操作API就无法满足这种应用场景的需求了, 我们需要一种更强的同步/互斥机制,那就是软件层面的「锁」的机制。

同步锁的「加锁」和「解锁」是放在一段代码的一前一后,成对出现的,这段代码被称为 Critical Section / Region (临界区) 。但锁保护的并不是这段代码本身,而是其中使用到的**多核/多线程共享的变量**,它「同步」(或者说串行化) 的是对这个变量的访问,通俗的语义就是“我有你就不能有,你有我就不会有”。

Linux中主要有两种同步锁,一种是 spinlock,一种是 mutex. spinlock 和 mutex 都既可以在用户进程中使用,也可以在内核中使用,它们的主要区别是:
前者不会导致睡眠和调度,属于 busy wait 形式的锁,  
后者可能导致睡眠和调度,属于 sleep wait 形式的锁。  

spinlock 是最基础的一种锁,像后面将要介绍的 rwlock(读写锁), seqlock(读写锁)等都是基于spinlock衍生出来的。就算是 mutex,它的实现与spinlock 也是密不可分。因此,本系列文章将首先围绕 spinlock展开介绍。

### 如何加锁

Linux 中 spinlock 机制发展到现在,其实现方式的大致有3种。

#### 第一种实现 - 经典的 CAS

最古老的一种做法是: spinlock 用一个整形变量表示,其初始值为1,表示 available 的状态。当一个CPU (设为CPU A) 获得spinlock后,会将该变量的值设为0,之后其他CPU试图获取这个 spinlock 时,会一直等待,直到 CPU A 释放 spinlock, 并将该变量的值设为1。

那么其他的 CPU 是以何种形式等待的,如果有多个CPU一起等待,形成了竞争又该如何处理？ 这里要用到经典的 CAS 操作 (Compare And Swap) 。

### cas spinlock

### wild spinlock

spinlock 是互斥原语,用于不可睡眠上下文环境访问共享数据的互斥。同一时间只有一个进程 (当然说法不够严谨,也可以是 softirq,hardirq等) 可以获得锁,其他不能获得spinlock的进程原地自旋,直到获取锁

显而易见,这种方式拿锁非常快,尤其是当没有锁竞争的时候,性能非常不错。不过这种方法有一个缺点: 它是不公平的。

何为不公平？
当锁的onwer释放锁后,锁的等待者需要发起竞争,这种机制没有办法保证等待时间最长的CPU能优先获得锁,并且激烈的竞争增加了额外的总线开销。

事实上,刚刚释放锁的那个处理器,由于拥有高速缓存原因,很大概率会优先拿到锁,同样无法保证锁的公平性,所以某些场景下spinlock会带来性能损失、实时性降低。
所以在该机制下,我们很难确保一个CPU从申请拿锁到真实获取锁的延迟时间,极端情况下,拿锁的时间可能是任意长。某些高要求实时性的业务场景是不能容忍的。

举个生活中的例子:
spinlock好比火车上上厕所,很多人同时竞争一个厕所,而恰巧你吃了不干净的东西,很捉急,若没有公平性,后果是灾难性的。

### Ticket Spinlock

历史又更近了一步,我们引入排队机制,以FIFO的顺序处理申请者。谁先申请,谁先获得。保证公平性。

ticket机制
来到主题,为解决上述问题,内核引入ticket spinlock,解决了不公平问题,它是如何做到的？

再举个例子: 去过银行都知道,办业务先取张票,票上面有一个编号,每新来一个客户编号会加1,银行显示屏上会显示当前正服务的客户编号。
当有多位客户等待时,银行按照编号顺序来对其进行服务。由此,实现了公平性,这类似于FIFO算法。

ticket spinlock就是采用了这种机制,spinlock的val变量被分割成2部分:
next是发票机最后发出的编号,而owner是正在被服务的编号。

```c
typedef struc {
    union{
        atomic_t val;
        struct __raw_tickets{
            u16 next;
            u16 owner;
        }
    }
}
```

ticket spinlock伪代码实现:

```c
//加锁
spin_lock(lock *l)
{
    int n = atomic_add(1, l.next);  //先拿票
    
    while(n != atomic_read(l.owner) + 1)  //查看是否轮到自己
        cpu_relax();
}

//放锁
spin_unlock(lock *l)
{
    atomic_add(1, l.owner); //服务完成,叫下一号
}
```

### mcs spinlock

MCS 来自于其发明人名字的首字母:  John Mellor-Crummey和Michael Scott。

MCS Spinlock 是一种基于链表的可扩展、高性能、公平的自旋锁,申请线程只在本地变量上自旋,直接前驱负责通知其结束自旋,从而极大地减少了不必要的处理器缓存同步的次数,降低了总线和内存的开销。

```java
import java.util.concurrent.atomic.AtomicReferenceFieldUpdater;

public class MCSLock {
      
public static class MCSNode {      
    volatile MCSNode next;  
    volatile boolean isBlock = true; // 默认是在等待锁
}

    volatile MCSNode queue; // 指向最后一个申请锁的MCSNode

    private static final AtomicReferenceFieldUpdater UPDATER = AtomicReferenceFieldUpdater
            .newUpdater(MCSLock.class, MCSNode.class, "queue");
    
    public void lock(MCSNode currentThread) {
        MCSNode predecessor = UPDATER.getAndSet(this, currentThread); // step 1
        if (predecessor != null) {
            predecessor.next = currentThread; // step 2
    
            while (currentThread.isBlock) { // step 3
            }
        }else { // 只有一个线程在使用锁,没有前驱来通知它,所以得自己标记自己为非阻塞
               currentThread.isBlock = false;
          }
    }
    
    public void unlock(MCSNode currentThread) {
        if (currentThread.isBlock) { // 锁拥有者进行释放锁才有意义
            return;
        }
    
        if (currentThread.next == null) {// 检查是否有人排在自己后面
            if (UPDATER.compareAndSet(this, currentThread, null)) {// step 4
                // compareAndSet返回true表示确实没有人排在自己后面
                return;
            } else {
                // 突然有人排在自己后面了,可能还不知道是谁,下面是等待后续者
                // 这里之所以要忙等是因为: step 1执行完后,step 2可能还没执行完
                while (currentThread.next == null) { // step 5
                }
            }
        }
    
        currentThread.next.isBlock = false;
        currentThread.next = null;  // for GC
    }
}
```

### qspinlock, queued spinlock

我们来到了 qspinlock 的时代, qspinlock 的出现就是为了解决 tickeet spinlock 的上述问题。我先来思考下造成该问题的原因。根因就是每个 CPU 都 spin 在共享变量 spinlock 上。所以我们只需要保证每个 CPU spin 的变量是不同的就可以避免这种情况了。所以我们需要换一种排队的方式。例如单链表。单链表也可以做到 FIFO, 每次解锁时, 也只需要通知链表头的 CPU 即可。这其实就是 MCS 锁的实现原理。qspinlock 的实现是建立在 MCS锁 的理论基础上。

---

[https://zhuanlan.zhihu.com/p/133445693](https://zhuanlan.zhihu.com/p/133445693)  
[https://zhuanlan.zhihu.com/p/80727111](https://zhuanlan.zhihu.com/p/80727111)  
[https://zhuanlan.zhihu.com/p/89058726](https://zhuanlan.zhihu.com/p/89058726)  
[https://zhuanlan.zhihu.com/p/100546935](https://zhuanlan.zhihu.com/p/100546935)  
