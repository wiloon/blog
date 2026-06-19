---
title: JDK 26 相对 JDK 25 的变化
author: "-"
date: 2026-06-19T18:49:31+08:00
lastmod: 2026-06-19T18:49:31+08:00
url: jdk-26
categories:
  - Java
tags:
  - java
  - openjdk
  - remix
  - AI-assisted
---

JDK 26 于 2026 年 3 月 17 日 GA，是紧接 JDK 25 LTS 之后的**短期特性版本**（非 LTS）。OpenJDK 为其提供约六个月的支持，至 2026 年 9 月 JDK 27 发布为止。生产环境仍以 JDK 25 LTS 为主；JDK 26 适合尝鲜新特性或验证升级路径。

参考：[JDK 26 项目页](https://openjdk.org/projects/jdk/26/)、[JDK 25 项目页](https://openjdk.org/projects/jdk/25/)、[JDK 26 Release Notes](https://jdk.java.net/26/release-notes)。

## 版本概览

| 项目 | JDK 25 | JDK 26 |
| ---- | ------ | ------ |
| 发布日期 | 2025-09-16 | 2026-03-17 |
| LTS | 是 | 否 |
| JSR | JSR 400 | JSR 401 |
| Class File 版本 | 69.0 | 70.0 |
| Unicode | 16.0.0 | 17.0.0 |
| 官方 JEP 数量 | 18 | 10 |

## JDK 26 新增或正式交付的 JEP

### JEP 500：Prepare to Make Final Mean Final

对通过深层反射修改 `final` 字段的行为发出**警告**，为后续在 JVM 层面严格禁止此类修改做准备。JDK 26 尚未完全封死，但应开始排查依赖 `setAccessible` 篡改 `final` 的代码。

### JEP 504：Remove the Applet API

移除 `java.applet` 包及相关 API。Applet 自 JDK 9 起已废弃，JDK 17 标记为待移除；现代浏览器早已不支持 NPAPI 插件，该 API 已无实际用途。仍引用 `Applet` 的代码在 JDK 26 上将无法编译。

### JEP 516：Ahead-of-Time Object Caching with Any GC

在 JDK 24/25 AOT 类加载与链接（JEP 483 等）基础上，将**对象缓存**扩展到可与**任意 GC** 配合使用。此前 AOT 缓存的对象布局与特定 GC 的堆头格式绑定；JDK 26 采用与 GC 无关、可流式传输的格式，使 ZGC、G1 等均可受益，加速应用冷启动。

### JEP 517：HTTP/3 for the HTTP Client API

标准库 `HttpClient` 新增 HTTP/3（基于 QUIC/UDP）支持。默认仍使用 HTTP/2；需显式指定版本。若服务端不支持 HTTP/3，客户端会透明降级到 HTTP/2。

### JEP 522：G1 GC: Improve Throughput by Reducing Synchronization

减少 G1 垃圾回收器中应用线程与 GC 线程之间的同步开销，提升吞吐量。属 HotSpot 运行时改进，无需改应用代码。

## 自 JDK 25 延续的预览 / 孵化特性

以下 JEP 在 JDK 25 中已出现，JDK 26 进入下一轮预览或孵化，并带有 API 或语义调整。

| JDK 26 JEP | JDK 25 对应 | 轮次 | 主要变化 |
| ---------- | ----------- | ---- | -------- |
| JEP 530 | JEP 507 | 原语类型模式匹配，第 4 次预览 | 增强 unconditional exactness；更严格的 dominance 检查 |
| JEP 526 | JEP 502 | Lazy Constants，第 2 次预览 | 自 Stable Values 更名；API 简化；新增 `List.lazyOf()`、`Map.lazyOf()` |
| JEP 525 | JEP 505 | Structured Concurrency，第 6 次预览 | `Joiner`、`StructuredTaskScope` 等接口继续演进 |
| JEP 524 | JEP 470 | PEM 编解码，第 2 次预览 | `PEMRecord` 更名为 `PEM`；加密 API 调整 |
| JEP 529 | JEP 508 | Vector API，第 11 次孵化 | 持续演进，尚未定稿 |

## JDK 25 有、JDK 26 未列入特性清单的内容

JDK 25 作为 LTS 集成了较多一次性交付的特性；下列 JEP 在 JDK 25 已落地或实验交付，**不属于** JDK 26 的增量 JEP 列表（不代表被移除，而是已在 25 中可用）：

| JEP | 简述 |
| --- | ---- |
| JEP 503 | 移除 32 位 x86 端口 |
| JEP 506 | Scoped Values（定稿） |
| JEP 509 | JFR CPU-Time Profiling（实验） |
| JEP 510 | Key Derivation Function API |
| JEP 511 | Module Import Declarations |
| JEP 512 | Compact Source Files and Instance Main Methods |
| JEP 513 | Flexible Constructor Bodies |
| JEP 514 | Ahead-of-Time Command-Line Ergonomics |
| JEP 515 | Ahead-of-Time Method Profiling |
| JEP 518 | JFR Cooperative Sampling |
| JEP 519 | Compact Object Headers |
| JEP 520 | JFR Method Timing & Tracing |
| JEP 521 | Generational Shenandoah |

从 JDK 25 升级到 JDK 26 时，上述能力通常**保留**；升级收益主要来自上文「新增或正式交付」及「延续预览」部分。

## 其他值得注意的变更（非独立 JEP）

- `Thread.stop()` 正式移除（参见 JDK-8368226）；该方法可能导致对象状态不一致，早已不推荐使用。
- `HttpBodyPublishers.ofFileChannel()`：支持通过 `FileChannel` 流式发送请求体，避免大文件整段读入内存。
- Javadoc 生成的 HTML 页面支持暗色模式。
- `InitialRAMPercentage` 默认值由 1 调整为更合理的堆初始比例（具体数值见 Release Notes）。
- 支持 Unicode 17.0.0。

## Java LTS 节奏

| 版本 | 类型 | 计划/实际发布 |
| ---- | ---- | ------------- |
| JDK 21 | LTS | 2023-09 |
| JDK 25 | LTS | 2025-09 |
| JDK 26–28 | 短期 | 每 6 个月一版 |
| **JDK 29** | **下一 LTS** | **2027-09（计划）** |

Oracle 自 JDK 17 起每**两年**发布一个 LTS。当前最新 LTS 为 **JDK 25**；下一个 LTS 为 **JDK 29**（计划 2027 年 9 月）。JDK 26、27、28 均为短期版本。

JDK 27 计划 2026 年 9 月发布。

## 相关链接

- [OpenJDK JDK 26](https://openjdk.org/projects/jdk/26/)
- [OpenJDK JDK 25](https://openjdk.org/projects/jdk/25/)
- [JDK 26 Release Notes](https://jdk.java.net/26/release-notes)
- [Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)
- 本站 OpenJDK 安装与发行版说明：[openjdk](./openjdk.md)
