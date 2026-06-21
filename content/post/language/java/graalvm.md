---
title: GraalVM
author: "-"
date: 2026-06-21T18:08:37+08:00
lastmod: 2026-06-21T18:08:37+08:00
url: graalvm
categories:
  - language
tags:
  - java
  - graalvm
  - jvm
  - remix
  - AI-assisted
---

## 是什么

[GraalVM](https://www.graalvm.org/) 是 Oracle 主导的 **高性能 JDK 发行版与工具链**，基于 OpenJDK，但不止「又一个 Temurin」：它在同一产品里组合了 **Java 运行时**、**Graal JIT 编译器**、**Native Image AOT**、**Truffle 多语言运行时** 等能力。

日常讨论里常把 GraalVM 缩略成「Native Image 用的那个 JDK」，实际上 Native Image 只是其组件之一；完整图景见下文与 [Java 虚拟机](./jvm.md) 生态对照。

## 发行版

| 版本 | 说明 |
| ---- | ---- |
| **Community Edition (CE)** | 开源（GPLv2 + Classpath exception），GitHub 发布 |
| **Enterprise Edition (EE)** | 商业支持，额外性能与工具（需 Oracle 许可） |

安装后通常提供 `java`、`javac`、`native-image`、`gu`（GraalVM Updater，用于安装/管理组件）等命令。具体组件集因版本与安装方式而异。

## 三种常见使用方式

```text
                         GraalVM 发行版
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
   JVM 模式（java）      Native Image           Truffle / Polyglot
   HotSpot + Graal JIT   AOT 本地二进制        JS/Python/Ruby 等同 JVM 上互操作
         │                     │
         │                     └── 见专文
         └── 仍跑 .class，可替代默认 C2 路径（视版本与 -XX 开关）
```

### 1. JVM 模式：Graal 作 JIT

用 GraalVM 自带的 `java` 跑字节码，底层仍是 **HotSpot VM**，但可用 **Graal 编译器** 作为 JIT 替代或补充传统 C1/C2（取决于 JDK 版本与 JVM 参数；OpenJDK 曾实验性集成 Graal JIT，JDK 17+ 默认路径以 C2 为主，Graal JIT 需显式启用或视发行版而定）。

- 仍是 `java -jar app.jar`，生态与 HotSpot 大体兼容
- 适合评估 Graal 编译器对特定负载的峰值性能，**不是**大多数团队的默认选型

### 2. Native Image：AOT 本地可执行文件

构建期将 Java 应用 AOT 编译为 **不依赖完整 HotSpot 的本地二进制**，运行时使用 **Substrate VM**。冷启动与内存占用是主要卖点；反射、动态加载等受限。

详见 [GraalVM Native Image 简介](./graalvm-native-image.md)。Spring Boot 3 走 [Spring AOT](./spring/spring-aot.md) + Native 构建链。

### 3. 多语言（Truffle）

Truffle 框架允许在 JVM 上高效运行 JavaScript、Python、Ruby 等，并与 Java 互操作。Polyglot API 可在同一进程内混用语言。本文不展开；Java 服务端选型通常只涉及前两种。

## 与 HotSpot / OpenJDK 的关系

| 维度 | 常见 OpenJDK（Temurin 等） | GraalVM |
| ---- | -------------------------- | ------- |
| 规范 | Java SE / JVM 规范 | 同样兼容，基于 OpenJDK 代码基 |
| 默认 `java` | HotSpot + C1/C2 | HotSpot + 可选 Graal JIT |
| Native 可执行文件 | 无（需另装 GraalVM 并跑 `native-image`） | 有 |
| 诊断 | jcmd、JFR、Attach 等 HotSpot 工具 | JVM 模式类似；Native 路径不同 |

**不要混用概念**：说「我们上了 GraalVM」要澄清是 **JVM 模式**、**Native Image 产物**，还是仅 CI 里用 GraalVM JDK 做构建。Native 路径下没有传统 HotSpot JIT 预热与完整 `-XX` 调优空间，见 [HotSpot JVM 简介](./hotspot.md) 对比。

## 与 jlink / JDK AOT 的区别

| 手段 | 层级 | 产物 |
| ---- | ---- | ---- |
| [jlink](../../cs/jpms-jigsaw.md) | JPMS 模块裁剪 | 更小的 JRE + 仍用 `java` 跑字节码 |
| JDK AOT 缓存（JEP 483 等） | HotSpot 启动优化 | 训练后的缓存，缩短下次 JVM 冷启动 |
| GraalVM Native Image | 全量 AOT 编译 | 本地二进制，非 HotSpot 运行时 |
| Spring AOT | Spring 容器构建期处理 | 为 Native 或更快 JVM 启动生成 hint 与 bean 代码 |

## 何时考虑 GraalVM

| 目标 | 建议路径 |
| ---- | -------- |
| 默认服务端 REST | 继续用 Temurin/Corretto + HotSpot |
| 缩小容器 JRE | [jlink](../../cs/jpms-jigsaw.md)，不必上 GraalVM |
| 毫秒级冷启动、Serverless | GraalVM **Native Image** + Spring AOT |
| 实验 JIT 峰值 | GraalVM **JVM 模式** + 压测验证 |

## 本站相关文档

| 主题 | 文章 |
| ---- | ---- |
| GraalVM 总览 | 本文 |
| Native Image 原理与用法 | [graalvm-native-image](./graalvm-native-image.md) |
| Spring 构建期 AOT | [spring-aot](./spring/spring-aot.md) |
| JVM 生态选型 | [jvm](./jvm.md) |
| HotSpot 专述 | [hotspot](./hotspot.md) |

## 参考

- [GraalVM 官网](https://www.graalvm.org/)
- [GraalVM Native Image 文档](https://www.graalvm.org/latest/reference-manual/native-image/)
- [GraalVM on GitHub](https://github.com/oracle/graal)
