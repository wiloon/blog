---
title: BeforeClass、AfterClass、Before与After示例
author: wiloon
type: post
date: 2016-01-27T06:49:03+00:00
url: /?p=8716
categories:
  - Uncategorized

---
http://www.cnblogs.com/xhzi/archive/2011/05/29/2061825.html

【测试目的】

测试加载顺序

【代码片段】

public class TestIt {
  
private TestJUnit tju = null;

@BeforeClass
  
public static void enter() {
  
System.out.println(&#8220;进来了！&#8221;);
  
}

@Before
  
public void init() {
  
System.out.println(&#8220;正在初始化。。&#8221;);
  
tju = new TestJUnit();
  
System.out.println(&#8220;初始化完毕！&#8221;);
  
}

@Test
  
public void testit() {
  
tju.run();
  
}

@After
  
public void destroy() {
  
System.out.println(&#8220;销毁对象。。。&#8221;);
  
tju = null;
  
System.out.println(&#8220;销毁完毕！&#8221;);
  
}

@AfterClass
  
public static void leave() {
  
System.out.println(&#8220;离开了！&#8221;);
  
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