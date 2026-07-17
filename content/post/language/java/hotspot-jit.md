---
title: HotSpot JIT 编译器（C1/C2）
author: "-"
date: 2017-03-30T06:06:29+00:00
lastmod: 2026-07-16T02:36:53+08:00
url: hotspot-jit
categories:
  - language
aliases:
  - jvm编译器
  - jvm-compiler
tags:
  - hotspot
  - java
  - jit
  - jvm
  - remix
  - AI-assisted
---

## 背景

OpenJDK 默认的 [HotSpot](./hotspot.md) 虚拟机通过 **解释器 + 即时编译（JIT）** 执行字节码：冷代码先解释运行，热点方法再编译为本地机器码。本文归纳 C1/C2 分工、分层编译与热点探测；JDK 21 之后的 AOT 预热见 [JDK 25 变更汇总](../jdk25-changes-from-jdk21.md)。

## C1 与 C2

HotSpot 内置两个 JIT 编译器，历史上也称 **Client 编译器** 与 **Server 编译器**，对应 **C1** 与 **C2**：

| 编译器 | 特点 |
| ---- | ---- |
| C1 | 编译快，做简单、可靠的优化 |
| C2 | 编译慢，做更重的优化，会依据运行时 profile 做激进优化 |

二者都只编译 **热点代码**（多次调用的方法，或多次执行的循环体），编译前须先做热点探测。

> Client/Server 两套 VM 的划分在 64 位 JDK 上已基本消失：现代 HotSpot 统一走 Server VM，并通过 **分层编译** 把 C1 的快速启动与 C2 的峰值性能结合起来（见下一节）。

## 分层编译（Tiered Compilation）

自 Java 7 起，Server VM **默认启用** 分层编译（`-XX:+TieredCompilation`，一般无需手动开）。HotSpot 用 **5 个执行级别** 在解释器与两个编译器之间过渡：

| Level | 执行方式 | 说明 |
| ---- | -------- | ---- |
| 0 | 解释器 | 带 MethodData（MDO）做 profiling |
| 1 | C1 | 全优化，不采集 profile |
| 2 | C1 | 带调用计数与回边计数 |
| 3 | C1 | 全量 profiling（在 Level 2 基础上采集更多 MDO 信息） |
| 4 | C2 | 全量 profile 引导优化，不再采集 profile |

典型路径：解释器（0）→ C1 带 profiling（2 或 3）→ C2（4）。编译策略会参考 C1/C2 编译队列长度动态调整阈值——例如 C2 队列过长时，可能先在 Level 2 停留，避免在 Level 3 的较慢代码上耗太久。

常用诊断开关：

```text
-Xint                          # 仅解释器
-XX:TieredStopAtLevel=1        # 最高到 C1（无 profiling）
-XX:-TieredCompilation         # 关闭分层，解释器 + C2 两阶段
```

## 热点探测：计数器

HotSpot 使用 **基于计数器** 的热点探测。每个方法关联两类计数器：

### 方法调用计数器

统计的不是方法被调用的绝对次数，而是 **一段时间内的相对调用频率**。若超过时间窗口后调用次数仍不足以触发编译，计数器会 **衰减一半**（热度衰减），避免偶发调用误判为热点。

### 回边计数器

统计方法内 **循环体（回边）** 的执行次数，**没有热度衰减**。当循环很热但方法整体调用不多时，仅靠调用计数器可能永远达不到编译阈值；回边计数器用于触发 **OSR 编译**。

## OSR（栈上替换）

**OSR**（On-Stack Replacement，栈上替换）指在 **方法执行过程中** 把正在运行的栈帧从解释器或低级别编译代码替换为更高级别编译结果，常见于 **循环体很热** 的场景。没有 OSR，长循环可能要等整次方法调用结束才有机会升级。

## 长期运行会不会让所有代码都变成机器码？

一个服务运行几个月不重启，JVM 里是否还会有代码停留在解释执行状态？答案是：会，而且这部分代码不会随运行时长增加而消失。原因是编译触发条件本身与「运行了多久」无关：

- **只看计数器，不看时长**：能否编译取决于上文「热点探测：计数器」里的方法调用计数器与回边计数器是否达到阈值。一段代码路径的调用次数不会因为进程存活得更久而自动增多——异常分支、只在启动时跑一次的初始化逻辑、极少访问的管理接口，无论运行一天还是一年，调用次数都不会变化，因此永远达不到编译阈值，永远解释执行。
- **计数器还会衰减**：方法调用计数器有热度衰减（见上文），调用不密集的代码即使总调用次数在变长的运行时间里慢慢累积，也可能因为衰减而始终攒不到阈值。
- **已编译代码也可能被打回解释执行**：这类代码触发了 **去优化（deoptimization）**——例如 C2 基于类层次分析（CHA）或类型 speculation 做的激进假设被后续加载的类打破，会触发 uncommon trap，把该方法打回解释器执行。是否会重新编译，取决于之后这段代码是否再次变热。
- **Code Cache 满了会让 JIT 直接停止编译**：`-XX:ReservedCodeCacheSize` 有上限，编译产物把 code cache 占满后（日志可见 `CodeCache is full`），即使是真正的热点方法也无法产出新的编译结果，只能继续留在解释执行，直到 sweeper 回收出空间。

综合来看，长时间运行只会让 **真正频繁执行** 的那部分代码逐步被识别并编译，其余天然低频的代码路径会一直保持解释执行，这也是刻意的设计取舍：为很少执行的代码做编译优化，收益覆盖不了编译本身的开销。

## JDK 21 到 JDK 25 的相关变化

上文描述的 C1/C2 架构与计数器机制 **未被替换**，但 JDK 21 之后有几处与 JIT 密切相关的演进：

### AOT 类加载与方法剖析（JEP 483 / 514 / 515）

- **JDK 24（JEP 483）**：AOT 缓存可保存类加载与链接结果，缩短冷启动。
- **JDK 25（JEP 515）**：训练运行中采集的 **方法执行 profile** 可写入 AOT 缓存；生产启动时 JIT 能更早、更准地编译热点，缩短 warmup。在线 profiling 与 JIT 仍会随运行继续，与 AOT profile 互补。

详见 [JDK 21 升级到 JDK 25 的变更汇总](../jdk25-changes-from-jdk21.md)；JDK 26 对 AOT 对象缓存的扩展见 [JDK 26 相对 JDK 25 的变化](./jdk-26.md)。相关 JVM 参数见 [HotSpot JVM 启动参数](./hotspot-options.md)。

### 实验性 Graal JIT 已移除

JDK 17（JEP 410）移除了基于 Graal 的 **实验性 JIT**；JDK 25 官方迁移文档再次确认该路径不再提供。日常 OpenJDK 的 JIT 仍是 **C1 + C2**，不是 Graal 编译器。

### 编译策略的回归与修复

JEP 515 引入后，大应用在部分 JDK 25 早期构建上曾出现编译吞吐下降（大量代码长时间停留在解释器），根因是编译策略中阈值缩放逻辑调整不当（[JDK-8368071](https://bugs.openjdk.org/browse/JDK-8368071)），后续版本已修复。若从 JDK 21 升级并关注 warmup，建议用目标负载做回归对比。

## 参考

- [Oracle：HotSpot 性能增强（分层编译）](https://docs.oracle.com/en/java/javase/25/vm/java-hotspot-virtual-machine-performance-enhancements.html)
- [OpenJDK：JEP 515 Ahead-of-Time Method Profiling](https://openjdk.org/jeps/515)
- [How Tiered Compilation works in OpenJDK（Microsoft）](https://devblogs.microsoft.com/java/how-tiered-compilation-works-in-openjdk/)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-19 | 文件重命名为 `jvm-compiler.md`；url 改为 `jvm-compiler`；补充分层编译、OSR、JDK 25 AOT 剖析与 Graal 移除说明 | 原文仅覆盖 C1/C2 与计数器，术语与新版 JDK 脱节 |
| 2026-06-19 | 增加 hotspot-options 互链 | JVM 文档职责拆分 |
| 2026-07-15 | 从 `content/post/cs/` 移至 `content/post/language/java/`；文件重命名为 `hotspot-jit.md`，url 改为 `hotspot-jit`，旧 url `jvm-compiler` 加入 aliases | 内容专指 HotSpot 的 JIT（C1/C2），原名 `jvm-compiler` 偏泛，易与 javac 或跨 JVM 通用编译混淆 |
| 2026-07-16 | 补充「长期运行会不会让所有代码都变成机器码」一节，串联计数器阈值、计数器衰减、去优化回退解释执行、Code Cache 上限四点 | 解答长时间运行的服务是否会让代码逐渐全部编译为机器码的疑问 |
