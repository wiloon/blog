---
title: 进入safepoint时如何让Java线程全部阻塞
author: "-"
date: 2013-09-13T10:49:30+00:00
url: /?p=5807
categories:
  - Java
tags:
  - reprint
---
## 进入safepoint时如何让Java线程全部阻塞

<http://blog.csdn.net/iter_zc/article/details/41892567>

在这篇聊聊JVM (六) 理解JVM的safepoint 中说了safepoint的基本概念，VM thread在进行GC前，必须要让所有的Java线程阻塞，从而stop the world，开始标记。JVM采用了主动式阻塞的方式，Java线程不是随时都可以进入阻塞，需要运行到特定的点，叫safepoint，在这些点的位置Java线程可以被全部阻塞，整个堆的状态是一个暂时稳定的状态，OopMap指出了这个时刻，寄存器和栈内存的哪些具体的地址是引用，从而可以快速找到GC roots来进行对象的标记操作。

那么当Java线程运行到safepoint的时候，JVM如何让Java线程挂起呢？这是一个复杂的操作。很多文章里面说了JIT编译模式下，编译器会把很多safepoint检查的操作插入到编译偶的指令中，比如下面的指令来自内存篇: JVM内存回收理论与实现
  
```java
  
0x01b6d627: call 0x01b2b210 ; OopMap{[60]=Oop off=460}
                                         
;_invokeinterface size
                                         
; - Client1::main@113 (line 23)
                                         
; {virtual_call}
   
0x01b6d62c: nop ; OopMap{[60]=Oop off=461}
                                         
;_if_icmplt
                                         
; - Client1::main@118 (line 23)
   
0x01b6d62d: test %eax,0x160100 ; {poll}
   
0x01b6d633: mov 0x50(%esp),%esi
   
0x01b6d637: cmp %eax,%esi

test %eax,0x160100 就是一个safepoint polling page操作。当JVM要停止所有的Java线程时会把一个特定内存页设置为不可读，那么当Java线程读到这个位置的时候就会被挂起

这个回答虽然是没有问题，但是有些点到为止的感觉，有些意犹未尽，我又深挖了一些资料，很多资料连着一起看才能说明问题，下面再深入说说到底JVM是如何让Java线程全部

阻塞的。

Points on Safepoints 这篇文章说明了一些问题。首先是关于一些safepoint的观点

All commercial GCs use safepoints.
  
The GC reigns in all threads at safepoints. This is when it has exact knowledge of things touched by the threads.
  
They can also be used for non-GC activity like optimization.
  
A thread at a safepoint is not necessarily idle but it often is.
  
Safepoint opportunities should be frequent.
  
All threads need to reach a global safepoint typically every dozen or so instructions (for example, at the end of loops).
  
safepoint机制可以stop the world，不仅仅是在GC的时候用，有很多其他地方也会用它来stop the world，阻塞所有Java线程，从而可以安全地进行一些操作。
  
看一下OpenJDK里面关于safepoint的一些说明

```java
 
// Begin the process of bringing the system to a safepoint.
  
// Java threads can be in several different states and are
  
// stopped by different mechanisms:
  
//
  
// 1. Running interpreted
  
// The interpeter dispatch table is changed to force it to
  
// check for a safepoint condition between bytecodes.
  
// 2. Running in native code
  
// When returning from the native code, a Java thread must check
  
// the safepoint _state to see if we must block. If the
  
// VM thread sees a Java thread in native, it does
  
// not wait for this thread to block. The order of the memory
  
// writes and reads of both the safepoint state and the Java
  
// threads state is critical. In order to guarantee that the
  
// memory writes are serialized with respect to each other,
  
// the VM thread issues a memory barrier instruction
  
// (on MP systems). In order to avoid the overhead of issuing
  
// a mem barrier for each Java thread making native calls, each Java
  
// thread performs a write to a single memory page after changing
  
// the thread state. The VM thread performs a sequence of
  
// mprotect OS calls which forces all previous writes from all
  
// Java threads to be serialized. This is done in the
  
// os::serialize_thread_states() call. This has proven to be
  
// much more efficient than executing a membar instruction
  
// on every call to native code.
  
// 3. Running compiled Code
  
// Compiled code reads a global (Safepoint Polling) page that
  
// is set to fault if we are trying to get to a safepoint.
  
// 4. Blocked
  
// A thread which is blocked will not be allowed to return from the
  
// block condition until the safepoint operation is complete.
  
// 5. In VM or Transitioning between states
  
// If a Java thread is currently running in the VM or transitioning
  
// between states, the safepointing code will wait for the thread to
  
// block itself when it attempts transitions to a new state.
  
//
```

可以看到JVM在阻塞全部Java线程之前，Java线程可能处在不同的状态，这篇聊聊JVM (五) 从JVM角度理解线程 说了JVM里面定义的线程所有的状态。

1. 当线程在解释模式下执行的时候，让JVM发出请求之后，解释器会把指令跳转到检查safepoint的状态，比如检查某个内存页位置，从而让线程阻塞
2. 当Java线程正在执行native code的时候，这种情况最复杂，篇幅也写的最多。当VM thread看到一个Java线程在执行native code，它不需要等待这个Java线程进入阻塞状态，因为当Java线程从执行native code返回的时候，Java线程会去检查safepoint看是否要block(When returning from the native code, a Java thread must check the safepoint _state to see if we must block)

后面说了一大堆关于如何让读写safepoint state和thread state按照严格顺序执行(serialized)，主要用两种做法，一种是加内存屏障(Memeory barrier)，一种是调用mprotected系统调用去强制Java的写操作按顺序执行 (The VM thread performs a sequence of mprotect OS calls which forces all previous writes from all Java threads to be serialized. This is done in the os::serialize_thread_states() call)

JVM采用的后者，因为内存屏障是一个很重的操作，要强制刷新CPU缓存，所以JVM采用了serialation page的方式。

说白了，就是在Java线程从执行native code状态返回的时候要作线程同步，采用serialtion page的方式做了线程同步，而不是采用内存屏障的方式。熟悉Java内存模型的同学知道，类似volatie这种轻量级同步变量采用的就是内存屏障的方式。

为什么要做线程同步呢，这篇 请教hotspot源码中关于Serialization Page的问题 解释了这个问题:

```java
  
AddressLiteral sync_state(SafepointSynchronize::address_of_state());
  
__ set(_thread_in_native_trans, G3_scratch);
  
__ st(G3_scratch, thread_state);
  
if(os::is_MP()) {
    
if (UseMembar) {
      
// Force this write out before the read below
      
__ membar(Assembler::StoreLoad);
    
} else {
      
// Write serialization page so VM thread can do a pseudo remote membar.
      
// We use the current thread pointer to calculate a thread specific
      
// offset to write to within the page. This minimizes bus traffic
      
// due to cache line collision.
      
__ serialize_memory(G2_thread, G1_scratch, G3_scratch);
    
}
  
}
  
__ load_contents(sync_state, G3_scratch);
  
__ cmp(G3_scratch, SafepointSynchronize::_not_synchronized);

这段代码首先将当前线程 (不妨称为thread A) 状态置为_thread_in_native_trans状态，然后读sync_state，看是否有线程准备进行GC，有则将当前线程block，等待GC线程进行GC。
  
由于读sync_state的过程不是原子的，存在一个可能的场景是thread A刚读到sync_stated，且其值是_not_synchronized，这时thread A被抢占，CPU调度给了准备发起GC的线程 (不妨称为thread B) ，该线程将sync_stated设置为了_synchronizing，然后读其他线程的状态，看其他线程是否都已经处于block状态或者_thread_in_native状态，是的话该线程就可以开始GC了，否则它还需要等待。

如果thread A在写线程状态与读sync_state这两个动作之间缺少membar指令，那么上述过程就有可能出现一个场景，就是thread A读到了sync_stated为_not_synchronized，而thread B还没有看到thread A的状态变为_thread_in_native_trans。这样thread B就会认为thread A已经具备GC条件 (因为处于_thread_in_native状态) ，如果其他线程此时也都准备好了，那thread B就会开始GC了。而thread A由于读到的sync_state是_not_synchronized，因此它不会block，而是会开始执行java代码，这样就会导致GC出错，进而系统崩溃。

主要原因就是读写safepoint state和thread state是不是原子的，需要同步操作，采用了serialization page是一个轻量级的同步方法。

关于serialation page具体的实现可以看这篇 关于memory_serialize_page的一些疑问 我看了之后的理解是相比与内存屏障每次写一个内存位置就要刷新CPU缓存的方式，serialization page采用了一个内存页的方式，每个线程顺序写一个位置，算法要保证多个线程不会写到同一个位置。然后VM thread把这个内存页设置为只读，把线程的状态刷新到相应的内存位置，然后再设置为可写。这样一是避免了刷新CPU缓存的操作，另外是一次可以批量处理多个线程。

  1. 当JVM以JIT编译模式运行的时候，就是最初说的在编译后代码插入一个检查全局的safepoint polling page，VM thread把它设置为不可读，让Java线程挂起 
  2. 当线程本来就是阻塞状态的时候，采用了safe region的方式，处于safe region的代码只有等到被允许的时候才能离开safe region，看这篇聊聊JVM (六) 理解JVM的safepoint

  3. 当线程处在状态转化的时候，线程会去检查safepoint状态，如果要阻塞，就自己阻塞了

那么线程到底是如何自己就阻塞了呢？在第2条的时候说了JVM可以使用mprotect 系统调用来保护一些所有线程可写的内存位置让他们不可写，当线程访问到这些被保护的内存位置时，会触发一个SIGSEGV信号,从而可以触发JVM的signal handler来阻塞这个线程(The GC thread can protect some memory to which all threads in the process can write (using the mprotect system call) so they no longer can. Upon accessing this temporarily forbidden memory, a signal handler kicks in
  
) 。这是mprotect的man page

  
If the calling process tries to access memory in a manner that violates the protection, then the kernel generates a SIGSEGV
  
signal for the process.

再看一下JVM如何处理SIGSEGV信号的 hotspot/src/os_cpu/linux_x86/vm/os_linux_x86.cpp
  
```java
  
// Check to see if we caught the safepoint code in the
      
// process of write protecting the memory serialization page.
      
// It write enables the page immediately after protecting it
      
// so we can just return to retry the write.
      
if ((sig == SIGSEGV) &&
          
os::is_memory_serialize_page(thread, (address) info->si_addr)) {
        
// Block current thread until the memory serialize page permission restored.
        
os::block_on_serialize_page_trap();
        
return true;
      
}

这下知道test %eax,0x160100 这个safepoint polling page操作为什么会阻塞线程了吧。
  
JVM要阻塞全部的Java线程的时候，要先检查所有的Java线程所处的状态，通过mprotect系统调用来保护一块全局的内存区域，然后让Java线程进入安全点去polling这个内存位置，当线程访问到这个forbidden内存位置的时候会触发JVM的signal handler来阻塞线程。

这个话题还涉及到JVM性能分析的一些场景。通过设置JVM参数 -XX:+PrintGCApplicationStoppedTime 会打出系统停止的时间，类似的日志如下面

```java 
  
Total time for which application threads were stopped: 0.0041000 seconds
  
Total time for which application threads were stopped: 0.0044230 seconds
  
Total time for which application threads were stopped: 0.0043610 seconds
  
Total time for which application threads were stopped: 0.0056040 seconds
  
Total time for which application threads were stopped: 0.0051020 seconds
  
Total time for which application threads were stopped: 8.2834300 seconds
  
Total time for which application threads were stopped: 0.0110790 seconds
  
Total time for which application threads were stopped: 0.0098720 seconds

可以看到有一行日志说系统等待了8秒，这是为什么呢，原因是有线程迟迟进入不到safepoint来阻塞，导致其他已经停止的线程也一直等待，VM Thread也在等待所有的Java线程都进入到safepoint阻塞才能开始GC。看这篇ParNew 应用暂停时间偶尔会出现好几秒的情况。
  
当遇到这种情况，就要分析是不是有大的循环操作，可能这些循环操作的时候JIT优化时没有插入safepoint检查的代码。

看到高性能虚拟机圈子的里面有好几个帖子说到全体Java线程进入到safepoint的时间较长，这和GC本身没有关系。如果有遇到这种情况的，可能就得去看代码是否有这种可能会被JIT优化，丢失safepoint的情况。How to get Java stacks when JVM can't reach a safepoint 这篇提到的问题也是safepoint没有被正确插入导致JVM Freezen，VM线程等待所有Java线程进入safepoint阻塞，而有Java线程做了大操作而迟迟无法进入safepoint。

参考资料:

Points on Safepoints
  
内存篇: JVM内存回收理论与实现
  
请教hotspot源码中关于Serialization Page的问题
  
关于memory_serialize_page的一些疑问

mprotect的man page

ParNew 应用暂停时间偶尔会出现好几秒的情况

How to get Java stacks when JVM can't reach a safepoint



## JVM的safepoint
http://blog.csdn.net/iter_zc/article/details/41847887

safepoint是JVM里面很重要的一个概念，在很多场景下都会看到它，尤其是在GC的时候。这篇讲讲safepoint。本人不是做JVM实现研究的，很多地方只能点到为止，希望能够讲清楚这个概念，具体的细节可以自己去找资料深入研究。

safepoint 安全点顾名思义是指一些特定的位置，当线程运行到这些位置时，线程的一些状态可以被确定(the thread's representation of it's Java machine state is well described)，比如记录OopMap的状态，从而确定GC Root的信息，使JVM可以安全的进行一些操作，比如开始GC。

safepoint指的特定位置主要有:

  1. 循环的末尾 (防止大循环的时候一直不进入safepoint，而其他线程在等待它进入safepoint) 
  2. 方法返回前

  3. 调用方法的call之后

  4. 抛出异常的位置

之所以选择这些位置作为safepoint的插入点，主要的考虑是"避免程序长时间运行而不进入safepoint"，比如GC的时候必须要等到Java线程都进入到safepoint的时候VMThread才能开始执行GC，如果程序长时间运行而没有进入safepoint，那么GC也无法开始，JVM可能进入到Freezen假死状态。在stackoverflow上有人提到过一个问题，由于BigInteger的pow执行时JVM没有插入safepoint,导致大量运算时线程一直无法进入safepoint，而GC线程也在等待这个Java线程进入safepoint才能开始GC，结果JVM就Freezen了。

How to get Java stacks when JVM can't reach a safepoint

JVM在很多场景下使用到safepoint, 最常见的场景就是GC的时候。对一个Java线程来说，它要么处在safepoint,要么不在safepoint。
  
1. Garbage collection pauses
  
2. Code deoptimization
  
3. Flushing code cache
  
4. Class redefinition (e.g. hot swap or instrumentation)
  
5. Biased lock revocation
  
6. Various debug operation (e.g. deadlock check or stacktrace dump)

GC的标记阶段需要stop the world，让所有Java线程挂起，这样JVM才可以安全地来标记对象。safepoint可以用来实现让所有Java线程挂起的需求。这是一种"主动式"(Voluntary Suspension)的实现。JVM有两种执行方式: 解释型和编译型(JIT)，JVM要保证这两种执行方式下safepoint都能工作。

在JIT执行方式下，JIT编译的时候直接把safepoint的检查代码加入了生成的本地代码，当JVM需要让Java线程进入safepoint的时候，只需要设置一个标志位，让Java线程运行到safepoint的时候主动检查这个标志位，如果标志被设置，那么线程停顿，如果没有被设置，那么继续执行。

例如hotspot在x86中为轮询safepoint会生成一条类似于"test %eax,0x160100"的指令，JVM需要进入gc前，先把0x160100设置为不可读，那所有线程执行到检查0x160100的test指令后都会停顿下来

```html 
  
0x01b6d627: call 0x01b2b210 ; OopMap{[60]=Oop off=460}
                                         
;_invokeinterface size
                                         
; - Client1::main@113 (line 23)
                                         
; {virtual_call}
   
0x01b6d62c: nop ; OopMap{[60]=Oop off=461}
                                         
;_if_icmplt
                                         
; - Client1::main@118 (line 23)
   
0x01b6d62d: test %eax,0x160100 ; {poll}
   
0x01b6d633: mov 0x50(%esp),%esi
   
0x01b6d637: cmp %eax,%esi

在解释器执行方式下，JVM会设置一个2字节的dispatch tables,解释器执行的时候会经常去检查这个dispatch tables，当有safepoint请求的时候，就会让线程去进行safepoint检查。

聊聊JVM (五) 从JVM角度理解线程 说了JVM中的线程类型，其中提到VMThread。VMThread会一直等待直到VMOperationQueue中有操作请求出现，比如GC请求。而VMThread要开始工作必须要等到所有的Java线程进入到safepoint。JVM维护了一个数据结构，记录了所有的线程，所以它可以快速检查所有线程的状态。当有GC请求时，所有进入到safepoint的Java线程会在一个Thread_Lock锁阻塞，直到当JVM操作完成后，VM释放Thread_Lock，阻塞的Java线程才能继续运行。

GC stop the world的时候，所有运行Java code的线程被阻塞，如果运行native code线程不去和Java代码交互，那么这些线程不需要阻塞。VM操作相关的线程也不会被阻塞。

safepoint只能处理正在运行的线程，它们可以主动运行到safepoint。而一些Sleep或者被blocked的线程不能主动运行到safepoint。这些线程也需要在GC的时候被标记检查，JVM引入了safe region的概念。safe region是指一块区域，这块区域中的引用都不会被修改，比如线程被阻塞了，那么它的线程堆栈中的引用是不会被修改的，JVM可以安全地进行标记。线程进入到safe region的时候先标识自己进入了safe region，等它被唤醒准备离开safe region的时候，先检查能否离开，如果GC已经完成，那么可以离开，否则就在safe region呆在。这可以理解，因为如果GC还没完成，那么这些在safe region中的线程也是被stop the world所影响的线程的一部分，如果让他们可以正常执行了，可能会影响标记的结果

可以设置JVM参数 -XX:+PrintSafepointStatistics –XX:PrintSafepointStatisticsCount=1 来输出safepoint的统计信息

参考资料:
  
找出栈上的指针/引用
  
What is a Java safepoint
  
GC safe-point (or safepoint) and safe-region

内存篇: JVM内存回收理论与实现

Safepoints in HotSpot JVM
