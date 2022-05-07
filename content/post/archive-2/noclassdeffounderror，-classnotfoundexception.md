---
title: NoClassDefFoundError, ClassNotFoundException
author: "-"
date: 2017-03-08T02:41:42+00:00
url: /?p=9899
categories:
  - Inbox
tags:
  - reprint
---
## NoClassDefFoundError, ClassNotFoundException
http://wxl24life.iteye.com/blog/1919359

java.lang.NoClassDefFoundError 和 java.lang.ClassNotFoundException 都是 Java 语言定义的标准异常。从异常类的名称看似乎都跟类的定义找不到有关,但是还是有些差异。我们先来看一下 java 规范中对这两个异常的说明: 

java.lang.NoClassDefFoundError:

Thrown if the Java Virtual Machine or a ClassLoader instance tries to load in the definition of a class (as part of a normal method call or as part of creating a new instance using the new expression) and no definition of the class could be found.

The searched-for class definition existed when the currently executing class was compiled, but the definition can no longer be found.
  
类加载器试图加载类的定义,但是找不到这个类的定义,而实际上这个类文件是存在的。

java.lang.ClassNotFoundException:

Thrown when an application tries to load in a class through its string name using:
  
1. The forName method in class Class.
  
2. The findSystemClass method in class ClassLoader .
  
3. The loadClass method in class ClassLoader.
  
but no definition for the class with the specified name could be found.
  
从规范说明看, java.lang.ClassNotFoundException 异常抛出的根本原因是类文件找不到。

另外,从两个异常的定义看,java.lang.NoClassDefFoundError 是一种 unchecked exception (也称 runtime exception) ,而 java.lang.ClassNotFoundException 是一种 checked exception。 (区分不了这两类异常？看这里 checked exception vs unchecked exception) 

———-

有了前面的分析,我们知道这他们是两个完全不同的异常。但是如果在实际运行代码时碰到了其中一个,还是很容易被混淆成同一个,尤其是当事先没有留意到这两个异常的差别时。

就我个人而言,在这两个异常里,平时碰到最多的是 java.lang.ClassNotFoundException。从异常的名字看,很容易理解这个异常产生的原因是缺少了 .class 文件,比如少引了某个 jar,解决方法通常需要检查一下 classpath 下能不能找到包含缺失 .class 文件的 jar。

但是,很多人在碰到 java.lang.NoClassDefFoundError 异常时也会下意识的去检查是不是缺少了 .class 文件,比如 SO 上的这位提问者 (java.lang.NoClassDefFoundError: Could not initialize class XXX) – "明明 classpath 下有那个 jar 为什么还报这个异常"。而实际上,这个异常的来源根本不是因为缺少 .class 文件。而碰到这个异常的解决办法,一般需要检查这个类定义中的初始化部分 (如类属性定义、static 块等) 的代码是否有抛异常的可能,如果是 static 块,可以考虑在其中将异常捕获并打印堆栈等,或者直接在对类进行初始化调用 (如 new Foobar()) 时作 try catch。

———-

前两天我也碰到了一个类似场景导致的 java.lang.NoClassDefFoundError:  Could not initialize class xxx 异常,下面详细记录一下。

我定义了一个类,为了使用 log4j 打印日志,调用 org.slf4j.LoggerFactory 创建了一个 Logger,并作为类的 static 属性,除此之外无其他的成员属性,代码如下: 

Java代码
  
public class Foo {
  
private static Logger logger = LoggerFactory.getLogger(Foo.class);
  
// … methods
  
}
  
在另一个类里创建 Foo 实例: 

Java代码
  
public class Bar {

public void someMethod() {
  
Foo foo = new Foo();
  
// …
  
}
  
}
  
在执行 new Foo() 时抛异常 java.lang.NoClassDefFoundError:  Could not initialize class Foo。经过一番排查,这个异常最后的原因出在了 LoggerFactory.getLogger(Foo.class) 调用抛错,关于 这条语句为什么会抛错,我会在另一篇文章里详细描述,在这里只是简单的说下原因: 由于 slf4j-api.jar 和 slf4j 的某个 binding jar 版本不兼容所致。

—-

总结,记住他们是两个不同的异常类,在碰到具体某个异常时,从名字并联系它的 message 信息 (如 "Could not initialize class ") 就很容易锁定问题来源。

完。