---
title: Java Iterator 迭代器
author: wiloon
type: post
date: 2014-02-28T05:45:10+00:00
url: /?p=6298
categories:
  - Uncategorized
tags:
  - Java

---
<span style="font-family: Arial;">http://www.cnblogs.com/amboyna/archive/2007/09/25/904804.html</span>

http://jnotnull.iteye.com/blog/262379

<span style="font-family: Arial;">迭代器（Iterator）</span>

<span style="font-family: Arial;">　　迭代器是一种设计模式，它是一个对象，它可以遍历并选择序列中的对象，而开发人员不需要了解该序列的底层结构。迭代器通常被称为“轻量级”对象，因为创建它的代价小。</span>

<span style="font-family: Arial;">　　Java中的Iterator功能比较简单，并且只能单向移动：</span>

<span style="font-family: Arial;">　　(1) 使用方法iterator()要求容器返回一个Iterator。第一次调用Iterator的next()方法时，它返回序列的第一个元素。注意：iterator()方法是java.lang.Iterable接口,被Collection继承。</span>

<span style="font-family: Arial;">　　(2) 使用next()获得序列中的下一个元素。</span>

<span style="font-family: Arial;">　　(3) 使用hasNext()检查序列中是否还有元素。</span>

<span style="font-family: Arial;">　　(4) 使用remove()将迭代器新返回的元素删除。</span>

<span style="font-family: Arial;">　　Iterator是Java迭代器最简单的实现，为List设计的ListIterator具有更多的功能，它可以从两个方向遍历List，也可以从List中插入和删除元素。</span>

<span style="font-family: Arial;">迭代器应用：<br /> list l = new ArrayList();<br /> l.add("aa&#8221;);<br /> l.add("bb&#8221;);<br /> l.add("cc&#8221;);<br /> for (Iterator iter = l.iterator(); iter.hasNext();) {<br /> String str = (String)iter.next();<br /> System.out.println(str);<br /> }<br /> /*迭代器用于while循环<br /> Iterator iter = l.iterator();<br /> while(iter.hasNext()){<br /> String str = (String) iter.next();<br /> System.out.println(str);<br /> }<br /> */</span>