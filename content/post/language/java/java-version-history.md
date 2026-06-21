---
title: Java version history, jdk history
author: "-"
date: 2026-06-20T13:30:19+08:00
lastmod: 2026-06-21T18:53:36+08:00
url: java-version-history
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
aliases:
  - java
  - java/version
  - /p4288/
---

Java 由 Sun Microsystems 于 1995 年发布，2010 年起由 Oracle 维护。讨论「版本」时容易混用 **J2SE 1.4**、**Java 5**、**Java SE 8**、**JDK 17** 等说法——它们分属**平台品牌**、**对外版本号**、**运行时版本字符串**、**class 文件格式**等不同层次。下文先列发布简史与各版本文档链接，再分节说明命名如何演变。

## 发布简史

| 时间 | 版本 | 备注 |
| ---- | ---- | ---- |
| 1995-05 | Java 1.0 | 语言与平台首次发布 → [JDK 1.0](./jdk-1.0.md) |
| 1997-02 | Java 1.1 | 内部类、JAR、RMI 等 → [JDK 1.1](./jdk-1.1.md) |
| 1998-12 | Java 1.2 | **Java 2 Platform**；Swing、集合框架 |
| 1999-04 | HotSpot 首次发布 | 独立 JVM 产品，可配 JDK 1.2 → [HotSpot](./hotspot.md) |
| 1999-06 | J2SE / J2EE / J2ME | 三版平台划分 |
| 2000-05 | Java 1.3 | HotSpot 成为 JDK 默认 VM（Classic 仍可选） |
| 2002-02 | **J2SE 1.4** | assert、NIO、regex、JUL；Classic VM 移除 → [JDK 1.4](./jdk-1.4.md) |
| 2004-09 | **Java 5** | 泛型、enum、for-each、JUC → [JDK 5](./jdk-5.md) |
| 2005-06 | Java SE 6 公布 | J2SE 更名为 **Java SE** |
| 2006-12 | Java SE 6 GA | 脚本引擎、Web Service 增强 |
| 2011-07 | Java SE 7 GA | NIO.2、ForkJoin → [JDK 7](./jdk-7.md) |
| 2014-03 | Java SE 8 GA | Lambda、Stream → [JDK 8](./jdk-8.md)；后被 Oracle **追溯认定为 LTS** |
| 2017-09 | Java SE 9 GA | 模块系统、半年发布模型 → [JDK 9](./jdk-9.md) |
| 2018-03 | Java SE 10 | 短期版本 |
| 2018-09 | **Java SE 11** | **新发布策略下首个 LTS** |
| 2019～2021 | Java 12～16 | 短期版本 |
| 2021-09 | **Java SE 17** | LTS 间隔改为每 2 年 → [JDK 17](./jdk-17.md) |
| 2022～2023 | Java 18～20 | 短期版本 |
| 2023-09 | **Java SE 21** | → [JDK 21 相对 JDK 17 的变化](../jdk21-changes-from-jdk17.md) |
| 2024～2025 | Java 22～24 | 短期版本 |
| 2025-09 | **Java SE 25** | → [JDK 25 相对 JDK 21 的变化](../jdk25-changes-from-jdk21.md) |
| 2026-03 | Java SE 26 | → [JDK 26 相对 JDK 25 的变化](./jdk-26.md) |
| 2027-09 | Java SE 29（计划） | 下一 LTS |

2010 年 Oracle 收购 Sun；2017 年起 OpenJDK 成为参考实现。发行版选型见 [OpenJDK](./openjdk.md)；企业版演变见 [Java EE](./java-ee.md)。

---

## 四个层次，不要混用

| 层次 | 问的是什么 | 例子 |
| ---- | ------------ | ---- |
| 平台品牌 | 产品叫什么 | J2SE 1.4 → Java SE 6 |
| 对外版本号 | 口头/文档里的主版本 | Java 1.4 → Java 5 → Java 17 |
| `java.version` | JVM 报告的运行时版本字符串 | `1.4.2_19` → `1.8.0_xxx` → `17.0.x` |
| class major version | `.class` 文件格式版本 | 1.4 → 48；17 → 61（[完整对照](#class-文件-major-version)） |

做版本判断或读 GC 日志时，先分清问的是哪一层。

---

## 平台品牌：J2SE → Java SE

1998 年 JDK 1.2 发布时，Sun 将这一代平台整体称为 **Java 2 Platform**，并拆成三版：

| 旧称 | 新称（约 2005～2006 起） | 用途 |
| ---- | ------------------------ | ---- |
| J2SE | **Java SE** | 标准版（桌面、服务器） |
| J2EE | **Java EE** | 企业版（2017 年后捐给 Eclipse，称 Jakarta EE） |
| J2ME | **Java ME** | 微型版（嵌入式、手机） |

「Java 2」里的 **2** 表示平台代际（1.2 大改），不是版本号 2.0。1.3、1.4 时代仍叫 J2SE 1.x，名称容易让人困惑。

**转变时间线：**

- **2004，JDK 5**：对外主推 **Java 5**，文档中仍有 J2SE 5.0 旧称
- **2005～2006，JDK 6**：官方稳定使用 **Java SE 6**，J2 前缀基本退出

详见 [Java EE](./java-ee.md) 中对 J2 时代的说明。

---

## 对外版本号：1.x → Java 5

| 时期 | 对外叫法 | 内部/编译器版本 |
| ---- | -------- | --------------- |
| 1996～2004 | Java 1.0～1.4 / J2SE 1.x | 1.0～1.4 |
| 2004 起 | **Java 5**（不再强调 1.5） | 仍 `-source 1.5`，`java.version` 为 `1.5.0_xxx` |
| 2006～2017 | Java 6、7、8 | `1.6.0_xxx`～`1.8.0_xxx` |
| 2017 起 | Java 9、11、17… | JDK 9 起 `java.version` 也改为 `9`、`11` 等（见下节） |

**JDK 5 是对外主版本号命名的起点**；**JDK 9 是 `java.version` 字符串去掉前导 `1.` 的起点**（[JEP 223](https://openjdk.org/jeps/223)）。

---

## `java.version` 字符串

| JDK | `java.version` 示例 | 说明 |
| --- | ------------------- | ---- |
| 1.4 | `1.4.2_19` | 对内对外均 1.x |
| 5～8 | `1.5.0_xxx`～`1.8.0_xxx` | 对外已称 Java 5/8，字符串仍 1.x |
| 9+ | `9`、`11.0.2`、`17.0.9` | 与对外主版本号一致 |
| 9+ 更新版 | `9.0.1`、`11.0.16` | `$MAJOR.$MINOR.$SECURITY`  scheme |

代码里解析版本：JDK 8 及以前需处理 `1.8` 这种前缀；JDK 9 起可直接读主版本号。详见 [JDK 9](./jdk-9.md#版本号说明)。

---

## LTS 与发布节奏

**LTS（Long-Term Support，长期支持版）** 是 **2017 年 Java 9 起新发布模型**的一部分，与 J2SE→Java SE、JEP 223 发生在同一时期，但解决的是不同问题：后者管**怎么叫版本**，LTS 管**发布后支持多久**。

### 2017 年之前：没有 LTS 概念

1.4 → 5 → 6 → 7 → 8 大约 **2～3 年一版**，Oracle/Sun 对主流版本提供较长商业支持，但**不区分「LTS 版」和「短期版」**——每一版都是「大版本」，没有半年一发的 feature release。

### 2017 年起：半年一发 + LTS 分层

**Java 9（2017-09）** 起 Oracle 宣布新节奏：

| 类型 | 发布间隔 | OpenJDK 支持 | 典型用途 |
| ---- | -------- | ------------ | -------- |
| **Feature Release** | 每 6 个月 | 约 6 个月（至下一版发布） | 尝鲜、验证 |
| **LTS** | 最初约每 3 年；**JDK 17 起改为每 2 年** | 多年（厂商可延长） | 生产环境 |

同一时期还伴随：**模块系统**（JDK 9）、**`java.version` 去 `1.` 前缀**（JEP 223）、**OpenJDK 与 Oracle JDK 逐步对齐**。

**新模型下第一个 LTS 是 JDK 11**（2018-09）。JDK 8 后被 Oracle **追溯认定为 LTS**，但发布时尚无 LTS 概念，属于旧节奏最后一版。路线图见 [JDK 26 相对 JDK 25 的变化](./jdk-26.md) 及 [Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)。

---

## 参考

- [JEP 223: New Version-String Scheme](https://openjdk.org/jeps/223)
- [Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)
- [Java Class File Version Numbers（Wikipedia）](https://en.wikipedia.org/wiki/Java_class_file#General_layout)

---

## class 文件 major version

编译器 `-target` 决定生成的 class 格式。常见对照：

| Java 版本 | major version |
| --------- | ------------- |
| 1.2 | 46 |
| 1.3 | 47 |
| 1.4 | 48 |
| 5 | 49 |
| 6 | 50 |
| 7 | 51 |
| 8 | 52 |
| 9 | 53 |
| 10 | 54 |
| 11 | 55 |
| 12 | 56 |
| 13 | 57 |
| 14 | 58 |
| 15 | 59 |
| 16 | 60 |
| 17 | 61 |
| 18 | 62 |
| 19 | 63 |
| 20 | 64 |
| 21 | 65 |
| 22 | 66 |
| 23 | 67 |
| 24 | 68 |
| 25 | 69 |
| 26 | 70 |

可用 `javap -verbose Foo.class | grep major` 查看。反编译或加载高版本 class 到低版本 JVM 时会报 `UnsupportedClassVersionError`。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-21 | 发布简史补充 HotSpot 1999 发布；区分 1.3 默认与 1.4 移除 Classic VM | 与 hotspot.md 时间线对齐 |
