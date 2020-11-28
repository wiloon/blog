---
title: HashSet、TreeSet、LinkedHashSet
author: w1100n
type: post
date: 2014-06-17T01:05:44+00:00
url: /?p=6726
categories:
  - Uncategorized
tags:
  - Java

---
在一个set中，是没有重复元素的。这也是使用set最主要的原因之一。Set的实现类有三个：HashSet，TreeSet，LinkedHashSet。什么时候使用哪一种实现类，是一个非常的问题。简单地说，如果我们想要一个快速的set，那么我们应该使用HashSet；如果我们需要一个已经排好序的set，那么TreeSet应该被使用；如果我们想一个可以根据插入顺序来读取的set，那么LinkedHashSet应该被使用。

1.Set接口
  
Set接口继承了Collection接口。在set中，不允许有重复的元素。每一个元素在set中都是唯一的。我们可以简单地添加元素至一个set中，最后，我们会得到一个自动删除重复元素的set。

2.HashSet vs. TreeSet vs. LinkedHashSet
  
HashSet 是使用一个哈希表实现的。元素是无序的。add、remove 及contains 方法的时间复杂度是一个常量 O(1)。

TreeSet 是使用一个树结构（算法书籍上的红黑树）来实现的。元素在set中被排好序，但是add、remove及contains方法的时间复杂度为O(log(n))。它提供了几个方法用来处理有序的set，比如first()，last()，headSet()，tailSet()等等。

LinkedHashSet介于HashSet与TreeSet之间。它由一个执行hash表的链表实现，因此，它提供顺序插入。基本方法的时间复杂度为O(1)。

HashMap和HashSet的区别是Java面试中最常被问到的问题。如果没有涉及到Collection框架以及多线程的面试，可以说是不完整。而Collection框架的问题不涉及到HashSet和HashMap，也可以说是不完整。HashMap和HashSet都是collection框架的一部分，它们让我们能够使用对象的集合。collection框架有自己的接口和实现，主要分为Set接口，List接口和Queue接口。它们有各自的特点，Set的集合里不允许对象有重复的值，List允许有重复，它对集合中的对象进行索引，Queue的工作原理是FCFS算法(First Come, First Serve)。

首先让我们来看看什么是HashMap和HashSet，然后再来比较它们之间的分别。

### <a class="external" href="https://github.com/stephanietang/ImportNew/blob/master/Java/Difference%20between%20HashMap%20and%20HashSet%20in%20Java.md#%E4%BB%80%E4%B9%88%E6%98%AFhashset" target="_blank" rel="nofollow" name="%E4%BB%80%E4%B9%88%E6%98%AFhashset"></a>什么是HashSet

HashSet实现了Set接口，它不允许集合中有重复的值，当我们提到HashSet时，第一件事情就是在将对象存储在HashSet之前，要先确保对象重写equals()和hashCode()方法，这样才能比较对象的值是否相等，以确保set中没有储存相等的对象。如果我们没有重写这两个方法，将会使用这个方法的默认实现。

public boolean add(Object o)方法用来在Set中添加元素，当元素值重复时则会立即返回false，如果成功添加的话会返回true。

### <a href="https://github.com/stephanietang/ImportNew/blob/master/Java/Difference%20between%20HashMap%20and%20HashSet%20in%20Java.md#%E4%BB%80%E4%B9%88%E6%98%AFhashmap" name="%E4%BB%80%E4%B9%88%E6%98%AFhashmap"></a>什么是HashMap

HashMap实现了Map接口，Map接口对键值对进行映射。Map中不允许重复的键。Map接口有两个基本的实现，HashMap和TreeMap。TreeMap保存了对象的排列次序，而HashMap则不能。HashMap允许键和值为null。HashMap是非synchronized的，但collection框架提供方法能保证HashMap synchronized，这样多个线程同时访问HashMap时，能保证只有一个线程更改Map。

public Object put(Object Key,Object value)方法用来将元素添加到map中。

你可以阅读<a href="http://www.importnew.com/7099.html" target="_blank">这篇文章</a>看看HashMap的工作原理，以及<a href="http://www.importnew.com/7010.html" target="_blank">这篇文章</a>看看HashMap和HashTable的区别。

### <a class="external" href="https://github.com/stephanietang/ImportNew/blob/master/Java/Difference%20between%20HashMap%20and%20HashSet%20in%20Java.md#hashset%E5%92%8Chashmap%E7%9A%84%E5%8C%BA%E5%88%AB" target="_blank" rel="nofollow" name="hashset%E5%92%8Chashmap%E7%9A%84%E5%8C%BA%E5%88%AB"></a>HashSet和HashMap的区别

<table>
  <tr>
    <td>
      *HashMap*
    </td>
    
    <td>
      *HashSet*
    </td>
  </tr>
  
  <tr>
    <td>
      HashMap实现了Map接口
    </td>
    
    <td>
      HashSet实现了Set接口
    </td>
  </tr>
  
  <tr>
    <td>
      HashMap储存键值对
    </td>
    
    <td>
      HashSet仅仅存储对象
    </td>
  </tr>
  
  <tr>
    <td>
      使用put()方法将元素放入map中
    </td>
    
    <td>
      使用add()方法将元素放入set中
    </td>
  </tr>
  
  <tr>
    <td>
      HashMap中使用键对象来计算hashcode值
    </td>
    
    <td>
      HashSet使用成员对象来计算hashcode值，对于两个对象来说hashcode可能相同，所以equals()方法用来判断对象的相等性，如果两个对象不同的话，那么返回false
    </td>
  </tr>
  
  <tr>
    <td>
      HashMap比较快，因为是使用唯一的键来获取对象
    </td>
    
    <td>
      HashSet较HashMap来说比较慢 
      
      
        
      
      
      
        </td> </tr> </tbody> </table> 
        
        
          http://blog.csdn.net/cynthia9023/article/details/17503023
        
        
        
          http://www.importnew.com/6931.html
        