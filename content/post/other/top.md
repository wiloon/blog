---
title: top command
author: "-"
date: 2013-01-06T13:44:27+00:00
url: top
categories:
  - Linux
tags:
  - reprint
  - remix
  - command
---
## top command

top 命令是常用的性能监控工具之一，用于监控系统整体性能和进程信息.
top 界面分为两个部份，上面部份显示关于系统整体性能，下面部份显示各进程信息。

第一行显示的内容和 uptime 命令一样， 可以显示和折叠 cpu 使用信息.

- top:  这个没有什么意思，只是个名称而已
- 01:47:56 :  系统当前时间
- up 1:26 :  系统开机到现在经过了多少时间
- 2 users:  当前2用户在线
- load average: 0.00,0.00,0.00:  系统1分钟、5分钟、15分钟的 CPU 负载信息

- Tasks:
  - 38 total: 当前有38个任务/进程
  - 1 running: 1个进程正在运行
  - 37 sleeping: 37个进程睡眠
  - 0 stopped: 停止的进程数
  - 0 zombie: 僵死的进程数

### 0 zombie: 僵死的进程数

zombie 进程 : 不是异常情况。 一个进程从创建到结束在最后那一段时间遍是僵尸。留在内存中等待父进程取的东西便是僵尸。任何程序都有僵尸状态，它占用一点内存资源，仅仅是表象而已不必害怕。如果程序有问题有机会遇见，解决大批量僵尸简单有效的办法是重起。kill是无任何效果的stop模式: 与sleep进程应区别，sleep会主动放弃cpu，而stop是被动放弃cpu ，例单步跟踪，stop(暂停)的进程是无法自己回到运行状态的。

### Cpu(s): 表示这一行显示CPU总体信息

- us: 用户态进程占用 CPU 时间百分比，不包含 renice 值为负的任务占用的CPU的时间。 CPU 消耗在 User space 的时间百分比
- sy: 内核线程占用 CPU 时间百分比, 消耗在 Kernel space 的时间百分比。
- ni: renice 值为负的任务的用户态进程的CPU时间百分比。nice 是优先级的意思, 表示被 nice 命令改变优先级的任务所占的百分比
- id: 空闲CPU时间百分比
- wa: IO wait 的缩写, io wait 所占的百分比, CPU 等待外部 I/O 的时间百分比，这段时间 CPU 不能干其他事，但是也没有执行运算，这个值太高就说明外部设备有问题
- hi: CPU硬中断时间百分比, hardware interrupt 的缩写，CPU 响应硬件中断请求的时间百分比
- si: CPU软中断时间百分比, software interrupt 的缩写，CPU 响应软件中断请求的时间百分比
- st: 虚拟cpu等待实际cpu的时间的百分比, stole time 的缩写，该项指标只对虚拟机有效，表示分配给当前虚拟机的 CPU 时间之中，被同一台物理机上的其他虚拟机偷走的时间百分比

```bash
#查看 user0 用户进程
top -u user0

#显示线程
top -H -p PID
  
printf "%x\n" tid
```

### 交互命令

- P: 按 CPU 使用率排序
- T: 按 MITE+ 排序
- M: 按 %MEM 排序
- f: 编辑基本视图中的显示字段
- Space: 立即刷新显示
- h: 显示帮助
- k: 杀死某进程。你会被提示输入进程 ID 以及要发送给它的信号。 一般的终止进程可以使用15信号;如果不能正常结束那就使用信号9强制结束该进程。默认值是信号15。在安全模式中此命令被屏蔽。

[n] 改变显示的进程数量。你会被提示输入数量。

[u] 按用户排序。

`[o][O]` 改变显示项目的顺序。

[Ctrl+L] 擦除并且重写屏幕。

[q] 退出程序。

[r] 重新安排一个进程的优先级别。系统提示用户输入需要改变的进程PID以及需要设置的进程优先级值。输入一个正值将使优先级降低，反之则可以使该进程拥有更高的优先权。默认值是10。

[S] 切换到累计模式。

[s] 改变两次刷新之间的延迟时间。系统将提示用户输入新的时间，单位为s。如果有小数，就换算成m s。输入0值则系统将不断刷新，默认值是5 s。需要注意的是如果设置太小的时间，很可能会引起不断刷新，从而根本来不及看清显示的情况，而且系统负载也会大大增加。

## 列表字段

### PID

进程ID

### USER

进程所有者的用户名

### PRI/PR

每个进程的优先级别

### NI

每个优先级的值
NI 是优先值，是用户层面的概念， PR是进程的实际优先级， 是给内核 (kernel) 看 (用) 的。

一般情况下，PR=NI+20, 如果一个进程的优先级PR是20， 那么它的NI(nice)值就是20-20=0。

可以通过改变NI来改变PR: PRI(new) = PRI(old) + nice

### VIRT

进程使用的虚拟内存总量，单位 KiB (按 f 键能看到 VIRT的单位是KiB)
VIRT: virtual memory usage。Virtual这个词很神，一般解释是: virtual adj.虚的, 实质的, [物]有效的, 事实上的。到底是虚的还是实的？让Google给Define之后，将就明白一点，就是这东西还是非物质的，但是有效果的，不发生在真实世界的，发生在软件世界的等等。这个内存使用就是一个应用占有的地址空间，只是要应用程序要求的，就全算在这里，而不管它真的用了没有。写程序怕出错，又不在乎占用的时候，多开点内存也是很正常的。

### RES, resident memory usage

进程使用的、未被换出的物理内存大小，单位 kb。RES = CODE + DATA
常驻内存。这个值就是该应用程序真实使用的内存，但还有两个小问题，一是有些东西可能放在交换分区上了 (SWAP), 二是有些内存可能是共享的。

### SHR, shared memory

共享内存。就是说这一块内存空间有可能也被其他应用程序使用着；而 VIRT - SHR 似乎就是这个程序所要求的并且没有共享的内存空间。

### DATA

单位 KiB
DATA: 数据占用的内存。如果top没有显示，按f键可以显示出来。这一块是真正的该程序要求的数据空间，是真正在运行中要使用的。

### Men: 内存占比

256412k total: 物理内存总量

30156k used: 使用的物理内存量

226256 free: 空闲的物理内存量

8176k buffers: 用作内核缓存的物理内存量

### Swap: 交换空间

337356k total: 交换区总量

0k used: 使用的交换区量

337356k free: 空闲的交换区量

12160k cached: 缓冲交换区总量

cpu states:

nice: 让出百分比irq: 中断处理占用

idle: 空间占用百分比 iowait: 输入输出等待(如果它很大说明外存有瓶颈，需要升级硬盘(SCSI))

Mem: 内存情况

设计思想: 把资源省下来不用便是浪费，如添加内存后free值会不变，buff值会增大。 判断物理内存够不够，看交换分区的使用状态。

### 字段

SIZE    进程的代码大小加上数据大小再加上堆栈空间大小的总数，单位是KB RSS 进程占用的物理内存的总数量，单位是KB
SHARE   进程使用共享内存的数量
STAT    进程的状态。其中S代表休眠状态;D代表不可中断的休眠状态;R代表运行状态;Z代表僵死状态;T代表停止或跟踪状态
%CPU    进程自最近一次刷新以来所占用的CPU时间和总时间的百分比
%MEM    进程占用的物理内存占总内存的百分比
TIME    进程自启动以来所占用的总CPU时间
CPU     CPU标识
COMMAND 进程的命令名称

---

>[https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/top.html](https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/top.html)  
>[http://www.cnblogs.com/gaojun/p/3406096.html](http://www.cnblogs.com/gaojun/p/3406096.html)
>[http://www.vimer.cn/2009/12/linux%E4%B8%8B%E7%9A%84%E5%86%85%E5%AD%98%E6%9F%A5%E7%9C%8B%EF%BC%88virtresshrdata%E7%9A%84%E6%84%8F%E4%B9%89%EF%BC%89.html](http://www.vimer.cn/2009/12/linux%E4%B8%8B%E7%9A%84%E5%86%85%E5%AD%98%E6%9F%A5%E7%9C%8B%EF%BC%88virtresshrdata%E7%9A%84%E6%84%8F%E4%B9%89%EF%BC%89.html)
>[http://blog.csdn.net/u011547375/article/details/9851455](http://blog.csdn.net/u011547375/article/details/9851455)
>[http://www.cnblogs.com/gaojun/p/3406096.html](http://www.cnblogs.com/gaojun/p/3406096.html)
>[http://www.cnblogs.com/seasonsluo/p/java_virt.html](http://www.cnblogs.com/seasonsluo/p/java_virt.html)  
>[https://www.jianshu.com/p/c5ac9ade3e68](https://www.jianshu.com/p/c5ac9ade3e68)
