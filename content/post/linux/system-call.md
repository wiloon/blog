---
author: "-"
date: "2021-04-15 22:41:14" 
title: "系统调用, System Call"
categories:
  - inbox
tags:
  - reprint
---
## "系统调用, System Call"

# 系统调用
计算机系统的各种硬件资源是有限的，在现代多任务操作系统上同时运行的多个进程都需要访问这些资源，为了更好的管理这些资源进程是不允许直接操作的，所有对这些资源的访问都必须有操作系统控制。也就是说操作系统是使用这些资源的唯一入口，而这个入口就是操作系统提供的系统调用 (System Call) 。在linux中系统调用是用户空间访问内核的唯一手段，除异常和陷入外，他们是内核唯一的合法入口。

一般情况下应用程序通过应用编程接口API，而不是直接通过系统调用来编程。在Unix世界，最流行的API是基于POSIX标准的。

操作系统一般是通过中断从用户态切换到内核态。中断就是一个硬件或软件请求，要求CPU暂停当前的工作，去处理更重要的事情。比如，在x86机器上可以通过int指令进行软件中断，而在磁盘完成读写操作后会向CPU发起硬件中断。

中断有两个重要的属性，中断号和中断处理程序。中断号用来标识不同的中断，不同的中断具有不同的中断处理程序。在操作系统内核中维护着一个中断向量表 (Interrupt Vector Table) ，这个数组存储了所有中断处理程序的地址，而中断号就是相应中断在中断向量表中的偏移量。

**一般地，系统调用都是通过软件中断实现的**，x86系统上的软件中断由int $0x80指令产生，而128号异常处理程序就是系统调用处理程序system_call()，它与硬件体系有关，在entry.S中用汇编写。接下来就来看一下Linux下系统调用具体的实现过程。

### 为什么需要系统调用
linux内核中设置了一组用于实现系统功能的子程序，称为系统调用。系统调用和普通库函数调用非常相似，只是系统调用由操作系统核心提供，运行于内核态，而普通的函数调用由函数库或用户自己提供，运行于用户态。

一般的，进程是不能访问内核的。它不能访问内核所占内存空间也不能调用内核函数。CPU硬件决定了这些 (这就是为什么它被称作"保护模式" (详细参见深入理解计算机系统-之-内存寻址 (二) –存储保护机制 (CPU实模式与保护模式) ) ) 。

为了和用户空间上运行的进程进行交互，内核提供了一组接口。透过该接口，应用程序可以访问硬件设备和其他操作系统资源。这组接口在应用程序和内核之间扮演了使者的角色，应用程序发送各种请求，而内核负责满足这些请求(或者让应用程序暂时搁置)。实际上提供这组接口主要是为了保证系统稳定可靠，避免应用程序肆意妄行，惹出大麻烦。

系统调用在用户空间进程和硬件设备之间添加了一个中间层。该层主要作用有三个: 

它为用户空间提供了一种统一的硬件的抽象接口。比如当需要读些文件的时候，应用程序就可以不去管磁盘类型和介质，甚至不用去管文件所在的文件系统到底是哪种类型。

系统调用保证了系统的稳定和安全。作为硬件设备和应用程序之间的中间人，内核可以基于权限和其他一些规则对需要进行的访问进行裁决。举例来说，这样可以避免应用程序不正确地使用硬件设备，窃取其他进程的资源，或做出其他什么危害系统的事情。

每个进程都运行在虚拟系统中，而在用户空间和系统的其余部分提供这样一层公共接口，也是出于这种考虑。如果应用程序可以随意访问硬件而内核又对此一无所知的话，几乎就没法实现多任务和虚拟内存，当然也不可能实现良好的稳定性和安全性。在Linux中，系统调用是用户空间访问内核的惟一手段；除异常和中断外，它们是内核惟一的合法入口。

Linux 的系统调用主要有以下这些: 

Task       Commands
进程控制    fork(); exit(); wait();
进程通信    pipe(); shmget(); mmap();
文件操作    open(); read(); write();
设备操作    ioctl(); read(); write();
信息维护    getpid(); alarm(); sleep();
安全        chmod(); umask(); chown();



### 从"read"看系统调用的耗时
1. fread和read有何不同
先看两段代码: 
#### fread
```c
#include<stdio.h>
#include<stdlib.h>
FILE* pf = fopen("test.txt", "r");
char buf[2] = { 0 };
int ret = 0;
do 
{
    ret = fread(buf, 1, 1, pf);
} while (ret);
```
#### read
```c
#include<stdio.h>
#include<stdlib.h>
FILE* pf = fopen("test.txt", "r");
char buf[2] = { 0 };
int ret = 0;
do 
{
    ret = read(buf, 1, 1, pf);
} while (ret);
```

两个文件的功能完全一样，打开同一个名为test.file的文件，并逐字节地读取整个文件。
将它们编译后得到的可执行程序fread和read分别在同一台PC (linux系统) 上执行，
fread与read的耗时相差数十倍之多！可见啊~read一个字节这种写法是相当不可取的！

2. 是什么引起的差异

但是，事情为什么会是这样的呢？让我们用strace来看看: 

看到了吧~fread库函数在内部做了缓存，每次读取4096个字节；而read就老老实实一个字节一个字节地读……

那么再想想，我们读的是什么？是磁盘。难道上面提到的差异，就是因为这4096倍的读磁盘次数差而引起的吗？并不是这样。

磁盘是块设备，每次读取的最小单位是块。而当我们通过系统调用读一个字节时，linux会怎么做呢？它会是读取一个块、然后返回一个字节、再把其余字节都丢掉吗？当然不会，这样的操作系统也太拙劣了……

实际上linux的文件系统层 (fs层) 不仅会将每次读的一整块数据缓存下来，还有预读机制 (一次预读多个块，以减少磁盘寻道时间) ，并且缓存的内容是放在文件对应的inode里面，是可以在进程间共享的。 (省略细节若干……) 

那么，fread与read执行的耗时差别来自于哪里呢？从代码看，它们都做了相同次数的函数调用；从内核看，它们都造成了基本上相同的磁盘IO……但是注意到，第一段代码中一共进行了N (N=约24M) 次fread函数调用，产生约N/4096次系统调用；第二段代码中一共进行了N次read函数调用，产生N次系统调用。实际上这里的耗时差就来自于4096倍的系统调用次数差！fread()库函数中缓存的作用并不是减少读磁盘的次数，而是减少系统调用的次数。

由此可见，系统调用比起普通函数调用有很大的开销，编写代码时应当注意避免滥用系统调用。

1. 进一步提高效率
为了进一步减少系统调用的次数，关于读文件的这个问题，我们还可以这样做: 
mmap
```c
#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<unistd.h>
#include<sys/mman,h>
int fd = fopen("test.txt", 0);
struct stat statbuf;
char* start;
char buf[2] = {0};
int ret = 0;
fstat(fd, &statbuf);
start = mmap(NULL, statbuf, st_size, PROT_READ, MAP_PRIVATE, fd, 0);
do 
{
    *buf = start[ret++];
} while (ret < statbuf.st_size);
```

同样是遍历整个文件，但是读文件的过程中不需要使用系统调用，直接把文件当成内存buffer来读就行了。其原理是: mmap的执行，仅仅是在内核中建立了文件与虚拟内存空间的映射关系。用户访问这些虚拟内存空间时，页表里面并没有这些空间的表项，于是CPU产生缺页异常。内核捕捉这些异常，逐渐将文件读入内存，并建立相关的页表项。 (省略细节若干……) 

将其编译后得到的可执行程序mmap和之前的fread、read分别在同一台PC上执行，得到的如果如下: 
在这里插入图片描述
mmap方式与fread方式相比，耗时又减少了好几倍。

4. 为什么
看到这里，我们不禁要问，系统调用为什么就这么耗时呢？系统调用与普通函数调用到底有什么不同？

两者都是在调用处进行跳转，转到被调用的代码中去执行；
系统调用使用的"跳转"指令相对复杂。因为跳转到内核空间去执行时，CPU特权级别需要改变 (否则没有权限访问到内核空间) 。于是，CPU必须封装一条指令，既实现跳转、又实现特权级别的改变，并且还要保证跳转到的地方就是内核代码 (否则用户程序用这个指令假跳一下，自己就拥有特权了) 。而软中断指令恰好能满足这三点要求，所以，X86下实现系统调用的经典方法就是"INT 0x80" (现在好像换sysenter了吧~ 但是指令要做的事情应该不会变) ；
两者都是执行到返回点，然后跳转回到原先的调用点；
系统调用的返回过程还伴随着很多的工作，比如**检查是否需要调度**、是否有**异步信号**需要处理、等等。然后，既然来的时候改变了CPU特权级别，返回的时候还得改回去；
- 两种调用中，调用前后的代码都在**相同的虚拟地址空间**中 (内核空间也属于用户进程所能看到的虚拟地址空间范围内，尽管进程一般情况下没有权限去访问) ，地址空间并没有切换；
运行内核代码时使用的栈是内核栈，系统调用时需要进行**栈的切换**；
两者的参数传递看似相同；
普通函数调用是通过栈来传递参数的；而系统调用是通过寄存器来传递参数，寄存器不够用时才逼不得已使用栈。因为栈要切换，参数传递起来不那么简单； (但是在这一点上，系统调用与普通函数调用的耗时并无太大差异。) 
CPU执行内核代码和执行用户程序代码没什么区别；
但是注意到，内核代码对用户参数是充分的不信任。以read/fread的buffer参数为例，fread库函数一般不会检查buffer参数是否合法。就算想要检查，也没这个能力。他不知道buffer是不是个野指针，不知道buffer的大小是否与len不符，不知道buffer指向的这块内存是否可写……他唯一能做的检查只是buffer是否为NULL，可惜这没什么意义。但是通过系统调用进入内核以后，情况就不同了。前面说到的那些检查，统统都要做，并且每次调用都要不厌其烦地做；
以上几点区别，仅是我目前能够想到的。但是管中窥豹，可见一斑。进入内核以后，要做的事情的确是很多很多。
>版权声明: 本文为cchao985771161原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。
>本文链接: https://blog.csdn.net/cchao985771161/article/details/105767444

### LINUX SYSTEM CALL TABLE FOR X86 64
http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/

### Linux Systemcall Int0x80方式、Sysenter/Sysexit Difference Comparation

1. 系统调用简介
2. Linux系统调用实现方式的演进
3. 通过INT 0x80中断方式进入系统调用
4. 通过sysenter指令方式直接进入系统调用
5. sysenter/sysexit编程示例
6. Linux SCI
7. 系统调用简介

由操作系统实现提供的所有系统调用所构成的集合即程序接口或应用编程接口(Application Programming Interface，API)。是应用程序同系统之间的接口

\linux-3.15.5\arch\x86\kernel\entry_32.S

syscall_call:
    /*
    调用系统函数
    sys_call_table也定义在是一张由指向实现各种系统调用的内核函数的函数指针组成的表: 
    linux-2.6.32.63\arch\x86\kernel\syscall_table_32.S
        ENTRY(sys_call_table)
            .long sys_restart_syscall    /* 0 - old "setup()" system call, used for restarting */
            .long sys_exit
            .long ptregs_fork
            .long sys_read
            .long sys_write
            .long sys_open        /* 5 */
            .long sys_close
            .long sys_waitpid
            .long sys_creat
            .long sys_link
            .long sys_unlink    /* 10 */
            .long ptregs_execve
            .long sys_chdir
            .long sys_time
            .long sys_mknod
            .long sys_chmod        /* 15 */
            .long sys_lchown16
            .long sys_ni_syscall    /* old break syscall holder */
            .long sys_stat
            .long sys_lseek
            .long sys_getpid    /* 20 */
            .long sys_mount
            .long sys_oldumount
            .long sys_setuid16
            .long sys_getuid16
            .long sys_stime        /* 25 */
            .long sys_ptrace
            .long sys_alarm
            .long sys_fstat
            .long sys_pause
            .long sys_utime        /* 30 */
            .long sys_ni_syscall    /* old stty syscall holder */
            .long sys_ni_syscall    /* old gtty syscall holder */
            .long sys_access
            .long sys_nice
            .long sys_ni_syscall    /* 35 - old ftime syscall holder */
            .long sys_sync
            .long sys_kill
            .long sys_rename
            .long sys_mkdir
            .long sys_rmdir        /* 40 */
            .long sys_dup
            .long sys_pipe
            .long sys_times
            .long sys_ni_syscall    /* old prof syscall holder */
            .long sys_brk        /* 45 */
            .long sys_setgid16
            .long sys_getgid16
            .long sys_signal
            .long sys_geteuid16
            .long sys_getegid16    /* 50 */
            .long sys_acct
            .long sys_umount    /* recycled never used phys() */
            .long sys_ni_syscall    /* old lock syscall holder */
            .long sys_ioctl
            .long sys_fcntl        /* 55 */
            .long sys_ni_syscall    /* old mpx syscall holder */
            .long sys_setpgid
            .long sys_ni_syscall    /* old ulimit syscall holder */
            .long sys_olduname
            .long sys_umask        /* 60 */
            .long sys_chroot
            .long sys_ustat
            .long sys_dup2
            .long sys_getppid
            .long sys_getpgrp    /* 65 */
            .long sys_setsid
            .long sys_sigaction
            .long sys_sgetmask
            .long sys_ssetmask
            .long sys_setreuid16    /* 70 */
            .long sys_setregid16
            .long sys_sigsuspend
            .long sys_sigpending
            .long sys_sethostname
            .long sys_setrlimit    /* 75 */
            .long sys_old_getrlimit
            .long sys_getrusage
            .long sys_gettimeofday
            .long sys_settimeofday
            .long sys_getgroups16    /* 80 */
            .long sys_setgroups16
            .long old_select
            .long sys_symlink
            .long sys_lstat
            .long sys_readlink    /* 85 */
            .long sys_uselib
            .long sys_swapon
            .long sys_reboot
            .long sys_old_readdir
            .long old_mmap        /* 90 */
            .long sys_munmap
            .long sys_truncate
            .long sys_ftruncate
            .long sys_fchmod
            .long sys_fchown16    /* 95 */
            .long sys_getpriority
            .long sys_setpriority
            .long sys_ni_syscall    /* old profil syscall holder */
            .long sys_statfs
            .long sys_fstatfs    /* 100 */
            .long sys_ioperm
            .long sys_socketcall
            .long sys_syslog
            .long sys_setitimer
            .long sys_getitimer    /* 105 */
            .long sys_newstat
            .long sys_newlstat
            .long sys_newfstat
            .long sys_uname
            .long ptregs_iopl    /* 110 */
            .long sys_vhangup
            .long sys_ni_syscall    /* old "idle" system call */
            .long ptregs_vm86old
            .long sys_wait4
            .long sys_swapoff    /* 115 */
            .long sys_sysinfo
            .long sys_ipc
            .long sys_fsync
            .long ptregs_sigreturn
            .long ptregs_clone    /* 120 */
            .long sys_setdomainname
            .long sys_newuname
            .long sys_modify_ldt
            .long sys_adjtimex
            .long sys_mprotect    /* 125 */
            .long sys_sigprocmask
            .long sys_ni_syscall    /* old "create_module" */
            .long sys_init_module
            .long sys_delete_module
            .long sys_ni_syscall    /* 130:    old "get_kernel_syms" */
            .long sys_quotactl
            .long sys_getpgid
            .long sys_fchdir
            .long sys_bdflush
            .long sys_sysfs        /* 135 */
            .long sys_personality
            .long sys_ni_syscall    /* reserved for afs_syscall */
            .long sys_setfsuid16
            .long sys_setfsgid16
            .long sys_llseek    /* 140 */
            .long sys_getdents
            .long sys_select
            .long sys_flock
            .long sys_msync
            .long sys_readv        /* 145 */
            .long sys_writev
            .long sys_getsid
            .long sys_fdatasync
            .long sys_sysctl
            .long sys_mlock        /* 150 */
            .long sys_munlock
            .long sys_mlockall
            .long sys_munlockall
            .long sys_sched_setparam
            .long sys_sched_getparam   /* 155 */
            .long sys_sched_setscheduler
            .long sys_sched_getscheduler
            .long sys_sched_yield
            .long sys_sched_get_priority_max
            .long sys_sched_get_priority_min  /* 160 */
            .long sys_sched_rr_get_interval
            .long sys_nanosleep
            .long sys_mremap
            .long sys_setresuid16
            .long sys_getresuid16    /* 165 */
            .long ptregs_vm86
            .long sys_ni_syscall    /* Old sys_query_module */
            .long sys_poll
            .long sys_nfsservctl
            .long sys_setresgid16    /* 170 */
            .long sys_getresgid16
            .long sys_prctl
            .long ptregs_rt_sigreturn
            .long sys_rt_sigaction
            .long sys_rt_sigprocmask    /* 175 */
            .long sys_rt_sigpending
            .long sys_rt_sigtimedwait
            .long sys_rt_sigqueueinfo
            .long sys_rt_sigsuspend
            .long sys_pread64    /* 180 */
            .long sys_pwrite64
            .long sys_chown16
            .long sys_getcwd
            .long sys_capget
            .long sys_capset    /* 185 */
            .long ptregs_sigaltstack
            .long sys_sendfile
            .long sys_ni_syscall    /* reserved for streams1 */
            .long sys_ni_syscall    /* reserved for streams2 */
            .long ptregs_vfork    /* 190 */
            .long sys_getrlimit
            .long sys_mmap_pgoff
            .long sys_truncate64
            .long sys_ftruncate64
            .long sys_stat64    /* 195 */
            .long sys_lstat64
            .long sys_fstat64
            .long sys_lchown
            .long sys_getuid
            .long sys_getgid    /* 200 */
            .long sys_geteuid
            .long sys_getegid
            .long sys_setreuid
            .long sys_setregid
            .long sys_getgroups    /* 205 */
            .long sys_setgroups
            .long sys_fchown
            .long sys_setresuid
            .long sys_getresuid
            .long sys_setresgid    /* 210 */
            .long sys_getresgid
            .long sys_chown
            .long sys_setuid
            .long sys_setgid
            .long sys_setfsuid    /* 215 */
            .long sys_setfsgid
            .long sys_pivot_root
            .long sys_mincore
            .long sys_madvise
            .long sys_getdents64    /* 220 */
            .long sys_fcntl64
            .long sys_ni_syscall    /* reserved for TUX */
            .long sys_ni_syscall
            .long sys_gettid
            .long sys_readahead    /* 225 */
            .long sys_setxattr
            .long sys_lsetxattr
            .long sys_fsetxattr
            .long sys_getxattr
            .long sys_lgetxattr    /* 230 */
            .long sys_fgetxattr
            .long sys_listxattr
            .long sys_llistxattr
            .long sys_flistxattr
            .long sys_removexattr    /* 235 */
            .long sys_lremovexattr
            .long sys_fremovexattr
            .long sys_tkill
            .long sys_sendfile64
            .long sys_futex        /* 240 */
            .long sys_sched_setaffinity
            .long sys_sched_getaffinity
            .long sys_set_thread_area
            .long sys_get_thread_area
            .long sys_io_setup    /* 245 */
            .long sys_io_destroy
            .long sys_io_getevents
            .long sys_io_submit
            .long sys_io_cancel
            .long sys_fadvise64    /* 250 */
            .long sys_ni_syscall
            .long sys_exit_group
            .long sys_lookup_dcookie
            .long sys_epoll_create
            .long sys_epoll_ctl    /* 255 */
            .long sys_epoll_wait
             .long sys_remap_file_pages
             .long sys_set_tid_address
             .long sys_timer_create
             .long sys_timer_settime        /* 260 */
             .long sys_timer_gettime
             .long sys_timer_getoverrun
             .long sys_timer_delete
             .long sys_clock_settime
             .long sys_clock_gettime        /* 265 */
             .long sys_clock_getres
             .long sys_clock_nanosleep
            .long sys_statfs64
            .long sys_fstatfs64
            .long sys_tgkill    /* 270 */
            .long sys_utimes
             .long sys_fadvise64_64
            .long sys_ni_syscall    /* sys_vserver */
            .long sys_mbind
            .long sys_get_mempolicy
            .long sys_set_mempolicy
            .long sys_mq_open
            .long sys_mq_unlink
            .long sys_mq_timedsend
            .long sys_mq_timedreceive    /* 280 */
            .long sys_mq_notify
            .long sys_mq_getsetattr
            .long sys_kexec_load
            .long sys_waitid
            .long sys_ni_syscall        /* 285 */ /* available */
            .long sys_add_key
            .long sys_request_key
            .long sys_keyctl
            .long sys_ioprio_set
            .long sys_ioprio_get        /* 290 */
            .long sys_inotify_init
            .long sys_inotify_add_watch
            .long sys_inotify_rm_watch
            .long sys_migrate_pages
            .long sys_openat        /* 295 */
            .long sys_mkdirat
            .long sys_mknodat
            .long sys_fchownat
            .long sys_futimesat
            .long sys_fstatat64        /* 300 */
            .long sys_unlinkat
            .long sys_renameat
            .long sys_linkat
            .long sys_symlinkat
            .long sys_readlinkat        /* 305 */
            .long sys_fchmodat
            .long sys_faccessat
            .long sys_pselect6
            .long sys_ppoll
            .long sys_unshare        /* 310 */
            .long sys_set_robust_list
            .long sys_get_robust_list
            .long sys_splice
            .long sys_sync_file_range
            .long sys_tee            /* 315 */
            .long sys_vmsplice
            .long sys_move_pages
            .long sys_getcpu
            .long sys_epoll_pwait
            .long sys_utimensat        /* 320 */
            .long sys_signalfd
            .long sys_timerfd_create
            .long sys_eventfd
            .long sys_fallocate
            .long sys_timerfd_settime    /* 325 */
            .long sys_timerfd_gettime
            .long sys_signalfd4
            .long sys_eventfd2
            .long sys_epoll_create1
            .long sys_dup3            /* 330 */
            .long sys_pipe2
            .long sys_inotify_init1
            .long sys_preadv
            .long sys_pwritev
            .long sys_rt_tgsigqueueinfo    /* 335 */
            .long sys_perf_event_open
复制代码
在entry_32.S中列出了Linux操作系统所支持的所有系统调用

 

1. Linux系统调用实现方式的演进

复制代码
1. 通过INT 0x80中断方式进入系统调用
在 2.6以前的 Linux 2.4 内核中，用户态 Ring3 代码请求内核态 Ring0 代码完成某些功能是通过系统调用完成的，而系统调用的是通过软中断指令(int 0x80) 实现的。在 x86 保护模式中，处理 INT 中断指令时
    1) CPU 首先从中断描述表 IDT 取出对应的门描述符
    2) 判断门描述符的种类
    3) 检查门描述符的级别 DPL 和 INT 指令调用者的级别 CPL，当 CPL<=DPL 也就是说 INT 调用者级别高于描述符指定级别时，才能成功调用
    4) 根据描述符的内容，进行压栈、跳转、权限级别提升
    5) 内核代码执行完毕之后，调用 IRET 指令返回，IRET 指令恢复用户栈，并跳转会低级别的代码 
/*
在发生系统调用，由 Ring3 进入 Ring0 的这个过程浪费了不少的 CPU 周期，例如，系统调用必然需要由 Ring3 进入 Ring0，权限提升之前和之后的级别是固定的，CPL 肯定是 3，而 INT 80 的 DPL 肯定也是 3，这样 CPU 检查门描述符的 DPL 和调用者的 CPL 就是完全没必要。正是由于如此，Intel x86 CPU 从 PII 300(Family 6，Model 3，Stepping 3)之后，开始支持新的系统调用指令 sysenter/sysexit
*/

2. 通过sysenter指令方式直接进入系统调用
sysenter 指令用于由 Ring3 进入 Ring0，SYSEXIT 指令用于由 Ring0 返回 Ring3。由于没有特权级别检查的处理，也没有压栈的操作，所以执行速度比 INT n/IRET 快了不少。
sysenter和sysexit都是CPU原生支持的指令集
复制代码
0x1: 不同系统调用方法的性能比较





Relevant Link:

http://www.ibm.com/developerworks/cn/linux/kernel/l-k26ncpu/
 

3. 通过INT 0x80中断方式进入系统调用

通过80中断(软中断)进入系统调用的方式是Linux 2.6之前的做法，关于这块的内容请参阅另一篇文章

http://www.cnblogs.com/LittleHann/p/3871630.html

4. 通过sysenter指令方式直接进入系统调用

0x1: sysenter/sysexit机制简介

复制代码
1. sysenter 指令
    1) 用于特权级 3 的用户代码调用特权级 0 的系统内核代码
    2) sysenter 指令可以在 3，2，1 这三个特权级别调用(Linux 中只用到了特权级 3)

2. SYSEXIT 指令
    1) 用于特权级 0 的系统代码返回用户空间中
    2) SYSEXIT 指令只能从特权级 0 调用 
复制代码
0x2: sysenter/sysexit和int n/iret的区别

复制代码
1. sysenter/sysexit
    1) 目标 Ring 0 代码段必须是平坦模式(Flat Mode)的 4GB 的可读可执行的非一致代码段
    2) 目标 RING 0 堆栈段必须是平坦模式(Flat Mode)的 4GB 的可读可写向上扩展的栈段 
    3) sysenter/sysexit 指令并不成对，sysenter 指令并不会把 SYSEXIT 所需的返回地址压栈，sysexit 返回的地址并不一定是 sysenter 指令的下一个指令地址。调用 sysenter/sysexit 指令地址的跳转是通过设置一组特殊寄存器实现的，这些寄存器可以通过 wrmsr 指令来设置。这些寄存器包括: 
        3.1) SYSENTER_CS_MSR: 用于指定要执行的 Ring 0 代码的代码段选择符，由它还能得出目标 Ring 0 所用堆栈段的段选择符 
        3.2) SYSENTER_EIP_MSR: 用于指定要执行的 Ring 0 代码的起始地址 
        3.3) SYSENTER_ESP_MSR: 用于指定要执行的Ring 0代码所使用的栈指针

2. int n/iret
    1) int n/iret是成对出现的，iret 返回的地址并一定是 int n 指令的下一个指令地址
复制代码
需要明白的是，不管是以前的INT 0x80中断方式进入系统调用，还是使用sysenter方式进入系统调用，对于系统调用来说，最终都是通过"sys_call_table"来根据调用号寻址，跳转到对应的系统调用处理例程里面的，所以我们对sys_call_table进行hijack replace hook不管在linux 2.4还是2.6以后都是有效的

0x3: sysenter执行流程

在 Ring3 的代码调用了 sysenter 指令之后，CPU 会做出如下的操作: 

1. 将 SYSENTER_CS_MSR 的值装载到 cs 寄存器
2．将 SYSENTER_EIP_MSR 的值装载到 eip 寄存器
3．将 SYSENTER_CS_MSR 的值加 8(Ring0 的堆栈段描述符)装载到 ss 寄存器 
4．将 SYSENTER_ESP_MSR 的值装载到 esp 寄存器
5．将特权级切换到 Ring0
6．如果 EFLAGS 寄存器的 VM 标志被置位，则清除该标志
7．开始执行指定的 Ring0 代码

0x3: sysexit执行流程

在 Ring0 代码执行完毕，调用 SYSEXIT 指令退回 Ring3 时，CPU 会做出如下操作: 

1. 将 SYSENTER_CS_MSR 的值加 16(Ring3 的代码段描述符)装载到 cs 寄存器
2．将寄存器 edx 的值装载到 eip 寄存器
3．将 SYSENTER_CS_MSR 的值加 24(Ring3 的堆栈段描述符)装载到 ss 寄存器
4．将寄存器 ecx 的值装载到 esp 寄存器
5．将特权级切换到 Ring3
6．继续执行 Ring3 的代码
Relevant Link:

http://www.ibm.com/developerworks/cn/linux/kernel/l-k26ncpu/
http://chenyufei.info/blog/2007-05-12/post-070512-221011-78/
http://articles.manugarg.com/systemcallinlinux2_6.html
 

5. sysenter/sysexit编程示例

复制代码
#include <stdio.h>

int pid;

int main() {
        __asm__(
                "movl $20, %eax    \n"
                "call *%gs:0x10    \n"   /* offset 0x10 is not fixed across the systems */
                "movl %eax, pid    \n"
        );
        printf("pid is %d\n", pid);
        return 0;
}
复制代码
 

6. Linux SCI

Linux中系统调用的实现会根据不同的架构而有所变化，而且即使在某种给定的体架构上也会不同。例如，早期的x86处理器使用了中断机制从用户空间迁移到内核空间中，不过新的IA-32处理器则提供了一些指令对这种转换进行优化(使用sysentersysexit指令)

0x1: 基于多路分解的系统调用实现

在Linux内核中，多路分解是一种很常见的逻辑架构，每个系统调用都是通过一个单一的入口点多路传入内核。eax寄存器用来标识应当调用的某个系统调用。例如，BSD(Berkeley Software Distribution)socket 调用(socket、bind、 connect 等)都与一个单独的系统调用索引(__NR_socketcall)关联在一起，不过在内核中会进行多路分解，通过另外一个参数进入适当的调用。请参看 ./linux/net/socket.c中的sys_socketcall 函数

关于BSD sys_socketcall的相关知识，请参阅另一篇文章

http://www.cnblogs.com/LittleHann/p/3875451.html
//搜索: 2. connect() API原理
0x2: 直接内核态子函数调用实现系统调用

通过一个系统调用，将工作委托给多个其他函数，是内核前期的常见做法，内核后来移植的某些体系结构(例如IA-64、AMD64)没有实现多路分解，而是直接使用原始多路复用的子函数直接作为系统调用
例如socketcall的多路分解就演变成了直接的子函数系统调用

Relevant Link:

http://www.ibm.com/developerworks/cn/linux/l-system-calls/
http://blog.chinaunix.net/uid-29643701-id-4240657.html 
 
---

### 从"read"看系统调用的耗时
https://codeleading.com/article/19673469609/
### 一次系统调用开销到底有多大
https://cloud.tencent.com/developer/article/1760744
### Linux Systemcall Int0x80方式、Sysenter/Sysexit Difference Comparation
https://www.cnblogs.com/littlehann/p/4111692.html

https://www.cnblogs.com/jiading/p/12606978.html
https://blog.csdn.net/gatieme/article/details/50779184
https://blog.csdn.net/gatieme/article/details/50646461

https://zhuanlan.zhihu.com/p/52845869

版权声明: 本文为cchao985771161原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。
本文链接: https://blog.csdn.net/cchao985771161/article/details/105767444

版权声明: 本文为CSDN博主「CHENG Jian」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/gatieme/article/details/50779184

https://cloud.tencent.com/developer/article/1760744  

## getrlimit(), setrlimit()
获取或设定资源使用限制。每种资源都有相关的软硬限制，软限制是内核强加给相应资源的限制值，硬限制是软限制的最大值。非授权调用进程只可以将其软限制指定为0~硬限制范围中的某个值，同时能不可逆转地降低其硬限制。授权进程可以任意改变其软硬限制。RLIM_INFINITY的值表示不对资源限制。


用法：

#include <sys/resource.h>

int getrlimit(int resource, struct rlimit *rlim);
int setrlimit(int resource, const struct rlimit *rlim);
参数：

resource：可能的选择有

RLIMIT_AS //进程的最大虚内存空间，字节为单位。
RLIMIT_CORE //内核转存文件的最大长度。
RLIMIT_CPU //最大允许的CPU使用时间，秒为单位。当进程达到软限制，内核将给其发送SIGXCPU信号，这一信号的默认行为是终止进程的执行。然而，可以捕捉信号，处理句柄可将控制返回给主程序。如果进程继续耗费CPU时间，核心会以每秒一次的频率给其发送SIGXCPU信号，直到达到硬限制，那时将给进程发送 SIGKILL信号终止其执行。
RLIMIT_DATA //进程数据段的最大值。
RLIMIT_FSIZE //进程可建立的文件的最大长度。如果进程试图超出这一限制时，核心会给其发送SIGXFSZ信号，默认情况下将终止进程的执行。
RLIMIT_LOCKS //进程可建立的锁和租赁的最大值。
RLIMIT_MEMLOCK //进程可锁定在内存中的最大数据量，字节为单位。
RLIMIT_MSGQUEUE //进程可为POSIX消息队列分配的最大字节数。
RLIMIT_NICE //进程可通过setpriority() 或 nice()调用设置的最大完美值。
RLIMIT_NOFILE //指定比进程可打开的最大文件描述词大一的值，超出此值，将会产生EMFILE错误。
RLIMIT_NPROC //用户可拥有的最大进程数。
RLIMIT_RTPRIO //进程可通过sched_setscheduler 和 sched_setparam设置的最大实时优先级。
RLIMIT_SIGPENDING //用户可拥有的最大挂起信号数。
RLIMIT_STACK //最大的进程堆栈，以字节为单位。

rlim：描述资源软硬限制的结构体，原型如下

struct rlimit {
　　rlim_t rlim_cur;
　　rlim_t rlim_max;
};
返回说明：

成功执行时，返回0。失败返回-1，errno被设为以下的某个值
EFAULT：rlim指针指向的空间不可访问
EINVAL：参数无效
EPERM：增加资源限制值时，权能不允许


>https://www.cnblogs.com/niocai/archive/2012/04/01/2428128.html

