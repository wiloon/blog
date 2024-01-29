---
title: wait(),notify(),notifyAll()
author: "-"
date: 2017-03-24T15:14:36+00:00
url: /?p=9921
categories:
  - Inbox
tags:
  - reprint
---
## wait(),notify(),notifyAll()
notifyAll 是一个重的方法,它会带来大量的上下文切换和锁竞争。

wait(),notify(),notifyAll()不属于Thread类,而是属于Object基础类,也就是说每个对像都有wait(),notify(),notifyAll()的功能.因为都个对像都有锁,锁是每个对像的基础,当然操作锁的方法也是最基础了。
  
wait导致当前的线程等待,直到其他线程调用此对象的 notify() 方法或 notifyAll() 方法,或被其他线程中断。wait只能由持有对像锁的线程来调用。
  
notify唤醒在此对象监视器上等待的单个线程。如果所有线程都在此对象上等待,则会选择唤醒其中一个线程(随机)。直到当前的线程放弃此对象上的锁,才能继续执行被唤醒的线程。同Wait方法一样,notify只能由持有对像锁的线程来调用.notifyall也一样,不同的是notifyall会唤配所有在此对象锁上等待的线程。
  
"只能由持有对像锁的线程来调用"说明wait方法与notify方法必须在同步块内执行,即synchronized(obj)之内.再者synchronized代码块内没有锁是寸步不行的,所以线程要继续执行必须获得锁。相辅相成。
  
看一个很经典的例子(生产者与消费者):

package ProductAndConsume;
  
import java.util.List;

public class Consume implements Runnable{
  
private List container = null;
  
private int count;
  
public Consume(List lst){
  
this.container = lst;
  
}
  
public void run() {

while(true){
  
synchronized (container) {
  
if(container.size()== 0){
  
try {
  
container.wait();//容器为空,放弃锁,等待生产
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
}
  
try {
  
Thread.sleep(100);
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
container.remove(0);
  
container.notify();
  
System.out.println("我吃了"+(++count)+"个");
  
}
  
}

}

}

package ProductAndConsume;
  
import java.util.List;

public class Product implements Runnable {
  
private List container = null;
  
private int count;
  
public Product(List lst) {
  
this.container = lst;
  
}

public void run() {
  
while (true) {
  
synchronized (container) {
  
if (container.size() > MultiThread.MAX) {
  
//如果容器超过了最大值,就不要在生产了,等待消费
  
try {
  
container.wait();
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
}
  
try {
  
Thread.sleep(100);
  
} catch (InterruptedException e) {
  
e.printStackTrace();
  
}
  
container.add(new Object());
  
container.notify();
  
System.out.println("我生产了"+(++count)+"个");
  
}
  
}

}

}

package ProductAndConsume;
  
import java.util.ArrayList;
  
import java.util.List;

public class MultiThread {
  
private List container = new ArrayList();
  
public final static int MAX = 5;
  
public static void main(String args[]){

MultiThread m = new MultiThread();

new Thread(new Consume(m.getContainer())).start();
  
new Thread(new Product(m.getContainer())).start();
  
new Thread(new Consume(m.getContainer())).start();
  
new Thread(new Product(m.getContainer())).start();
  
}
  
public List getContainer() {
  
return container;
  
}

public void setContainer(List container) {
  
this.container = container;
  
}

http://guojuanjun.blog.51cto.com/277646/321695
  
http://blog.csdn.net/iter_zc/article/details/40651971