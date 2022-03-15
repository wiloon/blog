---
title: java 数组 list set, 数组转set
author: "-"
date: 2011-09-08T06:42:29+00:00
url: /?p=715
categories:
  - Java
tags:
  - Java

---
## java 数组 list set, 数组转set
http://jerval.iteye.com/blog/1001643

//数组->Set
  
String[] strs = {"AA","BB"};
  
Set<String> set2 = new HashSet<String>(Arrays.asList(strs));
  
System.out.println(set2);
  
//Set->数组
  
Set<String> set3 = new HashSet<String>(Arrays.asList("PP","OO"));
  
String[] strSet = new String[set3.size()];
  
set3.toArray(strSet);
  
System.out.println(Arrays.toString(strSet));

List(interface): 次序是List最重要的特点；它确保维护元素特定的顺序。List为Collection添加了许多方法，使得能够向List中间插入与移除元素(只推荐LinkedList使用)。一个List可以生成ListIterator，使用它可以从两个方向遍历List，也可以从List中间插入和删除元素。

ArrayList: 由数组实现的List。它允许对元素进行快速随机访问，但是向List中间插入与移除元素的速度很慢。ListIterator只应该用来由后向前遍历ArrayList，而不是用来插入和删除元素，因为这比LinkedList开销要大很多。

LinkedList: 对顺序访问进行了优化，向List中间插入与删除得开销不大，随机访问则相对较慢(可用ArrayList代替)。它具有方法addFirst()、addLast()、getFirst()、getLast()、removeFirst()、removeLast()，这些方法(没有在任何接口或基类中定义过)使得LinkedList可以当作堆栈、队列和双向队列使用。

####################################

Set(interface): 存入Set的每个元素必须是唯一的，因为Set不保存重复元素。加入Set的Object必须定义equals()方法以确保对象的唯一性。Set与Collection有完全一样的接口。Set接口不保证维护元素的次序。

HashSet: 为快速查找而设计的Set。存入HashSet的对象必须定义hashCode()。采用散列函数对元素进行排序，这是专门为快速查询而设计的；

TreeSet: 保持次序的Set，底层为树结构。使用它可以从Set中提取有序的序列。TreeSet采用红黑树的数据结构进行排序元素；

LinkedHashSet: 具有HashSet的查询速度，且内部使用链表维护元素的顺序(插入的次序)。于是在使用迭代器遍历Set时，结果会按元素插入的次序显示。LinkedHashSet内部使用散列以加快查询速度，同时使用链表维护元素的次序，使得看起来元素是以插入的顺序保存的。

需要注意的是，生成自己的类时，Set需要维护元素的存储顺序，因此要实现Comparable接口并定义compareTo()方法。