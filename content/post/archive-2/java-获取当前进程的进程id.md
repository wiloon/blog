---
title: Java 获取 进程PID
author: "-"
date: 2017-03-30T06:49:26+00:00
url: /?p=9992
categories:
  - Uncategorized

tags:
  - reprint
---
## Java 获取 进程PID
```java
  
String name = ManagementFactory.getRuntimeMXBean().getName();
          
// get pid
          
String pid = name.split("@")[0];
          
logger.info("PID:{}", pid);
  
```

之前并不知道Java中如何能够获取当前进程 (也就是包含当前Java程序的JVM所在进程) 的进程ID,还以为要通过JNI或者通过Runtime.exec执行shell命令等方式才能获取到当前进程的进程ID,今天在偶然中看到一种在Java程序里,获取当前进程ID的方法,记录下来,以后应该会用到: ) 
  
首先,从JDK1.5之后,Java开始提供包: java.lang.management

java.lang.management 提供了一系列的用来在运行时管理和监督JVM和OS的管理接口。

今天我将用到的就是这个包中的一个类: ManagementFactory。

当然,这只是java.lang.management包中的一个小功能,该包还提供了很多其他的管理接口,参照java doc如下: 

Interface Summary
  
ClassLoadingMXBean
  
The management interface for the class loading system of the Java virtual machine.
  
CompilationMXBean
  
The management interface for the compilation system of the Java virtual machine.
  
GarbageCollectorMXBean
  
The management interface for the garbage collection of the Java virtual machine.
  
MemoryManagerMXBean
  
The management interface for a memory manager.
  
MemoryMXBean
  
The management interface for the memory system of the Java virtual machine.
  
MemoryPoolMXBean
  
The management interface for a memory pool.
  
OperatingSystemMXBean
  
The management interface for the operating system on which the Java virtual machine is running.
  
RuntimeMXBean
  
The management interface for the runtime system of the Java virtual machine.
  
ThreadMXBean
  
The management interface for the thread system of the Java virtual machine.

http://blog.csdn.net/derekjiang/article/details/7162415