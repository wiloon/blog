---
title: JVMTI（Java 虚拟机工具接口）
author: "-"
date: 2026-05-31T07:25:07+08:00
lastmod: 2026-05-31T07:25:07+08:00
url: jvmti
categories:
  - language
tags:
  - AI-assisted
  - hotspot
  - java
  - jpda
  - jvm
  - jvmti
  - remix
---

## 背景

调试器断点、IDE 热替换、[jcmd](./jcmd.md) 部分能力、[Attach API](./attach-api.md) 的 `loadAgentLibrary`、native agent，底层都依赖 JVM 提供的 **native 级** 工具接口。在 HotSpot/OpenJDK 上，这一层主要是 **JVMTI**。

## JVMTI 是什么

**JVMTI**（Java Virtual Machine Tool Interface）是 JVM 实现的 **C 语言 native 接口**（`jvmti.h`），用于：

- 调试：断点、单步、查看栈与局部变量
- 分析：采样、分配追踪
- 类与字节码：监听类加载、**重定义已加载类**（与 IDE HotSwap 相关）
- Agent：native agent 在 `Agent_OnLoad` 里通过 `JavaVM::GetEnv` 拿到 `jvmtiEnv`

它 **不是** Java 应用直接 `import` 的包；Java 侧看到的是更高层的封装。

| 前身（已淘汰） | 用途 |
| -------------- | ---- |
| JVMDI | 调试 |
| JVMPI | 性能分析 |

JDK 5+ 由 **JVMTI** 统一替代（见 [JPDA](./java-debug-JPDA.md) 文中的历史说明）。

## 与 JPDA、Instrumentation 的关系

```text
IDE / jdb（调试器）
  ↓ JDI（Java API）
  ↓ JDWP（线协议，如 dt_socket）
  ↓ JVMTI Agent（如 jdwp.so）→ JVMTI 调用
  ↓ HotSpot JVM

java.lang.instrument（Java Agent，premain/agentmain）
  ↓ JVM 内部同样依赖 JVMTI 等 native 能力实现 redefine/retransform
```

| 接口 | 语言 | 典型用途 |
| ---- | ---- | -------- |
| **JVMTI** | C / native | 调试器后端、profiler、native agent |
| **JPDA**（JDI + JDWP + JVMTI） | 调试体系 | Eclipse/IDEA 远程调试、JDB |
| **`java.lang.instrument`** | Java | BTrace、Arthas、`-javaagent`、部分 APM |

三者都落在 **同一 JVM 进程** 里，但入口不同：写 Java 诊断 agent 用 `instrument` + [Attach](./attach-api.md)；写调试器走 **JPDA**；写 native 库 agent 用 **JVMTI** + `loadAgentLibrary`。

详见 [JAVA 调试与 JPDA](./java-debug-JPDA.md)、[Java ASM 与运行时字节码织入](./java-asm.md)。

## 与 Attach、BTrace 的关系

[Attach API](./attach-api.md) 的 `VirtualMachine.loadAgent(jar)` 走 **Java Agent**（`agentmain` + `Instrumentation`），一般不直接写 JVMTI。

同一条 attach 通道上的 `loadAgentLibrary` / `loadAgentPath` 则加载 **native** agent（`.so` / `.dll`），入口是 JVMTI 的 `Agent_OnLoad`。

BTrace、async-profiler 等多数是 **JAR agent + instrument**，不是手写 JVMTI；但 JVM 在实现 `retransformClasses` 时仍会在 native 层用到 JVMTI 能力。

## 参考

- [Java Platform Debugger Architecture](https://docs.oracle.com/javase/8/docs/technotes/guides/jpda/)（JPDA 总览）
- [JVMTI 说明（OpenJDK）](https://openjdk.org/groups/hotspot/docs/Serviceability.html)
- [JPDA 与远程调试](./java-debug-JPDA.md)
- [Attach API](./attach-api.md)
