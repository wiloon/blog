---
title: Runtime
author: "-"
date: 2015-06-01T13:40:03+00:00
url: /?p=7740
categories:
  - Inbox
tags:
  - Java

---
## Runtime

<http://blog.csdn.net/csh624366188/article/details/6684327>

<http://lavasoft.blog.51cto.com/62575/15565>

Runtime.getRuntime()可以取得当前JVM的运行时环境,这也是在Java中唯一一个得到运行时环境的方法。

2. Runtime上其他大部分的方法都是实例方法,也就是说每次进行运行时调用时都要用到getRuntime方法。

3. Runtime中的exit方法是退出当前JVM的方法,估计也是唯一的一个吧,因为我看到System类中的exit实际上也是通过调用Runtime.exit()来退出JVM的,这里说明一下Java对Runtime返回值的一般规则 (后边也提到了) ,0代表正常退出,非0代表异常中止,这只是Java的规则,在各个操作系统中总会发生一些小的混淆。
  
4. Runtime.addShutdownHook()方法可以注册一个hook在JVM执行shutdown的过程中,方法的参数只要是一个初始化过但是没有执行的Thread实例就可以。 (注意,Java中的Thread都是执行过了就不值钱的哦)

5. 说到addShutdownHook这个方法就要说一下JVM运行环境是在什么情况下shutdown或者abort的。文档上是这样写的,当最后一个非精灵进程退出或者收到了一个用户中断信号、用户登出、系统shutdown、Runtime的exit方法被调用时JVM会启动shutdown的过程,在这个过程开始后,他会并行启动所有登记的shutdown hook (注意是并行启动,这就需要线程安全和防止死锁) 。当shutdown过程启动后,只有通过调用halt方法才能中止shutdown的过程并退出JVM。

那什么时候JVM会abort退出那？首先说明一下,abort退出时JVM就是停止运行但并不一定进行shutdown。这只有JVM在遇到SIGKILL信号或者windows中止进程的信号、本地方法发生类似于访问非法地址一类的内部错误时会出现。这种情况下并不能保证shutdown hook是否被执行。

常见的应用

1. 内存管理:
  
Java提供了无用单元自动收集机制。通过totalMemory()和freeMemory()方法可以知道对象的堆内存有多大,还剩多少。
  
Java会周期性的回收垃圾对象 (未使用的对象) ,以便释放内存空间。但是如果想先于收集器的下一次指定周期来收集废弃的对象,可以通过调用gc()方法来根据需要运行无用单元收集器。一个很好的试验方法是先调用gc()方法,然后调用freeMemory()方法来查看基本的内存使用情况,接着执行代码,然后再次调用freeMemory()方法看看分配了多少内存。下面的程序演示了这个构想。
  
//此实例来自《java核心技术》卷一

class MemoryDemo{
  
public static void main(String args[]){
  
Runtime r = Runtime.getRuntime();
  
long mem1,mem2;
  
Integer someints[] = new Integer[1000];
  
System.out.println("Total memory is : " + r.totalMemory());
  
mem1 = r.freeMemory();
  
System.out.println("Initial free is : " + mem1);
  
r.gc();
  
mem1 = r.freeMemory();
  
System.out.println("Free memory after garbage collection : " + mem1);
  
//allocate integers
  
for(int i=0; i<1000; i++) someints[i] = new Integer(i);
  
mem2 = r.freeMemory();
  
System.out.println("Free memory after allocation : " + mem2);
  
System.out.println("Memory used by allocation : " +(mem1-mem2));
  
//discard Intergers
  
for(int i=0; i<1000; i++) someints[i] = null;
  
r.gc(); //request garbage collection
  
mem2 = r.freeMemory();
  
System.out.println("Free memory after collecting " + "discarded integers : " + mem2);
  
}
  
}

编译后运行结果如下 (不同的机器不同时间运行的结果也不一定一样) :
  
Total memory is : 2031616
  
Initial free is : 1818488
  
Free memory after garbage collection : 1888808
  
Free memory after allocation : 1872224
  
Memory used by allocation : 16584
  
Free memory after collecting discarded integers : 1888808
  
2. 执行其他程序
  
在安全的环境中,可以在多任务操作系统中使用Java去执行其他特别大的进程 (也就是程序) 。ecec()方法有几种形式命名想要运行的程序和它的输入参数。ecec()方法返回一个Process对象,可以使用这个对象控制Java程序与新运行的进程进行交互。ecec()方法本质是依赖于环境。
  
下面的例子是使用ecec()方法启动windows的记事本notepad。这个例子必须在Windows操作系统上运行。
  
//此实例来自《Java核心技术》卷一
  
class ExecDemo {
  
public static void main(String args[]){
  
Runtime r = Runtime.getRuntime();
  
Process p = null;
  
try{
  
p = r.exec("notepad");
  
} catch (Exception e) {
  
System.out.println("Error executing notepad.");
  
}
  
}
  
}
  
ecec()还有其他几种形式,例子中演示的是最常用的一种。ecec()方法返回Process对象后,在新程序开始运行后就可以使用Process的方法了。可以用destory()方法杀死子进程,也可以使用waitFor()方法等待程序直到子程序结束,exitValue()方法返回子进程结束时返回的值。如果没有错误,将返回0,否则返回非0。下面是关于ecec()方法的例子的改进版本。例子被修改为等待,直到运行的进程退出:
  
//此实例来自《Java核心技术》卷一
  
class ExecDemoFini {
  
public static void main(String args[]){
  
Runtime r = Runtime.getRuntime();
  
Process p = null;
  
try{
  
p = r.exec("notepad");
  
p.waitFor();
  
} catch (Exception e) {
  
System.out.println("Error executing notepad.");
  
}
  
System.out.println("Notepad returned " + p.exitValue());
  
}
  
}
  
下面是运行的结果 (当关闭记事本后,会接着运行程序,打印信息) :
  
Notepad returned 0
  
请按任意键继续. . .
  
当子进程正在运行时,可以对标准输入输出进行读写。getOutputStream()方法和getInPutStream()方法返回对子进程的标准输入和输出。
