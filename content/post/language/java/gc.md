---
title: Java GC
author: "-"
date: 2017-06-04T09:15:09+00:00
lastmod: 2026-07-14T06:14:08+08:00
url: gc
categories:
  - Java
tags:
  - GC
  - remix
  - AI-assisted
---

## 分代模型

### 名词解释

在 GC 的世界里，对象指的是通过应用程序利用的数据的集合，是 GC 的基本单位，一般由头（header）和域（field）构成。

- 活动对象：能通过引用程序引用的对象，即可以直接或间接从全局变量空间中引出的对象
- 非活动对象：不能通过程序引用的对象，即被清除的目标
- 垃圾（Garbage）：系统运行过程中产生的无用对象，这些对象占据一定的内存空间，如果长期不被释放，可能导致 OOM
- 垃圾收集器（Garbage Collector）：负责回收垃圾对象的组件
- 垃圾回收（Garbage Collect）：垃圾收集器工作时对垃圾进行回收的动作

### 新生代（Young Generation）

1. 所有新生成的对象首先都放在新生代，新生代的目标是尽可能快速地收集掉那些生命周期短的对象。
2. 新生代内存按照 8:1:1 的比例分为一个 Eden 区和两个 Survivor 区（Survivor0、Survivor1）。大部分对象在 Eden 区中生成。回收时先将 Eden 区存活对象复制到 Survivor0 区，然后清空 Eden 区；当 Survivor0 区也存放满时，则将 Eden 区和 Survivor0 区的存活对象复制到 Survivor1 区，然后清空 Eden 区和 Survivor0 区，此时 Survivor0 区为空，再将 Survivor0 区和 Survivor1 区角色互换，如此往复。
3. 当 Survivor1 区不足以存放 Eden 区和 Survivor0 区的存活对象时，就将存活对象直接存放到老年代。若老年代也满了，就会触发一次 Full GC，即新生代、老年代都进行回收。
4. 新生代发生的 GC 也叫 Minor GC，发生频率比较高（不一定要等 Eden 区满了才触发）。

### 老年代（Tenured Gen，Old Generation）

1. 在新生代中经历了 N 次垃圾回收后仍然存活的对象，会被放到老年代中，因此老年代中存放的都是生命周期较长的对象。
2. 老年代内存比新生代大很多（大概比例是 1:2），当老年代内存满时触发 Major GC 即 Full GC。Full GC 发生频率比较低，因为老年代对象存活时间长、存活率高。

### 持久代（Permanent Generation）与 Metaspace

持久代用于存放静态文件，如 Java 类、方法等。持久代对垃圾回收没有显著影响，但有些应用可能动态生成或调用一些 class（例如 Hibernate），这种情况下需要设置一个比较大的持久代空间来存放运行过程中新增的类。

需要注意的是，持久代（PermGen）是 JDK 7 及之前的实现；JDK 8 起 HotSpot 已将其移除，替换为 Metaspace，Metaspace 使用本地内存而非堆内存，不再受 `-XX:MaxPermSize` 限制。

### 新生代 / 老年代对应哪些收集器

新生代、老年代是堆的分代划分，本身是一个通用概念，并不绑定某一种具体的垃圾收集器；HotSpot 里大多数收集器都是围绕这个模型工作的，但组合方式不同：

- 新生代收集器：Serial、ParNew、Parallel Scavenge（均采用复制算法）
- 老年代收集器：Serial Old、Parallel Old、CMS（均采用标记清除或标记整理算法）
- 跨代收集器：G1 用 Region 同时管理新生代和老年代，逻辑上仍保留新生代 / 老年代的概念，但物理上不再是两块连续的内存区域
- 非分代收集器：ZGC、Shenandoah 不区分新生代和老年代，对整个堆做并发标记整理（JDK 21 起 ZGC 也提供了分代版本，行为向传统分代模型靠拢）

具体每种收集器的算法与适用场景见下文「垃圾回收算法」与「垃圾收集器」两节。

## 核心概念

### STW（Stop the World）

传统的垃圾收集算法会在垃圾收集的执行期间暂停应用程序：一旦触发垃圾收集，垃圾收集器会抢占 CPU 使用权，占据大量计算资源以完成标记和清除工作，但很多追求实时性的应用程序无法接受长时间的 STW。

不管选择哪种 GC 算法，STW 都不可避免。STW 意味着应用从正常运行状态停下来进入 GC 执行过程：一旦 STW 发生，除了 GC 所需的线程外，其他线程都将停止工作，直到 GC 任务结束才继续。GC 调优通常就是为了改善 STW 的时间，尽量减少 STW 对应用程序造成的暂停时间。

垃圾收集线程是垃圾收集器工作时的线程；应用程序和 GC 都是一种线程，以 Java 的 `main` 方法为例，应用程序的线程指的是 `main` 方法的主线程，GC 线程是 JVM 的内部线程。在 GC 过程中，如果 GC 线程必须暂停应用程序线程（用户线程），则发生 STW；也可以允许 GC 线程和应用程序线程一起运行，即 GC 并不暂停应用程序线程。

### 串行、并行、并发

串行和并行指的是垃圾收集器工作时暂停应用程序（发生 STW），使用单核 CPU（串行）还是多核 CPU（并行）：

- 串行（Serial）：使用单核 CPU 串行地进行垃圾收集
- 并行（Parallel）：使用多核 CPU 并行地进行垃圾收集；并行是指 GC 线程有多个，但运行 GC 线程时用户线程是阻塞的
- 并发（Concurrent）：垃圾收集时不会暂停应用程序线程，大部分阶段用户线程和 GC 线程都在运行，也就是垃圾收集器和应用程序并发运行

### Minor GC / Major GC / Full GC

新生代 GC（Minor GC）：指发生在新生代的垃圾收集动作。因为 Java 对象大多具备朝生夕灭的特性，所以 Minor GC 非常频繁，一般回收速度也比较快。

老年代 GC（Major GC / Full GC）：指发生在老年代的 GC。出现 Major GC 时经常会伴随至少一次 Minor GC（但非绝对，Parallel Scavenge 收集器的收集策略里就有直接进行 Major GC 的策略选择过程）。Major GC 的速度一般会比 Minor GC 慢 10 倍以上。

Full GC 是对整个堆（包括 Young、Tenured 和 Perm）进行整理。因为需要对整个堆进行回收，所以比 Minor GC 要慢，应该尽可能减少 Full GC 的次数；JVM 调优很大一部分工作就是对 Full GC 的调节。可能触发 Full GC 的原因有：

1. 老年代（Tenured）被写满
2. 持久代（Perm）被写满
3. `System.gc()` 被显式调用
4. 上一次 GC 之后堆的各域分配策略发生动态变化

### 吞吐量

吞吐量就是 CPU 用于运行用户代码的时间与 CPU 总消耗时间的比值，即 `吞吐量 = 运行用户代码时间 / (运行用户代码时间 + 垃圾收集时间)`。例如虚拟机总共运行了 100 分钟，其中垃圾收集花掉 1 分钟，那吞吐量就是 99%。

### 悬挂指针

本来不应该被回收的对象却被回收了，这在内存管理中是非常严重的错误，称为悬挂指针，即指针没有指向特定类型的合法对象，影响了内存的安全性。想要并发或者增量地标记对象，还是需要使用屏障技术。

> <https://draveness.me/golang/docs/part3-runtime/ch07-memory/golang-garbage-collector/>

## 垃圾回收机制的意义

Java 语言的一个显著特点是引入了垃圾回收机制，使 C++ 程序员最头疼的内存管理问题迎刃而解，Java 程序员在编写程序时不再需要考虑内存管理。由于有垃圾回收机制，Java 中的对象不再有“作用域”的概念，只有对象的引用才有“作用域”。垃圾回收可以有效防止内存泄漏，有效使用空闲内存。

Java 语言规范没有明确说明 JVM 使用哪种垃圾回收算法，但任何一种垃圾回收算法一般要做两件基本的事情：（1）发现无用对象；（2）回收被无用对象占用的内存空间，使该空间可被程序再次使用。

## 垃圾回收算法

### 引用计数法（Reference Counting）

引用计数是垃圾收集器中的早期策略。这种方法中，堆中每个对象实例都有一个引用计数：对象被创建并赋值给一个变量时，计数设置为 1；任何其它变量被赋值为这个对象的引用时，计数加 1（`a = b`，则 `b` 引用的对象实例的计数器加 1）；但当一个对象实例的某个引用超过了生命周期或被设置为一个新值时，对象实例的引用计数器减 1。任何引用计数器为 0 的对象实例可以被当作垃圾收集；一个对象实例被垃圾收集时，它引用的任何对象实例的引用计数器也减 1。

优点：引用计数收集器可以很快地执行，交织在程序运行中，对不能被长时间打断的实时环境比较有利。

缺点：无法检测出循环引用。如父对象有一个对子对象的引用，子对象反过来引用父对象，它们的引用计数永远不可能为 0。此外引用计数需要额外开销，计数器的运算需要频繁访问内存，因为计数器需要不断被更新，所以它们不是只读的，也不能保证线程安全。

引用计数算法无法解决循环引用问题，例如：

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

最后两句将 `object1` 和 `object2` 赋值为 `null`，也就是说它们指向的对象已经不可能再被访问，但由于两者互相引用对方，导致引用计数器都不为 0，垃圾收集器就永远不会回收它们。

### 分代回收的算法选择

JVM 的分代回收算法：根据不同代的特点（不同对象的生命周期不一样）采取最适合的收集算法。老年代的特点是每次垃圾收集时只有少量对象需要回收，新生代的特点是每次垃圾回收时都有大量对象需要回收，不同生命周期的对象采取不同的回收算法可以提高回收效率：

- 新生代：由于新生代产生大量临时对象，存活对象少、回收对象多，采用**复制算法**（Copy）最高效
- 老年代：经过几次标记后仍未被回收才转移到老年代的对象，存活率高、回收对象少，采用**标记清除**或**标记整理**算法

对象一般出生在 Eden 区，新生代 GC 过程中对象在两个 Survivor 区之间移动，如果 Survivor 区中的对象存活到适当的年龄，会被晋升到老年代。当对象在老年代死亡时，就需要更高级别、更重量级的 GC 算法，复制算法不适用于老年代，因为老年代没有多余的空间用于复制。

新生代 GC 还有两项常见优化：

- 指针碰撞（bump-the-pointer）：跟踪 Eden 上新创建的对象。由于新对象总是分配在 Eden 空间已用区域的最上面，后续创建新对象时只需要判断其大小是否满足剩余 Eden 空间即可，因此具有更快的内存分配速度。但在多线程环境下，为了保证多个线程在 Eden 空间上创建对象时的线程安全，不可避免要引入锁，锁竞争的开销会拖累对象创建的性能。
- 线程本地分配缓冲区（TLAB，Thread-Local Allocation Buffer）：HotSpot 通过 TLAB 解决了上述多线程问题，允许每个线程在 Eden 上拥有自己的小片空间，线程只能访问自己的 TLAB 区域，因此指针碰撞技术能在不加锁的情况下通过 TLAB 完成快速的内存分配。

### 复制算法（Copying）

- 适用场景：新生代
- 优点：没有标记和清除阶段
- 缺点：需要额外空间
- 存活对象移动：是
- 内存碎片：无

该算法的提出是为了克服句柄的开销和解决堆碎片问题。开始时把堆分成一个对象面和多个空闲面，程序从对象面为对象分配空间；当对象面满了，基于复制算法的垃圾收集就从根集合扫描活动对象，并将每个活动对象复制到空闲面（使活动对象所占的内存之间没有空闲洞），这样空闲面变成了对象面，原来的对象面变成了空闲面，程序会在新的对象面中分配内存。一种典型的基于复制算法的垃圾回收是 stop-and-copy 算法，它将堆分成对象面和空闲区域面，在两者切换的过程中程序暂停执行。

### 标记清除算法（Mark-Sweep）

GC 标记清除算法由标记阶段和清除阶段构成：标记阶段会把所有的活动对象都标记出来，然后在清除阶段回收没有被标记的非活动对象。

标记清除算法是最常见的垃圾收集算法之一，是**跟踪式（Tracing）**垃圾收集器，执行过程分成两个阶段：

- 标记阶段：从根对象出发查找并标记堆中所有存活的对象
- 清除阶段：遍历堆中的全部对象，回收未被标记的垃圾对象并将回收的内存加入空闲链表

#### 根搜索算法

根搜索算法是从离散数学中的图论引入的：程序把所有的引用关系看作一张图，从一个节点 GC Root 开始，寻找对应的引用节点，找到之后继续寻找这个节点的引用节点，当所有引用节点都寻找完毕后，剩余的节点则被认为是没有被引用到的节点，即无用节点。

Java 中可作为 GC Root 的对象有：

1. 虚拟机栈中引用的对象（本地变量表）
2. 方法区中静态属性引用的对象
3. 方法区中常量引用的对象
4. 本地方法栈中引用的对象（Native 对象）

标记清除算法采用从根集合进行扫描、对存活对象标记的方式，不需要移动对象，仅对不存活的对象进行处理，在存活对象比较多的情况下效率很高，但由于直接回收不存活的对象，会造成内存碎片。该算法最大的问题是存在大量的空间碎片，因为回收后的空间是不连续的；在对象的堆空间分配过程中，尤其是大对象的内存分配，不连续的内存空间的工作效率要低于连续的空间。

**优点：**

- 实现简单
- 与保守式 GC 算法兼容
- 不需要移动对象

**缺点：**

- 碎片化严重：由上面描述的分配方式可知，容易产生大量小的分块
- 分配速度慢：空闲区块用链表实现，分块可能都不连续，每次分配都需要遍历空闲链表，极端情况需要遍历整个链表
- 与写时复制技术不兼容
- 整个过程需要标记对象的存活状态，用户程序在垃圾收集过程中不能执行，需要更复杂的机制来解决 STW 问题

#### 写时复制

写时复制（copy-on-write）是众多 UNIX 操作系统用到的内存优化方法，比如 Linux 系统中使用 `fork()` 函数复制进程时，大部分内存空间都不会被复制，只是复制进程，只有内存中内容被改变时才会复制内存数据。如果使用标记清除算法，这些内存会被设置标志位，就会频繁发生不应该发生的复制。

#### 三色标记（Tri-color Marking）

为了解决原始标记清除算法带来的长时间 STW，多数现代的追踪式垃圾收集器都会实现三色标记算法的变种以缩短 STW 的时间。三色标记算法将程序中的对象分成白色、黑色和灰色三类：

- 白色对象：潜在的垃圾，其内存可能会被垃圾收集器回收
- 黑色对象：活跃的对象，包括不存在任何引用外部指针的对象以及从根对象可达的对象
- 灰色对象：活跃的对象，因为存在指向白色对象的外部指针，垃圾收集器会扫描这些对象的子对象

> <https://draveness.me/golang/docs/part3-runtime/ch07-memory/golang-garbage-collector/>
>
> <https://juejin.cn/post/6996123086296252453>

在 JVM 中，CMS（Concurrent Mark Sweep）和 G1（Garbage First）是两种常见的使用了三色标记算法的垃圾收集器。

#### 三色不变性（Tri-color invariant）

- 强三色不变性：黑色对象不会指向白色对象，只会指向灰色对象或黑色对象
- 弱三色不变性：黑色对象指向的白色对象必须包含一条从灰色对象经由多个白色对象的可达路径

屏障技术就是在并发或增量标记过程中保证三色不变性的重要技术。

### 标记整理算法（Mark-Compact）

标记整理算法（也称标记清除-整理算法，MarkSweepCompact）采用与标记清除算法一样的方式进行对象标记，但在清除时不同：在回收不存活对象占用的空间后，会将所有存活对象往内存空间的一端移动，并更新对应的指针。标记整理算法是在标记清除算法的基础上又进行了对象的移动，因此成本更高，但解决了内存碎片的问题。基于该算法的收集器实现中，一般会增加句柄和句柄表。

## 垃圾收集器

如果说收集算法是内存回收的方法论，那么垃圾收集器就是内存回收的具体实现。Java 虚拟机规范对垃圾收集器应该如何实现并没有任何规定，因此不同厂商、不同版本的虚拟机所提供的垃圾收集器可能会有很大差别，一般都会提供参数供用户根据应用特点和要求组合出各个年代所使用的收集器。

- 新生代收集器：Serial、Parallel Scavenge、ParNew
- 老年代收集器：Serial Old、Parallel Old、CMS
- 跨新生代和老年代的收集器：G1

在谈论垃圾收集器的上下文中，并行（Parallel）指多条垃圾收集线程并行工作，但此时用户线程仍处于等待状态；并发（Concurrent）指用户线程与垃圾收集线程同时执行（但不一定是并行的，可能会交替执行），用户程序继续运行，垃圾收集程序运行于另一个 CPU 上。

### 新生代收集器

#### Serial

`-XX:+UseSerialGC` 表示 "Serial" + "Serial Old" 组合，算法为复制算法（Copy）。

Serial 收集器是最基本、发展历史最悠久的收集器，曾经（在 JDK 1.3.1 之前）是虚拟机新生代收集的唯一选择。它将幸存对象从 Eden 复制到 Survivor 空间，并在 Survivor 空间之间复制，直到判定这些对象已经存活足够长的时间，在某个点一次性将它们复制到老年代。

这个收集器是单线程的，且这个“单线程”不仅意味着只会使用一个 CPU 或一条收集线程完成垃圾收集工作，更重要的是在它进行垃圾收集时，必须暂停其他所有工作线程直到收集结束，即 STW。

应用场景：Serial 收集器是虚拟机运行在 Client 模式下的默认新生代收集器。

优势：简单而高效（与其他收集器的单线程实现相比）。对于限定单核 CPU 的环境来说，Serial 收集器由于没有线程交互的开销，专心做垃圾收集自然可以获得最高的单线程收集效率。

#### ParNew

`-XX:+UseParNewGC`（ParNew + CMS），新生代收集器，算法为复制算法（Copy）。

ParNew 收集器是 Serial 收集器的多线程版本，除了使用多条线程进行垃圾收集外，其余行为，包括可用的所有控制参数、收集算法、STW、对象分配规则、回收策略等都与 Serial 收集器完全一样，在实现上两者也共用了相当多的代码。

应用场景：ParNew 收集器是许多运行在 Server 模式下的虚拟机中首选的新生代收集器，很重要的原因是除了 Serial 收集器外，目前只有它能与 CMS 收集器配合工作。JDK 1.5 时期，HotSpot 推出了在强交互应用中具有划时代意义的垃圾收集器 CMS，这是 HotSpot 虚拟机中第一款真正意义上的并发收集器，第一次实现了让垃圾收集线程与用户线程同时工作。不幸的是，CMS 作为老年代的收集器却无法与 JDK 1.4.0 中已经存在的新生代收集器 Parallel Scavenge 配合工作，所以在 JDK 1.5 中使用 CMS 收集老年代时，新生代只能选择 ParNew 或 Serial 收集器中的一个。

ParNew 收集器在单 CPU 环境中绝对不会有比 Serial 收集器更好的效果，甚至由于存在线程交互的开销，该收集器在通过超线程技术实现的两个 CPU 的环境中都不能百分之百保证超越 Serial 收集器；但随着可用 CPU 数量的增加，它对于 GC 时系统资源的有效利用还是很有好处的。

`-XX:+UseConcMarkSweepGC` 开启此参数使用 ParNew & CMS（Serial Old 为替补）组合。它区别于 Parallel Scavenge 的地方在于可以与 CMS 搭配使用，也是并行使用多个线程，内部有一个回调功能允许老年代操作它收集的对象。

#### Parallel Scavenge

`-XX:+UseParallelGC`（Parallel Scavenge + Serial Old），新生代收集器，算法为复制算法（Copy）。

Parallel Scavenge 使用多个 GC 线程实现复制收集，行为与 Serial 收集器类似，但是并行使用多个线程。

应用场景：停顿时间越短越适合需要与用户交互的程序，良好的响应速度能提升用户体验；而高吞吐量则可以高效利用 CPU 时间，尽快完成程序的运算任务，主要适合在后台运算而不需要太多交互的任务。

对比 CMS 等收集器：Parallel Scavenge 收集器的关注点与其他收集器不同，CMS 等收集器的关注点是尽可能缩短垃圾收集时用户线程的停顿时间，而 Parallel Scavenge 收集器的目标则是达到一个可控制的吞吐量（Throughput）。由于与吞吐量关系密切，Parallel Scavenge 收集器也常被称为“吞吐量优先”收集器。

对比 ParNew 收集器：两者的一个重要区别是 Parallel Scavenge 收集器具有自适应调节策略，即 `-XX:+UseAdaptiveSizePolicy`。开启这个参数后，就不需要手工指定新生代大小、Eden 与 Survivor 区比例、晋升老年代对象年龄等细节参数了，虚拟机会根据当前系统运行情况收集性能监控信息，动态调整参数以提供最合适的停顿时间或最大吞吐量，这种调节方式称为 GC 自适应调节策略（GC Ergonomics）。

#### G1 的新生代

`-XX:+UseG1GC` 启用。G1（Garbage-First）使用 “Garbage First” 算法将堆划分成许多更小的空间，这些空间在 G1 的新生代中仍然被分为 Eden 区和 Survivor 区。

### 老年代收集器

#### Serial Old

`-XX:+UseParallelGC`（Parallel Scavenge + Serial Old），算法为 MarkSweepCompact。

Serial Old 是 Serial 收集器的老年代版本，使用单线程进行标记-清除-压缩（mark-sweep-compact）。

应用场景：Client 模式下主要给虚拟机使用；Server 模式下有两大用途，一是在 JDK 1.5 及之前的版本中与 Parallel Scavenge 收集器搭配使用，二是作为 CMS 收集器的后备预案，在并发收集发生 Concurrent Mode Failure 时使用。

#### Parallel Old

`-XX:+UseParallelOldGC`（Parallel Scavenge + Parallel Old），算法为 MarkSweepCompact。

Parallel Old（PS MarkSweep）是 Parallel Scavenge 收集器的老年代版本，使用多个 GC 线程和“标记-整理”算法进行压缩收集。

应用场景：在注重吞吐量以及 CPU 资源敏感的场合，都可以优先考虑 Parallel Scavenge 加 Parallel Old 收集器组合。这个收集器是在 JDK 1.6 中才开始提供的，在此之前，如果新生代选择了 Parallel Scavenge 收集器，老年代除了 Serial Old 收集器外别无选择（Parallel Scavenge 无法与 CMS 配合工作）。由于 Serial Old 收集器在服务端应用性能上的拖累，即使使用了 Parallel Scavenge 收集器，也未必能在整体应用上获得吞吐量最大化的效果——单线程的老年代收集无法充分利用服务器多 CPU 的处理能力，在老年代很大且硬件比较高级的环境中，这种组合的吞吐量甚至不一定比 ParNew 加 CMS 的组合更好。直到 Parallel Old 收集器出现后，“吞吐量优先”收集器才有了比较名副其实的应用组合。

#### CMS（Concurrent Mark Sweep）

CMS 是非常有名的 JVM 垃圾回收器，起到了承上启下的作用，开启了并发回收的篇章，但由于许多小问题，现在基本已经被淘汰。

> <https://juejin.cn/post/6859931488352370702>

`-XX:+UseConcMarkSweepGC`（ParNew + CMS），算法为标记-清除（Mark-Sweep）。

CMS 收集器是一种以获取最短回收停顿时间为目标的收集器。目前很大一部分 Java 应用集中在互联网站或 B/S 系统的服务端上，这类应用尤其重视服务的响应速度，希望系统停顿时间最短，CMS 收集器就非常符合这类应用的需求。

CMS 收集器基于“标记-清除”算法实现，整个过程分为 4 个步骤：

1. 初始标记（CMS initial mark）：仅仅标记一下 GC Roots 能直接关联到的对象，速度很快，需要 STW
2. 并发标记（CMS concurrent mark）：进行 GC Roots Tracing 的过程
3. 重新标记（CMS remark）：修正并发标记期间因用户程序继续运作而导致标记产生变动的那部分对象的标记记录，这个阶段的停顿时间一般会比初始标记阶段稍长，但远比并发标记的时间短，仍然需要 STW
4. 并发清除（CMS concurrent sweep）：清除对象

由于耗时最长的并发标记和并发清除过程中收集器线程都可以与用户线程一起工作，从总体上说，CMS 收集器的内存回收过程是与用户线程并发执行的。

**优点：** CMS 是一款优秀的收集器，主要优点在名字上已经体现出来了——并发收集、低停顿。

**缺点：**

- CMS 收集器对 CPU 资源非常敏感：面向并发设计的程序普遍对 CPU 资源比较敏感，在并发阶段虽然不会导致用户线程停顿，但会因为占用一部分 CPU 资源而导致应用程序变慢，总吞吐量降低。CMS 默认启动的回收线程数是 `(CPU 数量 + 3) / 4`，也就是当 CPU 在 4 个以上时，并发回收时垃圾收集线程占用不少于 25% 的 CPU 资源，并随着 CPU 数量增加而下降；但当 CPU 不足 4 个（例如 2 个）时，CMS 对用户程序的影响就可能变得很大。
- CMS 收集器无法处理浮动垃圾：由于 CMS 并发清理阶段用户线程还在运行，伴随程序运行自然还会产生新的垃圾，这部分垃圾出现在标记过程之后，CMS 无法在当次收集中处理掉，只能留待下一次 GC 清理，称为“浮动垃圾”。同时因为垃圾收集阶段用户线程还需要运行，需要预留足够的内存空间给用户线程使用，因此 CMS 收集器不能像其他收集器那样等到老年代几乎完全填满再进行收集，需要预留一部分空间供并发收集时的程序运作使用。如果 CMS 运行期间预留的内存无法满足程序需要，就会出现一次 Concurrent Mode Failure，这时虚拟机将启动后备预案，临时启用 Serial Old 收集器重新进行老年代的垃圾收集，停顿时间就会变得很长。
- CMS 收集器会产生大量空间碎片：CMS 基于“标记-清除”算法实现，意味着收集结束时会有大量空间碎片产生。空间碎片过多时会给大对象分配带来很大麻烦，往往会出现老年代还有很大空间剩余，但无法找到足够大的连续空间来分配当前对象，不得不提前触发一次 Full GC。

### 跨代收集器：G1

`-XX:+UseG1GC` 启用，G1 更推荐在至少 6G 的堆上使用。

G1（Garbage-First）是一款面向服务端应用的垃圾收集器，HotSpot 开发团队赋予它的使命是替换掉 JDK 1.5 中发布的 CMS 收集器。与其他 GC 收集器相比，G1 具备如下特点：

- **并行与并发**：G1 能充分利用多 CPU、多核环境下的硬件优势，使用多个 CPU 缩短 STW 停顿的时间；部分其他收集器原本需要停顿 Java 线程执行的 GC 动作，G1 收集器仍然可以通过并发的方式让 Java 程序继续执行。
- **分代收集**：与其他收集器一样，分代概念在 G1 中依然得以保留。虽然 G1 不需要其他收集器配合就能独立管理整个 GC 堆，但它能够采用不同的方式处理新创建的对象和已经存活了一段时间、熬过多次 GC 的旧对象，以获取更好的收集效果。
- **空间整合**：与 CMS 的“标记-清除”算法不同，G1 从整体来看是基于“标记-整理”算法实现的收集器，从局部（两个 Region 之间）来看是基于“复制”算法实现的；无论如何，这两种算法都意味着 G1 运作期间不会产生内存空间碎片，收集后能提供规整的可用内存，这种特性有利于程序长时间运行，分配大对象时不会因无法找到连续内存空间而提前触发下一次 GC。
- **可预测的停顿**：这是 G1 相对于 CMS 的另一大优势。降低停顿时间是 G1 和 CMS 共同的关注点，但 G1 除了追求低停顿外，还能建立可预测的停顿时间模型，能让使用者明确指定在一个长度为 M 毫秒的时间片段内，消耗在垃圾收集上的时间不得超过 N 毫秒。

在 G1 之前的其他收集器进行收集的范围都是整个新生代或者老年代，而 G1 不再是这样。使用 G1 收集器时，Java 堆的内存布局与其他收集器有很大差别：它将整个 Java 堆划分为多个大小相等的独立区域（Region），虽然还保留新生代和老年代的概念，但两者不再是物理隔离的了，它们都是一部分 Region（不需要连续）的集合。

G1 收集器之所以能建立可预测的停顿时间模型，是因为它可以有计划地避免在整个 Java 堆中进行全区域的垃圾收集。G1 跟踪各个 Region 里面垃圾堆积的价值大小（回收所获得的空间大小以及回收所需时间的经验值），在后台维护一个优先列表，每次根据允许的收集时间，优先回收价值最大的 Region（这也是 Garbage-First 名称的由来）。这种使用 Region 划分内存空间以及有优先级的区域回收方式，保证了 G1 收集器在有限的时间内可以获取尽可能高的收集效率。

G1 收集器的运作大致可划分为以下几个步骤：

1. **初始标记（Initial Marking）**：仅仅标记一下 GC Roots 能直接关联到的对象，并且修改 TAMS（Next Top at Mark Start）的值，让下一阶段用户程序并发运行时能在正确可用的 Region 中创建新对象。这阶段需要停顿线程，但耗时很短。
2. **并发标记（Concurrent Marking）**：从 GC Root 开始对堆中对象进行可达性分析，找出存活的对象，这阶段耗时较长，但可与用户程序并发执行。
3. **最终标记（Final Marking）**：修正在并发标记期间因用户程序继续运作而导致标记产生变动的那部分标记记录，虚拟机将这段时间对象的变化记录在线程 Remembered Set Logs 里，最终标记阶段需要把 Remembered Set Logs 的数据合并到 Remembered Set 中。这阶段需要停顿线程，但可并行执行。
4. **筛选回收（Live Data Counting and Evacuation）**：首先对各个 Region 的回收价值和成本进行排序，根据用户期望的 GC 停顿时间制定回收计划。这个阶段其实也可以与用户程序一起并发执行，但因为只回收一部分 Region，时间是用户可控制的，停顿用户线程将大幅提高收集效率。

## 收集器发展时间线

按 JDK 版本梳理各收集器出现、转正、废弃的节点：

| JDK 版本 | 事件 |
| --- | --- |
| JDK 1.3.1 及以前 | 只有 Serial（+ Serial Old）一种选择 |
| JDK 1.4.1（2002） | Parallel Scavenge 出现，`-XX:+UseParallelGC`；此时老年代仍只能搭配 Serial Old |
| JDK 1.4.2（2003） | CMS 作为实验特性引入；ParNew 随之出现，专门配合 CMS 收集新生代 |
| JDK 1.5 / J2SE 5.0（2004） | CMS 转为正式支持，`-XX:+UseConcMarkSweepGC` = ParNew + CMS |
| JDK 1.6（2006） | Parallel Old 出现，`-XX:+UseParallelOldGC` = Parallel Scavenge + Parallel Old |
| JDK 6u14（2008） | G1 作为实验特性引入 |
| JDK 7u4（2012） | G1 转为正式支持 |
| JDK 8（2014） | JEP 173 标记 ParNew+SerialOld、DefNew+CMS 组合以及 CMS 增量模式（iCMS）为过时用法，启动时打印警告 |
| JDK 9（2017） | G1 成为默认收集器；JEP 214 移除上述过时组合（使用即拒绝启动）；CMS 本身（ParNew+CMS 组合）被标记废弃（JEP 291），独立的 `-XX:+UseParNewGC` 开关也一并标记废弃 |
| JDK 10（2018） | `-XX:+UseParNewGC` 开关被彻底移除，此后 ParNew 只能通过 `-XX:+UseConcMarkSweepGC` 隐式启用 |
| JDK 11（2018） | Epsilon 无操作收集器引入（JEP 318）；ZGC 作为实验特性引入（JEP 333） |
| JDK 12（2019） | Shenandoah 作为实验特性引入（JEP 189） |
| JDK 14（2020） | CMS 正式移除（JEP 363），ParNew 因此完全退场 |
| JDK 15（2020） | ZGC（JEP 377）、Shenandoah（JEP 379）转为正式支持 |
| JDK 21（2023） | 分代 ZGC 作为实验特性引入（JEP 439） |
| JDK 23（2024） | 分代 ZGC 成为默认模式（JEP 474） |
| JDK 24（2025） | 非分代 ZGC 模式被移除，ZGC 只保留分代模式（JEP 490） |

需要注意四点：

1. Shenandoah 只存在于 OpenJDK 社区构建（如 Eclipse Temurin、Red Hat build），Oracle 官方 JDK 发行版不包含它。
2. 从 JDK 9 起，如无特殊配置，各版本默认收集器都是 G1。
3. 被移除的不止 CMS 一个：`ParNew+SerialOld`、`DefNew+CMS` 这类冷门组合，以及 CMS 增量模式，在 JDK 9（JEP 214）就已经移除；独立的 `-XX:+UseParNewGC` 开关在 JDK 10 移除；CMS 本体（连带隐式携带的 ParNew）则是 JDK 9 标记废弃、JDK 14（JEP 363）才真正移除。Serial、Parallel（含 Serial Old / Parallel Old）、G1、ZGC、Shenandoah 这几个主线收集器则从未被移除或废弃，参数一直可用。
4. 两类移除的行为不同：JDK 9 移除 JEP 214 里的过时组合时，用了对应参数 JVM 会直接拒绝启动；而 JDK 14 移除 CMS 时只是打印 `Ignoring option UseConcMarkSweepGC; support was removed` 警告并回退到默认收集器，并不会启动失败。

### JDK 17（LTS）可用收集器速查

Oracle 官方为每个 JDK 版本都维护着「可用收集器」文档（[JDK 17 版](https://docs.oracle.com/en/java/javase/17/gctuning/available-collectors.html)），JDK 17 这一节列出的是：

| 收集器 | 启用参数 | 说明 |
| --- | --- | --- |
| Serial | `-XX:+UseSerialGC` | 单线程，适合小数据量、单核场景 |
| Parallel | `-XX:+UseParallelGC` | 多线程，吞吐量优先 |
| G1（默认） | `-XX:+UseG1GC` | 大多数硬件/系统配置下的默认收集器 |
| ZGC | `-XX:+UseZGC` | JDK 15 转正，全并发低延迟，停顿控制在几毫秒级 |
| Shenandoah | `-XX:+UseShenandoahGC` | JDK 15 转正；仅 OpenJDK 社区构建提供，Oracle 官方 JDK 不含 |

也就是说 JDK 17 并不是只剩 G1 和 ZGC 两个选项，Serial、Parallel 依然保留；只是生产环境常见配置是「默认 G1，延迟敏感场景切 ZGC/Shenandoah」。CMS 和 ParNew 在 JDK 17 里已经彻底不存在。

## 如何查看当前使用的 GC

### JMX

通过 JMX 的 `java.lang.GarbageCollector` MBean 可以查看当前 JVM 使用的 GC。

### Java 代码

输出结果与 JMX 查看的结果相同：

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
```

生产环境某次输出示例为 `Copy`、`MarkSweepCompact`，代表正在使用单线程的垃圾回收器 `-XX:+UseSerialGC`。

## 总结

虽然是在对各个收集器进行比较，但并非为了挑选出一个最好的收集器，因为直到现在为止还没有最好的收集器出现，更没有万能的收集器，所以只能选择对具体应用最合适的收集器。这一点不需要多加解释就能证明：如果有一种放之四海皆准、任何场景下都适用的完美收集器存在，那 HotSpot 虚拟机就没必要实现这么多不同的收集器了。

`-XX:+ScavengeBeforeFullGC`（JDK 1.4.1 引入）：在执行 Full GC 之前先执行一次 Minor GC，VM 会分两次停顿，可以缩短最大停顿时间。

## 参考链接

- <http://www.jianshu.com/p/50d5c88b272d>
- <http://www.cnblogs.com/sunniest/p/4575144.html>
- <http://www.infoq.com/cn/news/2017/03/garbage-collection-algorithm>
- Visualizing Garbage Collection Algorithms：<https://spin.atomicobject.com/2014/09/03/visualizing-garbage-collection-algorithms/embed/#?secret=w2JRHHSugP>
- <https://www.ibm.com/developerworks/cn/java/j-lo-JVMGarbageCollection/index.html>
- <https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/collectors.html>
- <http://www.oracle.com/technetwork/systems/vmoptions-jsp-140102.html>
- <http://zqhxuyuan.github.io/2016/07/26/JVM/>
- <https://juejin.im/post/5b546bc9f265da0f8f203968>
- <https://www.cnblogs.com/woshimrf/p/jvm-garbage.html>

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-14 | 文件重命名为 `gc.md`；url 改为 `gc`；标题改为「Java GC 垃圾回收机制与收集器」；全文重新分节整理，合并重复的 STW / Minor GC-Major GC-Full GC / 悬挂指针等定义；补充「新生代/老年代对应哪些收集器」小节及 Metaspace 说明；标签由 `reprint` 改为 `remix`、`AI-assisted` | 原文件名与目录重复、结构松散且存在多处重复定义，作者要求整理并明确新生代/老年代与具体 GC 收集器的对应关系 |
