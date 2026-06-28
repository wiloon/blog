---
title: Java Classpath 与 Module Path
author: "-"
date: 2026-06-28T07:12:53+08:00
lastmod: 2026-06-28T07:12:53+08:00
url: classpath
categories:
  - language
tags:
  - java
  - jvm
  - classloader
  - maven
  - remix
  - AI-assisted
---

## Classpath 是什么

**Classpath（类路径）** 是 JVM 在运行时**查找 `.class` 文件和 JAR 包的搜索路径集合**。当代码里出现 `new Foo()` 或 `Foo.class` 时，类加载器要把 `com.example.Foo` 这个名字解析成磁盘上的 `com/example/Foo.class` 字节码，去哪里找，就由 classpath 决定。

可以把它理解成「类的 `PATH` 环境变量」：shell 的 `PATH` 决定 `ls`、`git` 这些命令去哪些目录找可执行文件；JVM 的 classpath 决定加载类时去哪些目录和 JAR 里找字节码。

一条 classpath 由多个条目组成，每个条目是**一个目录**或**一个 JAR/ZIP 文件**：

- 目录条目：以该目录为根，按包名展开找 `.class`（如条目 `target/classes` + 类 `com.foo.Bar` → 找 `target/classes/com/foo/Bar.class`）
- JAR 条目：把 JAR 当成一个打包的目录，在其中按同样规则找

分隔符与操作系统有关：**Linux/macOS 用冒号 `:`**，**Windows 用分号 `;`**。

## 如何设置 classpath

按优先级从高到低，常见几种方式：

| 方式 | 写法 | 说明 |
| ---- | ---- | ---- |
| `-cp` / `-classpath` | `java -cp app.jar:lib/* com.foo.Main` | 命令行显式指定，最常用；详见 [java -cp](./java-cp.md) |
| `CLASSPATH` 环境变量 | `export CLASSPATH=...` | 全局生效，易污染，现代项目基本不用 |
| 可执行 JAR 的 `Class-Path` | `MANIFEST.MF` 里的 `Class-Path:` | JAR 内清单声明依赖；见 [MANIFEST.MF](../../other/manifest-mf.md) |
| 默认值 | 不指定时为当前目录 `.` | 仅在没有任何设置时 |

`-cp` 支持通配符 `lib/*`（匹配该目录下所有 JAR，但**不递归**子目录），但不能写成 `lib/*.jar`。指定了 `-cp` 后默认的当前目录 `.` 会失效，需要的话要显式写进去。

## classpath 与依赖管理工具

平时写 Maven/Gradle 项目，几乎不手写 classpath——构建工具替你算好了：

1. Maven/Gradle 解析 `pom.xml` / `build.gradle` 的依赖树，下载所有 JAR 到本地仓库
2. 运行（`mvn exec`、IDE Run、`gradle bootRun`）时，工具把「你的 `target/classes` + 全部依赖 JAR」拼成一条很长的 classpath 传给 `java`

所以「某个依赖在不在 classpath 上」，本质就是「`pom.xml` 里有没有声明（且 scope 让它在运行期可见）这个依赖」。Spring Boot 的 `@ConditionalOnClass` 判断「classpath 上有没有某个类」，等价于在问「你引没引那个依赖 JAR」。

Spring Boot 打成 fat jar 后另有一套布局（`BOOT-INF/lib/` + 自定义 `JarLauncher`），不走标准 `Class-Path`，细节见 [Spring Boot Executable JAR](./spring/spring-boot-executable-jar.md)。

## classpath 与类加载器

classpath 是「去哪找」，类加载器是「怎么加载」。二者配合：**AppClassLoader（System ClassLoader）** 负责加载 classpath 上的类；核心库由 Bootstrap 加载，与 classpath 无关。双亲委托、命名空间等机制见 [Java ClassLoader](./classloader.md)。

一个常见误区：**「应用跑起来后所有操作都在读 classpath」是不对的**。只有「**首次加载某个类**」或「**读取 JAR 内资源**」（如 `getResourceAsStream`）才走 classpath；类一旦加载进方法区、对象在堆上运行，普通业务逻辑不会反复扫 classpath。

## Module Path（模块路径）

JDK 9 引入 **JPMS（Java Platform Module System，模块系统）** 后，多了一条与 classpath 并列的 **module path（模块路径，`--module-path` / `-p`）**。两者都是「找代码的路径」，但模型不同：

| 维度 | Classpath | Module Path |
| ---- | ---- | ---- |
| 引入版本 | 一直都有 | JDK 9+ |
| 单位 | 一堆松散的类 / JAR | **模块**（带 `module-info.class` 的 JAR，或 automatic module） |
| 封装 | 无；任何 public 类都可被任意访问 | 强封装：只有 `exports` 的包对外可见 |
| 依赖声明 | 隐式（全靠 classpath 拼对） | 显式：`module-info.java` 里 `requires` |
| 缺依赖何时报错 | 运行期 `NoClassDefFoundError` | **启动期**就校验模块图，缺失直接报错 |
| 重复/冲突 | 后者被遮蔽，易出诡异问题 | 同名模块冲突会启动失败，更早暴露 |

放在 classpath 上的普通 JAR 会进入一个特殊的 **unnamed module（无名模块）**，能读取所有模块、行为基本和 JDK 8 一致——这是为了向后兼容。也就是说，**你完全可以继续只用 classpath**，不碰模块系统，绝大多数应用（包括大量 Spring Boot 项目）至今如此。

模块系统主要解决两类历史问题：

- **可靠配置**：用 `requires` 显式声明依赖，把「缺 JAR 才在运行期崩」提前到启动期校验，替代脆弱的 classpath。
- **强封装**：用 `exports` 控制哪些包对外可见，内部实现包（如 `sun.misc.*`）真正藏起来，避免被随意调用。

JDK 自身从 JDK 9 起就模块化了（`java.base`、`java.sql` 等），这部分对所有程序生效；但**你的应用要不要模块化是可选的**。JPMS 的来龙去脉、`module-info`、automatic module 等见 [JPMS / Project Jigsaw](../../cs/jpms-jigsaw.md)。

## 小结

- classpath 是 JVM 查找类与 JAR 的搜索路径，相当于「类的 PATH」。
- 日常由 Maven/Gradle 自动拼装；`@ConditionalOnClass` 等「类在不在」本质是问「依赖引没引」。
- 只有加载类 / 读 JAR 资源才用到 classpath，不是运行期一直在扫。
- module path 是 JDK 9+ 的并列机制，带强封装与显式依赖；不用它时 JAR 进入 unnamed module，行为同传统 classpath。
