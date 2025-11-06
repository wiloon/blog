---
title: python signal pause
author: "-"
date: 2025-07-30 14:33:39
url: python/signal-pause
categories:
  - Python
tags:
  - reprint
  - remix
---
## python signal.pause() vs time.sleep()

### signal.pause()

系统调用实现, 直接向内核发起系统调用, 让当前线程进入休眠状态, 直到接收到信号为止.
内核将进程状态从 RUNNING → INTERRUPTIBLE_SLEEP
进程从CPU运行队列(CPU Run Queue)中移除


### time.sleep() 是一个非阻塞函数, 它会在指定的时间内暂停当前线程的执行.

用户空间循环实现, 用户空间循环：完全在用户模式下运行
进程状态：持续保持 RUNNING 状态
CPU调度：获得常规CPU时间片
系统调用：重复调用 nanosleep() 或 select()

## CPU运行队列 (Run Queue)

CPU运行队列是一个数据结构（通常是链表或红黑树），包含所有准备执行但正在等待CPU时间的进程/线程。

CPU运行队列是包含所有准备执行的进程/线程的数据结构，这些进程已经准备好使用CPU，只是在等待CPU时间片。
状态：进程处于 READY 状态
CPU占用：这些进程会消耗CPU时间
调度：调度器从这里选择下一个执行的进程
负载计算：运行队列长度影响系统负载平均值

## 等待队列 (Wait Queue)
等待队列包含不能立即执行的进程，它们在等待某些事件发生（如I/O完成、信号到达、锁释放等）。
状态：进程处于 WAITING/BLOCKED 状态
CPU占用：不消耗CPU时间, 0%（进程不被调度）
上下文切换：最少（仅当信号到达时）
事件驱动：等待特定事件唤醒
负载计算：不计入系统负载

## INTERRUPTIBLE_SLEEP

INTERRUPTIBLE_SLEEP 是一种进程状态。在 Linux 操作系统中，进程会经历多种状态，而可中断睡眠（Interruptible Sleep，通常用 'S' 表示）就是其中之一。
进程不会占用 CPU 资源，而是自愿放弃 CPU，以便系统可以更有效地管理资源。

与 INTERRUPTIBLE_SLEEP 相对的是不可中断睡眠（Uninterruptible Sleep，通常用 'D' 表示），处于此状态的进程通常正在执行关键的 I/O 操作，并且不能被信号中断，直到操作完成。


## 进程状态代码

R (Running)：在运行队列中或正在运行
S (Sleeping)：可中断睡眠，在等待队列中
D (Disk Sleep)：不可中断睡眠
Z (Zombie)：僵尸进程

