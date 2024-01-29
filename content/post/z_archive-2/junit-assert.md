---
title: JUnit Assert
author: "-"
date: 2016-03-03T03:17:23+00:00
url: /?p=8769
categories:
  - Inbox
tags:
  - reprint
---
## JUnit Assert
junit中的assert方法全部放在Assert类中,总结一下junit类中assert方法的分类。
  
1.assertTrue/False([String message,]boolean condition);
  
判断一个条件是true还是false。感觉这个最好用了,不用记下来那么多的方法名。
  
2.fail([String message,]);
  
失败,可以有消息,也可以没有消息。
  
3.assertEquals([String message,]Object expected,Object actual);
  
判断是否相等,可以指定输出错误信息。
  
第一个参数是期望值,第二个参数是实际的值。
  
这个方法对各个变量有多种实现。在JDK1.5中基本一样。
  
但是需要主意的是float和double最后面多一个delta的值。
  
4.assertNotNull/Null([String message,]Object obj);
  
判读一个对象是否非空(非空)。
  
5.assertSame/NotSame([String message,]Object expected,Object actual);
  
判断两个对象是否指向同一个对象。看内存地址。
  
7.failNotSame/failNotEquals(String message, Object expected, Object actual)
  
当不指向同一个内存地址或者不相等的时候,输出错误信息。
  
注意信息是必须的,而且这个输出是格式化过的。