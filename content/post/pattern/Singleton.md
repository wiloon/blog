---
title: 单例 Singleton
author: "-"
date: 2012-10-16T06:09:56+00:00
url: Singleton
categories:
  - Java
tags:
  - DesignPattern

---
## 单例 Singleton

### 静态内部类 static nested class

这种方法也是《Effective Java》上所推荐的。
  
这种写法仍然使用JVM本身机制保证了线程安全问题；由于 SingletonHolder 是私有的，除了 getInstance() 之外没有办法访问它，因此它是懒汉式的；同时读取实例的时候不会进行同步，没有性能缺陷；也不依赖 JDK 版本。

这是利用了JVM的特性：静态内部类时在类加载时实现的，因此不会受到多线程的影响，自然也就不会出现多个实例。

```java
public class Singleton {
    private static class SingletonHolder {
        private static final Singleton INSTANCE = new Singleton();
    }

    private Singleton() {
    }

    public static final Singleton getInstance() {
        return SingletonHolder.INSTANCE;
    }
}
```

## 单例模式 (Singleton)

1. 介绍: 也叫单子模式，是一种常用的软件设计模式。在应用这个模式时，单例对象的类必须保证只有一个实例存在。许多时候整个系统只需要拥有一个的全局对象，这样有利于我们协调系统整体的行为。比如在某个服务器程序中，该服务器的配置信息存放在一个文件中，这些配置数据由一个单例对象统一读取，然后服务进程中的其他对象再通过这个单例对象获取这些配置信息。这种方式简化了在复杂环境下的配置管理。
  
2. 实现单例模式的思路是: 一个类能返回对象一个引用(永远是同一个)和一个获得该实例的方法 (必须是静态方法，通常使用getInstance这个名称)； 当我们调用这个方法时，如果类持有的引用不为空就返回这个引用，如果类保持的引用为空就创建该类的实例并将实例的引用赋予该类保持的引用；同时我们还将该类的构造函数定义为私有方法，这样其他处的代码就无法通过调用该类的构造函数来实例化该类的对象，只有通过该类提供的静态方法来得到该类的唯一实例。
  
3. 注意事项: 单例模式在多线程的应用场合下必须小心使用。如果当唯一实例尚未创建时，有两个线程同时调用创建方法，那么它们同时没有检测到唯一实例的存在，从而同时各自创建了一个实例，这样就有两个实例被构造出来，从而违反了单例模式中实例唯一的原则。 解决这个问题的办法是为指示类是否已经实例化的变量提供一个互斥锁(虽然这样会降低效率)。
  
4. 实现方式: 通常单例模式在Java语言中，有两种构建方式:
  
饿汉方式:指全局的单例实例在类装载时构建。(一般认为这种方式要更加安全些)
  
懒汉方式:指全局的单例实例在第一次被使用时构建。
  
5. 示例:

```java
/*
方式一: 饿汉式单例模式
缺点是它不是一种懒加载模式 (lazy initialization) ，单例会在加载类后一开始就被初始化，即使客户端没有调用 getInstance()方法。
饿汉式的创建方式在一些场景中将无法使用: 譬如 Singleton 实例的创建是依赖参数或者配置文件的，
在 getInstance() 之前必须调用某个方法设置参数给它，那样这种单例写法就无法使用了。
*/
 package org.qiujy.test;
public class Singleton1 {
//构造方式设为private,外部不能访问
 private Singleton1() {
 }
// 在自己内部定义自己的一个private实例,只供内部调用
 private static final Singleton1 instance = new Singleton1();
// 提供了一个供外部访问本class的静态方法,可以直接访问
 public static Singleton1 getInstance() {
 return instance;
 }
 }

//方式二: 懒汉式单例模式
package org.qiujy.test;

public class Singleton2 {
private static Singleton2 instance = null;

//这个synchronized很重要
 public static synchronized Singleton2 getInstance() {
// 第一次使用时生成实例
 if (instance == null){
 instance = new Singleton2();
 }

return instance;
 }
 }
 //------------------------------------------------------------------------------------//

//多线程2: 双重判断
public class Singleton { 
 private static volatile Singleton singleton; 
 private static Lock lock = new ReentrantLock(); 

 private Singleton(){}; 
 public static Singleton getInstance(){ 
 if(singleton == null){ 
 lock.lock(); 
 try { 
 if(singleton == null){ 
 singleton = new Singleton(); 
 } 
 } finally{ 
 lock.unlock(); 
 } 
 }
 return singleton; 
 } 
} 
/*
这里为什么用 volatile, 主要还是因为 singleton = new Singleton(); 并不是原子性的，它会分为3步: 

给 instance 分配内存
调用 Singleton 的构造函数来初始化成员变量
将instance对象指向分配的内存空间 (执行完这步 instance 就为非 null 了) 
但是在 JVM 的即时编译器中存在指令重排序的优化。也就是说上面的第二步和第三步的顺序是不能保证的，
最终的执行顺序可能是 1-2-3 也可能是 1-3-2。如果是后者，则在 3 执行完毕、2 未执行之前，被线程二抢占了，
这时 instance 已经是非 null 了 (但却没有初始化) ，所以线程二会直接返回 instance，然后使用，然后顺理成章地报错。 
所以这里的 volatile 主要是用来做禁止指令重排序的。
*/

Google公司的工程师Bob Lee写的新的懒汉单例模式
public class Singleton {
static class SingletonHolder {
 static Singleton instance = new Singleton();
 }

public static Singleton getInstance() {
 return SingletonHolder.instance;
 }

}
//在加载singleton时并不加载它的内部类SingletonHolder，而在调用getInstance () 时调用SingletonHolder时才加载SingletonHolder，
//从而调用singleton的构造函数，实例化singleton，从而达到lazy loading的效果。
```

golang
  
[https://blog.csdn.net/qibin0506/article/details/50733314](https://blog.csdn.net/qibin0506/article/details/50733314)

[http://blog.csdn.net/qjyong/article/details/1721342](http://blog.csdn.net/qjyong/article/details/1721342)

[http://wuchong.me/blog/2014/08/28/how-to-correctly-write-singleton-pattern/](http://wuchong.me/blog/2014/08/28/how-to-correctly-write-singleton-pattern/)

[http://www.iteye.com/topic/537563](http://www.iteye.com/topic/537563)

[https://github.com/pzxwhc/MineKnowContainer/issues/74](https://github.com/pzxwhc/MineKnowContainer/issues/74)
  
[http://www.wiloon.com/?p=9951](http://www.wiloon.com/?p=9951)
>[https://juejin.cn/post/6844903655510917128](https://juejin.cn/post/6844903655510917128)
