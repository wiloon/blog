---
title: JDK 7
author: "-"
date: 2017-03-25T01:59:05+00:00
lastmod: 2026-06-20T12:33:14+08:00
url: jdk-7
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
aliases:
  - java-7-新特性
  - java-7-numeric-literals
  - jdk-7-features
---

JDK 7（Java SE 7）于 2011 年 7 月发布，是 Java 6 之后的一次重要版本更新。相对 JDK 6，主要变化集中在**语言语法**、**NIO 文件 API**、**并发框架**、**JVM/GC** 和**诊断工具**几方面。

## 概览

### 语言与编译器

- 钻石操作符（Diamond Operator）`<>` 
- try-with-resources 自动资源管理
- 多异常捕获（multi-catch）
- `switch` 支持 `String`
- 二进制整数字面量（`0b` 前缀）
- 数字字面量中的下划线

### 类库

- NIO.2（`java.nio.file`）：`Path`、`Files`、目录遍历、`WatchService`
- 异步 I/O：`AsynchronousSocketChannel` 等
- 并发增强：`ForkJoinPool`、[`Phaser`](../../cs/java-7-phaser.md)、`LinkedTransferQueue`、`ThreadLocalRandom`
- JDBC 4.1
- `invokedynamic` 与 Method Handles（JSR 292，为 JVM 动态语言与后续 Lambda 铺路）

### JVM 与 GC

- G1 垃圾收集器（7u4 起实验性提供）
- 字符串常量池从 PermGen 移至 Java Heap
- 64 位 HotSpot 默认启用 Compressed Oops

### 工具与诊断

- [`jcmd`](./jcmd.md) 与 Diagnostic Command 框架（见 [Attach API](./attach-api.md)）
- VisualVM 随 JDK 分发

---

## 钻石操作符

泛型实例化时，若右侧类型参数可从左侧声明推断，可省略重复的类型参数，写 `<>`：

```java
// JDK 6
Map<String, List<String>> map = new HashMap<String, List<String>>();

// JDK 7
Map<String, List<String>> map = new HashMap<>();
```

---

## try-with-resources

实现了 `AutoCloseable`（`Closeable` 的子接口）的资源，可在 try 语句中声明，块结束时自动调用 `close()`，且支持 suppressed exception：

```java
try (BufferedReader br = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
    return br.readLine();
}
```

JDBC 4.1 中 `Connection`、`Statement`、`ResultSet` 也实现了 `AutoCloseable`，可同样使用。

---

## 多异常捕获

一个 `catch` 块可同时捕获多种异常类型，异常参数隐式为 `final`：

```java
try {
    // ...
} catch (IOException | SQLException ex) {
    logger.log(Level.SEVERE, ex.getMessage(), ex);
}
```

---

## switch 支持 String

`switch` 的 case 标签可以是 `String`（内部基于 `hashCode` 与 `equals` 实现，注意 `null` 会抛 `NullPointerException`）：

```java
String key = "A";
switch (key) {
    case "A":
        System.out.println("A");
        break;
    case "B":
        System.out.println("B");
        break;
    default:
        System.out.println("other");
}
```

---

## 二进制字面量与数字下划线

JDK 7 起整数字面量可用 `0b` / `0B` 表示二进制；可在数字之间插入 `_` 提高可读性（编译时忽略，不能出现在数字开头/结尾或小数点旁）：

```java
int mask = 0b0010_0101;
long ccNumber = 1234_5678_9012_3456L;
float pi = 3.14_15F;
long hex = 0xFF_EC_DE_5E;
int add = 12_3 + 3_2_1;
```

完整示例：

```java
public class NumericLiteralsDemo {
    public static void main(String[] args) {
        long ccNumber = 1234_5678_9012_3456L;
        long ssn = 999_99_9999L;
        float pi = 3.14_15F;
        byte byteInBinary = 0b0010_0101;
        long longInBinary = 0b11010010_01101001_10010100_10010010;
        System.out.println("ccNumber=" + ccNumber);
        System.out.println("byteInBinary=" + byteInBinary);
    }
}
```

---

## NIO.2（java.nio.file）

JDK 7 引入全新的文件 API，替代部分 `java.io.File` 的用法：

| 类 / 接口 | 作用 |
| ---- | ---- |
| `Path` / `Paths` | 路径表示与解析 |
| `Files` | 读写、复制、移动、删除、属性读写 |
| `DirectoryStream` | 目录遍历 |
| `FileVisitor` | 递归遍历目录树 |
| `WatchService` | 监听目录变更事件 |

```java
Path dir = Paths.get("/tmp/data");
Files.createDirectories(dir);
Path file = dir.resolve("hello.txt");
Files.write(file, "JDK 7 NIO.2".getBytes(StandardCharsets.UTF_8));
List<String> lines = Files.readAllLines(file);
```

---

## 并发增强

### ForkJoin 框架

[`ForkJoinPool`](../../cs/fork-join.md) 与 `ForkJoinTask` 面向可分解的计算密集型任务，采用工作窃取（work-stealing）调度，适合分治算法。

### Phaser

[`Phaser`](../../cs/java-7-phaser.md) 是可重用的同步屏障，支持动态注册/注销参与者，比 `CyclicBarrier` 更灵活，适合多阶段并行流水线。

### 其他

- `LinkedTransferQueue`：实现 `TransferQueue`，支持生产者直接 hand-off 给消费者
- `ThreadLocalRandom`：高并发场景下比 `Random` 更高效

---

## invokedynamic 与 Method Handles

JSR 292 在 JVM 字节码层加入 `invokedynamic` 指令，并提供 `java.lang.invoke` 包（`MethodHandles`、`MethodType` 等）。JDK 7 本身几乎用不到，但为 Groovy、JRuby 等动态语言以及 **JDK 8 Lambda** 的实现奠定了基础。

---

## JVM 与 GC 变化

### G1 垃圾收集器

G1（Garbage-First）在 JDK 7u4 以**实验性**选项提供（`-XX:+UseG1GC`），面向大堆、可预测停顿；JDK 9 起成为默认 GC 之一。详见 [InfoQ：JDK 7 G1](http://www.infoq.com/cn/articles/jdk7-garbage-first-collector)。

### 字符串常量池位置

JDK 7 将字符串常量池从 **PermGen** 移到 **Java Heap**。这意味着：

- `-XX:StringTableSize` 可调（默认约 60013）
- 大量 `intern()` 不再直接挤占 PermGen，但仍会占用堆内存

PermGen 在 JDK 8 中被 **Metaspace** 取代（见 [JDK 8](./jdk-8.md)）。

---

## 工具

- **jcmd**：统一诊断入口，可列出 Java 进程、触发 GC、查看 VM 标志等（JDK 7u40 起完善，见 [`jcmd`](./jcmd.md)）
- **VisualVM**：监控 CPU、内存、线程，分析堆 dump

---

## 与 JDK 8 的衔接

JDK 7 解决了泛型样板代码、资源泄漏、文件 API 老旧等痛点；JDK 8 在此基础上引入 Lambda、Stream、`java.time` 等更大规模的语法与类库变革。对比阅读：[JDK 8](./jdk-8.md)。

---

## 参考

- [Java 7 新特性（IBM developerWorks）](https://www.ibm.com/developerworks/cn/java/j-lo-jdk7-1/)
- [Java 7 的 6 个新特性](http://blog.ubone.com/blog/2014/11/18/java-7de-6ge-xin-te-xing/)
- [Underscores in Numeric Literals](https://www.yiibai.com/java/underscores-in-numeric-literals-java-7-feature.html)
- [JDK 7 Garbage First Collector（InfoQ）](http://www.infoq.com/cn/articles/jdk7-garbage-first-collector)
- [OpenJDK JDK 7 Project](https://openjdk.org/projects/jdk7/)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 文件重命名为 `java-7-numeric-literals.md`；更新 title、url、categories、tags；整理正文与参考链接 | 文件名含中文不符合规范；内容与标题对齐 |
| 2026-06-20 | 重命名为 `jdk-7-features.md`；扩展为 JDK 7 全特性概览；添加 aliases | 用户需要系统了解 JDK 7 引入的特性 |
| 2026-06-20 | title 改为「JDK 7 特性」；修正 JDK 8 站内链接 | 全系列统一命名，去掉「新特性」 |
| 2026-06-20 | 重命名为 `jdk-7.md`；title 改为「JDK 7」；url 改为 `jdk-7` | 全系列统一简洁命名 |
