---
title: 'Java HashMap 初始化'
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=6769
categories:
  - Uncategorized
tags:
  - Java

---
## 'Java HashMap 初始化'
如果你接触过不同的语言，从语法和代码层面来说，Java 是一种不折不扣的"臃肿、啰嗦"的语言，从另一方面来说这种臃肿和啰嗦也体现了它严谨的一面，作为适合构建大型、复杂项目的理由之一。

1. HashMap 初始化的文艺写法

HashMap 是一种常用的数据结构，一般用来做数据字典或者 Hash 查找的容器。普通青年一般会这么初始化: 
  
HashMap<String, String> map = new HashMap<String, String>();
  
map.put("Name", "June");
  
map.put("QQ", "2572073701");
  
看完这段代码，很多人都会觉得这么写太啰嗦了，对此，文艺青年一般这么来了: 

```java
HashMap<String, String> map = new HashMap<String, String>() {
  
{
  
put("Name", "June");
  
put("QQ", "2572073701");
  
}
  
};
```

嗯，看起来优雅了不少，一步到位，一气呵成的赶脚。然后问题来了，有童鞋会问: 纳尼？这里的双括号到底什么意思，什么用法呢？哈哈，其实很简单，看看下面的代码你就知道啥意思了。
  
public class Test {
  
02

/*private static HashMap<String, String> map = new HashMap<String, String>() {
  
{
  
put("Name", "June");
  
put("QQ", "2572073701");
  
}
  
};*/
  
09

public Test() {
  
System.out.println("Constructor called: 构造器被调用");
  
}
  
13

static {
  
System.out.println("Static block called: 静态块被调用");
  
}
  
17

{
  
System.out.println("Instance initializer called: 实例初始化块被调用");
  
}
  
21

public static void main(String[] args) {
  
new Test();
  
System.out.println("=======================");
  
new Test();
  
26

}
  
}
  
output:
  
Static block called: 静态块被调用
  
Instance initializer called: 实例初始化被调用
  
Constructor called: 构造器被调用
  
=======================
  
Instance initializer called: 实例初始化被调用
  
Constructor called: 构造器被调用
  
Note: 关于 static 的作用与用法如果不了解，请参考: 
  
http://my.oschina.net/leejun2005/blog/193439#OSC_h3_1 为什么 main 方法是 public static void？

http://my.oschina.net/leejun2005/blog/144349#OSC_h3_2 设计模式之: 聊聊 java 中的单例模式 (Singleton) 

也就是说第一层括弧实际是定义了一个匿名内部类 (Anonymous Inner Class)，第二层括弧实际上是一个实例初始化块 (instance initializer block)，这个块在内部匿名类构造时被执行。这个块之所以被叫做"实例初始化块"是因为它们被定义在了一个类的实例范围内。
  
上面代码如果是写在 Test 类中，编译后你会看到会生成 Test$1.class 文件，反编译该文件内容: 
  
D:\eclipse_indigo\workspace_home\CDHJobs\bin\pvuv\>jad -p Test$1.class
  
// Decompiled by Jad v1.5.8g. Copyright 2001 Pavel Kouznetsov.
  
// Jad home page: http://www.kpdus.com/jad.html
  
// Decompiler options: packimports(3)
  
// Source File Name: Test.java
  
06

package pvuv.zhaopin;
  
08

import java.util.HashMap;
  
10

// Referenced classes of package pvuv.zhaopin:
  
// Test
  
13

class Test$1 extends HashMap // 创建了一个 HashMap 的子类
  
{
  
16

Test$1()
  
{ // 第二个 {} 中的代码放到了构造方法中去了
  
put("Name", "June");
  
put("QQ", "2572073701");
  
}
  
}
  
23

D:\eclipse_indigo\workspace_home\CDHJobs\bin\pvuv\>
  
2. 推而广之

这种写法，推而广之，在初始化 ArrayList、Set 的时候都可以这么玩，比如你还可以这么玩: 
  
List<String> names = new ArrayList<String>() {
  
{
  
for (int i = 0; i < 10; i++) {
  
add("A" + i);
  
}
  
}
  
};
  
System.out.println(names.toString()); // [A0, A1, A2, A3, A4, A5, A6, A7, A8, A9]
  
3. Java7: 增加对 collections 的支持

在 Java 7 中你可以像 Ruby, Perl、Python 一样创建 collections 了。

Note:  (这些集合是不可变的) : 
  
List<String> list = new ArrayList<String>();
  
list.add("item");
  
String item = list.get(0);
  
04

Set<String> set = new HashSet<String>();
  
set.add("item");
  
07

Map<String, Integer> map = new HashMap<String, Integer>();
  
map.put("key", 1);
  
int value = map.get("key");
  
11

// 现在你还可以: 
  
13

List<String> list = ["item"];
  
String item = list[0];
  
16

Set<String> set = {"item"};
  
18

Map<String, Integer> map = {"key" : 1};
  
int value = map["key"];
  
4. 文艺写法的潜在问题

文章开头提到的文艺写法的好处很明显就是一目了然。这里来罗列下此种方法的坏处，如果这个对象要串行化，可能会导致串行化失败。
  
1.此种方式是匿名内部类的声明方式，所以引用中持有着外部类的引用。所以当时串行化这个集合时外部类也会被不知不觉的串行化，当外部类没有实现serialize接口时，就会报错。
  
2.上例中，其实是声明了一个继承自HashMap的子类。然而有些串行化方法，例如要通过Gson序列化为json，或者要串行化为xml时，类库中提供的方式，是无法串行化Hashset或者HashMap的子类的，从而导致串行化失败。解决办法: 重新初始化为一个HashMap对象: 

new HashMap(map);
  
这样就可以正常初始化了。
  
5. 执行效率问题

当一种新的工具或者写法出现时，猿们都会来一句: 性能怎么样？ (这和男生谈论妹纸第一句一般都是: "长得咋样？三围多少？"一个道理:)) 
  
关于这个两种写法我这边笔记本上测试文艺写法、普通写法分别创建 10,000,000 个 Map 的结果是 1217、1064，相差 13%。
  
public class Test {
  
02

public static void main(String[] args) {
  
long st = System.currentTimeMillis();
  
/*
  
for (int i = 0; i < 10000000; i++) {
  
HashMap<String, String> map = new HashMap<String, String>() {
  
{
  
put("Name", "June");
  
put("QQ", "2572073701");
  
}
  
};
  
}
  
System.out.println(System.currentTimeMillis() - st); // 1217
  
*/
  
16

for (int i = 0; i < 10000000; i++) {
  
HashMap<String, String> map = new HashMap<String, String>();
  
map.put("Name", "June");
  
map.put("QQ", "2572073701");
  
}
  
System.out.println(System.currentTimeMillis() - st); // 1064
  
}
  
}
  
6. Refer:

 (1) Double Brace Initialization In Java! http://viralpatel.net/blogs/double-brace-initialization-in-java/

 (2) Double Brace Initialization Idiom and its Drawbacks http://java.dzone.com/articles/double-brace-initialization

 (3) Hidden Features of Java http://stackoverflow.com/questions/15496/hidden-features-of-java

 (4) Java 大括号语法糖 http://my.oschina.net/trydofor/blog/79222

 (5) Java 7 的新特性: http://code.joejag.com/2009/new-language-features-in-java-7/

http://www.iteye.com/news/11490-java-7?page=5

 (6) java map双括号初始化方式的问题 http://blog.csdn.net/liubo2012/article/details/8591956

 (7) Efficiency of Java "Double Brace Initialization"? http://stackoverflow.com/questions/924285/efficiency-of-java-double-brace-initialization