---
title: jdk中的jar包, rt.jar ,dt.jar ,tool.jar
author: "-"
date: 2011-08-30T08:50:49+00:00
url: /?p=649
categories:
  - Java
tags:$
  - reprint
---
## jdk中的jar包, rt.jar ,dt.jar ,tool.jar
重点包

rt.jar : 运行时包

dt.jar: dt.jar是关于运行环境的类库

tools.jar: tools.jar是工具类库,编译和运行需要的都是toos.jar里面的类分别是sun.tools.java. ; sun.tols.javac.;
charsets.jar: Java 字符集，这个类库中包含 Java 所有支持字符集的字符
cldrdata.jar: http://cldr.unicode.org/ CLDR - Unicode Common Locale Data Repository
deploy.jar: deploy.jar是Java部署堆栈的一部分，用于applet和Webstart应用程序。 deploy.jar是Java安装目录的常见部分 - 该文件运行某些产品的安装。 正确设置Java路径后，用户可以执行此文件 (只需双击它或按文件上的Enter键) ，要部署的应用程序将运行其安装程序。 例如。 诺基亚OVI套件通常使用这种部署形式。 作为彼此的JAVA包，如果您将其重命名为ZIP并打开内容，则可以检查包中的类。

dnsns.jar:与 DNS 有关

jaccess.jar: Java Access Bridge is a technology that exposes the Java Accessibility API in a Microsoft Windows DLL, enabling Java applications and applets that implement the Java Accessibility API to be visible to assistive technologies on Microsoft Windows systems. Java Accessibility API is part of Java Accessibility Utilities, which is a set of utility classes that help assistive technologies provide access to GUI toolkits that implement the Java Accessibility API. Java Access Bridge是一种在Microsoft Windows DLL中公开Java Accessibility API的技术，使实现Java Accessibility API的Java应用程序和applet对Microsoft Windows系统上的辅助技术可见。 Java Accessibility API是Java Accessibility Utilities的一部分，它是一组实用程序类，可帮助辅助技术提供对实现Java Accessibility API的GUI工具包的访问。

javafx-mx.jar: JavaFx 相关 Contains the following JavaFX utility jar files: ant-javafx.jar: Ant tasks for packaging and deployment.javafx-doclet.jar: A doclet for producing customized and nicely formatted documentation for the users of your JavaFX library.javafx-mx.jar: A file used for debugging.

javaws.jar: Java Web Start contains the JNLP (Java Network Launching Protocol) API and its reference implementation. JNLP (Java Network Launching Protocol ) 是java提供的一种可以通过浏览器直接执行java应用程序的途径，它使你可以直接通过一个网页上的url连接打开一个java应用程序。

jce.jar: Java 加密扩展类库，含有很多非对称加密算法在里面，但也是可扩展的。

jconsole.jar: jconsole Jconsole控制台 Java监视和管理控制台

jfr.jar: Flight Recorder Files 飞行记录器JFR (java flight recorder) 

jfxrt.jar:javaFx相关的java包

jfxswt.jar: javaFx相关的与 swt有关java包

jsse.jar: The Java Secure Socket Extension

localedata.jar: contains many of the resources needed for non US English locales 本地机器语言的数据，比如日期在使用中文时，显示的是"星期四"之类的

management-agent.jar: JVM本身提供了一组管理的API，通过该API，我们可以获取得到JVM内部主要运行信息，包括内存各代的数据、JVM当前所有线程及其栈相关信息等等。各种JDK自带的剖析工具，包括jps、jstack、jinfo、jstat、jmap、jconsole等，都是基于此API开发的。

nashorn.jar: A Next-Generation JavaScript Engine for the JVM JVM的JavaScript解析引擎

packager.jar: The Java Packager tool can be used to compile, package, sign, and deploy Java and JavaFX applications from the command line. It can be used as an alternative to an Ant task or building the applications in an IDE. The Java Packager tool is not available for the Solaris platform.

plugin.jar: 按字面意思，应该是插件API的意思, 与UI和浏览器有关

resources.jar: 资源包 (图片、properties文件) 

sa-jdi.jar: ServiceAbility JDK SA工具 https://www.jianshu.com/p/7c40274441a4

sunec.jar: JCE providers for Java Cryptography APIs

sunjce_provider.jar: 为JCE 提供的加密安全套件

sunpkcs11.jar: PKCS#11 证书工具

zipfs.jar: Zip File System Provider
 
rt.jar ,dt.jar ,tools.jar都是 做什么用的 ,分别什么时候需要设置到classpath里?
  
---------------------

rt.jar是JAVA基础类库，dt.jar是关于运行环境的类库，tools.jar是工具类库

设置在classpath里是为了让你 import *
  
---------------------

web系统都用到tools.jar

你用winrar看看里面是什么内容啦
  
---------------------

1.
  
rt.jar 默认就在 根classloader的加载路径里面 放在claspath是多此一举
  
不信你可以去掉classpath里面的rt.jar
  
然后用 java -verbose XXXX 的方式运行一个简单的类就知道 JVM的系统根Loader的路径里面
  
不光rt.jar jrelib下面的大部分jar 都在这个路径里

2.
  
tools.jar 是系统用来编译一个类的时候用到的 也就是javac的时候用到
  
javac XXX.java
  
实际上就是运行
  
java -Calsspath=%JAVA_HOME%libtools.jar xx.xxx.Main XXX.java
  
javac就是对上面命令的封装 所以tools.jar 也不用加到classpath里面

3.
  
dt.jar是关于运行环境的类库,主要是swing的包
  
JDK 1.5 及以上的版不需要再设置 classpath, 只要把path配好就行。

#from http://download.oracle.com/javase/6/docs/technotes/tools/windows/jdkfiles.html
  
jdk1.6.0lib
  
Files used by the development tools. These include tools.jar, which contains non-core classes for support of the tools and utilities in the JDK. Also includes dt.jar, the DesignTime archive of BeanInfo files that tell interactive development environments (IDE's) how to display the Java components and how to let the developer customize them for an application.

c:jdk1.6.0jrebin
  
Executable files and DLLs for tools and libraries used by the Java platform. The executable files are identical to files in /jdk1.6.0/bin. The java launcher tool serves as an application launcher (and replaced the old jre tool that shipped with 1.1 versions of the JDK). This directory does not need to be in the PATH environment variable.

c:jdk1.6.0jrelib
  
Code libraries, property settings, and resource files used by the Java runtime environment. For example:
  
rt.jar - the bootstrap classes (the RunTime classes that comprise the Java platform's core API).
  
charsets.jar - character conversion classes.

https://www.jianshu.com/p/e9ba412d66f3

