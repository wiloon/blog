---
author: "-"
date: "2021-04-18 11:33:40" 
title: "写时复制 (Copy-on-write: COW) "

categories:
  - inbox
tags:
  - reprint
---
## "写时复制 (Copy-on-write: COW) "


写入时复制 (英语: Copy-on-write，简称COW) 是一种计算机程序设计领域的优化策略。其核心思想是，如果有多个调用者 (callers) 同时请求相同资源 (如内存或磁盘上的数据存储) ，他们会共同获取相同的指针指向相同的资源，直到某个调用者试图修改资源的内容时，系统才会真正复制一份专用副本 (private copy) 给该调用者，而其他调用者所见到的最初的资源仍然保持不变。这过程对其他的调用者都是透明的 (transparently) 。此作法主要的优点是如果调用者没有修改该资源，就不会有副本 (private copy) 被创建，因此多个调用者只是读取操作时可以共享同一份资源。

在java中的应用举例
 

java中有两个类: CopyOnWriteArrayList、CopyOnWriteArraySet使用了写时复制技术手段，CopyOnWriteArrayList的实现: 

A thread-safe variant of java.util.ArrayList in which all mutative operations (add, set, and so on) are implemented by making a fresh copy of the underlying array.

在多线程环境，凡是读操作都没有进行加锁操作，而写操作都会在锁的保护下复制一份数据，在复制的数据上做修改，修改完后，再把底层数组的引用指向修改后的新数组。

复制数据意味着需要浪费内存空间，所以在读

写少的并发场景下比较合适。

 /**
     * The lock protecting all mutators.  (We have a mild preference
     * for builtin monitors over ReentrantLock when either will do.)
     */
    final transient Object lock = new Object();
 
    /** The array, accessed only via getArray/setArray. */
    private transient volatile Object[] array;
所有的修改操作都会使用lock对象内置的锁得以并发安全修改。Object[] array用volatile修饰，保证内存可见性就可以。

 

Linux系统创建新进程
 

unix操作系统中有两种创建新进程的几种，分别是fork和exec。

 (1) fork可以创建当前进程的一个副本，父进程和子进程只有PID不同。在该系统调用执行之后，系统中有两个进程，都执行同样的操作。父进程内存的内容将被复制，至少从程序的角度来看是这样。 Linux 使用了一种写时复制技术来使 fork 操作更高效， 主要的原理是将内存复制操作延迟到父进程或子进程向某内存页面写入数据之前， 在只读访问的情况下父进程和子进程可以共用同一个内存页。

 (2) exec将一个新程序加载到当前进程的内存中并执行。旧程序的内存页将刷出，其内容将替换为新的数据。然后执行新程序。

 

当然还有很多使用了写时复制优化性能的地方

 

参考: 

https://unix.stackexchange.com/questions/58145/how-does-copy-on-write-in-fork-handle-multiple-fork

https://stackoverflow.com/questions/628938/what-is-copy-on-write

https://wikipedia.hk.wjbk.site/wiki/寫入時複製

http://ifeve.com/java-copy-on-write/

https://hackerboss.com/i-have-seen-the-future-and-it-is-copy-on-write/

https://hackerboss.com/copy-on-write-101-part-1-what-is-it/

深入Linux内核架构.pdf
————————————————
版权声明: 本文为CSDN博主「A_Beaver」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/doctor_who2004/article/details/103551335


vfork(): 这个做法更加火爆，内核连子进程的虚拟地址空间结构也不创建了，直接共享了父进程的虚拟空间，当然了，这种做法就顺水推舟的共享了父进程的物理空间

---

https://blog.csdn.net/doctor_who2004/article/details/103551335  
https://www.cnblogs.com/biyeymyhjob/archive/2012/07/20/2601655.html  
