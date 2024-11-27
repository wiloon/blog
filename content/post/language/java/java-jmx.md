---
title: java jmx
author: "-"
date: 2017-02-07T07:24:12+00:00
url: /?p=9748
categories:
  - Inbox
tags:
  - reprint
---
## java jmx
在 Java 程序的运行过程中,对 JVM 和系统的监测一直是 Java 开发人员在开发过程所需要的。一直以来,Java 开发人员必须通过一些底层的 JVM API,比如 JVMPI 和 JVMTI 等,才能监测 Java 程序运行过程中的 JVM 和系统的一系列情况,这种方式一直以来被人所诟病,因为这需要大量的 C 程序和 JNI 调用,开发效率十分低下。于是出现了各种不同的专门做资源管理的程序包。为了解决这个问题,Sun 公司也在其 Java SE 5 版本中,正式提出了 Java 管理扩展 (Java Management Extensions,JMX) 用来管理检测 Java 程序 (同时 JMX 也在 J2EE 1.4 中被发布) 。
  
JMX 的提出,让 JDK 中开发自检测程序成为可能,也提供了大量轻量级的检测 JVM 和运行中对象 / 线程的方式,从而提高了 Java 语言自己的管理监测能力。

开启JMX,用 JVisvualVM, jmc 或 jconsole 连接JVM
  
oracle jdk 自带JVisvualVM, jmc, openjdk 只有jconsole

### 通过jcmd开启 - 不需要重启JVM:

```bash
# jmxremote.rmi.port: 监听jmx客户端的端口
# jmxremote.rmi.port: jmx数据传输端口,如果此项未配置,jmx会随机开一个新端口跟客户端传输数据.
jcmd <PID> ManagementAgent.start \
jmxremote.port=1099 \
jmxremote.rmi.port=1099 \
jmxremote.ssl=false \
jmxremote.authenticate=false
```

### 关闭jmx

```bash
jcmd <PID> ManagementAgent.stop
```

### 通过JVM启动参数开启,需要重启JVM.

```bash
# JVM command line option:
-Dcom.sun.management.jmxremote.port=1099
-Dcom.sun.management.jmxremote.rmi.port=1099
-Dcom.sun.management.jmxremote.ssl=false
-Dcom.sun.management.jmxremote.authenticate=false
-Djava.rmi.server.hostname=192.168.1.54
```

注: 
  
1. -Dcom.sun.management.jmxremote.port: 这个是配置远程 connection 的端口号的,要确定这个端口没有被占用
  
2. -Dcom.sun.management.jmxremote.ssl=false 指定了 JMX 是否启用 ssl
  
3. -Dcom.sun.management.jmxremote.authenticate=false   指定了JMX 是否启用鉴权 (需要用户名,密码鉴权) 
  
4. -Djava.rmi.server.hostname : 这个是配置 server 的 IP 的

http://www.cnblogs.com/princessd8251/p/4374882.html
  
https://github.com/springside/springside4/wiki/Jmx
  
https://www.ibm.com/developerworks/cn/java/j-lo-jse63/
  
http://tuhaitao.iteye.com/blog/786391
  
http://docs.oracle.com/javase/8/docs/technotes/guides/management/agent.html