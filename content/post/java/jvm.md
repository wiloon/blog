---
title: jvm
author: "-"
date: ""
url: ""
categories:
  - Java
tags:
  - inbox
---
## jvm
JVM是Java Virtual Machine (Java虚拟机）的缩写

常用jvm
目前市面上普遍使用的JVM大致有三种

- Sun公司的HotSpot——绝大多数java开发者都用的是这款，绝对的主力
- Oracle公司的JRockit——这款主要用于金融和军事
- IBM公司的J9 VM——这款是IBM硬件绑定的，用户也很少

IBM 开源了它开发的 J9 Java 虚拟机 (JVM)，并将其贡献给了 Eclipse 基金会，重命名为 Eclipse OpenJ9。J9 是一个高性能可伸缩的 Java 虚拟机，是许多 IBM 企业级软件产品的核心，OpenJ9 可作为 Hotspot 的替代者用于 OpenJDK

Java虚拟机四大组成部分
- 执行引擎(解释器和即时编译器)
- 类加载器
- 运行时数据区
- 垃圾回收器

### 执行引擎 Execution Engine
Java虚拟机的执行引擎主要是用来执行Java字节码。JVM的执行引擎执行字节码通过两种解释器执行的：字节码解释器与模板解释器，运行过程中，可能会触发即时编译 (JIT），涉及到几种即时编译器，下面分别进行介绍。
执行引擎是Java虛拟机核心的组成部分之一。


虚拟机是一个相对于“物理机”的概念，这两种机器都有代码执行能力，其区别是物理机的执行引擎是直接建立在处理器、缓存、指令集和操作系统层面上的，而虚拟机的执行引擎则是由软件自行实现的，因此可以不受物理条件制约地定制指令集与执行引擎的结构体系，能够执行那些不被硬件直接支持的指令集格式。


JVM的主要任务是负责装载字节码到其内部，但字节码并不能够直接运行在操作系统之上，因为字节码指令并非等价于本地机器指令，它内部包含的仅仅只是一些能够被JVM所识别的字节码指令、符号表，以及其他辅助信息。


如果想要让一个Java程序运行起来，执行引擎(Execution Engine)的任务就是将字节码指令解释/编译为对应平台上的本地机器指令才可以。简单来说，JVM中的执行引擎充当了将高级语言翻译为机器语言的译者。
 

### 解释器分类
在Java的发展历史里，一共有两套解释执行器，即古老的字节码解释器、现在普遍使用的模板解释器。


字节码解释器：在执行时通过纯软件代码模拟字节码的执行，效率非常低下。


模板解释器：将每一条字节码和一个模板函数相关联，模板函数中直接产生这条字节码执行时的本地机器代码，从而很大程度上提高了解释器的性能。


在HotSpot VM中，解释器主要由Interpreter模块和Code模块构成。

Interpreter模块:实现了解释器的核心功能
Code模块:用于管理HotSpotVM在运行时生成的本地机器指令



JIT编译器(Just In Time Compiler)
就是虚拟机将源代码直接编译成和本地机器平台相关的汇编语言,通过汇编生成机器代码。
现代虚拟机为了提高执行效率，会使用即时编译技术将方法编译成本地机器代码后再执行
Hotspot JIT编译器生成的是汇编代码，保存在方法区的JIT缓存区
本地机器代码不等于机器码，不同平台虚拟机翻译成本地的能识别的指令集，或者说是汇编语言。指令集由不同的架构构成,如：x86指令集
为什么还需要解释器
有些开发人员会感觉到诧异，既然HotSpot VM中已经内置JIT编译器了，那么为什么还需要再使用解释器来“拖累”程序的执行性能呢?比如JRockit VM内部就不包含解释器，字节码全部都依靠即时编译器编译后执行。
首先明确:
当程序启动后，解释器可以马上发挥作用，省去编译的时间，立即执行。编译器要想发挥作用，把代码编译成本地代码，需要一定的执行时间。但编译为本地代码后，执行效率高。
所以:
尽管JRockitVM中程序的执行性能会非常高效，但程序在启动时必然需要花费更长的时间来进行编译。对于服务端应用来说，启动时间并非是关注重点，但对于那些看中启动时间的应用场景而言，或许就需要采用解释器与即时编译器并存的架构来换取一一个平衡点。在此模式下，当Java虛拟器启动时，解释器可以首先发挥作用，而不必等待即时编译器全
部编译完成后再执行，这样可以省去许多不必要的编译时间。随着时间的推移，编译器发挥作用，把越来越多的代码编译成本地代码，获得更高的执行效率。同时，解释执行在编译器进行激进优化不成立的时候，作为编译器的“逃生门”
当虚拟机启动的时候，解释器可以首先发挥作用，而不必等待即时编译器全部编译完成再执行，这样可以省去许多不必要的编译时间。并且随着程序运行时间的推移，即时编译器逐渐发挥作用，根据热点探测功能，将有价值的字节码编译为汇编语言，以换取更高的程序执行效率。

作者：小伙子vae
链接：https://juejin.cn/post/6995362542386151431
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

### HotSpot

https://github.com/openjdk/jdk/tree/master/src/hotspot

## java, JVM flags, params, 参数, xms xmx xmn xss
### -Xms, -XX:InitialHeapSize
单位是 Byte，但同时也支持使用速记符号，比如“k”或者“K”代表“kilo”，“m”或者“M”代表“mega”，“g”或者“G”代表“giga”。
JVM初始分配的堆内存大小，默认物理内存的1/64(<1GB)

### -Xmx, -XX:MaxHeapSize
最大堆大小,默认物理内存的1/4(<1GB),

```bash
java -Xms128m -Xmx2g MyApp
java -XX:MaxHeapSize=2g app0

```

### -XX:MaxNewSize

设置Yong Generation的最大值大小

### -XX:NewSize

设置Yong Generation的初始值大小

### -XX:OldSize

设置JVM启动分配的老年代内存大小，类似于新生代内存的初始大小-XX:NewSize。

### -XX:MinHeapDeltaBytes

每次扩展堆的时候最小增长

### -XX:+PrintCommandLineFlags
显示出VM初始化完毕后所有跟最初的默认值不同的参数及它们的值。  (JDK5以上支持) 

```bash
java -XX:+PrintCommandLineFlags -version
```

### -XX:+PrintFlagsInitial

displays what options were provided to HotSpot initially, before HotSpot has made its own tweaks.

### -XX:+PrintFlagsFinal

displays what options HotSpot ended up using for running Java code

```bash
java -XX:+PrintFlagsFinal -version| grep GC
```

### -XX:CICompilerCount

JIT(just-in-time 即时) 编译器后台的编译线程数

### -XX:+PrintCompilation

使用 -XX:+PrintCompilation 编译的日志就会打印在console里面，如果需要更详细记录到文件的话，
  
就加上 -XX:+LogCompilation -XX:LogFile=<path to file>，这两个flag会开启记录xml格式的更详细编译日志。

### -XX:+UseCompressedClassPointers

压缩类指针
  
对象的类指针 (_klass) 被压缩至32bit
  
使用类指针压缩空间的基地址

### -XX:+UseCompressedOops

压缩对象指针
  
oops是指普通对象指针
  
Java堆中对象的对象指针被压缩到32bit
  
使用堆基地址 (如果在低26G内存空间中，为0) 即，指针的偏移量针对于堆的基地址

### -XX:+TraceClassLoading    -Xlog:class+load=info
-XX:+TraceClassLoading 显示类的加载信息, jdk 16 里面作废掉了,  用 -Xlog:class+load=info

### -XX:+HeapDumpOnOutOfMemoryError
JVM在发生内存溢出时自动的生成堆内存快照
默认情况下，堆内存快照会保存在JVM的启动目录下名为java_pid<pid>.hprof 的文件里 (在这里<pid>就是JVM进程的进程号) 。也可以通过设置-XX:HeapDumpPath=<path>来改变默认的堆内存快照生成路径，<path>可以是相对或者绝对路径。

---

-XX:MaxDirectMemorySize

-XX:MetaspaceSize
  
-XX:MaxMetaspaceSize=128m

jdk7---
  
-XX:PermSize=64M JVM初始分配的非堆内存
  
-XX:MaxPermSize=128M JVM最大允许分配的非堆内存，按需分配

-Xmn
  
年轻代大小(1.4or lator)
  
注意: 此处的大小是 (eden+ 2 survivor space).与jmap -heap中显示的New gen是不同的。
  
整个堆大小=年轻代大小 + 年老代大小 + 持久代大小.
  
增大年轻代后,将会减小年老代大小.此值对系统性能影响较大,Sun官方推荐配置为整个堆的3/8

-XX:MaxDirectMemorySize
  
指定最大的堆外内存大小

JVM启动参数共分为三类: 
          
其一是标准参数 (-) ，所有的JVM实现都必须实现这些参数的功能，而且向后兼容；
          
其二是非标准参数 (-X) ，指的是JVM底层的一些配置参数，这些参数在一般开发中默认即可，不需要任何配置。但是在生产环境中，并不保证所有jvm实现都满足，所以为了提高性能，往往需要调整这些参数，以求系统达到最佳性能。
                                             
另外这些参数不保证向后兼容，也即是说"如有变更，恕不在后续版本的JDK通知" (这是官网上的原话) ；
          
其三是非Stable参数 (-XX) ，这类参数在jvm中是不稳定的，不适合日常使用的，后续也是可能会在没有通知的情况下就直接取消了，需要慎重使用。

### -Xss, -XX:ThreadStackSize, java 线程栈
-Xss 是在HotSpot之前就在使用的配置(很多其它的java虚拟机都支持), -XX:ThreadStackSize 是 HotSpot 特有的配置.
Xss越大，每个线程的大小就越大，占用的内存越多，能容纳的线程就越少; Xss越小，则递归的深度越小，容易出现栈溢出 java.lang.StackOverflowError。减少局部变量的声明，可以节省栈帧大小，增加调用深度。不显式设置-Xss或-XX:ThreadStackSize时，在Linux x64上ThreadStackSize的默认值就是 1024KB

不显式设置-Xss或-XX:ThreadStackSize时，在Linux x64上ThreadStackSize的默认值就是1024KB，给Java线程创建栈会用这个参数指定的大小。这是前一块代码的意思。如果把-Xss或者-XX:ThreadStackSize设为0，就是使用“系统默认值”。而在Linux x64上HotSpot VM给Java栈定义的“系统默认”大小也是1MB。所以这个条件下普通Java线程的默认栈大小怎样都是1MB。至于操作系统栈大小 (ulimit -s) : 这个配置只影响进程的初始线程；后续用pthread_create创建的线程都可以指定栈大小。HotSpot VM为了能精确控制Java线程的栈大小，特意不使用进程的初始线程 (primordial thread) 作为Java线程。

---

作者: RednaxelaFX
链接: https://www.zhihu.com/question/27844575/answer/38370294
来源: 知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

http://mail.openjdk.java.net/pipermail/hotspot-dev/2011-June/004272.html

http://mail.openjdk.java.net/pipermail/hotspot-dev/2011-July/004288.html


jvm的线程栈申请的内存空间属于堆外内存，是向操作系统申请的，也不是JVM直接内存

https://blog.csdn.net/x763795151/article/details/90417816

---

-XX:NewRatio=n: 设置年轻代和年老代的比值。如:为3，表示年轻代与年老代比值为1: 3，年轻代占整个年轻代年老代和的1/4
  
-XX:SurvivorRatio=n: 年轻代中Eden区与两个Survivor区的比值。注意Survivor区有两个。如: 3，表示Eden: Survivor=3: 2，一个Survivor区占整个年轻代的1/5
  
-XX:MaxPermSize=n:设置持久代大小

XX:+DisableExplicitGC
  
忽略手动调用GC的代码使得 System.gc()的调用就会变成一个空调用，完全不会触发任何GC。

ExplicitGCInvokesConcurrent
  
使用CMS GC，做并行full gc

### 垃圾收集器设置

-XX:+UseSerialGC: 使用串行收集器，Force HotSpot to use Serial Collector, **启动参数中直接增加此key, 不需要设置值为true; 这样写是错误的: -XX:+UseSerialGC=true**
  
-XX:+UseParallelGC: 使用并行收集器
  
-XX:+UseParallelOldGC: 使用并行年老代收集器,配置年老代垃圾收集方式为并行收集。JDK6.0支持对年老代并行收集。
  
-XX:+UseConcMarkSweepGC: 使用并发收集器
  
XX:+UseParNewGC: 使用ParNew + Serial Old 收集器组合
  
-XX:+UseG1GC: 使用G1收集器

### 垃圾回收统计信息

-XX:+PrintGC
  
-XX:+PrintGCDetails
  
-XX:+PrintGCTimeStamps
  
-Xloggc:filename

### 并行收集器设置

-XX:ParallelGCThreads=n:设置并行收集器收集时使用的CPU数。并行收集线程数。
  
-XX:MaxGCPauseMillis=n:设置并行收集最大暂停时间
  
-XX:GCTimeRatio=n:设置垃圾回收时间占程序运行时间的百分比。公式为1/(1+n)

### 并发收集器设置

-XX:+CMSIncrementalMode:设置为增量模式。适用于单CPU情况。
  
-XX:ParallelGCThreads=n:设置并发收集器年轻代收集方式为并行收集时，使用的CPU数。并行收集线程数。

堆大小设置
  
JVM 中最大堆大小有三方面限制: 相关操作系统的数据模型 (32-bt还是64-bit) 限制；系统的可用虚拟内存限制；系统的可用物理内存限制。32位系统下，一般限制在1.5G~2G；64为操作系统对内存无限制。我在Windows Server 2003 系统，3.5G物理内存，JDK5.0下测试，最大可设置为1478m。
  
典型设置: 
  
java -Xms3550m -Xmx3550m -Xmn2g -Xss128k
  
-Xms3550m: 设置JVM初始内存为3550m。此值可以设置与-Xmx相同，以避免每次垃圾回收完成后JVM重新分配内存。
  
–Xmx3550m: 设置JVM最大可用内存为3550M。
  
-Xmn2g: 设置年轻代大小为2G。整个JVM内存大小=年轻代大小 + 年老代大小 + 持久代大小。持久代一般固定大小为64m，所以增大年轻代后，将会减小年老代大小。此值对系统性能影响较大，Sun官方推荐配置为整个堆的3/8。
  
-Xss128k: 设置每个线程的堆栈大小。JDK5.0以后每个线程堆栈大小为1M，以前每个线程堆栈大小为256K。根据应用的线程所需内存大小进行调整。在相同物理内存下，减小这个值能生成更多的线程。但是操作系统对一个进程内的线程数还是有限制的，不能无限生成，经验值在3000~5000左右。
  
java -Xmx3550m -Xms3550m -Xss128k -XX:NewRatio=4 -XX:SurvivorRatio=4 -XX:MaxPermSize=16m -XX:MaxTenuringThreshold=0
  
-XX:NewRatio=4:设置年轻代 (包括Eden和两个Survivor区) 与年老代的比值 (除去持久代) 。设置为4，则年轻代与年老代所占比值为1: 4，年轻代占整个堆栈的1/5
  
-XX:SurvivorRatio=4: 设置年轻代中Eden区与Survivor区的大小比值。设置为4，则两个Survivor区与一个Eden区的比值为2:4，一个Survivor区占整个年轻代的1/6
  
-XX:MaxPermSize=16m:设置持久代大小为16m。
  
-XX:MaxTenuringThreshold=0: 设置垃圾最大年龄。如果设置为0的话，则年轻代对象不经过Survivor区，直接进入年老代。对于年老代比较多的应用，可以提高效率。如果将此值设置为一个较大值，则年轻代对象会在Survivor区进行多次复制，这样可以增加对象再年轻代的存活时间，增加在年轻代即被回收的概论。
  
回收器选择
  
JVM给了三种选择: 串行收集器、并行收集器、并发收集器，但是串行收集器只适用于小数据量的情况，所以这里的选择主要针对并行收集器和并发收集器。默认情况下，JDK5.0以前都是使用串行收集器，如果想使用其他收集器需要在启动时加入相应参数。JDK5.0以后，JVM会根据当前系统配置进行判断。
  
吞吐量优先的并行收集器
  
如上文所述，并行收集器主要以到达一定的吞吐量为目标，适用于科学技术和后台处理等。
  
典型配置: 
  
java -Xmx3800m -Xms3800m -Xmn2g -Xss128k -XX:+UseParallelGC -XX:ParallelGCThreads=20
  
-XX:+UseParallelGC: 选择垃圾收集器为并行收集器。此配置仅对年轻代有效。即上述配置下，年轻代使用并发收集，而年老代仍旧使用串行收集。
  
-XX:ParallelGCThreads=20: 配置并行收集器的线程数，即: 同时多少个线程一起进行垃圾回收。此值最好配置与处理器数目相等。
  
java -Xmx3550m -Xms3550m -Xmn2g -Xss128k -XX:+UseParallelGC -XX:ParallelGCThreads=20 -
  
java -Xmx3550m -Xms3550m -Xmn2g -Xss128k -XX:+UseParallelGC -XX:MaxGCPauseMillis=100
  
-XX:MaxGCPauseMillis=100:设置每次年轻代垃圾回收的最长时间，如果无法满足此时间，JVM会自动调整年轻代大小，以满足此值。
  
java -Xmx3550m -Xms3550m -Xmn2g -Xss128k -XX:+UseParallelGC -XX:MaxGCPauseMillis=100-XX:+UseAdaptiveSizePolicy
  
-XX:+UseAdaptiveSizePolicy: 设置此选项后，并行收集器会自动选择年轻代区大小和相应的Survivor区比例，以达到目标系统规定的最低相应时间或者收集频率等，此值建议使用并行收集器时，一直打开。
  
响应时间优先的并发收集器
  
如上文所述，并发收集器主要是保证系统的响应时间，减少垃圾收集时的停顿时间。适用于应用服务器、电信领域等。
  
典型配置: 
  
java -Xmx3550m -Xms3550m -Xmn2g -Xss128k -XX:ParallelGCThreads=20 -XX:+UseConcMarkSweepGC -
  
-XX:+UseConcMarkSweepGC: 设置年老代为并发收集。测试中配置这个以后，-XX:NewRatio=4的配置失效了，原因不明。所以，此时年轻代大小最好用-Xmn设置。
  
-XX:+UseParNewGC:设置年轻代为并行收集。可与CMS收集同时使用。JDK5.0以上，JVM会根据系统配置自行设置，所以无需再设置此值。
  
java -Xmx3550m -Xms3550m -Xmn2g -Xss128k -XX:+UseConcMarkSweepGC -XX:CMSFullGCsBeforeCompaction=5 -XX:+UseCMSCompactAtFullCollection
  
-XX:CMSFullGCsBeforeCompaction: 由于并发收集器不对内存空间进行压缩、整理，所以运行一段时间以后会产生"碎片"，使得运行效率降低。此值设置运行多少次GC以后对内存空间进行压缩、整理。
  
-XX:+UseCMSCompactAtFullCollection: 打开对年老代的压缩。可能会影响性能，但是可以消除碎片
  
辅助信息
  
JVM提供了大量命令行参数，打印信息，供调试使用。主要有以下一些: 
  
-XX:+PrintGC
  
输出形式: [GC 118250K->113543K(130112K), 0.0094143 secs] [Full GC 121376K->10414K(130112K), 0.0650971 secs]
  
-XX:+PrintGCDetails
  
输出形式: [GC [DefNew: 8614K->781K(9088K), 0.0123035 secs] 118250K->113543K(130112K), 0.0124633 secs] [GC [DefNew: 8614K->8614K(9088K), 0.0000665 secs][Tenured: 112761K->10414K(121024K), 0.0433488 secs] 121376K->10414K(130112K), 0.0436268 secs]
  
-XX:+PrintGCTimeStamps -XX:+PrintGC: PrintGCTimeStamps可与上面两个混合使用
  
输出形式: 11.851: [GC 98328K->93620K(130112K), 0.0082960 secs]
  
-XX:+PrintGCApplicationConcurrentTime:打印每次垃圾回收前，程序未中断的执行时间。可与上面混合使用
  
输出形式: Application time: 0.5291524 seconds
  
-XX:+PrintGCApplicationStoppedTime: 打印垃圾回收期间程序暂停的时间。可与上面混合使用
  
输出形式: Total time for which application threads were stopped: 0.0468229 seconds
  
-XX:PrintHeapAtGC:打印GC前后的详细堆栈信息
  
输出形式: 
  
34.702: [GC {Heap before gc invocations=7:
  
def new generation total 55296K, used 52568K [0x1ebd0000, 0x227d0000, 0x227d0000)
  
eden space 49152K, 99% used [0x1ebd0000, 0x21bce430, 0x21bd0000)
  
from space 6144K, 55% used [0x221d0000, 0x22527e10, 0x227d0000)
  
to space 6144K, 0% used [0x21bd0000, 0x21bd0000, 0x221d0000)
  
tenured generation total 69632K, used 2696K [0x227d0000, 0x26bd0000, 0x26bd0000)
  
the space 69632K, 3% used [0x227d0000, 0x22a720f8, 0x22a72200, 0x26bd0000)
  
compacting perm gen total 8192K, used 2898K [0x26bd0000, 0x273d0000, 0x2abd0000)
  
the space 8192K, 35% used [0x26bd0000, 0x26ea4ba8, 0x26ea4c00, 0x273d0000)
  
ro space 8192K, 66% used [0x2abd0000, 0x2b12bcc0, 0x2b12be00, 0x2b3d0000)
  
rw space 12288K, 46% used [0x2b3d0000, 0x2b972060, 0x2b972200, 0x2bfd0000)
  
34.735: [DefNew: 52568K->3433K(55296K), 0.0072126 secs] 55264K->6615K(124928K)Heap after gc invocations=8:
  
def new generation total 55296K, used 3433K [0x1ebd0000, 0x227d0000, 0x227d0000)
  
eden space 49152K, 0% used [0x1ebd0000, 0x1ebd0000, 0x21bd0000)
  
from space 6144K, 55% used [0x21bd0000, 0x21f2a5e8, 0x221d0000)
  
to space 6144K, 0% used [0x221d0000, 0x221d0000, 0x227d0000)
  
tenured generation total 69632K, used 3182K [0x227d0000, 0x26bd0000, 0x26bd0000)
  
the space 69632K, 4% used [0x227d0000, 0x22aeb958, 0x22aeba00, 0x26bd0000)
  
compacting perm gen total 8192K, used 2898K [0x26bd0000, 0x273d0000, 0x2abd0000)
  
the space 8192K, 35% used [0x26bd0000, 0x26ea4ba8, 0x26ea4c00, 0x273d0000)
  
ro space 8192K, 66% used [0x2abd0000, 0x2b12bcc0, 0x2b12be00, 0x2b3d0000)
  
rw space 12288K, 46% used [0x2b3d0000, 0x2b972060, 0x2b972200, 0x2bfd0000)
  
}
  
, 0.0757599 secs]
  
-Xloggc:filename:与上面几个配合使用，把相关日志信息记录到文件以便分析。
  


### GC

-XX:+HeapDumpOnOutOfMemoryError, -XX:HeapDumpPath
  
JVM 在发生内存溢出时自动的生成堆内存快照。有了这个参数，当我们不得不面对内存溢出异常的时候会节约大量的时间。默认情况下，堆内存快照会保存在 JVM 的启动目录下名为 java_pid.hprof 的文件里 (在这里 就是 JVM 进程的进程号) 。也可以通过设置 - XX:HeapDumpPath= 来改变默认的堆内存快照生成路径， 可以是相对或者绝对路径。

-verbose.gc开关可显示GC的操作内容。打开它，可以显示最忙和最空闲收集行为发生的时间、收集前后的内存大小、收集需要的时间等。
  
-verbose:gc - Same as "-XX:+PrintGC".
  
-verbose:gc -Xloggc:$CATALINA_HOME/logs/gc.log
  
将虚拟机每次垃圾回收的信息写到日志文件中，文件名由file指定

-XX:+PrintGCDetails //包含-XX:+PrintGC
  
只要设置-XX:+PrintGCDetails 就会自动带上-verbose:gc和-XX:+PrintGC
  
-XX:+PrintGC - Print a shot message after each garbage collection is done.

-XX:+PrintGCDetails - Print a long message with more details after each garbage collection is done.
  
-XX:+PrintGCTimeStamps - Print a timestamp relative to the JVM start time when a garbage collection occurs.
  
-XX:+PrintGCDateStamps - Print a calendar data and timestamp when a garbage collection occurs.
  
-Xloggc:/path/gc.log - Force garbage collection message to be logged into a file instead of the console.

-XX:+UseGCLogFileRotation 启用GC日志文件的自动转储 (Since Java)
  
-XX:NumberOfGClogFiles=1 GC日志文件的循环数目 (Since Java)
  
-XX:GCLogFileSize=1M 控制GC日志文件的大小 (Since Java)

-XX:+PrintGCDateStamps/-XX:+PrintGCTimeStamps 输出gc的触发时间

JVM gc参数设置与分析
  
原文: 

http://hi.baidu.com/i1see1you/item/295c1dc81f91ab55bdef69e5
  
gc日志分析工具: http://qa.blog.163.com/blog/static/19014700220128199421589/
  
Java GC 日志图解: http://www.chinasb.org/archives/2012/09/4921.shtml
  
概述
  
java的最大好处是自动垃圾回收，这样就无需我们手动的释放对象空间了，但是也产生了相应的负效果，gc是需要时间和资源的，不好的gc会严重影响系统的系能，因此良好的gc是JVM的高性能的保证。JVM堆分为新生代，旧生代和年老代，新生代可用的gc方式有: 串行gc (Serial Copying) ，并行回收gc(Parellel Scavenge)，并行gc(ParNew)，旧生代和年老代可用的gc方式有串行gc(Serial MSC),并行gc(Parallel MSC)，并发gc (CMS) 。

回收方式的选择
  
jvm有client和server两种模式，这两种模式的gc默认方式是不同的: 

client模式下，新生代选择的是串行gc，旧生代选择的是串行gc

server模式下，新生代选择的是并行回收gc，旧生代选择的是并行gc

一般来说我们系统应用选择有两种方式: 吞吐量优先和暂停时间优先，对于吞吐量优先的采用server默认的并行gc方式，对于暂停时间优先的选用并发gc (CMS) 方式。

CMS gc
  
CMS，全称Concurrent Low Pause Collector，是jdk1.4后期版本开始引入的新gc算法，在jdk5和jdk6中得到了进一步改进，它的主要适合场景是对响应时间的重要性需求大于对吞吐量的要求，能够承受垃圾回收线程和应用线程共享处理器资源，并且应用中存在比较多的长生命周期的对象的应用。CMS是用于对tenured generation的回收，也就是年老代的回收，目标是尽量减少应用的暂停时间，减少full gc发生的几率，利用和应用程序线程并发的垃圾回收线程来标记清除年老代。在我们的应用中，因为有缓存的存在，并且对于响应时间也有比较高的要求，因此希望能尝试使用CMS来替代默认的server型JVM使用的并行收集器，以便获得更短的垃圾回收的暂停时间，提高程序的响应性。

CMS并非没有暂停，而是用两次短暂停来替代串行标记整理算法的长暂停，它的收集周期是这样: 

初始标记(CMS-initial-mark) -> 并发标记(CMS-concurrent-mark) -> 重新标记(CMS-remark) -> 并发清除(CMS-concurrent-sweep) ->并发重设状态等待下次CMS的触发(CMS-concurrent-reset)。

其中的1，3两个步骤需要暂停所有的应用程序线程的。第一次暂停从root对象开始标记存活的对象，这个阶段称为初始标记；第二次暂停是在并发标记之后，暂停所有应用程序线程，重新标记并发标记阶段遗漏的对象 (在并发标记阶段结束后对象状态的更新导致) 。第一次暂停会比较短，第二次暂停通常会比较长，并且 remark这个阶段可以并行标记。

而并发标记、并发清除、并发重设阶段的所谓并发，是指一个或者多个垃圾回收线程和应用程序线程并发地运行，垃圾回收线程不会暂停应用程序的执行，如果你有多于一个处理器，那么并发收集线程将与应用线程在不同的处理器上运行，显然，这样的开销就是会降低应用的吞吐量。Remark阶段的并行，是指暂停了所有应用程序后，启动一定数目的垃圾回收进程进行并行标记，此时的应用线程是暂停的。

full gc
  
full gc是对新生代，旧生代，以及持久代的统一回收，由于是对整个空间的回收，因此比较慢，系统中应当尽量减少full gc的次数。

如下几种情况下会发生full gc: 

旧生代空间不足
  
持久代空间不足
  
CMS GC时出现了promotion failed和concurrent mode failure
  
统计得到新生代minor gc时晋升到旧生代的平均大小小于旧生代剩余空间
  
直接调用System.gc，可以DisableExplicitGC来禁止
  
存在rmi调用时，默认会每分钟执行一次System.gc，可以通过-Dsun.rmi.dgc.server.gcInterval=3600000来设置大点的间隔。
  
Gc日志参数
  
通过在tomcat启动脚本中添加相关参数生成gc日志

打开-xx:+printGCdetails开关，可以详细了解GC中的变化。
  
打开-XX:+PrintGCTimeStamps开关，可以了解这些垃圾收集发生的时间，自JVM启动以后以秒计量。
  
最后，通过-xx:+PrintHeapAtGC开关了解堆的更详细的信息。
  
为了了解新域的情况，可以通过-XX:+PrintTenuringDistribution开关了解获得使用期的对象权。
  
-Xloggc:$CATALINA_BASE/logs/gc.log gc日志产生的路径
  
-XX:+PrintGCApplicationStoppedTime 输出GC造成应用暂停的时间
  
-XX:+PrintGCDateStamps GC发生的时间信息
  
Opentsdb打开Gc参数

# tsdb.local

# http://opentsdb.net/docs/build/html/user_guide/cli/index.html

GCARGS="-XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps\
  
-XX:+PrintTenuringDistribution -Xloggc:/tmp/tsd-gc-`date +%s`.log"
  
if test -t 0; then # if stdin is a tty, don't turn on GC logging.
  
GCARGS=
  
fi

# The Sun JDK caches all name resolution results forever, which is stupid.

# This forces you to restart your application if any of the backends change

# IP. Instead tell it to cache names for only 10 minutes at most.

FIX_DNS='-Dsun.net.inetaddr.ttl=600'
  
JVMARGS="$JVMARGS $GCARGS $FIX_DNS"
  
常用JVM参数
  
分析gc日志后，经常需要调整jvm内存相关参数，常用参数如下

-Xms(-XX:InitialHeapSize)
  
初始堆大小，默认为物理内存的1/64(<1GB)；默认(MinHeapFreeRatio参数可以调整)空余堆内存小于40%时，JVM就会增大堆直到-Xmx的最大限制

-Xmx(-XX:MaxHeapSize)
  
最大堆大小，默认(MaxHeapFreeRatio参数可以调整)空余堆内存大于70%时，JVM会减少堆直到 -Xms的最小限制
  
-Xms 和 - Xmx 是 - XX:InitialHeapSize 和 - XX:MaxHeapSize 的缩写

-Xmn: 新生代的内存空间大小，注意: 此处的大小是 (eden+ 2 survivor space)。与jmap -heap中显示的New gen是不同的。整个堆大小=新生代大小 + 老生代大小 + 永久代大小。在保证堆大小不变的情况下，增大新生代后,将会减小老生代大小。此值对系统性能影响较大,Sun官方推荐配置为整个堆的3/8。
  
-XX:SurvivorRatio: 新生代中Eden区域与Survivor区域的容量比值，默认值为8。两个Survivor区与一个Eden区的比值为2:8,一个Survivor区占整个年轻代的1/10。
  
-Xss: 每个线程的堆栈大小。JDK5.0以后每个线程堆栈大小为1M,以前每个线程堆栈大小为256K。应根据应用的线程所需内存大小进行适当调整。在相同物理内存下,减小这个值能生成更多的线程。但是操作系统对一个进程内的线程数还是有限制的，不能无限生成，经验值在3000~5000左右。一般小的应用， 如果栈不是很深， 应该是128k够用的，大的应用建议使用256k。这个选项对性能影响比较大，需要严格的测试。和threadstacksize选项解释很类似,官方文档似乎没有解释,在论坛中有这样一句话:"-Xss is translated in a VM flag named ThreadStackSize"一般设置这个值就可以了。

-XX:PermSize
  
设置永久代(perm gen)初始值。默认值为物理内存的1/64。

-XX:MaxPermSize
  
设置持久代最大值。物理内存的1/4。

示例
  
下面对如下的参数进行分析: 

JAVA_OPTS="-server -Xms2000m -Xmx2000m -Xmn800m -XX:PermSize=64m -XX:MaxPermSize=256m -XX:SurvivorRatio=4

-Djava.awt.headless=true
  
-XX:+PrintGCTimeStamps -XX:+PrintGCDetails
  
-Dsun.rmi.dgc.server.gcInterval=600000 -Dsun.rmi.dgc.client.gcInterval=600000
  
-XX:+UseConcMarkSweepGC -XX:MaxTenuringThreshold=15"

-XX:SurvivorRatio=4
  
SurvivorRatio为新生代空间中的Eden区和救助空间Survivor区的大小比值，默认是32，也就是说Eden区是 Survivor区的32倍大小，要注意Survivo是有两个区的，因此Surivivor其实占整个young genertation的1/34。调小这个参数将增大survivor区，让对象尽量在survitor区呆长一点，减少进入年老代的对象。去掉救助空间的想法是让大部分不能马上回收的数据尽快进入年老代，加快年老代的回收频率，减少年老代暴涨的可能性，这个是通过将-XX:SurvivorRatio 设置成比较大的值 (比如65536)来做到。

-Djava.awt.headless=true
  
Headless模式是系统的一种配置模式。在该模式下，系统缺少了显示设备、键盘或鼠标。

-XX:+PrintGCTimeStamps -XX:+PrintGCDetails
  
设置gc日志的格式

-Dsun.rmi.dgc.server.gcInterval=600000 -Dsun.rmi.dgc.client.gcInterval=600000
  
指定rmi调用时gc的时间间隔

-XX:+UseConcMarkSweepGC -XX:MaxTenuringThreshold=15
  
采用并发gc方式，经过15次minor gc 后进入年老代

Xms 是指设定程序启动时占用内存大小。一般来讲，大点，程序会启动的快一点，但是也可能会导致机器暂时间变慢。

Xmx 是指设定程序运行期间最大可占用的内存大小。如果程序运行需要占用更多的内存，超出了这个设置值，就会抛出OutOfMemory异常。

Xss 是指设定每个线程的堆栈大小。这个就要依据你的程序，看一个线程大约需要占用多少内存，可能会有多少线程同时运行等。

以上三个参数的设置都是默认以Byte为单位的，也可以在数字后面添加[k/K]或者[m/M]来表示KB或者MB。而且，超过机器本身的内存大小也是不可以的，否则就等着机器变慢而不是程序变慢了。

-Xmsn
  
Specify the initial size, in bytes, of the memory allocation pool. This value must be a multiple of 1024 greater than 1MB. Append the letter k or K to indicate kilobytes, or m or M to indicate megabytes. The default value is chosen at runtime based on system configuration. For more information, see HotSpot Ergonomics
  
Examples:
  
-Xms6291456
  
-Xms6144k
  
-Xms6m

-Xmxn
  
Specify the maximum size, in bytes, of the memory allocation pool. This value must a multiple of 1024 greater than 2MB. Append the letter k or K to indicate kilobytes, or m or M to indicate megabytes. The default value is chosen at runtime based on system configuration. For more information, see HotSpot Ergonomics
  
Examples:
  
-Xmx83886080
  
-Xmx81920k
  
-Xmx80m

-Xssn
  
Set thread stack size.

一些常见问题
  
为了避免Perm区满引起的full gc，建议开启CMS回收Perm区选项: +CMSPermGenSweepingEnabled -XX:+CMSClassUnloadingEnabled

默认CMS是在tenured generation沾满68%的时候开始进行CMS收集，如果你的年老代增长不是那么快，并且希望降低CMS次数的话，可以适当调高此值: -XX:CMSInitiatingOccupancyFraction=80

遇到两种fail引起full gc: Prommotion failed和Concurrent mode failed时: 
  
Prommotion failed的日志输出大概是这样: 

[ParNew (promotion failed): 320138K->320138K(353920K), 0.2365970 secs]42576.951: [CMS: 1139969K->1120688K( 166784K), 9.2214860 secs] 1458785K->1120688K(2520704K), 9.4584090 secs]

这个问题的产生是由于救助空间不够，从而向年老代转移对象，年老代没有足够的空间来容纳这些对象，导致一次full gc的产生。解决这个问题的办法有两种完全相反的倾向: 增大救助空间、增大年老代或者去掉救助空间。

Concurrent mode failed的日志大概是这样的: 

(concurrent mode failure): 1228795K->1228598K(1228800K), 7.6748280 secs] 1911483K->1681165K(1911488K), [CMS Perm : 225407K->225394K(262144K)], 7.6751800 secs]

问题的产生原因是由于CMS回收年老代的速度太慢，导致年老代在CMS完成前就被沾满，引起full gc，避免这个现象的产生就是调小-XX:CMSInitiatingOccupancyFraction参数的值，让CMS更早更频繁的触发，降低年老代被占满的可能。

Gc日志分析工具
  
GC日志格式
  
2012-11-15T16:57:12.524+0800: 8.490 : [GC 8.490: [ParNew: 118016K->11244K(118016K), 0.0525525 secs] 183413K->83007K(511232K), 0.0527229 secs] [Times: user=0.08 sys=0.00, real=0.05 secs]

8.490: 表示虚拟机启动运行到8.490秒是进行了一次monor Gc(not Full GC)
  
ParNew: 表示对年轻代进行的GC，使用ParNew收集器
  
118016K->11244K(118016K): 118016K 年轻代收集前大小，11244K 收集完以后的大小，118016K 当前年轻代分配的总大小
  
0.0525525 secs: 表示对年轻代进行垃圾收集时，用户线程暂停的时间，即此次年轻代收集花费的时间
  
183413K->83007K(511232K):JVM heap堆收集前后heap堆内存的变化
  
0.0527229 secs: 整个JVM此次垃圾造成用户线程的暂停时间。
  
更全一点的参数说明: 
  
[GC [<collector>: <starting occupancy1> -> <ending occupancy1>, <pause time1> secs] <starting occupancy3> -> <ending occupancy3>, <pause time3> secs]<collector> GC收集器的名称
  
<starting occupancy1> 新生代在GC前占用的内存
  
<ending occupancy1> 新生代在GC后占用的内存 <pause time1> 新生代局部收集时jvm暂停处理的时间
  
<starting occupancy3> JVM Heap 在GC前占用的内存
  
<ending occupancy3> JVM Heap 在GC后占用的内存 <pause time3> GC过程中jvm暂停处理的总时间 

GCHisto
  
http://java.net/projects/gchisto

直接点击gchisto.jar就可以运行，点add载入gc.log

统计了总共gc次数，youngGC次数，FullGC次数，次数的百分比，GC消耗的时间，百分比，平均消耗时间，消耗时间最小最大值等

统计的图形化表示

YoungGC,FullGC不同消耗时间上次数的分布图，勾选可以显示youngGC或fullGC单独的分布情况

整个时间过程详细的gc情况，可以对整个过程进行剖析

GCLogViewer
  
http://code.google.com/p/gclogviewer/

gclogviewer是一个支持jdk 6的gc log可视化工具。

GCLogViewer支持: 

支持根据gc log生成GC的趋势图；
  
生成调优建议所需的数据趋势图。
  
整个过程gc情况的趋势图，还显示了gc类型，吞吐量，平均gc频率，内存变化趋势等。
  
Tools里还能比较不同gc日志:

HPjmeter
  
获取地址 https://h20392.www2.hpe.com/portal/swdepot/displayProductInfo.do?productNumber=HPJMETER
  
参考文档 http://www.javaperformancetuning.com/tools/hpjtune/index.shtml
  
工具很强大，但只能打开由以下参数生成的GC log， -verbose:gc -Xloggc:gc.log,添加其他参数生成的gc.log无法打开。

GCViewer
  
http://www.tagtraum.com/gcviewer.html
  
这个工具用的挺多的，但只能在JDK1.5以下的版本中运行，1.6以后没有对应。

garbagecat
  
http://code.google.com/a/eclipselabs.org/p/garbagecat/wiki/Documentation

其它监控方法
  
Jvisualvm
  
Jvisualvm动态分析jvm内存情况和gc情况，插件: visualGC

jvisualvm还可以heapdump出对应hprof文件 (默认存放路径: 监控的服务器 /tmp下) ，利用相关工具，比如HPjmeter可以对其进行分析

grep Full gc.log粗略观察FullGC发生频率

jstat –gcutil [pid] [intervel] [count]

jmap
  
jmap -histo pid可以观测对象的个数和占用空间

jmap -heap pid可以观测jvm配置参数，堆内存各区使用情况

jprofiler,jmap dump出来用MAT分析
  
如果要分析的dump文件很大的话，就需要很多内存，很容易crash。

所以在启动时，我们应该加上一些参数:  Java –Xms512M –Xmx1024M –Xss8M

-XX:InitialCodeCacheSize and -XX:ReservedCodeCacheSize

JVM 一个有趣的，但往往被忽视的内存区域是 "代码缓存"，它是用来存储已编译方法生成的本地代码。代码缓存确实很少引起性能问题，但是一旦发生其影响可能是毁灭性的。如果代码缓存被占满，JVM 会打印出一条警告消息，并切换到 interpreted-only 模式: JIT 编译器被停用，字节码将不再会被编译成机器码。因此，应用程序将继续运行，但运行速度会降低一个数量级，直到有人注意到这个问题。就像其他内存区域一样，我们可以自定义代码缓存的大小。相关的参数是 - XX:InitialCodeCacheSize 和 - XX:ReservedCodeCacheSize，它们的参数和上面介绍的参数一样，都是字节值。
  
-XX:+UseCodeCacheFlushing

如果代码缓存不断增长，例如，因为热部署引起的内存泄漏，那么提高代码的缓存大小只会延缓其发生溢出。为了避免这种情况的发生，我们可以尝试一个有趣的新参数: 当代码缓存被填满时让 JVM 放弃一些编译代码。通过使用 - XX:+UseCodeCacheFlushing 这个参数，我们至少可以避免当代码缓存被填满的时候 JVM 切换到 interpreted-only 模式。不过，我仍建议尽快解决代码缓存问题发生的根本原因，如找出内存泄漏并修复它。

GC日志
  
<http://www.wiloon.com/?p=5584>
  
http://sunbean.blog.51cto.com/972509/768034
  
http://xstarcd.github.io/wiki/Java/JVM_GC.html
  
http://wiki.jikexueyuan.com/project/jvm-parameter/memory-tuning.html
  
https://docs.oracle.com/javase/8/docs/technotes/tools/unix/java.html
  
http://blog.csdn.net/phj88/article/details/8011830
  
http://unixboy.iteye.com/blog/174173
  
https://www.zhihu.com/question/27844575
  
http://www.cnblogs.com/redcreen/archive/2011/05/04/2037057.html
  
http://www.oracle.com/technetwork/java/javase/tech/vmoptions-jsp-140102.html
  
http://xmlandmore.blogspot.com/2014/08/jdk-8-usecompressedclasspointers-vs.html
  
https://www.cnblogs.com/mingforyou/archive/2012/03/03/2378143.html
  
https://www.cnblogs.com/zhulin-jun/p/6516292.html

https://docs.oracle.com/en/java/javase/16/migrate/removed-tools-and-components.html#GUID-BBCF36FE-C892-4769-95CB-AB3FFC3A3B13

