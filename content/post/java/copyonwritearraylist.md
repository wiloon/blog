---
title: CopyOnWriteArrayList
author: "-"
date: 2012-07-08T07:46:46+00:00
url: CopyOnWriteArrayList
categories:
  - Java
tags:
  - reprint
---
## CopyOnWriteArrayList
>http://www.cnblogs.com/sunwei2012/archive/2010/10/08/1845656.html

除了加锁外，还有一种方式可以防止并发修改异常，就是读写分离技术 (不是数据库上的) 。

先回顾一下一个常识: 
    
1. JAVA中"="操作只是将引用和某个对象关联，假如同时有一个线程将引用指向另外一个对象，一个线程获取这个引用指向的对象，那么他们之间不会发生ConcurrentModificationException，他们是在虚拟机层面阻塞的，而且速度非常快，几乎不需要CPU时间。
2. JAVA中两个不同的引用指向同一个对象，当第一个引用指向另外一个对象时，第二个引用还将保持原来的对象。
    
基于上面这个常识，我们再来探讨下面这个问题: 
    
在CopyOnWriteArrayList里处理写操作 (包括add、remove、set等) 是先将原始的数据通过JDK1.6的Arrays.copyof()来生成一份新的数组
    
然后在新的数据对象上进行写，写完后再将原来的引用指向到当前这个数据对象 (这里应用了常识1) ，这样保证了每次写都是在新的对象上 (因为要保证写的一致性，这里要对各种写操作要加一把锁，JDK1.6在这里用了重入锁) ，
    
然后读的时候就是在引用的当前对象上进行读 (包括get，iterator等) ，不存在加锁和阻塞，针对iterator使用了一个叫COWIterator的阉割版迭代器，因为不支持写操作，当获取CopyOnWriteArrayList的迭代器时，是将迭代器里的数据引用指向当前引用指向的数据对象，无论未来发生什么写操作，都不会再更改迭代器里的数据对象引用，所以迭代器也很安全 (这里应用了常识2) 。
    
CopyOnWriteArrayList中写操作需要大面积复制数组，所以性能肯定很差，但是读操作因为操作的对象和写操作不是同一个对象，读之间也不需要加锁，读和写之间的同步处理只是在写完后通过一个简单的"="将引用指向新的数组对象上来，这个几乎不需要时间，这样读操作就很快很安全，适合在多线程里使用，绝对不会发生ConcurrentModificationException，所以最后得出结论: CopyOnWriteArrayList适合使用在读操作远远大于写操作的场景里，比如缓存。
  
