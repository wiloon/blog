---
title: LinkedBlockingDeque
author: "-"
date: 2015-09-14T06:21:51+00:00
url: /?p=8256
categories:
  - Uncategorized

tags:
  - reprint
---
## LinkedBlockingDeque
http://www.cnblogs.com/linjiqin/p/3214725.html

Java多线程-新特征-阻塞栈LinkedBlockingDeque
  
对于阻塞栈，与阻塞队列相似。不同点在于栈是"后入先出"的结构，每次操作的是栈顶，而队列是"先进先出"的结构，每次操作的是队列头。

这里要特别说明一点的是，阻塞栈是Java6的新特征。、

Java为阻塞栈定义了接口: java.util.concurrent.BlockingDeque，其实现类也比较多，具体可以查看JavaAPI文档。

下面看一个简单例子: 
  
package cn.thread;

import java.util.concurrent.BlockingDeque;
  
import java.util.concurrent.LinkedBlockingDeque;

/**
  
* 阻塞栈
  
*
  
* @author 林计钦
  
* @version 1.0 2013-7-25 下午05:05:49
  
*/
  
public class LinkedBlockingDequeTest {
  
public static void main(String[] args) throws InterruptedException {
  
BlockingDeque bDeque = new LinkedBlockingDeque(20);
  
for (int i = 0; i < 30; i++) {
  
// 将指定元素添加到此阻塞栈中，如果没有可用空间，将一直等待 (如果有必要) 。
  
bDeque.putFirst(i);
  
System.out.println("向阻塞栈中添加了元素:" + i);
  
}
  
System.out.println("程序到此运行结束，即将退出--");
  
}
  
}

向阻塞栈中添加了元素:0
  
向阻塞栈中添加了元素:1
  
向阻塞栈中添加了元素:2
  
向阻塞栈中添加了元素:3
  
向阻塞栈中添加了元素:4
  
向阻塞栈中添加了元素:5
  
向阻塞栈中添加了元素:6
  
向阻塞栈中添加了元素:7
  
向阻塞栈中添加了元素:8
  
向阻塞栈中添加了元素:9
  
向阻塞栈中添加了元素:10
  
向阻塞栈中添加了元素:11
  
向阻塞栈中添加了元素:12
  
向阻塞栈中添加了元素:13
  
向阻塞栈中添加了元素:14
  
向阻塞栈中添加了元素:15
  
向阻塞栈中添加了元素:16
  
向阻塞栈中添加了元素:17
  
向阻塞栈中添加了元素:18
  
向阻塞栈中添加了元素:19

从上面结果可以看到，程序并没结束，二是阻塞住了，原因是栈已经满了，后面追加元素的操作都被阻塞了。