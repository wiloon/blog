---
title: jdk tool, java tool, jvm tool
author: "-"
date: 2017-02-06T00:31:53+00:00
url: /?p=9713
categories:
  - Uncategorized

tags:
  - reprint
---
## jdk tool, java tool, jvm tool
### jcmd
Java 命令行(Java Command),用于向正在运行的JVM发送诊断命令请求。

### jmc
Java任务控制工具(Java Mission Control),主要用于HotSpot JVM的生产时间监测、分析、诊断。
  
<https://blog.wiloon.com/?p=9724>

### java
Java运行工具,用于运行.class字节码文件或.jar文件。

### javac
Java编译工具(Java Compiler),用于编译Java源代码文件。

### jconsole
图形化用户界面的监测工具,主要用于监测并显示运行于Java平台上的应用程序的性能和资源占用等信息。

### jhat
Java堆分析工具(Java Heap Analysis Tool),用于分析Java堆内存中的对象信息。

### jmap
Java内存映射工具(Java Memory Map),主要用于打印指定Java进程、核心文件或远程调试服务器的共享对象内存映射或堆内存细节。

### jstack
Java堆栈跟踪工具,主要用于打印指定Java进程、核心文件或远程调试服务器的Java线程的堆栈跟踪信息。
wiloon.com/jstack

### jstat
JVM统计监测工具(JVM Statistics Monitoring Tool),主要用于监测并显示JVM的性能统计信息。
  
<https://blog.wiloon.com/?p=411>

### jstatd

jstatd(VM jstatd Daemon)工具是一个RMI服务器应用,用于监测HotSpot JVM的创建和终止,
  
并提供一个接口,允许远程监测工具附加到运行于本地主机的JVM上。

### jvisualvm

JVM监测、故障排除、分析工具,主要以图形化界面的方式提供运行于指定虚拟机的Java应用程序的详细信息。

### appletviewer

小程序浏览器,一种执行HTML文件上的Java小程序的Java浏览器。 (chrome, firefox 不再支持NPAPI) 

### extcheck

扩展检测工具,主要用于检测指定jar文件与当前已安装的Java SDK扩展之间是否存在版本冲突。

### idlj

IDL转Java编译器(IDL-to-Java Compiler),用于为指定的IDL文件生成Java绑定。
  
IDL意即接口定义语言(Interface Definition Language)。

### jar

jar文件管理工具,主要用于打包压缩、解压jar文件。

### jarsigner

jar密匙签名工具。

### javadoc

Java文档工具,主要用于根据Java源代码中的注释信息生成HTML格式的API帮助文档。

### javah

Java头文件工具,用于根据Java类生成C/C++头文件和源文件(主要用于JNI开发领域)。

### javap

Java反编译工具,主要用于根据Java字节码文件反汇编为Java源代码文件。

### javapackager

JavaFX包装器,用于执行与封装或签名JavaFX应用有关的任务。javafxpackager在JDK1.8的时候更名为javapackager包含在 jdk 里,可以用于常规 Java 独立应用程序的打包 (包括打包 jre 和附带一个启动器) 

### javaws

Java Web Start,使您可以从Web下载和运行Java应用程序,下载、安装、运行、更新Java应用程序都非常简单方便。
  
Java Web Start是帮助客户机端应用程序开发的一个新技术,该技术的独特之处在于将你关心客户机是如何启动 (从Web浏览器或是桌面) 中解放出来。并且,该技术提供了一个使Web服务器能独立发布和更新客户机代码的集合部署方案。
  
Java Web Start是一个软件技术,它包含了applet的可移植性、Servlet和Java Server Pages (JSP) 的可维护性以及象XML和HTML这样的标记语言的简易性。它是基于Java的应用程序,允许从标准的Web服务器启动、部署和更新功能完成的Java 2客户机应用程序。
  
Java Web Start自身是一个Java应用程序,所以该软件是平台独立的,并且支持Java2平台的任何客户机系统都支持该软件。当客户机应用程序启动时,Java Web Start自动执行更新,在从原来的高速缓存装入应用程序的同时,从Web下载罪行的版本。Java Web Start还提供了一个Java应用程序管理器 (Java Application Manager) 实用程序,即提供了多种选项,如清除下载的应用程序的高速缓存、指定多种JRE的使用,设置HTTP代理、还允许最终用户组织他们的Java应用程序。

### jdb

Java调试工具(Java Debugger),主要用于对Java应用进行断点调试。

### jinfo

Java配置信息工具(Java Configuration Information),用于打印指定Java进程、核心文件或远程调试服务器的配置信息。

### jjs

jjs是个基于Nashorn引擎的命令行工具。它接受一些JavaScript源代码为参数,并且执行这些源代码。

### jps
JVM进程状态工具(JVM Process Status Tool),用于显示目标系统上的HotSpot JVM的Java进程信息。

### jrunscript

Java命令行脚本外壳工具(command line script shell),主要用于解释执行javascript、groovy、ruby等脚本语言。

### jsadebugd

Java可用性代理调试守护进程(Java Serviceability Agent Debug Daemon),
  
主要用于附加到指定的Java进程、核心文件,或充当一个调试服务器。jstatd/jsadebugd: 提供远程代理服务,支持jstat/jinfo/jstack通过远程获取信息

### keytool

密钥和证书管理工具,主要用于密钥和证书的创建、修改、删除等。

### native2ascii

本地编码到ASCII编码的转换器(Native-to-ASCII Converter),用于"任意受支持的字符编码"
  
和与之对应的"ASCII编码和(或)Unicode转义"之间的相互转换。
  
native2ascii简介: native2ascii是sun java sdk提供的一个工具。用来将别的文本类文件 (比如_.txt,_.ini,_.properties,_.java等等) 编码转为Unicode编码。为什么要进行转码,原因在于程序的国际化。Unicode编码的定义: Unicode (统一码、万国码、单一码) 是一种在计算机上使用的字符编码。它为每种语言中的每个字符设定了统一并且唯一的二进制编码,以满足跨语言、跨平台进行文本转换、处理的要求。1990年开始研发,1994年正式公布。随着计算机工作能力的增强,Unicode也在面世以来的十多年里得到普及。 (声明: Unicode编码定义来自互联网) 。

### orbd

对象请求代理守护进程(Object Request Broker Daemon),它使客户端能够透明地定位和
  
调用位于CORBA环境的服务器上的持久对象。

### pack200

JAR文件打包压缩工具,它可以利用Java类特有的结构,对普通JAR文件进行高效压缩,以便于能够更快地进行网络传输。

### policytool

策略工具,用于管理用户策略文件(.java.policy)。

### rmic

Java RMI 编译器,为使用JRMP或IIOP协议的远程对象生成stub、skeleton、和tie类,也用于生成OMG IDL。

### rmid

Java RMI 激活系统守护进程,rmid启动激活系统守护进程,允许在虚拟机中注册或激活对象。

### rmiregistry

Java 远程对象注册表,用于在当前主机的指定端口上创建并启动一个远程对象注册表。

### schemagen

XML schema生成器,用于生成XML schema文件。

### serialver

序列版本命令,用于生成并返回serialVersionUID。

### servertool

Java IDL 服务器工具,用于注册、取消注册、启动和终止持久化的服务器。

### tnameserv

Java IDL瞬时命名服务。

### unpack200

JAR文件解压工具,将一个由pack200打包的文件解压提取为JAR文件。

### wsgen

XML Web Service 2.0的Java API,生成用于JAX-WS Web Service的JAX-WS便携式产物。

### wsimport

XML Web Service 2.0的Java API,主要用于根据服务端发布的wsdl文件生成客户端存根及框架

### xjc

主要用于根据XML schema文件生成对应的Java类。

- apt

注解处理工具(Annotation Processing Tool),主要用于注解处理。

### jabswitch

Java访问桥开关(Java Access Bridge switch),用于启用/禁用Java访问桥。
  
Java访问桥内置于Java 7 Update 6及以上版本,主要为Windows系统平台提供一套访问Java应用的API。

### javaw

Java运行工具,用于运行.class字节码文件或.jar文件,但不会显示控制台输出信息,适用于运行图形化程序。

### java-rmi

Java远程方法调用(Java Remote Method Invocation)工具,主要用于在客户机上调用远程服务器上的对象。

### kinit

主要用于获取或缓存Kerberos协议的票据授权票据。

### klist

允许用户查看本地凭据缓存和密钥表中的条目(用于Kerberos协议)。

### ktab

Kerberos密钥表管理工具,允许用户管理存储于本地密钥表中的主要名称和服务密钥。

### packager

这是微软提供的对象包装程序,用于对象安装包。

http://0opslab.com/2016/01/20/JDK%E5%91%BD%E4%BB%A4/