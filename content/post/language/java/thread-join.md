---
title: "Java Thread.join() 原理与用法"
author: "-"
date: 2015-01-13T05:52:17+00:00
lastmod: 2026-07-16T04:02:34+08:00
url: thread-join
categories:
  - language
tags:
  - java
  - thread
  - remix
  - AI-assisted
---

## join() 是做什么用的

`join()` 定义在 `Thread` 类里，作用是让**当前线程等待另一个线程结束**。谁调用了 `t.join()`，谁就会阻塞，直到线程 `t` 执行完毕才继续往下走。

容易搞混的一点是"谁等谁"：`t.join()` 阻塞的不是 `t` 自己，而是执行这行代码所在的那个线程。

## 为什么需要 join()

典型场景：主线程启动一个子线程去做耗时运算，主线程处理完自己手头的事情后，需要用到子线程算出来的结果——这时就要用 `join()`，等子线程真正跑完再继续，否则可能拿到还没算完的结果。

## 用例子理解

写三个类来演示：`CustomThread1` 循环打印 5 次、每次间隔 1 秒；`CustomThread` 在 `run()` 里调用了 `t1.join()`，要等 `t1` 跑完才继续；`JoinTestDemo` 是入口。

```java
class CustomThread1 extends Thread {
    public CustomThread1() {
        super("[CustomThread1] Thread");
    }

    @Override
    public void run() {
        String threadName = Thread.currentThread().getName();
        System.out.println(threadName + " start.");
        try {
            for (int i = 0; i < 5; i++) {
                System.out.println(threadName + " loop at " + i);
                Thread.sleep(1000);
            }
            System.out.println(threadName + " end.");
        } catch (InterruptedException e) {
            System.out.println("Exception from " + threadName + ".run");
        }
    }
}

class CustomThread extends Thread {
    private final CustomThread1 t1;

    public CustomThread(CustomThread1 t1) {
        super("[CustomThread] Thread");
        this.t1 = t1;
    }

    @Override
    public void run() {
        String threadName = Thread.currentThread().getName();
        System.out.println(threadName + " start.");
        try {
            t1.join();
            System.out.println(threadName + " end.");
        } catch (InterruptedException e) {
            System.out.println("Exception from " + threadName + ".run");
        }
    }
}

public class JoinTestDemo {
    public static void main(String[] args) throws InterruptedException {
        String threadName = Thread.currentThread().getName();
        System.out.println(threadName + " start.");

        CustomThread1 t1 = new CustomThread1();
        CustomThread t = new CustomThread(t1);

        t1.start();
        Thread.sleep(2000);
        t.start();
        t.join(); // main thread waits for t to finish
        System.out.println(threadName + " end!");
    }
}
```

main 线程先启动 `t1`，睡 2 秒后再启动 `t`，最后调用 `t.join()` 等 `t` 结束。执行顺序大致是：

| 顺序 | 发生了什么 |
| ---- | ---- |
| 1 | main 启动，随后 `sleep(2000)` |
| 2 | t1 启动，开始循环打印 loop 0、1 |
| 3 | 2 秒后 main 唤醒，启动 t |
| 4 | t 调用 `t1.join()`，阻塞等待 t1 |
| 5 | t1 继续打印 loop 2、3、4，然后结束 |
| 6 | t1 结束，t 从 `join()` 处唤醒，打印 end 并结束 |
| 7 | t 结束，main 从 `t.join()` 处唤醒，打印 end! |

如果把最后的 `t.join()` 去掉，main 线程不会再等 `t` 结束——它在 `Thread.sleep(2000)` 之后就直接打印 `end!` 并退出，`t` 是否跑完跟 main 无关。这说明 `join()` 只影响调用它的那个线程，不会影响其他线程。

## 从源码看 join()

无参的 `join()` 调用的是 `join(0)`：

```java
public final void join() throws InterruptedException {
    join(0);
}
```

`join(long millis)` 的核心逻辑是一个基于 `wait()` 的循环，只要目标线程还活着（`isAlive()`），调用者就一直等：

```java
public final synchronized void join(long millis) throws InterruptedException {
    long base = System.currentTimeMillis();
    long now = 0;

    if (millis < 0) {
        throw new IllegalArgumentException("timeout value is negative");
    }

    if (millis == 0) {
        while (isAlive()) {
            wait(0); // wait indefinitely until this thread dies
        }
    } else {
        while (isAlive()) {
            long delay = millis - now;
            if (delay <= 0) {
                break;
            }
            wait(delay);
            now = System.currentTimeMillis() - base;
        }
    }
}
```

`millis == 0` 表示一直等到线程死亡为止；线程结束时 JVM 会唤醒所有在等它的线程，`join()` 本质上就是"在目标线程对象上 wait，直到它死亡为止"。

有一点容易被忽略：如果线程对象已经创建但还没调用过 `start()`，此时调用它的 `join()` 不会阻塞，会直接往下执行——因为这时 `isAlive()` 返回 `false`。

## 小结

`join()` 让调用者线程等待目标线程结束，本质上是在目标线程对象上做 `wait()`，等目标线程死亡时被唤醒通知。它只影响调用它的那个线程，常用于"主线程需要等子线程算完结果再继续"的场景。

原文参考：<http://blog.csdn.net/bzwm/article/details/3881392>

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-16 | 重写全文结构与措辞，修正代码块（原文代码块围栏未正确闭合、逐行断行严重）；文件移动到 `content/post/language/java/thread-join.md`；categories 由 `Inbox` 改为 `language`；标题改为 "Java Thread.join() 原理与用法"；标签由 `reprint` 改为 `java`、`thread`、`remix`、`AI-assisted` | 原文排版错乱（代码块缺少正确闭合围栏，正文逐行断行），分类与标签不准确，且原本归在 development 目录，与站内 Java 内容惯例（language/java）不符 |
