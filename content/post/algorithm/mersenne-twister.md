---
title: Mersenne Twister 随机数算法
author: "-"
date: 2026-07-13T21:40:00+08:00
lastmod: 2026-07-13T21:40:00+08:00
url: mersenne-twister
categories:
  - algorithm
tags:
  - algorithm
  - random
  - remix
  - AI-assisted
---

## Mersenne Twister 是什么

Mersenne Twister（简称 MT，梅森旋转算法）是松本真（Makoto Matsumoto）和西村拓士（Takuji Nishimura）在 1997 年发表的伪随机数生成算法（PRNG），名字来自它的周期长度——最常用的变体 **MT19937** 的周期是 `2^19937 - 1`，这是一个梅森素数（Mersenne prime，形如 `2^p - 1` 的素数）。

它是目前应用最广泛的通用 PRNG 之一：Python、PHP、R、Ruby、Excel 的默认随机数生成器用的都是 MT19937；C++11 标准库 `<random>` 里的 `std::mt19937` 也是它。相比 [Xorshift 伪随机数算法](./xorshift.md) 和 [Java Random 随机数](../language/java/java-random.md) 里的线性同余法（LCG），MT 的随机质量（统计意义上的均匀性、独立性）好得多，周期也长得多，代价是内部状态更大、实现更复杂。

和 xorshift、LCG 一样，MT **不是**密码学安全的随机数生成器（不是 CSPRNG）：观察连续 624 个输出就能反推出完整的内部状态，从而预测后续所有输出，所以不能用在密钥生成、令牌生成等安全场景，这些场景要用专门的 CSPRNG（比如 Java 的 `java.security.SecureRandom`）。

## 核心设计

### 状态：624 个 32 位整数

MT19937 的内部状态是一个长度 624 的 32 位整数数组，一共 `624 * 32 = 19968` 位，比 xorshift（几十到几百位状态）或 LCG（48 位状态）大得多——这也是"随机质量更好"的代价之一：状态越大，能表达的不同序列就越多，越不容易在短序列内暴露周期性规律。

### 生成流程分两步

1. **状态推进（twist）**：每消耗完 624 个输出后，对整个状态数组做一次"扭转"变换，生成下一批 624 个新状态。扭转的核心是对相邻状态做位组合，再乘上一个固定的常数矩阵（用移位和异或实现，不是真正的矩阵乘法，效果类似线性反馈移位寄存器）。
2. **输出提炼（tempering）**：每次取值时，不直接返回状态数组里的原始整数，而是先对它做一轮固定的移位、掩码、异或组合（tempering），目的是消除原始状态里明显的统计规律，让直接输出的比特看起来更均匀。

这种"大状态 + 定期批量刷新 + 每次输出前额外处理"的设计，是 MT 和 xorshift/LCG 这类"每次输出就是一次状态更新"的算法的主要区别。

### 为什么周期这么长

LCG 的周期上限是模数 `m`（`java.util.Random` 是 `2^48`），xorshift32 的周期上限是 `2^32 - 1`；而 MT19937 用一个 624 个 32 位整数组成的巨大状态空间，配合精心设计的扭转变换，让周期达到 `2^19937 - 1`——这是一个天文数字，实际使用中不可能真的把周期跑完，可以认为在任何实际应用场景下都"不会重复"。

## 和 xorshift、LCG 的取舍

| 算法 | 状态大小 | 周期 | 速度 | 随机质量 | 典型应用 |
| ---- | -------- | ---- | ---- | -------- | -------- |
| LCG | 48~64 位 | 通常 `2^48` 左右 | 很快 | 一般，有明显统计缺陷 | `java.util.Random` |
| xorshift | 32~128 位 | 最高到 `2^128 - 1` | 最快 | 中等，够用但有已知统计弱点 | HotSpot 默认 hashCode（[Java hashCode 对象哈希值的计算方法](../language/java/java-hash-code.md)）、游戏/模拟 |
| Mersenne Twister | 19968 位 | `2^19937 - 1` | 较慢（状态大、tempering 有额外开销） | 好，通过大部分标准统计测试 | Python/PHP/R 默认随机数、C++ `std::mt19937` |

选择哪种算法本质是在"速度"和"随机质量/周期"之间取舍：哈希表内部生成对象哈希值这种场景，只需要"看起来随机、足够快"，用 xorshift 绰绰有余；而科学计算、蒙特卡洛模拟这类对随机数统计性质要求高、需要跑大量样本的场景，会更倾向选 Mersenne Twister。

## 参考

- Matsumoto, M., & Nishimura, T. (1998). *Mersenne Twister: a 623-dimensionally equidistributed uniform pseudo-random number generator*. ACM Transactions on Modeling and Computer Simulation.
