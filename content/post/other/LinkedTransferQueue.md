---
title: LinkedTransferQueue
author: "-"
date: 2015-09-14T06:17:39+00:00
url: LinkedTransferQueue
categories:
  - Java
tags:
  - reprint
  - Queue
---
## LinkedTransferQueue

LinkedTransferQueue是在JDK1.7时，J.U.C包新增的一种比较特殊的阻塞队列，它除了具备阻塞队列的常用功能外，还有一个比较特殊的transfer方法。

我们知道，在普通阻塞队列中，当队列为空时，消费者线程（调用take或poll方法的线程）一般会阻塞等待生产者线程往队列中存入元素。而LinkedTransferQueue的transfer方法则比较特殊：

当有消费者线程阻塞等待时，调用transfer方法的生产者线程不会将元素存入队列，而是直接将元素传递给消费者；
如果调用transfer方法的生产者线程发现没有正在等待的消费者线程，则会将元素入队，然后会阻塞等待，直到有一个消费者线程来获取该元素。

有一篇论文讨论了其算法与性能: 地址: <http://www.cs.rice.edu/~wns1/papers/2006-PPoPP-SQ.pdf>

LinkedTransferQueue 实现了一个重要的接口 TransferQueue, 该接口含有下面几个重要方法:
  
1. transfer(E e)
若当前存在一个正在等待获取的消费者线程，即立刻移交之；否则，会插入当前元素e到队列尾部，并且等待进入阻塞状态，到有消费者线程取走该元素。

2. tryTransfer(E e)  
若当前存在一个正在等待获取的消费者线程 (使用take()或者poll()函数) ，使用该方法会即刻转移/传输对象元素e；  
若不存在，则返回false，并且不进入队列。这是一个不阻塞的操作。  

3. tryTransfer(E e, long timeout, TimeUnit unit)  
若当前存在一个正在等待获取的消费者线程，会立即传输给它; 否则将插入元素e到队列尾部，并且等待被消费者线程获取消费掉,  
若在指定的时间内元素e无法被消费者线程获取，则返回false，同时该元素被移除。  

4. hasWaitingConsumer()
判断是否存在消费者线程

5. getWaitingConsumerCount()
  
获取所有等待获取元素的消费线程数量

其实transfer方法在SynchronousQueue的实现中就已存在了,只是没有做为API暴露出来。SynchronousQueue有一个特性:它本身不存在容量,只能进行线程之间的
  
元素传送。SynchronousQueue在执行offer操作时，如果没有其他线程执行poll，则直接返回false.线程之间元素传送正是通过transfer方法完成的。

有一个使用案例，我们知道ThreadPoolExecutor调节线程的原则是: 先调整到最小线程，最小线程用完后，他会将优先将任务放入缓存队列(offer(task)),等缓冲队列用完了，才会向最大线程数调节。这似乎与我们所理解的线程池模型有点不同。我们一般采用增加到最大线程后，才会放入缓冲队列中，以达到最大性能。ThreadPoolExecutor代码片段:

public void execute(Runnable command) {
  
if (command == null)
  
throw new NullPointerException();
  
if (poolSize >= corePoolSize || !addIfUnderCorePoolSize(command)) {
  
if (runState == RUNNING && workQueue.offer(command)) {
  
if (runState != RUNNING || poolSize == 0)
  
ensureQueuedTaskHandled(command);
  
}
  
else if (!addIfUnderMaximumPoolSize(command))
  
reject(command); // is shutdown or saturated
  
}
  
}
  
如果我们采用SynchronousQueue作为ThreadPoolExecuto的缓冲队列时，在没有线程执行poll时(即存在等待线程)，则workQueue.offer(command)返回false,这时ThreadPoolExecutor就会增加线程，最快地达到最大线程数。但也仅此而已，也因为SynchronousQueue本身不存在容量,也决定了我们一般无法采用SynchronousQueue作为ThreadPoolExecutor的缓存队列。而一般采用LinkedBlockingQueue的offer方法来实现。最新的LinkedTransferQueue也许可以帮我们解决这个问题，后面再说。

transfer算法比较复杂，实现很难看明白。大致的理解是采用所谓双重数据结构(dual data structures)。之所以叫双重，其原因是方法都是通过两个步骤完成:
  
保留与完成。比如消费者线程从一个队列中取元素，发现队列为空，他就生成一个空元素放入队列,所谓空元素就是数据项字段为空。然后消费者线程在这个字段上旅转等待。这叫保留。直到一个生产者线程意欲向队例中放入一个元素，这里他发现最前面的元素的数据项字段为NULL，他就直接把自已数据填充到这个元素中，即完成了元素的传送。大体是这个意思，这种方式优美了完成了线程之间的高效协作。

对于LinkedTransferQueue,Doug Lea进行了尽乎极致的优化。Grizzly的采用了PaddedAtomicReference:
  
public LinkedTransferQueue() {
  
QNode dummy = new QNode(null, false);
  
head = new PaddedAtomicReference<QNode>(dummy);
  
tail = new PaddedAtomicReference<QNode>(dummy);
  
cleanMe = new PaddedAtomicReference<QNode>(null);
  
}
  
static final class PaddedAtomicReference<T> extends AtomicReference<T> {        // enough padding for 64bytes with 4byte refs
  
Object p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, pa, pb, pc, pd, pe;
  
PaddedAtomicReference(T r) { super(r); }
  
}
  
PaddedAtomicReference相对于父类AtomicReference只做了一件事情，就将共享变量追加到64字节。我们可以来计算下，一个对象的引用占4个字节，
  
它追加了15个变量共占60个字节，再加上父类的Value变量，一共64个字节。这么做的原因。请参考<http://www.infoq.com/cn/articles/ftf-java-volatile>
  
<http://rdc.taobao.com/team/jm/archives/1719> 这两文章。做JAVA，如果想成为Doug Lea这样的大师，也要懂体系结构(待续)

    Java 7中的TransferQueue
  
<http://guojuanjun.blog.51cto.com/277646/948298>

<https://segmentfault.com/a/1190000016460411>
