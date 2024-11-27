---
title: 'java.lang.OutOfMemoryError,unable to create new native thread'
author: "-"
date: 2015-10-27T01:42:13+00:00
url: /?p=8434
categories:
  - Inbox
tags:
  - reprint
---
## 'java.lang.OutOfMemoryError,unable to create new native thread'
http://www.blogjava.net/ldd600/archive/2009/09/25/296397.html

星期一早上到了公司,据称产品环境抛出了最可爱的异常—OutOfMemory, 它是这样来描述他自己的: 

java.lang.OutOfMemoryError: unable to create new native thread

而且这位仁兄竟然还堂而皇之地同时出现在了3个application里面,所有应用全部遭殃。

那可爱的OOM是如何产生的呢？直接原因是创建的线程太多了,根本原因是某个地方的内存限制了。

搜罗了一下在网上找到了一个计算公式: 

(MaxProcessMemory - JVMMemory – ReservedOsMemory) / (ThreadStackSize) = Number of threads

MaxProcessMemory: 进程最大的寻址空间,但我想这个值应该也不会超过虚拟内存和物理内存的总和吧。关于不同系统的进程可寻址的最大空间,可参考下面表格: 

Maximum Address Space Per Process
  
Operating System
  
Maximum Address Space Per Process
  
Redhat Linux 32 bit
  
2 GB
  
Redhat Linux 64 bit
  
3 GB
  
Windows 98/2000/NT/Me/XP
  
2 GB
  
Solaris x86 (32 bit)
  
4 GB
  
Solaris 32 bit
  
4 GB
  
Solaris 64 bit
  
Terabytes
  
JVMMemory: Heap + PermGen

ReservedOSMemory: Native heap,JNI

便可推导出单个JVM Instance可支持的最大线程数的估计值: 

(MaxProcessMemory<固定值> – Xms<初始化值,最小值> – XX:PermSize<初始化值,最小值> – 100m<估算值>) / Xss = Number of threads<最大值>

在本地(32bit windows)试了试,可达的线程的最大值差不多就是这个数,它不受物理内存的限制,会利用虚拟内存,从任务管理器看到memory已经是5500 m左右了 (开了两个jvm) ,我机器的物理内存是2g,也不知道这个准不准,后来还抛出了"unable to create new native thread"的兄弟"Exception in thread "CompilerThread0" java.lang.OutOfMemoryError: requested 471336 bytes for Chunk::new. Out of swap space?"。

本地测完了后,就该轮到dev环境了,linux2.6,64bit,双核,8G (虚拟机) ,总的物理内存是16g。在上面整了一下,创建到了15000多个线程的时候挂掉了。此时其他application也不能创建新的线程,而且db也报错了,操作系统不能fork新的线程了。这应该是操作系统的哪里限制了新线程的创建,

·         max thread,linux2.6似乎是32000

·         最大可用内存: 物理内存+虚拟内存

·         配置,在linux可以限制可用资源的大小,show一下这些参数

core file size          (blocks, -c) 0

data seg size           (kbytes, -d) unlimited

file size               (blocks, -f) unlimited

pending signals                 (-i) 1024

max locked memory       (kbytes, -l) 32

max memory size         (kbytes, -m) unlimited

open files                      (-n) 65536

pipe size            (512 bytes, -p) 8

POSIX message queues     (bytes, -q) 819200

stack size              (kbytes, -s) 10240

cpu time               (seconds, -t) unlimited

max user processes              (-u) 16384

virtual memory          (kbytes, -v) unlimited

file locks                      (-x) unlimited
  
为了进一步确定在linux上一个jvm因为达到了最大寻址空间OOM了,不会影响其他jvm,我在Linux做了进一步测试,一开始用Sun文档中说的最大寻址空间3G试了一下,发现根本不对,达到了3G后还是非常high地在创建新的线程。于是出动超级无敌变态的JVM初始化配置。

oracle   27408 27017 12 13:45 ?        00:00:07 /home/oracle/ias1013/FWAPP/FWDev/jdk/bin/java -server -Xmx4096m -Xms4096m -XX:+HeapDumpOnOutOfMemoryError -XX:PermSize=4096m -XX:MaxPermSize=4096m -XX:HeapDumpPath=/home/oracle/ias1013/FWAPP/FWDev/j2ee/OC4J_OOMTest/workEnv/log -Xss100m
  
结果在create 3379个线程后,"unable to create new native thread"出现了,这时其他jvm都是可以create新线程的。如果按照上面公式计算,linux 64bit,2.6kernel,它的最大寻址空间肯定超过了300g,当然应该还没有达到可用内存的限制,因为其他JVM还能create新线程。

我还怀疑是不是oracle application server上的某个配置参数限制了总的线程数,影响了所有application,但我们的产品环境一个application就是一个单独的application server。

现在基本上可以确定是操作系统哪里设置错了,我想System team的帅哥们应该把产品环境的某个参数配置错了,系统本身的影响肯定不会有了,因为产品环境上我们只create了800左右个线程,就OOM了,那应该就是配置的问题了,怀疑的参数有下面四个

max user processes              (-u) 2048

virtual memory          (kbytes, -v) unlimited

max memory size         (kbytes, -m) unlimited

stack size              (kbytes, -s) 10240

最后发现只有max user processes 和virtual memory对总的线程数有影响,我把max user processes降到2048后,发现此时只能创建 2000左右个线程了(Xms64m, Xss1m),进一步地把virtual memory下调到2048000K发现能创建的就更少了1679 (Xms64m, Xss1m) ,而它只会对当前shell起作用,而多个application server应该是不同的shell,所以他是打酱油的。另外两个参数好像就是来做做俯卧撑的,操作系统stack size是不应该会有什么影响,我们把它上调到102400,还是可以创建2000左右的线程数 (max user processes) ,因为java有自己的线程模型,它的栈的大小是用Xss来控制的。Max memory size不知道是啥东西,照理说如果是最大内存应该不会只在旁边做俯卧撑,那这个参数到底是春哥还是曾哥,查了一下man ulimit,有下面解释

-a     All current limits are reported

-c     The maximum size of core files created

-d     The maximum size of a process data segment

-f     The maximum size of files created by the shell

-l     The maximum size that may be locked into memory

-m     The maximum resident set size (has no effect on Linux)

-n     The maximum number of open file descriptors (most systems do not allow this value to be set)

-p     The pipe size in 512-byte blocks (this may not be set)

-s     The maximum stack size

-t     The maximum amount of cpu time in seconds

-u     The maximum number of processes available to a single user

-v     The maximum amount of virtual memory available to the shell

"Has no effect on Linux"就足以证明它确实只是来做做俯卧撑的。最后查出只有"max user processes"会对所有application能创建总的线程数有限制。