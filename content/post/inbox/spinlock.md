---
title: "spinlock"
author: "-"
date: "2021-07-10 11:58:17"
url: "spinlock"
categories:
  - inbox
tags:
  - inbox
---

### wild spinlock
spinlock是互斥原语，用于不可睡眠上下文环境访问共享数据的互斥。同一时间只有一个进程（当然说法不够严谨，也可以是softirq，hardirq等）可以获得锁，其他不能获得spinlock的进程原地自旋，直到获取锁
ticket spinlock
历史又更近了一步，我们引入排队机制，以FIFO的顺序处理申请者。谁先申请，谁先获得。保证公平性。

qspinlock
我们来到了qspinlock的时代，qspinlock的出现就是为了解决tickeet spinlock的上述问题。我先来思考下造成该问题的原因。根因就是每个CPU都spin在共享变量spinlock上。所以我们只需要保证每个CPU spin的变量是不同的就可以避免这种情况了。所以我们需要换一种排队的方式。例如单链表。单链表也可以做到FIFO，每次解锁时，也只需要通知链表头的CPU即可。这其实就是MCS锁的实现原理。qspinlock的实现是建立在MCS锁的理论基础上。我们先探究下MCS锁是如何实现。



https://zhuanlan.zhihu.com/p/133445693

