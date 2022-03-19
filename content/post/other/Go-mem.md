---
title: Go mem, Go 内存
author: "-"
date: 2011-12-25T08:41:01+00:00
url: go/mem
categories:
  - Go
tags:
  - reprint
---
## Go mem, Go 内存
用户程序（Mutator）会通过内存分配器（Allocator）在堆上申请内存，而垃圾收集器（Collector）负责回收堆上的内存空间，内存分配器和垃圾收集器共同管理着程序中的堆内存空间。


>https://draveness.me/golang/docs/part3-runtime/ch07-memory/golang-garbage-collector/
