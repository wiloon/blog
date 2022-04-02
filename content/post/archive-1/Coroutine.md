---
title: 协程, Coroutine
author: "-"
date: 2015-02-04T02:27:10+00:00
url: Coroutine
categories:
  - Coroutine

tags:
  - reprint
---
## 协程, Coroutine

协程的概念很早就提出来了， 但是直到最近几年才某些语言 如 Lua, Golang 中得到广泛应用。


- 没有线程切换的开销, 协程之间的切换不需要涉及任何系统调用或任何阻塞调用                                                                        
- 协程是协作式多任务的
- 线程典型是抢占式多任务的