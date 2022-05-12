---
title: java static import
author: "-"
date: 2012-05-14T06:47:02+00:00
url: /?p=3135
categories:
  - Java
tags:$
  - reprint
---
## java static import
http://blog.csdn.net/ygc87/article/details/7371254

import static (静态导入) 是JDK1.5中的新特性，一般我们导入一个类都用 import com.....ClassName;而静态导入是这样: import static com.....ClassName.\*;这里多了个static，还有就是类名ClassName后面多了个 .\* ，意思是导入这个类里的静态方法。当然，也可以只导入某个静态方法，只要把 .* 换成静态方法名就行了。然后在这个类中，就可以直接用方法名调用静态方法，而不必用ClassName.方法名的方式来调用。

例如，你在某个类中定义了一些简便的打印方法: 



print?
  
package com.ygc.print;

public class Print {
  
// 打印，换行
  
public static void print(Object obj) {
  
System.out.println(obj);
  
}

// 换行
  
public static void print() {
  
System.out.println();
  
}

// 打印
  
public static void printnb(Object obj) {
  
System.out.print(obj);
  
}
  
}

然后你想在其他的类里面使用这些方法: 



print?
  
package com.ygc;

import static com.ygc.print.Print.*;

class Test {
  
public void println(String s) {
  
print(s);
  
}
  
}


## java static import
 jdk1.5 static import
 static import
 static import就是允许在代码中直接引用别的类的static变量和方法 (当然，在权限许可范围内) ，我们可以简单的把它当成import的延续。
 它的语法如下: 
 import static CLASS_NAME.MEMBER_NAME;
 或者 import static CLASS_NAME.×;
 事实上，Tiger引入static import最主要考虑到两个需要，第一个就是对一些工具性的，常用的静态方法进行直接引用。
 比如,java.lang.Math里的一大堆数学方法abs,exp等。
 第二个就是对常数变量进行直接引用，其中也包扩对enum的直接引用 (参考上一篇文章Season的例子) 
 [code]
 //StaticImportTest.java
 import static java.lang.Math.*;
  
  
    public class StaticImportTest{
  
  
    public static void main(String arsg[]){
 System.out.println("1 + 1 ="+(1+1));
 System.out.println("abs(-1)="+abs(-1));
 System.out.println("exp(1.5)="+exp(1.5));
 System.out.println("Pi = "+PI);
 System.out.println("E = "+E);
  
  
    }
  
  
    }
 ```
  
  
    这样的代码不仅省却了Programmer的劳动，在可读性上也是有所增强。
  
  
    static import的限制和import也基本一样，就是不能出现二义性。
 另外，static import不支持先import类，然后import static 类.*(不加package)的形式
 如
 [code]
 import??java.util.*;
 import static Calendar.*;
 ......
 ```
  
  
    就算在同一个包也是如此。
  
  
    值得注意的是，过多的static import也许可能影响程序的可读性，如: 
 [code]
 //StaticImportTest2.java
 import static java.lang.Integer.parseInt;
 import static java.lang.Double.*;
  
  
    public class StaticImportTest{
  
  
    public static void main(String arsg[]){
 String iv = "1239";
 String dv = "123.3456";
 System.out.println(iv+":"+parseInt(iv));
 System.out.println(dv+":"+parseDouble(dv));
 System.out.println("Double's MaxValue is:"+MAX_VALUE );
  
  
    }
 ```
  
  
    虽然能编译通过，但是却很容易混绕读者视线。
  

