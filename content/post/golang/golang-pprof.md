---
title: "golang  内存分析"
author: "-"
date: "2020-09-30 13:44:20" 
url: "go-mem"
categories:
  - inbox
tags:
  - inbox
---

### pprof

    import _ "net/http/pprof"

    go func() {
        http.ListenAndServe("0.0.0.0:8080", nil)
    }()

    http://localhost:8080/debug/pprof/
    默认512kb进行 一次采样

https://lrita.github.io/2017/05/26/golang-memory-pprof/#golang-pprof

### runtime.MemStats
MemStats是一个结构体，里面指标很多，常用的有: 

HeapObjects: 堆中已经分配的对象总数，GC内存回收后HeapObjects取值相应减小。
HeapAlloc:  堆中已经分配给对象的字节数，GC内存回收后HeapAlloc取值相应减小。
TotalAlloc:  堆中已经分配给对象的总的累计字节数，只增不减，GC内存回收后也不减小。
HeapSys: 从操作系统为堆申请到的字节数。
HeapIdle: 堆的闲置区间，包括已经归还给操作系统的物理字节数（HeapReleased）
HeapReleased: 已经归还给操作系统的物理字节数，是HeapIdle的子集。

>https://blog.haohtml.com/archives/21685
>https://blog.csdn.net/pengpengzhou/article/details/106901368
