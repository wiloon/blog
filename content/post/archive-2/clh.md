---
title: CLH队列,CLH锁
author: "-"
date: 2017-05-17T02:57:37+00:00
url: clh
categories:
  - lock

tags:
  - reprint
---
## CLH队列,CLH锁

CLH的发明人是: Craig,Landin and Hagersten。
CLH锁即 Craig, Landin, and Hagersten (CLH) locks
CLH锁是一个自旋锁,能确保无饥饿性,提供先来先服务的公平性。
CLH锁是一种基于链表的可扩展、高性能、公平的自旋锁,申请线程只在本地变量上自旋,它不断轮询前驱的状态,如果发现前驱释放了锁就结束自旋。

### CLH算法实现
CLH队列锁表示为QNode对象的链表,QNode中含有一个locked字段,该字段若为true表示该线程需要获取锁,且不释放锁,为false表示线程释放了锁。结点之间是通过隐形的链表相连,之所以叫隐形的链表是因为这些结点之间没有明显的next指针,每个线程通过一个线程局部变量pred指向其前驱,线程通过检测前驱结点的locked域来判断是否轮到自己。如果该域为true,则前驱线程要么已经获得锁要么正在等待锁；如果该域为false,则前驱进程已释放锁,轮到自己了。正常情况下,队列链中只有一个结点的locked域为false。CLHLock上还有一个尾指针,始终指向队列的最后一个结点。

当一个线程调用lock()方法想获得锁时,将自己的locked域置为true,表示该线程不准备释放锁,然后并将自己的结点加入到队列链尾部。最后就是在前驱的locked域上旋转,等待前驱释放锁。当这个线程调用unlock()方法要释放锁时,线程要将自己的locked域置为false,表示已经释放锁,然后将前驱结点作为自己的新结点以便日后访问。

```java
  
//clh 1
  
class ClhSpinLock {
      
private final ThreadLocal<Node> prev;
      
private final ThreadLocal<Node> node;
      
private final AtomicReference<Node> tail = new AtomicReference<Node>(new Node());

public ClhSpinLock() {
          
this.node = new ThreadLocal<Node>() {
              
protected Node initialValue() {
                  
return new Node();
              
}
          
};

this.prev = new ThreadLocal<Node>() {
              
protected Node initialValue() {
                  
return null;
              
}
          
};
      
}

public void lock() {
          
final Node node = this.node.get();
          
node.locked = true;
          
// 一个CAS操作即可将当前线程对应的节点加入到队列中,
          
// 并且同时获得了前继节点的引用,然后就是等待前继释放锁
          
Node pred = this.tail.getAndSet(node);
          
this.prev.set(pred);
          
while (pred.locked) {// 进入自旋
          
}
      
}

public void unlock() {
          
final Node node = this.node.get();
          
node.locked = false;// 改变状态,让后续线程结束自旋
          
this.node.set(this.prev.get());
      
}

private static class Node {
          
private volatile boolean locked;
      
}
  
}

//clh 2
  
import java.util.concurrent.atomic.AtomicReferenceFieldUpdater;

public class CLHLock {
      
public static class CLHNode {
          
private volatile boolean isLocked = true; // 默认是在等待锁
      
}

@SuppressWarnings("unused" )
      
private volatile CLHNode tail ;
      
private static final AtomicReferenceFieldUpdater<CLHLock, CLHNode> UPDATER = AtomicReferenceFieldUpdater
                    
.newUpdater(CLHLock.class, CLHNode .class , "tail" );

public void lock(CLHNode currentThread) {
          
CLHNode preNode = UPDATER.getAndSet( this, currentThread);
          
if(preNode != null) {//已有线程占用了锁,进入自旋
              
while(preNode.isLocked ) {
              
}
          
}
      
}

public void unlock(CLHNode currentThread) {
          
// 如果队列里只有当前线程,则释放对当前线程的引用 (for GC) 。
          
if (!UPDATER.compareAndSet(this, currentThread, null)) {
              
// 还有后续线程
              
currentThread.isLocked = false ;// 改变状态,让后续线程结束自旋
          
}
      
}
  
}
  
```

### NUMA与SMP
  
### SMP ( Symmetric Multi-Processor ) , 对称多处理器结构
对称多处理器结构,指服务器中多个CPU对称工作,每个CPU访问内存地址所需时间相同。其主要特征是共享,包含对CPU,内存,I/O等进行共享。SMP的优点是能够保证内存一致性,缺点是这些共享的资源很可能成为性能瓶颈,随着CPU数量的增加,每个CPU都要访问相同的内存资源,可能导致内存访问冲突,可能会导致CPU资源的浪费。常用的PC机就属于这种。
  
### NUMA ( Non-Uniform Memory Access )
非一致存储访问,将CPU分为CPU模块,每个CPU模块由多个CPU组成,并且具有独立的本地内存、I/O槽口等,模块之间可以通过互联模块相互访问,访问本地内存的速度将远远高于访问远地内存(系统内其它节点的内存)的速度,这也是非一致存储访问NUMA的由来。NUMA优点是可以较好地解决原来SMP系统的扩展问题,缺点是由于访问远地内存的延时远远超过本地内存,因此当CPU数量增加时,系统性能无法线性增加。

http://googi.iteye.com/blog/1736570
  
http://blog.csdn.net/aesop_wubo/article/details/7533186
  
http://zhanjindong.com/2015/03/11/java-concurrent-package-aqs-clh-and-spin-lock