---
title: isAssignableFrom
author: "-"
date: 2014-06-09T06:10:03+00:00
url: /?p=6715
categories:
  - Uncategorized
tags:
  - Java

---
## isAssignableFrom

isAssignableFrom 是用来判断一个类Class1和另一个类Class2是否相同或是另一个类的超类或接口。
  
通常调用格式是
  
Class1.isAssignableFrom(Class2)
  
调用者和参数都是 java.lang.Class 类型。

而 instanceof 是用来判断一个对象实例是否是一个类或接口的或其子类子接口的实例。
  
格式是:  oo instanceof TypeName
  
第一个参数是对象实例名，第二个参数是具体的类名或接口名，例如 String，InputStream。

用下面的代码进行测试，我们就可以发现他们的不同之处
