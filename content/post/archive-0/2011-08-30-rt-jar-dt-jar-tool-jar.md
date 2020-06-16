---
title: rt.jar ,dt.jar ,tool.jar
author: wiloon
type: post
date: 2011-08-30T08:50:49+00:00
url: /?p=649
bot_views:
  - 8
views:
  - 3
categories:
  - Java

---
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