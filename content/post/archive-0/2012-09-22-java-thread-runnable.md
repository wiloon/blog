---
title: Java 多线程/Thread
author: wiloon
type: post
date: 2012-09-22T11:22:57+00:00
url: /?p=4198
categories:
  - Java
tags:
  - Java
  - Thread

---
### Runnable接口

在实际开发中一个多线程的操作很少使用Thread类，而是通过Runnable接口完成。

```java
public interface Runnable{
public void run();
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

但是在使用Runnable定义的子类中没有start()方法，只有Thread类中才有。此时观察Thread类，有一个构造方法：public Thread(Runnable targer)此构造方法接受Runnable的子类实例，也就是说可以通过Thread类来启动Runnable实现的多线程。（start()可以协调系统的资源）:

"\`java
  
import org.runnable.demo.MyThread;

public class ThreadDemo01 {
  
public static void main(String[] args) {
  
MyThread mt1=new MyThread("线程a");
  
MyThread mt2=new MyThread("线程b");
  
new Thread(mt1).start();
  
new Thread(mt2).start();
  
}

}

[/java]

· 两种实现方式的区别和联系：

在程序开发中只要是多线程肯定永远以实现Runnable接口为主，因为实现Runnable接口相比

继承Thread类有如下好处：

->避免点继承的局限，一个类可以继承多个接口。

->适合于资源的共享

以卖票程序为例，通过Thread类完成：

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

下面通过三个线程对象，同时卖票：

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

如果用Runnable就可以实现资源共享，下面看例子：

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

虽然现在程序中有三个线程，但是一共卖了10张票，也就是说使用Runnable实现多线程可以达到资源共享目的。

Runnable接口和Thread之间的联系：

public class Thread extends Object implements Runnable

发现Thread类也是Runnable接口的子类。

 

<http://jinguo.iteye.com/blog/286772>

Runnable是Thread的接口，在大多数情况下“推荐用接口的方式”生成线程，因为接口可以实现多继承，况且Runnable只有一个run方法，很适合继承。

在使用Thread的时候只需要new一个实例出来，调用start()方法即可以启动一个线程。
  
Thread Test = new Thread();
  
Test.start();

在使用Runnable的时候需要先new一个继承Runnable的实例，之后用子类Thread调用。

[java]
   
Test impelements Runnable
   
Test t = new Test();
   
Thread test = new Thread(t);

[/java]

在某个题目里，需要分别打印出a与b各10次，并且每打印一次a睡1秒，打印一次b睡2秒。

可以在run方法外面定义String word与int time
  
之后用

[java]
   
Thread t1 = new Thread();
   
Thread t2 = new Thread();

t1.word = "a"
   
t1.time = 1000

t2.Word = "b"
   
t2.time = 2000

t1.start();
   
t2.start();

[/java]

--Runnable的代码

[java]

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

[/java]

http://blog.csdn.net/wwww1988600/article/details/7309070

https://www.kancloud.cn/digest/java-multithreading/134267

locl condition

http://blog.csdn.net/ghsau/article/details/7481142

<p id="java">
  创建和启动线程的三种方式
 https://jisonami.github.io/2016/09/04/JavaThread1/

<blockquote data-secret="Y65uz4t1vN" class="wp-embedded-content">
  
    <a href="http://www.wiloon.com/wordpress/?p=9968">多线程的代价及上下文切换</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://www.wiloon.com/wordpress/?p=9968&embed=true#?secret=Y65uz4t1vN" data-secret="Y65uz4t1vN" width="600" height="338" title=""多线程的代价及上下文切换" - w1100n" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>