---
title: "Java 读取环境变量"
author: "-"
date: 2015-08-14T07:37:39+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: environment-variables
tags:
  - Java
  - remix
  - AI-assisted
categories:
  - Java
aliases:
  - /java读-环境变量/
---
## Java读 环境变量
http://ling091.iteye.com/blog/354052

读取环境变量时可以使用 System.getProperty 或 System.getenv 方法。

System.getProperty 方法 ( JDK1.4 ) 用来读取针对 JVM 的属性，如程序当前的运行路径、路径分隔符、 Java 版本等， ( 见 System.getProperty() 参数大全 ) ，它也可以读取在运行程序时设置的自定义属性。
  
* 获取一个JVM已定义属性
  
```bash
//获取系统当前的运行路径
System.out.println("current path = " + System.getProperty("user.dir") );
```

输出: current path = E:\program\java\test\Test

* 获取应用程序的属性: 

在命令中输入下面的命令，其中的-D用于设置一个属性 -`D<name>`=`<value>`

```text
SET myvar=Hello world
SET myothervar=nothing
java -Dmyvar="%myvar%" -Dmyothervar="%myothervar%" myClass
```

myClass中读取这些属性

```java
String myvar = System.getProperty("myvar");
String myothervar = System.getProperty("myothervar");
```

如果要读取操作系统的环境变量 (如 Path 、 TEMP 或 TMP 、 JAVA_HOME 等。) 则可以使用 System.getenv 方法，但是由于某些原因，该方法被去掉了，直到 JDK1.5 后，该方法又被加进去 [3] 。

* 获取一个系统环境变量

```bash
//获取JAVA_HOME环境变量:
System.out.println("JAVA_HOME = " + System.getenv("JAVA_HOME") );
```

输出: JAVA_HOME = C:\Program Files\Java\jdk1.6.0_07
  
```xml
<!--><!--> <!-->
```
  
参考: 

```xml
<!--><!-->  <!-->
```

[1] Read environment variables from an application ．

http://www.rgagnon.com/javadetails/java-0150.html ．

```xml
<!--><!-->
```
  
[2] Retrieve environment variables (JDK1.5) ．

http://www.rgagnon.com/javadetails/java-0466.html ．
  
```xml
<!--><!--> <!-->
[3] Retrieve environment variable (JNI)
http://www.rgagnon.com/javadetails/java-0460.html
<!--><!--> <!-->
```

[4]Common XP environment variables

http://www.rgagnon.com/pbdetails/pb-0254.html

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `environment-variables.md`；title 改为「Java 读取环境变量」；url 改为 `environment-variables`；旧 url 加入 aliases；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
