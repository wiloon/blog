---
title: ps
author: "-"
date: 2011-07-20T07:50:28+00:00
url: ps
categories:
  - Linux
tags:
  - remix

---
## ps
Linux中的 ps 命令是 Process Status 的缩写。

### 输出指定的字段
```bash
ps -eo pid, ppid, command
ps -e -o 'pid,comm,args,pcpu,rsz,vsz,stime,user,uid' 其中 rsz 是是实际内存
ps -e -o 'pid,comm,args,pcpu,rsz,vsz,stime,user,uid' | grep oracle | sort -nrk5
```
其中 rsz 为实际内存，上例实现按内存排序，由大到小
  
### ububtu install ps command

   apt install procps

http://blog.fpliu.com/it/software/procps

ps命令用来列出系统中当前运行的那些进程。ps命令列出的是当前那些进程的快照，就是执行ps命令的那个时刻的那些进程，如果想要动态的显示进程信息，就可以使用top命令。

要对进程进行监测和控制，首先必须要了解当前进程的情况，也就是需要查看当前进程，而 ps 命令就是最基本同时也是非常强大的进程查看命令。使用该命令可以确定有哪些进程正在运行和运行的状态、进程是否结束、进程有没有僵死、哪些进程占用了过多的资源等等。总之大部分信息都是可以通过执行该命令得到的。

ps 为我们提供了进程的一次性的查看，它所提供的查看结果并不动态连续的；如果想对进程时间监控，应该用 top 工具。

kill 命令用于杀死进程。

linux 上进程有5种状态: 
1. 运行 (正在运行或在运行队列中等待) 
2. 中断 (休眠中, 受阻, 在等待某个条件的形成或接受到信号) 
3. 不可中断 (收到信号不唤醒和不可运行, 进程必须等待直到有中断发生) 
4. 僵死 (进程已终止, 但进程描述符存在, 直到父进程调用wait4()系统调用后释放) 
5. 停止 (进程收到SIGSTOP, SIGSTP, SIGTIN, SIGTOU信号后停止运行运行) 

ps工具标识进程的5种状态码: 
- R 运行 runnable (on run queue) 
- S 中断 sleeping 
- D 不可中断 uninterruptible sleep (usually IO) 
- Z 僵死 a defunct ("zombie") process 
- T 停止 traced or stopped 


**默认情况下，ps 不会显示很多进程信息，只是列出与当前终端会话相关的进程**

```bash
# ps -ef 默认按 PID排序, 最近启动的进程会列在末尾.
ps -ef
ps -efl
# 
ps -aux 

#进程启动时间  
ps -p <PID> -o lstart  
ps -ef  
ps f 用ASCII字符显示树状结构，表达程序间的相互关系。
ps -Lf <PID> 查看对应进程下的线程
### 指定显示的字段
ps -eo pid,ppid,command
```

### 参数
    -e, -A  显示所有进程, 默认情况下，ps 不会显示很多进程信息，只是列出与当前终端会话相关的进程, -e 参数会显示系统所有进程
    -j     作业格式
    -l     长格式 (有F,wchan,C,PRI,NI 等字段) 
    a      显示现行终端机下的所有程序，包括其他用户的程序。  
    e      列出程序时，显示每个程序所使用的环境变量。  
    f      用 ASCII 字符显示树状结构，表达程序间的相互关系。  
    u      以用户为主的格式来显示程序状况。  
    x      显示所有程序，不以终端机来区分. 
    -L     Show threads, possibly with LWP and NLWP columns
    -T     显示线程 (Show threads, possibly with SPID column) “SID”栏表示线程ID，而“CMD”栏则显示了线程名称。
    -o, o, --format <format>     用户自定义格式,输出指定的字段

#### 输出格式控制
    -f  打印完整格式的列表, -f 参数可以跟其它 UNIX-style 参数一起使用(如: ps -fa, ps -fx ...), 附加 -f 之后会输出一些额外的字段, 并且会打印进程的完整的命令行参数.

### Head 标头
    F           代表这个程序的旗标 (flag)， 4 代表使用者为 super user  
    S           代表这个程序的状态 (STAT)，关于各 STAT 的意义将在内文介绍  
    USER        用户名  
    UID         用户ID (User ID)   
    PID         进程ID (Process ID)   
    PPID        父进程的进程ID (Parent Process id)   
    SID         会话ID (Session id)   
    %CPU        进程的cpu占用率
    C           CPU 使用的资源百分比  
    %MEM        进程的内存占用率  
    VSZ         进程所使用的虚存的大小 (Virtual Size)   
    RSS         进程使用的驻留集大小或者是实际内存的大小，Kbytes字节。 系统在内存分配的时候，其实并没有申请相应的物理页帧，只有在真正赋值的时候才会申请物理页帧。这也是 VSZ (进程虚拟内存大小) 和 RSS (常驻物理内存大小) 的最大区别。

    TTY         与进程关联的终端 (tty) , 登入者的终端机位置
    STAT        进程的状态: 进程状态使用字符表示的 (STAT的状态码) 
    START       进程启动时间和日期  
    TIME        进程使用的总cpu时间  
    COMMAND     正在执行的命令行命令  
    NI          优先级(Nice)   
    PRI         进程优先级编号(Priority)   
    WCHAN       进程正在睡眠的内核函数名称；该函数的名称是从/root/system.map文件中获得的。  
    FLAGS       与进程相关的数字标识    
    ADDR        这个是 kernel function，指出该程序在内存的那个部分。如果是个 running的程序，一般就是 "-"  
    SZ          使用掉的内存大小  
    TIME        使用掉的 CPU 时间。  
    CMD         命令的名称和参数
    UID         User ID
    PID         processid,进程标识符
    PPID        parent processid，父进程标识符2，
    LWP         light weight process or thread， 轻量级进程, alias spid, tid
    NLWP        number of lwps(threads) in the process, 进程中线程的数量
    MAJFL is the major page fault count,

### STAT 进程的状态
    R 运行    Runnable (on run queue)            正在运行或在运行队列中等待。
    S 睡眠    Sleeping                休眠中, 受阻, 在等待某个条件的形成或接受到信号。
    I 空闲    Idle
    Z 僵死    Zombie (a defunct process)        进程已终止, 但进程描述符存在, 直到父进程调用wait4()系统调用后释放。
    D 不可中断    Uninterruptible sleep (ususally IO)    收到信号不唤醒和不可运行, 进程必须等待直到有中断发生。不可中断的睡眠，通常是I/O
    T 终止    Terminate                进程收到SIGSTOP, SIGSTP, SIGTIN, SIGTOU信号后停止运行运行。 停止或被追踪 terminate终止
    P 等待交换页
    W 无驻留页    has no resident pages        没有足够的记忆体分页可分配。换出,表示当前页面不在内存 (从内核2.6开始无效) 
    X 死掉的进程
    < 高优先级进程 
    N 低优先级进程 
    L 内存锁页    Lock                有记忆体分页分配并缩在记忆体内
    s 进程的领导者 (在它之下有子进程) ；
    l 多进程的 (使用 CLONE_THREAD, 类似 NPTL pthreads) 
    + 位于后台的进程组 

### CPU占用最多的前10个进程
    ps auxw|head -1;ps auxw|sort -rn -k3|head -10
### 内存消耗最多的前10个进程
    ps auxw|head -1;ps auxw|sort -rn -k4|head -10
### 虚拟内存使用最多的前10个进程
    ps auxw|head -1;ps auxw|sort -rn -k5|head -10

### 也可以试试

ps auxw -sort=rss
  
ps auxw -sort=%cpu
 

串行端口终端 (/dev/ttySn) 
  
伪终端 (/dev/pty/) 
  
控制终端 (/dev/tty) 
  
控制台终端 (/dev/ttyn,   /dev/console) 
  
虚拟终端(/dev/pts/n)

### ps aux, ps -ef

Linux下显示系统进程的命令ps，最常用的有ps -ef 和ps aux。这两个到底有什么区别呢？两者没太大差别，讨论这个问题，要追溯到Unix系统中的两种风格，

System Ｖ风格和BSD 风格，ps aux最初用到Unix Style中(BSD的格式)，而ps -ef被用在System V Style中，两者输出略有不同。现在的大部分Linux系统都是可以同时使用这两种方式的。
>https://www.cnblogs.com/5201351/p/4206461.html

## ps aux

- RSS

RSS:RSS is Resident Set Size, the non-swapped physical memory used by process.

rss        RSS      resident set size, the non-swapped physical memory that a
                    task has used (in kiloBytes). (alias rssize, rsz).

版权声明：本文为CSDN博主「逝鸿」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_21127313/article/details/79877483

>https://www.cnblogs.com/hunttown/p/5452253.html
>http://elinux.org/Runtime_Memory_Measurement   
>https://www.cnblogs.com/peida/archive/2012/12/19/2824418.html  
>https://man7.org/linux/man-pages/man1/ps.1.html