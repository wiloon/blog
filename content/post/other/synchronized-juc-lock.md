---
title: Synchronized 和 java.util.concurrent.locks.Lock 的区别
author: lcf
date: 2012-09-25T02:06:50+00:00
url: synchronized-concurrent-locks
categories:
  - Java
tags:
  - lock
---
## Synchronized 和 java.util.concurrent.locks.Lock 的区别

主要相同点: Lock 能完成 Synchronized 所实现的所有功能。

主要不同点: Lock 有比 Synchronized 更精确的线程语义和更好的性能。Synchronized 会自动释放锁，但是 Lock 一定要求程序员手工释放，并且必须在 finally 从句中释放。

### synchronized 修饰方法

synchronized 修饰方法时 表示同一个对象在不同的线程中表现为同步队列

如果实例化不同的对象 那么synchronized就不会出现同步效果了。

#### 对象的锁

所有对象都自动含有单一的锁。
  
JVM负责跟踪对象被加锁的次数。如果一个对象被解锁，其计数变为0。在任务 (线程) 第一次给对象加锁的时候，计数变为1。每当这个相同的任务 (线程) 在此对象上获得锁时，计数会递增。
  
只有首先获得锁的任务 (线程) 才能继续获取该对象上的多个锁。
  
每当任务离开一个 synchronized 方法，计数递减，当计数为0的时候，锁被完全释放，此时别的任务就可以使用此资源。
  
### synchronized同步块
  
2.1同步到单一对象锁
  
当使用同步块时，如果方法下的同步块都同步到一个对象上的锁，则所有的任务 (线程) 只能互斥的进入这些同步块。
  
Resource1.java演示了三个线程 (包括main线程) 试图进入某个类的三个不同的方法的同步块中，虽然这些同步块处在不同的方法中，但由于是同步到同一个对象 (当前对象 synchronized (this)) ，所以对它们的方法依然是互斥的。
  
比如

```java

Class Test{
public static User user=null;
Public synchronized void add(User u){
user=u;
Dao.save(user)

}

}

//如果在线程1中 Test test=new Test();

User u=new User();

u.setUserName("liaomin");

u.setUserPassword("liaomin");

Test.add(u);

//如果在线程2中 Test tes1t=new Test();

User u1=new User();

u1.setUserName("huqun");

u1.setUserPassword("huqun");

Tes1t.add(u1);

```

那么 现在线程1 和线程2同时启动 如果对象new的不是同一个Test

那么出现线程交叉的话 那么插入数据库中的数据就是相同的

因为你的user变量时静态的   你给他赋值第一次 假如还没有save的时候

另外一个线程改变了user的值 那么第一个线程插入时也就是第二次赋予的值了

所以要实现同步 那么可以改方法为静态的就能达到同步的效果了

修改如下

```java

Public static synchronized void add(User u)

{

user=u;

Dao.save(user)

}

```

修改为static的方法是存在于堆中

是全局方法 针对于所有实例化与未实例化的对象只存在一个 所以会出现同步队列

当然不用static 也可以 那就用 lock

```java

Class Test

{

public static User user=null;

Lock lock=new ReentrantLock();

Public void add(User u)

{

lock.lock();

user=u;

Dao.save(user);

lock.unlock();

}

}

//这样无论你new多少个对象都会是线程同步的, 相当于

Public static synchronized void add(User u)

{

user=u;

Dao.save(user)

}

```

同时 lock 性能上高于synchronized  
只是 lock 需要手动关闭  
