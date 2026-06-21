---
title: Spring AOT 简介
author: "-"
date: 2026-06-21T18:05:54+08:00
lastmod: 2026-06-21T18:05:54+08:00
url: spring-aot
categories:
  - language
tags:
  - java
  - spring
  - spring-boot
  - aot
  - graalvm
  - remix
  - AI-assisted
---

## 是什么

Spring AOT（Ahead-Of-Time）是 **Spring Framework 6 / Spring Boot 3** 引入的构建期处理机制：在**打包或 Native 编译之前**，对 Spring `ApplicationContext` 做静态分析，生成预先计算好的 bean 定义、反射/资源 hint，以及（可选）面向 GraalVM Native Image 的入口代码。

默认 Spring Boot 应用在运行时做 classpath 扫描、`@Configuration` 解析、条件装配（`@Conditional`）和大量反射；Spring AOT 把这些工作**尽量前移到构建期**，使：

- 在 **HotSpot JVM** 上跑的处理后 JAR，启动更快（仍用 `java -jar`）
- 在 **GraalVM Native Image** 路径上，构建器能拿到闭世界分析所需的元数据

## 不要和 JDK AOT 混淆

博客与 JDK 发行说明里还有另一类「AOT」，含义不同：

| 名称 | 层级 | 做什么 |
| ---- | ---- | ------ |
| **Spring AOT** | Spring 框架 / Boot 插件 | 构建期处理 IoC 容器，生成 bean 与 Native hint |
| **GraalVM Native Image AOT** | GraalVM 工具链 | 字节码 → 本地机器码 + Substrate VM |
| **JDK AOT 缓存**（JEP 483 等） | HotSpot JVM | 训练运行后缓存类加载/链接/剖析，缩短**下次** JVM 冷启动 |

Spring AOT 常与 GraalVM Native Image **配合使用**，但不是同一 thing；JDK 24+ 的 AOT 缓存与 Spring AOT **可以并存**，也互不替代。JDK 侧见 [JDK 25 变更汇总](../../jdk25-changes-from-jdk21.md)、[JVM 编译器](../../../cs/jvm-compiler.md)。

## 解决什么问题

GraalVM Native Image 要求构建期知道所有可能用到的反射、资源、代理类。Spring 传统启动方式大量依赖运行时扫描与动态特性，直接对 fat jar 跑 `native-image` 通常会失败或缺配置。

Spring AOT 在构建期：

1. 启动一个特殊的 `ApplicationContext` 做**模拟装配**（受 `@Conditional` 等约束）
2. 将结果 bean 定义**固化**为生成的 Java 源码/字节码（而非运行时扫描）
3. 输出 **GraalVM reachability metadata**（反射、资源、序列化、JNI 等 hint）
4. 为 Native 构建生成专用 `Application` 入口类

这样 Native Image 构建器能「看见」Spring 应用在构建期实际会触达的类与方法。

## 两种使用方式

### 1. JVM 模式（处理后仍用 HotSpot）

构建时执行 `process-aot`，生成的代码打进 JAR，运行时仍是普通 JVM：

```bash
./mvnw -DskipTests process-aot package
java -jar target/myapp.jar
```

启动路径跳过部分运行时扫描，冷启动通常比未处理 JAR 快，但**仍有 JVM 启动成本**；峰值吞吐仍依赖 HotSpot JIT。

### 2. Native Image 模式

在 Spring AOT 之上再跑 GraalVM `native-image`：

```bash
./mvnw -Pnative native:compile -DskipTests
# Gradle: ./gradlew nativeCompile
```

产物为本地可执行文件；详见 [GraalVM Native Image 简介](../graalvm-native-image.md)。

```text
未处理 Spring Boot:
  java -jar app.jar  →  扫描 / 反射 / 条件装配  →  运行

Spring AOT（JVM）:
  process-aot  →  生成 bean 与 hint  →  java -jar app.jar（更快启动）

Spring AOT + Native:
  process-aot  →  native-image  →  ./app（毫秒级启动）
```

## 构建期发生了什么

典型 Maven 流程（Spring Boot 3 插件内置，无需单独声明旧版 `spring-aot-maven-plugin`）：

1. **`process-aot`**（或 `native` profile 构建链中的等价步骤）：分析 `@SpringBootApplication` 入口，生成代码到 `target/spring-aot/main`（Gradle 为 `build/generated/aot`）
2. **`compile` / `package`**：将生成源一并编译进 artifact
3. **`native:compile`**（可选）：以 AOT 产出 + 依赖为输入，调用 GraalVM Native Image

生成物大致包括：

- 预计算的 `BeanDefinition` / `BeanFactory` 初始化代码
- `META-INF/native-image/` 下的 JSON hint（反射、资源等）
- Native 用的 `Application` 主类（类名因版本而异，由插件生成）

## 与 Spring Boot 的关系

Spring Boot 3 把 AOT 作为 **first-class** 能力集成进构建插件，而不是要求应用手写 `reflect-config.json`。官方 Native 文档与 `native` Maven profile 均假设已走 Spring AOT 流程。

[Spring Boot](./spring-boot.md) 总览里仅一句带过；REST API **默认不会**启用 AOT——需显式 `process-aot` 或 `-Pnative` 构建。

常见约束：

- 构建期无法确定的 `@Conditional` 分支（如依赖环境变量才成立的 bean）可能导致 Native 构建缺 bean
- 运行时注册 bean、`BeanFactoryPostProcessor` 动态改定义等模式需改写或注册 hint
- 未适配 Spring 6 AOT 的第三方 starter 可能在 Native 构建或运行时报错

## 何时需要 Spring AOT

| 场景 | 是否需要 |
| ---- | -------- |
| 普通 Spring Boot REST + HotSpot 容器 | 否（默认即可） |
| 想缩短 JVM 冷启动、又不用 Native | 可选 `process-aot` |
| GraalVM Native Image / Serverless 极冷启动 | 需要（Native 构建链会自动带上） |
| 仅用 jlink 裁 JRE | 否（与 Spring AOT 无关，见 [JPMS 与 Jigsaw](../../../cs/jpms-jigsaw.md)） |

## 参考

- [Spring Framework AOT](https://docs.spring.io/spring-framework/reference/core/aot.html)
- [Spring Boot Native Image](https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html)
- [GraalVM 简介](../graalvm.md)
- [GraalVM Native Image 简介](../graalvm-native-image.md)
- [Spring Boot](./spring-boot.md)
