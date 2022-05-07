---
title: OutOfMemoryError, StackOverflowError
author: "-"
date: 2014-04-09T06:35:46+00:00
url: /?p=6499
categories:
  - Inbox
tags:
  - Java

---
## OutOfMemoryError, StackOverflowError
这是IGT笔试的题目，分别写出可以造成两种错误的代码。由于之前测试过HashMap的容量的时候出现过内存不足的错误，所以能写出来，但StackOverflowError没什么印象了。

回来查了下StackOverflowError的资料，在德问社区上有人发帖子java产生StackOverflowError的原因是什么?询问: 

请问java.lang.StackOverflowError产生的原因有什么?

已知的有死循环,循环的嵌套层数达到了环境的设定值

谢谢

有人回复说: 

死循环本身是不会StackOverflow的，只有无限递归的时候会出现。原则上循环嵌套次数本身是没有限制的，限制的是占用的栈空间，如果你的函数里定义了很多很多变量，栈空间就会用完得比较快。

还有人讲的更详细: 

JVM里会有两种StackOverflowError, 一种是对应JVM stack, 一种是对应Native Method stack. 我们一般说的都是JVM stack.

每一个JVM线程维护自己的JVM stack. JVM stack里面存放 JVM栈帧. 栈帧中存放 数据和中间结果(本地变量数组, 操作符栈, 和对runtime 常量池的引用). 这些数据都比较小(对象都在堆中, 栈帧仅存放对象引用), 所以想单纯通过 在栈帧中存放大数据的方法 去引入StackOverflowError, 基本是不现实的.一般都是因为方法调用嵌套层数过大.

http://docs.oracle.com/javase/specs/jvms/se7/html/jvms-2.html#jvms-2.5.2

JVM stack的大小是可以调节的, sun的windows jvm6 x64,jvm栈默认大小为1024k.可以通过-Xss1024k来调节. http://www.oracle.com/technetwork/java/hotspotfaq-138619.html#threads_oom

另外，在oracle的docsChapter 2. The Structure of the Java Virtual Machine中，有如下解释: 

Java Virtual Machine Stacks
  
The following exceptional conditions are associated with Java Virtual Machine stacks:

If the computation in a thread requires a larger Java Virtual Machine stack than is permitted, the Java Virtual Machine throws a StackOverflowError.

If Java Virtual Machine stacks can be dynamically expanded, and expansion is attempted but insufficient memory can be made available to effect the expansion, or if insufficient memory can be made available to create the initial Java Virtual Machine stack for a new thread, the Java Virtual Machine throws an OutOfMemoryError.

Heap
  
The following exceptional condition is associated with the heap:

If a computation requires more heap than can be made available by the automatic storage management system, the Java Virtual Machine throws an OutOfMemoryError.
  
也就是说，对于堆栈stack(或heap)来说，如果线程需要的空间大于允许值，则为StackOverflowError；如果stack空间可以动态增加，但最后内存还是不够，则为OutOfMemoryError。

我写了下无限递归代码进行测试: 

public static void main(String[] argv){
      
int i = getInt(2);

}

public static int getInt(int i){
      
return getInt(i++);
  
}
  
跑完之后，结果如下: 

Exception in thread "main" java.lang.StackOverflowError
  
确实如此。

另外，也顺便又测了一下内存溢出的错误，代码如下: 

public static void main(String[] argv){
      
HashMap<Integer, Integer> map = new HashMap<Integer,Integer>();
      
for(int i=0;i<Integer.MAX_VALUE;i++){
          
map.put(i, i);
      
}
  
}
  
输出结果为: 

Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
  
和预期一致

当Java程序申请内存，超出VM可分配内存的时候，VM首先可能会GC，如果GC完还是不够，或者申请的直接超过VM可能有的，就会抛出内存溢出异常。从VM规范中我们可以得到，一下几种异常。

java.lang.StackOverflowError: (很少) 
  
java.lang.OutOfMemoryError: heap space(比较常见)
  
java.lang.OutOfMemoryError: PermGen space (经常出现)
  
java.lang.OutOfMemoryError: GC overhead limit exceeded (某项操作使用大量内存时发生) 

以下分别解释一下，从最常见的开始: 
  
java.lang.OutOfMemoryError: PermGen space 这个异常比较常见，是说ＪＶＭ里的Perm内存区的异常溢出，由于JVM在默认的情况下，Perm默认为64M，而很多程序需要大量的Perm区内 存，尤其使用到像Spring等框架的时候，由于需要使用到动态生成类，而这些类不能被GC自动释放，所以导致OutOfMemoryError: PermGen space异常。解决方法很简单，增大JVM的 -XX:MaxPermSize 启动参数，就可以解决这个问题，如过使用的是默认变量通常是64M[5.0 and newer: 64 bit VMs are scaled 30% larger; 1.4 amd64: 96m; 1.3.1 -client: 32m.]，改成128M就可以了，-XX:MaxPermSize=128m。如果已经是128m (Eclipse已经是128m了) ，就改成 256m。我一般在服务器上为安全起见，改成256m。

java.lang.OutOfMemoryError: heap space或 其它OutOfMemoryError，这个异常实际上跟上面的异常是一个异常，但解决方法不同，所以分开来写。上面那个异常是因为JVM的perm区内 存区分少了引起的 (JVM的内 存区分为 young,old,perm三种) 。而这个异常是因为JVM堆内 存或者说总体分少了。解决方法是更改 -Xms -Xmx 启动参数，通常是扩大1倍。xms是管理启动时最小内 存量的，xmx是管里JVM最大的内 存量的。

注: OutOfMemoryError可能有很多种原因，根据JVM Specification, 可能有一下几种情况，我先简单列出。stack: stack分区不能动态扩展，或不足以生成新的线程。Heap:需要更多的内 存，而不能获得。Method Area :如果不能满足分配需求。runtime constant pool(从Method Area分配内 存)不足以创建class or interface。native method stacks不能够动态扩展，或生成新的本地线程。

java.lang.OutOfMemoryError: GC overhead limit exceeded，这个是JDK6新添的错误类型。是发生在GC占用大量时间为释放很小空间的时候发生的，是一种保护机制。我在JSP导大Excel的时候碰到过。最终解决方案是，关闭该功能，使用—— -XX:-UseGCOverheadLimit

最后说说java.lang.StackOverflowError，老实说这个异常我也没碰见过，但JVM Specification就提一下，规范上说有一下几种境况可能抛出这个异常，一个是Stacks里的线程超过允许的时候，另一个是当native method要求更大的内 存，而超过native method允许的内 存的时候。根据SUN的文档，提高-XX:ThreadStackSize=512的值。

总的来说调优JVM的内 存，组要目的就是在使用内 存尽可能小的，使程序运行正常，不抛出内 纯溢出的bug。而且要调好最小内 存，最大内 存的比，避免GC时浪费太多时间，尤其是要尽量避免FULL GC。

补充: 由于JDK1.4新增了nio，而nio的buffer分配内存比较特殊 (读写流可以共享内存) 。如果有大量数据交互，也可能导致java.lang.OutOfMemoryError。相应的JDK新增了一个特殊的参数: -XX:MaxDirectMemorySize 默认是64M，可以改大些如128M。

-XX:MaxDirectMemorySize=<size>

Specifies the maximum amount of memory in bytes that the Java NIO library can allocate for direct memory buffers. The default is 64 megabytes, which corresponds to

-XX:MaxDirectMemorySize=64m . The use of direct memory buffers can minimize the copying cost when doing IO operations.

http://arthur503.github.io/blog/2013/10/10/Java-OutOfMemoryError-and-StackOverflowError.html

http://java.sun.com/javase/technologies/hotspot/gc/gc_tuning_6.html#par_gc.oom

http://java.sun.com/docs/books/jvms/second_edition/html/Overview.doc.html

http://java.sun.com/j2se/1.5.0/docs/tooldocs/windows/java.html

http://java.sun.com/javase/technologies/hotspot/vmoptions.jsp
  
http://java-boy.iteye.com/blog/463454