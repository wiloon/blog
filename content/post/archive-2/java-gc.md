---
title: java, jvm GC
author: "-"
date: 2017-06-04T09:15:09+00:00
url: java/gc
categories:
  - java
tags:
  - reprint
  - GC
---
## java, jvm GC

- STW (Stop the World)
- 悬挂指针


### 查看当前使用的 GC

#### jmx

JMX 查看当前JVM使用的GC
  
MBean
  
java.lang.GarbageCollector

#### java code

输出结果跟JMX查看的结果相同.

```java
import java.lang.management.GarbageCollectorMXBean;
import java.lang.management.ManagementFactory;
import java.util.List;

public class TestGC {
    public static void main(String args[]) {
        List<GarbageCollectorMXBean> l = ManagementFactory.getGarbageCollectorMXBeans();
        for (GarbageCollectorMXBean b : l) {
            System.out.println(b.getName());
        }
    }
}

prod gc:
Copy
MarkSweepCompact
// 输出 Copy, MarkSweepCompact 代表正在使用单线程的垃圾回收器 -XX:+UseSerialGC

```

## 名词解释:

在 GC 的世界里对象指的是通过应用程序利用的数据的集合。是 GC 的基本单位。一般由头 (header) 和域 (field) 构成。
  
活动对象:能通过引用程序引用的对象就被称为活动对象。 (可以直接或间接从全局变量空间中引出的对象) 
  
非活动对象:不能通过程序引用的对象呗称为非活动对象。 (这就是被清除的目标) 
  
垃圾: Garbage (名词) ,在系统运行过程当中所产生的一些无用的对象,这些对象占据着一定的内存空间,如果长期不被释放,可能导致OOM。
  
垃圾收集器: Garbage Collector (名词) ,负责回收垃圾对象的垃圾收集器
  
垃圾回收: Garbage Collect (动词) ,垃圾收集器工作时,对垃圾进行回收

#### 年轻代 (Young Generation) 

1. 所有新生成的对象首先都是放在年轻代的。年轻代的目标就是尽可能快速的收集掉那些生命周期短的对象。
2. 新生代内存按照8:1:1的比例分为一个eden区和两个survivor(survivor0,survivor1)区。一个Eden区,两个 Survivor区(一般而言)。大部分对象在Eden区中生成。回收时先将eden区存活对象复制到一个survivor0区,然后清空eden区,当这个survivor0区也存放满了时,则将eden区和survivor0区存活对象复制到另一个survivor1区,然后清空eden和这个survivor0区,此时survivor0区是空的,然后将survivor0区和survivor1区交换,即保持survivor1区为空, 如此往复。
3. 当survivor1区不足以存放 eden和survivor0的存活对象时,就将存活对象直接存放到老年代。若是老年代也满了就会触发一次Full GC,也就是新生代、老年代都进行回收
4. 新生代发生的GC也叫做Minor GC,MinorGC发生频率比较高(不一定等Eden区满了才触发)

#### 年老代 (Tenured Gen, Old Generation) 

1. 在年轻代中经历了N次垃圾回收后仍然存活的对象,就会被放到年老代中。因此,可以认为年老代中存放的都是一些生命周期较长的对象。
2. 内存比新生代也大很多(大概比例是1:2),当老年代内存满时触发Major GC即Full GC,Full GC发生频率比较低,老年代对象存活时间比较长,存活率标记高。

#### 持久代 (Permanent Generation) 

用于存放静态文件,如Java类、方法等。持久代对垃圾回收没有显著影响,但是有些应用可能动态生成或者调用一些class,例如Hibernate 等,在这种时候需要设置一个比较大的持久代空间来存放这些运行过程中新增的类。

### 垃圾回收线程/GC线程: 

垃圾收集器工作时的线程。
  
应用程序和GC都是一种线程,以Java的main方法为例: 应用程序的线程指的是main方法的主线程,GC线程是JVM的内部线程。
  
在GC过程中,如果GC线程必须暂停应用程序线程 (用户线程) ,则发生STW(Stop the World)。当然也可以允许GC线程和应用程序线程一起运行,即GC并不会暂停应用程序的线程。
  
串行、并行、并发: 串行和并行指的是垃圾收集器工作时暂停应用程序 (发生STW) ,使用单核CPU (串行) 还是多核CPU (并行) 。
  
串行 (Serial) : 使用单核CPU串行地进行垃圾收集
  
并行 (Parallel) : 使用多CPU并行地进行垃圾收集,并行是GC线程有多个,但在运行GC线程时,用户线程是阻塞的
  
并发 (Concurrent) : 垃圾收集时不会暂停应用程序线程,大部分阶段用户线程和GC线程都在运行,我们称垃圾收集器和应用程序是并发运行的。

GC暂停/Stop The World/STW: 不管选择哪种GC算法,Stop-the-world都是不可避免的。Stop-the-world意味着从应用中停下来并进入到GC执行过程中去。一旦Stop-the-world发生,除了GC所需的线程外,其他线程都将停止工作,中断了的线程直到GC任务结束才继续它们的任务。GC调优通常就是为了改善stop-the-world的时间 (尽量减少STW对应用程序造成的暂停时间) 。

Minor GC/Majar GC/Full GC
  
Minor GC 清理的是新生代空间,因此也叫做新生代GC
  
Major GC 清理的是老年代的空间,因此也叫做老年代GC
  
Full GC 清理的是整个堆: 包括新生代、老年代空间

### 垃圾回收机制的意义

Java语言中一个显著的特点就是引入了垃圾回收机制,使c++程序员最头疼的内存管理的问题迎刃而解,它使得Java程序员在编写程序的时候不再需要考虑内存管理。由于有个垃圾回收机制,Java中的对象不再有"作用域"的概念,只有对象的引用才有"作用域"。垃圾回收可以有效的防止内存泄露,有效的使用空闲的内存。

### 垃圾回收机制中的算法

Java语言规范没有明确地说明JVM使用哪种垃圾回收算法,但是任何一种垃圾回收算法一般要做2件基本的事情:  (1) 发现无用信息对象； (2) 回收被无用对象占用的内存空间,使该空间可被程序再次使用

### 引用计数法(Reference Counting)

引用计数是垃圾收集器中的早期策略。在这种方法中,堆中每个对象实例都有一个引用计数。当一个对象被创建时,且将该对象实例分配给一个变量,该变量计数设置为1。当任何其它变量被赋值为这个对象的引用时,计数加1 (a = b,则b引用的对象实例的计数器+1) ,但当一个对象实例的某个引用超过了生命周期或者被设置为一个新值时,对象实例的引用计数器减1。任何引用计数器为0的对象实例可以被当作垃圾收集。当一个对象实例被垃圾收集时,它引用的任何对象实例的引用计数器减1。

#### 优缺点

优点: 引用计数收集器可以很快的执行,交织在程序运行中。对程序需要不被长时间打断的实时环境比较有利。
  
缺点:  无法检测出循环引用。如父对象有一个对子对象的引用,子对象反过来引用父对象。这样,他们的引用计数永远不可能为0.引用计数需要额外的开销,计数器的运算需要频繁使用内存。因为计数器需要不断被更新,所以它们不是只读的,而且不能保证线程安全。

#### 引用计数算法无法解决循环引用问题,例如: 

```java
public class Main {
    public static void main(String[] args) {
        MyObject object1 = new MyObject();
        MyObject object2 = new MyObject();
        object1.object = object2;
        object2.object = object1;
        object1 = null;
        object2 = null;
    }
}
```

最后面两句将object1和object2赋值为null,也就是说object1和object2指向的对象已经不可能再被访问,但是由于它们互相引用对方,导致它们的引用计数器都不为0,那么垃圾收集器就永远不会回收它们。

## 垃圾回收算法

JVM的分代回收算法: 根据不同代的特点(不同的对象的生命周期是不一样的)采取最适合的收集算法,老年代的特点是每次垃圾收集时只有少量对象需要被回收,新生代的特点是每次垃圾回收时都有大量的对象需要被回收。
  
不同生命周期的对象可以采取不同的回收算法,以便提高回收效率。

新生代: 由于新生代产生很多临时对象,大量对象需要进行回收,所以采用**复制**算法(Copy)是最高效的: 存活对象少,回收对象多
  
老年代: 回收的对象很少,都是经过几次标记后都不是可回收的状态转移到老年代的,所以仅有少量对象需要回收,故采用**标记清除**或者**标记整理**算法: 存活对象多,回收对象少
  
不同代的GC算法选择: 把Java堆分为新生代和老年代: 短命对象归为新生代,长命对象归为老年代。
  
少量对象存活,适合复制算法: 在新生代中,每次GC时都发现有大批对象死去,只有少量存活,那就选用复制算法,只需要付出少量存活对象的复制成本就可以完成GC。
  
大量对象存活,适合用标记-清理/标记-整理: 在老年代中,因为对象存活率高、没有额外空间对他进行分配担保,就必须使用"标记-清理"/"标记-整理"算法进行GC。
  
新生代和老年代使用不同的GC算法 (不同区中对象的存活特性不同) ,基于大多数新生对象都会在GC中被收回,新生代的GC使用复制算法
  
对象一般出生在Eden区,年轻代GC过程中,对象在2个幸存区之间移动,如果幸存区中的对象存活到适当的年龄,会被移动 (提升) 到老年代。
  
当对象在老年代死亡时,就需要更高级别的GC,更重量级的GC算法,复制算法不适用于老年代,因为没有多余的空间用于复制

JVM的新生代GC优化
  
指针碰撞 (bump-the-pointer) : Bump-the-pointer技术会跟踪在Eden上新创建的对象。由于新对象被分配在Eden空间的最上面,所以后续如果有新对象创建,只需要判断新创建对象的大小是否满足剩余的Eden空间。如果新对象满足要求,则其会被分配到Eden空间,同样位于Eden的最上面。所以当有新对象创建时,只需要判断此新对象的大小即可,因此具有更快的内存分配速度。
  
然而,在多线程环境下,将会有别样的状况。为了满足多个线程在Eden空间上创建对象时的线程安全,不可避免的会引入锁,因此随着锁竞争的开销,创建对象的性能也大打折扣。
  
线程局部分配缓冲区 (Thread-Local Allocation Buffers) : 
  
在HotSpot中正是通过TLABs解决了多线程问题。TLABs允许每个线程在Eden上有自己的小片空间,线程只能访问其自己的TLAB区域,因此bump-the-pointer能通过TLAB在不加锁的情况下完成快速的内存分配。

### 复制算法, copying算法(Copy)

优点: 没有标记和清除
  
缺点:需要额外空间
  
适用场景:新生代
  
存活对象移动: Y
  
内存碎片:N

该算法的提出是为了克服句柄的开销和解决堆碎片的垃圾回收。它开始时把堆分成 一个对象 面和多个空闲面, 程序从对象面为对象分配空间,当对象满了,基于copying算法的垃圾 收集就从根集中扫描活动对象,并将每个 活动对象复制到空闲面(使得活动对象所占的内存之间没有空闲洞),这样空闲面变成了对象面,原来的对象面变成了空闲面,程序会在新的对象面中分配内存。一种典型的基于coping算法的垃圾回收是stop-and-copy算法,它将堆分成对象面和空闲区域面,在对象面与空闲区域面的切换过程中,程序暂停执行。

### 标记清除算法(Mark Sweep GC) 或 tracing 算法(Tracing Collector)

GC 标记清除算法由标记阶段和清除阶段构成。在标记阶段会把所有的活动对象都做上标记, 然后在清除阶段会把没有标记的对象, 也就是非活动对象回收。

标记清除（Mark-Sweep）算法是最常见的垃圾收集算法，标记清除收集器是**跟踪式(Tracing)**垃圾收集器，其执行过程可以分成标记（Mark）和清除（Sweep）两个阶段：

标记阶段 — 从根对象出发查找并标记堆中所有存活的对象；
清除阶段 — 遍历堆中的全部对象，回收未被标记的垃圾对象并将回收的内存加入空闲链表；

#### 根搜索算法

根搜索算法是从离散数学中的图论引入的, 程序把所有的引用关系看作一张图, 从一个节点 GC ROOT 开始, 寻找对应的引用节点, 找到这个节点以后, 继续寻找这个节点的引用节点, 当所有的引用节点寻找完毕之后, 剩余的节点则被认为是没有被引用到的节点,即无用的节点。

java 中可作为 GC Root 的对象有
  
1. 虚拟机栈中引用的对象 (本地变量表) 
2. 方法区中静态属性引用的对象
3. 方法区中常量引用的对象
4. 本地方法栈中引用的对象 (Native对象) 

标记清除算法采用从根集合进行扫描, 对存活的对象标记, 标记清除算法不需要进行对象的移动, 并且仅对不存活的对象进行处理,在存活对象比较多的情况下极为高效, 但由于标记清除算法直接回收不存活的对象, 因此会造成内存碎片。
  
该算法最大的问题是存在大量的空间碎片, 因为回收后的空间是不连续的。在对象的堆空间分配过程中, 尤其是大对象的内存分配,不连续的内存空间的工作效率要低于连续的空间。

#### 优点

- 实现简单  
- 与保守式 GC 算法兼容
- 不需要移动对象

#### 缺点

- 碎片化严重 由上面描述的分配算法可知, 容易产生大量小的分块  
- 分配速度慢 由于空闲区块是用链表实现,分块可能都不连续, 每次分配都需要遍历空闲链表, 极端情况是需要遍历整个链表的。  
- 与写时复制技术不兼容  
- 整个过程需要标记对象的存活状态，用户程序在垃圾收集的过程中也不能执行，需要用到更复杂的机制来解决 STW 的问题。

##### 写时复制

写时复制 (copy-on-write) 是众多 UNIX 操作系统用到的内存优化的方法。比如在 Linux 系统中使用 fork() 函数复制进程时, 大部分内存空间都不会被复制, 只是复制进程, 只有在内存中内容被改变时才会复制内存数据。
  
如果使用标记清除算法, 这些内存会被设置标志位, 就会频繁发生不应该发生的复制。  

#### 三色标记, Tri-color Marking
为了解决原始标记清除算法带来的长时间 STW，多数现代的追踪式垃圾收集器都会实现三色标记算法的变种以缩短 STW 的时间。三色标记算法将程序中的对象分成白色、黑色和灰色三类4：

白色对象 — 潜在的垃圾，其内存可能会被垃圾收集器回收；
黑色对象 — 活跃的对象，包括不存在任何引用外部指针的对象以及从根对象可达的对象；
灰色对象 — 活跃的对象，因为存在指向白色对象的外部指针，垃圾收集器会扫描这些对象的子对象；

>https://draveness.me/golang/docs/part3-runtime/ch07-memory/golang-garbage-collector/
>https://juejin.cn/post/6996123086296252453

在JVM虚拟机中有两种常见垃圾回收器使用了三色标记算法：

CMS(Concurrent Mark Sweep)
G1(Garbage First)

##### 三色不变性（Tri-color invariant）

强三色不变性 — 黑色对象不会指向白色对象，只会指向灰色对象或者黑色对象；
弱三色不变性 — 黑色对象指向的白色对象必须包含一条从灰色对象经由多个白色对象的可达路径

屏障技术就是在并发或者增量标记过程中保证三色不变性的重要技术。

### 标记-整理算法 (Mark Compact)/ 标记清除-整理算法 (Mark Sweep Compact, MarkSweepCompact)

**标记-整理**算法采用**标记清除**算法一样的方式进行对象的标记,但在清除时不同,在回收不存活的对象占用的空间后,会将所有的存活对象往左端空闲空间移动,并更新对应的指针。**标记-整理**算法是在**标记清除**算法的基础上,又进行了对象的移动,因此成本更高,但是却解决了内存碎片的问题。在基于Compacting算法的收集器的实现中,一般增加句柄和句柄表。

### GC, 垃圾收集器

新生代收集器使用的收集器: Serial、Parallel Scavenge、PraNew
  
老年代收集器使用的收集器: Serial Old、Parallel Old、CMS
  
跨年轻态和旧生代的回收器: G1

如果说收集算法是内存回收的方法论,那么垃圾收集器就是内存回收的具体实现。
  
Java虚拟机规范中对垃圾收集器应该如何实现并没有任何规定,因此不同的厂商、不同版本的虚拟机所提供的垃圾收集器都可能会有很大差别,并且一般都会提供参数供用户根据自己的应用特点和要求组合出各个年代所使用的收集器。

并发和并行
  
这两个名词都是并发编程中的概念,在谈论垃圾收集器的上下文语境中,它们可以解释如下。

并行 (Parallel) : 指多条垃圾收集线程并行工作,但此时用户线程仍然处于等待状态。
  
并发 (Concurrent) : 指用户线程与垃圾收集线程同时执行 (但不一定是并行的,可能会交替执行) ,用户程序在继续运行,而垃圾收集程序运行于另一个CPU上。

Minor GC 和 Full GC
  
新生代GC (Minor GC) : 
  
指发生在新生代的垃圾收集动作,因为Java对象大多都具备朝生夕灭的特性,所以Minor GC非常频繁,一般回收速度也比较快。

老年代GC (Major GC / Full GC) : 
  
指发生在老年代的GC,出现了Major GC,经常会伴随至少一次的Minor GC (但非绝对的,在Parallel Scavenge收集器的收集策略里就有直接进行Major GC的策略选择过程) 。Major GC的速度一般会比Minor GC慢10倍以上。

Full GC
  
对整个堆进行整理,包括Young、Tenured和Perm。Full GC因为需要对整个堆进行回收,所以比Scavenge GC要慢,因此应该尽可能减少Full GC的次数。在对JVM调优的过程中,很大一部分工作就是对于FullGC的调节。有如下原因可能导致Full GC: 
  
1. 年老代 (Tenured) 被写满
  
2. 持久代 (Perm) 被写满
  
3. System.gc()被显示调用
  
4. 上一次GC之后Heap的各域分配策略动态变化

吞吐量
  
吞吐量就是CPU用于运行用户代码的时间与CPU总消耗时间的比值,即吞吐量 = 运行用户代码时间 / (运行用户代码时间 + 垃圾收集时间) 。
  
虚拟机总共运行了100分钟,其中垃圾收集花掉1分钟,那吞吐量就是99%。

## 新生代收集器

### Serial 收集器

-XX:+UseSerialGC 表示 "Serial" + "Serial Old"组合
  
算法: 复制算法(Copy)
  
Serial收集器是最基本、发展历史最悠久的收集器,曾经 (在JDK 1.3.1之前) 是虚拟机新生代收集的唯一选择。
  
将幸存对象从 Eden复制到幸存 Survivor空间,并且在幸存Survivor空间之间复制,直到它决定这些对象已经足够长了,在某个点一次性将它们复制到旧生代old generation.

特性: 
  
这个收集器是一个单线程的收集器,但它的"单线程"的意义并不仅仅说明它只会使用一个CPU或一条收集线程去完成垃圾收集工作,更重要的是在它进行垃圾收集时,必须暂停其他所有的工作线程,直到它收集结束。Stop The World

应用场景: 
  
Serial收集器是虚拟机运行在Client模式下的默认新生代收集器。

优势: 
  
简单而高效 (与其他收集器的单线程比) ,对于限定单个CPU的环境来说,Serial收集器由于没有线程交互的开销,专心做垃圾收集自然可以获得最高的单线程收集效率。

### Parallel Scavenge/PS Scavenge

Parallel Scavenge, PS Scavenge
  
-XX:+UseParallelGC (Parallel Scavenge + Serial Old)
  
新生代收集器
  
算法: 复制算法(Copy)
  
Parallel Scavenge 使用多个GC线程实现复制收集。如同上面的Serial 收集器一样,但是它是并行使用多个线程。

应用场景: 
  
停顿时间越短就越适合需要与用户交互的程序,良好的响应速度能提升用户体验,而高吞吐量则可以高效率地利用CPU时间,尽快完成程序的运算任务,主要适合在后台运算而不需要太多交互的任务。

对比分析: 

Parallel Scavenge收集器 VS CMS等收集器: 
  
Parallel Scavenge收集器的特点是它的关注点与其他收集器不同,CMS等收集器的关注点是尽可能地缩短垃圾收集时用户线程的停顿时间,而Parallel Scavenge收集器的目标则是达到一个可控制的吞吐量 (Throughput) 。
  
由于与吞吐量关系密切,Parallel Scavenge收集器也经常称为"吞吐量优先"收集器。

Parallel Scavenge收集器 VS ParNew收集器: 
  
Parallel Scavenge收集器与ParNew收集器的一个重要区别是它具有自适应调节策略。

GC自适应的调节策略: 
  
Parallel Scavenge收集器有一个参数-XX:+UseAdaptiveSizePolicy。当这个参数打开之后,就不需要手工指定新生代的大小、Eden与Survivor区的比例、晋升老年代对象年龄等细节参数了,虚拟机会根据当前系统的运行情况收集性能监控信息,动态调整这些参数以提供最合适的停顿时间或者最大的吞吐量,这种调节方式称为GC自适应的调节策略 (GC Ergonomics) 。

### ParNew 收集器

-XX:+UseParNewGC (ParNew + CMS)
  
新生代收集器
  
算法: 复制算法(Copy)
  
ParNew收集器也是Serial收集器的多线程版本,除了使用多条线程进行垃圾收集之外,其余行为包括Serial收集器可用的所有控制参数、收集算法、Stop The World、对象分配规则、回收策略等都与Serial收集器完全一样,在实现上,这两种收集器也共用了相当多的代码。

应用场景: 
  
ParNew收集器是许多运行在Server模式下的虚拟机中首选的新生代收集器。

很重要的原因是: 除了Serial收集器外,目前只有它能与CMS收集器配合工作。
  
在JDK 1.5时期,HotSpot推出了一款在强交互应用中几乎可认为有划时代意义的垃圾收集器——CMS收集器,这款收集器是HotSpot虚拟机中第一款真正意义上的并发收集器,它第一次实现了让垃圾收集线程与用户线程同时工作。
  
不幸的是,CMS作为老年代的收集器,却无法与JDK 1.4.0中已经存在的新生代收集器Parallel Scavenge配合工作,所以在JDK 1.5中使用CMS来收集老年代的时候,新生代只能选择ParNew或者Serial收集器中的一个。

Serial收集器 VS ParNew收集器: 
  
ParNew收集器在单CPU的环境中绝对不会有比Serial收集器更好的效果,甚至由于存在线程交互的开销,该收集器在通过超线程技术实现的两个CPU的环境中都不能百分之百地保证可以超越Serial收集器。
  
然而,随着可以使用的CPU的数量的增加,它对于GC时系统资源的有效利用还是很有好处的。
  
UseConcMarkSweepGC: 开启此参数使用ParNew & CMS (serial old为替补) 搜集器。
  
区别于"Parallel Scavenge"在于它与CMS可搭配使用,它也是并行使用多个线程,内部有一个回调功能允许旧生代操作它收集的对象。

### G1 Young Generation

enabled with -XX:+UseG1GC
  
the garbage first collector, uses the 'Garbage First' algorithm which splits up the heap into lots of smaller spaces, but these are still separated into Eden and Survivor spaces in the young generation for G1.

## 旧生代几种垃圾收集方式

### Serial Old收集器

-XX:+UseParallelGC (Parallel Scavenge +  Serial Old)
  
算法: MarkSweepCompact
  
Serial Old是Serial收集器的老年代版本,使用单个线程进行mark-sweep-compact(标志-清扫-压缩)

应用场景: 
  
Client模式
  
Serial Old收集器的主要意义也是在于给Client模式下的虚拟机使用。

Server模式
  
如果在Server模式下,那么它主要还有两大用途: 一种用途是在JDK 1.5以及之前的版本中与Parallel Scavenge收集器搭配使用,另一种用途就是作为CMS收集器的后备预案,在并发收集发生Concurrent Mode Failure时使用。

### Parallel Old 收集器(停止-复制算法)

-XX:+UseParallelOldGC ( Parallel Scavenge +  Parallel Old)
  
算法: MarkSweepCompact
  
Parallel Old (PS MarkSweep) 是一种使用多个GC线程压缩收集。
  
特性: 
  
Parallel Old是Parallel Scavenge收集器的老年代版本,使用多线程和"标记－整理"算法。

应用场景: 
  
在注重吞吐量以及CPU资源敏感的场合,都可以优先考虑Parallel Scavenge加Parallel Old收集器。

这个收集器是在JDK 1.6中才开始提供的,在此之前,新生代的Parallel Scavenge收集器一直处于比较尴尬的状态。原因是,如果新生代选择了Parallel Scavenge收集器,老年代除了Serial Old收集器外别无选择 (Parallel Scavenge收集器无法与CMS收集器配合工作) 。由于老年代Serial Old收集器在服务端应用性能上的"拖累",使用了Parallel Scavenge收集器也未必能在整体应用上获得吞吐量最大化的效果,由于单线程的老年代收集中无法充分利用服务器多CPU的处理能力,在老年代很大而且硬件比较高级的环境中,这种组合的吞吐量甚至还不一定有ParNew加CMS的组合"给力"。直到Parallel Old收集器出现后,"吞吐量优先"收集器终于有了比较名副其实的应用组合。

### CMS 收集器, Concurrent Mark Sweep (CMS) collector

CMS，是非常有名的JVM垃圾回收器，它起到了承上启下的作用，开启了并发回收的篇章。但是CMS由于许多小问题，现在基本已经被淘汰。
>https://juejin.cn/post/6859931488352370702

-XX:+UseConcMarkSweepGC(ParNew + CMS)
  
标记-清理算法/Mark-Sweep Collector

特性: 
  
CMS (Concurrent Mark Sweep) 收集器是一种以获取最短回收停顿时间为目标的收集器。目前很大一部分的Java应用集中在互联网站或者B/S系统的服务端上,这类应用尤其重视服务的响应速度,希望系统停顿时间最短,以给用户带来较好的体验。CMS收集器就非常符合这类应用的需求。
  
CMS收集器是基于"标记—清除"算法实现的,它的运作过程相对于前面几种收集器来说更复杂一些,整个过程分为4个步骤: 

初始标记 (CMS initial mark) 
  
初始标记仅仅只是标记一下GC Roots能直接关联到的对象,速度很快,需要"Stop The World"。

并发标记 (CMS concurrent mark) 
  
并发标记阶段就是进行GC Roots Tracing的过程。

重新标记 (CMS remark) 
  
重新标记阶段是为了修正并发标记期间因用户程序继续运作而导致标记产生变动的那一部分对象的标记记录,这个阶段的停顿时间一般会比初始标记阶段稍长一些,但远比并发标记的时间短, 仍然需要"Stop The World"

并发清除 (CMS concurrent sweep) 
  
并发清除阶段会清除对象。

由于整个过程中耗时最长的并发标记和并发清除过程收集器线程都可以与用户线程一起工作,所以,从总体上来说,CMS收集器的内存回收过程是与用户线程一起并发执行的。

优点: 
  
CMS是一款优秀的收集器,它的主要优点在名字上已经体现出来了: 并发收集、低停顿。

缺点: 
  
CMS收集器对CPU资源非常敏感
  
其实,面向并发设计的程序都对CPU资源比较敏感。在并发阶段,它虽然不会导致用户线程停顿,但是会因为占用了一部分线程 (或者说CPU资源) 而导致应用程序变慢,总吞吐量会降低。
  
CMS默认启动的回收线程数是 (CPU数量+3) / 4,也就是当CPU在4个以上时,并发回收时垃圾收集线程不少于25%的CPU资源,并且随着CPU数量的增加而下降。但是当CPU不足4个 (譬如2个) 时,CMS对用户程序的影响就可能变得很大。

CMS收集器无法处理浮动垃圾
  
CMS收集器无法处理浮动垃圾,可能出现"Concurrent Mode Failure"失败而导致另一次Full GC的产生。

由于CMS并发清理阶段用户线程还在运行着,伴随程序运行自然就还会有新的垃圾不断产生,这一部分垃圾出现在标记过程之后,CMS无法在当次收集中处理掉它们,只好留待下一次GC时再清理掉。这一部分垃圾就称为"浮动垃圾"。
  
也是由于在垃圾收集阶段用户线程还需要运行,那也就还需要预留有足够的内存空间给用户线程使用,因此CMS收集器不能像其他收集器那样等到老年代几乎完全被填满了再进行收集,需要预留一部分空间提供并发收集时的程序运作使用。要是CMS运行期间预留的内存无法满足程序需要,就会出现一次"Concurrent Mode Failure"失败,这时虚拟机将启动后备预案: 临时启用Serial Old收集器来重新进行老年代的垃圾收集,这样停顿时间就很长了。

CMS收集器会产生大量空间碎片
  
CMS是一款基于"标记—清除"算法实现的收集器,这意味着收集结束时会有大量空间碎片产生。

空间碎片过多时,将会给大对象分配带来很大麻烦,往往会出现老年代还有很大空间剩余,但是无法找到足够大的连续空间来分配当前对象,不得不提前触发一次Full GC。

### G1收集器

-XX:+UseG1GC
  
G1更推荐在至少6G的堆上使用

特性: 
  
G1 (Garbage-First) 是一款面向服务端应用的垃圾收集器。HotSpot开发团队赋予它的使命是未来可以替换掉JDK 1.5中发布的CMS收集器。与其他GC收集器相比,G1具备如下特点。

并行与并发
  
G1能充分利用多CPU、多核环境下的硬件优势,使用多个CPU来缩短Stop-The-World停顿的时间,部分其他收集器原本需要停顿Java线程执行的GC动作,G1收集器仍然可以通过并发的方式让Java程序继续执行。

分代收集
  
与其他收集器一样,分代概念在G1中依然得以保留。虽然G1可以不需要其他收集器配合就能独立管理整个GC堆,但它能够采用不同的方式去处理新创建的对象和已经存活了一段时间、熬过多次GC的旧对象以获取更好的收集效果。

空间整合
  
与CMS的"标记—清理"算法不同,G1从整体来看是基于"标记—整理"算法实现的收集器,从局部 (两个Region之间) 上来看是基于"复制"算法实现的,但无论如何,这两种算法都意味着G1运作期间不会产生内存空间碎片,收集后能提供规整的可用内存。这种特性有利于程序长时间运行,分配大对象时不会因为无法找到连续内存空间而提前触发下一次GC。

可预测的停顿
  
这是G1相对于CMS的另一大优势,降低停顿时间是G1和CMS共同的关注点,但G1除了追求低停顿外,还能建立可预测的停顿时间模型,能让使用者明确指定在一个长度为M毫秒的时间片段内,消耗在垃圾收集上的时间不得超过N毫秒。

在G1之前的其他收集器进行收集的范围都是整个新生代或者老年代,而G1不再是这样。使用G1收集器时,Java堆的内存布局就与其他收集器有很大差别,它将整个Java堆划分为多个大小相等的独立区域 (Region) ,虽然还保留有新生代和老年代的概念,但新生代和老年代不再是物理隔离的了,它们都是一部分Region (不需要连续) 的集合。

G1收集器之所以能建立可预测的停顿时间模型,是因为它可以有计划地避免在整个Java堆中进行全区域的垃圾收集。G1跟踪各个Region里面的垃圾堆积的价值大小 (回收所获得的空间大小以及回收所需时间的经验值) ,在后台维护一个优先列表,每次根据允许的收集时间,优先回收价值最大的Region (这也就是Garbage-First名称的来由) 。这种使用Region划分内存空间以及有优先级的区域回收方式,保证了G1收集器在有限的时间内可以获取尽可能高的收集效率。

执行过程: 
  
G1收集器的运作大致可划分为以下几个步骤: 

初始标记 (Initial Marking) 
  
初始标记阶段仅仅只是标记一下GC Roots能直接关联到的对象,并且修改TAMS (Next Top at Mark Start) 的值,让下一阶段用户程序并发运行时,能在正确可用的Region中创建新对象,这阶段需要停顿线程,但耗时很短。

并发标记 (Concurrent Marking) 
  
并发标记阶段是从GC Root开始对堆中对象进行可达性分析,找出存活的对象,这阶段耗时较长,但可与用户程序并发执行。

最终标记 (Final Marking) 
  
最终标记阶段是为了修正在并发标记期间因用户程序继续运作而导致标记产生变动的那一部分标记记录,虚拟机将这段时间对象变化记录在线程Remembered Set Logs里面,最终标记阶段需要把Remembered Set Logs的数据合并到Remembered Set中,这阶段需要停顿线程,但是可并行执行。

筛选回收 (Live Data Counting and Evacuation) 
  
筛选回收阶段首先对各个Region的回收价值和成本进行排序,根据用户所期望的GC停顿时间来制定回收计划,这个阶段其实也可以做到与用户程序一起并发执行,但是因为只回收一部分Region,时间是用户可控制的,而且停顿用户线程将大幅提高收集效率。

### 总结

虽然我们是在对各个收集器进行比较,但并非为了挑选出一个最好的收集器。因为直到现在为止还没有最好的收集器出现,更加没有万能的收集器,所以我们选择的只是对具体应用最合适的收集器。这点不需要多加解释就能证明: 如果有一种放之四海皆准、任何场景下都适用的完美收集器存在,那HotSpot虚拟机就没必要实现那么多不同的收集器了。

-XX:+ScavengeBeforeFullGC
  
Do young generation GC prior to a full GC. (Introduced in 1.4.1.)
  
在执行FullGC之前执行MinorGC,VM会分2次停顿,可以缩短最大停顿时间

http://www.jianshu.com/p/50d5c88b272d
  
http://www.cnblogs.com/sunniest/p/4575144.html
  
http://www.infoq.com/cn/news/2017/03/garbage-collection-algorithm

- Visualizing Garbage Collection Algorithms
>https://spin.atomicobject.com/2014/09/03/visualizing-garbage-collection-algorithms/embed/#?secret=w2JRHHSugP
  
https://www.ibm.com/developerworks/cn/java/j-lo-JVMGarbageCollection/index.html
  
https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/collectors.html
  
http://www.oracle.com/technetwork/systems/vmoptions-jsp-140102.html
  
http://zqhxuyuan.github.io/2016/07/26/JVM/
  
https://juejin.im/post/5b546bc9f265da0f8f203968
  
https://www.cnblogs.com/woshimrf/p/jvm-garbage.html

### 悬挂指针

本来不应该被回收的对象却被回收了，这在内存管理中是非常严重的错误，我们将这种错误称为悬挂指针，即指针没有指向特定类型的合法对象，影响了内存的安全性5，想要并发或者增量地标记对象还是需要使用屏障技术。
>https://draveness.me/golang/docs/part3-runtime/ch07-memory/golang-garbage-collector/

### STW (Stop the World)

传统的垃圾收集算法会在垃圾收集的执行期间暂停应用程序，一旦触发垃圾收集，垃圾收集器会抢占 CPU 的使用权占据大量的计算资源以完成标记和清除工作，然而很多追求实时的应用程序无法接受长时间的 STW。
