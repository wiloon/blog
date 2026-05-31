---
title: HotSpot JVM 简介
author: "-"
date: 2026-05-31T07:25:07+08:00
lastmod: 2026-05-31T07:25:07+08:00
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

日常说的「JVM」在 OpenJDK 发行版里，默认实现几乎都是 **HotSpot**。本文只做 **架构索引**；GC、类加载、attach 等细节见各专题文。

## HotSpot 是什么

**HotSpot** 是 Oracle/OpenJDK 中 **默认的 Java 虚拟机实现**（C++）。你安装的 `java` 命令、容器里的 JDK 镜像，除非明确换用 OpenJ9、GraalVM Native 等，否则跑的就是 HotSpot。

| 实现 | 说明 |
| ---- | ---- |
| **HotSpot** | OpenJDK 默认；[Attach](./attach-api.md)、[BTrace](./btrace.md)、JFR（JDK 11+ 开源）等文档均默认指它 |
| Eclipse OpenJ9 | IBM J9 开源分支，attach/工具链与 HotSpot 不完全相同 |
| GraalVM | 可含 HotSpot 作运行时，或 Native Image 等另一路径 |

博客 [jvm](./jvm.md) 一文偏通用 JVM 概念（ inbox 状态）；**HotSpot 专文** 以本文为入口。

## 核心组成（简图）

```text
Java 源码 → javac → .class
                    ↓
              类加载（见 [classloader](/classloader)）
                    ↓
         解释执行 + C1/C2 即时编译（JIT）
                    ↓
         运行时数据区（堆、栈、元空间等）
                    ↓
         垃圾收集器（见 [java-gc](/java-gc) 等）
```

与诊断相关的 **HotSpot 内置能力**（不另挂 agent jar 也可部分使用）：

- **AttachListener** + **Diagnostic Command**（[jcmd](./jcmd.md)、[Attach API](./attach-api.md)）
- **JPDA / JVMTI** 调试后端（[JPDA](./java-debug-JPDA.md)、[JVMTI](./jvmti.md)）
- **JFR**（[Java Flight Recorder](./java-flight-recorder-jfr.md)）

动态挂 **外部** agent（BTrace、Arthas）同样依赖 HotSpot 的 attach 与 instrument 实现。

## 博客内相关文章

| 主题 | 文章 |
| ---- | ---- |
| 通用 JVM / 执行引擎 | [jvm](./jvm.md) |
| GC | [java-gc](./java-gc.md)、[parallel-scavenge](../../cs/parallel-scavenge.md) 等 |
| 类加载 | [classloader](./classloader.md) |
| Attach / jcmd | [attach-api](./attach-api.md)、[jcmd](./jcmd.md) |
| 字节码织入 | [java-asm](./java-asm.md) |
| 开发期热替换 | [DCEVM 与 HotSwapAgent](../../cs/dcevm-hotswapagent.md) |
| Safepoint | [safepoint](../../other/safepoint.md) |

## 参考

- [OpenJDK HotSpot](https://openjdk.org/projects/hotspot/)
- [OpenJDK](https://openjdk.org/)
