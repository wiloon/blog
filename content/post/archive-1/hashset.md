---
title: HashSet、TreeSet、LinkedHashSet
author: "-"
date: 2014-06-17T01:05:44+00:00
url: hashset
categories:
  - java
tags:
  - collection

---
## HashSet、TreeSet、LinkedHashSet
## HashSet, TreeSet, LinkedHashSet
在一个set中，是没有重复元素的。这也是使用set最主要的原因之一。Set的实现类有三个: HashSet，TreeSet，LinkedHashSet。什么时候使用哪一种实现类?。简单地说，如果我们想要一个快速的set，那么我们应该使用HashSet；如果我们需要一个已经排好序的set，那么TreeSet应该被使用；如果我们想一个可以根据插入顺序来读取的set，那么LinkedHashSet应该被使用。

### Set接口
  
Set接口继承了Collection接口。在set中，不允许有重复的元素。每一个元素在set中都是唯一的。我们可以简单地添加元素至一个set中，最后，我们会得到一个自动删除重复元素的set。

### HashSet vs. TreeSet vs. LinkedHashSet
  
HashSet 是使用一个哈希表实现的。元素是无序的。add、remove 及contains 方法的时间复杂度是一个常量 O(1)。

TreeSet 是使用红黑树 来实现的。元素在set中被排好序，但是add、remove及contains方法的时间复杂度为O(log(n))。它提供了几个方法用来处理有序的set，比如first()，last()，headSet()，tailSet()等等。

### LinkedHashSet
LinkedHashSet介于HashSet与TreeSet之间。它由一个执行hash表的链表实现，因此，它提供顺序插入。基本方法的时间复杂度为O(1)。

HashMap和HashSet的区别是Java面试中最常被问到的问题。如果没有涉及到Collection框架以及多线程的面试，可以说是不完整。而Collection框架的问题不涉及到HashSet和HashMap，也可以说是不完整。HashMap和HashSet都是collection框架的一部分，它们让我们能够使用对象的集合。collection框架有自己的接口和实现，主要分为Set接口，List接口和Queue接口。它们有各自的特点，Set的集合里不允许对象有重复的值，List允许有重复，它对集合中的对象进行索引，Queue的工作原理是FCFS算法(First Come, First Serve)。

首先让我们来看看什么是HashMap和HashSet，然后再来比较它们之间的分别。

### 什么是HashSet

HashSet实现了Set接口，它不允许集合中有重复的值，当我们提到HashSet时，第一件事情就是在将对象存储在HashSet之前，要先确保对象重写equals()和hashCode()方法，这样才能比较对象的值是否相等，以确保set中没有储存相等的对象。如果我们没有重写这两个方法，将会使用这个方法的默认实现。

public boolean add(Object o)方法用来在Set中添加元素，当元素值重复时则会立即返回false，如果成功添加的话会返回true。

### 什么是HashMap

HashMap实现了Map接口，Map接口对键值对进行映射。Map中不允许重复的键。Map接口有两个基本的实现，HashMap和TreeMap。TreeMap保存了对象的排列次序，而HashMap则不能。HashMap允许键和值为null。HashMap是非synchronized的，但collection框架提供方法能保证HashMap synchronized，这样多个线程同时访问HashMap时，能保证只有一个线程更改Map。

public Object put(Object Key,Object value)方法用来将元素添加到map中。

### HashSet和HashMap的区别

对于HashSet而言，它的底层是基于HashMap实现的。HashSet底层使用HashMap来保存所有元素。
HashSet的实现其实非常简单，它只是封装了一个HashMap对象来存储所有的集合元素。所有放入HashSet中的集合元素实际上由HashMap的key来保存，而HashMap的value则存储了一个PRESENT，它是一个静态的Object对象。
HashSet的绝大部分方法都是通过调用HashMap的方法来实现的，因此HashSet和HashMap两个集合在实现本质上是相同的。

注意：由于HashSet的add()方法添加集合元素实际上转变为调用HashMap的put()方法来添加key-value对，当新放入HashMap的Entry中key与集合中原有Entry的key相同 (hashCode()返回值相等，通过equals比较也返回true）时，新添加的Entry的value将覆盖原来Entry的value，但key不会有任何改变。因此，如果向HashSet中添加一个已经存在的元素，新添加的集合元素 (底层由HashMap的key保存）不会覆盖已有的集合元素。
————————————————
版权声明：本文为CSDN博主「bear_wr」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/bear_wr/article/details/52275874