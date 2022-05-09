---
title: jconsole
author: "-"
date: 2012-11-14T05:47:49+00:00
url: /?p=4670
categories:
  - Inbox
tags:
  - reprint
---
## jconsole
http://jiajun.iteye.com/blog/810150

一、JConsole是什么
      
从Java 5开始 引入了 JConsole。JConsole 是一个内置 Java 性能分析器，可以从命令行或在 GUI shell 中运行。您可以轻松地使用 JConsole (或者，它更高端的 "近亲" VisualVM ) 来监控 Java 应用程序性能和跟踪 Java 中的代码。
  
二、如何启动JConsole
  
如果是从命令行启动，使 JDK 在 PATH 上，运行 jconsole 即可。
  
如果从 GUI shell 启动，找到 JDK 安装路径，打开 bin 文件夹，双击 jconsole 。
      
当分析工具弹出时 (取决于正在运行的 Java 版本以及正在运行的 Java 程序数量) ，可能会出现一个对话框，要求输入一个进程的 URL 来连接，也可能列出许多不同的本地 Java 进程 (有时包含 JConsole 进程本身) 来连接。如图所示: 

想分析那个程序就双击那个进程。
  
三、如何设置JAVA程序运行时可以被JConsolse连接分析
  
本地程序 (相对于开启JConsole的计算机) ，无需设置任何参数就可以被本地开启的JConsole连接 (Java SE 6开始无需设置，之前还是需要设置运行时参数 -Dcom.sun.management.jmxremote ) 
  
无认证连接 (下面的设置表示: 连接的端口为8999、无需认证就可以被连接)
  
Java代码 收藏代码
  
-Dcom.sun.management.jmxremote.port=8999 \
  
-Dcom.sun.management.jmxremote.authenticate=false \
  
-Dcom.sun.management.jmxremote.ssl=false

如果考虑到安全因素，需要认证，需要安全连接，也是可以搞定的。参考: http://download.oracle.com/javase/6/docs/technotes/guides/management/agent.html#gdenv
  
四、JConsole如何连接远程机器的JAVA程序 (举例说明) 
  
1. 写一个简单的一直运行的JAVA程序，运行在某台机器上如(192.168.0.181)
  
Java代码 收藏代码
  
java -cp . -Dcom.sun.management.jmxremote.port=8999 -Dcom.sun.managent.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false JConsoleTest

2. 另外一台机器进行连接
  
可以直接使用命令: 
  
Java代码 收藏代码
  
jconsole.exe 192.168.0.181:8999
   
也可以在已经打开的JConsole界面操作 连接->新建连接->选择远程进程->输入远程主机IP和端口号->点击"连接"，如图: 

然后就会进入分析界面: 
  
性能分析
  
下面说说如何分析，如何使用这六个标签
  
概述: Displays overview information about the Java VM and monitored values.
  
内存: 显示内存使用信息
  
线程: 显示线程使用信息
  
类: 显示类装载信息
  
_VM摘要:_显示java VM信息
  
MBeans: 显示 MBeans.
  
概述

    概述很简单没啥说的，自己看看吧，不过值得一提的是对着图点击右键可以保存数据到CSV文件，以后可以使用其他工具来分析这些数据。
    

内存

    这个比较有价值，参看堆内存，非堆内存，内存池的状况总体内存的分配和使用情况以及不同的GC进行垃圾回收的次数和时间。可以手动进行GC查看内存变化。
    

在分析JAVA内存问题进行调优时候非常有用，你要学习JVM内存模型，之后会发现这里的每个值都具有意义。

GC的算法和参数对性能有显著的影响，注意垃圾回收次数、时间、以及partial GC和full GC，调整你所使用的不同GC和以及各个GC下的参数，然后在这个视图下观察，以得到好的性能。

这里贴一下 Java HotSpot VM garbage collector 下generational GC 的各代的划分图: 

关于GC，可以参考: http://www.oracle.com/technetwork/java/gc-tuning-5-138395.html
  
线程

    左下角显示所有的活动线程 (如果线程过多，可以在下面的过滤栏中输入字符串过滤出你想要观察的线程) 。点击某个显示会显示这个线程的名称、状态、阻塞和等待的次数、堆栈的信息。
    
    统计图显示的是线程数目的峰值 (红色) 和当前活动的线程 (蓝色) 。
    

另外下面有个按钮"检测到死锁"，有时候会有用处。
  
类

没啥要说的。
  
VM摘要

也没啥要说的，看看吧，内存状况，操作系统...
  
MBean

这里可以有一些额外的操作。
  
插件
  
Java代码 收藏代码
  
jconsole -pluginpath C:\Java\jdk1.6.0_22\demo\management\JTop\JTop.jar

一看便知，是个什么东西。
  
推荐使用升级版 JConsole 即 jvisualvm 。