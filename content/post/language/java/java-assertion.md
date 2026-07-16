---
title: Java 断言（assert）
author: "-"
date: 2012-09-21T08:16:05+00:00
lastmod: 2026-06-20T14:03:52+08:00
url: java-assertion
categories:
  - language
tags:
  - java
  - remix
  - AI-assisted
aliases:
  - /p4159/
---

`assert` 自 [JDK 1.4](./jdk-1-4.md) 起成为 Java 语言关键字，在 JDK 21、25 等当前版本中依然存在，语法与语义未变。但它**不是**单元测试框架里的断言，也**不适合**承担业务代码对外契约校验。本文说明语法、运行时开关，以及在新版本 Java 里何时该用、何时不该用。

## 与现代 Java 的关系

`assert` 没有被废弃，也没有被新语法取代。JDK 5 之后的泛型、JDK 7 的 `Objects.requireNonNull`、JDK 14 的 `switch` 表达式等，解决的是**类型安全、空值检查、控制流**等问题，与 `assert` 的「内部不变量检查」定位不同。

现代代码里更常见的替代手段：

| 场景 | 更常见的做法 |
| ---- | ------------ |
| 对外参数校验 | `Objects.requireNonNull`、`IllegalArgumentException`、Bean Validation |
| 不可达分支 | `switch` 的 `default` 抛异常，或 `sealed` + 穷尽匹配 |
| 单元测试断言 | JUnit `assertEquals`、AssertJ `assertThat`、TestNG `assertTrue` |
| 开发期内部不变量 | 少数团队仍用 `assert`；更多团队用显式 `if` + 抛 `IllegalStateException` |

结论：**`assert` 在新版本 Java 里仍可用，但已不是主流推荐写法**；日常业务与库 API 更倾向显式异常，测试用测试框架断言。

## 与单元测试断言的区别

这是两个完全不同的概念：

| | Java `assert` | JUnit / AssertJ 等 |
| -- | ------------- | ------------------ |
| 形式 | 语言关键字 | 测试框架 API |
| 默认行为 | 运行时**关闭**，需 `-ea` 开启 | 测试运行时**始终执行** |
| 失败时 | 抛出 `AssertionError`（`Error` 子类） | 抛出 `AssertionFailedError` 等，标记测试失败 |
| 典型用途 | 源码里的内部不变量 | 验证方法返回值、异常、状态 |

单元测试几乎**不会**用 Java `assert` 关键字来写断言。Maven Surefire、Gradle 默认也不给测试进程加 `-ea`。测试里应使用框架提供的 `assert*` 方法。

## 业务代码里建议用吗

**不建议**把 `assert` 当作业务逻辑的一部分，原因如下。

### 1. 生产环境默认关闭

`assert` 在 JVM 启动时默认不启用。线上进程通常不带 `-ea`，`assert` 语句等于不存在。若用它校验用户输入、外部 API 响应、数据库字段，等于**没有校验**。

### 2. 失败类型是 Error，不是可控异常

`assert` 失败抛出 `AssertionError`，继承 `Error` 而非 `Exception`。按 Java 惯例，`Error` 表示 JVM 或程序处于不可恢复状态，业务代码不应依赖捕获它来做流程控制。

### 3. Effective Java 的划分

Joshua Bloch 在 *Effective Java* 中区分两类检查：

- **参数校验**（precondition）：调用方可能传错 → 用 `IllegalArgumentException`、`NullPointerException`（`Objects.requireNonNull`）等，**必须**在关闭 `assert` 时也生效。
- **内部不变量**（invariant）：仅开发者逻辑错误才会触发 → 才适合考虑 `assert`。

公共 API 的参数检查**不能**用 `assert`；私有方法里对「调用方已保证成立」的前提，历史上有人用 `assert`，但今天更常见的是显式 `if` + `IllegalStateException`，行为不依赖 `-ea`。

### 4. 副作用表达式

`assert` 的布尔表达式在关闭时不求值，开启时求值。若表达式含方法调用或状态修改，开启/关闭 `assert` 会导致不同行为，容易埋坑。`Objects.requireNonNull` 等则始终执行。

### 实践建议

| 代码类型 | 是否建议用 `assert` |
| -------- | ------------------- |
| Controller / Service 业务逻辑 | 否，用显式校验 + 业务异常 |
| 对外公开的库 API | 否 |
| 私有方法内部不变量（开发期） | 可以，但团队内不统一时优先 `IllegalStateException` |
| 单元测试 | 否，用 JUnit / AssertJ |
| 算法原型、本地调试 | 可以，配合 `-ea` |

## 语法

两种形式：

```java
assert expression;
assert expression : detail;
```

- `expression`：布尔表达式。
- `detail`：可选；失败时传给 `AssertionError` 构造参数，类型为任意表达式（常用于字符串拼接说明）。

```java
assert value > 0;
assert value > 0 : "value=" + value;
assert ref != null : "ref is null";
assert isBalanced();
```

语义：

- **关闭** `assert`：语句无操作，`expression` 与 `detail` 均不求值。
- **开启** `assert`：先求值 `expression`；为 `false` 时抛出 `AssertionError`；为 `true` 且带 `detail` 时不再计算 `detail`。
- 若求值过程中先抛出其他异常，则传播该异常，不会变成 `AssertionError`。

## 编译与运行

JDK 1.4 起 `assert` 已是关键字，现代 JDK **无需** `-source 1.4` 即可编译。

运行时通过 JVM 参数控制（默认全部关闭）：

| 参数 | 含义 |
| ---- | ---- |
| `-ea` / `-enableassertions` | 开启用户类断言 |
| `-da` / `-disableassertions` | 关闭用户类断言 |
| `-esa` / `-enablesystemassertions` | 开启系统类断言 |
| `-dsa` / `-disablesystemassertions` | 关闭系统类断言 |

常见组合：

| 命令示例 | 说明 |
| -------- | ---- |
| `java -ea MyApp` | 开启所有用户类 |
| `java -da MyApp` | 关闭所有用户类 |
| `java -ea:com.example.pkg MyApp` | 仅开启指定包 |
| `java -ea:com.example.pkg... MyApp` | 开启包及其子包 |
| `java -ea:MyClass MyApp` | 仅开启指定类 |
| `java -dsa:MyClass:pkg1 MyApp` | 关闭指定类与包 |

`...` 表示包及其子包；单独 `...` 表示默认（无名）包。

程序内也可用 `ClassLoader` 动态调整：`setDefaultAssertionStatus`、`setPackageAssertionStatus`、`setClassAssertionStatus`、`clearAssertionStatus`。

## 设计要点

- **运行时开关**：与 C 语言编译期 `NDEBUG` 不同，Java 在运行时决定是否检查，同一份字节码可带或不带 `-ea` 运行。
- **`AssertionError` 是 `Error`**：强调「不应恢复的逻辑错误」，而非普通运行时异常。
- **无继承语义**：子类开启断言不会自动开启父类中的 `assert`；按**声明所在类**的包/类名匹配 `-ea` / `-da`。

继承示例：父类 `Base.baseMethod()` 含 `assert false`，子类 `Derived` 的 `main` 调用它时：

| 命令 | 结果 |
| ---- | ---- |
| `java Derived` | 不触发，正常打印 |
| `java -ea Derived` | 在 `Base` 的 assert 处失败 |
| `java -ea:Derived Derived` | 仅子类 assert 生效，`Base` 的不检查 |

## 适用场景（若仍选择使用）

仅在 `-ea` 开启时有意义，且表达式应短小、无副作用：

1. **不可达分支**：`switch` 的 `default: assert false;`（今天更推荐 `default` 直接抛 `IllegalStateException`）。
2. **私有方法前提**：调用方已保证的条件，如 `assert param != null`（公共方法应抛 `NullPointerException`）。
3. **复杂计算后的内部不变量**：如 `assert value >= 0` 验证私有算法中间状态。
4. **类不变量**：多方法共享的状态关系，在关键操作前后检查（需注意性能与是否依赖 `-ea`）。

反例：用 `assert` 检查 HTTP 请求参数、解析 JSON 字段、判断用户权限——这些必须在 `assert` 关闭时同样有效。

## 小结

- `assert` 在现行 JDK 中**仍然合法**，但属于**边缘特性**，不是现代 Java 的默认风格。
- **单元测试**用 JUnit / AssertJ 等，**不是** Java `assert` 关键字。
- **业务代码**应对外契约用显式异常与校验框架；**不要**指望生产环境默认开启的 `assert`。
- 若团队保留 `assert`，限定在私有实现、开发/测试环境 `-ea`，并避免带副作用的表达式。

## 参考资料

- [JSR 41: A Simple Assertion Facility](https://jcp.org/jsr/detail/41.jsp)
- [Programming With Assertions](https://docs.oracle.com/javase/8/docs/technotes/guides/language/assert.html)（Oracle 文档，适用于各版本语义说明）
- Joshua Bloch, *Effective Java*, Item 9: Check parameters for validity

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 重写全文；补充现代 Java 使用建议；整理语法、JVM 参数与表格；更新 front matter | 原 IBM 转载稿格式损坏且缺少当前实践指导 |
