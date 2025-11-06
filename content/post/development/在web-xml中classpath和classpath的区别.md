---
title: '在web.xml中classpath和classpath*的区别'
author: "-"
date: 2014-05-21T03:37:41+00:00
url: /?p=6647
categories:
  - Inbox
tags:
  - Web

---
## '在web.xml中classpath和classpath*的区别'

  写spring的代码到现在,一直都很习惯性的拷贝web.xml中的内容,没怎么在意里面的内容,最近认真研究了下,很多东西都不是很理解,特别是classpath和classpath*的区别,研究了许久才搞明白,记录下备忘。




  classpath 和 classpath* 区别: 


  classpath: 只会到你指定的class路径中查找找文件;


  classpath*: 不仅包含class路径,还包括jar文件中(class路径)进行查找.




  举个简单的例子,在我的web.xml中是这么定义的: classpath*:META-INF/spring/application-context.xml


  那么在META-INF/spring这个文件夹底下的所有application-context.xml都会被加载到上下文中,这些包括META-INF/spring文件夹底下的 application-context.xml,META-INF/spring的子文件夹的application-context.xml以及jar中的application-context.xml。




  如果我在web.xml中定义的是: classpath:META-INF/spring/application-context.xml


  那么只有META-INF/spring底下的application-context.xml会被加载到上下文中。
