---
title: jcmd
author: "-"
date: 2017-02-06T04:58:07+00:00
url: jcmd
categories:
  - Java
tags:
  - reprint
---
## jcmd

New Features in JDK7 update 4
  
JRockit command line utility JRCMD (JRockit Command). JRCMD was a command line tool to enumerate the Java processes running on the local machine, and to send commands (referred to as "Diagnostic Commands") to them. JRCMD has been renamed JCMD (Java Command).
  
jcmd用于向正在运行的JVM发送诊断信息请求,是从JDK1.7开始提供可以说是jstack和jps的结合体

```bash
#查看java进程, jcmd 不带参数时默认列出所有java进程。
jcmd [-l]

# help
jcmd PID help

# For more information about a specific command, 查看某一个命令的帮助信息。
jcmd PID help ManagementAgent.start

#打印线程栈
jcmd PID Thread.print

# 打印线程栈 + 锁信息
jcmd PID Thread.print -l

#打印 Thread.print 命令的帮助信息
kill -3 <PID> #仅限Linux平台
jstack <PID>

# jcmd提供了输出HPROF格式的堆dump接口。运行jcmd GC.heap_dump 即可。
# 注意这里的FILENAME是相对于运行中的jvm目录来说的,因此避免找不到dump的文件,这里推荐使用绝对路径。此外,也建议使用.hprof作为输出文件的扩展名。
# hprof文件分析工具: NetBeans, Elipse的MAT,jhat
jcmd PID GC.heap_dump /tmp/dump.hprof

# 打印出堆直方图(同时也打印出存活对象的数目)
jcmd <PID> GC.class_histogram

#启动参数
jcmd <PID> VM.command_line

#查看JVM参数, 如: -XX:MaxHeapSize, -XX:MaxNewSize
jcmd <PID> VM.flags

#uptime
jcmd <PID> VM.uptime

# 查看系统变量
jcmd <PID> VM.system_properties
```

jcmd [ pid | main-class ] command [ arguments ]

### JFR

JFR需要JDK的商业证书,需要解锁jdk的商业特性。
  
JFR.stop
  
JFR.start
  
JFR.dump
  
JFR.check

### NMT

VM.native_memory

### 解锁jdk的商业特性

VM.check_commercial_features
  
VM.unlock_commercial_features
  
https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr007.html

### JMX

<http://blog.wiloon.com/?p=9748>
  
ManagementAgent.stop
  
ManagementAgent.start_local
  
ManagementAgent.start

### rotate GC log

GC.rotate_log

#类元数据大小的详细信息。使用这个功能启动程序时需要加上-XX:+UnlockDiagnosticVMOptions选项。
  
#Provide statistics about Java class meta data. Requires -XX:+UnlockDiagnosticVMOptions.
  
GC.class_stats

#查看系统中类统计信息,类型的存活对象数目。 jmap -histo:live <PID>,这里的以byte为单位的占用大小是浅尺寸(shallow size),并没有包括子对象的大小。
  
GC.class_histogram

#Generate a HPROF format dump of the Java heap,jmap dump
  
GC.heap_dump

#Call java.lang.System.runFinalization()
  
#强制调用已经失去引用的对象的finalize方法
  
GC.run_finalization

#Call java.lang.System.gc()
  
#告诉垃圾收集器打算进行垃圾收集,而垃圾收集器进不进行收集是不确定的

GC.run

#系统变量
  
VM.system_properties

#版本信息
  
VM.version

http://qkxue.net/info/188931/jcmd-jmc
  
http://qifuguang.me/2015/08/01/%5BJDK%E5%B7%A5%E5%85%B7%E5%AD%A6%E4%B9%A0%E4%B8%83%5Djcmd%E5%91%BD%E4%BB%A4%E4%BD%BF%E7%94%A8/
  
http://0opslab.com/2016/01/19/JDK%E5%91%BD%E4%BB%A4jcmd/
  
https://segmentfault.com/a/1190000007518014
  
<http://hirt.se/blog/?p=211>
  
http://www.rowkey.me/blog/2016/11/16/java-trouble-shooting/
  
http://0opslab.com/2016/01/19/JDK%E5%91%BD%E4%BB%A4jcmd/
  
http://www.rowkey.me/blog/2016/11/16/java-trouble-shooting/