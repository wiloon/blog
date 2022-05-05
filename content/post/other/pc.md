---
title: 程序计数器, The Program Counter, PC
author: "-"
date: 2013-09-27T05:25:40+00:00
url: /?p=5826

categories:
  - inbox
tags:
  - reprint
---
## 程序计数器, The Program Counter, PC

program counter (PC) 一般也被叫做 instruction pointer (IP), 在intel x86 cpu里有时候也被叫做 instruction address register (IAR), instruction counter, 或者是 instruction sequencer 的一部分,

### 程序计数器

程序计数器是用于存放执行指令的地方。

为了保证程序(在操作系统中理解为进程)能够连续地执行下去,CPU必须具有某些手段来确定下一条指令的地址。而程序计数器正是起到这种作用,所以通常又称为指令计数器。

在程序开始执行前,必须将它的起始地址,即程序的一条指令所在的内存单元地址送入PC,因此程序计数器 (PC) 的内容即是从内存提取的第一条指令的地址。当执行指令时,CPU将自动修改PC的内容,即每执行一条指令PC增加一个量,这个量等于指令所含的字节数,以便使其保持的总是将要执行的下一条指令的地址。由于大多数指令都是按顺序来执行的,所以修改的过程通常只是简单的对PC加1。

当程序转移时,转移指令执行的最终结果就是要改变PC的值,此PC值就是转去的地址,以此实现转移。有些机器中也称PC为指令指针IP (Instruction Pointer) 。

程序计数器 (Program Counter Register) 是一块较小的内存空间,它的作用可以看做是当前线程所执行的字节码的行号指示器。在虚拟机的概念模型里 (仅是概念模型,各种虚拟机可能会通过一些更高效的方式去实现) ,字节码解释器工作时就是通过改变这个计数器的值来选取下一条需要执行的字节码指令,分支、循环、跳转、异常处理、线程恢复等基础功能都需要依赖这个计数器来完成。
由于Java虚拟机的多线程是通过线程轮流切换并分配处理器执行时间的方式来实现的,在任何一个确定的时刻,一个处理器 (对于多核处理器来说是一个内核) 只会执行一条线程中的指令。因此,为了线程切换后能恢复到正确的执行位置,每条线程都需要有一个独立的程序计数器,各条线程之间的计数器互不影响,独立存储,我们称这类内存区域为"线程私有"的内存
如果线程正在执行的是一个Java方法,这个计数器记录的是正在执行的虚拟机字节码指令的地址；如果正在执行的是Natvie方法,这个计数器值则为空 (Undefined) 。此内存区域是唯一一个在Java虚拟机规范中没有规定任何OutOfMemoryError情况的区域。

以上描述截取自:

《深入理解Java虚拟机:JVM高级特性与最佳实践》 作者:  周志明

Each thread of a running program has its own pc register, or program counter, which is created when the thread is started. The pc register is one word in size, so it can hold both a native pointer and a returnValue. As a thread executes a Java method, the pc register contains the address of the current instruction being executed by the thread. An "address" can be a native pointer or an offset from the beginning of a method's bytecodes. If a thread is executing a native method, the value of the pc register is undefined.
  
对于一个运行中的Java程序而言,其中的每一个线程都有它自己的PC (程序计数器) ,在线程启动时创建。大小是一个字长。因此它既能持有一个本地指针,也能够持有一个returnAddress。当线程执行某个Java方法时,PC的内容总是下一条将被指向指令的"地址"。这里的"地址"可以是一个本地指针,也可以是在方法字节码中相对于该方法起始指令的偏移量。如果该线程正在执行一个本地方法,那么此时PC寄存器的值为"undefined"。

以上描述截取自:
  
《Inside the Java Virtual Machine 2nd Edition》 作者: Bill Venners

<http://denverj.iteye.com/blog/1218120>

版权声明: 本文为CSDN博主「Rachel-Zhang」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/abcjennifer/article/details/5529647>

><https://en.wikipedia.org/wiki/Program_counter>
