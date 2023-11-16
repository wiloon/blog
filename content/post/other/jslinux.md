---
title: jstatd
author: "-"
date: 2013-02-21T10:39:39+00:00
url: /?p=5221
categories:
  - Linux
tags:
  - reprint
---
## jstatd

jstatd 是一个基于RMI (Remove Method Invocation) 的服务程序，它用于监控基于HotSpot的JVM中资源的创建及销毁，并且提供了一个远程接口允许远程的监控工具连接到本地的JVM执行命令。
jstatd是基于RMI的，所以在运行jstatd的服务器上必须存在RMI注册中心，如果没有通过选项"-p port"指定要连接的端口，jstatd会尝试连接RMI注册中心的默认端口。后面会谈到如何连接到一个默认的RMI内部注册中心，如何禁止默认的RMI内部注册中心的创建，以及如何启动一个外部注册中心。

2. 参数选项

jstatd 命令支持如下的选项:

-nr 如果RMI注册中心没有找到，不会创建一个内部的RMI注册中心。

-p port RMI注册中心的端口号，默认为1099。

-n rminame 默认为JStatRemoteHost；如果同一台主机上同时运行了多个jstatd服务，rminame可以用于唯一确定一个jstatd服务；这里需要注意一下，如果开启了这个选项，那么监控客户端远程连接时，必须同时指定hostid及vmid，才可以唯一确定要连接的服务，这个可以参看jps章节中列出远程服务器上Java进程的示例。

-J 用于传递jvm选项到由javac调用的java加载器中，例如，"-J-Xms48m"将把启动内存设置为48M，使用-J选项可以非常方便的向基于Java的开发的底层虚拟机应用程序传递参数。

3. 安全性

jstatd 服务只能监视具有适当的本地访问权限的JVM，因此jstatd进程与被监控的JVM必须运行在相同的用户权限中。但是有一些特殊的用户权限，如基于UNIX (TM) 为系统的root用户，它有权限访问系统中所有JVM的资源，如果jstatd进程运行在这种权限中，那么它可以监视系统中的所有JVM，但是这也带来了额外的安全问题。

jstatd 服务不会对客户端进行任何的验证，因此运行了jstatd服务的JVMs，网络上的任何用户的都具有访问权限，这种暴露不是我们所希望的，因此在启动jstatd之前本地安全策略必须要加以考虑，特别是在生产环境中或者是在不安全的网络环境中。

如果没有其他安全管理器被安装，jstatd服务将会安装一个RMISecurityPolicy的实例，因此需要在一个安全策略文件中指定，该策略文件必须符合的默认策略实施的策略文件语法。

下面的这个示例策略将允许jstatd服务具有JVM全部的访问权限:

grant codebase "file:${java.home}/../lib/tools.jar" {

permission java.security.AllPermission;
  
};
  
```

    注: 此处策略中的java.home，和JAVA_HOME不是一个概念，童鞋们不要搞错了，此处的java.home指的是JRE的路径，
    

这个是Java的系统属性，不需要手工指定，通常是这个jdk下面的jre路径,即可以认为${java.home}和${JAVA_HOME}/jre是等价，
  
如果想查看这个变量的值，可以任意找一个运行着的Java应用，找到它的PID，然后通过如下jinfo命令查看就可以查看到java.home的值

jinfo ${PID}|grep java.home
      
也可以在Java代码中通过如下方式获取到: 

System.out.println(System.getProperty("java.home"))

    将上面的策略内容拷贝一个文件中，文件名可以随意取，为了形象我们将文件名命名为jstatd.all.policy，文件存放的路径也可以随意，只有你当前登陆的用户具有访问权限就可以，然后执行以下命令就可以启动jstatd服务: 
    

```bash
  
jstatd -J-Djava.security.policy=jstatd.all.policy
  
```

    如果是在具有安全限制的环境中，jstatd的策略安全一定要设置得当，并且只允许受信任的服务器或者网络访问，以免遭受网络攻击，如果存在安全隐患，最好不要启动jstatd服务，就在本地使用jstat及jps等工具对JVM进行监控了。

1. 示例
  
4.1、使用内部RMI注册中心

下面这个示例演示了通过内部RMI注册中心启动jstatd，这个示例假设没有其它的服务绑定到默认的RMI注册中心端口 (默认端口是1099) 。

jstatd -J-Djava.security.policy=jstatd.all.policy

注: 如果基于默认端口1099的RMI注册中心原来没有被启动过，那么上面运行的命令首先会启动端口为1099的RMI注册中心，然后再启动jstatd服务，此时即使jstatd停止了，RMI注册中心也不会停止；如果是再次执行上面的命令，就不会再次启动RMI注册中心，jstatd会直接注册到注册中心。

4.2、使用外部的RMI注册中心

这个示例演示了使用一个外部的RMI注册中心来启动jstatd，如果默认的内部注册中心已经被启动了，下面的这个示例就会抛出"端口1099已经被占用"的异常，因为它尝试在1099端口启动外部RMI注册中心:

rmiregistry&jstatd -J-Djava.security.policy=all.policy

这个示例演示了使用一个外部的RMI注册中心来启动jstatd，此注册中心的端口为2020:

rmiregistry 2020&jstatd -J-Djava.security.policy=all.policy -p 2020

这个示例演示了使用一个外部的RMI注册中心来启动jstatd，此注册中心的端口为2020，并且绑定到RMI注册中心的名为AlternateJstatdServerName:

rmiregistry 2020&jstatd -J-Djava.security.policy=all.policy -p 2020 -n AlternateJstatdServerName

注: 这个端口为2020的RMI注册中心，我们会在jps章节中使用到。

4.3、禁止内部RMI注册中心的创建

这个示例演示了jstatd在启动的时候，如果没有找到默认的RMI注册中心，也不会创建默认的注册中心。这个示例中如果没有RMI注册中心在运行，此示例就会报错，如果存在就会正常运行:

jstatd -J-Djava.security.policy=all.policy -nr

4.4、开启RMI日记记录

这个示例演示的是jstatd运行在开启了日志记录功能的RMI注册中，这个对于问题查找或监控服务状态非常有用:

jstatd -J-Djava.security.policy=all.policy -J-Djava.rmi.server.logCalls=true

jstatd vs. JMX
  
jstatd

jstatd is a daemon that is distributed with JDK. You start it from the command line (it's likely necessary to run it as the user running the target JVM or as root) on the target machine and VisualVM will contact it to fetch information about the remote JVMs.

Advantages: Can connect to a running JVM, no need to start it with special parameters
  
Disadvantages: Much more limited monitoring capabilities (f.ex. no CPU usage monitoring, not possible to run the Sampler and/or take thread dumps).

JMX
  
Advantages: Using JMX will give you the full power of VisualVM.
  
You will generally want to use something like the following properties when starting the target JVM (though you could also enable SSL and/or require username and password):

[http://blog.csdn.net/fenglibing/article/details/17323515](http://blog.csdn.net/fenglibing/article/details/17323515)
  
[https://docs.oracle.com/javase/8/docs/technotes/tools/unix/jstatd.html](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/jstatd.html)
  
[https://theholyjava.wordpress.com/2012/09/21/visualvm-monitoring-remote-jvm-over-ssh-jmx-or-not/](https://theholyjava.wordpress.com/2012/09/21/visualvm-monitoring-remote-jvm-over-ssh-jmx-or-not/)
