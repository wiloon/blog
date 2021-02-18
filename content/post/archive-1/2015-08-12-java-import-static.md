---
title: java import static
author: w1100n
type: post
date: 2015-08-12T01:22:29+00:00
url: /?p=8095
categories:
  - Uncategorized
tags:
  - Java

---
http://blog.csdn.net/ygc87/article/details/7371254

import static（静态导入）是JDK1.5中的新特性，一般我们导入一个类都用 import com.....ClassName;而静态导入是这样：import static com.....ClassName.\*;这里多了个static，还有就是类名ClassName后面多了个 .\* ，意思是导入这个类里的静态方法。当然，也可以只导入某个静态方法，只要把 .* 换成静态方法名就行了。然后在这个类中，就可以直接用方法名调用静态方法，而不必用ClassName.方法名的方式来调用。

例如，你在某个类中定义了一些简便的打印方法：

[java][/java]

view plaincopyprint?
  
package com.ygc.print;

public class Print {
  
// 打印，换行
  
public static void print(Object obj) {
  
System.out.println(obj);
  
}

// 换行
  
public static void print() {
  
System.out.println();
  
}

// 打印
  
public static void printnb(Object obj) {
  
System.out.print(obj);
  
}
  
}

然后你想在其他的类里面使用这些方法：

[java][/java]

view plaincopyprint?
  
package com.ygc;

import static com.ygc.print.Print.*;

class Test {
  
public void println(String s) {
  
print(s);
  
}
  
}

