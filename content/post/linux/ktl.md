---
author: "-"
date: "2021-05-05 08:36:31" 
title: kernel thread, 内核线程, KTL
url: "ktl"
categories:
  - OS
tags:
  - thread
  - kernel
---
## kernel thread, 内核线程, KTL

## 内核线程, ktl

### 为什么需要内核线程

Linux 内核可以看作一个服务进程(管理软硬件资源，响应用户进程的种种合理以及不合理的请求).

内核需要多个执行流并行，为了防止可能的阻塞，支持多线程是必要的.

内核线程就是内核的分身，一个分身可以处理一件特定事情。内核线程的调度由内核负责，一个内核线程处于阻塞状态时不影响其他的内核线程，因为其是调度的基本单位。

这与用户线程是不一样的。因为内核线程只运行在内核态

因此，它只能使用大于P AGE_OFFSET (传统的x86_32上是3G) 的地址空间。

内核线程概述
内核线程是直接由内核本身启动的进程。内核线程实际上是将内核函数委托给独立的进程，它与内核中的其他进程"并行"执行。内核线程经常被称之为内核守护进程。

他们执行下列任务

- 周期性地将修改的内存页与页来源块设备同步
- 如果内存页很少使用，则写入交换区
- 管理延时任务 (Deferred work）,如:中断的下半部
- 实现文件系统的事务日志

内核线程主要有两种类型

- 线程启动后一直等待，直至内核请求线程执行某一特定操作。
- 线程启动后按周期性间隔运行，检测特定资源的使用，在用量超出或低于预置的限制时采取行动。

它们在CPU的管态执行，而不是用户态。

它们只可以访问虚拟地址空间的内核部分 (高于TASK_SIZE的所有地址) ，但不能访问用户空间

内核线程的进程描述符 task_struct
task_struct 进程描述符中包含两个跟 **进程地址空间** 相关的字段 mm, active_mm

```c
struct task_struct
{
    // ...
    struct mm_struct *mm;
    struct mm_struct *avtive_mm;
    //...
};
```

大多数计算机上系统的全部虚拟地址空间分为两个部分: 供用户态程序访问的虚拟地址空间和供内核访问的内核空间。每当内核执行上下文切换时, 虚拟地址空间的用户层部分都会切换, 以便当前运行的进程匹配, 而内核空间不会放生切换。

### mm

对于普通用户进程来说，mm 指向虚拟地址空间的用户空间部分，而对于内核线程，mm 为NULL。这为优化提供了一些余地, 可遵循所谓的惰性 TLB 处理(lazy TLB handing)。

### active_mm

active_mm 主要用于优化，由于内核线程不与任何特定的用户层进程相关，内核并不需要倒换虚拟地址空间的用户层部分，保留旧设置即可。由于内核线程之前可能是任何用户层进程在执行，故用户空间部分的内容本质上是随机的，内核线程决不能修改其内容，故将mm设置为NULL，同时如果切换出去的是用户进程，内核将原来进程的 mm 存放在新内核线程的 active_mm 中，因为某些时候内核必须知道用户空间当前包含了什么。

### 惰性 TLB 进程

为什么没有 mm 指针的进程称为惰性 TLB 进程?

假如内核线程之后运行的进程与之前是同一个, 在这种情况下, 内核并不需要修改用户空间地址表。地址转换后备缓冲器(即TLB)中的信息仍然有效。只有在内核线程之后, 执行的进程是与此前不同的用户层进程时, 才需要切换(并对应清除TLB数据)。

内核线程和普通的进程间的区别在于内核线程没有独立的地址空间，mm指针被设置为NULL；它只在 内核空间运行，从来不切换到用户空间去；并且和普通进程一样，可以被调度，也可以被抢占。

### 内核线程的创建

创建内核线程接口的演变
内核线程可以通过两种方式实现:

古老的接口 kernel_create 和 daemonize

将一个函数传递给 kernel_thread 创建并初始化一个 task，该函数接下来负责帮助内核调用daemonize 已转换为内核守护进程，daemonize随后完成一些列操作, 如该函数释放其父进程的所有资源，不然这些资源会一直锁定直到线程结束。阻塞信号的接收, 将init用作守护进程的父进程

更加现在的方法kthead_create和kthread_run

创建内核更常用的方法是辅助函数 kthread_create，该函数创建一个新的内核线程。最初线程是停止的，需要使用 wake_up_process启动它。

使用kthread_run，与kthread_create不同的是，其创建新线程后立即唤醒它，其本质就是先用kthread_create创建一个内核线程，然后通过wake_up_process唤醒它

### 2号进程 kthreadd 的诞生

早期的 kernel_create 和daemonize接口

在早期的内核中, 提供了kernel_create和daemonize接口, 但是这种机制操作复杂而且将所有的任务交给内核去完成。

但是这种机制低效而且繁琐, 将所有的操作塞给内核, 我们创建内核线程的初衷不本来就是为了内核分担工作, 减少内核的开销的么

### Workqueue 机制

因此在linux-2.6以后, 提供了更加方便的接口kthead_create和kthread_run, 同时将内核线程的创建操作延后, 交给一个工作队列workqueue, 参见<http://lxr.linux.no/linux+v2.6.13/kernel/kthread.c#L21>，

Linux中的workqueue机制就是为了简化内核线程的创建。通过kthread_create并不真正创建内核线程, 而是将创建工作create work插入到工作队列helper_wq中, 随后调用 workqueue 的接口就能创建内核线程。并且可以根据当前系统CPU的个数创建线程的数量，使得线程处理的事务能够并行化。workqueue是内核中实现简单而有效的机制，他显然简化了内核daemon的创建，方便了用户的编程.

工作队列 (workqueue) 是另外一种将工作推后执行的形式.工作队列可以把工作推后，交由一个内核线程去执行，也就是说，这个下半部分可以在进程上下文中执行。最重要的就是工作队列允许被重新调度甚至是睡眠。

具体的信息, 请参见

>Linux workqueue 工作原理

### 2号进程 kthreadd

但是这种方法依然看起来不够优美, 我们何不把这种创建内核线程的工作交给一个特殊的内核线程来做呢？

于是 linux-2.6.22 引入了 kthreadd 进程, 并随后演变为2号进程, 它在系统初始化时同1号进程一起被创建 (当然肯定是通过kernel_thread), 参见 rest_init 函数, 并随后演变为创建内核线程的真正建造师, 参见kthreadd和kthreadd函数, 它会循环的是查询工作链表static LIST_HEAD(kthread_create_list);中是否有需要被创建的内核线程, 而我们的通过kthread_create执行的操作, 只是在内核线程任务队列kthread_create_list中增加了一个create任务, 然后会唤 kthreadd进程来执行真正的创建操作
内核线程会出现在系统进程列表中, 但是在ps的输出中进程名command由方括号包围, 以便与普通进程区分。

使用 ps -eo pid,ppid,command, 我们可以看到系统中, 所有内核线程都用[]标识, 而且这些进程父进程id均是2, 而2号进程kthreadd的父进程是0号进程

### kernel_thread

kernel_thread是最基础的创建内核线程的接口, 它通过将一个函数直接传递给内核来创建一个进程, 创建的进程运行在内核空间, 并且与其他进程线程共享内核虚拟地址空间

kernel_thread的实现经历过很多变革
早期的kernel_thread执行更底层的操作, 直接创建了task_struct并进行初始化,

引入了kthread_create和kthreadd 2号进程后, kernel_thread的实现也由统一的_do_fork(或者早期的do_fork)托管实现

早期实现

早期的内核中, kernel_thread并不是使用统一的 do_fork或者_do_fork这一封装好的接口实现的, 而是使用更底层的细节

kthreadd is a daemon thread that runs in kernel space. The reason is that kernel needs to some times create threads but creating thread in kernel is very tricky. Hence kthreadd is a thread that kernel uses to spawn newer threads if required from there . This thread can access userspace address space also but should not do so . Its managed by kernel...

参见

<http://lxr.free-electrons.com/source/kernel/fork.c?v=2.4.37#L613>

我们可以看到它内部调用了更加底层的 arch_kernel_thread创建了一个线程

arch_kernel_thread

其具体实现请参见

<http://lxr.free-electrons.com/ident?v=2.4.37;i=arch_kernel_thread>

但是这种方式创建的线程并不适合运行，因此内核提供了daemonize函数, 其声明在include/linux/sched.h中

//  <http://lxr.free-electrons.com/source/include/linux/sched.h?v=2.4.37#L800>
extern void daemonize(void);

定义在kernel/sched.c

<http://lxr.free-electrons.com/source/kernel/sched.c?v=2.4.37#L1326>

主要执行如下操作

该函数释放其父进程的所有资源，不然这些资源会一直锁定直到线程结束。

阻塞信号的接收

将init用作守护进程的父进程

我们可以看到早期内核的很多地方使用了这个接口, 比如

可以参见

<http://lxr.free-electrons.com/ident?v=2.4.37;i=daemonize>

我们将了这么多kernel_thread, 但是我们并不提倡我们使用它, 因为这个是底层的创建内核线程的操作接口, 使用kernel_thread在内核中执行大量的操作, 虽然创建的代价已经很小了, 但是对于追求性能的linux内核来说还不能忍受

因此我们只能说kernel_thread是一个古老的接口, 内核中的有些地方仍然在使用该方法, 将一个函数直接传递给内核来创建内核线程

新版本的实现

于是linux-3.x下之后, 有了更好的实现, 那就是

延后内核的创建工作, 将内核线程的创建工作交给一个内核线程来做, 即kthreadd 2号进程

但是在kthreadd还没创建之前, 我们只能通过kernel_thread这种方式去创建,
同时kernel_thread的实现也改为由_do_fork(早期内核中是do_fork)来实现, 参见kernel/fork.c

pid_t kernel_thread(int (*fn)(void*), void *arg, unsigned long flags)
{
    return _do_fork(flags|CLONE_VM|CLONE_UNTRACED, (unsigned long)fn,
            (unsigned long)arg, NULL, NULL, 0);
}

kthread_create
struct task_struct *kthread_create_on_node(int (*threadfn)(void *data),
void*data,
                                          int node,
                                          const char namefmt[], ...);

# define kthread_create(threadfn, data, namefmt, arg...) \
       kthread_create_on_node(threadfn, data, NUMA_NO_NODE, namefmt, ##arg)

创建内核更常用的方法是辅助函数kthread_create，该函数创建一个新的内核线程。最初线程是停止的，需要使用wake_up_process启动它。

kthread_run
/**

- kthread_run - create and wake a thread.
- @threadfn: the function to run until signal_pending(current).
- @data: data ptr for @threadfn.
- @namefmt: printf-style name for the thread.
*
- Description: Convenient wrapper for kthread_create() followed by
- wake_up_process().  Returns the kthread or ERR_PTR(-ENOMEM).
 */
# define kthread_run(threadfn, data, namefmt, ...)                          \
({                                                                         \
struct task_struct*__k                                            \
            = kthread_create(threadfn, data, namefmt, ## **VA_ARGS**); \
    if (!IS_ERR(__k))                                                  \
            wake_up_process(__k);                                      \
    __k;                                                               \
})

使用kthread_run，与kthread_create不同的是，其创建新线程后立即唤醒它，其本质就是先用kthread_create创建一个内核线程，然后通过wake_up_process唤醒它

内核线程的退出
线程一旦启动起来后，会一直运行，除非该线程主动调用do_exit函数，或者其他的进程调用kthread_stop函数，结束线程的运行。

    int kthread_stop(struct task_struct *thread);
kthread_stop() 通过发送信号给线程。

如果线程函数正在处理一个非常重要的任务，它不会被中断的。当然如果线程函数永远不返回并且不检查信号，它将永远都不会停止。

在执行kthread_stop的时候，目标线程必须没有退出，否则会Oops。原因很容易理解，当目标线程退出的时候，其对应的task结构也变得无效，kthread_stop引用该无效task结构就会出错。

为了避免这种情况，需要确保线程没有退出，其方法如代码中所示:

thread_func()
{
    // do your work here
    // wait to exit
    while(!thread_could_stop())
    {
           wait();
    }
}

exit_code()
{
     kthread_stop(_task);   //发信号给task，通知其可以退出了
}

这种退出机制很温和，一切尽在thread_func()的掌控之中，线程在退出时可以从容地释放资源，而不是莫名其妙地被人"暗杀"。
————————————————
版权声明: 本文为CSDN博主「CHENG Jian」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/gatieme/article/details/51589205>

### idle进程(PID = 0)

### init进程(PID = 1)

### kthreadd(PID = 2)

kthreadd进程由idle通过kernel_thread创建，并始终运行在内核空间, 负责所有内核线程的调度和管理
它的任务就是管理和调度其他内核线程kernel_thread, 会循环执行一个kthreadd的函数，该函数的作用就是运行kthread_create_list全局链表中维护的kthread, 当我们调用kernel_thread创建的内核线程会被加入到此链表中，因此所有的内核线程都是直接或者间接的以kthreadd为父进程

所有其它的内核线程的ppid 都是 2，也就是说它们都是由kthreadd thread创建的
所有的内核线程在大部分时间里都处于阻塞状态(TASK_INTERRUPTIBLE)只有在系统满足进程需要的某种资源的情况下才会运行

### ksoftirq/n

处理软中断  
<http://abcdxyzk.github.io/blog/2015/01/03/kernel-irq-ksoftirqd/>  

softirq实际上也是一种注册回调的机制，ps –elf 可以看到注册的函数由一个守护进程 (ksoftirgd) 专门来处理，而且是每个cpu一个守护进程。

### kworker

显示的格式kworker/%u:%d%s

        u：是unbound的缩写，代表没有绑定特定的CPU，kworker /u2:0中的 2 是 work_pool 的ID。  
        不带u的就是绑定特定cpu的workerq，它在init_workqueues中初始化，给每个cpu分配worker，如果该worker的nice小于0，说明它的优先级很高，所以就加了H属性。  
        具有负面价值的勤劳工人的名字后缀为'H'。

————————————————
版权声明：本文为CSDN博主「lyblyblyblin」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/lyblyblyblin/article/details/79346459>

kworker意思是’Linux kernel doing work’(系统调用，processing system calls)，它是内核工作线程的’占位符’进程，它实际上执行内核的大部分工作，如中断、计时器、I/O等，CPU中’system’时间大部分由此产生。在系统中，一般会出现多个kworker进程，如kworker/0:1跟第一个cpu核心有关，依次类推。

在日常维护中，kworker进程有时会占用大量的io或cpu。

### migration

migration: 每个处理器核对应一个migration内核线程，主要作用是作为相应CPU核的迁移进程，用来执行进程迁移操作，内核中的函数是migration_thread()。属于2.6内核的负载平衡系统，该进程在系统启动时自动加载 (每个 cpu 一个) ，并将自己设为 SCHED_FIFO 的实时进程，然后检查 runqueue::migration_queue 中是否有请求等待处理，如果没有，就在 TASK_INTERRUPTIBLE 中休眠，直至被唤醒后再次检查。migration_queue仅在set_cpu_allowed() 中添加，当进程 (比如通过 APM 关闭某 CPU 时) 调用set_cpu_allowed()改变当前可用 cpu，从而使某进程不适于继续在当前 cpu 上运行时，就会构造一个迁移请求数据结构 migration_req_t，将其植入进程所在 cpu 就绪队列的migration_queue 中，然后唤醒该就绪队列的迁移 daemon (记录在runqueue::migration_thread 属性中) ，将该进程迁移到合适的cpu上去在目前的实现中，目的 cpu 的选择和负载无关，而是"any_online_cpu(req->task->cpus_allowed)"，也就是按 CPU 编号顺序的第一个 allowed 的CPU。所以，和 load_balance() 与调度器、负载平衡策略密切相关不同，migration_thread() 应该说仅仅是一个 CPU 绑定以及 CPU 电源管理等功能的一个接口。这个线程是调度系统的重要组成部分，也不能被关闭。

### watchdog

每个处理器核对应一个watchdog 内核线程，watchdog用于监视系统的运行，在系统出现故障时自动重新启动系统，包括一个内核 watchdog module 和一个用户空间的 watchdog 程序。在Linux 内核下, watchdog的基本工作原理是: 当watchdog启动后(即/dev/watchdog设备被打开后)，如果在某一设定的时间间隔 (1分钟) 内 /dev/watchdog没有被执行写操作, 硬件watchdog电路或软件定时器就会重新启动系统，每次写操作会导致重新设定定时器。/dev/watchdog是一个主设备号为10， 从设备号130的字符设备节点。 Linux内核不仅为各种不同类型的watchdog硬件电路提供了驱动，还提供了一个基于定时器的纯软件watchdog驱动。如果不需要这种故障处理 机制，或者有相应的替代方案，可以在menuconfig的
   Device Drivers —>
      Watchdog Timer Support
处取消watchdog功能

### kdevtmpfs

this thread populates and maintains a device node tree

### kauditd

内核线程 kauditd 通过 netlink 机制 (NETLINK_AUDIT) 将审计消息定向发送给用户态的审计后台 auditd的主线程，auditd主线程再通过事件队列将审计消息传给审计后台的写log文件线程，写入log文件。另一方面，审计后台还通过一个与 socket 绑定的管道将审计消息发送给audispd应用程序，可把事件传送给其他应用程序做进一步处理。
><https://ixyzero.com/blog/archives/3421.html>

### khungtaskd

khungtaskd 监控TASK_UNINTERRUPTIBLE状态的进程，如果在120s周期内没有切换，就会打印详细信息。
><https://www.cnblogs.com/arnoldlu/p/10529621.html>

### kcompactd*

页面整理

><https://www.coder.work/article/6802420>
><https://blog.csdn.net/gatieme/article/details/51566690>
