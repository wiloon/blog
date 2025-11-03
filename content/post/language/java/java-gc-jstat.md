---
title: java gc监控, jstat
author: "-"
date: 2011-08-09T02:44:44+00:00
url: /?p=411
categories:
  - Development
tags:
  - Java

---
## java gc监控, jstat
```bash
jstat -<option> [-t] [-h] <vmid> [<interval> [<count>]]
jstat -gc -h3 <jvm PID> 3000 -1
# -gc 显示gc的信息，查看gc的次数，及时间。
# -h: 即-h跟数字，代表隔几行显示标题
# interval: 毫秒,代表监控间隔时间段，默认毫秒做单位
# count: 代表取数次数
```

Jstat在分析java的内存GC时的应用
  
jstat可以查看堆内各个部分的使用量，以及加载类的数量。使用时，需加上查看进程的进程id，和所选参数。

参数: 
      
jstat -class pid: Statistics on the behavior of the class loader. 显示加载class的数量，及所占空间等信息;
      
jstat -compiler pid: Statistics of the behavior of the HotSpot Just-in-Time compiler.显示VM实时编译的数量等信息;
      
jstat -gc pid: Statistics of the behavior of the garbage collected heap.可以显示gc的信息，查看gc的次数，及时间。其中最后五项，分别是young gc的次数，young gc的时间，full gc的次数，full gc的时间，gc的总时间。
      
jstat -gccapacity:可以显示，VM内存中三代 (young,old,perm) 对象的使用和占用大小，如: PGCMN显示的是最小perm的内存使用量，PGCMX显示的是perm的内存最大使用量，PGC是当前新生成的perm内存占用量，PC是但前perm内存占用量。其他的可以根据这个类推， OC是old内纯的占用量。
      
jstat -gcnew pid:new对象的信息。
      
jstat -gcnewcapacity pid:new对象的信息及其占用量。
      
jstat -gcold pid:old对象的信息。
      
jstat -gcoldcapacity pid:old对象的信息及其占用量。
      
jstat -gcpermcapacity pid: perm对象的信息及其占用量。
      
jstat -util pid:统计gc信息统计。
      
jstat -printcompilation pid:当前VM执行的信息。
      
除了以上一个参数外，还可以同时加上 两个数字，如: jstat -printcompilation 3024 250 6是每250毫秒打印一次，一共打印6次，还可以加上-h3每三行显示一下标题。
  
语法结构: 
  
Usage: jstat -help|-options
         
jstat -<option> [-t] [-h] <vmid> [<interval> [<count>]]
  
参数:
  
-t Display a timestamp column as the first column of output. The timestamp is the time since the start time of the target JVM.
  
Options — 选项，我们一般使用 -gcutil 查看gc情况比较多
  
vmid — VM的进程号，即当前运行的java进程号
  
interval– 间隔时间，单位为秒或者毫秒
  
count — 打印次数，如果缺省则打印无数次

### -gc

S0C Current survivor space 0 capacity (KB).
  
S1C Current survivor space 1 capacity (KB).
  
S0U Survivor space 0 utilization (KB).(utilization:已使用空间)
  
S1U Survivor space 1 utilization (KB).
  
EC Current eden space capacity (KB).
  
EU Eden space utilization (KB).
  
OC Current old space capacity (KB).
  
OU Old space utilization (KB).
  
MC: Metaspace capacity (kB).
  
MU: Metacspace utilization (kB).
  
CCSC: Compressed class space capacity (kB).
  
CCSU: Compressed class space used (kB).
  
PC Current permanent space capacity (KB).(Perm space)
  
PU Permanent space utilization (KB).
  
YGC Number of young generation GC Events.(从应用程序启动到采样时发生 Young GC 的次数 )
  
YGCT Young generation garbage collection time.
  
FGC Number of full GC events.
  
FGCT Full garbage collection time.
  
GCT Total garbage collection time.

如: [root@localhost bin]# jstat -gcutil 25332 1000 10  (25332是java的进程号，ps -ef | grep java) 

分代概念: 

分代是Java垃圾收集的一大亮点，根据对象的生命周期长短，把堆分为3个代: Young，Old和Permanent，根据不同代的特点采用不同的收集算法，扬长避短也。

Young(Nursery)，年轻代。研究表明大部分对象都是朝生暮死，随生随灭的。因此所有收集器都为年轻代选择了复制算法。

复制算法优点是只访问活跃对象，缺点是复制成本高。因为年轻代只有少量的对象能熬到垃圾收集，因此只需少量的复制成本。而且复制收集器只访问活跃对象，对那些占了最大比率的死对象视而不见，充分发挥了它遍历空间成本低的优点。

Young (年轻代) 

年 轻代分三个区。一个Eden区，两个Survivor区。大部分对象在Eden区中生成。当Eden区满时，还存活的对象将被复制到Survivor区  (两个中的一个) ，当这个Survivor区满时，此区的存活对象将被复制到另外一个Survivor区，当这个Survivor去也满了的时候，从第一 个Survivor区复制过来的并且此时还存活的对象，将被复制"年老区(Tenured)"。需要注意，Survivor的两个区是对称的，没先后关 系，所以同一个区中可能同时存在从Eden复制过来 对象，和从前一个Survivor复制过来的对象，而复制到年老区的只有从第一个Survivor去过来的对象。而且，Survivor区总有一个是空 的。

Tenured (年老代) 

年老代存放从年轻代存活的对象。一般来说年老代存放的都是生命期较长的对象。

Perm (持久代) 

用 于存放静态文件，如今Java类、方法等。持久代对垃圾回收没有显著影响，但是有些应用可能动态生成或者调用一些class，例如mybatis等， 在这种时候需要设置一个比较大的持久代空间来存放这些运行过程中新增的类。持久代大小通过-XX:MaxPermSize=进行设置。

Gc的基本概念

gc分为full gc 跟 minor gc，当每一块区满的时候都会引发gc。

Scavenge GC

一般情况下，当新对象生成，并且在Eden申请空间失败时，就触发了Scavenge GC，堆Eden区域进行GC，清除非存活对象，并且把尚且存活的对象移动到Survivor区。然后整理Survivor的两个区。

Full GC

对整个堆进行整理，包括Young、Tenured和Perm。Full GC比Scavenge GC要慢，因此应该尽可能减少Full GC。有如下原因可能导致Full GC: 

Tenured被写满

Perm域被写满

System.gc()被显示调用

上一次GC之后Heap的各域分配策略动态变化

http://www.cnblogs.com/mazj611/p/3481610.html
  
https://docs.oracle.com/javase/8/docs/technotes/tools/unix/jstat.html
  
https://www.jianshu.com/p/082340b9cd63