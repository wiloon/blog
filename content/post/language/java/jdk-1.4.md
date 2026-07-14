---
title: JDK 1.4
author: "-"
date: 2026-06-20T13:22:57+08:00
lastmod: 2026-06-24T09:40:55+08:00
url: jdk-1.4
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
---

JDK 1.4（J2SE 1.4）于 2002 年 2 月发布。对外称 **Java 2 Platform, Standard Edition 1.4**；命名体系与后续演变见 [Java 版本历史](./java-version-history.md)。

1.4 GA 后，下一代 **Tiger（JDK 5）** 的语言特性即在 JCP 并行规划——含 **JSR 175 注解**（2002 年 3 月立项），并非等 1.4 维护多年后才起步。详见 [JDK 5](./jdk-5.md) §发布历程。

注意：[`jdk14.md`](./jdk14.md) 记录的是 **JDK 14**（2020），与本文的 **JDK 1.4** 不是同一版本。

## 版本号说明

| 维度 | JDK 1.4 |
| ---- | ------- |
| 平台品牌 | J2SE 1.4 |
| `java.version` | `1.4.2_19` 等 |
| class major version | 48 |
| 下一版本 | [JDK 5](./jdk-5.md) |

完整命名演变见 [Java 版本历史](./java-version-history.md)。

## 概览

### 语言

- [`assert` 断言](./java-assertion.md)（`-source 1.4` 编译，运行时 `-ea` 开启）

### 类库

- [`java.util.regex`](./java正则表达式.md) 正则表达式（详见 [分组与捕获](./java-正则表达式-分组与捕获.md)）
- **NIO**（`java.nio`）：Buffer、Channel、Selector、[内存映射文件](./java-randomaccessfile.md)
- **`java.util.logging`**（JUL，Java 原生日志，见 [commons-logging 与 log4j](./commons-logging-log4j.md)、[jcl-over-slf4j](./jcl-over-slf4j.md)）
- **`java.util.prefs`** Preferences API（用户/系统配置持久化）
- [**URI** 与 URL 区分](./java-url-uri.md)（`java.net.URI`）
- 链式异常（`Throwable.initCause()`）
- Image I/O、Java Web Start、Sound API 等

### JVM 与性能

- **HotSpot 成为唯一 VM**（1.4.0 起移除 Classic VM；HotSpot 自 JDK 1.3 起已是默认实现，见 [HotSpot](./hotspot.md)）
- **Parallel Scavenge** 新生代收集器（1.4.0）；1.4.1 起 GC 调优选项增强（见 [Java GC](./gc.md)）
- 1.4.2 引入**自旋锁**（`-XX:+UseSpinning`，见 [Java Lock](./java-lock.md)）

### 工具与诊断

- [JPDA](./java-debug-JPDA.md)（Java Platform Debugger Architecture）架构完善

---

## assert 断言

JDK 1.4 在语言层新增 `assert` 关键字，用于开发/测试阶段的条件检查；默认关闭，生产环境通常不启用。语法、`-ea` / `-da` 运行参数及设计取舍详见 [Java assertion](./java-assertion.md)。

```java
assert value >= 0 : "value must be non-negative: " + value;
```

编译需 `-source 1.4`；老版本 JDK 无法识别 `assert` 关键字。

---

## 正则表达式（java.util.regex）

JDK 1.4 之前 Java 无标准正则 API，需依赖第三方库。1.4 起内置 `Pattern` / `Matcher`：

```java
Pattern p = Pattern.compile("[A-Z0-9]{10}");
boolean ok = p.matcher("ABC1234567").matches();
```

入门与常用语法见 [Java 正则表达式](./java正则表达式.md)。

---

## NIO（New I/O）

`java.nio` 提供面向 Buffer / Channel 的 I/O 模型，支持非阻塞 I/O 与多路复用（`Selector`），是对传统 `InputStream` / `OutputStream` 的补充。

| 组件 | 作用 |
| ---- | ---- |
| `Buffer` | 内存缓冲区（`ByteBuffer` 等） |
| `Channel` | 与 Buffer 配合的 I/O 通道 |
| `Selector` | 多路复用，支撑 NIO 服务器 |
| `MappedByteBuffer` | 内存映射文件，可替代部分 [RandomAccessFile](./java-randomaccessfile.md) 场景 |

NIO 文件路径 API（`java.nio.file`）要到 [JDK 7](./jdk-7.md) 才引入（NIO.2）。

---

## java.util.logging

JDK 1.4 内置 JUL（Java Util Logging），提供标准日志 API。许多项目后来选用 Log4j、SLF4J 等；与 JUL 的桥接、选型讨论见 [commons-logging 与 log4j](./commons-logging-log4j.md)。

```java
Logger logger = Logger.getLogger("com.example");
logger.info("hello");
```

---

## URI 与 URL

JDK 1.4 起 `java.net.URI` 与 `URL` 职责分离：URI 表语法结构，URL 是含定位信息的 URI 特例。详见 [Java URL URI](./java-url-uri.md)。

---

## 链式异常

异常可通过 `initCause()` 关联根因，改善早期 Java 异常栈信息不足的问题：

```java
try {
    // ...
} catch (IOException ex) {
    throw new RuntimeException("read failed", ex); // JDK 1.4 起支持 cause 链
}
```

---

## 与 JDK 5 的衔接

JDK 1.4 尚无**泛型**、**增强 for 循环**、**自动装箱**、**enum**、**变长参数**等语法——这些均在 [JDK 5](./jdk-5.md) 引入。JDK 5 文档中的 JDK 1.4 对比示例（下标 for、`Iterator` + raw type）可作为理解语法演进的参考。

---

## 参考

- [J2SE 1.4 Documentation](https://docs.oracle.com/javase/1.4.2/docs/)
- [OpenJDK JDK 5 Project（含 1.4 历史）](https://openjdk.org/projects/jdk/)
- [Programming With Assertions（Oracle）](https://docs.oracle.com/javase/1.4.2/docs/guide/lang/assert.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-21 | 修正 HotSpot 表述：1.3 默认、1.4 移除 Classic VM | 与 hotspot.md、java-version-history 对齐 |
| 2026-06-24 | 首段补充 Tiger / JSR 175 与 1.4 的时间衔接；链到 jdk-5.md | 厘清 1.4 与 JDK 5 规划并行关系 |
| 2026-06-24 | 首段补充 Tiger / JSR 175 与 1.4 的衔接；链到 jdk-5.md | 厘清 1.4 与 JDK 5 规划时间线 |
