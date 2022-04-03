---
title: Java读 环境变量
author: "-"
date: 2015-08-14T07:37:39+00:00
url: /?p=8122
tags:
  - java

categories:
  - inbox
---
## Java读 环境变量
http://ling091.iteye.com/blog/354052

读取环境变量时可以使用 System.getProperty 或 System.getenv 方法。

System.getProperty 方法 ( JDK1.4 ) 用来读取针对 JVM 的属性，如程序当前的运行路径、路径分隔符、 Java 版本等， ( 见 System.getProperty() 参数大全 ) ，它也可以读取在运行程序时设置的自定义属性。
  
* 获取一个JVM已定义属性
  
//获取系统当前的运行路径
  
System.out.println("current path = " + System.getProperty("user.dir") );

输出: current path = E:\program\java\test\Test

* 获取应用程序的属性: 

在命令中输入下面的命令，其中的-D用于设置一个属性 -D<name>=<value>

SET myvar=Hello world
  
SET myothervar=nothing
  
java -Dmyvar="%myvar%" -Dmyothervar="%myothervar%" myClass

myClass中读取这些属性

String myvar = System.getProperty("myvar");
  
String myothervar = System.getProperty("myothervar");

如果要读取操作系统的环境变量 (如 Path 、 TEMP 或 TMP 、 JAVA_HOME 等。) 则可以使用 System.getenv 方法，但是由于某些原因，该方法被去掉了，直到 JDK1.5 后，该方法又被加进去 [3] 。

* 获取一个系统环境变量

//获取JAVA_HOME环境变量: 
  
System.out.println("JAVA_HOME = " + System.getenv("JAVA_HOME") );

输出: JAVA_HOME = C:\Program Files\Java\jdk1.6.0_07
  
<!--><!--> <!-->
  
参考: 

<!--><!-->  <!-->

[1] Read environment variables from an application ．

http://www.rgagnon.com/javadetails/java-0150.html ．

<!--><!-->
  
[2] Retrieve environment variables (JDK1.5) ．

http://www.rgagnon.com/javadetails/java-0466.html ．
  
<!--><!--> <!-->

[3] Retrieve environment variable (JNI)

http://www.rgagnon.com/javadetails/java-0460.html

<!--><!--> <!-->

[4]Common XP environment variables

http://www.rgagnon.com/pbdetails/pb-0254.html