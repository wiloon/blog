---
title: Java Exchanger
author: "-"
date: 2013-07-22T07:52:38+00:00
url: /?p=5690
categories:
  - Inbox
tags:
  - reprint
---
## Java Exchanger

<http://mouselearnjava.iteye.com/blog/1921947>

本文介绍Exchanger工具类, 然后采用Exchanger给出一个两个线程交换数值的简单实例。

  1. Exchanger介绍
  
    Java代码 收藏代码
  
    /**  
      * A synchronization point at which two threads can exchange objects. 
      * Each thread presents some object on entry to the {@link #exchange 
      * exchange} method, and receives the object presented by the other 
      * thread on return.
  
        */ 

从上面的注释中可以看出: Exchanger提供了一个同步点,在这个同步点,两个线程可以交换数据。每个线程通过exchange()方法的入口提供数据给另外的线程,并接收其它线程提供的数据,并返回。

Exchanger通过Lock和Condition来完成功能,Exchanger的一个重要的public方法是exchange方法,用于线程的数据交换,

  1. Exchanger工具类的使用案例
  
    本文给出一个简单的例子,实现两个线程之间交换数据,用Exchanger来做非常简单。 

Java代码 收藏代码
  
package my.concurrent.exchanger;

import java.util.concurrent.Exchanger;
  
import java.util.concurrent.atomic.AtomicReference;

public class ThreadA implements Runnable {

    private final Exchanger<Integer> exchanger;  
    
    private final AtomicReference<Integer> last = new AtomicReference<Integer>(  
            5);  
    
    public ThreadA(Exchanger<Integer> exchanger) {  
        this.exchanger = exchanger;  
    }  
    
    public void run() {  
        try {  
            while (true) {  
                last.set(exchanger.exchange(last.get()));  
                System.out.println(" After calling exchange. Thread A has value: " + last.get());  
                Thread.sleep(2000);  
            }  
        } catch (InterruptedException e) {  
            e.printStackTrace();  
        }  
    }  

}

Java代码 收藏代码
  
package my.concurrent.exchanger;

import java.util.concurrent.Exchanger;
  
import java.util.concurrent.atomic.AtomicReference;

public class ThreadB implements Runnable {

    private Exchanger<Integer> exchanger;  
    
    private final AtomicReference<Integer> last = new AtomicReference<Integer>(  
            10);  
    
    public ThreadB(Exchanger<Integer> exchanger) {  
        this.exchanger = exchanger;  
    }  
    
    public void run() {  
        try {  
            while (true) {  
                last.set(exchanger.exchange(last.get()));  
                System.out.println(" After calling exchange. Thread B has value: " + last.get());  
                Thread.sleep(2000);  
            }  
        } catch (InterruptedException e) {  
            e.printStackTrace();  
        }  
    }  

}

Java代码 收藏代码
  
package my.concurrent.exchanger;

import java.util.concurrent.Exchanger;

public class ExchangerTest {

    public static void main(String[] args) {  
        Exchanger<Integer> exchanger = new Exchanger<Integer>();  
        new Thread(new ThreadA(exchanger)).start();  
        new Thread(new ThreadB(exchanger)).start();  
    }  

}
