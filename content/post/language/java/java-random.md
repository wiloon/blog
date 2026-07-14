---
title: Java Random 随机数
author: "-"
date: 2012-05-25T07:56:45+00:00
lastmod: 2026-07-13T21:35:00+08:00
url: java-random
categories:
  - language
tags:
  - java
  - random
  - remix
  - AI-assisted
---

## Java 里获取随机数的几种方式

在 Java 中，获取随机数广义上有三种途径：

1. 用 `System.currentTimeMillis()` 拿到当前时间的毫秒数，当作一个"看起来随机"的数字。
2. 用 `Math.random()`，返回一个 `[0, 1)` 之间均匀分布的 `double` 值。
3. 用 `java.util.Random` 类，功能更完整的专业随机数工具类。

`Math.random()` 内部其实也是委托给一个 `java.util.Random` 实例（每个类第一次调用时惰性初始化一个内部单例），所以第 2、3 种本质上是同一套实现。

## java.util.Random 的用法

`Random` 有两种构造方法：

- `Random()`：用当前时间 `System.currentTimeMillis()` 作为种子（seed）。
- `Random(long seed)`：用指定的 `seed` 初始化。

产生 `Random` 对象后，调用 `nextInt()`、`nextLong()`、`nextFloat()`、`nextDouble()`、`nextBoolean()`、`nextGaussian()`（返回符合高斯/正态分布的 `double`）等方法获得不同类型的随机数。

如果两个 `Random` 对象用相同的种子、并且以相同的顺序调用相同的方法，它们返回的值会完全相同——因为随机数序列完全由种子和内部算法决定：

```java
import java.util.Random;

public class TestRandom {
    public static void main(String[] args) {
        Random random1 = new Random(100);
        System.out.println(random1.nextInt());
        System.out.println(random1.nextFloat());
        System.out.println(random1.nextBoolean());

        Random random2 = new Random(100);
        System.out.println(random2.nextInt()); // 和 random1 完全一样
        System.out.println(random2.nextFloat());
        System.out.println(random2.nextBoolean());
    }
}
```

指定范围内的随机数，可以用取模运算符 `%`（配合 `Math.abs` 避免负数）：

```java
Random random = new Random();
for (int i = 0; i < 10; i++) {
    System.out.println(Math.abs(random.nextInt()) % 10);
}
```

或者用 `Math.random()` 配合四则运算，生成 `[min, max]` 之间的整数：

```java
long min = 1000;
long max = 9999;
long value = Math.round(Math.random() * (max - min) + min);
```

## java.util.Random 内部用的是什么算法

`java.util.Random` **不是** Mersenne Twister，也不是 [Xorshift 伪随机数算法](../../algorithm/xorshift.md) ，而是一种**线性同余法**（LCG，Linear Congruential Generator）——历史最悠久、实现最简单的一类伪随机数算法。

`java.util.Random` 的具体递推公式（源码里可以直接看到）：

```java
seed = (seed * 0x5DEECE66DL + 0xBL) & ((1L << 48) - 1);
```

也就是经典 LCG 的形式 `seed = (a * seed + c) mod m`，其中乘数 `a = 0x5DEECE66D`、增量 `c = 0xB`、模数 `m = 2^48`（用 48 位掩码实现取模）。这几个常数不是随便选的，来自 Knuth《The Art of Computer Programming》里给出的一组已知能让周期达到最大值 `2^48` 的参数——只要种子非零，序列要循环 `2^48` 次才会重复。`Random(long seed)` 构造方法会先对传入的种子做一次 `scramble`（和 `0x5DEECE66DL` 异或），避免用户传入的种子直接暴露在内部状态里。

`nextInt()` 等方法在这个 48 位种子的基础上，取高位的若干比特转换成目标类型（比如 `nextInt()` 取高 32 位）。

这个算法速度快、实现简单，但周期短（`2^48`）、随机质量一般，不能用于密码学场景（`java.security.SecureRandom` 才是密码学安全的随机数生成器）。要更长周期、更好统计质量的伪随机数，通常会选 [Mersenne Twister 随机数算法](../../algorithm/mersenne-twister.md)——但 Java 标准库的 `Random` 从 JDK 1.0 就是 LCG，出于兼容性至今没有换过实现（`Random(long seed)` + 相同调用序列必须能复现完全相同的结果，这是公开文档承诺的行为，换算法就是破坏兼容性）。

## 参考

- [JAVA产生指定范围的随机数 - CSDN](http://blog.csdn.net/herrapfel/article/details/1885016)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-13 | 文件重命名为 `java-random.md`；url 由 `java获取随机数` 改为 `java-random`；标题改为「Java Random 随机数」；categories 改为 `language`；清理原文重复冗余的代码示例与格式问题，修正 `nextGoussian` 笔误为 `nextGaussian`；新增 `java.util.Random` 内部算法一节，说明其使用线性同余法（LCG）而非 Mersenne Twister 或 xorshift，并给出具体递推公式；添加 `java`、`random` 标签，删除 `reprint`，加上 `remix`、`AI-assisted` | 原文件名含中文，不符合文件名规范；原文只讲用法，没有回答"内部用什么算法"这个问题 |
