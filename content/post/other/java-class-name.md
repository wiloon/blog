---
title: Java 取当前类名, 方法名
author: "-"
date: 2013-05-13T04:54:06+00:00
url: /?p=5462
categories:
  - Inbox
tags:
  - reprint
---
## Java 取当前类名, 方法名

<http://blog.csdn.net/a578559967/article/details/7688971>

```java
  
public class ClassName {
      
public static void main(String[] args) {
          
testGetClassName();
      
}

public static void testGetClassName() {
          
// 方法1: 通过SecurityManager的保护方法getClassContext()
          
String clazzName = new SecurityManager() {
              
public String getClassName() {
                  
return getClassContext()[1].getName();
              
}
          
}.getClassName();
          
System.out.println(clazzName);

// 方法2: 通过Throwable的方法getStackTrace()
          
String clazzName2 = new Throwable().getStackTrace()[1].getClassName();
          
System.out.println(clazzName2);

// 方法3: 通过分析匿名类名称()
          
String clazzName3 = new Object() {
              
public String getClassName() {
                  
String clazzName = this.getClass().getName();
                  
return clazzName.substring(0, clazzName.lastIndexOf('$'));
              
}
          
}.getClassName();
          
System.out.println(clazzName3);

//方法4: 通过Thread的方法getStackTrace()
          
String clazzName4 = Thread.currentThread().getStackTrace()[2].getClassName();
          
System.out.println(clazzName4);

System.out.println(Thread.currentThread().getStackTrace()[0].getMethodName());
          
System.out.println(Thread.currentThread().getStackTrace()[1].getMethodName());
          
System.out.println(Thread.currentThread().getStackTrace()[2].getMethodName());
      
}
  
}
  
```
