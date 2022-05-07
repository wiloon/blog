---
title: Java URL URI
author: "-"
date: 2014-02-26T05:24:54+00:00
url: /?p=6287
categories:
  - Inbox
tags:
  - Java

---
## Java URL URI
http://blog.csdn.net/majiabao123/article/details/4202158

从JDK1.4开始，java.net包对统一资源定位符(uniform resource locator URL)和统一资源标识符(uniform resource identifier URI)作了非常有用的区分。

URI是个纯粹的句法结构，用于指定标识Web资源的字符串的各个不同部分。URL是URI的一个特例，它包含了定位Web资源的足够信息。其他URI，比如: 

mailto: <cay@horstman.com>

则不属于定位符，因为根据该标识符无法定位任何资源。像这样的URI我们称之为URN(统一资源名称)。

在Java类库中，URI类不包含任何访问资源的方法，它唯一的作用就是解析。相反的是，URL类可以打开一个到达资源的流。因此URL类只能作用于那些Java类库知道该如何处理的模式，例如: http: ，https: ，ftp:，本地文件系统(file:)，和Jar文件(jar:)。

URI类的作用之一是解析标识符并将它们分解成各个不同的组成部分。你可以用以下方法读取它们: 

getSchema

getHost

getPort

getPath

getQuery

URI类的另一个作用是处理绝对标识符和相对标识符。如果存在一个如下的绝对URI: 

<http://docs.mycompany.com/api/java/net/serversocket.html>

和一个如下的相对URI: 

../../java/net/socket.html#Socket()

那么你可以将它们合并成一个绝对URI: 

<http://docs.mycompany.com/api/java/net/socket.html#Socket>()

这个过程被称为相对URL的转换。

与此相反的过程成为相对化。例如: 假设你有一个基本URI: 

<http://docs.mycompany/api>

和另一个URI: 

<http://docs.mycompany/api/java/lang/String.html>

那么相对化后的URI就是: 

java/lang/String.html