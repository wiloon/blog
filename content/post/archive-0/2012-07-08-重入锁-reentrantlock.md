---
title: 重入锁 ReentrantLock
author: wiloon
type: post
date: 2012-07-08T08:14:54+00:00
url: /?p=3805
categories:
  - Java

---
ReentrantLock的实现不仅可以替代隐式的synchronized关键字，而且能够提供超过关键字本身的多种功能。
  
这里提到一个锁获取的公平性问题，如果在绝对时间上，先对锁进行获取的请求一定被先满足，那么这个锁是公平的，反之，是不公平的，也就是说等待时间最长的线程最有机会获取锁，也可以说锁的获取是有序的。ReentrantLock这个锁提供了一个构造函数，能够控制这个锁是否是公平的。
  
而锁的名字也是说明了这个锁具备了重复进入的可能，也就是说能够让当前线程多次的进行对锁的获取操作，这样的最大次数限制是Integer.MAX_VALUE，约21亿次左右。
  
事实上公平的锁机制往往没有非公平的效率高，因为公平的获取锁没有考虑到操作系统对线程的调度因素，这样造成JVM对于等待中的线程调度次序和操作系统对线程的调度之间的不匹配。对于锁的快速且重复的获取过程中，连续获取的概率是非常高的，而公平锁会压制这种情况，虽然公平性得以保障，但是响应比却下降了，但是并不是任何场景都是以TPS作为唯一指标的，因为公平锁能够减少“饥饿”发生的概率，等待越久的请求越是能够得到优先满足。

实现分析
  
在ReentrantLock中，对于公平和非公平的定义是通过对同步器AbstractQueuedSynchronizer的扩展加以实现的，也就是在tryAcquire的实现上做了语义的控制。

非公平的获取语义：
   
final boolean nonfairTryAcquire(int acquires) {
      
final Thread current = Thread.currentThread();
      
int c = getState();
      
if (c == 0) {
          
if (compareAndSetState(0, acquires)) {
              
setExclusiveOwnerThread(current);
              
return true;
          
}
      
} else if (current == getExclusiveOwnerThread()) {
          
int nextc = c + acquires;
                  
if (nextc < 0) // overflow
              
throw new Error("Maximum lock count exceeded");
          
setState(nextc);
          
return true;
      
}
      
return false;
  
}
  
上述逻辑主要包括：

如果当前状态为初始状态，那么尝试设置状态；
  
如果状态设置成功后就返回；
  
如果状态被设置，且获取锁的线程又是当前线程的时候，进行状态的自增；
  
如果未设置成功状态且当前线程不是获取锁的线程，那么返回失败。
  
公平的获取语义：
  
01
  
protected final boolean tryAcquire(int acquires) {
  
02
      
final Thread current = Thread.currentThread();
  
03
      
int c = getState();
  
04
      
if (c == 0) {
  
05
          
if (!hasQueuedPredecessors() && compareAndSetState(0, acquires)) {
  
06
              
setExclusiveOwnerThread(current);
  
07
              
return true;
  
08
          
}
  
09
      
} else if (current == getExclusiveOwnerThread()) {
  
10
          
int nextc = c + acquires;
  
11
          
if (nextc < 0)
  
12
              
throw new Error("Maximum lock count exceeded");
  
13
          
setState(nextc);
  
14
          
return true;
  
15
      
}
  
16
      
return false;
  
17
  
}
  
上述逻辑相比较非公平的获取，仅加入了当前线程（Node）之前是否有前置节点在等待的判断。hasQueuedPredecessors()方法命名有些歧义，其实应该是currentThreadHasQueuedPredecessors()更为妥帖一些，也就是说当前面没有人排在该节点（Node）前面时候队且能够设置成功状态，才能够获取锁。

释放语义：
  
01
  
protected final boolean tryRelease(int releases) {
  
02
      
int c = getState() &#8211; releases;
  
03
      
if (Thread.currentThread() != getExclusiveOwnerThread())
  
04
          
throw new IllegalMonitorStateException();
  
05
      
boolean free = false;
  
06
      
if (c == 0) {
  
07
          
free = true;
  
08
          
setExclusiveOwnerThread(null);
  
09
      
}
  
10
      
setState(c);
  
11
      
return free;
  
12
  
}
  
上述逻辑主要主要计算了释放状态后的值，如果为0则完全释放，返回true，反之仅是设置状态，返回false。
  
下面将主要的笔墨放在公平性和非公平性上，首先看一下二者测试的对比：
  
测试用例如下：

01
  
public class ReentrantLockTest {
  
02
      
private static Lock fairLock = new ReentrantLock(true);
  
03
      
private static Lock unfairLock = new ReentrantLock();
  
04

05
      
@Test
  
06
      
public void fair() {
  
07
          
System.out.println("fair version");
  
08
          
for (int i = 0; i < 5; i++) {
  
09
              
Thread thread = new Thread(new Job(fairLock));
  
10
              
thread.setName("" + i);
  
11
              
thread.start();
  
12
          
}
  
13

14
          
try {
  
15
              
Thread.sleep(5000);
  
16
          
} catch (InterruptedException e) {
  
17
              
e.printStackTrace();
  
18
          
}
  
19
      
}
  
20

21
      
@Test
  
22
      
public void unfair() {
  
23
          
System.out.println("unfair version");
  
24
          
for (int i = 0; i < 5; i++) {
  
25
              
Thread thread = new Thread(new Job(unfairLock));
  
26
              
thread.setName("" + i);
  
27
              
thread.start();
  
28
          
}
  
29

30
          
try {
  
31
              
Thread.sleep(5000);
  
32
          
} catch (InterruptedException e) {
  
33
              
e.printStackTrace();
  
34
          
}
  
35
      
}
  
36

37
      
private static class Job implements Runnable {
  
38
          
private Lock lock;
  
39
          
public Job(Lock lock) {
  
40
              
this.lock = lock;
  
41
          
}
  
42

43
          
@Override
  
44
          
public void run() {
  
45
              
for (int i = 0; i < 5; i++) {
  
46
                  
lock.lock();
  
47
                  
try {
  
48
                      
System.out.println("Lock by:"
  
49
                              
+ Thread.currentThread().getName());
  
50
                  
} finally {
  
51
                      
lock.unlock();
  
52
                  
}
  
53
              
}
  
54
          
}
  
55
      
}
  
56
  
}
  
调用非公平的测试方法，返回结果(部分)：
  
unfair version
  
Lock by:0
  
Lock by:0
  
Lock by:2
  
Lock by:2
  
Lock by:2
  
Lock by:2
  
Lock by:2
  
Lock by:0
  
Lock by:0
  
Lock by:0
  
Lock by:1
  
Lock by:1
  
Lock by:1
  
调用公平的测试方法，返回结果：
  
fair version
  
Lock by:0
  
Lock by:1
  
Lock by:0
  
Lock by:2
  
Lock by:3
  
Lock by:4
  
Lock by:1
  
Lock by:0
  
Lock by:2
  
Lock by:3
  
Lock by:4
  
仔细观察返回的结果(其中每个数字代表一个线程)，非公平的结果一个线程连续获取锁的情况非常多，而公平的结果连续获取的情况基本没有。那么在一个线程获取了锁的那一刻，究竟锁的公平性会导致锁有什么样的处理逻辑呢？
  
通过之前的同步器(AbstractQueuedSynchronizer)的介绍，在锁上是存在一个等待队列，sync队列，我们通过复写ReentrantLock的获取当前锁的sync队列，输出在ReentrantLock被获取时刻，当前的sync队列的状态。
  
修改测试如下：

01
  
public class ReentrantLockTest {
  
02
      
private static Lock fairLock = new ReentrantLock2(true);
  
03
      
private static Lock unfairLock = new ReentrantLock2();
  
04
      
@Test
  
05
      
public void fair() {
  
06
          
System.out.println("fair version");
  
07
          
for (int i = 0; i < 5; i++) {
  
08
              
Thread thread = new Thread(new Job(fairLock)) {
  
09
                  
public String toString() {
  
10
                      
return getName();
  
11
                  
}
  
12
              
};
  
13
              
thread.setName("" + i);
  
14
              
thread.start();
  
15
          
}
  
16
          
// sleep 5000ms
  
17
      
}
  
18

19
      
@Test
  
20
      
public void unfair() {
  
21
          
System.out.println("unfair version");
  
22
          
for (int i = 0; i < 5; i++) {
  
23
              
Thread thread = new Thread(new Job(unfairLock)) {
  
24
                  
public String toString() {
  
25
                      
return getName();
  
26
                  
}
  
27
              
};
  
28
              
thread.setName("" + i);
  
29
              
thread.start();
  
30
          
}
  
31
          
// sleep 5000ms
  
32
      
}
  
33

34
      
private static class Job implements Runnable {
  
35
          
private Lock lock;
  
36

37
          
public Job(Lock lock) {
  
38
              
this.lock = lock;
  
39
          
}
  
40

41
          
@Override
  
42
          
public void run() {
  
43
              
for (int i = 0; i < 5; i++) {
  
44
                  
lock.lock();
  
45
                  
try {
  
46
                      
System.out.println("Lock by:"
  
47
                              
+ Thread.currentThread().getName() + " and "
  
48
                              
+ ((ReentrantLock2) lock).getQueuedThreads()
  
49
                              
+ " waits.");
  
50
                  
} finally {
  
51
                      
lock.unlock();
  
52
                  
}
  
53
              
}
  
54
          
}
  
55
      
}
  
56

57
      
private static class ReentrantLock2 extends ReentrantLock {
  
58
          
// Constructor Override
  
59

60
          
private static final long serialVersionUID = 1773716895097002072L;
  
61

62
          
public Collection<Thread> getQueuedThreads() {
  
63
              
return super.getQueuedThreads();
  
64
          
}
  
65
      
}
  
66
  
}
  
上述逻辑主要是通过构造ReentrantLock2用来输出在sync队列中的线程内容，而且每个线程的toString方法被重写，这样当一个线程获取到锁时，sync队列里的内容也就可以得知了，运行结果如下：
  
调用非公平方法，返回结果：
  
unfair version
  
Lock by:0 and [] waits.
  
Lock by:0 and [] waits.
  
Lock by:3 and [2, 1] waits.
  
Lock by:3 and [4, 2, 1] waits.
  
Lock by:3 and [4, 2, 1] waits.
  
Lock by:3 and [0, 4, 2, 1] waits.
  
Lock by:3 and [0, 4, 2, 1] waits.
  
Lock by:1 and [0, 4, 2] waits.
  
Lock by:1 and [0, 4, 2] waits.
  
调用公平方法，返回结果：
  
fair version
  
Lock by:0 and [] waits.
  
Lock by:1 and [0, 4, 3, 2] waits.
  
Lock by:2 and [1, 0, 4, 3] waits.
  
Lock by:3 and [2, 1, 0, 4] waits.
  
Lock by:4 and [3, 2, 1, 0] waits.
  
Lock by:0 and [4, 3, 2, 1] waits.
  
Lock by:1 and [0, 4, 3, 2] waits.
  
Lock by:2 and [1, 0, 4, 3] waits.
  
可以明显看出，在非公平获取的过程中，“插队”现象非常严重，后续获取锁的线程根本不顾及sync队列中等待的线程，而是能获取就获取。反观公平获取的过程，锁的获取就类似线性化的，每次都由sync队列中等待最长的线程（链表的第一个，sync队列是由尾部结点添加，当前输出的sync队列是逆序输出）获取锁。一个 hasQueuedPredecessors方法能够获得公平性的特性，这点实际上是由AbstractQueuedSynchronizer来完成的，看一下acquire方法：

1
  
public final void acquire(int arg) {
  
2
      
if (!tryAcquire(arg) && acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
  
3
          
selfInterrupt();
  
4
  
}
  
可以看到，如果获取状态和在sync队列中排队是短路的判断，也就是说如果tryAcquire成功，那么是不会进入sync队列的，可以通过下图来深刻的认识公平性和AbstractQueuedSynchronizer的获取过程。
  
非公平的，或者说默认的获取方式如下图所示：

对于状态的获取，可以快速的通过tryAcquire的成功，也就是黄色的Fast路线，也可以由于tryAcquire的失败，构造节点，进入sync队列中排序后再次获取。因此可以理解为Fast就是一个快速通道，当例子中的线程释放锁之后，快速的通过Fast通道再次获取锁，就算当前sync队列中有排队等待的线程也会被忽略。这种模式，可以保证进入和退出锁的吞吐量，但是sync队列中过早排队的线程会一直处于阻塞状态，造成“饥饿”场景。
  
而公平性锁，就是在tryAcquire的调用中顾及当前sync队列中的等待节点（废弃了Fast通道），也就是任意请求都需要按照sync队列中既有的顺序进行，先到先得。这样很好的确保了公平性，但是可以从结果中看到，吞吐量就没有非公平的锁高了。

<http://ifeve.com/reentrantlock-and-fairness/>