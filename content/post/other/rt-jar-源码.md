---
title: rt.jar 源码
author: "-"
date: 2012-04-28T06:05:06+00:00
url: /?p=3047
categories:
  - Java
tags:
  - reprint
---
## rt.jar 源码
[http://topic.csdn.net/u/20110125/10/06139927-2e44-4c76-b41c-fa7ea3206dd3.html](http://topic.csdn.net/u/20110125/10/06139927-2e44-4c76-b41c-fa7ea3206dd3.html)

java全部源代码,src.zip中没有的,在openjdk里的源代码加到eclipse里面..
  
本来想问的.现在摸索出来了..可以到
  
[http://download.java.net/openjdk/jdk6/](http://download.java.net/openjdk/jdk6/)下载源码 或者搜索 openjdk jdk6 ..如果你的jdk是jdk 5 或者jdk 7.那就搜索 openjdk jdk5 或者 openjdk jdk7..
  
下载完以后解压缩..

eclipse里面选中 windows -preference-java-installed jres-选中jre6(你的可能是jre5 或者jre7)-edit-选中rt.jar-source attachment-external folders..
  
选中解压缩的openjdk目录下的子目录 解压所在目录/jdk/src/share/classes/ ..然后重启eclipse..
  
这样子原来添加src.zip所不能看的源代码,比如rt.jar下sun.misc包里的class..现在就可以看源代码了..