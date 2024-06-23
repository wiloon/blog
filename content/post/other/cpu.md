---
title: CPU
author: "-"
date: 2015-06-30T02:32:13+00:00
url: cpu
categories:
  - CS
tags:
  - reprint
---
## CPU

CPU执行过的指令都遵循以下的流程: CPU首先依据指令指针取得(Fetch)将要执行的指令在代码段的地址，接下来解码(Decode)地址上的指令。解码之后，会进入真正的执行(Execute)阶段，之后会是"写回"(Write Back)阶段，将处理的最终结果写回内存或寄存器中，并更新指令指针寄存器指向下一条指令。
  
1982年，处理器中引入了指令缓存。
  
1989年，i486处理器引入了五级流水线。
  
1995年Intel发布Pentium Pro处理器时，加入了乱序执行核心(Out-of-order core, OOO core)。
  
乱序执行也并不一定100%达到顺序执行代码的效果。有些时候确实需要引入内存屏障来确保执行的先后顺序。
  
[http://www.infoq.com/cn/articles/x86-high-performance-programming-pipeline?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global](http://www.infoq.com/cn/articles/x86-high-performance-programming-pipeline?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global)

### 乱序执行

乱序执行 vs 顺序提交
我们知道，在cpu中为了能够让指令的执行尽可能地并行起来，从而发明了流水线技术。但是如果两条指令的前后存在依赖关系，比如数据依赖，控制依赖等，此时后一条语句就必需等到前一条指令完成后，才能开始。

cpu为了提高流水线的运行效率，会做出比如: 1)对无依赖的前后指令做适当的乱序和调度；2)对控制依赖的指令做分支预测；3)对读取内存等的耗时操作，做提前预读；等等。以上总总，都会导致指令乱序的可能。

指令在cpu核内部确实是乱序执行和调度的，但是它们对外表现却是顺序提交的。

### Store Buffer

[https://zhuanlan.zhihu.com/p/141655129](https://zhuanlan.zhihu.com/p/141655129)

store buffer是什么
在之前的文章介绍中，我们了解到每个CPU都会有自己私有L1 Cache。从我了解的资料来说，L1 Cache命中的情况下，访问数据一般需要2个指令周期。而且当CPU遭遇写数据cache未命中时，内存访问延迟增加很多。硬件工程师为了追求极致的性能，在CPU和L1 Cache之间又加入一级缓存，我们称之为store buffer。store buffer和L1 Cache还有点区别，store buffer只缓存CPU的写操作。store buffer访问一般只需要1个指令周期，这在一定程度上降低了内存写延迟。不管cache是否命中，CPU都是将数据写入store buffer。store buffer负责后续以FIFO次序写入L1 Cache。store buffer大小一般只有几十个字节。大小和L1 Cache相比，确实是小巫见大巫了。

### Invalid Queue

## 超线程

超线程技术就是利用特殊的硬件指令，把一个物理芯片模拟成两个逻辑处理核心，让单个处理器都能使用线程级并行计算，进而兼容多线程操作系统和软件，减少了CPU的闲置时间，提高的CPU的运行效率。这种超线程技术(如双核四线程)由处理器硬件的决定，同时也需要操作系统的支持才能在计算机中表现出来

[https://www.cnblogs.com/Survivalist/p/11527949.html](https://www.cnblogs.com/Survivalist/p/11527949.html)

## '查CPU,  核心数'

```bash
lscpu

cat /proc/cpuinfo |grep name

# 总核数 = 物理CPU个数 X 每颗物理CPU的核数 
# 总逻辑CPU数 = 物理CPU个数 X 每颗物理CPU的核数 X 超线程数

# 查看物理CPU个数
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l

# 查看每个物理CPU中core的个数(即核数)
cat /proc/cpuinfo| grep "cpu cores"| uniq

# 查看逻辑CPU的个数
cat /proc/cpuinfo| grep "processor"| wc -l
grep 'model name' /proc/cpuinfo | wc -l

```

## Intel CPU

## Cascade Lake

第二代智能英特尔® 至强® 可扩展处理器，前身为 Cascade Lake，搭载英特尔® C620 系列芯片组（前身为 Purley refresh)， 配有内置英特尔® 深度学习加速（英特尔® DL Boost），可针对人工智能工作负载提供高性能推断和视觉。它可整合多元化的物联网工作负载、处理海量数据集并支持接近实时的交易。现在，借助英特尔® Distribution of OpenVINO™ Toolkit 等已进行 CPU 优化的软件工具套件和框架，您可以获得更好的内置深度学习功能，加快部署速度，并降低总拥有成本 (TCO)。

## Skylake

Intel Skylake 是英特尔的微处理器架构，是Intel Haswell／Broadwell微架构的继任者。[1]Intel Skylake微架为使用14纳米制程制造。[2] 根据Intel于2016年公开的Tick-Tock发展战略模式，Skylake是一个“Architechture”版本，意思是在“Process”制程基础上，更新微处理器架构，提升性能[3]。Skylake的下一代架构为Kaby Lake（已于2016年下半年发布）

## E5-2680

至强® 处理器 E5-2680

## CPU Benchmarks

[https://www.cpubenchmark.net/high_end_cpus.html](https://www.cpubenchmark.net/high_end_cpus.html)
