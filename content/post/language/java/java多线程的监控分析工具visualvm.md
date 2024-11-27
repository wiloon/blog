---
title: jvisualvm, JVM 监控分析工具(VisualVM)
author: "-"
date: 2015-11-04T02:02:03+00:00
url: /?p=8447
categories:
  - Inbox
tags:
  - reprint
---
## jvisualvm, JVM 监控分析工具(VisualVM)
Visual GC
  
GC time Time taken to perform garbage collection
  
Compile time Time spent in just-in-time (JIT) compilation

if visualvm can not find java
  
start visualvm with -jdkhome
  
visualvm.exe -jdkhome D:\java\jdk7

插件安装目录
  
C:\Users\user0\AppData\Roaming\VisualVM\8u131

在Java多线程程序运行时,多数情况下我们不知道到底发生了什么,只有出了错误的日志的时候,我们才知道原来代码中有死锁。撇开代码检查工具,我们先讨论一下利用VisualVM监控,分析我们的多线程的运行情况。 (注: 实践本文内容的JDK的版本需要1.6.07以上) 

什么是VisualVM

VisualVM是JDK的一个集成的分析工具,自从JDK 6 Update 7以后已经作为Sun的JDK的一部分。

VisualVM可以做的: 监控应用程序的性能和内存占用情况、监控应用程序的线程、进行线程转储(Thread Dump)或堆转储(Heap Dump)、跟踪内存泄漏、监控垃圾回收器、执行内存和CPU分析,保存快照以便脱机分析应用程序；同时它还支持在MBeans上进行浏览和操作。尽管 VisualVM自身要在JDK6以上的运行,但是JDK1.4以上版本的程序它都能被它监控。

在JDK1.6.07以上的版本中: 到$JAVA_HOME/bin,点击jvisualvm.exe图标就可以启动VisualVM；当然也可以点击这里获取官方的最新版本,支持: 英文,中文,日文。

VisualVM功能集成较多,我们这里只讨论它对象线程的监控分析。
  
VisualVM监控线程

当我们运行VisualVM的时候,可以在应用程序》本地中看到VisualVM和eclipse的运行程序,然后我们启动eclipse中的一个 线程: com.longtask.thread.TestVisualVm,可以看到在菜单中多了一个该线程的显示。点击右边的 线程 菜单,可以看到线程运行的跟踪情况。

点击 thread dump,可以生成该线程的运行情况的tdump文件,通过thread dump提供的相关信息,我们可以看到线程在什么地方被阻塞了以及线程的其他状态。

把日志另存为文件,到Thread Dump Analyzer的主页点击图标下载TDA,然后用TDA打开刚才VisualVM保存的 thread dump文件,查看相关的分析结果。

**远程监控**
  
我们也可以用VisualVM来监控远程java线程的运行情况。
  
启动RMI服务

1: 新建一个jstatd.all.policy文件,在里面添加以下内容来保证jstatd服务启动的时候不报异常: 

grant codebase "file:${java.home}/../lib/tools.jar" {
  
permission java.security.AllPermission;
  
};
  
2: netstat -ano | grep -i 1099 查看1099端口是否被占用了,如果被占用,则需要选择其他端口来启动jstatd服务

3: 如果端口被占用,用以下方式启动jstatd服务: 

rmiregistry 2020 & jstatd -J-Djava.security.policy=jstatd.all.policy -p 2020
  
更多jstatd的文档请参考sun公司的官方文档 这里
  
远程监控Jboos服务

1: 修改JDK下面的jmx的配置文件: 

切换至$JAVA_HOME所在目录/jre/lib/management下,

I: 将jmxremote.access、jmxremote.password.template权限调整为读写: 

grant codebase "file:${java.home}/../lib/tools.jar" {
  
permission java.security.AllPermission;
  
};
  
II: vi jmxremote.password去掉

# monitorRole QED

# controlRole R&D

的#号

2: 在Jboss的启动文件中添加以下信息: 

JAVA_OPTS="-Dcom.sun.management.jmxremote.port=2899 \
  
-Dcom.sun.management.jmxremote.ssl=false \
  
-Dcom.sun.management.jmxremote.authenticate=false \
  
-Djava.rmi.server.hostname=10.212.20.9  其他配置"
  
3: 检查启动情况: 

netstat -a | grep -i 2899 查看端口占有情况

如果2899端口被其他程序占用,在jboss配置文件中调整端口-Dcom.sun.management.jmxremote.port=\****

而后在VisualVM中就添加远程连接,选择jmx方式,就可以监控jboss的运行情况了。

参考文档: 
  
1: jstatd的帮助文档

2: VisualVM的帮助文档

3: Java VisualVM 的文档

4: JConsole的FAQ

5: Thread Dump Analyzer 帮助文档

YourKit Java Profiler
          
YourKit 是一个用于分析Java 与.NET 应用程序的智能工具,YourKit Java Profiler 已经被IT 专业人士与分析师公认为最好的分析工具。通过YourKit 技术解决方案可以以非常高的的专业水平分析出CPU 与内存使用情况。
          
YourKit Java Profiler 还获得了Java Developer's Journal(Java 开发者杂志)的编辑选择奖,其功能的强大可见一斑。
          
YourKit 网站官方: http://www.yourkit.com
          
YourKit Java Profiler 下载地址: http://www.yourkit.com/download/index.jsp
          
YourKit Java Profiler 提供了Java 与.NET 两种语言的支持,并且支持基本所有操作系统,目前最新版本为12.0.6。

### visualVM Thread state
  
Running: running/runnable
  
Sleeping: Thread.sleep()
  
Wait: wait/timed_wating
  
Park: LockSupport.park()
  
Monitor:Blocked

---

http://my.oschina.net/kone/blog/157239
  
https://visualvm.github.io/
  
https://visualvm.github.io/plugins.html

http://www.longtask.com/blog/?p=465

http://blog.csdn.net/fenglibing/article/details/17323515