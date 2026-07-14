---
title: Xorshift 伪随机数算法
author: "-"
date: 2026-07-13T21:20:00+08:00
lastmod: 2026-07-14T05:15:48+08:00
url: xorshift
categories:
  - algorithm
tags:
  - algorithm
  - random
  - java
  - remix
  - AI-assisted
---

## Xorshift 是什么

Xorshift 是 George Marsaglia 在 2003 年发表的一类伪随机数生成算法（PRNG，Pseudo-Random Number Generator），核心思路是反复对一个整数状态做"自己和自己移位后的版本"做异或（XOR），只用异或和移位两种运算就能生成看起来随机的数字序列。

它属于线性反馈移位寄存器（LFSR，Linear Feedback Shift Register）的一种变体，相比传统的线性同余法（LCG，Linear Congruential Generator，也就是很多语言标准库 `rand()` 背后的算法）不需要乘法和取模，只用位运算，速度快很多；相比更复杂的 Mersenne Twister（`java.util.Random` 用的不是这个，但 Python、PHP 等语言的默认随机数用的是它），实现更简单、状态更小。

代价是随机质量不如 Mersenne Twister，不能用于密码学场景（不是 CSPRNG，Cryptographically Secure PRNG），但对哈希表、游戏、模拟、需要"看起来随机就行"的场景完全够用，且速度优势明显。

## 基本算法

最经典的 32 位 xorshift 只需要一个非零的整数状态 `x` 和三次移位异或：

```c
uint32_t xorshift32(uint32_t x) {
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    return x;
}
```

每次调用把上一次的输出作为下一次的输入（状态），就能生成一串伪随机序列。三个移位量 `(13, 17, 5)` 不是随便选的——Marsaglia 在论文里给出了一批能保证生成的序列覆盖 `2^32 - 1` 个非零状态（即最大周期）的移位量组合，`(13, 17, 5)` 是其中常用的一组。如果移位量选得不好，会导致序列过早循环或者分布不均匀。

64 位状态的版本同理，只是移位量不同：

```c
uint64_t xorshift64(uint64_t x) {
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    return x;
}
```

## 为什么异或和移位比乘除法快

xorshift 只用异或和移位，LCG 需要乘法，还常常需要取模——这两类操作在 CPU 上的实际开销差距很大，不只是"位运算听起来更底层"这种直觉。

- **异或、移位**：现代 CPU 上通常 1 个时钟周期就能算完，而且是完全流水线化的，每个周期都能发射一条新指令；超标量 CPU 往往还有好几个 ALU 端口能并行执行这类运算，吞吐量很高。
- **乘法**：x86 上整数乘法延迟通常在 3~5 个周期，比位运算贵不少，虽然乘法单元本身也是流水线化的（吞吐量还行），但很多简单的嵌入式处理器根本没有硬件乘法器，要靠"逐位移位相加"的循环在软件里模拟，代价是位宽的线性倍数。
- **取模（本质是除法）**：这是真正的大头。整数除法在 x86 上 32 位延迟大概 20~26 个周期，64 位能到 40+ 周期，而且除法单元通常没有完全流水线化，前一条没算完，后一条往往发射不了。根本原因是除法算法本身是顺序依赖的——就像小学的竖式除法，商的高位必须先求出来才能算下一位，没法像乘法那样把部分积并行展开。

LCG 的递推式 `seed = (a * seed + c) mod m` 一次乘法已经比位运算贵好几倍，如果 `m` 不是 2 的幂，取模还要再付一次除法的高昂代价——这也是为什么 [Java Random 随机数](../language/java/java-random.md) 里 `java.util.Random` 特意把模数选成 `2^48`，好把取模换成一次按位与掩码，绕开除法。而 xorshift 全程只有异或和移位，每一步都是 1 周期、全流水线、多端口并行，这才是"速度快很多"的真正原因。

## 为什么异或加移位能生成"随机"序列

单独看，异或和移位都是完全确定、可逆的位运算，不像乘法或加法那样会产生进位、溢出这些"打乱"数据的副作用。xorshift 的技巧在于：把状态的一部分（移位后的版本）和原始状态做异或，相当于让状态的高位和低位互相"搅拌"——右移会把高位的信息传播到低位，左移则相反，三次不同方向、不同幅度的移位加异或，多轮之后状态里的每一位都或多或少被其他位污染过，看起来就失去了规律性。

数学上，xorshift 的每一步都可以看成状态向量在 `GF(2)`（模 2 的有限域）上乘一个固定的可逆矩阵，序列的周期由这个矩阵的阶决定，选择好的移位量本质上是在选一个阶尽可能大（接近 `2^n - 1`）的矩阵。

## 和 Java 的关系

`java.util.Random` 本身用的不是 xorshift，而是一种线性同余法（48 位种子，`seed = (seed * 0x5DEECE66DL + 0xB) & ((1L << 48) - 1)`）。

但 HotSpot JVM 生成对象默认 `hashCode()`（identity hash code）时用的正是 Marsaglia's xorshift：每个线程维护一份私有的 xorshift 状态，每次有对象要生成默认哈希值，就推进一次这个线程本地的 xorshift 序列，取结果作为哈希值。这样做每个线程互不干扰（不需要加锁竞争一个全局种子），生成速度也远快于取内存地址或全局随机数发生器。具体见 [Java hashCode 对象哈希值的计算方法](../language/java/java-hash-code.md#object-默认的-hashcode-是怎么算的)。

### HotSpot 用的具体变体：四状态 xor128

前面「基本算法」一节讲的是单个状态变量的 `xorshift32`/`xorshift64`；HotSpot 实际用的是 Marsaglia 论文里另一个示例——四状态版本，通常叫 `xor128`，用四个 32 位整数 `x, y, z, w` 轮转：

```c
uint32_t t = x ^ (x << 11);
x = y; y = z; z = w;
w = (w ^ (w >> 19)) ^ (t ^ (t >> 8));
return w;
```

HotSpot 的 native `Thread` 类（是 JVM 内部的线程对象，不是 `java.lang.Thread`）专门加了四个字段 `_hashStateX`、`_hashStateY`、`_hashStateZ`、`_hashStateW`，就是为了存这四个状态。这四个字段是 `Thread` 这个 C++ 对象的普通成员变量，`Thread` 对象本身分配在 native 内存（C-heap）里，和线程 ID、TLAB 指针这些线程私有数据放在一起——**不是** Java 方法调用用的那个调用栈（call stack），跟"栈"这种内存区域没关系，纯粹是"这个字段挂在哪个线程对象上"的问题。线程创建时做一次性初始化：`_hashStateX` 用 `os::random()`（操作系统随机源）取值，保证不同线程、不同进程的起点不一样；`_hashStateY`、`_hashStateZ`、`_hashStateW` 是固定常量 `842502087`、`0x8767`、`273326509`，照抄自 Marsaglia 论文示例代码里的初始值。每次要生成一个默认哈希值，就用当前线程这四个字段跑一轮上面的运算：结果既是本次的哈希值，也顺带更新了这四个字段，作为下一次调用的新状态。

### 为什么状态挂在线程上，不是挂在对象上

直觉上可能会觉得，既然算的是"这个对象的哈希值"，状态是不是该跟着对象走？但 identity hash code 只会**求值一次**——第一次被用到时（调用 `hashCode()`、`System.identityHashCode()`，或者对象被用作锁）就算出来，写进对象头（mark word）缓存住，之后终身不变。既然只求一次，就没有"这个对象自己的一段随机数序列"需要维护，需要的只是"在算这一次的当下，找一个足够快、足够不可预测的数字来源"。

真正决定"挂在哪里"的是并发安全：如果全 JVM 只有一份共享的 xorshift 状态，多个线程同时创建对象、同时触发哈希值计算时，就得靠 CAS 或加锁来串行化对这份共享状态的读写，变成一个全局竞争点。把状态拆成每个线程私有一份，各线程推进各自的序列，互不干扰、零同步开销——这和 TLAB（线程本地分配缓冲区）解决对象分配竞争问题的思路是一样的。所以哈希值最终确实是"属于这个对象"的（算出来就缓存住，伴随对象一生不变），但产生这个值时用的随机数来源，只是"当时恰好是哪个线程在跑"，跟对象本身的内容、地址都没有关系。

## 参考

- Marsaglia, G. (2003). *Xorshift RNGs*. Journal of Statistical Software, 8(14). https://doi.org/10.18637/jss.v008.i14
- [OpenJDK synchronizer.cpp（`get_next_hash` 实现）](https://github.com/openjdk/jdk/blob/master/src/hotspot/share/runtime/synchronizer.cpp)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-14 | 澄清 `_hashStateX/Y/Z/W` 四个字段挂在 native `Thread` 对象的 native 内存（C-heap）上，明确不是 Java 调用栈 | 读者提问是否为线程栈上的字段，原文表述容易引起歧义 |
