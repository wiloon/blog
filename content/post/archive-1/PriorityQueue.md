---
title: PriorityQueue
author: "-"
date: 2015-06-27T13:00:28+00:00
url: /?p=7904
categories:
  - Uncategorized
tags:
  - Java

---
## PriorityQueue

<http://java-er.com/blog/java-priority-queue/>

PriorityQueue 是个基于优先级堆的极大优先级队列。

此队列按照在构造时所指定的顺序对元素排序，既可以根据元素的自然顺序来指定排序 (参阅 Comparable) ，
  
也可以根据 Comparator 来指定，这取决于使用哪种构造方法。优先级队列不允许 null 元素。
  
依靠自然排序的优先级队列还不允许插入不可比较的对象 (这样做可能导致 ClassCastException)

比如队列 1 3 5 10 2 自动会被排列 1 2 3 5 10

package com.javaer.examples.datastruct;

import java.util.Comparator;
  
import java.util.PriorityQueue;
  
import java.util.Queue;

import org.apache.poi.ss.formula.functions.Count;

public class PriorityQueueExample {

/**
  
* @param args
  
*/
  
public static void main(String[] args) {
  
// TODO Auto-generated method stub
  
Queue<Integer> qi = new PriorityQueue<Integer>();

qi.add(5);
  
qi.add(2);
  
qi.add(1);
  
qi.add(10);
  
qi.add(3);

while (!qi.isEmpty()){
  
System.out.print(qi.poll() + ",");
  
}
  
System.out.println();
  
System.out.println("----------");

Comparator<Integer> cmp;
  
cmp = new Comparator<Integer>() {
  
public int compare(Integer e1, Integer e2) {
  
return e2 - e1;
  
}
  
};
  
Queue<Integer> q2 = new PriorityQueue<Integer>(5,cmp);
  
q2.add(2);
  
q2.add(8);
  
q2.add(9);
  
q2.add(1);
  
while (!q2.isEmpty()){
  
System.out.print(q2.poll() + ",");
  
}

}

}

output

1,2,3,5,10,
  
----------
  
9,8,2,1,
  
自定义的比较器，可以让我们自由定义比较的顺序

Comparator cmp;
  
cmp = new Comparator() {
  
public int compare(Integer e1, Integer e2) {
  
return e2 - e1;
  
}
  
};

此队列的头是按指定排序方式的最小元素。如果多个元素都是最小值，则头是其中一个元素——选择方法是任意的。
  
队列检索操作 poll、remove、peek 和 element 访问处于队列头的元素。
  
优先级队列是无界的，但是有一个内部容量，控制着用于存储队列元素的数组的大小。
  
它总是至少与队列的大小相同。随着不断向优先级队列添加元素，其容量会自动增加。无需指定容量增加策略的细节。

注意1: 该队列是用数组实现，但是数组大小可以动态增加，容量无限。

注意2:此实现不是同步的。不是线程安全的。如果多个线程中的任意线程从结构上修改了列表， 则这些线程不应同时访问 PriorityQueue 实例，这时请使用线程安全的PriorityBlockingQueue 类。

注意3:不允许使用 null 元素。

注意4: 此实现为插入方法 (offer、poll、remove() 和 add 方法) 提供 O(log(n)) 时间；

为 remove(Object) 和 contains(Object) 方法提供线性时间；
  
为检索方法 (peek、element 和 size) 提供固定时间。

注意5:方法iterator()中提供的迭代器并不保证以有序的方式遍历优先级队列中的元素。

至于原因可参考下面关于PriorityQueue的内部实现
  
如果需要按顺序遍历，请考虑使用 Arrays.sort(pq.toArray())。

注意6: 可以在构造函数中指定如何排序。如:

PriorityQueue()
  
使用默认的初始容量 (11) 创建一个 PriorityQueue，并根据其自然顺序来排序其元素 (使用 Comparable) 。
  
PriorityQueue(int initialCapacity)
  
使用指定的初始容量创建一个 PriorityQueue，并根据其自然顺序来排序其元素 (使用 Comparable) 。
  
PriorityQueue(int initialCapacity, Comparator comparator)
  
使用指定的初始容量创建一个 PriorityQueue，并根据指定的比较器comparator来排序其元素。

注意7:此类及其迭代器实现了 Collection 和 Iterator 接口的所有可选 方法。

PriorityQueue的内部实现
  
PriorityQueue对元素采用的是堆排序，头是按指定排序方式的最小元素。堆排序只能保证根是最大 (最小) ，整个堆并不是有序的。
  
方法iterator()中提供的迭代器可能只是对整个数组的依次遍历。也就只能保证数组的第一个元素是最小的。
  
实例1的结果也正好与此相符

<http://blog.csdn.net/hiphopmattshi/article/details/7334487>
