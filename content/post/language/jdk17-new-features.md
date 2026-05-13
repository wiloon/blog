---
title: JDK 17 新特性
author: "-"
date: 2026-04-25T10:27:40+08:00
lastmod: 2026-05-13T13:37:33+08:00
url: jdk17-new-features
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
---

## 概述

JDK 17 是 Java 的长期支持版本（LTS），于 2021 年 9 月发布。相比 JDK 16，JDK 17 引入了多项新特性和改进，同时也包含了一些孵化特性的正式毕业版本。

## 正式特性（JEP）

### JEP 306: 恢复始终严格的浮点语义

将浮点运算恢复为始终严格模式（strict），删除了 `strictfp` 关键字的限制效果。在历史上，Java 曾因不同硬件平台的差异引入了扩展精度模式，随着现代硬件的普及，该差异不再存在，因此恢复了一致的浮点行为。

### JEP 356: 增强型伪随机数生成器

提供新的接口和实现用于伪随机数生成器（PRNG），新增了 `RandomGenerator` 接口和多个算法实现，如 `Xoshiro256PlusPlus`、`L64X128MixRandom` 等。

```java
RandomGenerator generator = RandomGeneratorFactory.of("L64X128MixRandom").create();
int randomInt = generator.nextInt(100);
```

### JEP 382: 新的 macOS 渲染管道

使用 Apple Metal API 实现 Java 2D 渲染管道，替代已废弃的 OpenGL API，提升在 macOS 上的图形渲染性能。

### JEP 391: macOS/AArch64 移植

将 JDK 移植到 macOS/AArch64（Apple Silicon）平台，支持原生运行于 M1 及后续芯片的 Mac 电脑。

### JEP 398: 废弃 Applet API

正式废弃 Applet API，标记为 `@Deprecated(forRemoval = true)`。浏览器早已不再支持 Java 插件，该 API 已无实际用途。

### JEP 407: 移除 RMI Activation

移除远程方法调用（RMI）的激活机制，`java.rmi.activation` 包已被删除。RMI Activation 早在 JDK 15 就已废弃。

### JEP 409: 密封类（Sealed Classes）正式版

密封类和密封接口从预览版（JDK 15/16）升级为正式特性，**用来限制哪些类可以继承或实现某个类/接口**。

#### 解决了什么问题

Java 原有两个极端：`final` 类完全不能继承，普通类/接口任何人都能继承，缺少"只允许指定的几个子类"这个中间选项。密封类解决了以下问题：

**1. 模式匹配的穷举性检查**

没有密封类时，`switch` 无法知道所有子类，必须写 `default`，漏掉某种情况编译器不报错：

```java
// 旧写法：漏掉 Triangle 也不报错
String desc = switch (shape) {
    case Circle c -> "圆";
    case Rectangle r -> "矩形";
    default -> "未知";  // 掩盖了遗漏
};

// 密封类：漏掉 Triangle 编译器直接报错
String desc = switch (shape) {
    case Circle c -> "圆";
    case Rectangle r -> "矩形";
    // 编译错误：缺少 Triangle
};
```

**2. 表达领域约束**

某些业务类型天然有固定变体，密封类可以在类型系统层面强制表达这种约束，而不只是靠文档约定。

**3. 比枚举更强**

枚举每个值只是单例，无法携带不同的字段；密封类每种子类可以有完全不同的结构：

```java
sealed interface PaymentResult permits Success, Failure, Pending {}

record Success(String transactionId, BigDecimal amount) implements PaymentResult {}
record Failure(String errorCode, String message) implements PaymentResult {}
record Pending(String trackingId) implements PaymentResult {}
```

#### 核心关键字

- `sealed` — 声明该类/接口是密封的
- `permits` — 列出允许继承的子类
- 子类必须选择三者之一：
  - `final` — 不能再被继承
  - `sealed` — 继续密封，再限制下一级
  - `non-sealed` — 开放，任何人都可以继承

```java
public sealed interface Shape
    permits Circle, Rectangle, Triangle {}

public final class Circle implements Shape {
    double radius;
}

public final class Rectangle implements Shape {
    double width, height;
}

public non-sealed class Triangle implements Shape {
    double base, height;
}
```

#### 主要用途

1. **模式匹配**：配合 `switch` 表达式，编译器知道所有可能的子类型，可做完整性检查
1. **领域建模**：明确表达"这个类型只有这几种变体"，类似枚举但功能更强
1. **替代部分枚举**：当枚举的每个值需要携带不同数据时，密封类更合适

```java
// 编译器知道 Shape 只有三种，switch 不需要 default
double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius * c.radius;
    case Rectangle r -> r.width * r.height;
    case Triangle t  -> 0.5 * t.base * t.height;
};
```

### JEP 410: 移除实验性 AOT 和 JIT 编译器

移除实验性的提前编译（AOT）和 JIT 编译器（基于 Graal），这些功能维护成本高且使用者少。

### JEP 411: 废弃安全管理器

废弃 `SecurityManager`，标记为 `@Deprecated(forRemoval = true)`，未来版本将会移除。

### JEP 412: 外部函数与内存 API（孵化）

提供与 JVM 堆外内存和原生代码交互的 API，作为 JNI 的替代方案。（孵化阶段，JDK 19 升为预览版）

```java
// 分配堆外内存
try (MemorySegment segment = MemorySegment.allocateNative(100)) {
    // 操作堆外内存
}
```

### JEP 414: 向量 API（第二次孵化）

提供用于向量计算的 API，利用 SIMD 指令实现高性能并行计算，第二次孵化版本在 JDK 16 基础上进行了优化。

### JEP 415: 上下文相关的反序列化过滤器

增强 Java 序列化过滤机制，允许为每个反序列化操作设置上下文相关的过滤器，提高应用程序安全性。

## 与 JDK 16 的主要区别

| 特性                | JDK 16               | JDK 17                |
| ------------------- | -------------------- | --------------------- |
| 密封类              | 预览版（第二次）     | 正式版                |
| instanceof 模式匹配 | 正式版（JEP 394）    | 继续支持              |
| Record 类           | 正式版（JEP 395）    | 继续支持              |
| 随机数生成器        | 无                   | 新增 API（JEP 356）   |
| 外部函数与内存 API  | 孵化（JEP 393）      | 第二次孵化（JEP 412） |
| macOS Metal 渲染    | 无                   | 新增（JEP 382）       |
| macOS AArch64       | 无                   | 支持（JEP 391）       |
| 安全管理器          | 废弃（JEP 411 预告） | 废弃（JEP 411）       |
| RMI Activation      | 废弃                 | 移除（JEP 407）       |
| LTS 版本            | 否                   | **是**                |

## 版本信息

- 发布日期：2021 年 9 月 14 日
- LTS 版本，JEP 数量：14 个

### Oracle 官方支持周期

| 阶段               | 截止时间         | 说明                                                                   |
| ------------------ | ---------------- | ---------------------------------------------------------------------- |
| Premier Support    | 2026 年 9 月     | 全面支持：bug 修复、安全补丁、新功能更新、性能改进                     |
| Extended Support   | 2029 年 9 月     | 仅安全补丁和关键 bug 修复，不引入新功能，Oracle JDK 用户通常需额外付费 |
| Sustaining Support | 2029 年 9 月之后 | 无限期，仅提供已有补丁的访问，不再产出新补丁                           |

## 从 JDK 17 升级到 JDK 21 的策略

JDK 17 的 Premier Support 于 2026 年 9 月到期，下一个 LTS 版本是 JDK 21。推荐采用三阶段迁移，而非一步到位：

### 阶段一：替换废弃 API（在 JDK 17 上完成）

1. 用 `jdeprscan --release 21` 扫描废弃 API 使用情况
2. 替换 `SecurityManager`、`finalize()`、`Thread.stop()` 等将被移除的 API
3. 检查所有未显式指定字符集的代码（如 `new String(bytes)`、`new FileReader(file)`），统一改为 `StandardCharsets.UTF_8`——JDK 18 起默认字符集改为 UTF-8，这是最常见的隐性 breaking change

### 阶段二：升级第三方库（仍在 JDK 17 上运行）

找到同时兼容 JDK 17 和 JDK 21 的库版本作为过渡版本，逐库升级，不要一次全换：

- Spring Boot → 3.2+（同时支持 JDK 17 和 JDK 21）
- Mockito → 5.x
- ByteBuddy → 1.14+
- 其他字节码增强类框架同步升级

升级后部署上线，稳定运行一段时间再进行下一阶段。

### 阶段三：升级 JDK 到 21

代码和依赖都已验证稳定后，切换 JDK 版本，代码不动：

1. 跑完整测试套件
2. 上线，观察 GC 行为、线程池等运行指标

这样每个阶段都有独立的回滚点，出问题能快速定位是代码变更还是运行时升级引入的。

## 参考

- [JDK 17 Release Notes](https://www.oracle.com/java/technologies/javase/17-relnote-issues.html)
- [OpenJDK JDK 17](https://openjdk.org/projects/jdk/17/)
- [JDK 17 to JDK 21 Migration Guide](https://docs.oracle.com/en/java/javase/21/migrate/)
