---
title: System.gc(), System.runFinalization()
author: "-"
date: 2017-06-02T05:29:15+00:00
url: /?p=10456
categories:
  - Inbox
tags:
  - reprint
---
## System.gc(), System.runFinalization()
System.gc:
  
告诉垃圾收集器打算进行垃圾收集,而垃圾收集器进不进行收集是不确定的。只是建议进行回收。
  
jvm有自己的gc策略,不建议手动调用。
  
system.gc其实是做一次full gc
  
system.gc会暂停整个进程
  
system.gc一般情况下我们要禁掉,使用-XX:+DisableExplicitGC
  
system.gc在cms gc下我们通过-XX:+ExplicitGCInvokesConcurrent来做一次稍微高效点的GC(效果比Full GC要好些)
  
system.gc最常见的场景是RMI/NIO下的堆外内存分配等

System.runFinalization()
  
Runs the finalization methods of any objects pending finalization.
  
Calling this method suggests that the Java Virtual Machine expend effort toward running the finalize methods of objects that have been found to be discarded but whose finalize methods have not yet been run. When control returns from the method call, the Java Virtual Machine has made a best effort to complete all outstanding finalizations.

The call System.runFinalization() is effectively equivalent to the call:
  
Runtime.getRuntime().runFinalization()

注意是suggest that 同gc一样都是建议JVM。 所以JVM可以选择执行或者不执行

java中的finalize()方法
  
当垃圾收集器认为没有指向对象实例的引用时,会在销毁该对象之前调用finalize()方法。该方法最常见的作用是确保释放实例占用的全部资源。java并不保证定时为对象实例调用该方法,甚至不保证方法会被调用,所以该方法不应该用于正常内存处理。

http://www.weyye.me/detail/System-gc-not-called/
  
http://blog.csdn.net/nyistzp/article/details/12253599
  
http://www.cnblogs.com/E-star/p/3423811.html
  
http://lovestblog.cn/blog/2015/05/07/system-gc/