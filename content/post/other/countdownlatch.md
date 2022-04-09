---
title: CountDownLatch
author: "-"
date: 2015-06-26T09:42:47+00:00
url: /?p=7869
categories:
  - Uncategorized
tags:
  - Java

---
## CountDownLatch

CountDownLatch是一个同步辅助类,在完成一组正在其他线程中执行的操作之前,它允许一个或多个线程一直等待。

**CountDownLatch和CyclicBarrier的区别**
  
(01) CountDownLatch的作用是允许1或N个线程等待其他线程完成执行；而CyclicBarrier则是允许N个线程相互等待。
  
(02) CountDownLatch的计数器无法被重置；CyclicBarrier的计数器可以被重置后使用,因此它被称为是循环的barrier。

下面通过CountDownLatch实现: "主线程"等待"5个子线程"全部都完成"指定的工作(休眠1000ms)"之后,再继续运行。

```java

import java.util.concurrent.CountDownLatch;
  
import java.util.concurrent.CyclicBarrier;

public class CountDownLatchTest1 {

private static int LATCH_SIZE = 5;
  
private static CountDownLatch doneSignal;
  
public static void main(String[] args) {

try {
  
doneSignal = new CountDownLatch(LATCH_SIZE);

// 新建5个任务
  
for(int i=0; i<LATCH_SIZE; i++)
  
new InnerThread().start();

System.out.println("main await begin.");
  
// "主线程"等待线程池中5个任务的完成
  
doneSignal.await();

System.out.println("main await finished.");
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
}

static class InnerThread extends Thread{
  
public void run() {
  
try {
  
Thread.sleep(1000);
  
System.out.println(Thread.currentThread().getName() + " sleep 1000ms.");
  
// 将CountDownLatch的数值减1
  
doneSignal.countDown();
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
}
  
}
  
}

```

主线程通过doneSignal.await()等待其它线程将doneSignal递减至0。其它的5个InnerThread线程,每一个都通过doneSignal.countDown()将doneSignal的值减1；当doneSignal为0时,main被唤醒后继续执行。


http://www.cnblogs.com/skywang12345/p/3533887.html#a1

http://zapldy.iteye.com/blog/746458