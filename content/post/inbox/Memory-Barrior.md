---
title: "Memory Barrior, 内存屏障"
author: "-"
date: "2021-07-09 19:40:37"
url: "Memory-Barrior"
categories:
  - inbox
tags:
  - inbox
---
### 内存屏障 Memory Barrior


### 重排序
同步的目的是保证不同执行流对共享数据并发操作的一致性。在单核时代，使用原子变量就很容易达成这一目的。甚至因为CPU的一些访存特性，对某些内存对齐数据的读或写也具有原子的特性。但在多核架构下即使操作是原子的，仍然会因为其他原因导致同步失效。

首先是现代编译器的代码优化和编译器指令重排可能会影响到代码的执行顺序。

其次还有指令执行级别的乱序优化，流水线、乱序执行、分支预测都可能导致处理器次序（Process Ordering，机器指令在CPU实际执行时的顺序）和程序次序（Program Ordering，程序代码的逻辑执行顺序）不一致。可惜不影响语义依旧只能是保证单核指令序列间，单核时代CPU的Self-Consistent特性在多核时代已不存在（Self-Consistent即重排原则：有数据依赖不会进行重排，单核最终结果肯定一致）。

除此还有硬件级别Cache一致性（Cache Coherence）带来的问题：CPU架构中传统的MESI协议中有两个行为的执行成本比较大。一个是将某个Cache Line标记为Invalid状态，另一个是当某Cache Line当前状态为Invalid时写入新的数据。所以CPU通过Store Buffer和Invalidate Queue组件来降低这类操作的延时。


### 编译器指令重排
    compiler-instruction-reordering