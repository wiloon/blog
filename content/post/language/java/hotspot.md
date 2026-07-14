---
title: HotSpot JVM 简介
author: "-"
date: 2026-05-31T07:25:07+08:00
lastmod: 2026-06-27T04:52:28+08:00
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

## 历史

HotSpot 的技术 lineage 来自 **Self / Strongtalk** 一脉的动态编译与热点探测。**Longview Technologies**（对外也称 Animorphic）1994 年成立，1997 年 2 月被 Sun 收购；收购后 Sun 在其 VM 技术上为 Java 编写更强的 JIT（C2 等），因运行时持续探测并优化**热点代码**而得名 HotSpot。

| 时间 | 节点 |
| ---- | ---- |
| 1999-04 | 作为独立产品 **Java HotSpot Performance Engine** 首次发布，可配合 JDK 1.2 使用 |
| 2000-05 | **JDK 1.3** 起 HotSpot 成为 JDK **默认** VM（Classic VM 仍可选） |
| 2002-02 | **JDK 1.4** 起移除 Classic VM，HotSpot 成为 **唯一** JVM 实现 |
| 2006-11 | Sun 以 GPL v2 开源 HotSpot（与 OpenJDK 一并发布） |
| 2010 起 | Oracle 收购 Sun 后继续维护；OpenJDK 为参考实现 |

JDK 1.0～1.2 附带的是 Sun 自研的 **Classic VM**（以解释执行为主，后期部分平台有 JIT），与今天的 HotSpot 不是同一套实现。版本脉络见 [Java 版本历史](./java-version-history.md)；各 JDK 版本要点见 [JDK 1.0](./jdk-1.0.md)、[JDK 1.4](./jdk-1.4.md) 等。

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
         垃圾收集器（见 [java-gc](./gc.md)）
```

启动与调优通过 **JVM 启动参数**（`-X`、`-XX`）配置，见 [HotSpot JVM 启动参数](./hotspot-options.md)。

## 内置诊断能力

不另挂 agent jar 也可使用的 HotSpot 能力：

- **AttachListener** + **Diagnostic Command**（[jcmd](./jcmd.md)、[Attach API](./attach-api.md)）
- **JPDA / JVMTI** 调试后端（[JPDA](./java-debug-JPDA.md)、[JVMTI](./jvmti.md)）
- **JFR**（[Java Flight Recorder](./java-flight-recorder-jfr.md)）

动态挂外部 agent（BTrace、Arthas）同样依赖 HotSpot 的 attach 与 instrument 实现。

## libjvm.so 与 JVM 主体

`libjvm.so` 才是 JVM 的真正主体。`/usr/bin/java` 只是个极小的启动器（几 KB），它的全部工作是解析参数、定位 JRE 安装路径，然后 `dlopen("libjvm.so")`：

```text
java -jar app.jar
  ↓
java 启动器（几 KB）
  → 找到 $JAVA_HOME/lib/server/libjvm.so
  → dlopen(libjvm.so)   ← JVM 主体进入内存
  ↓
JVM 初始化：堆、栈、方法区、GC、JIT
  ↓
读 MANIFEST.MF → 加载主类 → ...
```

`libjvm.so` 位于 `$JAVA_HOME/lib/server/libjvm.so`，通常是 JDK 安装里最大的单个文件（数十 MB）。它包含：

| 组成 | 说明 |
| ---- | ---- |
| 字节码解释器 | 执行 `.class` 字节码 |
| JIT 编译器 | C1（client）、C2（server） |
| GC 实现 | Serial、Parallel、G1、ZGC、Shenandoah |
| 类加载器 | Java `ClassLoader` 的 C++ 实现 |
| 运行时 | 线程管理、锁、内存管理 |

Spring Boot fat jar 启动时 `libjvm.so` 何时进内存，见 [Spring Boot Executable JAR](./spring/spring-boot-executable-jar.md) §启动全流程。

## 实现语言与自举

HotSpot（OpenJDK / Oracle JDK 自带的 JVM）主要用 **C++** 编写，少量 C 与平台相关汇编：

| 组成 | 语言 |
| ---- | ---- |
| 解释器、GC、类加载 | C++ |
| OS 级原语（线程、内存映射） | C |
| JIT 生成的机器码模板（Stub） | 汇编（x86 / ARM） |

这是自然选择：管理裸内存、操作 CPU 寄存器、发起系统调用正是 C/C++ 擅长的。Java 无法用自己实现虚拟机——运行任何 Java 程序都已经需要一个现成的 JVM，这是「先有鸡还是先有蛋」的问题。JDK 标准库（`java.lang.*` 等）是 Java 写的，但任何触及 OS 的操作（文件、网络、线程）最终都会调到 `libjvm.so` 里的 `native` 方法。

### Java vs Go vs Rust 的自举

「自举」（self-hosting）指一门语言的编译器用它自己写，并能编译自己。

| 语言 | 编译器 | 运行时 | 是否完全自举 |
| ---- | ------ | ------ | ------------ |
| Java | `javac`（Java） | JVM（C++） | **部分**：`javac` 能编译 `javac`，但 JVM 是 C++，且运行 `javac` 本身就需要现成 JVM |
| Go | `gc`（Go，自 1.5 起） | 无独立 VM | **完全**：编译为本地机器码 |
| Rust | `rustc`（Rust） | 无独立 VM | **完全**：编译为本地机器码 |

```text
Java:  .java → javac(Java) → .class → JVM(C++) 执行   ← 始终依赖 C++
Go:    .go   → gc(Go)      → 机器码                   ← 完全脱离 C
Rust:  .rs   → rustc(Rust) → 机器码                   ← 完全脱离 C
```

Go 与 Rust 能彻底摆脱 C 的关键，是它们**直接编译为本地机器码**，无需 C 写的运行时来执行编译器输出。Java 走 GraalVM Native Image 也能产出本地二进制（见 [GraalVM Native Image](./graalvm-native-image.md)）。

## 博客内相关文章

| 主题 | 文章 |
| ---- | ---- |
| JVM 生态与选型 | [jvm](./jvm.md) |
| JIT / 分层编译 / C1·C2 | [jvm-compiler](../../cs/jvm-compiler.md) |
| 启动参数（堆、GC、日志、JIT） | [hotspot-options](./hotspot-options.md) |
| GC 概念与算法 | [java-gc](./gc.md)、[jvm-gc](./jvm-gc.md) |
| 类加载 | [classloader](./classloader.md) |
| Attach / jcmd | [attach-api](./attach-api.md)、[jcmd](./jcmd.md) |
| 字节码织入 | [java-asm](./asm.md) |
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
| 2026-06-21 | 新增「历史」节：1999 首次发布、1.3 默认、1.4 唯一 | 补充 HotSpot 起源与 JDK 集成时间线 |
| 2026-06-27 | 新增「libjvm.so 与 JVM 主体」「实现语言与自举」（含 Java/Go/Rust 自举对比） | 合并 comments-tree 启动打包文档相关章节 |
