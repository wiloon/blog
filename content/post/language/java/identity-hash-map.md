---
title: "IdentityHashMap：基于引用相等的 Map 实现"
author: "-"
date: 2026-07-13T22:29:07+08:00
lastmod: 2026-07-13T22:29:07+08:00
url: identity-hash-map
categories:
  - Java
tags:
  - java
  - collections
  - remix
  - AI-assisted
---

`java.util.IdentityHashMap` 自 **JDK 1.4** 起存在，表面上实现了 `Map` 接口，但官方文档明确说它**不是通用 Map 实现**——判等方式和内部存储结构都和 `HashMap` 不同，只应该用在明确需要"引用相等"语义的少数场景。

## 与 HashMap 的核心区别：引用相等而非逻辑相等

`HashMap` 判断两个 key 是否相同，用的是 `equals()`；`IdentityHashMap` 用的是 `==`，也就是判断是否是同一个对象引用。计算哈希值时也不调用 key 自身的 `hashCode()`，而是统一用 `System.identityHashCode(key)`。

```java
Map<String, Integer> hashMap = new HashMap<>();
Map<String, Integer> identityMap = new IdentityHashMap<>();

String a = new String("key");
String b = new String("key");

hashMap.put(a, 1);
hashMap.put(b, 2);
System.out.println(hashMap.size());     // 1，a.equals(b) 为 true，视为同一个 key

identityMap.put(a, 1);
identityMap.put(b, 2);
System.out.println(identityMap.size()); // 2，a != b，视为两个不同的 key
```

这个差异不仅体现在 key 上，`entrySet()`、`keySet()`、`values()` 这些视图集合里元素的比较，同样是引用相等语义，而不是 `HashMap` 视图那种基于 `equals()` 的语义。

## 内部实现：开放地址法 + 线性探测

`HashMap` 用的是开链法（数组 + 链表/红黑树），而 `IdentityHashMap` 用的是**开放地址法的线性探测**，这一点在 [开链法与开放地址法](../../algorithm/hash-collision-resolution.md) 里也提到过。

它的存储结构是一个**扁平的 `Object[]` 数组**，key 存在偶数下标，紧跟着的奇数下标存对应的 value，而不是像 `HashMap` 那样为每个键值对分配一个 `Node` 对象：

```java
// java.util.IdentityHashMap 源码节选（JDK 21）
private static int hash(Object x, int length) {
    int h = System.identityHashCode(x);
    // Multiply by -254 to use the hash LSB and to ensure index is even
    return ((h << 1) - (h << 8)) & (length - 1);
}

private static int nextKeyIndex(int i, int len) {
    return (i + 2 < len ? i + 2 : 0);
}
```

`get()` 的查找逻辑很直白：算出起始下标，命中就返回，遇到空槽位就说明没有这个 key，否则线性向后探测下一对 key/value：

```java
public V get(Object key) {
    Object k = maskNull(key);
    Object[] tab = table;
    int len = tab.length;
    int i = hash(k, len);
    while (true) {
        Object item = tab[i];
        if (item == k)
            return (V) tab[i + 1];
        if (item == null)
            return null;
        i = nextKeyIndex(i, len);
    }
}
```

因为线性探测依赖"空槽位"来判断查找失败，`null` 不能直接存进数组当 key，否则会和"这里本来就没有值"混淆。`IdentityHashMap` 的解法是用一个内部哨兵对象 `NULL_KEY` 代替真正的 `null` key 存进数组，取值时再转换回 `null`：

```java
static final Object NULL_KEY = new Object();

private static Object maskNull(Object key) {
    return (key == null ? NULL_KEY : key);
}
```

## 负载因子固定为 2/3，且不可配置

`HashMap` 默认负载因子是 0.75，可以通过构造函数调整；`IdentityHashMap` 的负载因子**固定为 2/3**，不提供配置入口。默认容量 32 对应"预期最大元素数"（`expectedMaxSize`）21，这也是无参构造函数背后的换算关系：

```java
private static final int DEFAULT_CAPACITY = 32; // 对应 expectedMaxSize = 21，负载因子 2/3
private static final int MINIMUM_CAPACITY = 4;   // 对应 expectedMaxSize = 2
```

## 典型应用场景

`IdentityHashMap` 的 Javadoc 里明确给出了它的设计初衷：

1. **拓扑保持的对象图变换（topology-preserving object graph transformations）**：比如序列化、深拷贝。这类场景需要维护一张"节点表"记录已经处理过的对象引用，且要求两个逻辑相等但不是同一个对象的实例被视为**不同**节点——这正是 `equals()` 语义会出错、必须用引用相等的地方。`java.io.ObjectOutputStream` 内部处理循环引用时就是类似的思路。
2. **维护代理对象表**：比如调试工具需要为程序中每一个对象维护一个对应的 proxy 对象，这时 key 就是原始对象本身，只关心它是不是同一个实例，不关心它的 `equals()`/`hashCode()` 是怎么实现的。
3. **绕开不可信或有开销的 `equals()`/`hashCode()`**：如果 key 的 `equals()`/`hashCode()` 实现有 bug、开销大，或者对象在插入后被修改导致 `hashCode()` 发生变化（这在 `HashMap` 里会导致该 entry 再也找不到），用引用相等的 `IdentityHashMap` 可以规避这类问题。

## 与 HashMap 对比

| 维度 | HashMap | IdentityHashMap |
| ---- | ------- | ---------------- |
| key 判等 | `equals()` | `==` |
| 哈希来源 | `hashCode()` | `System.identityHashCode()` |
| 冲突解决 | 开链法（链表 / 红黑树） | 开放地址法（线性探测） |
| 存储结构 | `Node<K,V>[]`，每个桶一条链/树 | 扁平 `Object[]`，key/value 交替存放 |
| 负载因子 | 默认 0.75，可配置 | 固定 2/3，不可配置 |
| null key/value | 允许 | 允许（内部用 `NULL_KEY` 哨兵对象表示 null key） |
| 线程安全 | 否 | 否 |
| 典型场景 | 通用 map | 序列化/深拷贝循环引用检测、代理对象表 |

## 使用注意事项

- **不是通用 `Map` 实现**：Javadoc 原话是 "This class is not a general-purpose Map implementation"，只在明确需要引用相等语义时使用。
- **非线程安全**：和 `HashMap` 一样未做同步，多线程结构性修改需要外部同步，或用 `Collections.synchronizedMap()` 包装。
- **fail-fast 迭代器**：结构性修改后继续用旧迭代器遍历会抛 `ConcurrentModificationException`，这一点和 `HashMap`、`Hashtable`（见 [HashMap 与 Hashtable 的区别](./hashmap-vs-hashtable.md)）一致。

更多关于 `HashMap` 本身在 JDK 1.7/1.8 的内部演进，参见 [HashMap](./hashmap.md)；开链法与开放地址法两种冲突解决思路的通用对比，参见 [开链法与开放地址法](../../algorithm/hash-collision-resolution.md)。
