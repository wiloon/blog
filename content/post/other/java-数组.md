---
title: 数组
author: "-"
date: 2012-01-02T09:17:29+00:00
url: /?p=1469
categories:
  - Java
  - Uncategorized

tags:
  - reprint
---
## 数组
线性表 (Linear List) 
  
每个线性表上的数据最多只有前和后两个方向。其实除了数组，链表...
  
数组支持随机访问，根据下标随机访问的时间复杂度为 O(1)

数组简单易用，在实现上使用的是连续的内存空间，可以借助 CPU 的缓存机制，预读数组中的数据，所以访问效率更高。而链表在内存中并不是连续存储，所以对 CPU 缓存不友好，没办法有效预读。

一维数组的声明方式: 
  
type var[]; 或type[] var;

声明数组时不能指定其长度 (数组中元素的个数) ，

Java中使用关键字new创建数组对象，格式为: 
  
数组名 = new 数组元素的类型 [数组元素的个数]

实例: 
  
TestNew.java: 

程序代码: 

```java
public class TestNew
{
public static void main(String args[]) {
int[] s ;
int i ;
s = new int[5] ;
for(i = 0 ; i < 5 ; i++) {
s[i] = i ;
}
for(i = 4 ; i >= 0 ; i–) {
System.out.println("" + s[i]) ;
}
}
}

```

初始化: 

1.动态初始化: 数组定义与为数组分配空间和赋值的操作分开进行；
  
2.静态初始化: 在定义数字的同时就为数组元素分配空间并赋值；
  
3.默认初始化: 数组是引用类型，它的元素相当于类的成员变量，因此数组分配空间后，每个元素也被按照成员变量的规则被隐士初始化。
  
实例: 

TestD.java(动态): 

程序代码: 

```java

public class TestD
  
{
  
public static void main(String args[]) {
  
int a[] ;
  
a = new int[3] ;
  
a[0] = 0 ;
  
a[1] = 1 ;
  
a[2] = 2 ;
  
Date days[] ;
  
days = new Date[3] ;
  
days[0] = new Date(2008,4,5) ;
  
days[1] = new Date(2008,2,31) ;
  
days[2] = new Date(2008,4,4) ;
  
}
  
}

class Date
  
{
  
int year,month,day ;
  
Date(int year ,int month ,int day) {
  
this.year = year ;
  
this.month = month ;
  
this.day = day ;
  
}
  
}

```

TestS.java(静态): 

程序代码: 

```java

public class TestS
  
{
  
public static void main(String args[]) {
  
int a[] = {0,1,2} ;
  
Time times [] = {new Time(19,42,42),new Time(1,23,54),new Time(5,3,2)} ;
  
}
  
}

class Time
  
{
  
int hour,min,sec ;
  
Time(int hour ,int min ,int sec) {
  
this.hour = hour ;
  
this.min = min ;
  
this.sec = sec ;
  
}
  
}

```

TestDefault.java(默认): 

程序代码: 

```java

public class TestDefault
  
{
  
public static void main(String args[]) {
  
int a [] = new int [5] ;
  
System.out.println("" + a[3]) ;
  
}
  
}

```

http://developer.51cto.com/art/200906/128274.htm