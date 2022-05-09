---
title: thread join
author: "-"
date: 2015-01-13T05:52:17+00:00
url: thread-join
categories:
  - Inbox
tags:
  - reprint
---
## thread join

thread join 之后,主线程的状态是waiting

一、在研究join的用法之前,先明确两件事情。

1.join方法定义在Thread类中,则调用者必须是一个线程,

例如:

Thread t = new CustomThread();//这里一般是自定义的线程类

t.start();//线程起动

t.join();//此处会抛出InterruptedException异常

2.上面的两行代码也是在一个线程里面执行的。

以上出现了两个线程,一个是我们自定义的线程类,我们实现了run方法,做一些我们需要的工作；另外一个线程,生成我们自定义线程类的对象,然后执行

customThread.start();

customThread.join();

在这种情况下,两个线程的关系是一个线程由另外一个线程生成并起动,所以我们暂且认为第一个线程叫做"子线程",另外一个线程叫做"主线程"。

二、为什么要用join()方法

主线程生成并起动了子线程,而子线程里要进行大量的耗时的运算(这里可以借鉴下线程的作用),当主线程处理完其他的事务后,需要用到子线程的处理结果,这个时候就要用到join();方法了。

三、join方法的作用

在网上看到有人说"将两个线程合并"。这样解释我觉得理解起来还更麻烦。不如就借鉴下API里的说法:

"等待该线程终止。"

解释一下,是主线程(我在"一"里已经命名过了)等待子线程的终止。也就是在子线程调用了join()方法后面的代码,只有等到子线程结束了才能执行。(Waits for this thread to die.)

四、用实例来理解

写一个简单的例子来看一下join()的用法,一共三个类:

1.CustomThread 类

  1. CustomThread1类
  2. JoinTestDemo 类,main方法所在的类。

代码1:

```java 
  
package wxhx.csdn2;
  
/**
   
*
   
* @author bzwm
   
*
   
*/
  
class CustomThread1 extends Thread {
      
public CustomThread1() {
          
super("[CustomThread1] Thread");
      
};
      
public void run() {
          
String threadName = Thread.currentThread().getName();
          
System.out.println(threadName + " start.");
          
try {
              
for (int i = 0; i < 5; i++) {
                  
System.out.println(threadName + " loop at " + i);
                  
Thread.sleep(1000);
              
}
              
System.out.println(threadName + " end.");
          
} catch (Exception e) {
              
System.out.println("Exception from " + threadName + ".run");
          
}
      
}
  
}
  
class CustomThread extends Thread {
      
CustomThread1 t1;
      
public CustomThread(CustomThread1 t1) {
          
super("[CustomThread] Thread");
          
this.t1 = t1;
      
}
      
public void run() {
          
String threadName = Thread.currentThread().getName();
          
System.out.println(threadName + " start.");
          
try {
              
t1.join();
              
System.out.println(threadName + " end.");
          
} catch (Exception e) {
              
System.out.println("Exception from " + threadName + ".run");
          
}
      
}
  
}
  
public class JoinTestDemo {
      
public static void main(String[] args) {
          
String threadName = Thread.currentThread().getName();
          
System.out.println(threadName + " start.");
          
CustomThread1 t1 = new CustomThread1();
          
CustomThread t = new CustomThread(t1);
          
try {
              
t1.start();
              
Thread.sleep(2000);
              
t.start();
              
t.join();//在代碼2里,將此處注釋掉
          
} catch (Exception e) {
              
System.out.println("Exception from main");
          
}
          
System.out.println(threadName + " end!");
      
}
  
}

打印结果: 

main start.//main方法所在的线程起动,但没有马上结束,因为调用t.join();,所以要等到t结束了,此线程才能向下执行。

[CustomThread1] Thread start.//线程CustomThread1起动

[CustomThread1] Thread loop at 0//线程CustomThread1执行

[CustomThread1] Thread loop at 1//线程CustomThread1执行

[CustomThread] Thread start.//线程CustomThread起动,但没有马上结束,因为调用t1.join();,所以要等到t1结束了,此线程才能向下执行。

[CustomThread1] Thread loop at 2//线程CustomThread1继续执行

[CustomThread1] Thread loop at 3//线程CustomThread1继续执行

[CustomThread1] Thread loop at 4//线程CustomThread1继续执行

[CustomThread1] Thread end. //线程CustomThread1结束了

[CustomThread] Thread end.// 线程CustomThread在t1.join();阻塞处起动,向下继续执行的结果

main end!//线程CustomThread结束,此线程在t.join();阻塞处起动,向下继续执行的结果。

修改一下代码,得到代码2: (这里只写出修改的部分)

```java 
  
public class JoinTestDemo {
      
public static void main(String[] args) {
          
String threadName = Thread.currentThread().getName();
          
System.out.println(threadName + " start.");
          
CustomThread1 t1 = new CustomThread1();
          
CustomThread t = new CustomThread(t1);
          
try {
              
t1.start();
              
Thread.sleep(2000);
              
t.start();
  
// t.join();//在代碼2里,將此處注釋掉
          
} catch (Exception e) {
              
System.out.println("Exception from main");
          
}
          
System.out.println(threadName + " end!");
      
}
  
}

打印结果: 

main start. // main方法所在的线程起动,但没有马上结束,这里并不是因为join方法,而是因为Thread.sleep(2000);

[CustomThread1] Thread start. //线程CustomThread1起动

[CustomThread1] Thread loop at 0//线程CustomThread1执行

[CustomThread1] Thread loop at 1//线程CustomThread1执行

main end!// Thread.sleep(2000);结束,虽然在线程CustomThread执行了t1.join();,但这并不会影响到其他线程(这里main方法所在的线程)。

[CustomThread] Thread start. //线程CustomThread起动,但没有马上结束,因为调用t1.join();,所以要等到t1结束了,此线程才能向下执行。

[CustomThread1] Thread loop at 2//线程CustomThread1继续执行

[CustomThread1] Thread loop at 3//线程CustomThread1继续执行

[CustomThread1] Thread loop at 4//线程CustomThread1继续执行

[CustomThread1] Thread end. //线程CustomThread1结束了

[CustomThread] Thread end. // 线程CustomThread在t1.join();阻塞处起动,向下继续执行的结果

五、从源码看join()方法

在CustomThread的run方法里,执行了t1.join();,进入看一下它的JDK源码: 

```java 
  
public final void join() throws InterruptedException {
  
n(0);
  
}

然后进入join(0)方法: 

```java 
     
/**
      
* Waits at most `millis` milliseconds for this thread to
      
* die. A timeout of `` means to wait forever. //注意这句
      
*
      
* @param millis the time to wait in milliseconds.
      
* @exception InterruptedException if another thread has interrupted
      
* the current thread. The _interrupted status_ of the
      
* current thread is cleared when this exception is thrown.
      
*/
     
public final synchronized void join(long millis) //参数millis为0.
     
throws InterruptedException {
  
long base = System.currentTimeMillis();
  
long now = 0;
  
if (millis < 0) {
             
throw new IllegalArgumentException("timeout value is negative");
  
}
  
if (millis == 0) {//进入这个分支
      
while (isAlive()) {//判断本线程是否为活动的。这里的本线程就是t1.
      
wait(0);//阻塞
      
}
  
} else {
      
while (isAlive()) {
      
long delay = millis - now;
      
if (delay <= 0) {
          
break;
      
}
      
wait(delay);
      
now = System.currentTimeMillis() - base;
      
}
  
}
     
}

单纯从代码上看,如果线程被生成了,但还未被起动,调用它的join()方法是没有作用的。将直接继续向下执行,这里就不写代码验证了。

http://blog.csdn.net/bzwm/article/details/3881392
