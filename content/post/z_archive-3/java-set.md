---
title: Java Set
author: "-"
date: 2019-08-19T02:40:38+00:00
url: /?p=14808
categories:
  - Inbox
tags:
  - reprint
---
## Java Set

版权声明: 本文为博主原创文章，遵循 CC 4.0 by-sa 版权协议，转载请附上原文出处链接和本声明。
  
本文链接: [https://blog.csdn.net/qq_33642117/article/details/52040345](https://blog.csdn.net/qq_33642117/article/details/52040345)
  
一，Set
  
Set:注重独一无二的性质,该体系集合可以知道某物是否已近存在于集合中,不会存储重复的元素
  
用于存储无序(存入和取出的顺序不一定相同)元素，值不能重复。

对象的相等性

   引用到堆上同一个对象的两个引用是相等的。如果对两个引用调用hashCode方法，会得到相同的结果，如果对象所属的类没有覆盖Object的hashCode方法的话，hashCode会返回每个对象特有的序号 (java是依据对象的内存地址计算出的此序号) ，所以两个不同的对象的hashCode值是不可能相等的。

如果想要让两个不同的Person对象视为相等的，就必须覆盖Object继下来的hashCode方法和equals方法，因为Object  hashCode方法返回的是该对象的内存地址，所以必须重写hashCode方法，才能保证两个不同的对象具有相同的hashCode，同时也需要两个不同对象比较equals方法会返回true

该集合中没有特有的方法，直接继承自Collection。

-| Itreable 接口 实现该接口可以使用增强for循环

-| Collection 描述所有集合共性的接口

-| List接口 可以有重复元素的集合

-| ArrayList

-| LinkedList

-| Set接口 不可以有重复元素的集合

案例: set集合添加元素并使用迭代器迭代元素。

public class Demo4 {

public static void main(String[] args) {

//Set 集合存和取的顺序不一致。

Set hs = new HashSet();

hs.add("世界军事");

hs.add("兵器知识");

hs.add("舰船知识");

hs.add("汉和防务");

System.out.println(hs);

// [舰船知识, 世界军事, 兵器知识, 汉和防务]

Iterator it = hs.iterator();

while (it.hasNext()) {

System.out.println(it.next());

}

}
  
}

————————————————
  
版权声明: 本文为CSDN博主「飘走的我」的原创文章，遵循CC 4.0 by-sa版权协议，转载请附上原文出处链接及本声明。
  
原文链接: [https://blog.csdn.net/qq_33642117/article/details/52040345](https://blog.csdn.net/qq_33642117/article/details/52040345)
