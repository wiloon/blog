---
title: Spring AOT
author: "-"
date: 2026-06-21T18:05:54+08:00
lastmod: 2026-07-15T22:37:23+08:00
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

默认 Spring Boot 应用在运行时做 [classpath 扫描](./spring-ioc.md#componentscan-与组件注解)、[`@Configuration` 解析](./spring-ioc.md#configuration-解析)、[条件装配](./spring-boot.md#conditionalon-条件注解)（`@Conditional` / `@ConditionalOn*`）和大量反射；Spring AOT 把这些工作**尽量前移到构建期**，使：

- 在 **HotSpot JVM** 上跑的处理后 JAR，启动更快（仍用 `java -jar`）
- 在 **GraalVM Native Image** 路径上，构建器能拿到闭世界分析所需的元数据

## 不要和 JDK AOT 混淆

博客与 JDK 发行说明里还有另一类「AOT」，含义不同：

| 名称 | 层级 | 做什么 |
| ---- | ---- | ------ |
| **Spring AOT** | Spring 框架 / Boot 插件 | 构建期处理 IoC 容器，生成 bean 与 Native hint |
| **GraalVM Native Image AOT** | GraalVM 工具链 | 字节码 → 本地机器码 + Substrate VM |
| **JDK AOT 缓存**（JEP 483 等） | HotSpot JVM | 训练运行后缓存类加载/链接/剖析，缩短**下次** JVM 冷启动 |

Spring AOT 常与 GraalVM Native Image **配合使用**，但不是同一 thing；JDK 24+ 的 AOT 缓存与 Spring AOT **可以并存**，也互不替代。JDK 侧见 [JDK 25 变更汇总](../../jdk25-changes-from-jdk21.md)、[JVM 编译器](../hotspot-jit.md)。

## 解决什么问题

核心矛盾是：**Spring 应用大量依赖运行时动态行为，而 AOT 编译要求构建期就把能确定的事算清楚。**

传统 Spring Boot 冷启动时要做 [classpath 扫描](./spring-ioc.md#componentscan-与组件注解)、[解析 `@Configuration`](./spring-ioc.md#configuration-解析)、[评估 `@Conditional`](./spring-boot.md#conditionalon-条件注解)、反射创建 bean 等；在 HotSpot 上能跑，但有两类场景吃亏：

1. **GraalVM Native Image** 要求「闭世界」——构建期必须知道所有可能用到的反射、资源、代理类；直接对 fat jar 跑 `native-image` 通常会失败或缺配置。
2. **频繁冷启动**（Serverless、弹性缩容到零等）——每次启动都重复扫描与装配，启动时间与资源占用偏高。

Spring AOT 的思路是把上述工作**尽量前移到构建期**，产出可固化的 bean 初始化代码与 Native hint。构建期固化的是 **Bean 定义**（扫描结果、配置解析结果、条件装配方案），**不是** Bean 实例；运行时仍要创建对象并完成依赖注入。

### 构建期的 ApplicationContext

`process-aot` 阶段会启动一个**特殊的** `ApplicationContext`，在构建机上做一次受约束的**预装配**（可理解为「彩排」）：

- 会走 [`@Configuration` 解析](./spring-ioc.md#configuration-解析)、[`@Conditional` 评估](./spring-boot.md#conditionalon-条件注解)等逻辑
- 目的是算出最终会注册哪些 bean、会触达哪些反射/资源/代理
- 结果固化成生成的 Java 源码/字节码，以及 `META-INF/native-image/` 下的 hint

它**不是**把生产环境的完整运行时上下文搬到构建期：依赖真实环境变量、网络或数据库才能决定的分支，构建期可能走不到，这也是 Native 构建常踩坑的原因之一（见下文「常见约束」）。

构建期具体步骤：

1. 启动上述特殊 `ApplicationContext` 做预装配
2. 将 bean 定义**固化**为生成的 Java 源码/字节码（而非运行时扫描）
3. 输出 **GraalVM reachability metadata**（反射、资源、序列化、JNI 等 hint）
4. 为 Native 构建生成专用 `Application` 入口类

这样 Native Image 构建器能「看见」Spring 应用在构建期实际会触达的类与方法。

## 两种使用方式

Spring AOT **不只服务 GraalVM**；GraalVM Native Image 是最典型、也几乎是「必须」的场景，但 **JVM 模式**（`process-aot` 后仍 `java -jar`）是另一条合法路径。

### 1. JVM 模式（处理后仍用 HotSpot）

**JVM 模式**指：构建期跑 `process-aot` 做预处理，**运行时仍用 HotSpot** 跑字节码，**不**编译成 GraalVM Native 可执行文件。

```bash
./mvnw -DskipTests process-aot package
java -jar target/myapp.jar
```

| 维度 | JVM 模式 | Native 模式 |
| ---- | -------- | ----------- |
| 构建 | `process-aot` + `package` | `process-aot` + `native-image` |
| 产物 | 普通 fat JAR（内含 AOT 生成代码） | 本地可执行文件 |
| 启动命令 | `java -jar app.jar` | `./app` |
| 运行时 | HotSpot JVM | Substrate VM |

JVM 模式能省掉的是 **Spring 容器装配**（[扫描](./spring-ioc.md#componentscan-与组件注解)、[`@Configuration` 解析](./spring-ioc.md#configuration-解析)、[条件装配](./spring-boot.md#conditionalon-条件注解)等），运行时走生成好的初始化代码，冷启动通常比未处理 JAR 快一截。

JVM 模式**省不掉**的是：

- JVM 自身启动（加载核心类、初始化运行时）
- 应用类的类加载
- JIT 预热（影响峰值吞吐，不是「能不能起来」）

因此 JVM 模式主要缩短 Spring 那一段，**不是**把整个 JVM 冷启动变成毫秒级；峰值吞吐仍依赖 HotSpot JIT。

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

- 构建期无法确定的 [`@Conditional`](./spring-boot.md#conditionalon-条件注解) 分支（如依赖环境变量才成立的 bean）可能导致 Native 构建缺 bean
- 运行时注册 bean、`BeanFactoryPostProcessor` 动态改定义等模式需改写或注册 hint
- 未适配 Spring 6 AOT 的第三方 starter 可能在 Native 构建或运行时报错

## 何时需要 Spring AOT

| 场景 | 是否需要 | 说明 |
| ---- | -------- | ---- |
| 普通 Spring Boot REST + HotSpot 长期运行 | 否 | 默认构建即可，启动优化收益通常不值得承担 AOT 约束 |
| 想缩短 JVM 冷启动、又不用 Native | 可选 | 单独 `process-aot`，有一定帮助，但别指望质变 |
| GraalVM Native Image | 需要 | Native 构建链会自动带上 Spring AOT |
| **AWS Lambda 等频繁冷启动 / Serverless** | **强烈建议 Native 路径** | 传统 Spring Boot + JVM 冷启动常达数秒到十几秒；`process-aot` + `native-image` 可压到数百毫秒级（视依赖而定）。仅 JVM 模式的 `process-aot` 有改善，但对 Lambda 往往仍不够理想 |
| 仅用 jlink 裁 JRE | 否 | 与 Spring AOT 无关，见 [JPMS 与 Jigsaw](../../../cs/jpms-jigsaw.md) |

Lambda 上另有 **SnapStart**（冻结已初始化 JVM 快照）等方案，与 Spring AOT 是不同层面；Spring 6+ 对 CRaC/SnapStart 有一定支持，但生态与 Native 比仍要逐案验证。

**一句话**：需要**频繁冷启动**的场景（Serverless、缩容到零、短生命周期容器）最值得上 Spring AOT；其中 Lambda 等场景通常要走到 **AOT + Native Image**，而不只是 `process-aot` 后仍 `java -jar`。

## 参考

- [Spring IoC：@Configuration 解析](./spring-ioc.md#configuration-解析)
- [Spring Boot：@ConditionalOn* 条件注解](./spring-boot.md#conditionalon-条件注解)
- [Spring Framework AOT](https://docs.spring.io/spring-framework/reference/core/aot.html)
- [Spring Boot Native Image](https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html)
- [GraalVM 简介](../graalvm.md)
- [GraalVM Native Image 简介](../graalvm-native-image.md)
- [Spring Boot](./spring-boot.md)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-24 | 补充构建期 ApplicationContext 预装配说明；展开 JVM 模式能省/不能省什么；增加 Lambda 等频繁冷启动场景 | 澄清 Spring AOT 不限于 GraalVM，并明确典型使用场景 |
| 2026-06-24 | 内链到 spring-ioc 配置解析、spring-boot 条件装配；补充 Bean 定义与实例区分 | 与 IoC/Boot 文档对齐，便于读者理解 AOT 前移了哪些步骤 |
| 2026-06-24 | 组件扫描内链锚点改为 spring-ioc 新专节 | 与 IoC 文 §@ComponentScan 标题对齐 |
| 2026-07-15 | 更新 jvm-compiler 互链为 hotspot-jit | jvm-compiler.md 更名为 hotspot-jit.md |
