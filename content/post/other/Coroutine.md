---
title: 协程, Coroutine
author: "-"
date: 2015-02-04T02:27:10+00:00
url: Coroutine
categories:
  - OS
tags:
  - reprint
  - Coroutine
---
## 协程, Coroutine

协程别名: 微线程，纤程。英文:Coroutine, Green threads, fibers

传统编程语言中子程序或者叫函数是层级调用的,

- 没有线程切换的开销, 协程之间的切换不需要涉及任何系统调用或任何阻塞调用
- 协程是协作式多任务的
- 线程典型是抢占式多任务的
