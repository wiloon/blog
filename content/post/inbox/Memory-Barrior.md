---
title: "Memory Barrior, 内存屏障"
author: "-"
date: "2021-07-09 19:40:37"
url: "Memory-Barrior"
categories:
  - cs
tags:
  - reprint


---
## "Memory Barrior, 内存屏障"

屏障技术
内存屏障技术是一种屏障指令，它可以让 CPU 或者编译器在执行内存相关操作时遵循特定的约束，目前多数的现代处理器都会乱序执行指令以最大化性能，但是该技术能够保证内存操作的顺序性，在内存屏障前执行的操作一定会先于内存屏障后执行的操作6。

[https://draveness.me/golang/docs/part3-runtime/ch07-memory/golang-garbage-collector/](https://draveness.me/golang/docs/part3-runtime/ch07-memory/golang-garbage-collector/)

### 内存屏障 Memory Barrior

内存屏障 (Memory barrier)
为什么会有内存屏障
每个CPU都会有自己的缓存 (有的甚至L1,L2,L3) ，缓存的目的就是为了提高性能，避免每次都要向内存取。但是这样的弊端也很明显: 不能实时的和内存发生信息交换，分在不同CPU执行的不同线程对同一个变量的缓存值不同。
用volatile关键字修饰变量可以解决上述问题，那么volatile是如何做到这一点的呢？那就是内存屏障，内存屏障是硬件层的概念，不同的硬件平台实现内存屏障的手段并java通过屏蔽这些差异，统一由jvm来生成内存屏障的指令。
内存屏障是什么
硬件层的内存屏障分为两种: Load Barrier 和 Store Barrier即读屏障和写屏障。
内存屏障有两个作用:
阻止屏障两侧的指令重排序；
强制把写缓冲区/高速缓存中的脏数据等写回主内存，让缓存中相应的数据失效。
对于Load Barrier来说，在指令前插入Load Barrier，可以让高速缓存中的数据失效，强制从新从主内存加载数据；
对于Store Barrier来说，在指令后插入Store Barrier，能让写入缓存中的最新数据更新写入主内存，让其他线程可见。
java内存屏障
java的内存屏障通常所谓的四种即LoadLoad,StoreStore,LoadStore,StoreLoad实际上也是上述两种的组合，完成一系列的屏障和数据同步功能。
LoadLoad屏障: 对于这样的语句Load1; LoadLoad; Load2，在Load2及后续读取操作要读取的数据被访问前，保证Load1要读取的数据被读取完毕。
StoreStore屏障: 对于这样的语句Store1; StoreStore; Store2，在Store2及后续写入操作执行前，保证Store1的写入操作对其它处理器可见。
LoadStore屏障: 对于这样的语句Load1; LoadStore; Store2，在Store2及后续写入操作被刷出前，保证Load1要读取的数据被读取完毕。
StoreLoad屏障: 对于这样的语句Store1; StoreLoad; Load2，在Load2及后续所有读取操作执行前，保证Store1的写入对所有处理器可见。它的开销是四种屏障中最大的。
volatile语义中的内存屏障
volatile的内存屏障策略非常严格保守，非常悲观且毫无安全感的心态:
在每个volatile写操作前插入StoreStore屏障，在写操作后插入StoreLoad屏障；
在每个volatile读操作前插入LoadLoad屏障，在读操作后插入LoadStore屏障；

由于内存屏障的作用，避免了volatile变量和其它指令重排序、线程之间实现了通信，使得volatile表现出了锁的特性。
final语义中的内存屏障
对于final域，编译器和CPU会遵循两个排序规则:
新建对象过程中，构造体中对final域的初始化写入和这个对象赋值给其他引用变量，这两个操作不能重排序； (废话嘛)
初次读包含final域的对象引用和读取这个final域，这两个操作不能重排序； (晦涩，意思就是先赋值引用，再调用final值)
总之上面规则的意思可以这样理解，必需保证一个对象的所有final域被写入完毕后才能引用和读取。这也是内存屏障的起的作用:
写final域: 在编译器写final域完毕，构造体结束之前，会插入一个StoreStore屏障，保证前面的对final写入对其他线程/CPU可见，并阻止重排序。
读final域: 在上述规则2中，两步操作不能重排序的机理就是在读final域前插入了LoadLoad屏障。
X86处理器中，由于CPU不会对写-写操作进行重排序，所以StoreStore屏障会被省略；而X86也不会对逻辑上有先后依赖关系的操作进行重排序，所以LoadLoad也会变省略。

作者: Rinoux
链接: [https://www.jianshu.com/p/2ab5e3d7e510](https://www.jianshu.com/p/2ab5e3d7e510)

### 重排序

同步的目的是保证不同执行流对共享数据并发操作的一致性。在单核时代，使用原子变量就很容易达成这一目的。甚至因为CPU的一些访存特性，对某些内存对齐数据的读或写也具有原子的特性。但在多核架构下即使操作是原子的，仍然会因为其他原因导致同步失效。

首先是现代编译器的代码优化和编译器指令重排可能会影响到代码的执行顺序。

其次还有指令执行级别的乱序优化，流水线、乱序执行、分支预测都可能导致处理器次序 (Process Ordering，机器指令在CPU实际执行时的顺序) 和程序次序 (Program Ordering，程序代码的逻辑执行顺序) 不一致。可惜不影响语义依旧只能是保证单核指令序列间，单核时代CPU的Self-Consistent特性在多核时代已不存在 (Self-Consistent即重排原则: 有数据依赖不会进行重排，单核最终结果肯定一致) 。

除此还有硬件级别Cache一致性 (Cache Coherence) 带来的问题: CPU架构中传统的MESI协议中有两个行为的执行成本比较大。一个是将某个Cache Line标记为Invalid状态，另一个是当某Cache Line当前状态为Invalid时写入新的数据。所以CPU通过Store Buffer和Invalidate Queue组件来降低这类操作的延时。

### 编译器指令重排

    compiler-instruction-reordering

### 为什么会有内存乱序(memory reording)

为了加快代码的执行，编译器或CPU通常会对内存操作顺序进行一些修改，这就是memory reording 。因为内存乱序是由编译器或CPU造成的，所以其发生的时间在编译期 (compiler reording) ，或运行期 (CPU reording) 。即使在多线程的程序中，内存乱序也很少被注意到，这是因为内存乱序有一个基本的原则: 不能修改单线程程序的行为。而且，在通常的多线程程序中，通常会通过加锁等方式来保持同步，这些方式通常都会阻止内存乱序的产生。但是，如果一个在多个线程间共享的内存资源没有锁保护的话，内存乱序的效果就会显现。下面这段话具体解释编译器和CPU为什么能通过乱序来加快执行速度:  

Memory access instructions, such as loads and stores, typically take longer to execute than other instructions. Therefore, compilers use registers to hold frequently used values and processors use high speed caches to hold the most frequently used memory locations. Another common optimization is for compilers and processors to rearrange the order that instructions are executed so that the processor does not have to wait for memory accesses to complete. This can result in memory being accessed in a different order than specified in the source code. While this typically will not cause a problem in a single thread of execution, it can cause a problem if the location can also be accessed from another processor or device.

总结一下，就是编译器乱序和CPU乱序的原因大致有两个: (1)局部性原理; (2)CPU乱序则更多的是由于CPU和内存读写的速度差距造成的，当然，归根到底都是CPU和memory的速度差距而引起的优化。

对内存进行操作的指令比如 load, store 一般比其它指令花费更长的时间，所以编译器用寄存器保存使用频率高的变量，处理器用高速缓存保存最近经常访问的内存区域。另外一种常用的优化方法是编译器或cpu对指令重排序，这样cpu不需要一直等待内存操作完成。这样会导致cpu实际访问内存的顺序有可能跟代码里写的不一样。这种重排序的操作一般不会对单线程的程序有影响，但是如果这块内存也同时被其它cpu或设备访问就可能有问题。

#### RISC, CISC 差异

在RISC
中，CPU并不会对内存中的数据进行操作，所有的计算都要求在寄存器中完成。而寄存器和内存的通信则由单独的指令来完成。而在CSIC中，CPU是可以直
接对内存进行操作的，这也是一个比较特别的地方。

更多的寄存器——和CISC
相比，基于RISC的处理器有更多的通用寄存器可以使用，且每个寄存器都可以进行数据存储或者寻址。

内存访问: X86指令可访问内存地址，而现代RISC CPU则使用LOAD/STORE模式，只有LOAD和STORE指令才能从内存中读取数据到寄存器，所有其他指令只对寄存器中的操作数计算。在CPU的速度是内存速度的5倍或5倍以上的情况下，后一种工作模式才是正途。

>[https://cothee.github.io/programming/2019/07/30/memory-reording/](https://cothee.github.io/programming/2019/07/30/memory-reording/)
>[https://blog.csdn.net/yongchaocsdn/article/details/57181573](https://blog.csdn.net/yongchaocsdn/article/details/57181573)
