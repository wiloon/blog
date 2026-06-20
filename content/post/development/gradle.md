---
title: Gradle, 目录
author: "-"
date: 2013-12-20T15:52:04+00:00
lastmod: 2026-06-20T18:47:15+08:00
url: gradle
categories:
  - development
tags:
  - Gradle
  - Maven
  - remix
  - AI-assisted

aliases:
  - /p6053/
  - /p7107/
---

## Gradle, 目录

Gradle 是以 Groovy / Kotlin DSL 为基础的 JVM 自动化构建工具，面向 Java 等语言项目。常见构建脚本为 `build.gradle`（Groovy）或 `build.gradle.kts`（Kotlin DSL）。

## Gradle 与 Gradle Wrapper（gradlew）

很多人第一次 clone 项目时会疑惑：**明明没装 Gradle，为什么 `./gradlew test` 也能跑？** 答案就在 Wrapper。

### 是什么关系

| 概念 | 说明 |
| ---- | ---- |
| **Gradle** | 安装在系统上的构建工具，命令是 `gradle`（例如 `brew install gradle`、SDKMAN） |
| **Gradle Wrapper** | 项目自带的一层「启动器」，命令是 `./gradlew`（Windows 用 `gradlew.bat`） |
| **关系** | `gradlew` 不负责实现编译逻辑；它只负责**下载并启动**项目指定版本的 Gradle，再把 `test`、`build` 等任务交给真正的 Gradle 执行 |

一句话：**Gradle 是引擎，gradlew 是带版本号的点火钥匙。**

日常开发、CI 里应优先用 `./gradlew`，而不是裸 `gradle`。这样所有人、每台机器用的是 `gradle-wrapper.properties` 里锁定的同一版本，避免「我这能编、你那报错」。

### Wrapper 相关文件

这些文件**应提交到 Git**（官方建议）：

| 路径 | 作用 |
| ---- | ---- |
| `gradlew` | Unix/macOS 启动脚本 |
| `gradlew.bat` | Windows 启动脚本 |
| `gradle/wrapper/gradle-wrapper.jar` | 小 bootstrap 程序，负责下载真正的 Gradle 发行包 |
| `gradle/wrapper/gradle-wrapper.properties` | 锁定 Gradle 版本，核心是 `distributionUrl` |

`distributionUrl` 示例：

```properties
distributionUrl=https\://services.gradle.org/distributions/gradle-9.6.0-bin.zip
```

首次运行 `./gradlew` 时，Wrapper 会把对应 zip 下载到 `~/.gradle/wrapper/dists/`，之后复用缓存。

### 执行流程（简化）

```text
./gradlew test
    → gradlew 读取 gradle-wrapper.properties
    → 本地无该版本则下载 Gradle 9.6.0
    → 启动 Gradle Daemon
    → 执行 test 任务（编译、跑 JUnit 等）
```

### 何时用 `gradle`，何时用 `./gradlew`

| 场景 | 推荐命令 |
| ---- | -------- |
| 日常编译、测试、打包 | `./gradlew build`、`./gradlew test` |
| CI / 协作者未装 Gradle | 只能用 `./gradlew` |
| 升级项目 Wrapper 版本 | 本机需已装 Gradle：`gradle wrapper --gradle-version 9.6.0` |
| 临时全局试命令 | `gradle`（版本随本机安装，可能与项目不一致） |

**JDK 与 Gradle 版本也要匹配。** 例如 JDK 26 需要 Gradle 9.4+ 才能作为运行 Gradle 的 JVM；老项目若 Wrapper 仍是 8.x，在 JDK 26 上可能直接启动失败——这时应升级 Wrapper，而不是降级 JDK。

### 常用 Wrapper 命令

```bash
./gradlew tasks          # 列出可用任务
./gradlew test           # 运行全部单元测试
./gradlew build          # 编译 + 测试 + 打包
./gradlew run            # 运行 application 插件配置的 main（若项目配置了）
./gradlew --version      # 查看本项目 Wrapper 锁定的 Gradle 版本
```

更多任务示例见 [Gradle basic, command](../language/java/gradle-command.md)。

## 项目目录里常见文件

| 路径 | 是否提交 Git | 说明 |
| ---- | ------------ | ---- |
| `build.gradle` / `build.gradle.kts` | 是 | 构建脚本 |
| `settings.gradle` / `settings.gradle.kts` | 是 | 多模块项目入口 |
| `gradle/wrapper/` | 是 | Wrapper 二进制与版本配置 |
| `gradlew`、`gradlew.bat` | 是 | Wrapper 启动脚本 |
| `src/` | 是 | 源码 |
| `build/` | 否 | 编译产物 |
| `.gradle/` | 否 | Gradle 缓存与元数据，本地自动生成 |
| `out/` | 否 | 部分 IDE 输出目录 |

## Gradle 与 Maven 对比（JDK 26 背景下）

两者都是 JVM 项目的构建工具：Gradle 用 Groovy/Kotlin DSL（`build.gradle.kts`），Maven 用 XML（`pom.xml`）。在 **JDK 26** 时代，「能不能用新 JDK」已不再是 Gradle 的独占优势——**最新稳定版两边都能跑**，选型应看项目形态和团队习惯。

### JDK 26 兼容性

| | Gradle 9.6 | Maven 3.9.16 |
| ---- | ---- | ---- |
| 构建工具本身跑在 JDK 26 上 | 9.4+ 官方支持 | 3.9.15+ 已修复 Java 26 控制台等问题 |
| 用 JDK 26 编译 / 测试 | Toolchain + `sourceCompatibility` | Toolchains + `maven-compiler-plugin` |
| 版本锁定 Wrapper | `./gradlew` + `gradle-wrapper.properties` | `./mvnw` + `.mvn/wrapper/maven-wrapper.properties` |

JDK 26 的语言与编译变化（默认 `--release 26`、JEP 500 等对反射的限制等）主要靠 **编译器与依赖库升级** 解决；构建工具负责调度，不替代码自动适配新语法。

**版本门槛（2026 年中）：** JDK 26 上跑 Gradle 需 Wrapper **9.4+**；Maven 建议 **3.9.15+**。老 Wrapper（如 Gradle 8.x）在 JDK 26 上可能直接启动失败，应升级 Wrapper 而非降级 JDK。

### 核心差异

| 维度 | Gradle | Maven |
| ---- | ------ | ----- |
| 配置风格 | DSL 脚本，可写逻辑与抽象 | XML + 约定，结构固定 |
| 学习曲线 | 灵活但脚本可能变复杂 | 标准项目上手快，XML 冗长 |
| 扩展方式 | 自定义 task、插件、Kotlin 代码 | 插件 + profile，少写「构建逻辑」 |
| 大型 / 多模块项目 | Configuration Cache、增量构建往往更有优势 | 成熟稳定，企业模板多 |
| 生态示例 | Spring Boot、Android 文档里 Gradle 常见 | 传统企业 Java、发布与私服插件极广 |
| 适合场景 | 多模块、定制 task、已在用 Kotlin DSL | 标准 Java 库、团队偏好「零脚本」构建 |

### 各自仍有的优势

**Gradle 更适合：**

- 多模块 monorepo，构建脚本需要条件分支、任务编排
- 需要 Configuration Cache / Build Cache 优化增量构建
- 项目已用 `build.gradle.kts`，或团队熟悉 Kotlin DSL
- 与 Spring Boot Gradle 插件、Android Gradle Plugin 等深度集成

**Maven 更适合：**

- 标准 Java 项目：依赖 + 插件即可，不想在构建里写代码
- 团队统一 `pom.xml` 结构，CI / 运维模板遍地
- 企业发布、签名、私服、静态分析等靠成熟 Maven 插件链
- 追求「构建只描述 what，不描述 how 的程序逻辑」

### 小项目怎么选

单模块 demo、几个 main + JUnit（例如本地 `java-playground` 一类仓库）：**Gradle 与 Maven 都能胜任**，JDK 26 不是换工具的理由。若已配置好 `./gradlew`，继续用 Gradle 即可；若团队只熟 Maven，换过去也不会因为 JDK 26 而吃亏。

```text
JDK 26  →  两者都支持，构建工具升到最新稳定版即可
选哪个  →  看项目复杂度与团队习惯，不是看 JDK 版本
```

Maven 基础命令见 [mvn, maven basic](./maven.md)。

## Gradle 修改缓存目录 `.gradle` 路径

```bash
export GRADLE_USER_HOME=/Users/lshare/.gradle
```

背景：Android Studio 的 Gradle 在缓存处理上有时会出问题，必要时需要手动删缓存再编译；有时也需要把缓存指到别的磁盘。

### 一针见血的设置方法（本文采用）

在 Gradle 安装目录，编辑 `bin/gradle`，找到：

```text
# Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this
```

在其下增加：

```bash
GRADLE_OPTS=-Dgradle.user.home=/yourpath/gradle/gradle_cache
```

适合需要用 Gradle 脚本编译、且希望全局生效的环境。

### 其他方法

**方法 1**：Android Studio 设置里改 Service directory path（仅 AS 编译场景）。

**方法 2**：在 `gradle.properties` 中增加（每个项目都要加一次）：

```properties
gradle.user.home=D:/Cache/.gradle
```

**方法 3**：环境变量（推荐与上面二选一）：

```bash
export GRADLE_USER_HOME=D:/Cache/.gradle
```

**方法 4**：命令行参数：

```bash
gradle -g D:/Cache/.gradle build
```

`gradle -help` 可查看各参数含义。

总结：个人推荐改 `bin/gradle` 或设置 `GRADLE_USER_HOME`。

参考：[CSDN - Gradle 修改缓存路径](http://blog.csdn.net/yanzi1225627/article/details/52024632)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 补充 Gradle 与 gradlew（Wrapper）关系、文件说明、常用命令；修正 categories；截断英文段落并入正文 | 说明 Wrapper 机制，便于 java-playground 等项目的日常用法 |
| 2026-06-20 | 补充 Gradle 与 Maven 对比（含 JDK 26 兼容性）；文内 Gradle 版本示例更新为 9.6.0 | 选型参考 |
