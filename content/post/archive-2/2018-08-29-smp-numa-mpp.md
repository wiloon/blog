---
title: smp, NUMA, MPP
author: w1100n
type: post
date: 2018-08-29T08:54:06+00:00
url: /?p=12612
categories:
  - Uncategorized

---
https://www.jianshu.com/p/81233f3c2c14

系统的性能很大程度上依赖于cpu 硬件架构的支持。这里记录一下cpu 常见的三大架构的区别

### SMP
SMP （Symmetric Multiprocessing） , 对称多处理器. 顾名思义, 在SMP中所有的处理器都是对等的, 它们通过总线连接共享同一块物理内存，这也就导致了系统中所有资源(CPU、内存、I/O等)都是共享的，当我们打开服务器的背板盖，如果发现有多个cpu的槽位，但是却连接到同一个内存插槽的位置，那一般就是smp架构的服务器，日常中常见的pc啊，笔记本啊，手机还有一些老的服务器都是这个架构，其架构简单，但是拓展性能非常差，从linux 上也能看到:

ls /sys/devices/system/node/# 如果只看到一个node0 那就是smp架构
  
可以看到只有仅仅一个node，经过大神们的测试发现，2至4个CPU比较适合smp架构。

### NUMA
NUMA （ Non-Uniform Memory Access），非均匀访问存储模型，这种模型的是为了解决smp扩容性很差而提出的技术方案，如果说smp 相当于多个cpu 连接一个内存池导致请求经常发生冲突的话，numa 就是将cpu的资源分开，以node 为单位进行切割，每个node 里有着独有的core ，memory 等资源，这也就导致了cpu在性能使用上的提升，但是同样存在问题就是2个node 之间的资源交互非常慢，当cpu增多的情况下，性能提升的幅度并不是很高。所以可以看到很多明明有很多core的服务器却只有2个node区。

### MPP
MPP (Massive Parallel Processing) ，这个其实可以理解为刀片服务器，每个刀扇里的都是一台独立的smp架构服务器，且每个刀扇之间均有高性能的网络设备进行交互，保证了smp服务器之间的数据传输性能。相比numa 来说更适合大规模的计算，唯一不足的是，当其中的smp 节点增多的情况下，与之对应的计算管理系统也需要相对应的提高。

作者: 钟大發
  
链接: https://www.jianshu.com/p/81233f3c2c14
  
來源: 简书
  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。