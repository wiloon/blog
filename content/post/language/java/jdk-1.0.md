---
title: JDK 1.0
author: "-"
date: 2026-06-20T14:15:54+08:00
lastmod: 2026-06-20T14:15:54+08:00
url: jdk-1.0
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
---

JDK 1.0 于 **1995 年 5 月 23 日**由 Sun Microsystems 正式发布，是 Java 语言与平台的**第一个对外产品版本**。命名与后续演变见 [Java 版本历史](./java-version-history.md)。

## 1.0 之前还有别的「版本」吗？

**没有更早的对外编号版本。** 在 1.0 之前只有 Sun 内部的研发代号与预览构建，不算正式产品线：

| 阶段 | 时间（约） | 说明 |
| ---- | ---------- | ---- |
| Green 项目 | 1991 起 | Sun 内部面向消费电子设备的研究项目 |
| **Oak** | 1991～1995 | 语言与运行时的内部代号（James Gosling 等） |
| 更名 Java | 1995 初 | 因商标冲突放弃 Oak，改用 Java |
| Alpha / Beta | 1995 上半年 | 面向开发者的预览版，供 Applet 等场景试用 |
| **JDK 1.0** | 1995-05 | 首个公开发布、可商用的 JDK |

因此讨论「Java 最早版本」时，**1.0 就是起点**；Oak、Alpha、Beta 是开发史里的名称，不是 0.x 或更早的正式版本号。下一版为 [JDK 1.1](./jdk-1.1.md)（1997 年 2 月）。

## 版本号说明

| 维度 | JDK 1.0 |
| ---- | ------- |
| 对外名称 | Java 1.0 / JDK 1.0 |
| `java.version` | `1.0.x` |
| class major version | 45（1.0.2 起常见为 45.3） |
| 下一版本 | [JDK 1.1](./jdk-1.1.md) |

## 概览

1.0 已经具备今天仍熟悉的核心语言形态：类与接口、继承、包、`final` / `static` / `synchronized`、异常（含 checked exception）、数组、基本类型与 `String`。标准库规模很小——大约 **212 个类、8 个包**，许多今天常用的 API 尚未出现。

### 语言与并发

- 面向对象基础语法与 checked exception 模型
- `Thread` 与 `Runnable`，以及 `synchronized` 关键字（见 [Java 线程](./java-thread.md)）
- 尚无内部类、反射、断言、`strictfp` 等（内部类在 1.1，断言在 [JDK 1.4](./jdk-1.4.md)）

### 类库（1.0 已有）

- **`java.lang`**：`Object`、`String`、包装类、异常层次
- **`java.util`**：`Vector`、`Hashtable`、`Stack`、`Date` 等（**尚无** [集合框架](./collection-list-set-map-区别.md)，那是 1.2 引入）
- **`java.io`**：流式 I/O、`File`
- **`java.net`**：Socket 等基础网络 API
- **`java.awt`**：AWT 图形界面（重量级、依赖本地 peer）
- **Applet**：在浏览器中嵌入 Java 小程序的 API（1.0 时代 Java 走红的入口之一）

### 1.0 尚未具备（后续版本才加入）

| 能力 | 大致引入版本 |
| ---- | ------------ |
| 内部类、反射、JAR | 1.1 |
| Swing、集合框架、`java.lang.ref` | 1.2 |
| HotSpot 成为默认 VM | 1.3～1.4（见 [HotSpot](./hotspot.md)） |
| `assert`、NIO、标准正则 | 1.4 |
| 泛型、enum、for-each、JUC | 5 |

### JVM

1.0 附带的是 Sun 自研的**解释型**虚拟机，以字节码解释执行为主；JIT 与 [HotSpot](./hotspot.md) 是此后若干年逐步演进的结果，与今天的 OpenJDK 默认 VM 不是同一套实现。

## 历史背景（简述）

1995 年 Java 随 **Applet** 与 Netscape 等浏览器集成而迅速获得关注：「一次编写，到处运行」针对的是跨平台 GUI 与小段 Web 逻辑。企业级服务端大规模采用则要等到 1.1 的 JDBC、1.2 的集合与 Swing，以及 J2EE 时代之后。平台品牌从 J2SE 到 Java SE、发布节奏与 LTS 等，见 [Java 版本历史](./java-version-history.md)。

就个人时间线而言，JDK 1.0 发布的 **1995 年 5 月**，我仍在读**小学六年级**，暑假后就要上初中。那时对**计算机**还是完全未知的状态——Java 在硅谷与浏览器里起步，与东北小城镇的课堂、日常没有任何交集；要到许多年之后，才会真正接触编程。

## 参考

- [Java version history（Wikipedia）](https://en.wikipedia.org/wiki/Java_version_history)
- [Java Class File Version Numbers（Wikipedia）](https://en.wikipedia.org/wiki/Java_class_file#General_layout)
