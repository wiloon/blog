---
title: BeforeClass、AfterClass、Before与After示例
author: "-"
date: 2016-01-27T06:49:03+00:00
url: /?p=8716
categories:
  - Inbox
tags:
  - reprint
---
## BeforeClass、AfterClass、Before与After示例
http://www.cnblogs.com/xhzi/archive/2011/05/29/2061825.html

【测试目的】

测试加载顺序

【代码片段】

public class TestIt {
  
private TestJUnit tju = null;

@BeforeClass
  
public static void enter() {
  
System.out.println("进来了！");
  
}

@Before
  
public void init() {
  
System.out.println("正在初始化。。");
  
tju = new TestJUnit();
  
System.out.println("初始化完毕！");
  
}

@Test
  
public void testit() {
  
tju.run();
  
}

@After
  
public void destroy() {
  
System.out.println("销毁对象。。。");
  
tju = null;
  
System.out.println("销毁完毕！");
  
}

@AfterClass
  
public static void leave() {
  
System.out.println("离开了！");
  
}
  
}
  
【运行结果】
  
进来了！
  
正在初始化。。
  
初始化完毕！
  
Hello,JUnit
  
销毁对象。。。
  
销毁完毕！
  
离开了！

【小小总结】

1. 注意加载和执行顺序