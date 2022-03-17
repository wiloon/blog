---
title: Go gc
author: "-"
date: 2019-06-11T05:17:27+00:00
url: go/gc
categories:
  - Go

tags:
  - reprint
---
## Go gc

## gctrace
```bash
GODEBUG='gctrace=1' go run main.go

```

```bash
gc 15 @941.135s 0%: 0.058+91+0.002 ms clock, 0.058+0.35/26/61+0.002 ms cpu, 75->75->38 MB, 77 MB goal, 1 P
```

gc # @#s #%: #+#+# ms clock, #+#/#/#+# ms cpu, #->#-># MB, # MB goal, # P
where the fields are as follows:
    gc #        the GC number, incremented at each GC
    @#s         time in seconds since program start
    #%          percentage of time spent in GC since program start
    #+...+#     wall-clock/CPU times for the phases of the GC
    #->#-># MB  heap size at GC start, at GC end, and live heap
    # MB goal   goal heap size
    # P         number of processors used
The phases are stop-the-world (STW) sweep termination, concurrent
mark and scan, and STW mark termination. The CPU times
for mark/scan are broken down in to assist time (GC performed in
line with allocation), background GC time, and idle GC time.
If the line ends with "(forced)", this GC was forced by a
runtime.GC() call and all phases are STW.

- gc 15: 第15次gc
- @941.135s: 这次gc的 markTermination 阶段完成后，距离runtime启动到现在的时间。
- 0%：当目前为止, gc的标记工作（包括两次mark阶段的 STW 和并发标记）所用的CPU时间占总CPU的百分比。
- 0.058+91+0.002 ms clock: 按顺序分成三部分, 0.058 表示 mark 阶段的 STW 时间（单P的); 91 表示并发标记用的时间（所有P的）；0.002 表示markTermination 阶段的 STW 时间（单P的）。
- 0.058+0.35/26/61+0.002 ms cpu: 按顺序分成三部分，0.058 表示整个进程在 mark 阶段 STW 停顿时间 (0.013 * 8)；+0.35/26/61 有三块信息，0.35 是 mutator assists 占用的时间，26 是 dedicated mark workers + fractional mark worker 占用的时间，61 是 idle mark workers 占用的时间。 这三块时间加起来会接近 2.9*8 (P的个数)；0.002 ms 表示整个进程在 markTermination 阶段 STW 停顿时间(0.050 * 8)。
- 75->75->38 MB: 按顺序分成三部分，75 表示开始 mark 阶段前的 heap_live 大小(GC开始时内存使用量); 75 表示开始 markTermination 阶段前的 heap_live 大小；38 表示被标记对象的大小。
- 77 MB goal: 表示下一次触发 GC 的内存占用阀值是 77 MB，等于8MB * 2，向上取整。
- 1 P: 本次gc共有多少个P(线程)。

## GODEBUG

```go
// 这些flag可以通过在go run 命令中设置GODEBUG变量来使用。但每个flag的不同取值对应的含义并没常量标识，都是硬编码
var debug struct {
    allocfreetrace   int32
    cgocheck         int32
    efence           int32
    gccheckmark      int32
    gcpacertrace     int32
    gcshrinkstackoff int32
    gcrescanstacks   int32
    gcstoptheworld   int32
    gctrace          int32
    invalidptr       int32
    sbrk             int32
    scavenge         int32
    scheddetail      int32
    schedtrace       int32
}

```
## GOGC
  
GOGC是Go运行时支持的最老的环境变量之一。它甚至比GOROOT还老
  
GOGC 用于控制GC的处发频率， 其值默认为100
  
意为直到自上次垃圾回收后heap size已经增长了100%时GC才触发运行。即是GOGC=100意味着live heap size 每增长一倍，GC触发运行一次。
  
如设定GOGC=200, 则live heap size 自上次垃圾回收后，增长2倍时，GC触发运行， 总之，其值越大则GC触发运行频率越低， 反之则越高，
  
如果GOGC=off 则关闭GC.
  
虽然go 1.5引入了低延迟的GC, 但是GOGC对GC运行频率的影响不变， 仍然是其值大于100,则越大GC运行频率越高，
  
反之则越低。

每次GC必须完成如下循环，旧的完成了再开启新的。 sweep termination, mark, mark termination, and sweep

https://studygolang.com/articles/6346
  
https://ieevee.com/assets/2018-01-28-gogc.html
  
http://legendtkl.com/2017/04/28/golang-gc/

### 并发垃圾收集
Go 语言在 v1.5 中引入了并发的垃圾收集器，该垃圾收集器使用了三色抽象和写屏障技术保证垃圾收集器执行的正确性
Go 语言的并发垃圾收集器会在扫描对象之前暂停程序做一些标记对象的准备工作,其中包括启动后台标记的垃圾收集器以及开启写屏障

v1.6 引入了去中心化的垃圾收集协调机制22，将垃圾收集器变成一个显式的状态机，任意的 Goroutine 都可以调用方法触发状态的迁移

STW 的垃圾收集器虽然需要暂停程序，但是它能够有效地控制堆内存的大小，Go 语言运行时的默认配置会在堆内存达到上一次垃圾收集的 2 倍时，触发新一轮的垃圾收集，这个行为可以通过环境变量 GOGC 调整，在默认情况下它的值为 100，即增长 100% 的堆内存才会触发 GC。

混合写屏障 #
在 Go 语言 v1.7 版本之前，运行时会使用 Dijkstra 插入写屏障保证强三色不变性，但是运行时并没有在所有的垃圾收集根对象上开启插入写屏障。因为应用程序可能包含成百上千的 Goroutine，而垃圾收集的根对象一般包括全局变量和栈对象，如果运行时需要在几百个 Goroutine 的栈上都开启写屏障，会带来巨大的额外开销，所以 Go 团队在实现上选择了在标记阶段完成时暂停程序、将所有栈对象标记为灰色并重新扫描，在活跃 Goroutine 非常多的程序中，重新扫描的过程需要占用 10 ~ 100ms 的时间。

>https://draveness.me/golang/docs/part3-runtime/ch07-memory/golang-garbage-collector/#fn:8


>https://github.com/golang/proposal

