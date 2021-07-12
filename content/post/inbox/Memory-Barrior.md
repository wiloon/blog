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
内存屏障（Memory barrier）
为什么会有内存屏障
每个CPU都会有自己的缓存（有的甚至L1,L2,L3），缓存的目的就是为了提高性能，避免每次都要向内存取。但是这样的弊端也很明显：不能实时的和内存发生信息交换，分在不同CPU执行的不同线程对同一个变量的缓存值不同。
用volatile关键字修饰变量可以解决上述问题，那么volatile是如何做到这一点的呢？那就是内存屏障，内存屏障是硬件层的概念，不同的硬件平台实现内存屏障的手段并java通过屏蔽这些差异，统一由jvm来生成内存屏障的指令。
内存屏障是什么
硬件层的内存屏障分为两种：Load Barrier 和 Store Barrier即读屏障和写屏障。
内存屏障有两个作用：
阻止屏障两侧的指令重排序；
强制把写缓冲区/高速缓存中的脏数据等写回主内存，让缓存中相应的数据失效。
对于Load Barrier来说，在指令前插入Load Barrier，可以让高速缓存中的数据失效，强制从新从主内存加载数据；
对于Store Barrier来说，在指令后插入Store Barrier，能让写入缓存中的最新数据更新写入主内存，让其他线程可见。
java内存屏障
java的内存屏障通常所谓的四种即LoadLoad,StoreStore,LoadStore,StoreLoad实际上也是上述两种的组合，完成一系列的屏障和数据同步功能。
LoadLoad屏障：对于这样的语句Load1; LoadLoad; Load2，在Load2及后续读取操作要读取的数据被访问前，保证Load1要读取的数据被读取完毕。
StoreStore屏障：对于这样的语句Store1; StoreStore; Store2，在Store2及后续写入操作执行前，保证Store1的写入操作对其它处理器可见。
LoadStore屏障：对于这样的语句Load1; LoadStore; Store2，在Store2及后续写入操作被刷出前，保证Load1要读取的数据被读取完毕。
StoreLoad屏障：对于这样的语句Store1; StoreLoad; Load2，在Load2及后续所有读取操作执行前，保证Store1的写入对所有处理器可见。它的开销是四种屏障中最大的。
volatile语义中的内存屏障
volatile的内存屏障策略非常严格保守，非常悲观且毫无安全感的心态：
在每个volatile写操作前插入StoreStore屏障，在写操作后插入StoreLoad屏障；
在每个volatile读操作前插入LoadLoad屏障，在读操作后插入LoadStore屏障；

由于内存屏障的作用，避免了volatile变量和其它指令重排序、线程之间实现了通信，使得volatile表现出了锁的特性。
final语义中的内存屏障
对于final域，编译器和CPU会遵循两个排序规则：
新建对象过程中，构造体中对final域的初始化写入和这个对象赋值给其他引用变量，这两个操作不能重排序；（废话嘛）
初次读包含final域的对象引用和读取这个final域，这两个操作不能重排序；（晦涩，意思就是先赋值引用，再调用final值）
总之上面规则的意思可以这样理解，必需保证一个对象的所有final域被写入完毕后才能引用和读取。这也是内存屏障的起的作用：
写final域：在编译器写final域完毕，构造体结束之前，会插入一个StoreStore屏障，保证前面的对final写入对其他线程/CPU可见，并阻止重排序。
读final域：在上述规则2中，两步操作不能重排序的机理就是在读final域前插入了LoadLoad屏障。
X86处理器中，由于CPU不会对写-写操作进行重排序，所以StoreStore屏障会被省略；而X86也不会对逻辑上有先后依赖关系的操作进行重排序，所以LoadLoad也会变省略。

作者：Rinoux
链接：https://www.jianshu.com/p/2ab5e3d7e510

### 重排序
同步的目的是保证不同执行流对共享数据并发操作的一致性。在单核时代，使用原子变量就很容易达成这一目的。甚至因为CPU的一些访存特性，对某些内存对齐数据的读或写也具有原子的特性。但在多核架构下即使操作是原子的，仍然会因为其他原因导致同步失效。

首先是现代编译器的代码优化和编译器指令重排可能会影响到代码的执行顺序。

其次还有指令执行级别的乱序优化，流水线、乱序执行、分支预测都可能导致处理器次序（Process Ordering，机器指令在CPU实际执行时的顺序）和程序次序（Program Ordering，程序代码的逻辑执行顺序）不一致。可惜不影响语义依旧只能是保证单核指令序列间，单核时代CPU的Self-Consistent特性在多核时代已不存在（Self-Consistent即重排原则：有数据依赖不会进行重排，单核最终结果肯定一致）。

除此还有硬件级别Cache一致性（Cache Coherence）带来的问题：CPU架构中传统的MESI协议中有两个行为的执行成本比较大。一个是将某个Cache Line标记为Invalid状态，另一个是当某Cache Line当前状态为Invalid时写入新的数据。所以CPU通过Store Buffer和Invalidate Queue组件来降低这类操作的延时。


### 编译器指令重排
    compiler-instruction-reordering
