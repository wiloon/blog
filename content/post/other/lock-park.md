---
title: "Java LockSupport, park unpark"
author: "-"
date: "2015-05-25T07:28:38+00:00"
url: "lock"
categories:
  - lock
tags:
  - java
---
## "Java LockSupport, park unpark"

LockSupport.park 调用后,线程状态是 WAITING

LockSupport.park() 和 unpark(),与object.wait()和notify()的区别？

1. 面向的主体不一样。LockSuport主要是针对Thread进行阻塞处理,可以指定阻塞队列的目标对象,每次可以指定具体的线程唤醒。Object.wait()是以对象为纬度,阻塞当前的线程和唤醒单个(随机)或者所有线程。
  
2. 实现机制不同。虽然LockSuport可以指定monitor的object对象,但和object.wait(),两者的阻塞队列并不交叉。object.notifyAll()不能唤醒LockSupport的阻塞Thread.

阻塞和唤醒是对于线程来说的,LockSupport的park/unpark更符合这个语义,以"线程"作为方法的参数, 语义更清晰,使用起来也更方便。而wait/notify的实现使得"线程"的阻塞/唤醒对线程本身来说是被动的,要准确的控制哪个线程、什么时候阻塞/唤醒很困难, 要不随机唤醒一个线程 (notify) 要不唤醒所有的 (notifyAll) 。

LockSupport.park() (以下简称 park() ) 可能是 java.util.concurrent 包最重要的函数了,因为很多 java.util.concurrent 中的功能类都是利用 park() 来实现它们各自的阻塞。在 park() 之前 Java 也有过类似功能的函数——suspend(),相应的唤醒函数是 resume()。不过 suspend() 有个严重的问题是父线程有可能在调用 suspend() 之前子线程已经调用了 resume(),那么这个 resume() 并不会解除在它之后的 suspend(),因此父线程就会陷入永久的等待中。相比于 suspend(),park() 可以在以下几种情况解除线程的等待状态: 

在 park() 前曾经调用过该线程的 unpark() 进而获得了一次"继续执行的权利",此时调用 park() 会立即返回,并且消耗掉相应的"继续执行的权利"。
  
在 park() 进入等待状态之后,有其他线程以该线程为目标调用 unpark()。
  
在 park() 进入等待状态之后,有其他线程以该线程为目标调用 interrupt()。
  
在 park() 进入等待状态之后,有可能会没有理由地解除等待状态。 (这也是为什么推荐在循环体中调用 park(),并在返回之后再次检查条件是否满足。) 
  
其中第一条就可以保证 park() 不会遇到和 suspend() 同样的问题。

最简单的使用 park() 是这样的
  
// 等待者(Thread1)
  
while (condition != true) {
      
LockSupport.park();
  
}

// 唤醒者(Thread2)
  
condition = true;
  
LockSupport.unpark(Thread1);

LockSupport类是Java6(JSR166-JUC)引入的一个类,提供了基本的线程同步原语. LockSupport 实际上是调用了Unsafe类里的函数,归结到Unsafe里,只有两个函数: 

public native void unpark(Thread jthread);
  
public native void park(boolean isAbsolute, long time);
  
isAbsolute参数是指明时间是绝对的,还是相对的。

仅仅两个简单的接口,就为上层提供了强大的同步原语。

先来解析下两个函数是做什么的。

unpark函数为线程提供"许可(permit)",线程调用park函数则等待"许可"。这个有点像信号量,但是这个"许可"是不能叠加的,"许可"是一次性的。

比如线程B连续调用了三次unpark函数,当线程A调用park函数就使用掉这个"许可",如果线程A再次调用park,则进入等待状态。

注意,unpark函数可以先于park调用。比如线程B调用unpark函数,给线程A发了一个"许可",那么当线程A调用park时,它发现已经有"许可"了,那么它会马上再继续运行。

实际上,park函数即使没有"许可",有时也会无理由地返回,这点等下再解析。

park和unpark的灵活之处

上面已经提到,unpark函数可以先于park调用,这个正是它们的灵活之处。

一个线程它有可能在别的线程unPark之前,或者之后,或者同时调用了park,那么因为park的特性,它可以不用担心自己的park的时序问题,否则,如果park必须要在unpark之前,那么给编程带来很大的麻烦！！

考虑一下,两个线程同步,要如何处理？

在Java5里是用wait/notify/notifyAll来同步的。wait/notify机制有个很蛋疼的地方是,比如线程B要用notify通知线程A,那么线程B要确保线程A已经在wait调用上等待了,否则线程A可能永远都在等待。编程的时候就会很蛋疼。

另外,是调用notify,还是notifyAll？

notify只会唤醒一个线程,如果错误地有两个线程在同一个对象上wait等待,那么又悲剧了。为了安全起见,貌似只能调用notifyAll了。

park/unpark模型真正解耦了线程之间的同步,线程之间不再需要一个Object或者其它变量来存储状态,不再需要关心对方的状态。

HotSpot里park/unpark的实现

每个java线程都有一个Parker实例,Parker类是这样定义的: 

class Parker : public os::PlatformParker {
  
private:
    
volatile int _counter ;
    
...
  
public:
    
void park(bool isAbsolute, jlong time);
    
void unpark();
    
...
  
}
  
class PlatformParker : public CHeapObj<mtInternal> {
    
protected:
      
pthread_mutex_t _mutex [1] ;
      
pthread_cond_t _cond [1] ;
      
...
  
}
  
可以看到Parker类实际上用Posix的mutex,condition来实现的。

在Parker类里的_counter字段,就是用来记录所谓的"许可"的。

当调用park时,先尝试直接能否直接拿到"许可",即_counter>0时,如果成功,则把_counter设置为0,并返回: 

void Parker::park(bool isAbsolute, jlong time) {
    
// Ideally we'd do something useful while spinning, such
    
// as calling unpackTime().

// Optional fast-path check:
    
// Return immediately if a permit is available.
    
// We depend on Atomic::xchg() having full barrier semantics
    
// since we are doing a lock-free update to _counter.
    
if (Atomic::xchg(0, &_counter) > 0) return;
  
如果不成功,则构造一个ThreadBlockInVM,然后检查_counter是不是>0,如果是,则把_counter设置为0,unlock mutex并返回: 

ThreadBlockInVM tbivm(jt);
  
if (_counter > 0) { // no wait needed
    
_counter = 0;
    
status = pthread_mutex_unlock(_mutex);
  
否则,再判断等待的时间,然后再调用pthread_cond_wait函数等待,如果等待返回,则把_counter设置为0,unlock mutex并返回: 

if (time == 0) {
    
status = pthread_cond_wait (_cond, _mutex) ;
  
}
  
_counter = 0 ;
  
status = pthread_mutex_unlock(_mutex) ;
  
assert_status(status == 0, status, "invariant") ;
  
OrderAccess::fence();
  
当unpark时,则简单多了,直接设置_counter为1,再unlock mutext返回。如果_counter之前的值是0,则还要调用pthread_cond_signal唤醒在park中等待的线程: 

void Parker::unpark() {
    
int s, status ;
    
status = pthread_mutex_lock(_mutex);
    
assert (status == 0, "invariant") ;
    
s = _counter;
    
_counter = 1;
    
if (s < 1) {
       
if (WorkAroundNPTLTimedWaitHang) {
          
status = pthread_cond_signal (_cond) ;
          
assert (status == 0, "invariant") ;
          
status = pthread_mutex_unlock(_mutex);
          
assert (status == 0, "invariant") ;
       
} else {
          
status = pthread_mutex_unlock(_mutex);
          
assert (status == 0, "invariant") ;
          
status = pthread_cond_signal (_cond) ;
          
assert (status == 0, "invariant") ;
       
}
    
} else {
      
pthread_mutex_unlock(_mutex);
      
assert (status == 0, "invariant") ;
    
}
  
}
  
简而言之,是用mutex和condition保护了一个_counter的变量,当park时,这个变量置为了0,当unpark时,这个变量置为1。
  
值得注意的是在park函数里,调用pthread_cond_wait时,并没有用while来判断,所以posix condition里的"Spurious wakeup"一样会传递到上层Java的代码里。

关于"Spurious wakeup",参考上一篇blog: http://blog.csdn.net/hengyunabc/article/details/27969613

if (time == 0) {
    
status = pthread_cond_wait (_cond, _mutex) ;
  
}
  
这也就是为什么Java dos里提到,当下面三种情况下park函数会返回: 

Some other thread invokes unpark with the current thread as the target; or
  
Some other thread interrupts the current thread; or
  
The call spuriously (that is, for no reason) returns.
  
相关的实现代码在: 

http://hg.openjdk.java.net/jdk7/jdk7/hotspot/file/81d815b05abb/src/share/vm/runtime/park.hpp

http://hg.openjdk.java.net/jdk7/jdk7/hotspot/file/81d815b05abb/src/share/vm/runtime/park.cpp

http://hg.openjdk.java.net/jdk7/jdk7/hotspot/file/81d815b05abb/src/os/linux/vm/os_linux.hpp

http://hg.openjdk.java.net/jdk7/jdk7/hotspot/file/81d815b05abb/src/os/linux/vm/os_linux.cpp

其它的一些东西: 

Parker类在分配内存时,使用了一个技巧,重载了new函数来实现了cache line对齐。

// We use placement-new to force ParkEvent instances to be
  
// aligned on 256-byte address boundaries. This ensures that the least
  
// significant byte of a ParkEvent address is always 0.

void * operator new (size_t sz) ;
  
Parker里使用了一个无锁的队列在分配释放Parker实例: 

volatile int Parker::ListLock = 0 ;
  
Parker * volatile Parker::FreeList = NULL ;

Parker \* Parker::Allocate (JavaThread \* t) {
    
guarantee (t != NULL, "invariant") ;
    
Parker * p ;

// Start by trying to recycle an existing but unassociated
    
// Parker from the global free list.
    
for (;;) {
      
p = FreeList ;
      
if (p == NULL) break ;
      
// 1: Detach
      
// Tantamount to p = Swap (&FreeList, NULL)
      
if (Atomic::cmpxchg_ptr (NULL, &FreeList, p) != p) {
         
continue ;
      
}

    // We've detached the list.  The list in-hand is now
    // local to this thread.   This thread can operate on the
    // list without risk of interference from other threads.
    // 2: Extract -- pop the 1st element from the list.
    Parker * List = p->FreeNext ;
    if (List == NULL) break ;
    for (;;) {
        // 3: Try to reattach the residual list
        guarantee (List != NULL, "invariant") ;
        Parker * Arv =  (Parker *) Atomic::cmpxchg_ptr (List, &FreeList, NULL) ;
        if (Arv == NULL) break ;
    
        // New nodes arrived.  Try to detach the recent arrivals.
        if (Atomic::cmpxchg_ptr (NULL, &FreeList, Arv) != Arv) {
            continue ;
        }
        guarantee (Arv != NULL, "invariant") ;
        // 4: Merge Arv into List
        Parker * Tail = List ;
        while (Tail->FreeNext != NULL) Tail = Tail->FreeNext ;
        Tail->FreeNext = Arv ;
    }
    break ;
    

}

if (p != NULL) {
      
guarantee (p->AssociatedWith == NULL, "invariant") ;
    
} else {
      
// Do this the hard way - materialize a new Parker..
      
// In rare cases an allocating thread might detach
      
// a long list - installing null into FreeList -and
      
// then stall. Another thread calling Allocate() would see
      
// FreeList == null and then invoke the ctor. In this case we
      
// end up with more Parkers in circulation than we need, but
      
// the race is rare and the outcome is benign.
      
// Ideally, the # of extant Parkers is equal to the
      
// maximum # of threads that existed at any one time.
      
// Because of the race mentioned above, segments of the
      
// freelist can be transiently inaccessible. At worst
      
// we may end up with the # of Parkers in circulation
      
// slightly above the ideal.
      
p = new Parker() ;
    
}
    
p->AssociatedWith = t ; // Associate p with t
    
p->FreeNext = NULL ;
    
return p ;
  
}

void Parker::Release (Parker * p) {
    
if (p == NULL) return ;
    
guarantee (p->AssociatedWith != NULL, "invariant") ;
    
guarantee (p->FreeNext == NULL , "invariant") ;
    
p->AssociatedWith = NULL ;
    
for (;;) {
      
// Push p onto FreeList
      
Parker * List = FreeList ;
      
p->FreeNext = List ;
      
if (Atomic::cmpxchg_ptr (p, &FreeList, List) == List) break ;
    
}
  
}
  
总结与扯谈

JUC(Java Util Concurrency)仅用简单的park, unpark和CAS指令就实现了各种高级同步数据结构,而且效率很高,令人惊叹。

在C++程序员各种自制轮子的时候,Java程序员则有很丰富的并发数据结构,如lock,latch,queue,map等信手拈来。

要知道像C++直到C++11才有标准的线程库,同步原语,但离高级的并发数据结构还有很远。boost库有提供一些线程,同步相关的类,但也是很简单的。Intel的tbb有一些高级的并发数据结构,但是国内boost都用得少,更别说tbb了。

最开始研究无锁算法的是C/C++程序员,但是后来很多Java程序员,或者类库开始自制各种高级的并发数据结构,经常可以看到有分析Java并发包的文章。反而C/C++程序员总是在分析无锁的队列算法。高级的并发数据结构,比如并发的HashMap,没有看到有相关的实现或者分析的文章。在C++11之后,这种情况才有好转。

因为正确高效实现一个Concurrent Hash Map是很困难的,要对内存CPU有深刻的认识,而且还要面对CPU不断升级带来的各种坑。

我认为真正值得信赖的C++并发库,只有Intel的tbb和微软的PPL。

LockSupport.park() 中断响应

```java
  
import java.util.concurrent.locks.LockSupport;
  
public class LockSupportTest {
      
public static void main(String[] args) {
          
try {
              
t2();
          
} catch (Exception e) {
              
e.printStackTrace();
          
}
      
}
      
public static void t2() throws Exception {
          
Thread t = new Thread(new Runnable() {
              
private int count = 0;

@Override
              
public void run() {
                  
long start = System.currentTimeMillis();
                  
long end = 0;

while ((end - start) <= 1000) {
                      
count++;
                      
end = System.currentTimeMillis();
                  
}

System.out.println("after 1 second.count=" + count);

//等待或许许可
                  
LockSupport.park();
                  
System.out.println("thread over." + Thread.currentThread().isInterrupted());

}
          
});

t.start();

Thread.sleep(2000);

// 中断线程
          
t.interrupt();

System.out.println("main over");
      
}
  
}

```

最终线程会打印出thread over.true。这说明线程如果因为调用park而阻塞的话,能够响应中断请求(中断状态被设置成true),但是不会抛出InterruptedException。

https://software.intel.com/en-us/node/506042 Intel® Threading Building Blocks

http://msdn.microsoft.com/en-us/library/dd492418.aspx Parallel Patterns Library (PPL)

另外FaceBook也开源了一个C++的类库,里面也有并发数据结构。

https://github.com/facebook/folly
  
http://www.importnew.com/20428.html
  
http://blog.dyngr.com/blog/2016/09/09/how-to-make-a-thread-wait/
  
https://www.zhihu.com/question/26471972/answer/74773092
  
http://blog.csdn.net/aitangyong/article/details/38373137