---
title: Java读取properties, getResourceAsStream
author: "-"
date: 2012-05-25T07:57:43+00:00
url: /?p=3209
categories:
  - Java
tags:
  - reprint
---
## Java读取properties, getResourceAsStream
http://lavasoft.blog.51cto.com/62575/62174
  
Java读取properties文件的方法比较多，网上我最多的文章是"Java读取properties文件的六种方法"，但在Java应用中，最常用还是通过java.lang.Class类的getResourceAsStream(String name) 方法来实现，但我见到众多读取properties文件的代码中，都会这么干: 

```java

// java object
InputStream in = getClass().getResourceAsStream("资源Name");

// static method
Class.class.getClassLoader().getResourceAsStream("foo.toml");
  
```

这里面有个问题，就是getClass()调用的时候默认省略了this！我们都知道，this是不能在static (静态) 方法或者static块中使用的，原因是static类型的方法或者代码块是属于类本身的，不属于某个对象，而this本身就代表当前对象，而静态方法或者块调用的时候是不用初始化对象的。

问题是: 假如我不想让某个类有对象，那么我会将此类的默认构造方法设为私有，当然也不会写别的共有的构造方法。并且我这个类是工具类，都是静态的方法和变量，我要在静态块或者静态方法中获取properties文件，这个方法就行不通了。

那怎么办呢？其实这个类就不是这么用的，他仅仅是需要获取一个Class对象就可以了，那还不容易啊－－取所有类的父类Object，用Object.class难道不比你的用你正在写类自身方便安全吗 ？呵呵，下面给出一个例子，以方便交流。

```java

import java.util.Properties;
  
import java.io.InputStream;
  
import java.io.IOException;

/**
  
* 读取Properties文件的例子
  
* File: TestProperties.java
  
* User: leizhimin
  
* Date: 2008-2-15 18:38:40
  
*/
  
public final class TestProperties {
  
private static String param1;
  
private static String param2;

static {
  
Properties prop = new Properties();
  
InputStream in = Object.class.getResourceAsStream("/test.properties");
  
try {
  
prop.load(in);
  
param1 = prop.getProperty("initYears1").trim();
  
param2 = prop.getProperty("initYears2").trim();
  
} catch (IOException e) {
  
e.printStackTrace();
  
}
  
}

/**
  
* 私有构造方法，不需要创建对象
  
*/
  
private TestProperties() {
  
}

public static String getParam1() {
  
return param1;
  
}

public static String getParam2() {
  
return param2;
  
}

public static void main(String args[]){
  
System.out.println(getParam1());
  
System.out.println(getParam2());
  
}
  
}
  
```

运行结果: 
  
152

Process finished with exit code 0

当然，把Object.class换成int.class照样行，呵呵，大家可以试试。

另外，如果是static方法或块中读取Properties文件，还有一种最保险的方法，就是这个类的本身名字来直接获取Class对象，比如本例中可写成TestProperties.class，这样做是最保险的方法。


load resouorces as utf8

```java
  
Properties properties = new Properties();
  
InputStream inputStream = new FileInputStream("path/to/file");
  
try {
      
Reader reader = new InputStreamReader(inputStream, "UTF-8");
      
try {
          
properties.load(reader);
      
} finally {
          
reader.close();
      
}
  
} finally {
     
inputStream.close();
  
}```
  
```