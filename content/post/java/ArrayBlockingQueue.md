---
title: ArrayBlockingQueue
author: "-"
date: 2012-08-26T12:22:11+00:00
url: ArrayBlockingQueue
categories:
  - Java
tags:
  - reprint
  - Queue
---
## ArrayBlockingQueue
  
ArrayBlockingQueue 是一个基于数组的阻塞队列实现，此队列按 FIFO (先进先出) 原则对元素进行排序, 在 ArrayBlockingQueue 内部，维护了一个定长数组，以便缓存队列中的数据对象，这是一个常用的阻塞队列，除了一个定长数组外，ArrayBlockingQueue内部还保存着两个整形变量，分别标识着队列的头部和尾部在数组中的位置。
  
ArrayBlockingQueue 在生产者放入数据和消费者获取数据，都是共用同一个锁对象，由此也意味着两者无法真正并行运行，这点尤其不同于 LinkedBlockingQueue, 按照实现原理来分析 ArrayBlockingQueue 完全可以采用分离锁，从而实现生产者和消费者操作的完全并行运行。Doug Lea 之所以没这样去做，也许是因为 ArrayBlockingQueue 的数据写入和获取操作已经足够轻巧，以至于引入独立的锁机制，除了给代码带来额外的复杂性外，其在性能上完全占不到任何便宜。 ArrayBlockingQueue 和 LinkedBlockingQueue 间还有一个明显的不同之处在于，前者在插入或删除元素时不会产生或销毁任何额外的对象实例，而后者则会生成一个额外的 Node 对象。这在长时间内需要高效并发地处理大批量数据的系统中，其对于 GC 的影响还是存在一定的区别。而在创建 ArrayBlockingQueue 时，我们还可以控制对象的内部锁是否采用公平锁，默认采用非公平锁。

队列的头部是在队列中存在时间最长的元素。队列的尾部是在队列中存在时间最短的元素。新元素插入到队列的尾部，队列检索操作则是从队列头部开始获得元素。

这是一个典型的 "有界缓存区"，固定大小的数组在其中保持生产者插入的元素和使用者提取的元素。一旦创建了这样的缓存区，就不能再增加其容量。试图向已满队列中放入元素会导致放入操作受阻塞；试图从空队列中检索元素将导致类似阻塞。

此类支持对等待的生产者线程和使用者线程进行排序的可选公平策略。默认情况下，不保证是这种排序。然而，通过将公平性 (fairness) 设置为 true 而构造的队列允许按照 FIFO 顺序访问线程。公平性通常会降低吞吐量，但也减少了可变性和避免了"不平衡性"。

ArrayBlockingQueue 在构造时需要指定容量，并可以选择是否需要公平性，如果公平参数被设置true，等待时间最长的线程会优先得到处理 (其实就是通过将 ReentrantLock 设置为 true 来达到这种公平性的: 即等待时间最长的线程会先操作) 。通常，公平性会使你在性能上付出代价，只有在的确非常需要的时候再使用它。它是基于数组的阻塞循环队列，此队列按 FIFO (先进先出) 原则对元素进行排序。

## PriorityBlockingQueue

PriorityBlockingQueue 是一个带优先级的队列，而不是先进先出队列。元素按优先级顺序被移除，该队列也没有上限 (看了一下源码，PriorityBlockingQueue 是对 PriorityQueue 的再次包装，是基于堆数据结构的，而 PriorityQueue 是没有容量限制的，与ArrayList一样，所以在优先阻塞队列上put时是不会受阻的。虽然此队列逻辑上是无界的，但是由于资源被耗尽，所以试图执行添加操作可能会导致 OutOfMemoryError) ，但是如果队列为空，那么取元素的操作take就会阻塞，所以它的检索操作take是受阻的。另外，往入该队列中的元素要具有比较能力。
  
最后，DelayQueue (基于PriorityQueue来实现的) 是一个存放Delayed 元素的无界阻塞队列，只有在延迟期满时才能从中提取元素。该队列的头部是延迟期满后保存时间最长的 Delayed 元素。如果延迟都还没有期满，则队列没有头部，并且poll将返回null。当一个元素的 getDelay(TimeUnit.NANOSECONDS) 方法返回一个小于或等于零的值时，则出现期满，poll就以移除这个元素了。此队列不允许使用 null 元素。 下面是延迟接口:

```java
public interface Delayed extends Comparable<Delayed> {
    long getDelay(TimeUnit unit);
}
```
  
放入 DelayQueue 的元素还将要实现 compareTo 方法，DelayQueue 使用这个来为元素排序。

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

## ArrayBlockingQueue VS LinkedBlockingQueue

ArrayBlockingQueue
ArrayBlockingQueue是接口BlockingQueue的阻塞实现队列之一。基于数组实现的一个阻塞队列，在创建对象时必须**指定容量大小**。并且可以**指定公平性与非公平性**，默认情况下为非公平的，即不保证等待时间最长的队列最优先能够访问队列。它能够实现插入和取出的阻塞方法put()和take()方法其实也是通过使用通知模式来实现。查看源码就可以知道ArrayBlockingQueue生产者方放入数据、消费者取出数据都是使用**同一把重入锁**，这就两者无法真正的实现生产者和消费者的并行。
LinkedBlockingQueue
LinkedBlockingQueue也是接口BlockingQueue的阻塞实现队列之一。基于链表实现的一个阻塞队列，在创建对象时如果不指定容量大小，则**默认大小为Integer.MAX_VALUE**，所以要注意一个问题，如果初始化时没有指定容量，生产者放入元素远大于消费者取出元素的速度时，那么生产的元素一直在链表中存在，这会对内存造成很大压力。由于是基于链表的，所以生产者每次放入元素会构造一个新节点对象，在大量并发的情况下可能会对系统**GC**造成一定影响，而ArrayBlockingQueue不存在这种情况。LinkedBlockingQueue同样是使用通知模式来实现。相对于ArrayBlockingQueue，LinkedBlockingQueue生产者和消费者分别使用**两把重入锁**来实现同步，所以可以提高系统的并发度。
————————————————
版权声明：本文为CSDN博主「乐乐Java路漫漫」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/b1303110335/article/details/105769565>
