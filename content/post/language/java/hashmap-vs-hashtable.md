---
title: "HashMap 与 Hashtable 的区别"
author: "-"
date: 2012-09-21T05:24:11+00:00
lastmod: 2026-07-03T01:02:03+08:00
url: hash/map-table
categories:
  - Java
tags:
  - java
  - remix
  - AI-assisted
---

## HashMap 与 Hashtable 的区别

`Hashtable` 的应用非常广泛，`HashMap` 是新框架中用来代替 `Hashtable` 的类，也就是说建议使用 `HashMap`，不要使用 `Hashtable`。可能你觉得 `Hashtable` 很好用，为什么不用呢？这里简单分析它们的区别。

1. `Hashtable` 的方法是同步的，`HashMap` 未经同步，所以在多线程场合要手动同步 `HashMap`，这个区别就像 `Vector` 和 `ArrayList` 一样。
1. `Hashtable` 不允许 null 值（key 和 value 都不可以），`HashMap` 允许 null 值（key 和 value 都可以）。
1. `HashMap` 去掉了 `Hashtable` 的 `contains(Object value)` 方法，但是加上了 `containsValue()` 和 `containsKey()` 方法。
1. `Hashtable` 使用 `Enumeration`，`HashMap` 使用 `Iterator`。以上只是表面的不同，它们的实现也有很大的不同。
1. `Hashtable` 中 hash 数组默认大小是 11，增加的方式是 `old * 2 + 1`。`HashMap` 中 hash 数组的默认大小是 16，而且一定是 2 的指数。
1. 哈希值的使用不同，`Hashtable` 直接使用对象的 `hashCode`：

```java
int hash = key.hashCode();
int index = (hash & 0x7FFFFFFF) % tab.length;
```

`HashMap` 重新计算 hash 值，并用位与运算代替求模：

```java
int hash = hash(k);
int i = indexFor(hash, table.length);

static int hash(Object x) {
    int h = x.hashCode();
    h += ~(h << 9);
    h ^= (h >>> 14);
    h += (h << 4);
    h ^= (h >>> 10);
    return h;
}

static int indexFor(int h, int length) {
    return h & (length - 1);
}
```

以上只是一些比较突出的区别，当然它们在实现上还有很多不同之处，比如 `HashMap` 对 null 的处理。

`HashMap` 可以看作三个视图：key 的 `Set`、value 的 `Collection`、`Entry` 的 `Set`。`HashSet` 其实就是 `HashMap` 的一个视图，`HashSet` 内部使用 `HashMap` 实现，和 `HashMap` 不同的是它不需要 key 和 value 两个值。

往 `HashSet` 中插入对象，其实只不过是内部做了：

```java
public boolean add(Object o) {
    return map.put(o, PRESENT) == null;
}
```

`HashMap` 是散列映射，它是基于 hash table 的一个实现，可以在常量时间内插入元素，或找出一组 key-value pair。`HashSet` 是散列集，它把查找时间看得很重要，其中所有元素必须要有 `hashCode()`。

## 历史背景与现代 Java 现状

`Hashtable` 从 **JDK 1.0**（1996 年）就存在，是 `java.util` 包中最早的类之一，比 JDK 1.2 引入的 Collections Framework（`HashMap`、`List`、`Set` 等）还早。JDK 1.2 对它做了改造，让它实现新增的 `Map` 接口，但它本身仍保留继承自更古老的 `Dictionary<K,V>` 抽象类。

在现代 Java（截至 Java 26）中，`Hashtable` 依然存在，**没有被废弃（deprecated）或移除**，具备完整的向后兼容性，但官方长期将其列为遗留（legacy）类，不推荐在新代码中使用。

`HashMap` 并不能完全替代 `Hashtable`，要分两种场景看：

- **单线程 / 无并发访问**：`HashMap` 是合适的替代，性能更好，且允许 null key/value。
- **多线程 / 需要线程安全**：`HashMap` 不能替代，因为它非同步。这种场景官方推荐使用 **`ConcurrentHashMap`**（`java.util.concurrent`，JDK 5 引入），而不是 `Hashtable`。`ConcurrentHashMap` 采用分段锁 / CAS 实现，并发性能远优于对整表加锁的 `Hashtable`。

也就是说，现代 Java 中 `Hashtable` 的两个角色被拆分替代：非线程安全场景用 `HashMap`，线程安全场景用 `ConcurrentHashMap`，`Hashtable` 基本没有存在的必要，只是历史遗留、保留兼容性。

**"legacy" 状态没有编译期强制标记**（不是 `@Deprecated`，不会有编译警告），更多体现在文档层面：

- `Hashtable` 的 Javadoc 类说明里明确写着：自 JDK 1.2 起它被改造实现 `Map` 接口纳入 Collections Framework；不需要线程安全时推荐用 `HashMap`，需要高并发线程安全时推荐用 `ConcurrentHashMap`。这段说明从 JDK 1.2 一直保留到最新版本。
- Oracle 官方 Collections Framework 教程里有专门一节 **"Legacy Classes"**，把 `Vector`、`Hashtable`、`Enumeration`、`Properties`、`Stack` 归为 Collections Framework 出现之前就存在、后来被改造纳入框架的遗留类。
- `Enumeration` 接口的 Javadoc 也有类似说明，建议改用 `Iterator`。
- 真正被弃用的 API（如 `Thread.stop()`）会加 `@Deprecated` 注解，`javac -Xlint:deprecation` 会报警告；`Hashtable`、`Vector` 只是"不推荐"，不是"已弃用"，没有这类编译期信号。

参考链接：

- http://oznyang.iteye.com/blog/30690
- http://zhaosoft.iteye.com/blog/243587
- http://coolshell.cn/articles/9606.html

## 维护记录

| 时间       | 修改内容                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 原因                                                                                                                                                                    |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-07-03 | 文件名从中文重命名为 `hashmap-vs-hashtable.md`；标题改为 "HashMap 与 Hashtable 的区别"；清理正文排版，代码块与说明文字分离，代码注释改为符合规范；补充 `lastmod`；标签由 `reprint` 改为 `remix` + `AI-assisted` + `java`；新增「历史背景与现代 Java 现状」一节，说明 `Hashtable` 引入版本（JDK 1.0）、现代 Java 中的地位、`ConcurrentHashMap` 的补充替代关系，以及 "legacy" 状态的具体标记来源（Javadoc 说明、Oracle Legacy Classes 教程，且无 `@Deprecated` 注解） | 文件名含中文，正文格式混乱，标签需符合当前规范；补充 `Hashtable` 历史、现代 Java 中是否可被 `HashMap` 完全替代，以及 legacy 状态在代码/文档中的具体体现，便于理解其现状 |

