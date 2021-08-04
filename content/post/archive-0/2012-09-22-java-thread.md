---
title: Java Thread/线程
author: "-"
date: "2012-09-22 11:22:57+00:00"
url: java-thread
tags:
  - Thread
categories:
  - Java
---
### 线程状态
[![WhlYxH.jpg](https://z3.ax1x.com/2021/07/26/WhlYxH.jpg)](https://imgtu.com/i/WhlYxH)  
[![W5Gb90.png](https://z3.ax1x.com/2021/07/27/W5Gb90.png)](https://imgtu.com/i/W5Gb90)

线程共包括以下5种状态。
1. 新建状态 (New)： 线程对象被创建后，就进入了新建状态。例如，Thread thread = new Thread()。
2. 就绪状态(Runnable): 也被称为 “可执行状态”。线程对象被创建后，其它线程调用了该对象的start()方法，从而来启动该线程。例如，thread.start()。处于就绪状态的线程，随时可能被CPU调度执行。
3. 运行状态(Running): 线程获取CPU权限进行执行。需要注意的是，线程只能从就绪状态进入到运行状态。
4. 阻塞状态(Blocked): 阻塞状态是线程因为某种原因放弃CPU使用权，暂时停止运行。直到线程进入就绪状态，才有机会转到运行状态。阻塞的情况分三种：
   - 等待阻塞 -- 通过调用线程的 wait() 方法，让线程等待某工作的完成。
   - 同步阻塞 -- 线程在获取 synchronized 同步锁失败(因为锁被其它线程所占用)，它会进入同步阻塞状态。
   - 其他阻塞 -- 通过调用线程的 sleep() 或 join() 或发出了I/O请求时，线程会进入到阻塞状态。当sleep()状态超时、join()等待线程终止或者超时、或者I/O处理完毕时，线程重新转入就绪状态。
5. 死亡状态(Dead): 线程执行完了或者因异常退出了run()方法，该线程结束生命周期。

这 5 种状态涉及到的内容包括 Object 类, Thread 类, 和 synchronized 关键字。 这些内容我们会在后面的章节中逐个进行学习。
Object 类，定义了 wait(), notify(), notifyAll( ) 等休眠/唤醒函数。
Thread 类，定义了一些列的线程操作函数。例如，sleep() 休眠函数, interrupt() 中断函数, getName() 获取线程名称等。
synchronized，是关键字；它区分为 synchronized 代码块和 synchronized 方法。 synchronized 的作用是让线程获取对象的同步锁。
在后面详细介绍 wait(), notify() 等方法时，我们会分析为什么 "wait(), notify() 等方法要定义在 Object 类，而不是 Thread 类中"

## 创建线程
### Runnable接口
在实际开发中一个多线程的操作很少使用 Thread 类，而是通过 Runnable 接口完成。

```java
    public interface Runnable{
      public void run();
      }
    }
```

例子：
```java
class MyThread implements Runnable{
    private String name;
        public MyThread(String name) {
        this.name = name;
    }
    public void run(){
        for(int i=0;i<100;i++){
        System.out.println("线程开始："+this.name+",i="+i);
        }
    }
};
```

但是在使用 Runnable 定义的子类中没有 start() 方法，只有 Thread 类中才有。此时观察 Thread 类，有一个构造方法：public Thread(Runnable targer)此构造方法接受Runnable的子类实例，也就是说可以通过Thread类来启动Runnable实现的多线程。（start()可以协调系统的资源）:

```java
import org.runnable.demo.MyThread;
public class ThreadDemo01 {
  public static void main(String[] args) {
    MyThread mt1=new MyThread("线程a");
    MyThread mt2=new MyThread("线程b");
    new Thread(mt1).start();
    new Thread(mt2).start();
  }
}
```

### 两种实现方式的区别和联系
在程序开发中只要是多线程肯定永远以实现Runnable接口为主，因为实现Runnable接口相比继承Thread类有如下好处：
- 避免点继承的局限，一个类可以继承多个接口。
- 适合于资源的共享

以卖票程序为例，通过Thread类完成：
```java
package org.demo.dff;

class MyThread extends Thread{

private int ticket=10;

public void run(){

for(int i=0;i<20;i++){

if(this.ticket>0){

System.out.println("卖票：ticket"+this.ticket-);

}

}

}

};
```
下面通过三个线程对象，同时卖票：
```java
package org.demo.dff;

public class ThreadTicket {

public static void main(String[] args) {

MyThread mt1=new MyThread();

MyThread mt2=new MyThread();

MyThread mt3=new MyThread();

mt1.start();//每个线程都各卖了10张，共卖了30张票

mt2.start();//但实际只有10张票，每个线程都卖自己的票

mt3.start();//没有达到资源共享

}

}
```
如果用Runnable就可以实现资源共享，下面看例子：
```java
package org.demo.runnable;

class MyThread implements Runnable{

private int ticket=10;

public void run(){

for(int i=0;i<20;i++){

if(this.ticket>0){

System.out.println("卖票：ticket"+this.ticket-);

}

}

}

}

package org.demo.runnable;

public class RunnableTicket {

public static void main(String[] args) {

MyThread mt=new MyThread();

new Thread(mt).start();//同一个mt，但是在Thread中就不可以，如果用同一

new Thread(mt).start();//个实例化对象mt，就会出现异常

new Thread(mt).start();

}

};
```
虽然现在程序中有三个线程，但是一共卖了10张票，也就是说使用Runnable实现多线程可以达到资源共享目的。

Runnable接口和Thread之间的联系：

public class Thread extends Object implements Runnable

发现Thread类也是Runnable接口的子类。

 

<http://jinguo.iteye.com/blog/286772>

Runnable是Thread的接口，在大多数情况下"推荐用接口的方式"生成线程，因为接口可以实现多继承，况且Runnable只有一个run方法，很适合继承。

在使用Thread的时候只需要new一个实例出来，调用start()方法即可以启动一个线程。
  
Thread Test = new Thread();
  
Test.start();

在使用Runnable的时候需要先new一个继承Runnable的实例，之后用子类Thread调用。

```java
   
Test impelements Runnable
   
Test t = new Test();
   
Thread test = new Thread(t);

```

在某个题目里，需要分别打印出a与b各10次，并且每打印一次a睡1秒，打印一次b睡2秒。

可以在run方法外面定义String word与int time
  
之后用

```java
   
Thread t1 = new Thread();
   
Thread t2 = new Thread();

t1.word = "a"
   
t1.time = 1000

t2.Word = "b"
   
t2.time = 2000

t1.start();
   
t2.start();

```

### Runnable的代码

```java

class T implements Runnable{
   
String s = "";
   
int time = 0;
   
public void run (){
   
for (int i=0;i<10;i++) {
   
try {
   
Thread.sleep(time);
   
} catch (InterruptedException e) {
   
Thread.interrupted();
   
}
   
System.out.println(s);
   
}
   
}
   
}
   
public class Test {
   
public static void main(String[] args) {
   
T t1 = new T();
   
T t2 = new T();
   
t1.s = "a";
   
t1.time = 100;
   
t2.s = "b";
   
t2.time = 200;
   
Thread a = new Thread(t1);
   
a.start();
   
Thread b = new Thread(t2);
   
b.start();

}
   
}

```
### 通过 java.util.concurrent 包中的线程池 创建线程
```java
ExecutorService es = Executors.newSingleThreadExecutor();  
        //创建Callable对象任务  
        CallableDemo calTask=new CallableDemo();  
        //提交任务并获取执行结果  
        Future<Integer> future =es.submit(calTask); 
```
### Callable
Runnable实现的是void run()方法，Callable实现的是 V call()方法，并且可以返回执行结果，其中Runnable可以提交给Thread来包装下，直接启动一个线程来执行，而Callable则一般都是提交给ExecuteService来执行。通常在开发中结合ExecutorService使用,将任务的提交与任务的执行解耦开,同时也能更好地利用Executor提供的各种特性
### 竞争条件 Race condition
什么是竞争条件以及竞争条件为什么会产生漏洞  
竞争条件是系统中的一种反常现象， 由于现代Linux系统中大量使用并发编程，对资源进行共享，如果产生错误的访问模式，便可能产生内存泄露， 系统崩溃，数据破坏，甚至安全问题。 竞争条件漏洞就是多个进程访问同一资源时产生的时间或者序列的冲突，并利用这个冲突来对系统进行攻击。 一个看起来无害的程序如果被恶意攻击者利用，将发生竞争条件漏洞  
https://www.cnblogs.com/0xJDchen/p/5988275.html

### 数据争用(data race) 和竞态条件(race condition)
在有关多线程编程的话题中，数据争用(data race) 和竞态条件(race condition)是两个经常被提及的名词，它们两个有着相似的名字，也是我们在并行编程中极力避免出现的。但在处理实际问题时，我们应该能明确区分它们两个。

1. 数据争用(data race)
定义：①多个线程对于同一个变量、②同时地、③进行读/写操作的现象并且④至少有一个线程进行写操作。（也就是说，如果所有线程都是只进行读操作，那么将不构成数据争用）
后果：如果发生了数据争用，读取该变量时得到的值将变得不可知，使得该多线程程序的运行结果将完全不可预测，可能直接崩溃。
如何防止：对于有可能被多个线程同时访问的变量使用排他访问控制，具体方法包括使用mutex（互斥量）和monitor（监视器），或者使用atomic变量。
2. 竞态条件(race condition)
相对于数据争用(data race)，竞态条件(race condition)指的是更加高层次的更加复杂的现象，一般需要在设计并行程序时进行细致入微的分析，才能确定。（也就是隐藏得更深）
定义：受各线程上代码执行的顺序和时机的影响，程序的运行结果产生（预料之外）的变化。
后果：如果存在竞态条件(race condition)，多次运行程序对于同一个输入将会有不同的结果，但结果并非完全不可预测，它将由输入数据和各线程的执行顺序共同决定。
如何预防：竞态条件产生的原因很多是对于同一个资源的一系列连续操作并不是原子性的，也就是说有可能在执行的中途被其他线程抢占，同时这个“其他线程”刚好也要访问这个资源。解决方法通常是：将这一系列操作作为一个critical section（临界区）。

### 代码示例
下面以C++实现的一个银行存款转账操作为例，说明数据争用(data race) 和竞态条件(race condition)的区别。

该系统的不変性条件：存款余额≥0，不允许借款。
3.1.数据争用的例子
int my_account = 0;      //我的账户余额
int your_account = 100;  //你的账户余额

// 转账操作: 存在数据争用(data race)！
bool racy_transfer(int& src, int& dst, int m)
{
  if (m <= src) {  //操作结果不可预测
    src -= m;      //操作结果不可预测
    dst += m;      //操作结果不可预测
    return true;
  } else {
    return false;
  }
}

// 将下面两个函数在两个线程分别运行
racy_transfer(your_account, my_account, 50);
racy_transfer(your_account, my_account, 80);

运行上面的的代码后，不光我们双方账号的余额不可预测，甚至整个系统会发生什么事情都无法保证。

### 竞态条件的例子
#include <atomic>
std::atomic<int> my_account = 0; //我的账户余额
std::atomic<int> your_account = 100;  //你的账户余额

// 汇款操作:没有数据争用(data race)，但存在竞态条件(race condition)！
bool unsafe_transfer(std::atomic<int>& src, std::atomic<int>& dst, int m)
{
  if (m <= src) {
    // ★在这个时候(m <= src)是否仍然成立？
    src -= m;
    dst += m;
    return true;
  } else {
    return false;
  }
}

//将下面两个函数在两个线程分别运行
unsafe_transfer(your_account, my_account, 50);//[A]
unsafe_transfer(your_account, my_account, 80);//[B]

上面代码中★所标注的就是竞态条件，也就是这时候m > src是完全有可能的。考虑以下三种情况：

[A]执行结束后，your_account == my_account == 50，[B]再开始执行，然而条件不满足，转账失败；
[B]执行结束后，your_account == 20 && my_account == 80，[A]再开始执行，然而条件不满足，转账失败；
[A]和[B]交错执行，而且都进入了if块之内，最终结果变成your_account == -30 && my_account == 130，程序虽然能正常退出，但显然违反了不变性条件——存款余额≥0。
对应于C++的std::atomic<int>、在Java有java.util.concurrent.atomic.AtomicInteger类（或者volatile修饰的变量）。

### 解决办法
#include <mutex>
int my_account = 0;//我的账户余额
int your_account = 100; //你的账户余额
std::mutex txn_guard;

//安全的转账操作
bool safe_transfer(int& src, int& dst, int m)
{
  //声明临界区开始
  std::lock_guard<std::mutex> lk(txn_guard);
  if (m <= src) {
    src -= m;
    dst += m;
    return true;
  } else {
    return false;
  }
}  //临界区结束

//将下面两个函数在两个线程分别运行
safe_transfer(your_account, my_account, 50);  // [A]
safe_transfer(your_account, my_account, 80);  // [B]

这样程序只会产生以下两种结果：

[A]执行结束后，your_account == my_account == 50，[B]再开始执行，然而条件不满足，转账失败：
[B]执行结束后，your_account == 20 && my_account == 80，[A]再开始执行，然而条件不满足，转账失败；
而不会出现[A]和[B]交错执行的情况，从而使数据始终符合系统规定的不变形条件。对应于C++的std::mutex和std::lock_guard，在Java有monitor（通常不用显式声明）+synchronized的组合。

### ThreadGroup


---

http://blog.csdn.net/wwww1988600/article/details/7309070

https://www.kancloud.cn/digest/java-multithreading/134267

locl condition

http://blog.csdn.net/ghsau/article/details/7481142

 
### 创建和启动线程的三种方式
 https://jisonami.github.io/2016/09/04/JavaThread1/
 
### 多线程的代价及上下文切换 
http://www.wiloon.com/wordpress/?p=9968

http://www.wiloon.com/wordpress/?p=9968&embed=true#?secret=Y65uz4t1vN


https://blog.csdn.net/gg_18826075157/article/details/72582939

————————————————
版权声明：本文为CSDN博主「烧煤的快感」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/gg_18826075157/article/details/72582939


https://www.cnblogs.com/skywang12345/p/java_threads_category.html
