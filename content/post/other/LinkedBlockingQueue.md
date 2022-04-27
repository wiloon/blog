---
title: LinkedBlockingQueue
author: "-"
date: 2015-09-14T06:55:36+00:00
url: LinkedBlockingQueue
categories:
  - Java
tags:
  - reprint
  - Queue
---
## LinkedBlockingQueue

基于链表的阻塞队列，同 ArrayBlockingQueue 类似，其内部也维持着一个数据缓冲队列 (该队列是一个链表) ，生产者存入的数据会缓存在队列内部，生产者立即返回；只有当队列缓冲区达到最大值缓存容量时 (LinkedBlockingQueue可以通过构造函数指定该值) ，才会阻塞生产者队列，直到消费者从队列中消费掉一份数据，生产者线程会被唤醒，反之对于消费者这端的处理也基于同样的原理。而LinkedBlockingQueue 之所以能够高效的处理并发数据，还因为其对于生产者端和消费者端 **分别采用了独立的锁** 来控制数据同步，这也意味着在高并发的情况下生产者和消费者可以并行地操作队列中的数据，以此来提高整个队列的并发性能。
  
作为开发者，我们需要注意的是，如果构造一个 LinkedBlockingQueue 对象，而没有指定其容量大小，LinkedBlockingQueue 会默认一个类似无限大小的容量 (Integer.MAX_VALUE) ，这样的话，如果生产者的速度一旦大于消费者的速度，也许还没有等到队列满阻塞产生，系统内存就有可能已被消耗殆尽了。

此队列按 FIFO (先进先出) 排序元素。队列的头部 是在队列中时间最长的元素。队列的尾部 是在队列中时间最短的元素。
  
新元素插入到队列的尾部，并且队列检索操作会获得位于队列头部的元素。链接队列的吞吐量通常要高于基于数组的队列，
  
但是在大多数并发应用程序中，其可预知的性能要低。
  
可选的容量范围构造方法参数作为防止队列过度扩展的一种方法。

1:如果未指定容量，默认容量为 Integer.MAX_VALUE ，容量范围可以在构造方法参数中指定作为防止队列过度扩展。
  
2:此对象是 线程阻塞-安全的
  
3: 不接受 null 元素
  
4:它实现了BlockingQueue接口。
  
5:实现了 Collection 和 Iterator 接口的所有可选方法。
  
6: 在JDK5/6中，LinkedBlockingQueue和ArrayBlocingQueue等对象的poll(long timeout, TimeUnit unit)存在内存泄露Leak的对象AbstractQueuedSynchronizer.Node，据称JDK5会在Update12里Fix，JDK6会在Update2里Fix
  
下面介绍几种常用的方法:

定义一个输出方法:

static void v(Object s){System.out.println(s.toString());}
  
LinkedBlockingQueue<String> bq=new LinkedBlockingQueue<String>();

for(int i=0;i<100;i++)
  
{
  
bq.add("i"+i);//如果空间已满，此方法会抛出异常，所以这就是put，或者offer方法的优势所在
  
}

String s1=bq.take();//i0
  
String s2=bq.take();//i1

bq.offer("ix",5,TimeUnit.SECONDS);//在尾部插入一个元素，如果有必要 ，等待 指定的时间，使得队列变得可用。返回boolean值 表示是否插入成功。

bq.put("ixx");//将指定的元素添加到队列的尾部，如有必要，则等待空间变得可用，如果空间满了，则会一直等到空间可用时，进行插入。

bq.poll();//poll() //poll(long timeout, TimeUnit unit) 检索并移除此队列的头，如果此队列为空，则返回 null。

bq.clear() 从队列彻底移除所有元素。

bq.peek()检索，但是不移除此队列的头，如果此队列为空，则返回 null。

//区别一下几种方法:

1.offer(E e) offer(E e,long timeout,TimeUnit unit)

和

put(E e)

都是想队列中插入元素，如果使用offer，则当队列可用或者等待指定时间后队列可用时，才能将元素插入成功。

如果使用put(E e)，则会一直等待队列可用时插入元素。因为此队列是线程阻塞的，所以会存在被其他线程锁住，不可使用的时期段

此队列的容量 要么为指定的固定容量，不指定，容量则为Integer.MAX_VALUE.

2.poll() poll(long timeout,TimeUnit unit)和peek();

poll方法是 立刻或者等待指定时间后，获取并且移除队列的头。如果队列为空，则为null

peek方法是 获取但不移除此队列的头，如果此队列为空，则为null

LinkedBlockingQueue的put,add和offer的区别
  
最近在学习<<Java并发编程实践>>，有很多java.util.concurrent包下的新类。LinkedBlockingQueue就是其中之一，顾名思义这是一个阻塞的线程安全的队列，底层应该采用链表实现。

看其API的时候发现，添加元素的方法竟然有三个: add,put,offer。

且这三个元素都是向队列尾部添加元素的意思。于是我产生了兴趣，要仔细探究一下他们之间的差别。

1.首先看一下add方法:

Inserts the specified element into this queue if it is possible to do so immediately without violating capacity restrictions, returning true upon success and throwing an IllegalStateException if no space is currently available.

This implementation returns true if offer succeeds, else throws an IllegalStateException.

LinkedBlockingQueue构造的时候若没有指定大小，则默认大小为Integer.MAX_VALUE，当然也可以在构造函数的参数中指定大小。LinkedBlockingQueue不接受null。

add方法在添加元素的时候，若超出了度列的长度会直接抛出异常:

public static void main(String args[]){
  
try {
  
LinkedBlockingQueue<String> queue=new LinkedBlockingQueue(2);

queue.add("hello");
  
queue.add("world");
  
queue.add("yes");
  
} catch (Exception e) {
  
// TODO: handle exception
  
e.printStackTrace();
  
}
  
}
  
//运行结果:
  
java.lang.IllegalStateException: Queue full
  
at java.util.AbstractQueue.add(Unknown Source)
  
at com.wjy.test.GrandPather.main(GrandPather.java:12)
  
2.再来看一下put方法:

Inserts the specified element at the tail of this queue, waiting if necessary for space to become available.

对于put方法，若向队尾添加元素的时候发现队列已经满了会发生阻塞一直等待空间，以加入元素。

public static void main(String args[]){
  
try {
  
LinkedBlockingQueue<String> queue=new LinkedBlockingQueue(2);

queue.put("hello");
  
queue.put("world");
  
queue.put("yes");

System.out.println("yes");
  
} catch (Exception e) {
  
// TODO: handle exception
  
e.printStackTrace();
  
}
  
}
  
//运行结果:
  
//在queue.put("yes")处发生阻塞
  
//下面的"yes"无法输出

3.最后看一下offer方法:

Inserts the specified element at the tail of this queue if it is possible to do so immediately without exceeding the queue's capacity, returning true upon success and false if this queue is full. When using a capacity-restricted queue, this method is generally preferable to method add, which can fail to insert an element only by throwing an exception.

offer方法在添加元素时，如果发现队列已满无法添加的话，会直接返回false。

public static void main(String args[]){
  
try {
  
LinkedBlockingQueue<String> queue=new LinkedBlockingQueue(2);

boolean bol1=queue.offer("hello");
  
boolean bol2=queue.offer("world");
  
boolean bol3=queue.offer("yes");

System.out.println(queue.toString());
  
System.out.println(bol1);
  
System.out.println(bol2);
  
System.out.println(bol3);
  
} catch (Exception e) {
  
// TODO: handle exception
  
e.printStackTrace();
  
}
  
}
  
//运行结果:
  
[hello, world]
  
true
  
true
  
false
  
好了，竟然说了这么多了，就把从队列中取元素的方法也顺便一说。

从队列中取出并移除头元素的方法有: poll，remove，take。
  
poll: 若队列为空，返回null。

remove:若队列为空，抛出NoSuchElementException异常。

take:若队列为空，发生阻塞，等待有元素。

<http://www.myexception.cn/database/1697409.html>
  
<http://www.cnblogs.com/Gordon-YangYiBao/archive/2012/08/07/2626410.html>

## LinkedBlockingDeque

<http://www.cnblogs.com/linjiqin/p/3214725.html>
  
对于阻塞栈，与阻塞队列相似。不同点在于栈是"后入先出"的结构，每次操作的是栈顶，而队列是"先进先出"的结构，每次操作的是队列头。

这里要特别说明一点的是，阻塞栈是Java6的新特征。

Java为阻塞栈定义了接口: java.util.concurrent.BlockingDeque，其实现类也比较多，具体可以查看JavaAPI文档。

下面看一个简单例子:
  
package cn.thread;

import java.util.concurrent.BlockingDeque;
  
import java.util.concurrent.LinkedBlockingDeque;

/**
  
* 阻塞栈
  
*
  
* @author 林计钦
  
* @version 1.0 2013-7-25 下午05:05:49
  
*/
  
public class LinkedBlockingDequeTest {
  
public static void main(String[] args) throws InterruptedException {
  
BlockingDeque bDeque = new LinkedBlockingDeque(20);
  
for (int i = 0; i < 30; i++) {
  
// 将指定元素添加到此阻塞栈中，如果没有可用空间，将一直等待 (如果有必要) 。
  
bDeque.putFirst(i);
  
System.out.println("向阻塞栈中添加了元素:" + i);
  
}
  
System.out.println("程序到此运行结束，即将退出--");
  
}
  
}

向阻塞栈中添加了元素:0
  
向阻塞栈中添加了元素:1
  
向阻塞栈中添加了元素:2
  
向阻塞栈中添加了元素:3
  
向阻塞栈中添加了元素:4
  
向阻塞栈中添加了元素:5
  
向阻塞栈中添加了元素:6
  
向阻塞栈中添加了元素:7
  
向阻塞栈中添加了元素:8
  
向阻塞栈中添加了元素:9
  
向阻塞栈中添加了元素:10
  
向阻塞栈中添加了元素:11
  
向阻塞栈中添加了元素:12
  
向阻塞栈中添加了元素:13
  
向阻塞栈中添加了元素:14
  
向阻塞栈中添加了元素:15
  
向阻塞栈中添加了元素:16
  
向阻塞栈中添加了元素:17
  
向阻塞栈中添加了元素:18
  
向阻塞栈中添加了元素:19

从上面结果可以看到，程序并没结束，二是阻塞住了，原因是栈已经满了，后面追加元素的操作都被阻塞了。
