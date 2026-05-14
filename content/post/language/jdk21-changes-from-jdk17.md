---
title: JDK 17 升级到 JDK 21 的变更汇总
author: "-"
date: 2026-05-13T13:37:33+08:00
lastmod: 2026-05-13T14:04:56+08:00
url: jdk21-changes-from-jdk17
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
---

JDK 17 到 JDK 21 跨越了 JDK 18、19、20 三个非 LTS 版本。本文汇总这四个版本引入的重要变更，重点关注 breaking change 和需要主动迁移的部分。

## JDK 18（2022 年 3 月）

### Breaking Change

**UTF-8 成为默认字符集（JEP 400）**

这是 17 → 21 迁移中最常见的隐性 breaking change。JDK 18 起，`Charset.defaultCharset()` 固定返回 UTF-8，不再跟随操作系统区域设置。

受影响的场景：

- `new String(bytes)` — 未指定编码，依赖平台默认值
- `new FileReader(file)` — 未指定编码
- `System.out.println()` 输出非 ASCII 字符
- 读写文件时未显式指定编码

**对 Linux 生产环境的实际影响**

大多数现代 Linux 发行版默认 locale 是 `en_US.UTF-8` 或 `zh_CN.UTF-8`，JDK 17 在这类环境下默认字符集本来就是 UTF-8，因此 JDK 18 的这一变更对标准 Linux 服务器**基本无感**。

真正有风险的场景：

- **Windows 开发/测试环境** — Windows 默认编码是 GBK/CP936，本地测试通过但部署到 Linux 后行为不同
- **精简容器镜像** — 某些极简 Docker 镜像不设置 locale，`LANG` 为空，JDK 17 此时默认字符集可能是 `US-ASCII`，升级到 JDK 18 后反而统一成了 UTF-8
- **遗留系统** — 有意依赖 GBK 平台编码处理中文数据（如读老数据库导出文件）的项目会出问题

修复方式：所有涉及字节/字符转换的地方显式指定 `StandardCharsets.UTF_8`。

```java
// 修复前（行为依赖平台）
String s = new String(bytes);
new FileReader(file);

// 修复后（行为确定）
String s = new String(bytes, StandardCharsets.UTF_8);
new FileReader(file, StandardCharsets.UTF_8);
```

### 新特性

- **JEP 408: 简单 Web 服务器** — `jwebserver` 命令，用于本地静态文件服务，开发调试用
- **JEP 413: Java API 文档中的代码片段**（`@snippet` 标签）
- **JEP 416: 使用方法句柄重新实现反射核心**（内部实现变更，API 不变）
- **JEP 417: 向量 API（第三次孵化）**
- **JEP 418: 互联网地址解析 SPI** — 可插拔的地址解析器，`InetAddress` 行为可自定义
- **JEP 419: 外部函数与内存 API（第二次孵化）**
- **JEP 420: switch 模式匹配（第二次预览）**
- **JEP 421: 废弃 Finalization** — `finalize()` 正式废弃，标记 `forRemoval`

---

## JDK 19（2022 年 9 月）

### 重要预览/孵化特性

- **JEP 425: 虚拟线程（第一次预览）** — Project Loom 的核心成果，轻量级线程
- **JEP 428: 结构化并发（孵化）** — 将多个并发任务作为一个工作单元管理
- **JEP 405: Record 模式（第一次预览）** — 在 `instanceof` 和 `switch` 中解构 record
- **JEP 427: switch 模式匹配（第三次预览）**
- **JEP 424: 外部函数与内存 API（预览）** — 从孵化升为预览
- **JEP 426: 向量 API（第四次孵化）**

### 移除/废弃

- `Thread.stop(boolean)` 已移除（`Thread.stop()` 无参版本在后续版本移除）

---

## JDK 20（2023 年 3 月）

### 重要预览/孵化特性

- **JEP 436: 虚拟线程（第二次预览）**
- **JEP 437: 结构化并发（第二次孵化）**
- **JEP 432: Record 模式（第二次预览）**
- **JEP 433: switch 模式匹配（第四次预览）**
- **JEP 434: 外部函数与内存 API（第二次预览）**
- **JEP 438: 向量 API（第五次孵化）**
- **JEP 429: 作用域值（孵化）** — 替代 `ThreadLocal` 的不可变线程绑定值

---

## JDK 21（2023 年 9 月，LTS）

### Breaking Change

**`Thread.stop()` 等方法实际抛出异常**

`Thread.stop()`、`Thread.suspend()`、`Thread.resume()` 在 JDK 21 调用时抛出 `UnsupportedOperationException`，不再有任何实际效果。

**`SecurityManager` 不可用**

JDK 17 废弃，JDK 21 调用 `System.setSecurityManager()` 会抛出 `UnsupportedOperationException`。

### 正式特性（从预览/孵化毕业）

**JEP 441: switch 模式匹配（正式版）**

```java
// 对任意类型进行模式匹配
Object obj = ...;
String result = switch (obj) {
    case Integer i -> "整数: " + i;
    case String s  -> "字符串: " + s;
    case null      -> "null";
    default        -> "其他";
};
```

**JEP 440: Record 模式（正式版）**

```java
// 解构 record
if (obj instanceof Point(int x, int y)) {
    System.out.println(x + ", " + y);
}

// 嵌套解构
if (shape instanceof Rectangle(Point(int x, int y), int w, int h)) {
    // ...
}
```

**JEP 444: 虚拟线程（正式版）**

Project Loom 的核心特性正式毕业。虚拟线程是轻量级线程，由 JVM 调度而非操作系统，适合高并发 I/O 密集型场景。

```java
// 创建虚拟线程
Thread vt = Thread.ofVirtual().start(() -> {
    System.out.println("虚拟线程运行中");
});

// 使用虚拟线程的 ExecutorService
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> doWork());
}
```

虚拟线程注意事项：

- `ThreadLocal` 仍可用，但在虚拟线程上大量使用会有内存压力，建议改用 Scoped Values
- 同步代码块（`synchronized`）会 pin 住载体线程，高并发时影响性能，建议改用 `ReentrantLock`
- 虚拟线程不建议用线程池，每个任务直接创建新虚拟线程即可

**JEP 445: 无名类和实例主方法（预览）**

简化 `Hello World`，降低初学门槛（JDK 21 为预览版）：

```java
// 无需 class 声明，无需 public static void main
void main() {
    System.out.println("Hello, World!");
}
```

**JEP 431: Sequenced Collections**

新增三个接口，为有序集合提供统一的首尾操作 API：

- `SequencedCollection` — `getFirst()`、`getLast()`、`addFirst()`、`addLast()`、`reversed()`
- `SequencedSet`
- `SequencedMap` — `firstEntry()`、`lastEntry()`、`reversed()`

```java
List<String> list = new ArrayList<>(List.of("a", "b", "c"));
list.getFirst(); // "a"
list.getLast();  // "c"
list.reversed(); // ["c", "b", "a"]
```

**JEP 430: 字符串模板（预览）**

```java
String name = "World";
String msg = STR."Hello, \{name}!";  // "Hello, World!"
```

**JEP 442: 外部函数与内存 API（第三次预览）**

**JEP 446: 作用域值（预览）**

替代 `ThreadLocal` 的方案，不可变、生命周期明确、对虚拟线程友好：

```java
static final ScopedValue<String> USER = ScopedValue.newInstance();

ScopedValue.where(USER, "alice").run(() -> {
    System.out.println(USER.get()); // "alice"
});
```

**JEP 453: 结构化并发（预览）**

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user  = scope.fork(() -> fetchUser());
    Future<Integer> order = scope.fork(() -> fetchOrder());
    scope.join().throwIfFailed();
    return new Response(user.resultNow(), order.resultNow());
}
```

### LTS 版本支持周期

| 阶段             | 截止时间     |
| ---------------- | ------------ |
| Premier Support  | 2028 年 9 月 |
| Extended Support | 2031 年 9 月 |

---

## 变更汇总对照表

| 类别     | 变更项                   | 引入版本       | 影响                              |
| -------- | ------------------------ | -------------- | --------------------------------- |
| Breaking | 默认字符集改为 UTF-8     | JDK 18         | 未指定编码的字节/字符转换可能乱码 |
| Breaking | `Thread.stop()` 抛异常   | JDK 21         | 调用直接失败                      |
| Breaking | `SecurityManager` 不可用 | JDK 21         | 调用直接抛异常                    |
| Breaking | `finalize()` 废弃        | JDK 18（废弃） | 将在后续版本移除                  |
| 新特性   | 虚拟线程                 | JDK 21（正式） | 高并发 I/O 场景性能大幅提升       |
| 新特性   | switch 模式匹配          | JDK 21（正式） | 替代繁琐的 instanceof 链          |
| 新特性   | Record 模式              | JDK 21（正式） | 解构 record，配合 switch 使用     |
| 新特性   | Sequenced Collections    | JDK 21（正式） | 有序集合统一 API                  |
| 新特性   | 结构化并发               | JDK 21（预览） | 简化并发任务管理                  |
| 新特性   | 作用域值                 | JDK 21（预览） | 替代 ThreadLocal                  |

## 参考

- [JDK 18 Release Notes](https://www.oracle.com/java/technologies/javase/18-relnote-issues.html)
- [JDK 19 Release Notes](https://www.oracle.com/java/technologies/javase/19-relnote-issues.html)
- [JDK 20 Release Notes](https://www.oracle.com/java/technologies/javase/20-relnote-issues.html)
- [JDK 21 Release Notes](https://www.oracle.com/java/technologies/javase/21-relnote-issues.html)
- [Migrating from JDK 17 to JDK 21](https://docs.oracle.com/en/java/javase/21/migrate/)
