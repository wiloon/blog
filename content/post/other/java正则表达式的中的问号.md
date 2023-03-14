---
title: java正则表达式的中的问号
author: "-"
date: 2012-08-19T03:35:38+00:00
url: /?p=3911
categories:
  - Java
tags:
  - Regex

---
## java正则表达式的中的问号

  java正则表达式中的  ? 是惰性匹配，具体的看下面的例子:  
  
 ```java
 Pattern pattern = Pattern.compile("<.*>");
 Matcher matcher =pattern.matcher("主页");
 System.out.println(matcher.replaceAll(""));

 ```

将输出空，因为没有加问号，此时进行的是最长匹配(贪婪匹配)
  
可以做如果更改
  
```java
Pattern pattern = Pattern.compile("<.*>");
Matcher matcher =pattern.matcher("主页[color=red]</a[/color]");
System.out.println(matcher.replaceAll(""));
```

将输出: 主页</a

如果把程序修改为:

```java
Pattern pattern = Pattern.compile("<.*?>");
Matcher matcher =pattern.matcher("主页");
System.out.println(matcher.replaceAll(""));
```

将输出: 主页

不加 ? 表示贪婪，加 ? 表示勉强，区别如下:

勉强是从左边一个一个地吃直到匹配为止，不加 ？的是一口吃掉整个字符串，然后从最后一个一个地吐出来直到匹配为止

字符串
 a=====b=====b===

        a.*b 将匹配满足条件最长的字符串 a=====b=====b
      
      
      
        工作方式: 
 首先将: a=====b=====b=== 全部吃掉，从右边一个一个地吐出来

        1. a=====b=====b=== 不匹配，吐出一字符

 1. a=====b=====b== 不匹配，再吐出一字符
 2. a=====b=====b= 不匹配，再吐出一字符
 3. a=====b=====b 匹配了，结束。如果再不匹配继续吐，直到没有字符了，匹配失败

        a.*? 将匹配满足条件最短的字符串 a=====b
      
      
      
        工作方式: 

 从左边一个一个地吃掉字符

 1. a 不能匹配表达式，继续吃
 2. a= 不能匹配表达式，继续吃
 3. a== 不能匹配表达式，继续吃
 4. a=== 不能匹配表达式，继续吃
 5. a==== 不能匹配表达式，继续吃
 6. a===== 不能匹配表达式，继续吃
 7. a=====b 呵呵，终于能匹配表达式了，匹配结束，匹配位置留于字符 b 后面，继续其他的匹配。如果不能匹配则一个一个地吃掉整个字符串直到吃完为止若还没有匹配则匹配失败。

        http://tristan-wang.iteye.com/blog/563157
      
      
      
        <http://topic.csdn.net/u/20110509/10/d3172841-d1af-4b62-a7f3-c8cdad70447e.html>
