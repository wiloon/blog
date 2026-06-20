---
title: HotSpot JVM 简介
author: "-"
date: 2026-05-31T07:25:07+08:00
lastmod: 2026-06-19T22:27:49+08:00
url: hotspot
categories:
  - language
tags:
  - AI-assisted
  - hotspot
  - java
  - jvm
  - openjdk
  - remix
---

## 背景

OpenJDK 发行版里默认的 Java 虚拟机实现是 **HotSpot**（C++）。你安装的 `java` 命令、容器里的 JDK 镜像，除非明确换用 OpenJ9 或 GraalVM Native Image，否则跑的就是 HotSpot。

**本文及子文描述 HotSpot**，不适用于 OpenJ9 的参数名、GC 实现与诊断工具。Java 领域还有哪些 JVM、如何选型，见 [Java 虚拟机生态与选型](./jvm.md)。

## HotSpot 是什么

HotSpot 得名于 **热点探测**（hot spot detection）：大部分时间只执行少量代码，JIT 优先编译这些热点方法。内置 **解释器**、**C1** 与 **C2** 两个 JIT 编译器，默认通过 **分层编译** 在启动速度与峰值性能之间折中。

| 对比 | HotSpot | Eclipse OpenJ9 | GraalVM Native Image |
| ---- | ------- | -------------- | --------------------- |
| 典型形态 | OpenJDK 默认 `java` | IBM Semeru | `native-image` 产物 |
| JIT | C1 + C2 | 自有 JIT | 构建期 AOT，无运行时 JIT |
| 常用诊断 | jcmd、JFR、Attach | 自有工具 | 与传统 JVM 排障不同 |

## 核心组成

```text
Java 源码 → javac → .class
                    ↓
              类加载（见 [classloader](./classloader.md)）
                    ↓
         解释执行 + C1/C2 即时编译（见 [jvm-compiler](../../cs/jvm-compiler.md)）
                    ↓
         运行时数据区（堆、栈、元空间等）
                    ↓
         垃圾收集器（见 [java-gc](./java-gc.md)）
```

启动与调优通过 **JVM 启动参数**（`-X`、`-XX`）配置，见 [HotSpot JVM 启动参数](./hotspot-options.md)。

## 内置诊断能力

不另挂 agent jar 也可使用的 HotSpot 能力：

- **AttachListener** + **Diagnostic Command**（[jcmd](./jcmd.md)、[Attach API](./attach-api.md)）
- **JPDA / JVMTI** 调试后端（[JPDA](./java-debug-JPDA.md)、[JVMTI](./jvmti.md)）
- **JFR**（[Java Flight Recorder](./java-flight-recorder-jfr.md)）

动态挂外部 agent（BTrace、Arthas）同样依赖 HotSpot 的 attach 与 instrument 实现。

## 博客内相关文章

| 主题 | 文章 |
| ---- | ---- |
| JVM 生态与选型 | [jvm](./jvm.md) |
| JIT / 分层编译 / C1·C2 | [jvm-compiler](../../cs/jvm-compiler.md) |
| 启动参数（堆、GC、日志、JIT） | [hotspot-options](./hotspot-options.md) |
| GC 概念与算法 | [java-gc](./java-gc.md)、[jvm-gc](./jvm-gc.md) |
| 类加载 | [classloader](./classloader.md) |
| Attach / jcmd | [attach-api](./attach-api.md)、[jcmd](./jcmd.md) |
| 字节码织入 | [java-asm](./java-asm.md) |
| 开发期热替换 | [DCEVM 与 HotSwapAgent](../../cs/dcevm-hotswapagent.md) |
| Safepoint | [safepoint](../../other/safepoint.md) |
| JDK 版本变更 | [JDK 21→25](../jdk25-changes-from-jdk21.md)、[JDK 26](./jdk-26.md) |

## 参考

- [OpenJDK HotSpot](https://openjdk.org/projects/hotspot/)
- [Java HotSpot VM Options](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-19 | 明确 HotSpot 边界；索引表增加 hotspot-options、jvm-compiler | 与 jvm.md 职责拆分 |
