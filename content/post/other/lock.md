---
title: Linux中的各种锁, 自旋锁/spin lock, 排队自旋锁、MCS锁、CLH锁, 
author: "-"
date: 2014-12-05T01:05:56+00:00
url: /lock
categories:
  - OS
tags:
  - Lock

---
## Linux中的各种锁, 自旋锁/spin lock, 排队自旋锁、MCS锁、CLH锁

# Linux中的各种锁

- 互斥锁
- 文件锁
- 读写锁

Linux作为典型的多用户、多任务、抢占式内核调度的操作系统,为了提高并行处理能力,无论在内核层面还是在用户层面都需要特殊的机制来确保任务的正确性和系统的稳定运行,就如同一个国家需要各种法律条款来约束每个公民的行为,才能有条不紊地运转。

在内核层面涉及到各种软硬件中断、进线程睡眠、抢占式内核调度、多处理器SMP架构等,因此内核在完成自己工作的时候一直在处理这些资源抢占的冲突问题。

在用户层面的进程,虽然Linux作为虚地址模式操作系统,为每个进程开辟了独立的虚拟地址空间,伪独占式拥有资源,但是仍然存在很多场景不得不产生多个进程共享资源的问题,来完成进程间的通信,但是在Go语言中进程间的通信使用消息来完成,处理地更优雅一些。

在线程层面,线程作为进程的一部分,进程内的多个线程只拥有自己的独立堆栈等少量结构,大部分的资源还是过线程共享,因此多线程的资源占用冲突比进程更加明显,所以多线程编程的线程安全问题是个重难点。综上可知,无论在kernel还是user space都必须有一些机制来确保对于资源共享问题的解决,然后这个机制就是接下来要说的: 同步和互斥。

### 同步和互斥机制

基本概念
同步和互斥的概念有时候很容易混淆,可以简单地认为同步是更加宏观角度的一种说法,互斥是冲突解决的细节方法。所谓同步就是调度者让任务按照约定的合理的顺序进行,但是当任务之间出现资源竞争,也就是竞态冲突时,使用互斥的规则强制约束允许数量的任务占用资源,从而解决各个竞争状态,实现任务的合理运行。

同步和互斥密不可分,有资料说互斥是一种特殊的同步,对此我不太理解,不过实际中想明白细节就行,文字游戏没有意义。

简单来说:

同步与互斥机制是用于控制多个任务对某些特定资源的访问策略
同步是控制多个任务按照一定的规则或顺序访问某些共享资源
互斥是控制某些共享资源在任意时刻只能允许规定数量的任务访问
角色分类
整个协调流程涉及的角色本质上只有三类:

不可独占的共享资源
多个使用者
调度者
调度者需要为多个运行任务制定访问使用规则来实现稳定运行,这个调度者可以是内核、可以是应用程序,具体场景具体分析。

重要术语
要很好地理解同步和互斥,就必须得搞清楚几个重要术语:

竞争冒险(race hazard)或竞态条件(race condition)
最早听说这个术语是在模电数电的课程上,门电路出现竞态条件造成错误的结果,在计算机里面就是多个使用者同时操作共享的变量造成结果的不确定。

临界区
临界区域critical section是指多使用者可能同时共同操作的那部分代码,比如自加自减操作,多个线程处理时就需要对自加自减进行保护,这段代码就是临界区域。

### Linux中常用的锁

在说锁之前还需要知道几个东西:信号量和条件变量。这两个东西和锁有一定的联系和区别,在不同的场合单独使用或者配合实现来说实现安全的并发,至于网上很多说互斥锁是一种信号量的特例,对于这种特例理解不了也罢。信号量和互斥锁的场景不一样,信号量主要是资源数量的管理(池化),实际用的频率远不如互斥锁,文字游戏着实无趣,实用主义至上,掌握高频工具的特点正确使用即可,大可不必过于学术派。在使用锁时需要明确几个问题:

锁的所有权问题 谁加锁 谁解锁 解铃还须系铃人
锁的作用就是对临界区资源的读写操作的安全限制
锁是否可以被多个使用者占用(互不影响的使用者对资源的占用)
占用资源的加锁者的释放问题 (锁持有的超时问题)
等待资源的待加锁者的等待问题(如何通知到其他等着资源的使用者)
多个临界区资源锁的循环问题(死锁场景)
带着问题明确想要达到的目的,我们同样可以根据自己的需求设计锁,Linux现有的锁如果从上面几个问题的角度去理解,就非常容易了。

### 自旋锁 spinlock

自旋锁的主要特征是使用者在想要获得临界区执行权限时,如果临界区已经被加锁,那么自旋锁并不会阻塞睡眠,等待系统来主动唤醒,而是原地忙轮询资源是否被释放加锁,自旋就是自我旋转,这个名字还是很形象的。自旋锁有它的优点就是避免了系统的唤醒,自己来执行轮询,如果在临界区的资源代码非常短且是原子的,那么使用起来是非常方便的,避免了各种上下文切换,开销非常小,因此在内核的一些数据结构中自旋锁被广泛的使用。

### 互斥锁 mutex

使用者使用互斥锁时在访问共享资源之前对进行加锁操作,在访问完成之后进行解锁操作,谁加锁谁释放,其他使用者没有释放权限。 加锁后,任何其他试图再次加锁的线程会被阻塞,直到当前进程解锁。 区别于自旋锁,互斥锁无法获取锁时将阻塞睡眠,需要系统来唤醒,可以看出来自旋锁自己原地旋转来确定锁被释放了,互斥锁由系统来唤醒,但是现实并不是那么美好的,因为很多业务逻辑系统是不知道的,仍然需要业务线程执行while来轮询是否可以重新加锁。考虑这种情况: 解锁时有多个线程阻塞,那么所有该锁上的线程都被变成就绪状态, 第一个变为就绪状态的线程又执行加锁操作,那么其他的线程又会进入等待,对其他线程而言就是虚假唤醒。 在这种方式下,只有一个线程能够访问被互斥锁保护的资源。

### 读写锁, 共享互斥锁, rwlock

读写锁也叫共享互斥锁: 读模式共享和写模式互斥,本质上这种非常合理,因为在数据没有被写的前提下,多个使用者读取时完全不需要加锁的。读写锁有读加锁状态、写加锁状态和不加锁状态三种状态,当读写锁在写加锁模式下,任何试图对这个锁进行加锁的线程都会被阻塞,直到写进程对其解锁。

读优先的读写锁: 读写锁 rwlock 默认的也是读优先,也就是:当读写锁在读加锁模式先,任何线程都可以对其进行读加锁操作,但是所有试图进行写加锁操作的线程都会被阻塞,直到所有的读线程都解锁,因此读写锁很适合读次数远远大于写的情况。这种情况需要考虑写饥饿问题,也就是大量的读一直轮不到写,因此需要设置公平的读写策略。在一次面试中曾经问到实现一个写优先级的读写锁,感兴趣的可以想想如何实现。

### RCU 锁, Read Copy Update Lock

RCU锁是读写锁的扩展版本,简单来说就是支持多读多写同时加锁,多读没什么好说的,但是对于多写同时加锁,还是存在一些技术挑战的。RCU锁翻译为Read Copy Update Lock,读-拷贝-更新 锁。Copy拷贝: 写者在访问临界区时,写者将先拷贝一个临界区副本,然后对副本进行修改；Update更新: RCU机制将在在适当时机使用一个回调函数把指向原来临界区的指针重新指向新的被修改的临界区,锁机制中的垃圾收集器负责回调函数的调用。更新时机: 没有CPU再去操作这段被RCU保护的临界区后,这段临界区即可回收了,此时回调函数即被调用。从实现逻辑来看,RCU锁在多个写者之间的同步开销还是比较大的,涉及到多份数据拷贝,回调函数等,因此这种锁机制的使用范围比较窄,适用于读多写少的情况,如网络路由表的查询更新、设备状态表更新等,在业务开发中使用不是很多。

### 可重入锁和不可重入锁

递归锁 recursive mutex 可重入锁(reentrant mutex)
非递归锁 non-recursive mutex 不可重入锁(non-reentrant mutex)
Windows下的Mutex和Critical Section是可递归的。Linux下的pthread_mutex_t锁默认是非递归的。在Linux中可以显式设置PTHREAD_MUTEX_RECURSIVE属性,将pthread_mutex_t设为递归锁避免这种场景。 同一个线程可以多次获取同一个递归锁,不会产生死锁。而如果一个线程多次获取同一个非递归锁,则会产生死锁。

如下代码对于非递归锁的死锁示例:

MutexLock mutex;
void testa()  
{  
    mutex.lock();  
    do_sth();
    mutex.unlock();  
}
void testb()  
{  
  mutex.lock();
  testa();  
  mutex.unlock();
}
代码中testb使用了mutex并且调用testa,但是testa中也调用了相同的mutext,这种场景下如果mutex是非递归的就会出现死锁。

条件变量condition variables
条件变量是用来等待线程而不是上锁的,通常和互斥锁一起使用。互斥锁的一个明显的特点就是某些业务场景中无法借助系统来唤醒,仍然需要业务代码使用while来判断,这样效率本质上比较低。而条件变量通过允许线程阻塞和等待另一个线程发送信号来弥补互斥锁的不足,所以互斥锁和条件变量通常一起使用,来让条件变量异步唤醒阻塞的线程。

条件变量和互斥锁的典型使用就是生产者和消费者模型,这个模型非常经典,也在面试中经常被问到,示例代码:

# include <stdio.h>
# include <pthread.h>
# define MAX 5

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t notfull = PTHREAD_COND_INITIALIZER;  //是否队满
pthread_cond_t notempty = PTHREAD_COND_INITIALIZER; //是否队空
int top = 0;
int bottom = 0;

void*produce(void* arg)
{
    int i;
    for ( i = 0; i < MAX*2; i++)
    {
        pthread_mutex_lock(&mutex);
        while ((top+1)%MAX == bottom)
        {
            printf("full! producer is waiting\n");
            //等待队不满
            pthread_cond_wait(notfull, &mutex);
        }
        top = (top+1) % MAX;
        //发出队非空的消息
        pthread_cond_signal(notempty);
        pthread_mutex_unlock(&mutex);
    }
    return (void*)1;
}
void*consume(void* arg)
{
    int i;
    for ( i = 0; i < MAX*2; i++)
    {
        pthread_mutex_lock(&mutex);
        while ( top%MAX == bottom)
        {
            printf("empty! consumer is waiting\n");
            //等待队不空
            pthread_cond_wait(notempty, &mutex);
        }
        bottom = (bottom+1) % MAX;
        //发出队不满的消息
        pthread_cond_signal(notfull);
        pthread_mutex_unlock(&mutex);
    }
    return (void*)2;
}
int main(int argc, char *argv[])
{
    pthread_t thid1;
    pthread_t thid2;
    pthread_t thid3;
    pthread_t thid4;

    int ret1;
    int ret2;
    int ret3;
    int ret4;

    pthread_create(&thid1, NULL, produce, NULL);
    pthread_create(&thid2, NULL, consume, NULL);
    pthread_create(&thid3, NULL, produce, NULL);
    pthread_create(&thid4, NULL, consume, NULL);

    pthread_join(thid1, (void**)&ret1);
    pthread_join(thid2, (void**)&ret2);
    pthread_join(thid3, (void**)&ret3);
    pthread_join(thid4, (void**)&ret4);
    return 0;
}
其中pthread_cond_wait的使用是个需要注意的地方:pthread_cond_wait()是先将互斥锁解开,并陷入阻塞,直到pthread_signal()发出信号后pthread_cond_wait()再加上锁,然后退出。

---

线程同步: 递归锁、非递归锁 | 学步园
​
www.xuebuyuan.com
互斥锁、死锁和递归锁 - Bigberg - 博客园
​
www.cnblogs.com
可递归锁与非递归锁-hfm_honey-ChinaUnix博客
​
blog.chinaunix.net
[https://blog.csdn.net/qq_15437629/article/details/79116590](https://blog.csdn.net/qq_15437629/article/details/79116590)
​
blog.csdn.net

### 自旋锁  
[http://www.wiloon.com/?p=10215](http://www.wiloon.com/?p=10215)  
[http://www.wiloon.com/?p=10215&embed=true#?secret=FazEXCjmAy](http://www.wiloon.com/?p=10215&embed=true#?secret=FazEXCjmAy)  

### 排队自旋锁
[http://www.wiloon.com/?p=5496](http://www.wiloon.com/?p=5496)  
[http://www.wiloon.com/?p=5496&embed=true#?secret=dvWR0yOf3D](http://www.wiloon.com/?p=5496&embed=true#?secret=dvWR0yOf3D)  

### MCS锁
[http://wiloon.com/mcs](http://wiloon.com/mcs)  
[http://www.wiloon.com/?p=5493&embed=true#?secret=nvFCYYcuyH](http://www.wiloon.com/?p=5493&embed=true#?secret=nvFCYYcuyH)  

### CLH锁
[https://wiloon.com/clh](https://wiloon.com/clh)  
[http://www.wiloon.com/?p=10307&embed=true#?secret=qftAW3eZtB](http://www.wiloon.com/?p=10307&embed=true#?secret=qftAW3eZtB)  

### mcs clh 差异

从代码实现来看,CLH比MCS要简单得多。  
从自旋的条件来看,CLH是在前驱节点的属性上自旋,而MCS是在本地属性变量上自旋。  
从链表队列来看,CLH的队列是隐式的,CLHNode并不实际持有下一个节点；MCS的队列是物理存在的。  
CLH锁释放时只需要改变自己的属性,MCS锁释放则需要改变后继节点的属性。  
注意: 这里实现的锁都是独占的,且不能重入的。  

---

[https://coderbee.net/index.php/concurrent/20131115/577](https://coderbee.net/index.php/concurrent/20131115/577)  
[https://zhuanlan.zhihu.com/p/88241719](https://zhuanlan.zhihu.com/p/88241719)  
[https://coderbee.net/index.php/concurrent/20131115/577/embed#?secret=S6ykvE6LpW](https://coderbee.net/index.php/concurrent/20131115/577/embed#?secret=S6ykvE6LpW)  
[https://www.zhihu.com/question/53303879](https://www.zhihu.com/question/53303879)  
