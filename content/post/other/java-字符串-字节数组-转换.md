---
title: java 字符串， 比较
author: "-"
date: 2015-08-13T08:10:39+00:00
url: /?p=8109
categories:
  - Inbox
tags:
  - Java

---
## java 字符串， 比较

### java简单的字符串大小比较——compareTo()方法

 在java编程中，我们会偶尔遇到字符串大小比较的问题，compareTo()方法很简单就实现这种功能。该方法用于判断一个字符串是大于、等于还是小于另一个字符串。判断字符串大小的依据是根据它们在字典中的顺序决定的。

    语法: Str1.compareTo(Str2);

    其返回的是一个int类型值。若Str1等于参数字符串Str2字符串，则返回0；若该Str1按字典顺序小于参数字符串Str2，则返回值小于0；若Str1按字典顺序大于参数字符串Str2，则返回值大于0。

    java中的compareto方法，返回参与比较的前后两个字符串的asc码的差值，看下面一组代码

    String a="a",b="b";
    System.out.println(a.compareto.b);
    则输出-1；
    若a="a",b="a"则输出0；
    若a="b",b="a"则输出1；

   单个字符这样比较，若字符串比较长呢？？
   若a="ab",b="b",则输出-1；
   若a="abcdef",b="b"则输出-1；
   也就是说，如果两个字符串首字母不同，则该方法返回首字母的asc码的差值；

  如果首字母相同呢？？
  若a="ab",b="a",输出1；
  若a="abcdef",b="a"输出5；
  若a="abcdef",b="abc"输出3；
  若a="abcdef",b="ace"输出-1；
   即参与比较的两个字符串如果首字符相同，则比较下一个字符，直到有不同的为止，返回该不同的字符的asc码差值，如果两个字符串不一样长，可以参与比较的字符又完全一样，则返回两个字符串的长度差值
参考: [http://blog.sina.com.cn/s/blog_8a7200cd010104nx.html](http://blog.sina.com.cn/s/blog_8a7200cd010104nx.html)

    http://www.blogjava.net/hgc-ghc/archive/2013/03/28/397084.html

```java

//char 转String

String str = String.valueOf(c);

//判断字符大小写
  
if( Character.isUpperCase(c))

```

**1、字节数组转换为字符串**

byte[] byBuffer = new byte[20];
  
... ...
  
String strRead = new String(byBuffer);
  
strRead = String.copyValueOf(strRead.toCharArray(), 0, byBuffer.length]);

**2、字符串转换成字节数组**

byte[] byBuffer = new byte[200];
  
String strInput="abcdefg";
  
byBuffer= strInput.getBytes();

注意: 如果字符串里面含有中文，要特别注意，在android系统下，默认是UTF8编码，一个中文字符相当于3个字节，只有gb2312下一个中文相当于2字节。这种情况下可采取以下办法:

byte[] byBuffer = new byte[200];
  
String strInput="我是字符串";
  
byBuffer= strInput.getBytes("gb2312");
