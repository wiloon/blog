---
title: java thread id, name
author: "-"
date: 2012-06-22T11:27:10+00:00
url: /?p=3615
categories:
  - Java
tags:
  - reprint
---
## java thread id, name
Thread.currendThread().getName()
  
这个可以返回线程对象的ID

设置线程名

```java

public class Thread3 {
  
public static void main(String[] args){
  
RunnableTest rt = new RunnableTest();
  
//定义两个线程，他们引用相同的数据
  
Thread t1 = new Thread(rt);
  
Thread t2 = new Thread(rt);
  
//设置线程的名字
  
t1.setName("线程1");
  
t2.setName("线程2");
  
//运行后，线程1 和线程2会交替运行
  
t1.start();
  
t2.start();
  
}
  
}

```