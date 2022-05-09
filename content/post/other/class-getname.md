---
title: class.getName
author: "-"
date: 2014-01-05T06:57:06+00:00
url: /?p=6140
categories:
  - Inbox
tags:
  - Java

---
## class.getName
<http://bbs.csdn.net/topics/70162498>

java.lang.Object
  
java.lang.Class

String getName()
  
Returns the name of the entity (class, interface, array class, primitive type, or void) represented by this Class object, as a String.


java的类映射函数..用来得到类的具体名字

比如说1个类mypackage.MyClass

MyClass.class.getName();就能得到mypackage.MyClass

在object里面这么用getClass().getName();