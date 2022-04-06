---
title: 'go 调试, pprof, go tool trace'
author: "-"
date: 2019-11-20T08:00:32+00:00
url: pprof
categories:
  - go
tags:
  - reprint
---
## 'go 调试,  pprof, go tool trace'

做 Profiling 第一步就是怎么获取应用程序的运行情况数据。go 语言提供了 runtime/pprof 和 net/http/pprof 两个库

## http api

```go
// pprof 的init函数会将pprof里的一些handler注册到http.DefaultServeMux上
// 当不使用http.DefaultServeMux来提供http api时，可以查阅其init函数，自己注册handler
import _ "net/http/pprof"

go func() {
    http.ListenAndServe("0.0.0.0:8080", nil)
}()

```

     http://localhost:8080/debug/pprof/

### cpu

go tool pprof http://localhost:8080/debug/pprof/profile?seconds=60

### mem

go tool pprof http://localhost:6060/debug/pprof/heap

### block

go tool pprof http://localhost:8080/debug/pprof/block

### mutex

go tool pprof http://localhost:6060/debug/pprof/mutex

## runtime/pprof

```go
// CPUProfile enables cpu profiling. Note: Default is CPU
defer profile.Start(profile.CPUProfile).Stop()

// GoroutineProfile enables goroutine profiling.
// It returns all Goroutines alive when defer occurs.
defer profile.Start(profile.GoroutineProfile).Stop()

// BlockProfile enables block (contention) profiling.
defer profile.Start(profile.BlockProfile).Stop()

// ThreadcreationProfile enables thread creation profiling.
defer profile.Start(profile.ThreadcreationProfile).Stop()

// MemProfile changes which type of memory profiling to 
// profile the heap.
defer profile.Start(profile.MemProfile).Stop()

// MutexProfile enables mutex profiling.
defer profile.Start(profile.MutexProfile).Stop()

```
## CPU profiling

CPU 性能分析(CPU profiling) 是最常见的性能分析类型。

启动 CPU 分析时，运行时(runtime) 将每隔 10ms 中断一次，记录此时正在运行的协程(goroutines) 的堆栈信息。

程序运行结束后，可以分析记录的数据找到最热代码路径(hottest code paths)。

Compiler hot paths are code execution paths in the compiler in which most of the execution time is spent, and which are potentially executed very often.
– What’s the meaning of “hot codepath”

一个函数在性能分析数据中出现的次数越多，说明执行该函数的代码路径(code path)花费的时间占总运行时间的比重越大。

```go
f, _ := os.OpenFile("/tmp/cpu0.pprof", os.O_CREATE|os.O_RDWR, 0644)
defer f.Close()
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()
```
### 分析数据

```bash
# 网页中查看
go tool pprof -http=:9999 cpu0.pprof
# 命令行中使用交互模式查看
go tool pprof cpu.pprof
```

### 火焰图, FlameGraph

火焰图（Flame Graph）是 Bredan Gregg 创建的一种性能分析图表  
从上往下是方法的调用栈, 横向长度代表 cpu 时长。

## Memory profiling

内存性能分析(Memory profiling) 记录堆内存分配时的堆栈信息，忽略栈内存分配信息。

内存性能分析启用时，默认每1000次采样1次，这个比例是可以调整的。因为内存性能分析是基于采样的，因此基于内存分析数据来判断程序所有的内存使用情况是很困难的。
Memory Profiling：内存分析，在应用程序进行堆分配时记录堆栈跟踪，用于监视当前和历史内存使用情况，以及检查内存泄漏

```go
import     "github.com/pkg/profile"
func main() {
    defer profile.Start(profile.MemProfile, profile.MemProfileRate(1)).Stop()
    concat(100)
}

```

```shell
go tool pprof -http=:9999 /tmp/profile215959616/mem.pprof

```

## block profiling

阻塞性能分析(block profiling) 是 Go 特有的。

阻塞性能分析用来记录一个协程等待一个共享资源花费的时间。在判断程序的并发瓶颈时会很有用。阻塞的场景包括：

在没有缓冲区的信道上发送或接收数据。
从空的信道上接收数据，或发送数据到满的信道上。
尝试获得一个已经被其他协程锁住的排它锁。
一般情况下，当所有的 CPU 和内存瓶颈解决后，才会考虑这一类分析。

## 锁性能分析
锁性能分析(mutex profiling) 与阻塞分析类似，但专注于因为锁竞争导致的等待或延时。

https://colobu.com/2016/12/21/how-to-dump-goroutine-stack-traces/
  
https://golang.org/pkg/net/http/pprof/
  
https://segmentfault.com/a/1190000016412013

```go
import _ "net/http/pprof"

go func() {
    fmt.Println(http.ListenAndServe("localhost:6060", nil))
}()

```

```bash
go tool pprof http://localhost:6060/debug/pprof/heap
```

## "golang  内存分析"

### pprof

    import _ "net/http/pprof"

    go func() {
        http.ListenAndServe("0.0.0.0:8080", nil)
    }()

    http://localhost:8080/debug/pprof/
    默认512kb进行 一次采样

https://lrita.github.io/2017/05/26/golang-memory-pprof/#golang-pprof

### runtime.MemStats
MemStats是一个结构体,里面指标很多,常用的有: 

HeapObjects: 堆中已经分配的对象总数,GC内存回收后HeapObjects取值相应减小。
HeapAlloc:  堆中已经分配给对象的字节数,GC内存回收后HeapAlloc取值相应减小。
TotalAlloc:  堆中已经分配给对象的总的累计字节数,只增不减,GC内存回收后也不减小。
HeapSys: 从操作系统为堆申请到的字节数。
HeapIdle: 堆的闲置区间,包括已经归还给操作系统的物理字节数 (HeapReleased) 
HeapReleased: 已经归还给操作系统的物理字节数,是HeapIdle的子集。

>https://blog.haohtml.com/archives/21685
>https://blog.csdn.net/pengpengzhou/article/details/106901368
>https://geektutu.com/post/hpg-pprof.html
>https://github.com/google/pprof/tree/master/doc

