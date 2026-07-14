---
title: Java hashCode 对象哈希值的计算方法
author: "-"
date: 2012-09-21T09:03:40+00:00
lastmod: 2026-07-13T21:12:03+08:00
url: java-hash-code
categories:
  - language
tags:
  - java
  - hash
  - remix
  - AI-assisted
aliases:
  - /p4169/
---

## equals 和 hashCode 的约定

Java 规定了 `hashCode()` 和 `equals()` 之间的约定：

1. 两个对象用 `equals()` 判断相等，则它们的 `hashCode()` 必须相等。
2. 反过来不成立：`hashCode()` 相等的两个对象，`equals()` 未必相等（也就是哈希冲突）。

自定义 `hashCode()` 时必须遵守第 1 条，否则这个对象放进 `HashMap`、`HashSet` 之类基于哈希的容器后会出现"明明 equals 相等却查不到"的 bug。第 2 条则说明哈希冲突是被允许的，容器内部（开链法或开放地址法）本来就要处理冲突，具体见 [开链法与开放地址法](../../algorithm/hash-collision-resolution.md)。

## Object 默认的 hashCode 是怎么算的

没有重写 `hashCode()` 的类，用的是 `Object` 的默认实现，也叫 **identity hash code**（身份哈希码）。一个常见的误解是"默认哈希值就是对象的内存地址"——这在 HotSpot JVM 里并不准确：

- 对象在 GC（尤其是分代 GC 的 minor GC）过程中会被移动到不同的内存区域，如果哈希值直接绑定内存地址，对象移动后哈希值就变了，这会破坏"同一个对象的 hashCode 在生命周期内不能变"的规定。
- 所以 HotSpot 实际上是单独生成、缓存一个哈希值（存在对象头里），和地址无关。生成算法由 JVM 参数 `-XX:hashCode=N` 控制，`N` 有 0~6 几种取值，比如 0 是全局的 Park-Miller 随机数生成器，1 是基于地址计算，4 是直接用地址，其余是自增计数器等方案；**默认值是 5**，用的是 [Marsaglia's xorshift 算法](../../algorithm/xorshift.md)，基于每个线程私有的状态做一次异或位移运算生成伪随机数，和地址、和对象内容都无关。

也就是说，默认的 `hashCode()` 本质上是一个和对象绑定的伪随机数，只是为了效率碰巧可能和地址相关的实现（`-XX:hashCode=1`/`4`）也存在，但不是默认策略。

## 常见类型是怎么重写 hashCode 的

绝大多数会被当作 `HashMap`/`HashSet` key 的类型都重写了 `hashCode()`，不用 identity hash：

- **`String.hashCode()`**：经典的多项式滚动哈希，公式是：

  ```text
  s[0]*31^(n-1) + s[1]*31^(n-2) + ... + s[n-1]
  ```

  选 31 是因为它是一个奇质数，分布效果好，而且 `31 * i` 可以被 JIT 编译器优化成 `(i << 5) - i`，用移位和减法代替乘法，兼顾了分布性和性能。

- **`Integer.hashCode()`**：直接返回自身的 int 值。
- **`Long.hashCode()`**：`(int) (value ^ (value >>> 32))`，把 64 位值的高 32 位和低 32 位异或压缩成 32 位。
- **`Double.hashCode()`**：先用 `doubleToLongBits` 转成 long，再按 `Long` 的方式处理。
- **`Boolean.hashCode()`**：`true` 固定是 1231，`false` 固定是 1237（两个随意选定的质数，只要求两者不同且分布还行）。

## HashMap 里哈希值的完整计算链路

`HashMap` 定位一个 key 该落在哪个桶，并不是只调用一次 `hashCode()`，而是三步：

1. **调用 `key.hashCode()`**：这是虚方法调用（多态），实际执行的是这个 key 所属类重写过的版本（比如上面 `String`/`Integer` 的算法），不是 `Object` 的默认实现。
2. **扰动（spread）**：JDK 8 之后的 `HashMap` 会对原始哈希值做一次高低位混合：

   ```java
   static final int hash(Object key) {
       int h;
       return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
   }
   ```

   `HashMap` 的桶数组长度总是 2 的幂，最终定位桶时只会用到哈希值的低若干位（见下一步），如果不做这次高低位异或，一些高位区分度好、低位却雷同的哈希值会导致大量 key 挤到同一个桶里。这一步和 Swiss Table 里把哈希值拆成 h1/h2 两部分是同一类问题的不同解法，具体见 [Swiss Table 哈希表](../../algorithm/swiss-table.md)。

3. **定位桶**：`index = (table.length - 1) & hash`。因为 `table.length` 是 2 的幂，这个按位与运算等价于取模，但比取模快。

所以完整链路是：`key.hashCode()`（多态，各类自己的算法）→ `HashMap.hash()` 高低位扰动 → `(n - 1) & hash` 定位桶。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-13 | 更新标题为「Java hashCode 对象哈希值的计算方法」；categories 改为 `language`；补充 Object 默认 hashCode（identity hash code）的生成算法、String/Integer/Long/Double/Boolean 等常见类型的 hashCode 算法、HashMap 内部完整的哈希计算链路（hashCode → 扰动 → 定位桶）；添加 `java`、`hash` 标签，删除 `reprint`，加上 `remix`、`AI-assisted`；补充站内互链，其中 Marsaglia's xorshift 算法链接到新建的专门文档 | 原文只讲了 equals/hashCode 契约，没有回答"哈希值具体是怎么算出来的"，内容与标题不符；xorshift 算法值得单独展开，抽成独立文档 |
