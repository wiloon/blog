---
title: java – volatile
author: "-"
date: 2014-02-12T02:12:30+00:00
url: volatile
categories:
  - Java
tags:
  - Java

---
## java – volatile
### volatile 关键字, Volatile ['vɑlətl]
volatile关键字告诉编译器,去**内存**里面取**最新**值。但是,即使取的是内存里的所谓“最新”值,事实上并不能保证最新。  

voldatile关键字首先具有“易变性”,声明为volatile变量编译器会强制要求读内存,相关语句不会直接使用上一条语句对应的的寄存器内容,而是重新从内存中读取。

其次具有”不可优化”性,volatile告诉编译器,不要对这个变量进行各种激进的优化,甚至将变量直接消除,保证代码中的指令一定会被执行。

最后具有“顺序性”,能够保证Volatile变量间的顺序性,编译器不会进行**乱序优化**。不过要注意与非volatile变量之间的操作,还是可能被编译器重排序的。

需要注意的是其含义跟**原子操作无关**,比如: volatile int a; a++; 其中a++操作实际对应三条汇编指令实现”读-改-写“操作 (RMW) ,并非原子的。

思考: bool 类型是不是适合使用, 不会出问题。
不同编程语言中 voldatile 含义与实现并不完全相同, Java 语言中 voldatile 变量可以被看作是一种轻量级的同步, 因其还附带了 acuire 和 release 语义。 实际上也是从 JDK5 以后才通过这个措施进行完善,其 volatile 变量具有 synchronized 的可见性特性, 但是不具备原子特性。 Java语言中有 volatile 修饰的变量, 赋值后多执行了一个 `load addl $0x0, (%esp)` 操作, 这个操作相当于一个 lock 指令, 就是增加一个完全的**内存屏障**指令, 这点与C++实现并不一样。 volatile 的读性能消耗与普通变量几乎相同, 但是写操作稍慢 ,因为它需要在本地代码中插入许多内存屏障指令来保证处理器不发生乱序执行。

Java 实践中仅满足下面这些条件才应该使用 volatile 关键字: 

- 变量写入操作不依赖变量当前值,或确保只有一个线程更新变量的值 (Java可以,C++仍然不能) 
- 该变量不会与其他变量一起纳入
- 变量并未被锁保护


C++中voldatile等于插入编译器级别屏障,因此并不能阻止CPU硬件级别导致的重排。C++11 中volatile语义没有任何变化,不过提供了std::atomic工具可以真正实现原子操作,而且默认加入了内存屏障 (可以通过在store与load操作时设置内存模型参数进行调整,默认为std::memory_order_seq_cst) 。

C++实践中推荐涉及并发问题都使用std::atomic,只有涉及特殊内存操作的时候才使用volatile关键字。这些情况通常IO相关,防止相关操作被编译器优化,也是volatile关键字发明的本意。

Volatile 修饰的成员变量在每次被线程访问时,都强迫从共享内存中重读该成员变量的值。而且,当成员变量发生变化时,强迫线程将变化值回写到共享内存。这样在任何时刻,两个不同的线程总是看到某个成员变量的值是相同的,更简单一点理解就是volatile修饰的变量值发生变化时对于另外的线程是可见的。

如何正确使用 volatile 可以参考下面这篇文章:  http://www.ibm.com/developerworks/cn/java/j-jtp06197.html Java 理论与实践: 正确使用 Volatile 变量

volatile关键字作用:
  
1. 保证了新值能立即存储到主内存,每次使用前立即从主内存中刷新。
  
2. 禁止指令重排序优化。
  
注: volatile 关键字不能保证在多线程环境下对共享数据的操作的正确性。可以使用在自己状态改变之后需要立即通知所有线程的情况下。

用在多线程,同步变量。 线程为了提高效率,将某成员变量(如A)拷贝了一份 (如B) ,线程中对A的访问其实访问的是B。只在某些动作时才进行A和B的同步。因此存在A和B不一致的情况。volatile就是用来避免这种情况的。volatile告诉jvm, 它所修饰的变量不保留拷贝,直接访问主内存中的 (也就是上面说的A)

在Java内存模型中,有main memory,每个线程也有自己的memory (例如寄存器)。为了性能,一个线程会在自己的memory中保持要访问的变量的副本。这样就会出现同一个变量在某个瞬间,在一个线程的memory中的值可能与另外一个线程memory中的值,或者main memory中的值不一致的情况。

一个变量声明为volatile,就意味着这个变量是随时会被其他线程修改的,因此不能将它cache在线程memory中。以下例子展现了volatile的作用: 

public class StoppableTask extends Thread {
  
private volatile boolean pleaseStop;
  
public void run() {
  
while (!pleaseStop) {
  
// do some stuff...
  
}
  
}
  
public void tellMeToStop() {
  
pleaseStop = true;
  
}
  
}
  
假如pleaseStop没有被声明为volatile,线程执行run的时候检查的是自己的副本,就不能及时得知其他线程已经调用tellMeToStop()修改了pleaseStop的值。

Volatile一般情况下不能代替sychronized,因为volatile不能保证操作的原子性,即使只是i++,实际上也是由多个原子操作组成: read i; inc; write i,假如多个线程同时执行i++,volatile只能保证他们操作的i是同一块内存,但依然可能出现写入脏数据的情况。如果配合Java 5增加的atomic wrapper classes,对它们的increase之类的操作就不需要sychronized。

Reference: 

http://www.javamex.com/tutorials/synchronization_volatile.shtml

http://www.javamex.com/tutorials/synchronization_volatile_java_5.shtml

http://www.ibm.com/developerworks/cn/java/j-jtp06197.html

=========================分割线2=================================

 

恐怕比较一下volatile和synchronized的不同是最容易解释清楚的。volatile是变量修饰符,而synchronized则作用于一段代码或方法；看如下三句get代码: 

 

Java代码 收藏代码

int i1;

int geti1() {return i1;}

volatile int i2;

int geti2()

{return i2;}

int i3;

synchronized int geti3() {return i3;}

geti1()

 

得到存储在当前线程中i1的数值。多个线程有多个i1变量拷贝,而且这些i1之间可以互不相同。换句话说,另一个线程可能已经改变了它线程内的i1值,而这个值可以和当前线程中的i1值不相同。事实上,Java有个思想叫"主"内存区域,这里存放了变量目前的"准确值"。每个线程可以有它自己的变量拷贝,而这个变量拷贝值可以和"主"内存区域里存放的不同。因此实际上存在一种可能: "主"内存区域里的i1值是1,线程1里的i1值是2,线程2里的i1值是3——这在线程1和线程2都改变了它们各自的i1值,而且这个改变还没来得及传递给"主"内存区域或其他线程时就会发生。

而 geti2()得到的是"主"内存区域的i2数值。用volatile修饰后的变量不允许有不同于"主"内存区域的变量拷贝。换句话说,一个变量经 volatile修饰后在所有线程中必须是同步的；任何线程中改变了它的值,所有其他线程立即获取到了相同的值。理所当然的,volatile修饰的变量存取时比一般变量消耗的资源要多一点,因为线程有它自己的变量拷贝更为高效。

既然volatile关键字已经实现了线程间数据同步,又要 synchronized干什么呢？呵呵,它们之间有两点不同。首先,synchronized获得并释放监视器——如果两个线程使用了同一个对象锁,监视器能强制保证代码块同时只被一个线程所执行——这是众所周知的事实。但是,synchronized也同步内存: 事实上,synchronized在" 主"内存区域同步整个线程的内存。因此,执行geti3()方法做了如下几步: 

  1. 线程请求获得监视this对象的对象锁 (假设未被锁,否则线程等待直到锁释放)  
  2. 线程内存的数据被消除,从"主"内存区域中读入 (Java虚拟机能优化此步。。。[后面的不知道怎么表达,汗]) 

  3. 代码块被执行

  4. 对于变量的任何改变现在可以安全地写到"主"内存区域中 (不过geti3()方法不会改变变量值) 

  5. 线程释放监视this对象的对象锁

因此volatile只是在线程内存和"主"内存间同步某个变量的值,而synchronized通过锁定和解锁某个监视器同步所有变量的值。显然synchronized要比volatile消耗更多资源。

 

=========================分割线3=================================

 

volatile关键字相信了解Java多线程的读者都很清楚它的作用。volatile关键字用于声明简单类型变量,如int、float、 boolean等数据类型。如果这些简单数据类型声明为volatile,对它们的操作就会变成原子级别的。但这有一定的限制。例如,下面的例子中的n就不是原子级别的: 

 

Java代码 收藏代码

package mythread;

 

public class JoinThread extends Thread

{

public static volatile int n = 0 ;

public void run()

{

for ( int i = 0 ; i < 10 ; i ++ )

try

{

n = n + 1 ;

sleep( 3 ); // 为了使运行结果更随机,延迟3毫秒

}

catch (Exception e)

{

}

}

public static void main(String[] args) throws Exception

{

 

Thread threads[] = new Thread[ 100 ];

for ( int i = 0 ; i < threads.length; i ++ )

// 建立100个线程

threads[i] = new JoinThread();

for ( int i = 0 ; i < threads.length; i ++ )

// 运行刚才建立的100个线程

threads[i].start();

for ( int i = 0 ; i < threads.length; i ++ )

// 100个线程都执行完后继续

threads[i].join();

System.out.println( " n= " + JoinThread.n);

}

}

如果对n的操作是原子级别的,最后输出的结果应该为n=1000,而在执行上面积代码时,很多时侯输出的n都小于1000,这说明n=n+1不是原子级别的操作。原因是声明为volatile的简单变量如果当前值由该变量以前的值相关,那么volatile关键字不起作用,也就是说如下的表达式都不是原子操作: 

n = n + 1 ;

n ++ ;

如果要想使这种情况变成原子操作,需要使用synchronized关键字,如上的代码可以改成如下的形式: 

Java代码 收藏代码

package mythread;

public class JoinThread extends Thread

{

public static int n = 0 ;

public static synchronized void inc()

{

n ++ ;

}

public void run()

{

for ( int i = 0 ; i < 10 ; i ++ )

try

{

inc(); // n = n + 1 改成了 inc();

sleep( 3 ); // 为了使运行结果更随机,延迟3毫秒

}

catch (Exception e)

{

}

}

public static void main(String[] args) throws Exception

{

Thread threads[] = new Thread[ 100 ];

for ( int i = 0 ; i < threads.length; i ++ )

// 建立100个线程

threads[i] = new JoinThread();

for ( int i = 0 ; i < threads.length; i ++ )

// 运行刚才建立的100个线程

threads[i].start();

for ( int i = 0 ; i < threads.length; i ++ )

// 100个线程都执行完后继续

threads[i].join();

System.out.println( " n= " + JoinThread.n);

}

}

上面的代码将n=n+1改成了inc(),其中inc方法使用了synchronized关键字进行方法同步。因此,在使用volatile关键字时要慎重,并不是只要简单类型变量使用volatile修饰,对这个变量的所有操作都是原来操作,当变量的值由自身的上一个决定时,如n=n+1、n++ 等,volatile关键字将失效,只有当变量的值和自身上一个值无关时对该变量的操作才是原子级别的,如n = m + 1,这个就是原级别的。所以在使用volatile关键时一定要谨慎,如果自己没有把握,可以使用synchronized来代替volatile。

volatile 变量是一种稍弱的同步机制在访问 volatile 变量时不会执行加锁操作,因此也就不会使执行线程阻塞,因此 volatile 变量是一种比 synchronized 关键字更轻量级的同步机制。
  
从内存可见性的角度看,写入 volatile 变量相当于退出同步代码块,而读取 volatile 变量相当于进入同步代码块。
  
在代码中如果过度依赖 volatile 变量来控制状态的可见性,通常会比使用锁的代码更脆弱,也更难以理解。仅当 volatile 变量能简化代码的实现以及对同步策略的验证时,才应该使用它。一般来说,用同步机制会更安全些。
  
加锁机制 (即同步机制) 既可以确保可见性又可以确保原子性,而 volatile 变量只能确保可见性,原因是声明为 volatile 的简单变量如果当前值与该变量以前的值相关,那么 volatile 关键字不起作用,也就是说如下的表达式都不是原子操作: count++、count = count+1。
  
当且仅当满足以下所有条件时,才应该使用 volatile 变量: 

对变量的写入操作不依赖变量的当前值,或者你能确保只有单个线程更新变量的值。
  
该变量没有包含在具有其他变量的不变式中。
  
总结: 在需要同步的时候,第一选择应该是 synchronized 关键字,这是最安全的方式,尝试其他任何方式都是有风险的。尤其在、jdK1.5 之后,对 synchronized 同步机制做了很多优化,如: 自适应的自旋锁、锁粗化、锁消除、轻量级锁等,使得它的性能明显有了很大的提升。

http://blog.csdn.net/orzorz/archive/2009/07/03/4319055.aspx
  
http://smallbug-vip.iteye.com/blog/2275743
  
https://my.oschina.net/feinik/blog/914309
  
http://aleung.blogbus.com/logs/32090434.html
  
http://wiki.jikexueyuan.com/project/java-concurrency/synchronized-and-volatile.html
>https://zhuanlan.zhihu.com/p/144740699
>https://cothee.github.io/programming/2019/07/30/memory-reording/