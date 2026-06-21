---
title: Java 虚拟机
author: "-"
date: 2021-05-19T18:06:35+08:00
lastmod: 2026-06-21T18:02:02+08:00
url: jvm
categories:
  - language
tags:
  - graalvm
  - hotspot
  - java
  - jvm
  - openj9
  - remix
  - AI-assisted
---

## 背景

日常说的「JVM」常混用两层含义：

- **JVM 规范**（JLS/JVMS）：字节码、class 文件格式、类加载语义、JNI、JPDA 等，与具体实现无关。
- **JVM 实现**：真正把字节码跑起来的运行时，如 HotSpot、OpenJ9。

安装 `java` 命令得到的是 **JDK 发行版**（见 [OpenJDK JDK 发行版](./openjdk-distributions.md)；安装命令见 [openjdk](./openjdk.md)），其中默认捆绑的虚拟机实现几乎都是 **HotSpot**。本文介绍 **JVM 实现**（HotSpot、OpenJ9、GraalVM Native 等）的差异与选型；**HotSpot 的参数与工具**见 [hotspot](./hotspot.md)。

## JDK 发行版 vs JVM 实现

**Temurin、Corretto、Dragonwell** 等是不同厂商打包的 **OpenJDK 发行版**，默认都跑 **HotSpot**，不是三种并列的 JVM。换 Temurin 换 Corretto，通常只是换构建源与支持方；要换虚拟机实现才看 OpenJ9（Semeru）或 GraalVM Native Image。发行版对照见 [openjdk-distributions.md](./openjdk-distributions.md)。

## 规范层：各实现共同遵守什么

无论用哪种 JVM，下列概念在规范层是共通的：

| 概念 | 说明 |
| ---- | ---- |
| 字节码 | `javac` 产出 `.class`，由虚拟机解释或 JIT 编译后执行 |
| 类加载 | 加载、链接、初始化；双亲委托等模型见 [classloader](./classloader.md) |
| JNI | Java 与本地代码互操作规范，见 [java-jni](./java-jni.md) |
| JPDA | 调试体系（JDI / JDWP / JVMTI），见 [java-debug-JPDA](./java-debug-JPDA.md) |

规范 **不** 规定用哪种垃圾收集器、有哪些 `-XX` 开关、是否提供 JFR——这些是实现细节。

## 主流 JVM 实现对照

| 实现 | 典型发行版 | 特点 | 适用场景 |
| ---- | ---------- | ---- | -------- |
| **HotSpot** | Oracle JDK、Temurin、Corretto、Dragonwell 等 | 生态最全；C1/C2 JIT、G1/ZGC/Shenandoah、JFR、jcmd、Attach 默认可用 | **默认首选**；绝大多数服务端与桌面应用 |
| **Eclipse OpenJ9** | IBM Semeru | 常更低内存占用、较快启动；工具链与 HotSpot 不同 | 容器密度高、内存敏感；需验证 agent/诊断工具兼容性 |
| **GraalVM** | GraalVM CE/EE | 可嵌 HotSpot 作 JIT 运行时，或通过 **Native Image** AOT 为本地可执行文件 | 极致冷启动（serverless、CLI）；见 [GraalVM 简介](./graalvm.md)、[Native Image](./graalvm-native-image.md) |
| **JRockit** | 已停止独立发展 | 曾用于金融低延迟；特性已并入 HotSpot | 仅作历史了解，见 [jrockit](./jrockit.md) |

```text
                    ┌─────────────────────────────────┐
                    │     Java 语言 + JVM 规范       │
                    └─────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
   OpenJDK HotSpot            Eclipse OpenJ9              GraalVM
   (默认 java 命令)            (Semeru 等)          ┌──────┴──────┐
          │                           │            ▼             ▼
          │                           │      HotSpot 运行时   Native Image
          ▼                           ▼            (JIT)         (AOT 本地二进制)
   jcmd / JFR / Attach            自有诊断工具
```

## 选型建议

1. **没有明确理由时，用 HotSpot**（即常见 OpenJDK 发行版）。文档、agent、APM、排障经验都围绕它积累最多。
2. **内存或启动是瓶颈**，且已验证依赖（Attach、部分 agent、GC 日志格式）在目标环境可用，可评估 **OpenJ9**。
3. **冷启动极敏感**（函数计算、短生命周期进程），评估 **GraalVM Native Image**（见 [GraalVM 简介](./graalvm.md)、[Native Image](./graalvm-native-image.md)）；需接受构建期分析、反射配置、动态类加载受限等成本。
4. **不要混用概念**：GraalVM 不等于「又一个 HotSpot」；Native Image 路径下没有传统 JIT 预热，也没有完整的 `-XX` 调优空间。

## HotSpot 执行路径（概念）

HotSpot 的典型路径（细节见专文）：

```text
源码 → javac → .class → 类加载 → 解释器 / C1 / C2（JIT）→ 堆上对象 → GC
```

- JIT 与分层编译：[HotSpot JIT 编译器（C1/C2）](../../cs/jvm-compiler.md)
- GC 算法与调优：[java-gc](./java-gc.md)
- 启动参数： [HotSpot JVM 启动参数](./hotspot-options.md)

## 本站文档边界

| 范围 | 入口 |
| ---- | ---- |
| JVM 实现生态与选型 | 本文 |
| HotSpot 架构与站内索引 | [hotspot](./hotspot.md) |
| GraalVM 总览 / Native Image | [graalvm](./graalvm.md) / [graalvm-native-image](./graalvm-native-image.md) |
| HotSpot `-X` / `-XX` 参数 | [hotspot-options](./hotspot-options.md) |
| OpenJDK 发行版（Temurin / Corretto 等） | [openjdk-distributions](./openjdk-distributions.md) |
| OpenJDK 安装命令备忘 | [openjdk](./openjdk.md) |

文中 **jmap、jstack、JFR、`-XX:+UseG1GC` 等默认指 HotSpot**；OpenJ9 需查阅其自有文档与工具。

## 参考

- [JVM Specification](https://docs.oracle.com/javase/specs/jvms/se21/html/index.html)
- [OpenJDK](https://openjdk.org/)
- [Eclipse OpenJ9](https://www.eclipse.org/openj9/)
- [GraalVM](https://www.graalvm.org/)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-19 | 重写为 JVM 生态与选型；原 HotSpot 参数迁至 [hotspot-options](./hotspot-options.md) | 职责拆分：规范/生态 vs HotSpot 实现细节 |
| 2026-06-21 | 链到新建 [graalvm-native-image.md](./graalvm-native-image.md) | Native Image 专文拆分 |
| 2026-06-21 | 链到 [graalvm.md](./graalvm.md) | GraalVM 总览专文 |
| 2026-06-21 | 新增「JDK 发行版 vs JVM 实现」；链到 [openjdk-distributions.md](./openjdk-distributions.md) | 区分发行版与虚拟机 |
