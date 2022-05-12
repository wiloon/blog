---
title: ConcurrentHashMap/CopyOnWriteArrayList
author: "-"
date: 2012-07-08T07:44:04+00:00
url: /?p=3800
categories:
  - Java
tags:$
  - reprint
---
## ConcurrentHashMap/CopyOnWriteArrayList
## ConcurrentHashMap, CopyOnWriteArrayList

并发集合类 ConcurrentHashMap 和 CopyOnWriteArrayList(转)
 
    在Java类库中出现的第一个关联的集合类是 Hashtable ，它是JDK 1.0的一部分。 Hashtable 提供了一种易于使用的、线程安全的、关联的map功能，这当然也是方便的。然而，线程安全性是凭代价换来的―― Hashtable 的所有方法都是同步的。此时，无竞争的同步会导致可观的性能代价。 Hashtable 的后继者 HashMap 是作为JDK1.2中的集合框架的一部分出现的，它通过提供一个不同步的基类和一个同步的包装器 Collections.synchronizedMap ，解决了线程安全性问题。通过将基本的功能从线程安全性中分离开来， Collections.synchronizedMap 允许需要同步的用户可以拥有同步，而不需要同步的用户则不必为同步付出代价。

    Hashtable 和 synchronizedMap 所采取的获得同步的简单方法 (同步 Hashtable 中或者同步的 Map 包装器对象中的每个方法) 有两个主要的不足。首先，这种方法对于可伸缩性是一种障碍，因为一次只能有一个线程可以访问hash表。同时，这样仍不足以提供真正的线程安全性，许多公用的混合操作仍然需要额外的同步。虽然诸如 get() 和 put() 之类的简单操作可以在不需要额外同步的情况下安全地完成，但还是有一些公用的操作序列，例如迭代或者put-if-absent (空则放入) ，需要外部的同步，以避免数据争用。
  
有条件的线程安全性
  
    同步的集合包装器 synchronizedMap 和 synchronizedList ，有时也被称作 有条件地线程安全――所有单个的操作都是线程安全的，但是多个操作组成的操作序列却可能导致数据争用，因为在操作序列中控制流取决于前面操作的结果。 清单1中第一片段展示了公用的put-if-absent语句块――如果一个条目不在 Map 中，那么添加这个条目。不幸的是，在 containsKey() 方法返回到 put() 方法被调用这段时间内，可能会有另一个线程也插入一个带有相同键的值。如果您想确保只有一次插入，您需要用一个对 Map m 进行同步的同步块将这一对语句包装起来。
  
  
http://www-128.ibm.com/developerworks/cn/java/j-jtp07233/index.html#listing1

中其他的例子与迭代有关。在第一个例子中， List.size() 的结果在循环的执行期间可能会变得无效，因为另一个线程可以从这个列表中删除条目。如果时机不得当，在刚好进入循环的最后一次迭代之后有一个条目被另一个线程删除了，则 List.get() 将返回 null ，而 doSomething() 则很可能会抛出一个 NullPointerException 异常。那么，采取什么措施才能避免这种情况呢？如果当您正在迭代一个 List 时另一个线程也可能正在访问这个 List ，那么在进行迭代时您必须使用一个 synchronized 块将这个 List 包装起来，在 List 1 上同步，从而锁住整个 List 。这样做虽然解决了数据争用问题，但是在并发性方面付出了更多的代价，因为在迭代期间锁住整个 List 会阻塞其他线程，使它们在很长一段时间内不能访问这个列表。
  
集合框架引入了迭代器，用于遍历一个列表或者其他集合，从而优化了对一个集合中的元素进行迭代的过程。然而，在 java.util 集合类中实现的迭代器极易崩溃，也就是说，如果在一个线程正在通过一个 Iterator 遍历集合时，另一个线程也来修改这个集合，那么接下来的 Iterator.hasNext() 或 Iterator.next() 调用将抛出 ConcurrentModificationException 异常。就拿刚才这个例子来讲，如果想要防止出现 ConcurrentModificationException 异常，那么当您正在进行迭代时，您必须使用一个在 List l 上同步的 synchronized 块将该 List 包装起来，从而锁住整个 List 。 (或者，您也可以调用 List.toArray() ，在不同步的情况下对数组进行迭代，但是如果列表比较大的话这样做代价很高) 。
清单 1. 同步的map中的公用竞争条件
 

Map m = Collections.synchronizedMap(new HashMap());

List l = Collections.synchronizedList(new ArrayList());
// put-if-absent idiom -- contains a race condition

// may require external synchronization

if (!map.containsKey(key))

map.put(key, value);
// ad-hoc iteration -- contains race conditions

// may require external synchronization

for (int i=0; i<list.size(); i++) {

doSomething(list.get(i));

}
// normal iteration -- can throw ConcurrentModificationException

// may require external synchronization

for (Iterator i=list.iterator(); i.hasNext(); ) {

doSomething(i.next());

}


 信任的错觉
  
  
    synchronizedList 和 synchronizedMap 提供的有条件的线程安全性也带来了一个隐患 ―― 开发者会假设，因为这些集合都是同步的，所以它们都是线程安全的，这样一来他们对于正确地同步混合操作这件事就会疏忽。其结果是尽管表面上这些程序在负载较轻的时候能够正常工作，但是一旦负载较重，它们就会开始抛出 NullPointerException 或 ConcurrentModificationException 。
 可伸缩性问题
  
  
    可伸缩性指的是一个应用程序在工作负载和可用处理资源增加时其吞吐量的表现情况。一个可伸缩的程序能够通过使用更多的处理器、内存或者I/O带宽来相应地处理更大的工作负载。锁住某个共享的资源以获得独占式的访问这种做法会形成可伸缩性瓶颈――它使其他线程不能访问那个资源，即使有空闲的处理器可以调用那些线程也无济于事。为了取得可伸缩性，我们必须消除或者减少我们对独占式资源锁的依赖。
  
  
    同步的集合包装器以及早期的 Hashtable 和 Vector 类带来的更大的问题是，它们在单个的锁上进行同步。这意味着一次只有一个线程可以访问集合，如果有一个线程正在读一个 Map ，那么所有其他想要读或者写这个 Map 的线程就必须等待。最常见的 Map 操作， get() 和 put() ，可能比表面上要进行更多的处理――当遍历一个hash表的bucket以期找到某一特定的key时， get() 必须对大量的候选bucket调用 Object.equals() 。如果key类所使用的 hashCode() 函数不能将value均匀地分布在整个hash表范围内，或者存在大量的hash冲突，那么某些bucket链就会比其他的链长很多，而遍历一个长的hash链以及对该hash链上一定百分比的元素调用 equals() 是一件很慢的事情。在上述条件下，调用 get() 和 put() 的代价高的问题不仅仅是指访问过程的缓慢，而且，当有线程正在遍历那个hash链时，所有其他线程都被锁在外面，不能访问这个 Map 。
  
  
     (哈希表根据一个叫做hash的数字关键字 (key) 将对象存储在bucket中。hash value是从对象中的值计算得来的一个数字。每个不同的hash value都会创建一个新的bucket。要查找一个对象，您只需要计算这个对象的hash value并搜索相应的bucket就行了。通过快速地找到相应的bucket，就可以减少您需要搜索的对象数量了。译者注) 
  
  
    get() 执行起来可能会占用大量的时间，而在某些情况下，前面已经作了讨论的有条件的线程安全性问题会让这个问题变得还要糟糕得多。 清单1 中演示的争用条件常常使得对单个集合的锁在单个操作执行完毕之后还必须继续保持一段较长的时间。如果您要在整个迭代期间都保持对集合的锁，那么其他的线程就会在锁外停留很长的一段时间，等待解锁。
  
  
    实例: 一个简单的cache
  
  
    Map 在服务器应用中最常见的应用之一就是实现一个 cache。 服务器应用可能需要缓存文件内容、生成的页面、数据库查询的结果、与经过解析的XML文件相关的DOM树，以及许多其他类型的数据。cache的主要用途是重用前一次处理得出的结果以减少服务时间和增加吞吐量。cache工作负载的一个典型的特征就是检索大大多于更新，因此 (理想情况下) cache能够提供非常好的 get() 性能。不过，使用会妨碍性能的cache还不如完全不用cache。
  
  
    如果使用 synchronizedMap 来实现一个cache，那么您就在您的应用程序中引入了一个潜在的可伸缩性瓶颈。因为一次只有一个线程可以访问 Map ，这些线程包括那些要从 Map 中取出一个值的线程以及那些要将一个新的 (key, value) 对插入到该map中的线程。
  
  
    减小锁粒度
  
  
    提高 HashMap 的并发性同时还提供线程安全性的一种方法是废除对整个表使用一个锁的方式，而采用对hash表的每个bucket都使用一个锁的方式 (或者，更常见的是，使用一个锁池，每个锁负责保护几个bucket) 。这意味着多个线程可以同时地访问一个 Map 的不同部分，而不必争用单个的集合范围的锁。这种方法能够直接提高插入、检索以及移除操作的可伸缩性。不幸的是，这种并发性是以一定的代价换来的――这使得对整个集合进行操作的一些方法 (例如 size() 或 isEmpty() ) 的实现更加困难，因为这些方法要求一次获得许多的锁，并且还存在返回不正确的结果的风险。然而，对于某些情况，例如实现cache，这样做是一个很好的折衷――因为检索和插入操作比较频繁，而 size() 和 isEmpty() 操作则少得多。
  
  
### ConcurrentHashMap
util.concurrent 包中的 ConcurrentHashMap 类 (也将出现在JDK 1.5中的 java.util.concurrent 包中) 是对 Map 的线程安全的实现，比起 synchronizedMap 来，它提供了好得多的并发性。多个读操作几乎总可以并发地执行，同时进行的读和写操作通常也能并发地执行，而同时进行的写操作仍然可以不时地并发进行 (相关的类也提供了类似的多个读线程的并发性，但是，只允许有一个活动的写线程)  。ConcurrentHashMap 被设计用来优化检索操作；实际上，成功的 get() 操作完成之后通常根本不会有锁着的资源。要在不使用锁的情况下取得线程安全性需要一定的技巧性，并且需要对Java内存模型 (Java Memory Model) 的细节有深入的理解。 ConcurrentHashMap 实现，加上 util.concurrent 包的其他部分，已经被研究正确性和线程安全性的并发专家所正视。
  
  
ConcurrentHashMap 通过稍微地松弛它对调用者的承诺而获得了更高的并发性。检索操作将可以返回由最近完成的插入操作所插入的值，也可以返回在步调上是并发的插入操作所添加的值 (但是决不会返回一个没有意义的结果) 。由 ConcurrentHashMap.iterator() 返回的 Iterators 将每次最多返回一个元素，并且决不会抛出 ConcurrentModificationException 异常，但是可能会也可能不会反映在该迭代器被构建之后发生的插入操作或者移除操作。在对集合进行迭代时，不需要表范围的锁就能提供线程安全性。在任何不依赖于锁整个表来防止更新的应用程序中，可以使用 ConcurrentHashMap来替代 synchronizedMap 或 Hashtable 。
  
  
上述改进使得 ConcurrentHashMap 能够提供比 Hashtable 高得多的可伸缩性，而且，对于很多类型的公用案例 (比如共享的cache) 来说，还不用损失其效率。
  
  
好了多少？
  
  
    表 1对 Hashtable 和 ConcurrentHashMap 的可伸缩性进行了粗略的比较。在每次运行过程中， n 个线程并发地执行一个死循环，在这个死循环中这些线程从一个 Hashtable 或者 ConcurrentHashMap 中检索随机的key value，发现在执行 put() 操作时有80%的检索失败率，在执行操作时有1%的检索成功率。测试所在的平台是一个双处理器的Xeon系统，操作系统是Linux。数据显示了10,000,000次迭代以毫秒计的运行时间，这个数据是在将对 ConcurrentHashMap的 操作标准化为一个线程的情况下进行统计的。您可以看到，当线程增加到多个时， ConcurrentHashMap 的性能仍然保持上升趋势，而 Hashtable 的性能则随着争用锁的情况的出现而立即降了下来。
  
  
    比起通常情况下的服务器应用，这次测试中线程的数量看上去有点少。然而，因为每个线程都在不停地对表进行操作，所以这与实际环境下使用这个表的更多数量的线程的争用情况基本等同。
  
  
表 1.Hashtable 与 ConcurrentHashMap在可伸缩性方面的比较
线程数 ConcurrentHashMap Hashtable 1 1.00 1.03 2 2.59 32.40 4 5.58 78.23 8 13.21 163.48 16 27.58 341.21 32 57.27 778.41

### CopyOnWriteArrayList
在那些遍历操作大大地多于插入或移除操作的并发应用程序中，一般用 CopyOnWriteArrayList 类替代 ArrayList 。如果是用于存放一个侦听器 (listener) 列表，例如在AWT或Swing应用程序中，或者在常见的JavaBean中，那么这种情况很常见 (相关的 CopyOnWriteArraySet 使用一个 CopyOnWriteArrayList 来实现 Set 接口) 。
  
如果您正在使用一个普通的 ArrayList 来存放一个侦听器列表，那么只要该列表是可变的，而且可能要被多个线程访问，您就必须要么在对其进行迭代操作期间，要么在迭代前进行的克隆操作期间，锁定整个列表，这两种做法的开销都很大。当对列表执行会引起列表发生变化的操作时， CopyOnWriteArrayList 并不是为列表创建一个全新的副本，它的迭代器肯定能够返回在迭代器被创建时列表的状态，而不会抛出 ConcurrentModificationException 。在对列表进行迭代之前不必克隆列表或者在迭代期间锁定列表，因为迭代器所看到的列表的副本是不变的。换句话说， CopyOnWriteArrayList 含有对一个不可变数组的一个可变的引用，因此，只要保留好那个引用，您就可以获得不可变的线程安全性的好处，而且不用锁定列表。
  
结束语
    同步的集合类 Hashtable 和 Vector ，以及同步的包装器类 Collections.synchronizedMap 和 Collections.synchronizedList ，为 Map 和 List 提供了基本的有条件的线程安全的实现。然而，某些因素使得它们并不适用于具有高度并发性的应用程序中――它们的集合范围的单锁特性对于可伸缩性来说是一个障碍，而且，很多时候还必须在一段较长的时间内锁定一个集合，以防止出现 ConcurrentModificationException s异常。 ConcurrentHashMap 和 CopyOnWriteArrayList 实现提供了更高的并发性，同时还保住了线程安全性，只不过在对其调用者的承诺上打了点折扣。 ConcurrentHashMap 和 CopyOnWriteArrayList 并不是在您使用 HashMap 或 ArrayList 的任何地方都一定有用，但是它们是设计用来优化某些特定的公用解决方案的。许多并发应用程序将从对它们的使用中获得好处。
  
