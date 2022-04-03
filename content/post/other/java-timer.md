---
title: java timer
author: "-"
date: 2011-10-13T08:55:42+00:00
url: /?p=673
categories:
  - Java

tags:
  - reprint
---
## java timer
### Timer和TimerTask
Timer是jdk中提供的一个定时器工具，使用的时候会在主线程之外起一个单独的线程执行指定的计划任务，可以指定执行一次或者反复执行多次。
TimerTask是一个实现了Runnable接口的抽象类，代表一个可以被Timer执行的任务。

### 一个Timer调度的例子
```java 
import java.util.Timer;
import java.util.TimerTask;
public class TestTimer {
public static void main(String args[]){

System.out.println("About to schedule task.");

new Reminder(3);

System.out.println("Task scheduled.");
  
}



public static class Reminder{

Timer timer;



public Reminder(int sec){

timer = new Timer();

timer.schedule(new TimerTask(){

public void run(){

System.out.println("Time's up!");

timer.cancel();

}

}, sec*1000);

}

}
}
```

运行之后，在console会首先看到: 

About to schedule task.
  
Task scheduled.

然后3秒钟后，看到

Time's up!

从这个例子可以看出一个典型的利用timer执行计划任务的过程如下: 

new一个TimerTask的子类，重写run方法来指定具体的任务，在这个例子里，我用匿名内部类的方式来实现了一个TimerTask的子类
  
new一个Timer类，Timer的构造函数里会起一个单独的线程来执行计划任务。jdk的实现代码如下: 

1 public Timer() {
  
2 this("Timer-" + serialNumber());
  
3 }
  
5 public Timer(String name) {
  
6 thread.setName(name);
  
7 thread.start();
  
8 }

调用相关调度方法执行计划。这个例子调用的是schedule方法。
  
任务完成，结束线程。这个例子是调用cancel方法结束线程。
  
3. 如何终止Timer线程

默认情况下，创建的timer线程会一直执行，主要有下面四种方式来终止timer线程: 

调用timer的cancle方法
  
把timer线程设置成daemon线程， (new Timer(true)创建daemon线程) ，在jvm里，如果所有用户线程结束，那么守护线程也会被终止，不过这种方法一般不用。
  
当所有任务执行结束后，删除对应timer对象的引用，线程也会被终止。
  
调用System.exit方法终止程序
  
4. 关于cancle方式终止线程

这种方式终止timer线程，jdk的实现比较巧妙，稍微说一下。

首先看cancle方法的源码: 
  
1 public void cancel() {
  
2 synchronized(queue) {
  
3 thread.newTasksMayBeScheduled = false;
  
4 queue.clear();
  
5 queue.notify(); // In case queue was already empty.
  
6 }
  
7 }

没有显式的线程stop方法，而是调用了queue的clear方法和queue的notify方法，clear是个自定义方法，notify是Objec自带的方法，很明显是去唤醒wait方法的。

再看clear方法: 
  
1 void clear() {
  
2 // Null out task references to prevent memory leak
  
3 for (int i=1; i<=size; i++)
  
4 queue[i] = null;
  
6 size = 0;
  
7 }

clear方法很简单，就是去清空queue，queue是一个TimerTask的数组，然后把queue的size重置成0，变成empty.还是没有看到显式的停止线程方法，回到最开始new Timer的时候，看看new Timer代码: 
  
1 public Timer() {
  
2 this("Timer-" + serialNumber());
  
3 }
  
5 public Timer(String name) {
  
6 thread.setName(name);
  
7 thread.start();
  
8 }

看看这个内部变量thread:

1 /**
  
2 * The timer thread.
  
3 */
  
4 private TimerThread thread = new TimerThread(queue);
  
不是原生的Thread,是自定义的类TimerThread.这个类实现了Thread类，重写了run方法，如下: 
  
1 public void run() {
  
2 try {
  
3 mainLoop();
  
4 } finally {
  
5 // Someone killed this Thread, behave as if Timer cancelled
  
6 synchronized(queue) {
  
7 newTasksMayBeScheduled = false;
  
8 queue.clear(); // Eliminate obsolete references
  
9 }
  
10 }
  
11 }

最后是这个mainLoop方法，这方法比较长，截取开头一段: 
  
1 private void mainLoop() {
  
2 while (true) {
  
3 try {
  
4 TimerTask task;
  
5 boolean taskFired;
  
6 synchronized(queue) {
  
7 // Wait for queue to become non-empty
  
8 while (queue.isEmpty() && newTasksMayBeScheduled)
  
9 queue.wait();
  
10 if (queue.isEmpty())
  
11 break; // Queue is empty and will forever remain; die

可以看到wait方法，之前的notify就是通知到这个wait，然后clear方法在notify之前做了清空数组的操作，所以会break，线程执行结束，退出。

  1. 反复执行一个任务

通过调用三个参数的schedule方法实现，最后一个参数是执行间隔，单位毫秒。

  1. schedule VS. scheduleAtFixedRate

这两个方法都是任务调度方法，他们之间区别是，schedule会保证任务的间隔是按照定义的period参数严格执行的，如果某一次调度时间比较长，那么后面的时间会顺延，保证调度间隔都是period,而scheduleAtFixedRate是严格按照调度时间来的，如果某次调度时间太长了，那么会通过缩短间隔的方式保证下一次调度在预定时间执行。举个栗子: 你每个3秒调度一次，那么正常就是0,3,6,9s这样的时间，如果第二次调度花了2s的时间，如果是schedule，就会变成0,3+2,8,11这样的时间，保证间隔，而scheduleAtFixedRate就会变成0,3+2,6,9，压缩间隔，保证调度时间。

  1. 一些注意点

每一个Timer仅对应唯一一个线程。
  
Timer不保证任务执行的十分精确。
  
Timer类的线程安全的。

1. 在应用开发中，经常需要一些周期性的操作，比如每5分钟执行某一操作等。对于这样的操作最方便、高效的实现方式就是使用java.util.Timer工具类。
  
private java.util.Timer timer;
  
timer = new Timer(true);
  
timer.schedule(
  
new java.util.TimerTask() { public void run() { //server.checkNewMail(); 要操作的方法 } }, 0, 5_60_1000);
  
第一个参数是要操作的方法，第二个参数是要设定延迟的时间，第三个参数是周期的设定，每隔多长时间执行该操作。
  
使用这几行代码之后，Timer本身会每隔5分钟调用一遍server.checkNewMail()方法，不需要自己启动线程。Timer本身也是多线程同步的，多个线程可以共用一个Timer，不需要外部的同步代码。
  
2. 
  
(1)Timer.schedule(TimerTask task,Date time)安排在制定的时间执行指定的任务。
  
(2)Timer.schedule(TimerTask task,Date firstTime ,long period)安排指定的任务在指定的时间开始进行重复的固定延迟执行．
  
(3)Timer.schedule(TimerTask task,long delay)安排在指定延迟后执行指定的任务．
  
(4)Timer.schedule(TimerTask task,long delay,long period)安排指定的任务从指定的延迟后开始进行重复的固定延迟执行．
  
(5)Timer.scheduleAtFixedRate(TimerTask task,Date firstTime,long period)安排指定的任务在指定的时间开始进行重复的固定速率执行．
  
(6)Timer.scheduleAtFixedRate(TimerTask task,long delay,long period)安排指定的任务在指定的延迟后开始进行重复的固定速率执行．

http://www.cnblogs.com/lingiu/p/3782813.html