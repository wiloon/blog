---
title: Go Synchronization, 同步
author: "-"
date: 2011-11-24T10:00:27+00:00
url: go/sync
categories:
  - go
tags:
  - reprint

---
## Go Synchronization, 同步

Go语言在设计上对同步 (Synchronization，数据同步和线程同步）提供大量的支持，比如 goroutine和channel同步原语，库层面有

- sync：提供基本的同步原语 (比如Mutex、RWMutex、Locker）和 工具类 (Once、WaitGroup、Cond、Pool、Map）
- sync/atomic：提供变量的原子操作 (基于硬件指令 compare-and-swap）

