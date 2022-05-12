---
title: Parallel Scavenge
author: "-"
date: 2017-06-05T06:18:02+00:00
url: java-gc-ps
categories:
  - Java
tags:$
  - reprint
---
## Parallel Scavenge
Parallel Scavenge收集器的特点是它的关注点与其他收集器不同,CMS等收集器的关注点尽可能地缩短垃圾收集时用户线程的停顿时间,而Parallel Scavenge收集器的目标则是达到一个可控制的吞吐量 (Throughput) 。所谓吞吐量就是CPU用于运行用户代码的时间与CPU总消耗时间的比值,即吞吐量 = 运行用户代码时间 / (运行用户代码时间 + 垃圾收集时间) ,虚拟机总共运行了100分钟,其中垃圾收集花掉1分钟,那吞吐量就是99%。

停顿时间越短就越适合需要与用户交互的程序,良好的响应速度能提升用户的体验；而高吞吐量则可以最高效率地利用CPU时间,尽快地完成程序的运算任务,主要适合在后台运算而不需要太多交互的任务。

Parallel Scavenge收集器提供了两个参数用于精确控制吞吐量,分别是控制最大垃圾收集停顿时间的-XX:MaxGCPauseMillis参数及直接设置吞吐量大小的 -XX:GCTimeRatio参数。

MaxGCPauseMillis参数允许的值是一个大于0的毫秒数,收集器将尽力保证内存回收花费的时间不超过设定值。不过大家不要异想天开地认为如果把这个参数的值设置得稍小一点就能使得系统的垃圾收集速度变得更快,GC停顿时间缩短是以牺牲吞吐量和新生代空间来换取的: 系统把新生代调小一些,收集300MB新生代肯定比收集500MB快吧,这也直接导致垃圾收集发生得更频繁一些,原来10秒收集一次、每次停顿100毫秒,现在变成5秒收集一次、每次停顿70毫秒。停顿时间的确在下降,但吞吐量也降下来了。

GCTimeRatio参数的值应当是一个大于0小于100的整数,也就是垃圾收集时间占总时间的比率,相当于是吞吐量的倒数。如果把此参数设置为19,那允许的最大GC时间就占总时间的5% (即1 / (1+19) ) ,默认值为99,就是允许最大1% (即1 / (1+99) ) 的垃圾收集时间。

由于与吞吐量关系密切,Parallel Scavenge收集器也经常被称为"吞吐量优先"收集器。除上述两个参数之外,Parallel Scavenge收集器还有一个参数-XX:+UseAdaptiveSizePolicy值得关注。这是一个开关参数,当这个参数打开之后,就不需要手工指定新生代的大小 (-Xmn) 、Eden与Survivor区的比例 (-XX:SurvivorRatio) 、晋升老年代对象年龄 (-XX:PretenureSizeThreshold) 等细节参数了,虚拟机会根据当前系统的运行情况收集性能监控信息,动态调整这些参数以提供最合适的停顿时间或最大的吞吐量,这种调节方式称为GC自适应的调节策略 (GC Ergonomics) 。如果读者对于收集器运作原理不太了解,手工优化存在困难的时候,使用Parallel Scavenge收集器配合自适应调节策略,把内存管理的调优任务交给虚拟机去完成将是一个很不错的选择。只需要把基本的内存数据设置好 (如-Xmx设置最大堆) ,然后使用MaxGCPauseMillis参数 (更关注最大停顿时间) 或GCTimeRatio参数 (更关注吞吐量) 给虚拟机设立一个优化目标,那具体细节参数的调节工作就由虚拟机完成了。自适应调节策略也是Parallel Scavenge收集器与ParNew收集器的一个重要区别。

HotSpot VM里多个GC有部分共享的代码。有一个分代式GC框架,Serial/Serial Old/ParNew/CMS都在这个框架内；在该框架内的young collector和old collector可以任意搭配使用,所谓的"mix-and-match"。
  
而ParallelScavenge与G1则不在这个框架内,而是各自采用了自己特别的框架。这是因为新的GC实现时发现原本的分代式GC框架用起来不顺手。请参考官方文档的Collector Styles一段。

ParallelScavenge (PS) 的young collector就如其名字所示,是并行的拷贝式收集器。本来这个young collector就是"Parallel Scavenge"所指,但因为它不兼容原本的分代式GC框架,为了凸显出它是不同的,所以它的young collector带上了PS前缀,全名变成PS Scavenge。对应的,它的old collector的名字也带上了PS前缀,叫做PS MarkSweep。
  
这个PS MarkSweep默认的实现实际上是一层皮,它底下真正做mark-sweep-compact工作的代码是跟分代式GC框架里的serial old (这个collector名字叫做MarkSweepCompact) 是共用同一份代码的。也就是说实际上PS MarkSweep与MarkSweepCompact在HotSpot VM里是同一个collector实现,包了两张不同的皮；这个collector是串行的。

在顶楼链接里的那帖就是基于这个事实,而将两者简单的一并描述为"serial old"。

能与PS系兼容的并行old collector可以通过-XX:+UseParallelOldGC来开启,但 (不幸的是) 它的collector名字显示出来也是PS MarkSweep。

还有这种代码增添混乱程度: 
  
C++代码 收藏代码
  
inline const char* PSOldGen::select_name() {
    
return UseParallelOldGC ? "ParOldGen" : "PSOldGen";
  
}

HotSpot VM的GC组老人之一Jon Masamitsu很久之前就写过blog讲解这个: https://blogs.oracle.com/jonthecollector/entry/our_collectors

简单来说,有这么多东西反映了HotSpot VM的开发历史和实现细节。我在写篇东西讲述这部分历史,哪天写完的话在这边也放个链接嗯。

DefNewGeneration是default new generation
  
ParNewGeneration是parallel new generation

原本HotSpot VM里没有并行GC,当时就只有NewGeneration；后来准备要加入young gen的并行GC,就把原本的NewGeneration改名为DefNewGeneration,然后把新加的并行版叫做ParNewGeneration。

这些XXXGeneration都在HotSpot VM的"分代式GC框架"内。本来HotSpot VM鼓励开发者尽量在这个框架内开发GC,但后来有个开发就是不愿意被这框架憋着,自己硬写了个没有使用已有框架的新并行GC,并拉拢性能测试团队用这个并行GC来跑分,成绩也还不错,于是这个GC就放进HotSpot VM里了。这就是我们现在看到的ParallelScavenge。

 (结果就是HotSpot GC组不得不维护两个功能几乎一样、但各种具体细节不同的并行GC。其实是件很头疼的事情嗯) 

Scavenge或者叫scavenging GC,其实就是copying GC的另一种叫法而已。HotSpot VM里的GC都是在minor GC收集器里用scavenging的,DefNew、ParNew和ParallelScavenge都是,只不过DefNew是串行的copying GC,而后两者是并行的copying GC。

由此名字就可以知道,"ParallelScavenge"的初衷就是把"scavenge"给并行化。换句话说就是把minor GC并行化。至于full GC,那不是当初关注的重点。

把GC并行化的目的是想提高GC速度,也就是提高吞吐量 (throughput) 。所以其实ParNew与ParallelScavenge都可叫做Throughput GC。
  
但是在HotSpot VM的术语里"Throughput GC"通常特指"ParallelScavenge"。

================================

ParallelScavenge和ParNew都是并行GC,主要是并行收集young gen,目的和性能其实都差不多。最明显的区别有下面几点: 
  
1. PS以前是广度优先顺序来遍历对象图的,JDK6的时候改为默认用深度优先顺序遍历,并留有一个UseDepthFirstScavengeOrder参数来选择是用深度还是广度优先。在JDK6u18之后这个参数被去掉,PS变为只用深度优先遍历。ParNew则是一直都只用广度优先顺序来遍历
  
2. PS完整实现了adaptive size policy,而ParNew及"分代式GC框架"内的其它GC都没有实现完 (倒不是不能实现,就是麻烦+没人力资源去做) 。所以千万千万别在用ParNew+CMS的组合下用UseAdaptiveSizePolicy,请只在使用UseParallelGC或UseParallelOldGC的时候用它。
  
3. 由于在"分代式GC框架"内,ParNew可以跟CMS搭配使用,而ParallelScavenge不能。当时ParNew GC被从Exact VM移植到HotSpot VM的最大原因就是为了跟CMS搭配使用。
  
4. 在PS成为主要的throughput GC之后,它还实现了针对NUMA的优化；而ParNew一直没有得到NUMA优化的实现。

http://book.51cto.com/art/201107/278917.htm
  
http://hllvm.group.iteye.com/group/topic/27629#post-199089
  
http://hllvm.group.iteye.com/group/topic/37095#post-242695