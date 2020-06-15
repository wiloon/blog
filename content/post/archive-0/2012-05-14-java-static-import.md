---
title: java static import
author: wiloon
type: post
date: 2012-05-14T06:47:02+00:00
url: /?p=3135
categories:
  - Java

---


<div id="article_content">
  <p>
    jdk1.5 static import<br /> static import<br /> static import就是允许在代码中直接引用别的类的static变量和方法（当然，在权限许可范围内），我们可以简单的把它当成import的延续。<br /> 它的语法如下：<br /> import static CLASS_NAME.MEMBER_NAME;<br /> 或者 import static CLASS_NAME.×;<br /> 事实上，Tiger引入static import最主要考虑到两个需要，第一个就是对一些工具性的，常用的静态方法进行直接引用。<br /> 比如,java.lang.Math里的一大堆数学方法abs,exp等。<br /> 第二个就是对常数变量进行直接引用，其中也包扩对enum的直接引用（参考上一篇文章Season的例子）<br /> [code]<br /> //StaticImportTest.java<br /> import static java.lang.Math.*;
  </p>
  
  <p>
    public class StaticImportTest{
  </p>
  
  <p>
    public static void main(String arsg[]){<br /> System.out.println("1 ＋ 1 ="+(1+1));<br /> System.out.println("abs(-1)="+abs(-1));<br /> System.out.println("exp(1.5)="+exp(1.5));<br /> System.out.println("Pi = "+PI);<br /> System.out.println("E = "+E);
  </p>
  
  <p>
    }
  </p>
  
  <p>
    }<br /> [/code]
  </p>
  
  <p>
    这样的代码不仅省却了Programmer的劳动，在可读性上也是有所增强。
  </p>
  
  <p>
    static import的限制和import也基本一样，就是不能出现二义性。<br /> 另外，static import不支持先import类，然后import static 类.*(不加package)的形式<br /> 如<br /> [code]<br /> import??java.util.*;<br /> import static Calendar.*;<br /> &#8230;&#8230;<br /> [/code]
  </p>
  
  <p>
    就算在同一个包也是如此。
  </p>
  
  <p>
    值得注意的是，过多的static import也许可能影响程序的可读性，如：<br /> [code]<br /> //StaticImportTest2.java<br /> import static java.lang.Integer.parseInt;<br /> import static java.lang.Double.*;
  </p>
  
  <p>
    public class StaticImportTest{
  </p>
  
  <p>
    public static void main(String arsg[]){<br /> String iv = "1239";<br /> String dv = "123.3456";<br /> System.out.println(iv+":"+parseInt(iv));<br /> System.out.println(dv+":"+parseDouble(dv));<br /> System.out.println("Double&#8217;s MaxValue is:"+MAX_VALUE );
  </p>
  
  <p>
    }<br /> [/code]
  </p>
  
  <p>
    虽然能编译通过，但是却很容易混绕读者视线。
  </p>
</div>