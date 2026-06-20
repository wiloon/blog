---
title: JDK 9
author: "-"
date: 2016-01-05T01:13:07+00:00
lastmod: 2026-06-20T12:49:58+08:00
url: jdk-9
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
aliases:
  - java-9
  - jdk-9-features
  - /p8623/
---

JDK 9（Java SE 9）于 2017 年 9 月 21 日发布。相对 JDK 8，最重要的变化是 **Java 平台模块系统（JPMS）**，以及 **`java.version` 去掉前导 `1.`**（[JEP 223](https://openjdk.org/jeps/223)）。版本号背景见 [Java 版本历史](./java-version-history.md)。

## 版本号说明

| 维度 | JDK 8 | JDK 9 |
| ---- | ----- | ----- |
| `java.version` | `1.8.0_xxx` | `9`、`9.0.1` 等 |
| 里程碑 | 对外 Java 8、对内仍 1.x | 对外与系统属性一致 |

详见 [Java 版本历史](./java-version-history.md)。

## 概览

### 平台与模块化

- Java 平台模块系统（JPMS，Project Jigsaw）
- `jlink`：定制运行时镜像
- `jmod`：模块打包格式
- 基于模块的 Runtime 镜像

### 语言与 API

- JShell（REPL）
- 接口 `private` 方法
- 集合工厂方法（`List.of`、`Set.of`、`Map.of` 等）
- Stream API 增强（`takeWhile`、`dropWhile`、`iterate`）
- `Optional` 增强
- Process API 改造
- VarHandle、Stack-Walking API
- 多版本 JAR（Multi-Release JARs）
- HTTP/2 Client（孵化）

### JVM、GC 与工具

- G1 成为默认 GC
- 统一 JVM 日志（Unified JVM Logging）
- 从 JDK 中移除 Java EE / CORBA 等模块（改由外部维护）
- Compact Strings（内部字符串存储优化）

---

## 模块系统（JPMS）

JDK 9 引入 `module-info.java` 描述模块依赖与导出包，目标是强封装、可裁剪的运行时：

```java
module com.example.app {
    requires java.logging;
    exports com.example.api;
}
```

配合 `jlink` 可构建只含所需模块的自定义 JRE，缩小部署体积。

---

## JShell

交互式 REPL，快速验证语法与 API（对应早期 Kulla 项目）：

```text
$ jshell
jshell> int x = 3 + 4
x ==> 7
jshell> System.out.println(x)
7
```

---

## 集合工厂方法

不可变集合的便捷创建（JEP 269）：

```java
List<String> list = List.of("a", "b", "c");
Set<Integer> set = Set.of(1, 2, 3);
Map<String, Integer> map = Map.of("one", 1, "two", 2);
```

---

## Stream API 增强

```java
Stream.of(1, 2, 3, 4, 5)
    .takeWhile(n -> n < 4)   // 1, 2, 3
    .forEach(System.out::println);
```

---

## 接口 private 方法

接口中可声明 `private` 方法，供默认方法或静态方法复用，减少重复代码。

---

## Process API

`ProcessHandle` 提供进程树信息；`Process.onExit()` 支持异步等待子进程结束，替代部分轮询 `exitValue()` 的写法。

---

## HTTP/2 Client（孵化）

`java.net.http` 包提供新的 HTTP Client API，支持 HTTP/2 与 WebSocket（JDK 11 中成为正式 API）。

---

## G1 默认 GC

JDK 9 起 HotSpot 默认使用 G1（JEP 248）。G1 在 JDK 7u4 以实验选项首次出现（见 [JDK 7](./jdk-7.md)）。

---

## 从 JDK 中移除的组件

Java EE 模块（如 JAXB、JAX-WS）、CORBA 等不再随 JDK 分发，需单独引入依赖。这是模块化后「JDK 只保留核心、扩展外置」策略的一部分。

---

## 与后续版本

- JDK 10～16：半年发布节奏下的增量 JEP
- JDK 17（LTS）：[JDK 17](./jdk-17.md)
- JDK 21（LTS）：[JDK 21 相对 JDK 17 的变化](../jdk21-changes-from-jdk17.md)

## 参考

- [Java 9 新特性（IBM developerWorks）](https://www.ibm.com/developerworks/cn/java/the-new-features-of-Java-9/index.html)
- [Java 9 On Track（InfoQ）](http://www.infoq.com/cn/news/2015/05/Java-9-On-Track-For-2016)
- [JEP 223: New Version-String Scheme](https://openjdk.org/jeps/223)
- [JEP 261: Module System](https://openjdk.org/jeps/261)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 重命名为 `jdk-9-features.md`；扩展为 JDK 9 全特性概览；补充版本号说明 | 整理文档；记录版本命名演变 |
| 2026-06-20 | title 改为「JDK 9 特性」 | 「新特性」仅适用于发布当期，回顾性文档用「特性」 |
| 2026-06-20 | 重命名为 `jdk-9.md`；title 改为「JDK 9」；url 改为 `jdk-9` | 全系列统一简洁命名 |
| 2026-06-20 | 版本号说明精简，链到 [Java 版本历史](./java-version-history.md) | 集中维护命名演变 |
