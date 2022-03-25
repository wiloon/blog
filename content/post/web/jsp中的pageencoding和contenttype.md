---
title: JSP中的PageEncoding和ContentType
author: "-"
date: 2012-09-26T02:42:12+00:00
url: /?p=4292
categories:
  - Java
  - Web
tags:
  - JSP

---
## JSP中的PageEncoding和ContentType
JSP页面中的PageEncoding和ContentType两种属性的区别是什么呢？我们先来看一下: 

**PageEncoding: **是JSP文件本身的编码

**ContentType:  **ContentType 属性指定响应的 HTTP 内容类型。如果未指定 ContentType，默认为 text/HTML。

ContentType的charset是指服务器发送给客户端时的内容编码

JSP要经过两次的"编码"，第一阶段会用PageEncoding，第二阶段是从utf-8到utf-8，第三阶段就是由Tomcat出来的网页， 用的是ContentType。

第一阶段是JSP编译成.java，它会根据pageEncoding的设定读取jsp，结果是由指定的编码方案翻译成统一的UTF-8 JAVA源码 (即.java) ，如果pageEncoding设定错了，或没有设定，出来的就是中文乱码。

第二阶段是由Javac的Java源码至Java byteCode的编译，不论JSP编写时候用的是什么编码方案，经过这个阶段的结果全部是UTF-8的Encoding的Java源码。

JAVAC用UTF-8的Encoding读取Java源码，编译成UTF-8 encoding的二进制码 (即.class) ，这是JVM对常数字串在二进制码 (java encoding) 内表达的规范。

第三阶段是Tomcat (或其的application container) 载入和执行阶段二的来的JAVA二进制码，输出的结果，也就是在客户端见到的，这时隐藏在阶段一和阶段二的参数ContentType就发挥了功效

ContentType的设定.

PageEncoding 和ContentType的预设都是 ISO8859-1. 而随便设定了其中一个, 另一个就跟着一样了(TOMCAT4.1.27是如此). 但这不是绝对的, 这要看各自JSPC的处理方式. 而PageEncoding不等于ContentType, 更有利亚洲区的文字CJKV系JSP网页的开发和展示, (例PageEncoding=GB2312 不等于 ContentType=utf-8)。

JSP文件不像Java，.java在被编译器读入的时候默认采用的是操作系统所设定的locale所对应的编码，比如中国大陆就是GBK，台湾就是BIG5或者MS950。而一般我们不管是在记事本还是在ue中写代码，如果没有经过特别转码的话，写出来的都是本地编码格式的内容。所以编译器采用的方法刚好可以让虚拟机得到正确的资料。

但是JSP文件不是这样，它没有这个默认转码过程，但是指定了PageEncoding就可以实现正确转码了。

举个例子:

  1. ﹤%@ page contentType="text/html;charset=utf-8" %﹥

大都会打印出乱码，因为我输入的"你好吗"是gbk的，但是服务器是否正确抓到"你好吗"不得而知。

但是如果更改为

  1. ﹤%@ page contentType="text/html;charset=utf-8" pageEncoding="GBK"%﹥

这样就服务器一定会是正确抓到"你好吗"了。

JSP中的pageEncoding和contentType通过上面的归纳，你是不是对他们的应用有了更新的认识呢？

http://blog.csdn.net/dragon4s/article/details/6604624

http://www.cnblogs.com/kevin-yuan/archive/2011/12/31/2308479.html

http://tech.sina.com.cn/s/2007-09-27/10121766102.shtml