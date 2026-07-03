---
title: "HashMap Initialization 初始化写法"
author: "-"
date: 2026-07-03T14:59:05+08:00
lastmod: 2026-07-03T14:59:05+08:00
url: hashmap-initialization
categories:
  - Java
tags:
  - java
  - remix
  - AI-assisted
---
不同的初始化写法在可读性、序列化兼容性和性能上有一些差异，本文记录双括号初始化写法及其注意事项。本文原本是 [HashMap](./hashmap.md) 的一部分，因主题独立而拆分为单独文章。

## 双括号初始化

HashMap 是一种常用的数据结构，一般用来做数据字典或者 Hash 查找的容器。普通写法一般会这么初始化：

```java
HashMap<String, String> map = new HashMap<String, String>();
map.put("Name", "June");
map.put("QQ", "2572073701");
```

看完这段代码，很多人都会觉得这么写太啰嗦了，对此，还有一种更紧凑的写法：

```java
HashMap<String, String> map = new HashMap<String, String>() {
    {
        put("Name", "June");
        put("QQ", "2572073701");
    }
};
```

看起来优雅了不少，一步到位。这里的双括号到底是什么意思呢？看看下面的代码就知道了：

```java
public class Test {
    /*
    private static HashMap<String, String> map = new HashMap<String, String>() {
        {
            put("Name", "June");
            put("QQ", "2572073701");
        }
    };
    */

    public Test() {
        System.out.println("Constructor called"); // constructor called
    }

    static {
        System.out.println("Static block called"); // static block called
    }

    {
        System.out.println("Instance initializer called"); // instance initializer called
    }

    public static void main(String[] args) {
        new Test();
        System.out.println("=======================");
        new Test();
    }
}
```

输出：

```text
Static block called
Instance initializer called
Constructor called
=======================
Instance initializer called
Constructor called
```

也就是说第一层括号实际是定义了一个匿名内部类（Anonymous Inner Class），第二层括号实际上是一个实例初始化块（instance initializer block），这个块在内部匿名类构造时被执行。这个块之所以被叫做"实例初始化块"是因为它们被定义在了一个类的实例范围内。

上面代码如果是写在 Test 类中，编译后会生成 `Test$1.class` 文件，反编译该文件内容可以看到：

```java
class Test$1 extends HashMap { // creates a subclass of HashMap
    Test$1() { // code from the second pair of braces goes into the constructor
        put("Name", "June");
        put("QQ", "2572073701");
    }
}
```

## 推而广之

这种写法推而广之，在初始化 ArrayList、Set 的时候也可以使用：

```java
List<String> names = new ArrayList<String>() {
    {
        for (int i = 0; i < 10; i++) {
            add("A" + i);
        }
    }
};
System.out.println(names.toString()); // [A0, A1, A2, A3, A4, A5, A6, A7, A8, A9]
```

## Java 7 集合字面量提案

在讨论 Java 7 新特性时，曾经有过让集合支持类似 Ruby、Perl、Python 字面量语法的提案（注：这个提案最终没有被 Java 采纳，目前仍需使用构造函数、`List.of()` 等方式创建集合）：

```java
// current syntax
List<String> list = new ArrayList<String>();
list.add("item");
String item = list.get(0);

Set<String> set = new HashSet<String>();
set.add("item");

Map<String, Integer> map = new HashMap<String, Integer>();
map.put("key", 1);
int value = map.get("key");

// proposed literal syntax (not adopted into the language)
List<String> list = ["item"];
String item = list[0];

Set<String> set = {"item"};

Map<String, Integer> map = {"key" : 1};
int value = map["key"];
```

## 双括号写法的潜在问题

双括号写法的好处很明显，一目了然；但如果这个对象要序列化，可能会导致序列化失败：

- 这种写法是匿名内部类的声明方式，所以引用中持有着外部类的引用。序列化这个集合时外部类也会被一起序列化，当外部类没有实现 `Serializable` 接口时，就会报错。
- 上例中其实是声明了一个继承自 `HashMap` 的匿名子类，而有些序列化方式（例如通过 Gson 序列化为 JSON，或序列化为 XML）无法处理 `HashSet`/`HashMap` 的子类，从而导致序列化失败。

解决办法：重新初始化为一个普通的 `HashMap` 对象：

```java
new HashMap<>(map);
```

这样就可以正常序列化了。

## 执行效率

当一种新的写法出现时，大家都会关心性能怎么样。测试笔记本上分别创建 10,000,000 个 Map，双括号写法与普通写法耗时分别是 1217ms、1064ms，相差约 13%：

```java
public class Test {
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

        for (int i = 0; i < 10000000; i++) {
            HashMap<String, String> map = new HashMap<String, String>();
            map.put("Name", "June");
            map.put("QQ", "2572073701");
        }
        System.out.println(System.currentTimeMillis() - st); // 1064
    }
}
```

## 参考

- [Double Brace Initialization In Java!](http://viralpatel.net/blogs/double-brace-initialization-in-java/)
- [Double Brace Initialization Idiom and its Drawbacks](http://java.dzone.com/articles/double-brace-initialization)
- [Hidden Features of Java](http://stackoverflow.com/questions/15496/hidden-features-of-java)
- [Java 大括号语法糖](http://my.oschina.net/trydofor/blog/79222)
- [Java 7 的新特性](http://code.joejag.com/2009/new-language-features-in-java-7/)
- [java map 双括号初始化方式的问题](http://blog.csdn.net/liubo2012/article/details/8591956)
- [Efficiency of Java "Double Brace Initialization"?](http://stackoverflow.com/questions/924285/efficiency-of-java-double-brace-initialization)
