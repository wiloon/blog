---
title: java static import
author: "-"
type: post
date: 2012-05-14T06:47:02+00:00
url: /?p=3135
categories:
  - Java

---
## java static import

    jdk1.5 static import
 static import
 static import就是允许在代码中直接引用别的类的static变量和方法（当然，在权限许可范围内) ，我们可以简单的把它当成import的延续。
 它的语法如下: 
 import static CLASS_NAME.MEMBER_NAME;
 或者 import static CLASS_NAME.×;
 事实上，Tiger引入static import最主要考虑到两个需要，第一个就是对一些工具性的，常用的静态方法进行直接引用。
 比如,java.lang.Math里的一大堆数学方法abs,exp等。
 第二个就是对常数变量进行直接引用，其中也包扩对enum的直接引用（参考上一篇文章Season的例子) 
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
  
