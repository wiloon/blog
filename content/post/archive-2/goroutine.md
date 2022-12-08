---
title: 协程, coroutine, goroutine
author: "-"
date: 2017-03-24T15:52:22+00:00
url: goroutine
categories:
  - Go
tags:
  - reprint
---
## 协程, coroutine, goroutine

- routine, [ruːˈtiːn], 例程
- coroutine, [kəruːˈtiːn], 协同程序, 协程

Goroutine 是 Go 中最基本的执行单元。每一个 Go 程序至少有一个 goroutine：主 goroutine. 当程序启动时， 它被自动创建。

goroutine 采用了一种 fork-join 的模型 [[fork-join#ForkJoin]]

每个协程至少需要消耗 2KB 的空间

### 调度器

### 进程

跑在一个cpu里面的并发都需要处理上下文切换的问题。进程就是这样抽象出来个一个概念,搭配虚拟内存、进程表之类的东西,用来管理独立的程序运行、切换。

协程,又称微线程,纤程。英文名 coroutine
  
子程序,或者称为函数,在所有语言中都是层级调用,比如A调用B,B在执行过程中又调用了 C, C 执行完毕返回,B执行完毕返回,最后是A执行完毕。

所以子程序调用是通过栈实现的,一个线程就是执行一个子程序。

子程序调用总是一个入口,一次返回,调用顺序是明确的。而协程的调用和子程序不同。

协程看上去也是子程序,但执行过程中,在子程序内部可中断,然后转而执行别的子程序,在适当的时候再返回来接着执行。

注意,在一个子程序中中断,去执行其他子程序,不是函数调用,有点类似CPU的中断。比如子程序A、B:

def A():

print '1'

print '2'

print '3'

def B():

print 'x'

print 'y'

print 'z'
  
假设由协程执行,在执行A的过程中,可以随时中断,去执行B,B也可能在执行过程中中断再去执行A,结果可能是:

x
  
y
  
z
  
但是在A中是没有调用B的,所以协程的调用比函数调用理解起来要难一些。

看起来A、B的执行有点像多线程,但协程的特点在于是一个线程执行,那和多线程比,协程有何优势？

最大的优势就是协程极高的执行效率。因为子程序切换不是线程切换,而是由程序自身控制,因此,没有线程切换的开销,和多线程比,线程数量越多,协程的性能优势就越明显。

第二大优势就是不需要多线程的锁机制,因为只有一个线程,也不存在同时写变量冲突,在协程中控制共享资源不加锁,只需要判断状态就好了,所以执行效率比多线程高很多。

因为协程是一个线程执行,那怎么利用多核CPU呢？最简单的方法是多进程+协程,既充分利用多核,又充分发挥协程的高效率,可获得极高的性能。

一个goroutine锁使用的最小的栈大小是2KB ~ 8 KB (go stack)

Goroutine 有着和 Java 线程完全不同的调度机制,Java 线程模型中线程和 KSE (Kernel space Entity) 是 1:1 的关系,一个用户线程对应一个 KSE。而 Groutine 和 KSE 是多对多的对应关系。虽然,Groutine 的调度机制不如由内核直接调度的线程机制效率那么高,但是由于 Groutine 间的切换可以不涉及内核级切换,所以代价小很多。

用户级线程,整个线程的库都是自己维护,"创建,撤销,切换",内核是不知道用户级线程存在的,缺点是阻塞时会阻塞整个进程。

Goroutine是Golang中轻量级线程的实现,由Go Runtime管理。Golang在语言级别支持轻量级线程,叫携程。Golang标准库提供的所有系统调用操作 (当然也包括所有同步IO操作) ,都会出让CPU给其他Goroutine。这让事情变得非常简单,让轻量级线程的切换管理不依赖于系统的线程和进程,也不依赖于CPU的核心数量。

### 进程、线程、轻量级进程、协程和go中的Goroutine 那些事儿

虽然用python时候在Eurasia和eventlet里了解过协程,但自己对协程的概念也就是轻量级线程,还有一个很通俗的红绿灯说法: 线程要守规则,协程看到红灯但是没有车仍可以通行。现在总结各个资料,从个人理解上说明下 进程 线程 轻量级进程 协程 go中的goroutine 那些事儿。

### 进程

操作系统中最核心的概念是进程,分布式系统中最重要的问题是进程间通信。

进程是"程序执行的一个实例" ,担当分配系统资源的实体。进程创建必须分配一个完整的独立地址空间。

进程切换只发生在内核态,两步:

1. 切换页全局目录以安装一个新的地址空间
2. 切换内核态堆栈和硬件上下文。  
另一种说法类似:
3. 保存CPU环境 (寄存器值、程序计数器、堆栈指针)
4. 修改内存管理单元MMU的寄存器
5. 转换后备缓冲器TLB中的地址转换缓存内容标记为无效。

### 线程

书中的定义: 线程是进程的一个执行流,独立执行它自己的程序代码。

维基百科: 线程 (英语: thread) 是操作系统能够进行运算调度的最小单位。

线程上下文一般只包含CPU上下文及其他的线程管理信息。线程创建的开销主要取决于为线程堆栈的建立而分配内存的开销,这些开销并不大。线程上下文切换发生在两个线程需要同步的时候,比如进入共享数据段。切换只CPU寄存器值需要存储,并随后用将要切换到的线程的原先存储的值重新加载到CPU寄存器中去。

用户级线程主要缺点在于对引起阻塞的系统调用的调用会立即阻塞该线程所属的整个进程。内核实现线程则会导致线程上下文切换的开销跟进程一样大,所以折衷的方法是轻量级进程 (Lightweight) 。在linux中,一个线程组基本上就是实现了多线程应用的一组轻量级进程。我理解为进程中存在用户线程、轻量级进程、内核线程。

语言层面实现轻量级进程的比较少,stackless python,erlang支持,java并不支持。

### 协程

协程的定义？颜开、许式伟均只说协程是轻量级的线程,一个进程可轻松创建数十万计的协程。仔细研究下,个人感觉这些都是忽悠人的说法。从维基百科上看,从Knuth老爷子的基本算法卷上看"子程序其实是协程的特例"。子程序是什么？子程序 (英语: Subroutine, procedure, function, routine, method, subprogram) ,就是函数嘛！所以协程也没什么了不起的,就是种更一般意义的程序组件,那你内存空间够大,创建多少个函数还不是随你么？

协程可以通过yield来调用其它协程。通过yield方式转移执行权的协程之间不是调用者与被调用者的关系,而是彼此对称、平等的。协程的起始处是第一个入口点,在协程里,返回点之后是接下来的入口点。子例程的生命期遵循后进先出 (最后一个被调用的子例程最先返回) ；相反,协程的生命期完全由他们的使用的需要决定。

线程和协程的区别:

一旦创建完线程,你就无法决定他什么时候获得时间片,什么时候让出时间片了,你把它交给了内核。而协程编写者可以有一是可控的切换时机,二是很小的切换代价。从操作系统有没有调度权上看,协程就是因为不需要进行内核态的切换,所以会使用它,会有这么个东西。赖永浩和dccmx 这个定义我觉得相对准确  协程－用户态的轻量级的线程。 (<http://blog.dccmx.com/2011/04/coroutine-concept/>)

为什么要用协程:

协程有助于实现:

状态机: 在一个子例程里实现状态机,这里状态由该过程当前的出口/入口点确定；这可以产生可读性更高的代码。
  
角色模型: 并行的角色模型,例如计算机游戏。每个角色有自己的过程 (这又在逻辑上分离了代码) ,但他们自愿地向顺序执行各角色过程的中央调度器交出控制 (这是合作式多任务的一种形式) 。
  
产生器: 它有助于输入/输出和对数据结构的通用遍历。
  
颜开总结的支持协程的常见的语言和平台,可做参考,但应深入调研下才好。

### goroutine

go 中的 Goroutine, 普遍认为是协程的 go 语言实现。《Go语言编程》中说 goroutine 是轻量级线程 (即协程 coroutine, 原书90页). 在第九章进阶话题中, 作者又一次提到, "从根本上来说, goroutine就是一种go语言版本的协程(coroutine)" (原书204页). 但作者Rob Pike并不这么说。

"一个Goroutine是一个与其他goroutines 并发运行在同一地址空间的Go函数或方法。一个运行的程序由一个或更多个goroutine组成。它与线程、协程、进程等不同。它是一个goroutine。"

在栈实现上,它的编译器分支下的实现gccgo是线程pthread,6g上是多路复用的threads (6g/8g/5g分别代表64位、32位及Arm架构编译器)

infoQ一篇文章介绍特性也说道:  goroutine是Go语言运行库的功能,不是操作系统提供的功能,goroutine不是用线程实现的。具体可参见Go语言源码里的pkg/runtime/proc.c

老赵认为goroutine就是把类库功能放进了语言里。

goroutine的并发问题: goroutine在共享内存中运行,通信网络可能死锁,多线程问题的调试糟糕透顶等等。一个比较好的建议规则: 不要通过共享内存通信,相反,通过通信共享内存。

并行 并发区别:

并行是指程序的运行状态,要有两个线程正在执行才能算是Parallelism；并发指程序的逻辑结构,Concurrency则只要有两个以上线程还在执行过程中即可。简单地说,Parallelism要在多核或者多处理器情况下才能做到,而Concurrency则不需要。 (<http://stackoverflow.com/questions/1050222/concurrency-vs-parallelism-what-is-the-difference>)

goroutine 初始时只给栈分配很小的空间,然后随着使用过程中的需要自动地增长。这就是为什么Go可以开千千万万个goroutine而不会耗尽内存。
Go 1.4 开始使用的是连续栈,而这之前使用的分段栈。

### 分段栈(Segmented Stacks)

分段栈 (segmented stacks)是Go语言最初用来处理栈的方案。
当创建一个goroutine时,Go运行时会分配一段8K字节的内存用于栈供goroutine运行使用。

每个go函数在函数入口处都会有一小段代码,这段代码会检查是否用光了已分配的栈空间,如果用光了,这段代码会调用morestack函数。

morestack函数
morestack函数会分配一段新内存用作栈空间,接下来它会将有关栈的各种数据信息写入栈底的一个struct中(下图中Stack info),包括上一段栈的地址。然后重启goroutine,从导致栈空间用光的那个函数 (下图中的Foobar) 开始执行。这就是所谓的“栈分裂 (stack split)”。
在新栈的底部,插入了一个栈入口函数lessstack。设置这个函数用于从那个导致我们用光栈空间的函数(Foobar)返回时用的。当那个函数(Foobar)返回时,我们回到lessstack (这个栈帧) ,lessstack会查找 stack底部的那个struct,并调整栈指针(stack pointer),使得我们返回到前一段栈空间。这样做之后,我们就可以将这个新栈段(stack segment)释放掉,并继续执行我们的程序了。

分段栈的问题
栈缩小是一个相对代价高昂的操作。如果在一个循环中调用的函数遇到栈分裂 (stack split),进入函数时会增加栈空间(morestack 函数),返回并释放栈段(lessstack 函数)。性能方面开销很大。

#### 连续栈 (continuous stacks)

go现在使用的是这套解决方案。
goroutine在栈上运行着,当用光栈空间,它遇到与旧方案中相同的栈溢出检查。但是与旧方案采用的保留一个返 回前一段栈的link不同,新方案创建一个两倍于原stack大小的新stack,并将旧栈拷贝到其中。
这意味着当栈实际使用的空间缩小为原先的 大小时,go运行时不用做任何事情。
栈缩小是一个无任何代价的操作 (栈的收缩是垃圾回收的过程中实现的．当检测到栈只使用了不到1/4时,栈缩小为原来的1/2) 。
此外,当栈再次增长时,运行时也无需做任何事情,我们只需要重用之前分配的空闲空间即可。

如何捕获到函数的栈空间不足
Go语言和C不同,不是使用栈指针寄存器和栈基址寄存器确定函数的栈的。

在Go的运行时库中,每个goroutine对应一个结构体G,大致相当于进程控制块的概念。这个结构体中存了stackbase 和 stackguard,用于确定这个 goroutine 使用的栈空间信息。每个Go函数调用的前几条指令,先比较栈指针寄存器跟 g->stackguard,检测是否发生栈溢出。如果栈指针寄存器值超越了stackguard就需要扩展栈空间。

旧栈数据复制到新栈
旧栈数据复制到新栈的过程,要考虑指针失效问题。
Go实现了精确的垃圾回收,运行时知道每一块内存对应的对象的类型信息。在复制之后,会进行指针的调整。具体做法是,对当前栈帧之前的每一个栈帧,对其中的每一个指针,检测指针指向的地址,如果指向地址是落在旧栈范围内的,则将它加上一个偏移使它指向新栈的相应地址。这个偏移值等于新栈基地址减旧栈基地址。

### Continuation

所谓Continuation就是保存接下来要做的事情的内容(the rest of the computation)。举个简单例子，我在写文档，突然接到电话要外出，这时我存档，存档的数据就是Continuation(继续即将的写作)，然后等会儿回来，调入存档，继续写作。Continuation这个概念就协程来说就是协程保护的现场。而对于函数来说就是保存函数调用现场——Stack Frame值和寄存器，以供以后调用继续从Continuation处执行。换一个角度看，它也可以看作是非结构化Goto语句的函数表达。当我们执行Yield从协程返回的时候，需要保存的就是Continuation了。从理论研究的角度上来说Continuation即是对程序"接下来要做的事情"所进行的一种建模，从而能对之作进一步的分析。Continuation是对未来的完整描述，这对于理论分析而言是有很多方便的地方。实际上任何程序都可以通过CPS(Continuation Passing Style)类型转换为使用Continuation的形式

><https://www.cnblogs.com/riceball/archive/2008/01/19/continuation.html>
><http://www.blogjava.net/killme2008/archive/2010/03/23/316273.html>
---

<https://xie.infoq.cn/article/cef6d2931a54f85142d863db7>

《现代操作系统》《分布式系统原理与范型》《深入理解linux内核》《go程序设计语言》

赖勇浩 协程三篇之仅一篇 <http://blog.csdn.net/lanphaday/article/details/5397038>

颜开 <http://qing.blog.sina.com.cn/tj/88ca09aa33002ele.html>

go程序设计语言中文 <http://tonybai.com/2012/08/28/the-go-programming-language-tutorial-part3/>   (中文翻译定义中漏了个 并发)

go程序设计语言英文<http://go.googlecode.com/hg-history/release-branch.r60/doc/GoCourseDay3.pdf>

go语言初体验 <http://blog.dccmx.com/2011/01/go-taste/>

<https://zh.wikipedia.org/wiki/Go>

<https://zh.wikipedia.org/wiki/>进程

<https://zh.wikipedia.org/wiki/>线程

<http://stackoverflow.com/questions/1050222/concurrency-vs-parallelism-what-is-the-difference>

<http://www.infoq.com/cn/articles/knowledge-behind-goroutine>

go语言编程书评: <http://book.douban.com/review/5726587/>

为什么我认为goroutine和channel是把别的平台上类库的功能内置在语言里
  
本质上协程就是用户空间下的线程。

<http://blog.zhaojie.me/2013/04/why-channel-and-goroutine-in-golang-are-buildin-libraries-for-other-platforms.html>
  
<https://studygolang.com/articles/9611>
  
<http://www.cnblogs.com/shenguanpu/archive/2013/05/05/3060616.html>
  
<https://www.zhihu.com/question/20511233>
<https://www.zhihu.com/question/21483863>  
<https://zhuanlan.zhihu.com/p/25513336>  

### goroutine id

```go
import (
    "fmt"
    "github.com/cihub/seelog"
    "runtime"
    "strconv"
    "strings"
)

func GoroutineId() int {
    defer func() {
        if err := recover(); err != nil {
            seelog.Error("panic recover:panic info:", err)
        }
    }()

    var buf [64]byte
    n := runtime.Stack(buf[:], false)
    idField := strings.Fields(strings.TrimPrefix(string(buf[:n]), "goroutine "))[0]
    id, err := strconv.Atoi(idField)
    if err != nil {
        panic(fmt.Sprintf("cannot get goroutine id: %v", err))
    }
    return id
}


```

###
