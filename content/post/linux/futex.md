---
title: "futex"
author: "-"
date: ""
url: "futex"
categories:
  - OS
tags:
  - lock
---
## "futex"

futex (fast userspace mutex) 是Linux的一个基础构件，可以用来构建各种更高级别的同步机制，比如锁或者信号量等等，POSIX信号量就是基于futex构建的。大多数时候编写应用程序并不需要直接使用futex，一般用基于它所实现的系统库就够了。

futex的性能非常优异，它是怎样做到的呢？这要从它的设计思想谈起。传统的SystemV IPC(inter process communication)进程间同步机制都是通过内核对象来实现的，以 semaphore 为例，当进程间要同步的时候，必须通过系统调用semop(2)进入内核进行PV操作。系统调用的缺点是开销很大，需要从user mode切换到kernel mode、保存寄存器状态、从user stack切换到kernel stack、等等，通常要消耗上百条指令。事实上，有一部分系统调用是可以避免的，因为现实中很多同步操作进行的时候根本不存在竞争，即某个进程从持有semaphore直至释放semaphore的这段时间内，常常没有其它进程对同一semaphore有需求，在这种情况下，内核的参与本来是不必要的，可是在传统机制下，持有semaphore必须先调用semop(2)进入内核去看看有没有人和它竞争，释放semaphore也必须调用semop(2)进入内核去看看有没有人在等待同一semaphore，这些不必要的系统调用造成了大量的性能损耗。futex就为了解决这个问题而生的，它的办法是: 在无竞争的情况下，futex的操作完全在user space进行，不需要系统调用，仅在发生竞争的时候进入内核去完成相应的处理(wait 或者 wake up)。所以说，futex是一种user mode和kernel mode混合的同步机制，需要两种模式合作才能完成，futex变量必须位于user space，而不是内核对象，futex的代码也分为user mode和kernel mode两部分，无竞争的情况下在user mode，发生竞争时则通过sys_futex系统调用进入kernel mode进行处理，具体来说: 

futex 变量是位于 user space 的一个整数，支持原子操作。futex 同步操作都是从user space开始的: 

当要求持有futex的时候，对futex变量执行”down”操作，即原子递减，如果变量变为0，则意味着没有竞争发生，进程成功持有futex 并继续在user mode运行；如果变量变为负数，则意味着有竞争发生，需要通过sys_fute x系统调用进入内核执行futex_wait操作，让进程进入休眠等待。
当释放futex的时候，对futex变量进行”up”操作，即原子递增，如果变量变成1，则意味着没有竞争发生，进程成功释放futex并继续在user mode执行；否则意味着有竞争，需要通过sys_futex 系统调用进入内核执行 futex_wake 操作，唤醒正在等待的进程。
如果需要在多个进程之间共享futex，那就必须把futex变量放在共享内存中，并确保这些进程都有访问共享内存的权限；如果仅需在线程之间使用futex的话，那么futex变量可以位于进程的私有内存中，比如普通的全局变量即可。

更详细的信息请参阅futex作者的论文: 
Fuss, Futexes and Furwocks: Fast Userlevel Locking in Linux
>http://linuxperf.com/?p=23

### 什么是 Futex
Futex,作为linux下的一种快速同步 (互斥) 机制
Futex 是Fast Userspace muTexes的缩写,由Hubertus Franke, Matthew Kirkwood, Ingo Molnar and Rusty Russell共同设计完成。几位都是linux领域的专家,其中可能Ingo Molnar大家更熟悉一些,毕竟是O(1)调度器和CFS的实现者。

Futex 按英文翻译过来就是快速用户空间互斥体。其设计思想其实 不难理解,在传统的Unix系统中,System V IPC(inter process communication),如 semaphores, msgqueues, sockets还有文件锁机制(flock())等进程间同步机制都是对一个内核对象操作来完成的, 这个内核对象对要同步的进程都是可见的, 其提供了共享 的状态信息和原子操作。当进程间要同步的时候必须要通过系统调用 (如semop())在内核中完成。可是经研究发现,很多同步是无竞争的, 即某个进程进入 互斥区,到再从某个互斥区出来这段时间,常常是没有进程也要进这个互斥区或者请求同一同步变量的。但是在这种情况下,这个进程也要陷入内核去看看有没有人和它竞争,退出的时侯还要陷入内核去看看有没有进程等待在同一同步变量上。这些不必要的系统调用(或者说内核陷入)造成了大量的性能开销。为了解决这个问 题,Futex就应运而生,Futex是一种用户态和内核态混合的同步机制。首先,同步的进程间通过mmap共享一段内存,futex变量就位于这段共享 的内存中且操作是原子的,当进程尝试进入互斥区或者退出互斥区的时候,先去查看共享内存中的futex变量,如果没有竞争发生,则只修改futex,而不用再执行系统调用了。当通过访问futex变量告诉进程有竞争发生,则还是得执行系统调用去完成相应的处理(wait 或者 wake up)。简单的说,futex就是通过在用户态的检查, (motivation) 如果了解到没有竞争就不用陷入内核了,大大提高了low-contention时候的效率。 Linux从2.5.7开始支持Futex。

>https://cloud.tencent.com/developer/article/1176832

### futex 诞生之前
在futex诞生之前,linux下的同步机制可以归为两类: 用户态的同步机制 和 内核态同步机制. 用户态的同步机制基本上就是利用原子指令实现的 spinlock。最简单的实现就是使用一个整型数,0表示未上锁,1表示已上锁。trylock操作就利用原子指令尝试将0改为1
```c
bool trylock(int lockval) {
    int old;
    atomic { old = lockval; lockval = 1; }  // 如: x86下的xchg指令
    return old == 0;
}
```

无论 spinlock 事先有没有被上锁,经历trylock之后,它肯定是已经上锁了。所以lock变量一定被置1。而trylock是否成功,取决于spinlock是事先就被上了锁的 (old==1) ,还是这次trylock上锁的(old==0). 而使用原子指令则可以避免多个进程同时看到old==0,并且都认为是自己把它改为1的。

spinlock的lock操作则是一个死循环,不断尝试 trylock, 直到成功。
对于一些很小的临界区,使用spinlock是很高效的。因为trylock失败时,可以预期持有锁的线程 (进程) 会很快退出临界区 (释放锁) 。所以死循环的忙等待很可能要比进程挂起等待更高效。
但是 spinlock 的应用场景有限,对于大的临界区,忙等待则是件很恐怖的事情,特别是当同步机制运用于等待某一事件时 (比如服务器工作线程等待客户端发起请求) 。所以很多情况下进程挂起等待是很有必要的。

内核提供的同步机制,诸如 semaphore、等,其实骨子里也是利用原子指令实现的 spinlock, 内核在此基础上实现了进程的睡眠与唤醒。
使用这样的锁,能很好的支持进程挂起等待。但是最大的缺点是每次 lock 与 unlock 都是一次系统调用,即使没有锁冲突,也必须要通过系统调用进入内核之后才能识别。 (关于系统调用开销大的问题,可以参阅: 《从"read"看系统调用的耗时》。) 

理想的同步机制应该是在没有锁冲突的情况下在用户态利用原子指令就解决问题,而需要挂起等待时再使用内核提供的系统调用进行睡眠与唤醒。换句话说,用户态的 spinlock 在 trylock 失败时,能不能让进程挂起,并且由持有锁的线程在 unlock 时将其唤醒？
如果你没有较深入地考虑过这个问题,很可能想当然的认为类似于这样就行了: 

void lock(int lockval) {
    while (!trylock(lockval)) {
        wait();  // 如: raise(SIGSTOP)
    }
}
但是如果这样做的话,检测锁的trylock操作和挂起进程的wait操作之间会存在一个窗口,如果其间 lock 发生变化 (比如锁的持有者释放了锁) ,调用者将进入不必要的 wait,甚至于wait之后再没有人能将它唤醒。 (详见《linux线程同步浅析》的讨论。) 

在futex诞生之前,要实现我们理想中的锁会非常别扭。比如可以考虑用 sigsuspend 系统调用来实现进程挂起: 
```c
class mutex {
private:
    int lockval;
    spinlocked_set<pid_t> waiters;    // 使用spinlock做保护的set
public:
    void lock() {
        pid_t mypid = getpid();
        waiters.insert(mypid);        // 先将自己加入mutex的等待队列
        while (!trylock(lockval)) {   // 再尝试加锁
            // 进程初始化时需要将SIGUSER1 mask掉,并在此时开启
            sigsuspend(MASK_WITHOUT_SIGUSER1);
        }
        waiters.remove(mypid)         // 上锁成功之后将自己从等待队列移除
    }
    void unlock() {
        lockval = 0;                  // 先释放锁
        pid_t waiter = waiters.first();  // 再检查等待队列
        if (waiter != 0) {            // 如果有人等待,发送SIGUSER1信号将其唤醒
            kill(waiter, SIGUSER1);
        }
    }
}
```
注意,这里的sigsuspend不同于简单的raise(SIGSTOP)之类wait操作。如果unlock时用于唤醒的kill操作先于sigsuspend发生,sigsuspend也一样能被唤醒。 (详见《linux线程同步浅析》的讨论。) 
这样的实现有点类似于老版本的 phread_cond,应该还是能 work 的。有些不太爽的地方,比如 sigsuspend 系统调用是全局的,并不单单考虑某一把锁。也就是说,lockA 的 unlock 可以将等待 lockB 的进程唤醒。尽管进程被唤醒之后会继续trylock,并不影响正确性；尽管多数情况下lockA.unlock也并不会试图去唤醒等待lockB的进程 (除了一些竞争情况下) ,因为后者很可能并不在lockA的等待队列中。
另一方面,用户态实现的等待队列也不太爽。它对进程的生命周期是无法感知的,很可能进程挂了,pid却还留在队列中 (甚至于一段时间之后又有另一个不相干的进程重用了这个pid,以至于它可能会收到莫名其妙的信号) 。所以,unlock的时候如果仅仅给队列中的一个进程发信号,很可能唤醒不了任何等待者。保险的做法只能是全部唤醒,从而引发“惊群“现象。不过,如果仅仅用在多线程 (同一进程内部) 倒也没关系,毕竟多线程不存在某个线程挂掉的情况 (如果线程挂掉,整个进程都会挂掉) ,而对于线程响应信号而主动退出的情况也是可以在主动退出前注意处理一下等待队列清理的问题。

### futex 来了
现在看来,要实现我们想要的锁,对内核就有两点需求: 
1. 支持一种锁粒度的睡眠与唤醒操作；
2. 管理进程挂起时的等待队列。

于是futex就诞生了。futex主要有 futex_wait 和futex_wake两个操作: 

// 在uaddr指向的这个锁变量上挂起等待 (仅当*uaddr==val时) 
int futex_wait(int *uaddr, int val);
// 唤醒n个在uaddr指向的锁变量上挂起等待的进程
int futex_wake(int *uaddr, int n);
内核会动态维护一个跟uaddr指向的锁变量相关的等待队列。
注意futex_wait的第二个参数, 由于用户态trylock与调用futex_wait之间存在一个窗口,其间lockval可能发生变化 (比如正好有人unlock了) 。所以用户态应该将自己看到的*uaddr的值作为第二个参数传递进去,futex_wait真正将进程挂起之前一定得检查lockval是否发生了变化,并且检查过程跟进程挂起的过程得放在同一个临界区中。 (参见《linux线程同步浅析》的讨论。) 如果futex_wait发现lockval发生了变化,则会立即返回,由用户态继续trylock。

futex实现了锁粒度的等待队列,而这个锁却并不需要事先向内核申明。任何时候,用户态调用futex_wait传入一个uaddr,内核就会维护起与之配对的等待队列。
这件事情听上去好像很复杂,实际上却很简单。其实它并不需要为每一个uaddr单独维护一个队列,futex只维护一个总的队列就行了,所有挂起的进程都放在里面。当然,队列中的节点需要能标识出相应进程在等待的是哪一个uaddr。这样,当用户态调用futex_wake时,只需要遍历这个等待队列,把带有相同uaddr的节点所对应的进程唤醒就行了。
作为优化,futex维护的这个等待队列由若干个带spinlock的链表构成。调用futex_wait挂起的进程,通过其uaddr hash到某一个具体的链表上去。这样一方面能分散对等待队列的竞争、另一方面减小单个队列的长度,便于futex_wake时的查找。每个链表各自持有一把spinlock,将"*uaddr和val的比较操作"与"把进程加入队列的操作"保护在一个临界区中。

另一个问题是关于uaddr参数的比较。futex支持多进程,需要考虑同一个物理内存单元在不同进程中的虚拟地址不同的问题。那么不同进程传递进来的uaddr如何判断它们是否相等,就不是简单数值比较的事情。相同的uaddr不一定代表同一个内存,反之亦然。
两个进程 (线程) 要想共享同存,无外乎两种方式: 通过文件映射 (映射真实的文件或内存文件、ipc shmem,以及有亲缘关系的进程通过带MAP_SHARED标记的匿名映射共享内存) 、通过匿名内存映射 (比如多线程) ,这也是进程使用内存的唯二方式。
那么futex就应该支持这两种方式下的uaddr比较。匿名映射下,需要比较uaddr所在的地址空间 (mm) 和uaddr的值本身；文件映射下,需要比较uaddr所在的文件inode和uaddr在该inode中的偏移。注意,上面提到的内存共享方式中,有一种比较特殊: 有亲缘关系的进程通过带MAP_SHARED标记的匿名映射共享内存。这种情况下表面上看使用的是匿名映射,但是内核在暗中却会转成到/dev/zero这个特殊文件的文件映射。若非如此,各个进程的地址空间不同,匿名映射下的uaddr永远不可能被futex认为相等。

futex和它的兄弟姐妹们
futex_wait和futex_wake就是futex的基本。之后,为了对其他同步方式做各种优化,futex又增加了若干变种。
futex等待系列的调用一般都可以传递timeout参数,支持超时唤醒。这一块逻辑相对较独立,本文中不再展开。

Bitset系列
int futex_wait_bitset(int *uaddr, int val, int bitset);
int futex_wake_bitset(int *uaddr, int n, int bitset);
额外传递了一个bitset参数,使用特定bitset进行wait的进程,只能被使用它的bitset超集的wake调用所唤醒。
这个东西给读写锁很好用,进程挂起的时候通过bitset标记自己是在等待读还是等待写。unlock时决定应该唤醒一个写等待的进程、还是唤醒全部读等待的进程。
没有bitset这个功能的话,要么只能unlock的时候不区分读等待和写等待,全部唤醒；要么只能搞两个uaddr,读写分别futex_wait其中一个,然后再用spinlock保护一下两个uaddr的同步。
 (参阅: http://locklessinc.com/articles/sleeping_rwlocks/) 

Requeue系列
int futex_requeue(int *uaddr, int n, int *uaddr2, int n2);
int futex_cmp_requeue(int *uaddr, int n, int *uaddr2, int n2, int val);
功能跟futex_wake有点相似,但不仅仅是唤醒n个等待uaddr的进程,而更进一步,将n2个等待uaddr的进程移到uaddr2的等待队列中 (相当于也futex_wake它们,然后强制让它们futex_wait在uaddr2上面) 。
在futex_requeue的基础上,futex_cmp_requeue多了一个判断,仅当*uaddr与val相等时才执行操作,否则直接返回,让用户态去重试。
这个东西是为pthread_cond_broadcast准备的。还是先来回顾一下pthread_cond的逻辑 (列一下,后面会多次用到) : 

pthread_cond_wait(mutex, cond):
    value = cond->value; /* 1 */
    pthread_mutex_unlock(mutex); /* 2 */
retry:
    pthread_mutex_lock(cond->mutex); /* 10 */
    if (value == cond->value) { /* 11 */
        me->next_cond = cond->waiter;
        cond->waiter = me;
        pthread_mutex_unlock(cond->mutex);
        unable_to_run(me);
        goto retry;
    } else
        pthread_mutex_unlock(cond->mutex); /* 12 */
    pthread_mutex_lock(mutex); /* 13 */
pthread_cond_signal(cond):
    pthread_mutex_lock(cond->mutex); /* 3 */
    cond->value++; /* 4 */
    if (cond->waiter) { /* 5 */
        sleeper = cond->waiter; /* 6 */
        cond->waiter = sleeper->next_cond; /* 7 */
        able_to_run(sleeper); /* 8 */
    }
    pthread_mutex_unlock(cond->mutex); /* 9 */
pthread_cond_broadcast跟pthread_cond_signal类似,不过它会唤醒所有 (而不是一个) 等待者。注意,pthread_cond_wait在被唤醒之后,第一件事情就是lock(mutex) (第13步) 。如果pthread_cond_broadcast一下子唤醒了N个等待者,它们醒来之后势必会争抢mutex,造成千军万马过独木桥的"惊群"现象。
作为一种优化,pthread_cond_broadcast不应该用futex_wake去唤醒所有等待者,而应该用futex_requeue唤醒一个等待者,然后将其他进程都转移到mutex的等待队列上去 (随后再由mutex的unlock来逐个唤醒) 。

为什么要有futex_cmp_requeue呢？因为futex_requeue其实是有问题的,它相当于直接把一批进程拖到uaddr2的等待队列里面去了,而没有在临界区里面做状态检查 (回想一下futex_wait里面检查*uaddr==val的重要性) 。那么,在进入futex_requeue和真正将进程移到uaddr2之间就存在一个窗口,这个间隙内可能有其他线程futex_wake(uaddr2),这将无法唤醒这些正要移动却尚未移动的进程,可能造成这些进程今后再也无法被唤醒了。
不过尽管futex_requeue并不严谨,pthread_cond_broadcast这个case却是OK的,因为在pthread_cond_broadcast唤醒等待者的时候,不可能有人futex_wake(uaddr2),因为这个锁正在被pthread_cond_broadcast持有,它将在唤醒操作结束后 (第9步) 才会释放。这也就是为什么futex_requeue有问题,却堂而皇之的被release了。

Wake & Operator
int futex_wake_op(int *uaddr1, int *uaddr2, int n1, int n2, int op);
这个系统调用有点像CISC的思路,一个调用中搞了很多动作。它尝试在uaddr1的等待队列中唤醒n1个进程,然后修改uaddr2的值,并且在uaddr2的值满足条件的情况下,唤醒uaddr2队列中的n2个进程。uaddr2的值如何修改？又需要满足什么样的条件才唤醒uaddr2？这些逻辑都pack在op参数中。
int类型的op参数,其实是一个struct: 

struct op {
    // 修改*uaddr2的方法: SET (*uaddr2=OPARG)、ADD(*uaddr2+=OPARG)、
    // OR(*uaddr2|=OPARG)、ANDN(*uaddr2&=~OPARG)、XOR(*uaddr2^=OPARG)
    int OP     : 4;
    // 判断*uaddr2是否满足条件的方法: EQ(==)、NE(!=)、LT(<)、LE(<=)、GT(>)、GE(>=)
    int CMP    : 4;
    int OPARG  : 12;// 修改*uaddr2的参数
    int CMPARG : 12;// 判断*uaddr2是否满足条件的参数
}
futex_wake_op搞这么一套复杂的逻辑,无非是希望一次系统调用里面处理两把锁,相当于用户态调用两次futex_wake。
假设用户态需要释放uaddr1和uaddr2两把锁 (值为0代表未上锁、1代表上锁、2代表上锁且有进程挂起等待) ,不使用futex_wake_op的话需要这么写: 

int old1, old2;
atomic { old1 = *uaddr1; *uaddr1 = 0; }
if (old1 == 2) {
    futex_wake(uaddr1, n1);
}
atomic { old2 = *uaddr2; *uaddr2 = 0; }
if (old2 == 2) {
    futex_wake(uaddr2, n2);
}
而使用futex_wake_op的话,只需要这样: 

int old1;
atomic { old1 = *uaddr1; *uaddr1 = 0; }
if (old1 == 2) {
    futex_wake_op(uaddr1, n1, uaddr2, n2, {
        // op参数的意思: 设置*uaddr2=0,并且如果old2==2,则执行唤醒
        OP=SET, OPARG=0, CMP=EQ, CMPARG=2
    } );
}
else {
    ... // 单独处理uaddr2
}
搞这么复杂,其实并不仅仅是省一次系统调用的问题。因为有可能在unlock(uaddr1)之后,被唤醒的进程立马会去lock(uaddr2)。而这时如果这边还没来得及unlock(uaddr2)的话,被唤醒的进程立刻又将被挂起,然后随着这边unlock(uaddr2)又会再度被唤醒。这不折腾么？
这个场景就可能发生在pthread_cond_wait和pthread_cond_signal之间。当pthread_cond_signal在唤醒等待者之后,会释放内部的锁 (第9步) 。而pthread_cond_wait在被唤醒之后立马又会尝试获取内部的锁,以重新检查状态 (第10步) 。若不是futex_wake_op将唤醒和释放锁两个动作一笔带过,这中间必定会有强烈的竞争。
当然,使用前面提到的futex_cmp_requeue也能避免过分竞争,pthread_cond_signal不要直接唤醒等待者,而是将其requeue到内部锁的等待队列,等这边释放锁之后才真正将其唤醒。不过既然pthread_cond_signal立马就会释放内部锁,先requeue再wake多少还是啰嗦了些。

Priority Inheritance系列
int futex_lock_pi(int *uaddr);
int futex_trylock_pi(int *uaddr);
int futex_unlock_pi(int *uaddr);
int futex_wait_requeue_pi(int *uaddr1, int val1, int *uaddr2);
int futex_cmp_requeue_pi(int *uaddr, int n1, int *uaddr2, int n2, int val);
Priority Inheritance,优先级继承,是解决优先级反转的一种办法。
futex_lock_pi/futex_trylock_pi/futex_unlock_pi,是带优先级继承的futex锁操作。
futex_cmp_requeue_pi是带优先级继承版本的futex_cmp_requeue,futex_wait_requeue_pi是与之配套使用的,用于替代普通的futex_wait。

### semop 
信号量的操作——semop函数
信号量的值与相应资源的使用情况有关，当它的值大于 0 时，表示当前可用的资源数的数量；当它的值小于 0 时，其绝对值表示等待使用该资源的进程个数。信号量的值仅能由 PV 操作来改变。

 
     在 Linux 下，PV 操作通过调用semop函数来实现。该函数定义在头文件 sys/sem.h中，原型如下: 
     int  semop (int  semid，struct sembuf  *sops，size_t nsops) ；
     函数的参数 semid 为信号量集的标识符；参数 sops 指向进行操作的结构体数组的首地址；参数 nsops 指出将要进行操作的信号的个数。semop 函数调用成功返回 0，失败返回 -1。
     semop 的第二个参数 sops 指向的结构体数组中，每个 sembuf 结构体对应一个特定信号的操作。因此对信号量进行操作必须熟悉该数据结构，该结构定义在 linux/sem.h，如下所示: 
     struct  sembuf{
         unsigned short   sem_num;      //信号在信号集中的索引，0代表第一个信号，1代表第二个信号  
         short            sem_op;      //操作类型
         short            sem_flg;    //操作标志
     };

>https://www.cnblogs.com/lixiaofei1987/p/3208414.html

### mutex, futex, java
首先，futex不是个完整的锁，它是“支持实现userspace的锁的building block“。也就是说，如果你想实现一个mutex，但不想把整个mutex都弄到内核里面去，可以通过futex来实现。但futex本身主要就是俩系统调用futex_wait和futex_wake.

java中的synchronized和linux系统的futex到底什么个关系？

为了更好的解释这个问题，这里先梳理下锁本身是怎么工作的。

一个完整的锁需要解决几个问题: 

争抢到一个内存，如果抢到了就算是得到了锁，可以继续干活；
如果没抢到，可以选择: 
继续抢 (spin) 
调用某个系统调用把自己挂起来排队
别的线程释放锁后，会通知排队挂起来的一个或几个线程。醒过来的线程再去重复第一步。
早期的锁，所有这些步骤都是内核态的。但后来大家发现，步骤1用CAS在用户态就可以干了。而多线程大部分的时候抢锁都是没有竞争的，一抢就能抢到。一下子没抢到多抢几次大概率也能抢到了。

那么能不能用一直做spin，永远不做2.2和3呢？答案是不行的。如果遇到了竞争，这也就意味着大量空耗CPU。

因此后来的锁的设计一般都优化成了这样: 

1. 在用户态写一段代码来抢锁，典型的实现是用CAS把一个指定的变量从0变成1。如果抢到了就结束了。此时是用户态的。

2. 如果抢不到，就看看是不是锁的持有者就是自己。如果是，也算是抢到了 (当然要对变量做特殊的标记) 。否则就spin几次重新抢。这也是用户态的。

3. 如果重试了N次，实在抢不到，此时调用futex_wait进入内核态，去把自己挂起+排队，等着被释放锁的线程futex_wake。

所以只有3进入内核态了。考虑到大部分情况都不是竞争很激烈的情况下，3根本就不用做。这样的锁的设计避免了由于系统调用导致的上下文切换，无疑很大的提高了效率。

Ok, 回到Java。Java的synchronized用JVM的monitor实现。而monitor实现内部用到了 pthread_mutex 和 pthread_cond 。这俩是 pthread 标准接口，实现在 glibc 里。而这俩的内部实现在 Linux上目前都用到了 futex。所以整体可以理解为 futex 帮助Java在Linux上实现了 synchronized 在内核那部分阻塞的功能；同时用户态的抢锁，重入控制等功能由JVM自己实现。两块代码共同提供了完整的synchronized功能。

所以当我们随便写一段synchornized会阻塞的Java代码: 


```java
public class TestFutex {
     private Integer a = new Integer(1);
 
     synchronized void showA() {
         System.out.println(a);
         try {
             Thread.sleep(3000);
         } catch(InterruptedException e) {
 
         }
     }
     class T extends Thread {
         @Override
         public void run() {
             showA();
         }
     }
 
     public T newThread() {
         return new T();
     }
 
     public static void main(String[] args) {
         TestFutex tf = new TestFutex();
         T t1 = tf.newThread();
         T t2 = tf.newThread();
         t1.start();
         t2.start();
     }
 }
```
并用 strace 去查看效果，你就会看到: 

root@ba32a8cedf75:/test# strace -e futex java -jar target/pingd-java-1.0-SNAPSHOT-jar-with-dependencies.jar
futex(0x7f8dacc130c8, FUTEX_WAKE_PRIVATE, 2147483647) = 0
futex(0x7f8dad64e9d0, FUTEX_WAIT, 97, NULL1

顺便说一句，基于AQS实现的JUC的那些 ReentrantLock，Semaphore 等内部也是类似的。其 LockSupport.park 内部用的也是这套东西。

>https://www.codenong.com/cs106084621/

---

https://developer.aliyun.com/article/6043  
https://blog.csdn.net/ctthuangcheng/article/details/8915169  