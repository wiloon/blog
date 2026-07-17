---
title: jstack
author: "-"
date: 2015-11-11T11:20:45+00:00
lastmod: 2026-07-16T03:44:07+08:00
url: jstack
categories:
  - Java
tags:
  - jvm
  - jstack
  - remix
  - AI-assisted
---

## 背景

jstack 用来查看某个 Java 进程内的线程堆栈信息，语法：

```bash
jstack [option] PID
jstack [option] executable core
jstack [option] [server-id@]remote-hostname-or-ip
```

常用参数：

| 参数 | 说明 |
| ---- | ---- |
| `-l` | long listing，额外打印锁信息；发生死锁时可用 `jstack -l pid` 观察锁持有情况 |
| `-m` | mixed mode，同时输出 Java 堆栈和 C/C++（Native 方法）堆栈 |
| `-F` | 当 `jstack [-l] pid` 无响应时强制 dump |

## 现代 JDK（含 JDK 26）里还有替代吗

有，而且是官方推荐的替代：**`jcmd <pid> Thread.print`**。

`jstack`、`jmap`、`jinfo` 这几个独立小工具早已被 Oracle 标记为 experimental / unsupported，官方故障排查文档现在统一推荐通过 `jcmd` 这个诊断入口来做线程栈、堆 dump、JFR 等操作：

```bash
jcmd <pid> Thread.print      # equivalent to: jstack <pid>
jcmd <pid> Thread.print -l   # equivalent to: jstack -l <pid>, with lock info
```

`jstack` 目前仍随 JDK 26 一起提供，还能正常使用，只是不建议在新脚本 / 新流程里继续依赖它。参数与用法详见 [jcmd](../language/java/jcmd.md)；更完整的生产诊断工具对比（Arthas、async-profiler、JFR 等）见 [生产环境诊断工具选型](../language/java/java-production-diagnostics-tooling.md)。

## 实战：定位 CPU 占用最高的线程

用到的命令：`ps`、`top`、`printf`、`jstack`、`grep`。

第一步，找到 Java 进程 PID（示例应用名为 `mrf-center`）：

```bash
ps -ef | grep mrf-center | grep -v grep
# root 21711 1 1 14:47 pts/3 00:02:10 java -jar mrf-center.jar
```

得到进程 PID 为 21711。第二步，找出该进程内最耗费 CPU 的线程，可以用 `ps -Lfp pid`、`ps -mp pid -o THREAD,tid,time` 或 `top -Hp pid`，这里用第三种：

```bash
top -Hp 21711
```

TIME 列就是各个 Java 线程耗费的 CPU 时间。假设 CPU 时间最长的线程 ID 是 21742，把它转成十六进制（jstack 输出里线程 ID 是十六进制）：

```bash
printf "%x\n" 21742
# 54ee
```

第三步，用 jstack 输出进程 21711 的堆栈信息，再按线程 ID 的十六进制值过滤：

```bash
jstack 21711 | grep 54ee
```

```text
"PollIntervalRetrySchedulerThread" prio=10 tid=0x00007f950043e000 nid=0x54ee in Object.wait() [0x00007f94c6eda000]
```

可以看到 CPU 消耗在 `PollIntervalRetrySchedulerThread` 这个类的 `Object.wait()` 上，对应到业务代码里是一段轮询任务的空闲等待逻辑：

```java
// Idle wait
getLog().info("Thread [" + getName() + "] is idle waiting...");
schedulerThreadState = PollTaskSchedulerThreadState.IdleWaiting;
long now = System.currentTimeMillis();
long waitTime = now + getIdleWaitTime();
long timeUntilContinue = waitTime - now;
synchronized (sigLock) {
    try {
        if (!halted.get()) {
            sigLock.wait(timeUntilContinue);
        }
    } catch (InterruptedException ignore) {
    }
}
```

`sigLock.wait(timeUntilContinue)` 就对应了前面 dump 里的 `Object.wait()`。

## 注意事项

- 不同 JVM 实现、不同版本的线程 dump 格式都不一样；下文示例以早期 HotSpot（5.0/6）为例，字段含义在现代 HotSpot 上基本沿用。
- 一次 dump 往往不足以确认问题，建议连续产生三次 dump，如果每次都指向同一个问题，才能确认问题的典型性。

## JVM 内置线程

线程 dump 里除了业务线程，还有一些 JVM 内部的后台线程，比如负责垃圾回收、低内存检测等任务，这些线程在 JVM 初始化时就已存在：

```text
"Low Memory Detector" daemon prio=10 tid=0x081465f8 nid=0x7 runnable [0x00000000..0x00000000]
"CompilerThread0" daemon prio=10 tid=0x08143c58 nid=0x6 waiting on condition [0x00000000..0xfb5fd798]
"Signal Dispatcher" daemon prio=10 tid=0x08142f08 nid=0x5 waiting on condition [0x00000000..0x00000000]
"Finalizer" daemon prio=10 tid=0x08137ca0 nid=0x4 in Object.wait() [0xfbeed000..0xfbeeddb8]
    at java.lang.Object.wait(Native Method)
    - waiting on <0xef600848> (a java.lang.ref.ReferenceQueue$Lock)
    at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:116)
    - locked <0xef600848> (a java.lang.ref.ReferenceQueue$Lock)
    at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:132)
    at java.lang.ref.Finalizer$FinalizerThread.run(Finalizer.java:159)
"Reference Handler" daemon prio=10 tid=0x081370f0 nid=0x3 in Object.wait() [0xfbf4a000..0xfbf4aa38]
    at java.lang.Object.wait(Native Method)
    - waiting on <0xef600758> (a java.lang.ref.Reference$Lock)
    at java.lang.Object.wait(Object.java:474)
    at java.lang.ref.Reference$ReferenceHandler.run(Reference.java:116)
    - locked <0xef600758> (a java.lang.ref.Reference$Lock)
"VM Thread" prio=10 tid=0x08134878 nid=0x2 runnable
"VM Periodic Task Thread" prio=10 tid=0x08147768 nid=0x8 waiting on condition
```

这几个内置线程的作用见 [DestroyJavaVM 与 JVM 内置线程](../language/java/destroy-java-vm.md)。

更多时候需要观察的是用户级别的线程：

```text
"Thread-1" prio=10 tid=0x08223860 nid=0xa waiting on condition [0xef47a000..0xef47ac38]
    at java.lang.Thread.sleep(Native Method)
    at testthread.MySleepingThread.method2(MySleepingThread.java:53)
    - locked <0xef63d600> (a testthread.MySleepingThread)
    at testthread.MySleepingThread.run(MySleepingThread.java:35)
    at java.lang.Thread.run(Thread.java:595)
```

从这段 dump 能看到三类信息：线程状态（`waiting on condition`）、线程的调用栈、线程当前锁住的资源（`<0xef63d600>`）。

## 线程状态解读

线程状态是 dump 里的一个重要指标，显示在每个线程 stacktrace 首行结尾处。

### Runnable

表示线程具备运行条件，正在运行队列中等待操作系统调度，或者正在运行。

### Wait on condition

表示线程在等待某个条件发生，具体原因要结合 stacktrace 分析。最常见的情况是等待网络读写：数据没准备好时线程阻塞，数据就绪后重新被激活。在 Java 引入 NIO 之前，每个网络连接都对应一个线程处理读写，即使没有数据可读写线程也会阻塞，容易造成资源浪费和调度压力；NIO 引入之后这个问题得到缓解。

如果发现大量线程都处于 `Wait on condition` 且从 stack 看是在等待网络读写，可能是网络瓶颈的征兆，需要结合 `netstat`、CPU 利用率（尤其是系统态占比）等工具综合判断。另一种常见情况是线程在 `sleep`，等到睡眠时间到了才会被唤醒。

### Waiting for monitor entry 与 in Object.wait()

Java 多线程之间的同步依赖 **Monitor**：每个对象都有且仅有一个 monitor，某一时刻只能被一个线程持有。持有 monitor 的线程是 "Active Thread"，其它线程分别在 "Entry Set" 和 "Wait Set" 两个队列里等待：

- 在 "Entry Set" 中等待的线程，状态显示为 `waiting for monitor entry`
- 在 "Wait Set" 中等待的线程，状态显示为 `in Object.wait()`

线程申请进入被 `synchronized` 保护的临界区时，如果该 monitor 未被占用、Entry Set 也没有其他等待线程，本线程直接成为 owner 并执行临界区代码，状态为 `Runnable`；如果 monitor 已被占用，本线程进入 Entry Set 排队，状态为 `waiting for monitor entry`：

```text
"Thread-0" prio=10 tid=0x08222eb0 nid=0x9 waiting for monitor entry [0xf927b000..0xf927bdb8]
    at testthread.WaitThread.run(WaitThread.java:39)
    - waiting to lock <0xef63bf08> (a java.lang.Object)
    - locked <0xef63beb8> (a java.util.ArrayList)
    at java.lang.Thread.run(Thread.java:595)
```

临界区的作用是保证内部代码执行的原子性和完整性，但同一时间只允许一个线程串行通过。如果 `synchronized` 使用不当或过度使用，会导致大量线程堆积在临界区入口，系统性能大幅下降；线程 dump 中若发现这种情况，应该审查源码。

线程获得 monitor、进入临界区后，如果发现继续运行的条件不满足，会调用该对象的 `wait()` 方法主动放弃 monitor，进入 Wait Set 排队，直到有其他线程调用 `notify()` / `notifyAll()` 才有机会重新竞争 monitor。这种线程在 dump 中表现为 `in Object.wait()`：

```text
"Thread-1" prio=10 tid=0x08223250 nid=0xa in Object.wait() [0xef47a000..0xef47aa38]
    at java.lang.Object.wait(Native Method)
    - waiting on <0xef63beb8> (a java.util.ArrayList)
    at java.lang.Object.wait(Object.java:474)
    at testthread.MyWaitThread.run(MyWaitThread.java:40)
    - locked <0xef63beb8> (a java.util.ArrayList)
    at java.lang.Thread.run(Thread.java:595)
```

注意这段 dump 里先 `locked` 又 `waiting on` 同一个对象，对应的代码是：

```java
synchronized (obj) {
    // ...
    obj.wait();
    // ...
}
```

线程先用 `synchronized` 获得对象的 monitor（对应 `locked`），执行到 `obj.wait()` 时放弃 monitor 所有权，进入 Wait Set（对应 `waiting on`）。多个结构相似的线程同时出现类似 dump 也是正常现象，比如多个消费者线程从同一个队列读数据：队列为空时它们都在这个队列对象上等待，队列来了数据后被 notify，但只有一个线程能抢到 lock 继续执行，其余线程继续等待。

### JDK 5.0 的 Lock

`synchronized` / monitor 机制使用不当容易造成性能问题。JDK 5.0 引入了 `java.util.concurrent.locks.Lock`，让开发者能更灵活地开发高性能并发程序，可以替代 `synchronized` / monitor。但 `Lock` 只是一个普通类，JVM 无法感知 `Lock` 对象的占用情况，因此线程 dump 中不会包含 `Lock` 相关信息——排查死锁等问题时不如 `synchronized` 方式直观。

## 案例分析

### 死锁

多线程程序里同步机制使用不当，可能造成死锁，表现为程序停顿或不再响应请求：

```text
"Thread-1" prio=5 tid=0x00acc490 nid=0xe50 waiting for monitor entry [0x02d3f000..0x02d3fd68]
    at deadlockthreads.TestThread.run(TestThread.java:31)
    - waiting to lock <0x22c19f18> (a java.lang.Object)
    - locked <0x22c19f20> (a java.lang.Object)
"Thread-0" prio=5 tid=0x00accdb0 nid=0xdec waiting for monitor entry [0x02cff000..0x02cff9e8]
    at deadlockthreads.TestThread.run(TestThread.java:31)
    - waiting to lock <0x22c19f20> (a java.lang.Object)
    - locked <0x22c19f18> (a java.lang.Object)
```

JDK 5 加强了死锁检测，线程 dump 会直接报告 Java 级别的死锁：

```text
Found one Java-level deadlock:
"Thread-1":
  waiting to lock monitor 0x0003f334 (object 0x22c19f18, a java.lang.Object),
  which is held by "Thread-0"
"Thread-0":
  waiting to lock monitor 0x0003f314 (object 0x22c19f20, a java.lang.Object),
  which is held by "Thread-1"
```

### 热锁

热锁也是导致系统性能瓶颈的常见原因，表现为多个线程对临界区或锁激烈竞争：

- 频繁的线程上下文切换：线程因等待资源阻塞时被操作系统切出，获得资源后再切入
- 大量系统调用：上下文切换和热锁竞争都会带来额外的系统调用
- 大部分 CPU 时间花在系统态：应用虽然很忙，但用户态 CPU 占比很低，业务代码得不到充分的 CPU 资源
- CPU 数目越多，性能反而可能越差：并发线程越多，上下文切换和系统态开销越大

排查思路是结合操作系统资源监控工具与线程 dump，找出线程都阻塞在哪些方法上。例如曾经遇到大多数线程都处于 `waiting for monitor entry` 或 `in Object.wait()`，且都阻塞在压缩 / 解压缩方法上；换用第三方压缩库替代 JDK 自带实现后，系统性能提升了几倍。

## 参考

- [jstack - Stack Trace (Java SE 8)](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/jstack.html)
- [jcmd](../language/java/jcmd.md)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-16 | categories 由 `inbox` 改为 `Java`；重新分节整理正文，修复代码块缺少语言标识、乱码断行等格式问题；新增「现代 JDK（含 JDK 26）里还有替代吗」一节，说明官方推荐用 `jcmd Thread.print` 替代；补充与 jcmd.md、destroy-java-vm.md、java-production-diagnostics-tooling.md 的站内互链；标签由 `reprint` 改为 `remix`、`AI-assisted` | 内容与站内其他 Java 诊断工具文章一致按规范整理，并回答作者关于现代 JDK 是否有 jstack 替代的提问 |
