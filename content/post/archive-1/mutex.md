---
title: mutex, 锁
author: "-"
date: 2014-11-19T08:39:34+00:00
url: mutex
categories:
  - lock
tags:
  - reprint
---
## mutex, 锁
# mutex
Mutual exclusion (或者锁) 的实现有硬件实现和软件实现, 软件实现是通过一些特别的算法譬如 Peterson's algorithm,这类软件实现通常比硬件实现需要更多的内存,而且由于现代计算机的乱序执行,需要手动加memory barrier来保证memory ordering,这里暂时不做讨论纯软件实现。CPU如果提供一些用来构建锁的atomic指令,一般会更高效一些。
### 锁的本质
所谓的锁,在计算机里本质上就是一块内存空间。当这个空间被赋值为1的时候表示加锁了,被赋值为0的时候表示解锁了,仅此而已。多个线程抢一个锁,就是抢着要把这块内存赋值为1。在一个多核环境里,内存空间是共享的。每个核上各跑一个线程,那如何保证一次只有一个线程成功抢到锁呢？你或许已经猜到了,这必须要硬件的某种 guarantee。具体的实现如下。
### 硬件
CPU如果提供一些用来构建锁的 atomic 指令, 譬如 x86 的 CMPXCHG (加上LOCK prefix), 能够完成 atomic 的 compare-and-swap (CAS), 用这样的硬件指令就能实现 spin lock. 本质上 LOCK 前缀的作用是锁定系统总线 (或者锁定某一块cache line) 来实现atomicity,可以了解下基础的缓存一致协议譬如MSEI。简单来说就是,如果指令前加了LOCK前缀,就是告诉其他核,一旦我开始执行这个指令了,在我结束这个指令之前,谁也不许动。缓存一致协议在这里面扮演了重要角色,这里先不赘述。这样便实现了一次只能有一个核对同一个内存地址赋值。
### 操作系统
mutex在linux内核中由 futex 系统调用支撑，如果没有竞争不需要陷入内核；内核的主要是 futex_wait/wake 函数配合上层完成业务逻辑；

一个 spin lock 就是让没有抢到锁的线程不断在 while 里面循环进行 compare-and-swap, 燃烧CPU, 浪费青春, 直到前面的线程放手 (对应的内存被赋值0) 。这个过程不需要操作系统的介入,这是运行程序和硬件之间的故事。如果需要长时间的等待,这样反复CAS轮询就比较浪费资源,这个时候程序可以向操作系统申请被挂起,然后持锁的线程解锁了以后再通知它。这样CPU就可以用来做别的事情,而不是反复轮询。
但是OS切换线程也需要一些开销,所以是否选择被挂起,取决于大概是否需要等很长时间,如果需要,则适合挂起切换为别的线程。线程向操作系统请求被**挂起**是通过一个系统调用,在linux上的实现就是 **futex**, 宏观来讲, OS需要一些全局的数据结构来记录一个被挂起线程和对应的锁的映射关系,这样一个数据结构天然是全局的,因为多个OS线程可能同时操作它。所以,实现高效的锁本身也需要锁。有没有一环套一环的感觉？futex的巧妙之处就在于,它知道访问这个全局数据结构不会太耗时,于是futex里面的锁就是spin lock。linux上pthread mutex 的实现就是用的 futex 。更多精彩内存参考talk: https://www.infoq.com/presentations/go-locks/
### 用户态的锁
像Goroutine线程就是go runtime来调度的,而不是OS,所以go routine线程切换的开销要远小于OS线程切换的开销。Goroutine的本质就是一个coroutine,这种轻量的线程在很多语言的runtime里面都有实现。最近Java也有了 (project loom) 。

### 其他high-level的锁
前面都是最底层的锁,用这些底层锁还可以构建更上层的锁。Condition variable,semaphore,RW lock之类的以后再写。

https://casatwy.com/pthreadde-ge-chong-tong-bu-ji-zhi.html

MUTual-EXclude Lock,互斥锁。 它是理解最容易,使用最广泛的一种同步机制。顾名思义,被这个锁保护的临界区就只允许一个线程进入,其它线程如果没有获得锁权限,那就只能在外面等着。

它使用得非常广泛,以至于大多数人谈到锁就是mutex。mutex是互斥锁,pthread里面还有很多锁,mutex只是其中一种。

### cmpxchg
cmpxchg是一个比较交换指令，原意是Compare and Exchange
cmpxchg 是 intel CPU 指令集中的一条指令, 这条指令经常用来实现原子锁, 我们来看 intel 文档中对这条指令的介绍: 

Compares the value in the AL, AX, EAX, or RAX register with the first operand (destination operand). If the two values are equal, the second operand (source operand) is loaded into the destination operand. Otherwise, the destination operand is loaded into the AL, AX, EAX or RAX register. RAX register is available only in 64-bit mode.

This instruction can be used with a LOCK prefix to allow the instruction to be executed atomically. To simplify the interface to the processor’s bus, the destination operand receives a write cycle without regard to the result of the comparison. The destination operand is written back if the comparison fails; otherwise, the source operand is written into the destination. (The processor never produces a locked read without also producing a locked write.)

可以看到 cmpxchg 指令有两个操作数, 同时还使用了 AX 寄存器。 首先,它将第一个操作数 (目的操作数) 和 AX 寄存器相比较, 如果相同则把第二个操作数 (源操作数) 赋值给第一个操作数,ZF 寄存器置一, 否则将第一个操作数赋值给 AX 寄存器且 ZF 寄存器置零。 在多核环境中,一般还在指令前加上 LOCK 前缀,来保证指令执行的原子性 (LOCK 前缀的主要功能应该是锁内存总线) 。

注: AT&T 风格的汇编语法中,第一个操作数是源操作数,第二个操作数是目的操作数。

cmpxchg 指令的操作具有原子性,可以用以下伪代码来表示: 

if (dst == %ax) {
    dst = src;
    ZF = 1;
} else {
    %ax = dst
    ZF = 0;
}

Linux 内核代码中使用宏来封装cmpxchg指令操作,相关源码在这里 https://elixir.bootlin.com/linux/latest/source/tools/arch/x86/include/asm/cmpxchg.h#L86

在上述例子中，eax就是old，ebx就是ptr指向的内容，ecx就是new。
cmpxchg %ecx, %ebx；如果EAX与EBX相等，则ECX送EBX且ZF置1；否则EBX送EAX，且ZF清0

也就是说， 在old和ptr指向的内容不相等的时候，将ptr的内容写入eax中，这样，ptr的内容就会返回给cmpxchg函数的调用者。这样就和原意相符合了。


Intel x86比较交换指令cmpxchg的作用与原理
cmpxchg是一个比较交换指令，原意是Compare and Exchange。

本文根据《Intel64和IA-32架构软件开发者手册》第2卷 (《Intel® 64 and IA-32 Architectures Software Developer's Manual》 Volume 2 (2A, 2B, 2C & 2D): Instruction Set Reference, A-Z) ，总结一下cmpxchg指令的作用，以及其实现原理。

指令格式
cmpxchg dest,src
复制代码
将AL、AX、EAX或RAX寄存器中的值与第一个操作数dest (目标操作数) 进行比较。 如果两个值相等，则将第二个操作数src (源操作数) 加载到目标操作数中。 如果不相等，则目标操作数被加载到AL、AX、EAX或RAX寄存器中。 RAX寄存器仅在64位模式下可用。

该指令可以与LOCK锁前缀一起使用，使得指令以原子的方式执行。 为了简化到处理器总线的接口，不管比较结果是否相等，目标操作数都将接收一个写周期。 如果比较失败 (不相等) ，则目标操作数将会被回写 (为原来的值) ；否则，源操作数将被写入目标操作数。 (处理器不会产生锁读，也不会产生锁写。)

在64位模式下，该指令的默认操作数大小为32位。 如果使用REX.R前缀，允许访问附加的寄存器 (R8-R15) 。 如果使用REX.W前缀，可以将操作数大小提升为64位。

以64位模式为例
CMPXCHG r/m32, r32
复制代码
指令说明:  比较寄存器EAX和目标操作数r/m32的值是否相等。 (这里提到的值，是指寄存器或内存单元中的值)  如果相等，则设置ZF标志位 (置为1) ，并将寄存器r32的值保存到操作数r/m32中，替换掉旧值； 如果不相等，则清除ZF标志位 (置为0) ，并将寄存器r/m32的值加载到寄存器EAX中，更新EAX为目标操作数的值。

其中:  r32: 表示源操作数，用于暂存新值。 r/m32: 表示目标操作数。如果指令执行成功，其对应地址存储的值将会被替换为新值。 EAX: 一个通用寄存器，用于暂存旧值，用来与目标操作数进行比较。

操作数符号的详细含义
r32:  表示一个双字 (32位) 的通用寄存器: EAX, ECX, EDX, EBX, ESP, EBP, ESI, EDI; 或者如果是在64位模式下使用REX.R，则表示一个可用的双字寄存器 (R8D-R15D) 。

r/m32:  表示一个双字 (32位) 通用寄存器或者内存操作数，用于操作数大小为32位的指令。 (如使用32位的寄存器、32位的内存单元)  双字通用寄存器有: EAX，ECX，EDX，EBX，ESP，EBP，ESI，EDI。 在64位模式下使用REX.R时，可以使用附加的双字寄存器 (R8D-R15D) 。

IA-32架构兼容性
在Intel486处理器之前的Intel处理器上不支持该指令。

指令伪代码
TEMP := DEST // 目标操作数的值保存到TEMP
IF accumulator = TEMP // 比较旧值与目标值是否相等
  THEN // 如果相等，则设置ZF为1，并将新值保存到目标操作数中
    ZF := 1; // 设置ZF为1
    DEST := SRC; // 将新值保存到目标操作数中
  ELSE // 如果不相等
    ZF := 0; // 清除ZF，设置ZF为0
    accumulator := TEMP; // 将目标操作数的值保存到累加器
    DEST := TEMP; // 将TEMP的值回写到目标操作数
FI;
复制代码
其中，accumulator表示累加器，指AL、AX、EAX或者RAX，具体取决于执行的是字节、单字、双字还是四字比较。 TEMP用于暂存目标操作数，在比较失败时赋值给累加器accumulator，并回写到目标操作数DEST。 ZF是状态寄存器中的一个零标志 (Zero Flag) 位，如果运算结果为零 (0) ，则设置 (1或true) ，否则进行重置

### c mutex
>https://blog.csdn.net/google19890102/article/details/62047798
>https://www.cnblogs.com/zengkefu/p/5683957.html
 
首先我们看一下互斥锁。所谓的互斥就是线程之间互相排斥，获得资源的线程排斥其它没有获得资源的线程。Linux使用互斥锁来实现这种机制。
既然叫锁，就有加锁和解锁的概念。当线程获得了加锁的资格，那么它将独享这个锁，其它线程一旦试图去碰触这个锁就立即被系统“拍晕”。当加锁的线程解开并放弃了这个锁之后，那些被“拍晕”的线程会被系统唤醒，然后继续去争抢这个锁。至于谁能抢到，只有天知道。但是总有一个能抢到。于是其它来凑热闹的线程又被系统给“拍晕”了……如此反复。感觉线程的“头”很痛: ) 
从互斥锁的这种行为看，线程加锁和解锁之间的代码相当于一个独木桥，同意时刻只有一个线程能执行。从全局上看，在这个地方，所有并行运行的线程都变成了排队运行了。比较专业的叫法是同步执行，这段代码区域叫临界区。同步执行就破坏了线程并行性的初衷了，临界区越大破坏得越厉害。所以在实际应用中，应该尽量避免有临界区出现。实在不行，临界区也要尽量的小。如果连缩小临界区都做不到，那还使用多线程干嘛？
互斥锁在Linux中的名字是mutex。这个似乎优点眼熟。对，在前面介绍NPTL的时候提起过，但是那个叫futex，是系统底层机制。对于提供给用户使用的则是这个mutex。Linux初始化和销毁互斥锁的接口是pthread_mutex_init()和pthead_mutex_destroy()，对于加锁和解锁则有pthread_mutex_lock()、pthread_mutex_trylock()和pthread_mutex_unlock()。这些接口的完整定义如下: 
int pthread_mutex_init(pthread_mutex_t *restrict mutex,const pthread_mutexattr_t *restrict attr);  
int pthread_mutex_destory(pthread_mutex_t *mutex );  
int pthread_mutex_lock(pthread_mutex_t *mutex);  
int pthread_mutex_trylock(pthread_mutex_t *mutex);  
int pthread_mutex_unlock(pthread_mutex_t *mutex);  
从这些定义中可以看到，互斥锁也是有属性的。只不过这个属性在绝大多数情况下都不需要改动，所以使用默认的属性就行。方法就是给它传递NULL。
phtread_mutex_trylock()比较特别，用它试图加锁的线程永远都不会被系统“拍晕”，只是通过返回EBUSY来告诉程序员这个锁已经有人用了。至于是否继续“强闯”临界区，则由程序员决定。系统提供这个接口的目的可不是让线程“强闯”临界区的。它的根本目的还是为了提高并行性，留着这个线程去干点其它有意义的事情。当然，如果很幸运恰巧这个时候还没有人拥有这把锁，那么自然也会取得临界区的使用权。
代码6演示了在Linux下如何使用互斥锁。

---

https://www.zhihu.com/question/332113890
https://www.infoq.com/presentations/go-locks/
https://en.wikipedia.org/wiki/Mutual_exclusion
https://en.wikipedia.org/wiki/Peterson's_algorithm
https://www.zhihu.com/question/53303879

作者: 陈清扬
链接: https://www.zhihu.com/question/332113890/answer/1052024052
来源: 知乎
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

https://coderatwork.cn/posts/linux-cmpxchg/

https://juejin.cn/post/6905287769006800903
