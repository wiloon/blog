---
title: HashMap,Hashtable
author: "-"
date: 2012-09-21T05:24:11+00:00
url: hash/map-table
categories:
  - Java
tags:$
  - reprint
---
## HashMap,Hashtable
## HashMap, Hashtable

HashTable的应用非常广泛，HashMap是新框架中用来代替HashTable的类，也就是说建议使用HashMap，不要使用HashTable。可能你觉得HashTable很好用，为什么不用呢？这里简单分析他们的区别。

1. HashTable的方法是同步的，HashMap未经同步，所以在多线程场合要手动同步HashMap这个区别就像 Vector 和ArrayList一样。
2. HashTable不允许null值(key和value都不可以), HashMap允许 null 值(key和value都可以)。
3. hashMap去掉了HashTable 的contains(Object value)方法，但是加上了containsValue (）和containsKey (）方法。
4. HashTable使用 Enumeration，HashMap使用 Iterator。以上只是表面的不同，它们的实现也有很大的不同。
5. HashTable中 hash数组默认大小是11，增加的方式是 old*2+1。HashMap 中 hash数组的默认大小是16，而且一定是2的指数。
6. 哈希值的使用不同，HashTable 直接使用对象的hashCode，代码是这样的: 
  

```java
int hash = key.hashCode();
int index = (hash & 0x7FFFFFFF) % tab.length;
//而HashMap重新计算hash值，而且用与代替求模: 
int hash = hash(k);
int i = indexFor(hash, table.length);
  
  
    static int hash(Object x) {
 int h = x.hashCode();
  
  
  h += ~(h << 9);
 h ^= (h >>> 14);
 h += (h << 4);
 h ^= (h >>> 10);
 return h;
 }
 static int indexFor(int h, int length) {
 return h & (length-1);
 }
  
  
    ```
  
  
以上只是一些比较突出的区别，当然他们的实现上还是有很多不同的，比如 HashMap对null的操作
  


  
    HashMap可以看作三个视图: key的Set，value的Collection，Entry的Set。 这里HashSet就是其实就是HashMap的一个视图。HashSet内部就是使用Hashmap实现的，和Hashmap不同的是它不需要Key和Value两个值。
  
  
    往hashset中插入对象其实只不过是内部做了
  
  
    public boolean add(Object o) {
  
  
    return map.put(o, PRESENT)==null;
 }
 HashMap为散列映射,它是基于hash table的一个实现,它可在常量时间内安插元素,或找出一组key-value pair.HashSet为散列集,它把查找时间看的很重要,其中所有元素必须要有hashCode()
  
  
http://oznyang.iteye.com/blog/30690
http://zhaosoft.iteye.com/blog/243587  
  
http://coolshell.cn/articles/9606.html
  
http://coolshell.cn/articles/9606.html/embed#?secret=NbrQHz1OQo
  
