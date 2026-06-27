---
title: GraalVM Native Image 简介
author: "-"
date: 2026-06-21T18:01:39+08:00
lastmod: 2026-06-27T04:52:28+08:00
url: graalvm-native-image
categories:
  - language
tags:
  - java
  - graalvm
  - native-image
  - aot
  - remix
  - AI-assisted
---

## 是什么

GraalVM Native Image 是 GraalVM 提供的 **AOT（Ahead-Of-Time）** 编译路径：在**构建期**把 Java 应用及其依赖静态分析，编译成**本地可执行文件**（Linux/macOS/Windows 上的单一二进制或小型目录），运行时**不再依赖**传统意义上的 `java -jar` + 完整 JRE/HotSpot 进程模型。

与日常默认的 HotSpot 路径对比：

```text
HotSpot:  源码 → javac → .class → java 启动 JVM → 解释/JIT → 运行
Native Image:  源码 → javac → .class → native-image 构建 → 本地二进制 → 直接运行
```

GraalVM 平台总览见 [GraalVM 简介](./graalvm.md)。作为运行时有两种常见用法，不要混为一谈：

- 作为 **HotSpot 上的高性能 JIT 编译器**（仍是 `java` 命令跑字节码）
- 作为 **Native Image 工具链**（产出独立可执行文件，本文主题）

## 为什么用它

| 维度 | HotSpot + JAR | Native Image |
| ---- | ------------- | -------------- |
| 冷启动 | 秒级常见（JVM 启动、类加载、Spring 扫描） | 毫秒级常见 |
| 内存占用 | 完整 JVM 堆与元空间 | 无 HotSpot 堆模型；通常更小 |
| 镜像/分发 | 需 JRE 或容器内 Java 运行时 | 单一二进制 + 可选少量资源文件 |
| 峰值吞吐 | JIT 预热后通常更强 | 无 C2 长时间优化，长时间 CPU 密集型可能不如 HotSpot |
| 构建 | `mvn package` 较快 | `native-image` 构建慢，CI 时间显著增加 |

典型场景：Serverless/函数计算、CLI 工具、Kubernetes 中**短生命周期**且**副本多**的 Pod、对启动延迟敏感的边缘服务。

## 工作原理（闭世界假设）

Native Image 在构建期做 **closed-world analysis**：只包含构建时能证明会用的类、方法和反射目标。构建器大致步骤：

1. 从入口（`main` 或 Spring AOT 生成的入口）做可达性分析
2. 将可达字节码 AOT 编译为本地机器码
3. 初始化部分类（build-time initialization，视配置而定）
4. 打包 Substrate VM（精简运行时，替代完整 HotSpot）与堆管理、线程等

因此运行时**不能**像 HotSpot 那样随意 `Class.forName` 加载未知类、无限反射、动态生成大量代理——除非在构建期通过 **reachability metadata**（反射配置、resource 配置、JNI 配置等）显式声明。

## 主要限制

| 限制 | 说明 |
| ---- | ---- |
| 反射 / 资源 | 构建期未声明的反射调用、classpath 资源可能运行时报错；框架需 AOT 适配或提供 hint |
| 动态代理 | CGLIB/JDK 动态代理需在分析阶段可见或注册 |
| 类加载 | 动态类加载、自定义 ClassLoader 场景受限 |
| JIT / `-XX` | 无 HotSpot C1/C2 预热；GC 与诊断模型与 HotSpot 不同 |
| 构建时间 | 中大型 Spring 应用 native 构建常需数分钟到十几分钟 |
| 调试 | 与传统 Java 调试体验不同；问题更常出现在构建期 |

Spring Boot 3.x 通过 [Spring AOT](./spring/spring-aot.md) 在构建时生成反射/bean 元数据，降低手工写 `reflect-config.json` 的负担。

## Substrate VM 与运行时结构

Native Image 产物里内嵌的精简运行时叫 **Substrate VM**：它负责 GC 与线程管理，但**不是字节码执行引擎**——没有解释器、没有 JIT。这类似 Go：Go 程序也内嵌一个 runtime（管 GC 与 goroutine 调度），但没人把 Go 称作「虚拟机语言」。

Fat Jar（HotSpot）与 Native Image 的运行时对比：

|  | Fat Jar（JVM） | Native Image |
| ---- | -------------- | ------------ |
| 字节码解释器 | ✅ HotSpot 解释 `.class` | ❌ 全部预编译为机器码 |
| JIT 编译器 | ✅ C1/C2 运行时优化热点 | ❌ 构建期 AOT，无运行时 JIT |
| 动态类加载 | ✅ | ❌ 类在构建期确定 |
| GC | HotSpot GC（G1、ZGC 等） | Substrate VM GC（Serial / G1） |
| 启动时间 | 3–10 秒 | 50–200 毫秒 |
| 内存 | 200–500 MB | 50–100 MB |
| 启动方式 | `java -jar app.jar` | `./app` |

```text
Fat Jar 运行时:
┌──────────────────────────────────────┐
│  应用 + Spring Framework             │  ← Java 字节码
│  JDK 标准库                          │
├──────────────────────────────────────┤
│  JVM (HotSpot): GC, JIT, 类加载      │  ← libjvm.so
├──────────────────────────────────────┤
│  OS                                  │
└──────────────────────────────────────┘

Native Image 运行时:
┌──────────────────────────────────────┐
│  应用 + Spring Framework             │  ← 机器码（AOT 编译）
│  JDK 标准库（用到的部分）            │
├──────────────────────────────────────┤
│  Substrate VM: 仅 GC + 线程管理      │  ← 无字节码解释器、无 JIT
├──────────────────────────────────────┤
│  OS                                  │
└──────────────────────────────────────┘
```

### Java vs Go：默认产物不同

|  | Go | Java（默认） | Java（GraalVM Native） |
| ---- | -- | ------------ | ---------------------- |
| 产物 | 本地 ELF 二进制 | `.class` / `.jar` 字节码 | 本地 ELF 二进制 |
| Linux 运行 | `./app` | `java -jar app.jar` | `./app` |
| 需要 JVM | 否 | 是 | 否 |

Go 一律编译为本地机器码（默认且唯一）；Java 默认产出字节码以保证「一次编写、到处运行」，由 JVM 在运行时屏蔽平台差异。GraalVM Native Image 让 Java 也能像 Go 一样产出本地二进制，代价是构建慢、反射与动态类加载需显式声明。JVM 为何用 C++ 实现、为何 Java 无法「自举」出虚拟机，见 [HotSpot](./hotspot.md) §实现语言与自举。

## 与 jlink 的区别

两者都能缩小部署体积，机制不同：

| | jlink | GraalVM Native Image |
| ---- | ----- | -------------------- |
| 产物 | 裁剪后的 **JRE 目录** + 仍用 `java` 跑字节码 | **本地可执行文件**，字节码已 AOT 编译 |
| 启动 | 仍需 JVM 启动 | 直接 exec，冷启动更快 |
| 运行时 | HotSpot（解释/JIT） | Substrate VM，无完整 HotSpot JIT |
| 对应用形态 | classpath fat jar 也可用（`jdeps` 分析有限） | 依赖构建期闭世界分析；Spring 等需 AOT 支持 |
| 详见 | [JPMS 与 Jigsaw](../../cs/jpms-jigsaw.md) | 本文 |

容器里 **jlink** 常见做法是 Dockerfile multi-stage 用 JDK 生成定制 JRE；**Native Image** 则是构建阶段产出二进制，运行镜像可用 `distroless` 或 `FROM scratch`（视 libc 链接方式而定）。

> **jpackage**（JDK 14，2020）是另一条路：把 jlink 产物再包成各平台原生安装包（macOS `.dmg`/`.pkg`、Windows `.msi`/`.exe`、Linux `.deb`/`.rpm`），面向桌面应用（如 JavaFX），不适合服务端服务。它仍跑 HotSpot 字节码，与 Native Image 的 AOT 二进制是不同方案。

## 基本用法

安装 GraalVM 与 `native-image` 组件（以 SDKMAN 或官方发行版为例）：

```bash
# Install native-image component (varies by GraalVM distribution)
gu install native-image

# Simple jar with explicit main class
native-image -jar app.jar -o app
./app
```

手工维护反射配置时，可使用 `META-INF/native-image/` 下的 JSON，或通过 agent 在 JVM 上跑一遍收集：

```bash
java -agentlib:native-image-agent=config-output-dir=./config -jar app.jar
# Exercise the app, then use generated configs in the next native-image build
```

Spring Boot 3 推荐使用插件一键构建（底层仍调用 Native Image）：

```bash
./mvnw -Pnative native:compile -DskipTests
# or
./gradlew nativeCompile
```

具体版本与 profile 名以项目所用 Spring Boot 文档为准。

## Spring Boot REST API 是否「自动 Native」

**不会。** 默认仍是 fat jar + HotSpot。要 Native 需：

- Spring Boot 3 + GraalVM，启用 AOT / native 构建 profile（见 [Spring AOT](./spring/spring-aot.md)）
- 或 `bootBuildImage` 配合支持 GraalVM 的 buildpack（与 Paketo jlink 裁剪是不同路径，JVM 容器打包见 [Spring Boot Container Packaging](./spring/spring-boot-container-packaging.md)）

Fat jar 直接丢给 `native-image` 往往缺少 Spring 所需的 AOT 处理；应走官方 **Spring Boot Native** 构建流程，而不是只对 jar 跑一遍 `native-image`。

## 何时选 Native Image

适合：

- 冷启动和内存是主要瓶颈
- 进程短生命周期、弹性伸缩频繁
- 团队愿意投入构建与 AOT 兼容排查

不适合作为默认：

- 长时间高吞吐、依赖 JIT 峰值性能
- 大量动态反射、脚本引擎、未适配 AOT 的老库
- 希望零配置、构建快、排障与 HotSpot 完全一致

多数 REST 服务仍用 **HotSpot + 容器 JRE** 或 **jlink 裁剪 JRE** 即可；Native Image 是**特定场景**的优化手段，不是 Java 部署的默认替换项。

## 参考

- [GraalVM 简介](./graalvm.md)
- [GraalVM Native Image 官方文档](https://www.graalvm.org/latest/reference-manual/native-image/)
- [Java 虚拟机生态与选型](./jvm.md)
- [HotSpot JVM 简介](./hotspot.md)
- [Spring Boot 3 Native 支持](https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html)
- [Spring AOT 简介](./spring/spring-aot.md)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-27 | 新增「Substrate VM 与运行时结构」（含 Go runtime 类比、Fat Jar vs Native 对比、Java vs Go 产物）；jlink 节补 jpackage 说明 | 合并 comments-tree 启动打包文档相关章节 |
