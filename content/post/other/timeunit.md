---
title: TimeUnit
author: "-"
date: 2011-11-19T06:46:00+00:00
url: /?p=1537
categories:
  - Java
tags:
  - reprint
---
## TimeUnit
http://chenjumin.iteye.com/blog/2182171

//关于秒的常用方法
  
TimeUnit.SECONDS.toMillis(1) 1秒转换为毫秒数
  
TimeUnit.SECONDS.toMinutes(60) 60秒转换为分钟数
  
TimeUnit.SECONDS.sleep(5) 线程休眠5秒
  
TimeUnit.SECONDS.convert(1, TimeUnit.MINUTES) 1分钟转换为秒数

//TimeUnit.DAYS 日的工具类
  
//TimeUnit.HOURS 时的工具类
  
//TimeUnit.MINUTES 分的工具类
  
//TimeUnit.SECONDS 秒的工具类
  
//TimeUnit.MILLISECONDS 毫秒的工具类

http://www.importnew.com/7219.html

### TimeUnit是什么
TimeUnit是java.util.concurrent包下面的一个类，TimeUnit提供了可读性更好的线程暂停操作，通常用来**替换 Thread.sleep()**，在很长一段时间里 Thread的sleep() 方法作为暂停线程的标准方式，几乎所有Java程序员都熟悉它，事实上sleep方法本身也很常用而且出现在很多面试中。如果你已经使用过 Thread.sleep()，当然我确信你这样做过，那么你一定熟知它是一个静态方法，暂停线程时它**不会释放锁**，该方法会抛出 InterrupttedException 异常 (如果有线程中断了当前线程) 。但是我们很多人并没有注意的一个潜在的问题就是它的可读性。Thread.sleep() 是一个重载方法，可以接收长整型毫秒和长整型的纳秒参数，这样对程序员造成的一个问题就是很难知道到底当前线程是睡眠了多少秒、分、小时或者天。看看下面这个Thread.sleep()方法: 

```java
Thread.sleep (2400000) 
```
  
粗略一看，你能计算出当前线程是等待多长时间吗？可能有些人可以，但是对于大多数程序员来说这种写法的可读性还是很差的，你需要把毫秒转换成秒和分，让我们来看看另外一个例子，这个例子比前面那个例子可读性稍微好一点: 

```java
Thread.sleep(4_60_1000);
```
  
这比前面那个例子已经好多了，但是仍然不是最好的，你注意到睡眠时间用毫秒，不容易猜出当前线程将等待4分钟。TimeUnit类解决了这个问题，通过指定DAYS、HOURS、MINUTES,SECONDS、MILLISECONDS和NANOSECONDS。java.utils.concurrent .TimeUnit 是Java枚举应用场景中最好的例子之一，所有TimeUnit都是枚举实例，让我们来看看线程睡眠4分钟用TimeUnit是如何使用的。

```java
TimeUnit.MINUTES.sleep(4); // sleeping for 4 minutes
```
  
类似你可以采用秒、分、小时级别来暂停当前线程。你可以看到这比Thread的sleep方法的可读的好多了。记住TimeUnit.sleep()内部调用的Thread.sleep()也会抛出InterruptException。你也可以查看JDK源代码去验证一下。下面是一个简单例子，它展示如果使用TimeUnit.sleep()方法。

```java
public class TimeUnitTest {

    public static void main(String args[]) throws InterruptedException {
    
        System.out.println("Sleeping for 4 minutes using Thread.sleep()");
        Thread.sleep(4 * 60 * 1000);
        System.out.println("Sleeping for 4 minutes using TimeUnit sleep()");
    
        TimeUnit.SECONDS.sleep(4);
        TimeUnit.MINUTES.sleep(4);
        TimeUnit.HOURS.sleep(1);
        TimeUnit.DAYS.sleep(1);
    }
}
```
  
除了sleep的功能外，TimeUnit还提供了便捷方法用于把时间转换成不同单位，例如，如果你想把秒转换成毫秒，你可以使用下面代码: 

TimeUnit.SECONDS.toMillis(44)
  
它将返回44,000

#### TimeUnit vs Thread.sleep()

目前我们讨论使用TimeUnit的好处是提高了可读性，但是有时候觉得其他方法更好，因为Thread.sleep()伴随java很早就出现了，几乎所有程序员都知道Thread.sleep()，都知道是将当前线程暂停，而对TimeUnit并不太熟悉。两个原因: 一是对比起Thread.sleep()，TimeUnit不是很常用，第二是在它不在Thread类中，就像wait和notify同样不是在Thread中，反正这些需要一段时间才能被采用,并成为一个标准的方式。

总结来说在你想用Thread.sleep()方法的地方你最好使用TimeUnit.sleep()方法来代替。它不仅可以提高代码的可读性而且能更加熟悉java.util.concurrent包，因为TimeUnit在并发编程中也是一个关键API。