---
title: 阻塞队列 BlockingQueue
author: "-"
date: 2013-12-20T04:52:28+00:00
url: /?p=6043
categories:
  - Uncategorized
tags:
  - Java

---
## 阻塞队列 BlockingQueue
什么是阻塞队列
  
阻塞队列 (BlockingQueue) 是一个支持两个附加操作的队列。这两个附加的操作是: 在队列为空时，获取元素的线程会等待队列变为非空。当队列满时，存储元素的线程会等待队列可用。阻塞队列常用于生产者和消费者的场景，生产者是往队列里添加元素的线程，消费者是从队列里拿元素的线程。阻塞队列就是生产者存放元素的容器，而消费者也只从容器里拿元素。

方法\处理方式 抛出异常 返回特殊值 一直阻塞 超时退出
  
插入方法 add(e) offer(e) put(e) offer(e,time,unit)
  
移除方法 remove() poll() take() poll(time,unit)
  
检查方法 element() peek() 不可用 不可用

抛出异常: 是指当阻塞队列满时候，再往队列里插入元素，会抛出IllegalStateException("Queue full")异常。当队列为空时，从队列里获取元素时会抛出NoSuchElementException异常 。
  
返回特殊值: 插入方法会返回是否成功，成功则返回true。移除方法，则是从队列里拿出一个元素，如果没有则返回null
  
一直阻塞: 当阻塞队列满时，如果生产者线程往队列里put元素，队列会一直阻塞生产者线程，直到拿到数据，或者响应中断退出。当队列空时，消费者线程试图从队列里take元素，队列也会阻塞消费者线程，直到队列可用。
  
超时退出: 当阻塞队列满时，队列会阻塞生产者线程一段时间，如果超过一定的时间，生产者线程就会退出。

Java里的阻塞队列
  
JDK7提供了7个阻塞队列。分别是

ArrayBlockingQueue : 一个由数组结构组成的有界阻塞队列。
  
LinkedBlockingQueue : 一个由链表结构组成的有界阻塞队列。
  
PriorityBlockingQueue : 一个支持优先级排序的无界阻塞队列。
  
DelayQueue: 一个使用优先级队列实现的无界阻塞队列。
  
SynchronousQueue: 一个不存储元素的阻塞队列。
  
LinkedTransferQueue: 一个由链表结构组成的无界阻塞队列。
  
LinkedBlockingDeque: 一个由链表结构组成的双向阻塞队列。

在JDK1.5新增的Concurrent包中，BlockingQueue很好的解决了多线程中，如何高效安全"传输"数据的问题。通过这些高效并且线程安全的队列类，为我们快速搭建高质量的多线程程序带来极大的便利。

认识BlockingQueue
  
阻塞队列，顾名思义，首先它是一个队列,通过一个共享的队列，可以使得数据由队列的一端输入，从另外一端输出；
  
常用的队列主要有以下两种:  (当然通过不同的实现方式，还可以延伸出很多不同类型的队列，DelayQueue就是其中的一种) 
  
先进先出 (FIFO) : 先插入的队列的元素也最先出队列，类似于排队的功能。从某种程度上来说这种队列也体现了一种公平性。
  
后进先出 (LIFO) : 后插入队列的元素最先出队列，这种队列优先处理最近发生的事件。

多线程环境中，通过队列可以很容易实现数据共享，比如经典的"生产者"和"消费者"模型中，通过队列可以很便利地实现两者之间的数据共享。假设我们有若干生产者线程，另外又有若干个消费者线程。如果生产者线程需要把准备好的数据共享给消费者线程，利用队列的方式来传递数据，就可以很方便地解决他们之间的数据共享问题。但如果生产者和消费者在某个时间段内，万一发生数据处理速度不匹配的情况呢？理想情况下，如果生产者产出数据的速度大于消费者消费的速度，并且当生产出来的数据累积到一定程度的时候，那么生产者必须暂停等待一下 (阻塞生产者线程) ，以便等待消费者线程把累积的数据处理完毕，反之亦然。然而，在concurrent包发布以前，在多线程环境下，我们每个程序员都必须去自己控制这些细节，尤其还要兼顾效率和线程安全，而这会给我们的程序带来不小的复杂度。好在此时，强大的concurrent包横空出世了，而他也给我们带来了强大的BlockingQueue。 (在多线程领域: 所谓阻塞，在某些情况下会挂起线程 (即阻塞) ，一旦条件满足，被挂起的线程又会自动被唤醒) 
  
下面两幅图演示了BlockingQueue的两个常见阻塞场景: 
  
当队列中没有数据的情况下，消费者端的所有线程都会被自动阻塞 (挂起) ，直到有数据放入队列。
  
当队列中填满数据的情况下，生产者端的所有线程都会被自动阻塞 (挂起) ，直到队列中有空的位置，线程被自动唤醒。
       
这也是我们在多线程环境下，为什么需要BlockingQueue的原因。作为BlockingQueue的使用者，我们再也不需要关心什么时候需要阻塞线程，什么时候需要唤醒线程，因为这一切BlockingQueue都给你一手包办了。既然BlockingQueue如此神通广大。

BlockingQueue的核心方法: 
  
**放入数据: **
  
]offer(anObject):
  
表示如果可能的话,将anObject加到BlockingQueue里,即如果BlockingQueue可以容纳,
  
则返回true,否则返回false. (本方法不阻塞当前执行方法的线程) 

offer(E o, long timeout, TimeUnit unit),
  
可以设定等待的时间，如果在指定的时间内，还不能往队列中加入BlockingQueue，则返回失败。

put(anObject):
  
把anObject加到BlockingQueue里,如果BlockQueue没有空间,则调用此方法的线程被阻断,直到BlockingQueue里面有空间再继续.

add 增加一个元索 如果队列已满，则抛出一个IIIegaISlabEepeplian异常

**获取数据: **
  
poll(time):
  
移除并返回BlockingQueue里排在首位的对象,若不能立即取出,则可以等time参数规定的时间,取不到时返回null;
  
pool()
  
如果取不到，不等待，直接返回null

poll(long timeout, TimeUnit unit): 
  
移除并返回BlockingQueue里队首的对象，如果在指定时间内，队列一旦有数据可取，则立即返回队列中的数据。否则知道时间超时还没有数据可取，返回null。

peek(): 返回队列头部的元素(不移除),如果队列为空，则返回null

take():
  
取走BlockingQueue里排在首位的对象,若BlockingQueue为空,阻断进入等待状态直到BlockingQueue有新的数据被加入;

drainTo():
  
一次性从BlockingQueue获取所有可用的数据对象 (还可以指定获取数据的个数) ，通过该方法，可以提升获取数据效率；不需要多次分批加锁或释放锁。

remove()
  
移除并返回队列头部的元素 如果队列为空，则抛出一个NoSuchElementException异常

Queue接口与List、Set同一级别，都是继承了Collection接口。LinkedList实现了Queue接口。Queue接口窄化了对LinkedList的方法的访问权限 (即在方法中的参数类型如果是Queue时，就完全只能访问Queue接口所定义的方法了，而不能直接访问LinkedList的非Queue的方法) ，以使得只有恰当的方法才可以使用。BlockingQueue 继承了Queue接口。

add, remove、element、offer 、poll、peek 其实是属于Queue接口。

阻塞队列的操作可以根据它们的响应方式分为以下三类: add、removee和element操作在你试图为一个已满的队列增加元素或从空队列取得元素时抛出异常。当然，在多线程程序中，队列在任何时间都可能变成满的或空的，所以你可能想使用offer、poll、peek方法。这些方法在无法完成任务时只是给出一个出错示而不会抛出异常。

注意: poll和peek方法出错进返回null。因此，向队列中插入null值是不合法的。

还有带超时的offer和poll方法变种，例如，下面的调用: 

boolean success = q.offer(x,100,TimeUnit.MILLISECONDS);

尝试在100毫秒内向队列尾部插入一个元素。如果成功，立即返回true；否则，当到达超时进，返回false。同样地，调用: 

Object head = q.poll(100, TimeUnit.MILLISECONDS);

如果在100毫秒内成功地移除了队列头元素，则立即返回头元素；否则在到达超时时，返回null。

最后，我们有阻塞操作put和take。put方法在队列满时阻塞，take方法在队列空时阻塞。

java.ulil.concurrent包提供了阻塞队列的4个变种。默认情况下，

[LinkedBlockingDeque][1]
  
[LinkedTransferQueue][2]
  
[SynchronousQueue][3]

LinkedBlockingQueue的容量是没有上限的 (说的不准确，在不指定时容量为Integer.MAX_VALUE，不要然的话在put时怎么会受阻呢) ，但是也可以选择指定其最大容量，它是基于链表的队列，此队列按 FIFO (先进先出) 排序元素。
  
ArrayBlockingQueue在构造时需要指定容量，并可以选择是否需要公平性，如果公平参数被设置true，等待时间最长的线程会优先得到处理 (其实就是通过将ReentrantLock设置为true来达到这种公平性的: 即等待时间最长的线程会先操作) 。通常，公平性会使你在性能上付出代价，只有在的确非常需要的时候再使用它。它是基于数组的阻塞循环队列，此队列按 FIFO (先进先出) 原则对元素进行排序。

PriorityBlockingQueue是一个带优先级的队列，而不是先进先出队列。元素按优先级顺序被移除，该队列也没有上限 (看了一下源码，PriorityBlockingQueue是对PriorityQueue的再次包装，是基于堆数据结构的，而PriorityQueue是没有容量限制的，与ArrayList一样，所以在优先阻塞队列上put时是不会受阻的。虽然此队列逻辑上是无界的，但是由于资源被耗尽，所以试图执行添加操作可能会导致 OutOfMemoryError) ，但是如果队列为空，那么取元素的操作take就会阻塞，所以它的检索操作take是受阻的。另外，往入该队列中的元素要具有比较能力。

下面的实例展示了如何使用阻塞队列来控制线程集。程序在一个目录及它的所有子目录下搜索所有文件，打印出包含指定关键字的文件列表。从下面实例可以看出，使用阻塞队列两个显著的好处就是: 多线程操作共同的队列时不需要额外的同步，另外就是队列会自动平衡负载，即那边 (生产与消费两边) 处理快了就会被阻塞掉，从而减少两边的处理速度差距。下面是具体实现: 

Java代码 收藏代码

public class BlockingQueueTest {

public static void main(String[] args) {

Scanner in = new Scanner(System.in);

System.out.print("Enter base directory (e.g. /usr/local/jdk5.0/src): ");

String directory = in.nextLine();

System.out.print("Enter keyword (e.g. volatile): ");

String keyword = in.nextLine();

final int FILE_QUEUE_SIZE = 10;// 阻塞队列大小

final int SEARCH_THREADS = 100;// 关键字搜索线程个数

// 基于ArrayBlockingQueue的阻塞队列

BlockingQueue<File> queue = new ArrayBlockingQueue<File>(

FILE_QUEUE_SIZE);

//只启动一个线程来搜索目录

FileEnumerationTask enumerator = new FileEnumerationTask(queue,

new File(directory));

new Thread(enumerator).start();

//启动100个线程用来在文件中搜索指定的关键字

for (int i = 1; i <= SEARCH_THREADS; i++)

new Thread(new SearchTask(queue, keyword)).start();

}

}

class FileEnumerationTask implements Runnable {

//哑元文件对象，放在阻塞队列最后，用来标示文件已被遍历完

public static File DUMMY = new File("");

private BlockingQueue<File> queue;

private File startingDirectory;

public FileEnumerationTask(BlockingQueue<File> queue, File startingDirectory) {

this.queue = queue;

this.startingDirectory = startingDirectory;

}

public void run() {

try {

enumerate(startingDirectory);

queue.put(DUMMY);//执行到这里说明指定的目录下文件已被遍历完

} catch (InterruptedException e) {

}

}

// 将指定目录下的所有文件以File对象的形式放入阻塞队列中

public void enumerate(File directory) throws InterruptedException {

File[] files = directory.listFiles();

for (File file : files) {

if (file.isDirectory())

enumerate(file);

else

//将元素放入队尾，如果队列满，则阻塞

queue.put(file);

}

}

}

class SearchTask implements Runnable {

private BlockingQueue<File> queue;

private String keyword;

public SearchTask(BlockingQueue<File> queue, String keyword) {

this.queue = queue;

this.keyword = keyword;

}

public void run() {

try {

boolean done = false;

while (!done) {

//取出队首元素，如果队列为空，则阻塞

File file = queue.take();

if (file == FileEnumerationTask.DUMMY) {

//取出来后重新放入，好让其他线程读到它时也很快的结束

queue.put(file);

done = true;

} else

search(file);

}

} catch (IOException e) {

e.printStackTrace();

} catch (InterruptedException e) {

}

}

public void search(File file) throws IOException {

Scanner in = new Scanner(new FileInputStream(file));

int lineNumber = 0;

while (in.hasNextLine()) {

lineNumber++;

String line = in.nextLine();

if (line.contains(keyword))

System.out.printf("%s:%d:%s%n", file.getPath(), lineNumber,

line);

}

in.close();

}

}

http://jiangzhengjun.iteye.com/blog/683593
  
http://www.cnblogs.com/jackyuj/archive/2010/11/24/1886553.html
  
http://www.infoq.com/cn/articles/java-blocking-queue

 [1]: http://www.wiloon.com/?p=8256
 [2]: http://www.wiloon.com/?p=8253
 [3]: http://www.wiloon.com/?p=8250