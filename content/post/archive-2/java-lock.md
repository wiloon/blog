---
title: java juc锁 Lock
author: "-"
date: 2017-03-24T15:09:53+00:00
url: /?p=9919
categories:
  - Inbox
tags:
  - reprint
---
## java juc锁 Lock
与synchronized不同的是,Lock完全用Java写成,在java这个层面是无关JVM实现的。
  
在java.util.concurrent.locks包中有很多Lock的实现类,常用的有ReentrantLock、ReadWriteLock (实现类ReentrantReadWriteLock) ,其实现都依赖java.util.concurrent.AbstractQueuedSynchronizer类

锁像synchronized同步块一样,是一种线程同步机制,但比Java中的synchronized同步块更复杂。因为锁 (以及其它更高级的线程同步机制) 是由synchronized同步块的方式实现的,所以我们还不能完全摆脱synchronized关键字 (译者注: 这说的是Java 5之前的情况) 。

自Java 5开始,java.util.concurrent.locks包中包含了一些锁的实现,因此你不用去实现自己的锁了。但是你仍然需要去了解怎样使用这些锁,且了解这些实现背后的理论也是很有用处的。可以参考我对java.util.concurrent.locks.Lock的介绍,以了解更多关于锁的信息。
  
Lock是java.util.concurrent.locks包下的接口,Lock 实现提供了比使用synchronized 方法和语句可获得的更广泛的锁定操作,它能以更优雅的方式处理线程同步问题

```java
  
//一个简单的锁
  
public class Counter{
      
private int count = 0;
      
public int inc(){
          
synchronized(this){
              
return ++count;
          
}
      
}
  
}
  
```

可以看到在inc()方法中有一个synchronized(this)代码块。该代码块可以保证在同一时间只有一个线程可以执行return ++count。虽然在synchronized的同步块中的代码可以更加复杂,但是++count这种简单的操作已经足以表达出线程同步的意思。

以下的Counter类用Lock代替synchronized达到了同样的目的: 

```java
  
public class Counter{
      
private Lock lock = new Lock();
      
private int count = 0;

public int inc(){
          
lock.lock();
          
int newCount = ++count;
          
lock.unlock();
          
return newCount;
      
}
  
}
  
```

lock()方法会对Lock实例对象进行加锁,因此所有对该对象调用lock()方法的线程都会被阻塞,直到该Lock对象的unlock()方法被调用。

```java
  
public class LockTest {
      
public static void main(String[] args) {
          
final OutPutter1 output = new OutPutter1();
          
new Thread() {
              
public void run() {
                  
output.output("zhangsan");
              
}
          
}.start();
          
new Thread() {
              
public void run() {
                  
output.output("lisi");
              
}
          
}.start();
      
}
  
}

class OutPutter1 {
      
private Lock lock = new ReentrantLock();// 锁对象

void output(String name) {
          
// 线程输出方法
          
lock.lock();// 得到锁
          
try {
              
for (int i = 0; i < name.length(); i++) {
                  
System.out.print(name.charAt(i));
              
}
          
} finally {
              
lock.unlock();// 释放锁
          
}
      
}
  
}
  
```

这样就实现了和sychronized一样的同步效果,需要注意的是,用sychronized修饰的方法或者语句块在代码执行完之后锁自动释放,而用Lock需要我们手动释放锁,所以为了保证锁最终被释放(发生异常情况),要把互斥区放在try内,释放锁放在finally内。

如果说这就是Lock,那么它不能成为同步问题更完美的处理方式,下面要介绍的是读写锁(ReadWriteLock),我们会有一种需求,在对数据进行读写的时候,为了保证数据的一致性和完整性,需要读和写是互斥的,写和写是互斥的,但是读和读是不需要互斥的,这样读和读不互斥性能更高些,来看一下不考虑互斥情况的代码原型: 


  
print?
  
public class ReadWriteLockTest {
  
public static void main(String[] args) {
  
final Data data = new Data();
  
for (int i = 0; i < 3; i++) {
  
new Thread(new Runnable() {
  
public void run() {
  
for (int j = 0; j < 5; j++) {
  
data.set(new Random().nextInt(30));
  
}
  
}
  
}).start();
  
}
  
for (int i = 0; i < 3; i++) {
  
new Thread(new Runnable() {
  
public void run() {
  
for (int j = 0; j < 5; j++) {
  
data.get();
  
}
  
}
  
}).start();
  
}
  
}
  
}
  
class Data {
  
private int data;// 共享数据
  
public void set(int data) {
  
System.out.println(Thread.currentThread().getName() + "准备写入数据");
  
try {
  
Thread.sleep(20);
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
this.data = data;
  
System.out.println(Thread.currentThread().getName() + "写入" + this.data);
  
}
  
public void get() {
  
System.out.println(Thread.currentThread().getName() + "准备读取数据");
  
try {
  
Thread.sleep(20);
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
System.out.println(Thread.currentThread().getName() + "读取" + this.data);
  
}
  
}
  
部分输出结果: 


  
print?
  
Thread-1准备写入数据
  
Thread-3准备读取数据
  
Thread-2准备写入数据
  
Thread-0准备写入数据
  
Thread-4准备读取数据
  
Thread-5准备读取数据
  
Thread-2写入12
  
Thread-4读取12
  
Thread-5读取5
  
Thread-1写入12
  
我们要实现写入和写入互斥,读取和写入互斥,读取和读取互斥,在set和get方法加入sychronized修饰符: 


  
print?
  
public synchronized void set(int data) {…}
  
public synchronized void get() {…}
  
部分输出结果: 
  

  
print?
  
Thread-0准备写入数据
  
Thread-0写入9
  
Thread-5准备读取数据
  
Thread-5读取9
  
Thread-5准备读取数据
  
Thread-5读取9
  
Thread-5准备读取数据
  
Thread-5读取9
  
Thread-5准备读取数据
  
Thread-5读取9
  
我们发现,虽然写入和写入互斥了,读取和写入也互斥了,但是读取和读取之间也互斥了,不能并发执行,效率较低,用读写锁实现代码如下: 


  
print?
  
class Data {
  
private int data;// 共享数据
  
private ReadWriteLock rwl = new ReentrantReadWriteLock();
  
public void set(int data) {
  
rwl.writeLock().lock();// 取到写锁
  
try {
  
System.out.println(Thread.currentThread().getName() + "准备写入数据");
  
try {
  
Thread.sleep(20);
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
this.data = data;
  
System.out.println(Thread.currentThread().getName() + "写入" + this.data);
  
} finally {
  
rwl.writeLock().unlock();// 释放写锁
  
}
  
}
  
public void get() {
  
rwl.readLock().lock();// 取到读锁
  
try {
  
System.out.println(Thread.currentThread().getName() + "准备读取数据");
  
try {
  
Thread.sleep(20);
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
System.out.println(Thread.currentThread().getName() + "读取" + this.data);
  
} finally {
  
rwl.readLock().unlock();// 释放读锁
  
}
  
}
  
}
  
部分输出结果: 


  
print?
  
Thread-4准备读取数据
  
Thread-3准备读取数据
  
Thread-5准备读取数据
  
Thread-5读取18
  
Thread-4读取18
  
Thread-3读取18
  
Thread-2准备写入数据
  
Thread-2写入6
  
Thread-2准备写入数据
  
Thread-2写入10
  
Thread-1准备写入数据
  
Thread-1写入22
  
Thread-5准备读取数据
  
从结果可以看出实现了我们的需求,这只是锁的基本用法,锁的机制还需要继续深入学习。

juc中的锁源码分析

juc中的锁分两种, 1. 可重入锁; 2. 读写锁. 两者都用到了一个通用组件 AbstractQueuedSynchronizer. 先从它说起

3.1 AbstractQueuedSynchronizer

利用了一个int来表示状态, 内部基于FIFO队列及UnSafe的CAS原语作为操纵状态的数据结构, AQS以单个 int 类型的原子变量来表示其状态,定义了4个抽象方法 ( tryAcquire(int)、tryRelease(int)、tryAcquireShared(int)、tryReleaseShared(int),前两个方法用于独占/排他模式,后两个用于共享模式 ) 留给子类实现,用于自定义同步器的行为以实现特定的功能。这方面的介绍大家看一下资料2, 描述非常清楚

引用资料2中的一段话:

同步器是实现锁的关键,利用同步器将锁的语义实现,然后在锁的实现中聚合同步器。可以这样理解: 锁的API是面向使用者的,它定义了与锁交互的公共行为,而每个锁需要完成特定的操作也是透过这些行为来完成的 (比如: 可以允许两个线程进行加锁,排除两个以上的线程) ,但是实现是依托给同步器来完成；同步器面向的是线程访问和资源控制,它定义了线程对资源是否能够获取以及线程的排队等操作。锁和同步器很好的隔离了二者所需要关注的领域,严格意义上讲,同步器可以适用于除了锁以外的其他同步设施上 (包括锁) 。
  
3.2 ReentrantLock

可重入锁, 支持公平和非公平策略(FairSync/NonFairSync), 默认非公平锁, 内部Sync继承于AbstractQueuedSynchronizer.

两者代码区别是:

FairSync 代码中对于尝试加锁时(tryAcquire)多了一个判断方法, 判断等待队列中是否还有比当前线程更早的, 如果为空,或者当前线程线程是等待队列的第一个时才占有锁

if (c == 0) {
      
if (!hasQueuedPredecessors() && //就是这里
          
compareAndSetState(0, acquires)) {
          
setExclusiveOwnerThread(current);
          
return true;
      
}
  
}

public final boolean hasQueuedPredecessors() {
      
// The correctness of this depends on head being initialized
      
// before tail and on head.next being accurate if the current
      
// thread is first in queue.
      
Node t = tail; // Read fields in reverse initialization order
      
Node h = head;
      
Node s;
      
return h != t &&
          
((s = h.next) == null || s.thread != Thread.currentThread());
  
}
  
3.3 ReentrantReadWriteLock

3.3.1 引子

可重入的读写锁, 首先我想到的是它的适用场景, 它与volatile有何区别, 又有何优势呢?

volatile只能保证可见性, 在1写N读的情况下, 使用它就足够了. 但是如何N写N读, 如何保证数据一致性而又减少并行度的损失呢? 就要看ReentrantReadWriteLock了.
  
3.3.2 源码分析:

读锁

public static class ReadLock implements Lock, java.io.Serializable {
      
private final Sync sync;

    protected ReadLock(ReentrantReadWriteLock lock) {
        sync = lock.sync;
    }
    
    public void lock() {
        sync.acquireShared(1);//共享锁
    }
    
    public void lockInterruptibly() throws InterruptedException {
        sync.acquireSharedInterruptibly(1);
    }
    
    public  boolean tryLock() {
        return sync.tryReadLock();
    }
    
    public boolean tryLock(long timeout, TimeUnit unit) throws InterruptedException {
        return sync.tryAcquireSharedNanos(1, unit.toNanos(timeout));
    }
    
    public  void unlock() {
        sync.releaseShared(1);
    }
    
    public Condition newCondition() {
        throw new UnsupportedOperationException();
    }
    

}
  
写锁

public static class WriteLock implements Lock, java.io.Serializable {
      
private final Sync sync;
      
protected WriteLock(ReentrantReadWriteLock lock) {
          
sync = lock.sync;
      
}
      
public void lock() {
          
sync.acquire(1);//独占锁
      
}

    public void lockInterruptibly() throws InterruptedException {
        sync.acquireInterruptibly(1);
    }
    
    public boolean tryLock( ) {
        return sync.tryWriteLock();
    }
    
    public boolean tryLock(long timeout, TimeUnit unit) throws InterruptedException {
        return sync.tryAcquireNanos(1, unit.toNanos(timeout));
    }
    
    public void unlock() {
        sync.release(1);
    }
    
    public Condition newCondition() {
        return sync.newCondition();
    }
    
    public boolean isHeldByCurrentThread() {
        return sync.isHeldExclusively();
    }
    
    public int getHoldCount() {
        return sync.getWriteHoldCount();
    }
    

}
  
WriteLock就是一个独占锁,这和ReentrantLock里面的实现几乎相同,都是使用了AQS的acquire/release操作。当然了在内部处理方式上与ReentrantLock还是有一点不同的。对比清单1和清单2可以看到,ReadLock获取的是共享锁,WriteLock获取的是独占锁。

AQS中有一个state字段 (int类型,32位) 用来描述有多少线程获持有锁。在独占锁的时代这个值通常是0或者1 (如果是重入的就是重入的次数) ,在共享锁的时代就是持有锁的数量。在上一节中谈到,ReadWriteLock的读、写锁是相关但是又不一致的,所以需要两个数来描述读锁 (共享锁) 和写锁 (独占锁) 的数量。显然现在一个state就不够用了。于是在ReentrantReadWrilteLock里面将这个字段一分为二,高位16位表示共享锁的数量,低位16位表示独占锁的数量 (或者重入数量) 。2^16-1=65536,所以共享锁和独占锁的数量最大只能是65535。
  
3.3.3 写入锁分析:

持有锁线程数非0 (c=getState()不为0) ,如果写线程数 (w) 为0 (那么读线程数就不为0) 或者独占锁线程 (持有锁的线程) 不是当前线程就返回失败,或者写入锁的数量 (其实是重入数) 大于65535就抛出一个Error异常

如果当且写线程数位0 (那么读线程也应该为0,因为步骤1已经处理c!=0的情况) ,并且当前线程需要阻塞那么就返回失败；如果增加写线程数失败也返回失败

设置独占线程 (写线程) 为当前线程,返回true。

protected final boolean tryAcquire(int acquires) {
      
Thread current = Thread.currentThread();
      
int c = getState();
      
int w = exclusiveCount(c);
      
if (c != 0) {
          
if (w == 0 || current != getExclusiveOwnerThread())
              
return false;
          
if (w + exclusiveCount(acquires) > MAX_COUNT)
              
throw new Error("Maximum lock count exceeded");
      
}
      
if ((w == 0 && writerShouldBlock(current)) ||
          
!compareAndSetState(c, c + acquires))
          
return false;
      
setExclusiveOwnerThread(current);
      
return true;
  
}
  
3.3.4 列出读写锁几个特性:

重入性

读写锁允许读线程和写线程按照请求锁的顺序重新获取读取锁或者写入锁。当然了只有写线程释放了锁,读线程才能获取重入锁。 写线程获取写入锁后可以再次获取读取锁,但是读线程获取读取锁后却不能获取写入锁。 另外读写锁最多支持65535个递归写入锁和65535个递归读取锁。
  
锁降级

写线程获取写入锁后可以获取读取锁,然后释放写入锁,这样就从写入锁变成了读取锁,从而实现锁降级的特性。
  
锁升级

读取锁是不能直接升级为写入锁的。因为获取一个写入锁需要释放所有读取锁,所以如果有两个读取锁视图获取写入锁而都不释放读取锁时就会发生死锁。
  
锁获取中断

读取锁和写入锁都支持获取锁期间被中断。这个和独占锁一致。
  
条件变量

写入锁提供了条件变量(Condition)的支持,这个和独占锁一致,但是读取锁却不允许获取条件变量,将得到一个UnsupportedOperationException异常。
  
参考资料:

http://zhwbqd.github.io/2015/02/13/lock-in-java.html
  
http://blog.csdn.net/ghsau/article/details/7461369,转载请注明。
  
http://blog.csdn.net/ghsau/article/details/7461369

## Java 锁

# 自旋锁,自适应自旋锁,锁消除,锁膨胀,轻量级锁,偏向锁

### 自旋锁
在互斥同步的时候,对性能影响最大的就是阻塞的实现,挂起线程,恢复线程等的操作都需要用户态转为内核态去完成。这些操作给性能带来了巨大的压力。

​ 虚拟机的开发团也注意到,共享数据的锁定状态只会持续很短的时间。为了这很短的时间让线程挂起,然后转为内核态的时间可能比锁定状态的时间更长。所以,我们可以让等待同步锁的进程不要进入阻塞,而是在原地稍微等待一会儿,不要放弃处理器的执行时间,看看持有锁的线程是不是很快就会释放锁。为了让线程等待,我们可以让线程执行一个 忙循环 (原地自旋) ,这就是自旋锁。

​ 自旋锁在 JDK1.4.2 之后就已经引入,但是默认是关闭的。我们可以使用 -XX:+UseSpinning参数来开启。在 JDK1.6 之后就默认开启了。自旋锁并不是阻塞,所以它避免了用户态到内核态的频繁转化,但是它是要占用处理器的执行时间的。

​ 如果占有对象锁的线程在很短的时间内就执行完,然后释放锁,这样的话,自旋锁的效果就会非常好。

​ 如果占有对象锁的线程执行时间很长,那么自旋锁会白白消耗处理器的执行时间,这就带来了性能的浪费。这样的话,还不如将等待的线程进行阻塞。默认的自旋次数是 10,也就是说,如果一个线程自旋 10 次之后,还没有拿到对象锁,那么就会进行阻塞。

​ 我们也可以使用参数 -XX:PreBlockSpin来更改。

### 自适应自旋锁

​ 无论是使用默认的 10 次,还是用户自定义的次数,对整个虚拟机来说所有的线程都是一样的。但是同一个虚拟机中线程的状态并不是一样的,有的锁对象长一点,有的短一点,所以,在 JDK1.6 的时候,引入了 自适应自旋锁。

​ 自适应自旋锁意味着自旋的时间不在固定了,而是根据当前的情况动态设置。

​ 主要取决于 同一个锁上一次的自旋时间和 锁的拥有者的状态。

​ 如果在同一个对象锁上,上一个获取这个对象锁的线程在自旋等待成功了,没有进入阻塞状态,说明这个对象锁的线程执行时间会很短,虚拟机认为这次也有可能再次成功,进而允许此次自旋时间可以更长一点。

​ 如果对于某个锁,自旋状态下很少获得过锁,说明这个对象锁的线程执行时间相对会长一点,那么以后虚拟机可能会直接省略掉自旋的过程。避免浪费处理器资源。

​ 自适应自旋锁的加入,随着程序运行时间的增长以及性能监控系统信息的不断完善,虚拟机对程序的自旋时间预测越来越准确,也就是 虚拟机越来越聪明了。


###  轻量级锁 (Lightweight Locking)
Java 的多线程安全是基于 Lock 机制实现的,而 Lock 的性能往往不如人意。  
原因是,monitorenter 与 monitorexit 这两个控制多线程同步的 bytecode 原语,是JVM依赖操作系统互斥(mutex)来实现的。  

互斥是一种会导致线程挂起,并在较短的时间内又需要重新调度回原线程的,较为消耗资源的操作。

为了优化Java的Lock机制,从Java6开始引入了轻量级锁的概念。

轻量级锁 (Lightweight Locking) 本意是为了减少多线程进入互斥的几率,并不是要替代互斥。
  
它利用了 CPU 原语 Compare-And-Swap(CAS, 汇编指令 `CMPXCHG`), 尝试在进入互斥前, 进行补救。

本文将详细介绍JVM如何利用CAS,实现轻量级锁。

原理详解
  
Java Object Model中定义,Object Header是一个2字 (1 word = 4 byte) 长度的存储区域。
  
第一个字长度的区域用来标记同步,GC以及hash code等,官方称之为 mark word。第二个字长度的区域是指向到对象的Class。

在2个word中,mark word是轻量级锁实现的关键。它的结构见下表

从表中可以看到,state为lightweight locked的那行即为轻量级锁标记。bitfieds名为指向lock record的指针,这里的lock record,其实是一块分配在线程堆栈上的空间区域。
  
用于CAS前,拷贝object上的mark word(为什么要拷贝,请看下文)。
  
第三项是重量级锁标记。后面的状态单词很有趣,inflated,译为膨胀,在这里意思其实是锁已升级到OS-level。
  
在本文的范围内,我们只关注第二和第三项即可。

为了能直观的理解lock,unlock与mark word之间的联系,我画了一张流程图: 

在图中,提到了拷贝object mark word,由于脱离了原始mark word,官方将它冠以displaced前缀,即displaced mark word(置换标记字)。
  
这个displaced mark word是整个轻量级锁实现的关键,在CAS中的compare就需要用它作为条件。

为什么要拷贝mark word？
  
其实很简单,原因是为了不想在lock与unlock这种底层操作上再加同步。

在拷贝完object mark word之后,JVM做了一步交换指针的操作,即流程中第一个橙色矩形框内容所述。
  
将object mark word里的轻量级锁指针指向lock record所在的stack指针,作用是让其他线程知道,该object monitor已被占用。
  
lock record里的owner指针指向object mark word的作用是为了在接下里的运行过程中,识别哪个对象被锁住了。

下图直观地描述了交换指针的操作。

exchange_pointer_1

最后一步unlock中,我们发现,JVM同样使用了CAS来验证object mark word在持有锁到释放锁之间,有无被其他线程访问。
  
如果其他线程在持有锁这段时间里,尝试获取过锁,则可能自身被挂起,而mark word的重量级锁指针也会被相应修改。
  
此时,unlock后就需要唤醒被挂起的线程。

转载请注明原文链接: http://kenwublog.com/theory-of-lightweight-locking-upon-cas

http://blog.csdn.net/hsuxu/article/details/9472389


https://xie.infoq.cn/article/25f183de98f8f3337f1a70603

