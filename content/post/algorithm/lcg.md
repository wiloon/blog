---
title: LCG 线性同余生成器
author: "-"
date: 2026-07-14T03:32:04+08:00
lastmod: 2026-07-14T03:32:04+08:00
url: lcg
categories:
  - algorithm
tags:
  - algorithm
  - random
  - java
  - remix
  - AI-assisted
---

## LCG 是什么

线性同余生成器（LCG，Linear Congruential Generator）是历史最悠久、实现最简单的一类伪随机数算法（PRNG，Pseudo-Random Number Generator）。1949 年由 D. H. Lehmer 提出雏形，此后几十年里几乎所有编程语言标准库的 `rand()` 都是它的某个变体。

它的核心是一条递推公式：给定当前状态 `seed`，用一次乘法、一次加法、一次取模算出下一个状态，同时把这个状态作为输出。相比 [Mersenne Twister 随机数算法](./mersenne-twister.md) 和 [Xorshift 伪随机数算法](./xorshift.md)，LCG 实现最简单、状态最小，但随机质量也最差，且不是密码学安全的随机数生成器（不是 CSPRNG，Cryptographically Secure PRNG），不能用在密钥生成、令牌生成等安全场景。

## 递推公式

```text
X(n+1) = (a * X(n) + c) mod m
```

四个参数决定了一个具体的 LCG：

- `X(0)`：种子（seed），初始状态
- `a`：乘数（multiplier）
- `c`：增量（increment）
- `m`：模数（modulus）

`c = 0` 的特例叫乘同余生成器（multiplicative congruential generator，也叫 Lehmer RNG）；`c != 0` 时才是完整的（mixed）LCG。取模运算保证了状态永远落在 `[0, m)` 区间内，序列迟早会回到某个之前出现过的状态并开始循环——这个循环长度就是"周期"，LCG 的周期上限是 `m`。

## 参数怎么选：Hull–Dobell 定理

不是随便选四个数字就能得到一个"好"的 LCG。如果参数选得不好，序列可能远没跑到 `m` 就开始循环，或者呈现明显的规律。Hull–Dobell 定理给出了 `c != 0` 时序列能达到最大周期 `m`（即遍历 `[0, m)` 里所有整数才循环）的充要条件：

1. `c` 与 `m` 互质
2. `a - 1` 能被 `m` 的每一个质因数整除
3. 如果 `m` 是 4 的倍数，`a - 1` 也必须是 4 的倍数

满足这三条，无论种子取什么值（只要在 `[0, m)` 内），序列都能跑满整个周期。[Hash 冲突处理](./hash-collision-resolution.md) 里提到的 Python dict 探测序列 `i = (i*5+1) & mask`（`mask = 2^n - 1`）就是一个精心选出的 LCG：`m = 2^n`、`a = 5`、`c = 1`——`c` 与 `2^n` 互质（1 和任何数都互质），`a - 1 = 4` 能整除 `m` 唯一的质因数 2，且 `m` 是 4 的倍数时 `a - 1 = 4` 也是 4 的倍数，三条全部满足，所以能保证遍历完所有 `2^n` 个槽位，不会死循环。

## 为什么模数常选 2 的幂

取模是 LCG 里最贵的一步。如果 `m` 不是 2 的幂，取模就是一次真正的整数除法，在现代 CPU 上延迟能到二三十个周期；如果 `m = 2^k`，取模等价于"只保留低 k 位"，一次按位与掩码就能算完，几乎不花时间。

`java.util.Random` 就是这么做的：

```java
// java.util.Random, simplified
protected int next(int bits) {
    seed = (seed * 0x5DEECE66DL + 0xBL) & ((1L << 48) - 1); // mod 2^48 via bitmask
    return (int) (seed >>> (48 - bits));
}
```

模数取 `2^48`，乘数 `a = 0x5DEECE66D`、增量 `c = 0xB`，来自 Knuth《The Art of Computer Programming》里给出的一组已知能让周期达到最大值 `2^48` 的常数。详见 [Java Random 随机数](../language/java/java-random.md)。

代价是模数为 2 的幂时，LCG 的低位质量会明显变差（见下一节），这也是为什么 `next(int bits)` 返回的是 `seed` 的**高位**（`seed >>> (48 - bits)`）而不是低位。

## 已知缺陷

### 低位周期短

当 `m = 2^k` 时，LCG 输出的第 `i` 个二进制位（从 0 开始数，最低位是第 0 位）的周期上限只有 `2^(i+1)`：最低位的周期最多是 2（不是 0101 就是 1010 这种简单交替，甚至更差），次低位周期最多是 4，以此类推。这就是为什么很多语言的标准库文档会提醒"不要直接用 `rand() % n` 取低位当随机数"——低位几乎不随机，应该优先用高位。

### 格子结构（lattice structure）

George Marsaglia 在 1968 年的论文《Random Numbers Fall Mainly in the Planes》里证明：把 LCG 连续 `d` 个输出组成的点 `(X(n), X(n+1), ..., X(n+d-1))` 画在 `d` 维空间里，这些点不是均匀散布的，而是精确地落在数量有限的几组平行超平面上。维度越高，平面数目越少、间距越大，统计上的"不随机"就越明显。这是 LCG 与生俱来的结构性缺陷，不是参数没选好，而是"乘法 + 取模"这个递推形式本身决定的，选参数只能缓解、不能根除。

### 不能用于密码学场景

已知任意连续几个输出（有时甚至只要 2~3 个），配合已知的 `a`、`c`、`m`，就能反解出内部状态 `X(n)`，从而预测后续所有输出。密钥生成、令牌生成等安全场景必须用专门的 CSPRNG，比如 Java 的 `java.security.SecureRandom`。

## 和 xorshift、Mersenne Twister 的取舍

| 算法 | 状态大小 | 周期 | 速度 | 随机质量 | 典型应用 |
| ---- | -------- | ---- | ---- | -------- | -------- |
| LCG | 32~64 位 | 通常等于模数 `m` | 很快 | 差，有格子结构、低位周期短等已知缺陷 | `java.util.Random`、glibc `rand()`、Python dict 探测序列 |
| xorshift | 32~128 位 | 最高到 `2^128 - 1` | 最快 | 中等，够用但有已知统计弱点 | HotSpot 默认 `hashCode()`（见 [Xorshift 伪随机数算法](./xorshift.md)） |
| Mersenne Twister | 19968 位 | `2^19937 - 1` | 较慢 | 好，通过大部分标准统计测试 | Python/PHP/R 默认随机数、C++ `std::mt19937`（见 [Mersenne Twister 随机数算法](./mersenne-twister.md)） |

LCG 今天仍然被大量使用，不是因为它随机质量好，而是因为够快、状态够小、实现足够简单，对哈希表探测序列、`java.util.Random` 这类"不追求统计质量、只要求快且可复现"的场景完全够用。真正需要高质量随机数的场景（科学计算、蒙特卡洛模拟）会选 Mersenne Twister，需要密码学安全的场景则要用专门的 CSPRNG，两者都不是 LCG 能替代的。

## 参考

- Lehmer, D. H. (1951). *Mathematical methods in large-scale computing units*. Annals of the Computation Laboratory of Harvard University.
- Knuth, D. E. *The Art of Computer Programming, Volume 2: Seminumerical Algorithms*.
- Marsaglia, G. (1968). *Random Numbers Fall Mainly in the Planes*. Proceedings of the National Academy of Sciences.
