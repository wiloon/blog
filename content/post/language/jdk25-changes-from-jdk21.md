---
title: JDK 21 升级到 JDK 25 的变更汇总
author: "-"
date: 2026-06-19T18:56:22+08:00
lastmod: 2026-06-19T18:56:22+08:00
url: jdk25-changes-from-jdk21
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
---

JDK 21（2023-09，LTS）到 JDK 25（2025-09，LTS）之间跨越了 JDK 22、23、24 三个非 LTS 版本。JDK 25 是 JDK 21 之后的**下一个 LTS**，Oracle 计划每两年发布一个 LTS（21 → 25 → 29）。

本文汇总这四个版本的重要变更，重点关注 breaking change 和需要主动迁移的部分。JDK 21 之前的变更见 [JDK 17 升级到 JDK 21 的变更汇总](./jdk21-changes-from-jdk17.md)；JDK 25 之后的变更见 [JDK 26 相对 JDK 25 的变化](./java/jdk-26.md)。

## JDK 22（2024 年 3 月）

### 正式特性

**JEP 454: Foreign Function & Memory API（正式版）**

[Project Panama](./java/project-panama.md) 的核心 API 定稿，替代 JNI 处理本地代码互操作：

```java
// 调用 C 库函数
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();
MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateFrom("hello");
    long len = (long) strlen.invoke(str);
}
```

**JEP 456: Unnamed Variables & Patterns（正式版）**

用 `_` 表示有意忽略的变量或模式绑定：

```java
// 忽略变量
int _ = computeSideEffect();

// 忽略 record 组件
if (r instanceof Point(int x, int _)) { ... }

// 增强 for 循环
for (var _ : items) { process(); }
```

**JEP 458: Launch Multi-File Source-Code Programs**

`java` 启动器可直接运行多文件源码程序，无需先手动编译全部源文件。

### 预览 / 孵化特性

- **JEP 447**: `super(...)` 之前的语句（预览）— 为 JEP 513 Flexible Constructor Bodies 铺路
- **JEP 457**: Class-File API（第一次预览）
- **JEP 461**: Stream Gatherers（第一次预览）
- **JEP 462**: Structured Concurrency（第二次预览）
- **JEP 463**: 隐式声明类与实例主方法（第二次预览）
- **JEP 464**: Scoped Values（第二次预览）
- **JEP 459**: 字符串模板（第二次预览；该特性后续已从路线图中移除，勿依赖）
- **JEP 460**: Vector API（第七次孵化）

### 运行时改进

- **JEP 423**: G1 Region Pinning — 改善 G1 与本地内存（如 FFM）交互时的 GC 行为

---

## JDK 23（2024 年 9 月）

### Breaking Change

**ZGC 默认启用分代模式（JEP 474）**

JDK 23 起 ZGC 默认以分代（Generational）模式运行。若应用针对非分代 ZGC 做过精细调优，需显式检查 GC 日志与延迟指标。

**废弃 `sun.misc.Unsafe` 内存访问方法（JEP 471）**

`Unsafe` 中直接操作堆外内存的方法标记为待移除，建议迁移到 Foreign Function & Memory API。JDK 24 起会对使用发出警告（JEP 498）。

### 新特性

- **JEP 467**: Markdown 文档注释 — Javadoc 支持 Markdown 语法
- **JEP 455**: 原语类型模式匹配（第一次预览）— `instanceof` / `switch` 支持 `int`、`long` 等
- **JEP 476**: Module Import Declarations（第一次预览）
- **JEP 482**: Flexible Constructor Bodies（第二次预览）
- **JEP 477**: 隐式声明类与实例主方法（第三次预览）
- **JEP 466**: Class-File API（第二次预览）
- **JEP 473**: Stream Gatherers（第二次预览）
- **JEP 480**: Structured Concurrency（第三次预览）
- **JEP 481**: Scoped Values（第三次预览）

---

## JDK 24（2025 年 3 月）

### Breaking Change

**Security Manager 永久禁用（JEP 486）**

JDK 21 起调用 `System.setSecurityManager()` 会抛 `UnsupportedOperationException`；JDK 24 进一步：

- 启动参数 `-Djava.security.manager` 会导致 JVM **启动失败**
- 运行时安装 Security Manager 抛异常
- Security Manager 相关 API 变为空操作，不再执行权限检查

绝大多数服务端应用不受影响。若仍依赖 Security Manager 做沙箱，需迁移到容器、OS 级隔离（seccomp、SELinux）或第三方方案。

**移除 ZGC 非分代模式（JEP 490）**

ZGC 仅保留分代模式，无法再切换回非分代实现。

**移除 Windows 32 位 x86 端口（JEP 479）**

Windows x86 32 位 JDK 构建不再提供。

**JNI 使用限制准备（JEP 472）**

为限制 JNI 滥用做准备；FFM API 是官方推荐的替代路径。

**`sun.misc.Unsafe` 内存访问警告（JEP 498）**

使用已废弃的 `Unsafe` 内存访问方法时，运行时会发出警告。

### 正式特性

**JEP 484: Class-File API（正式版）**

以标准 API 读写、转换 class 文件，替代 ASM 等第三方字节码库的常见场景：

```java
ClassModel classModel = ClassFile.of().parse(bytes);
for (ClassElement element : classModel) {
    if (element instanceof MethodModel m) {
        System.out.println(m.methodName());
    }
}
```

**JEP 485: Stream Gatherers（正式版）**

为 Stream API 增加自定义中间操作（gatherer），支持窗口、分组等灵活聚合。

**JEP 491: 虚拟线程同步不再 Pin 载体线程**

虚拟线程在 `synchronized` 块中不再固定（pin）到平台线程，高并发 I/O 场景下 `synchronized` 对虚拟线程的性能影响显著降低。行为变化可能影响依赖 pin 语义做线程本地假设的代码（极少见）。

### 实验 / 预览特性

- **JEP 483**: Ahead-of-Time Class Loading & Linking — AOT 缓存加速启动
- **JEP 404**: Generational Shenandoah（实验）
- **JEP 450**: Compact Object Headers（实验）— 缩小对象头，降低堆占用
- **JEP 478**: Key Derivation Function API（预览）
- **JEP 496 / 497**: 抗量子 KEM 与数字签名算法
- **JEP 493**: 无需 JMOD 链接运行时镜像
- **JEP 475**: G1 Late Barrier Expansion

---

## JDK 25（2025 年 9 月，LTS）

### Breaking Change

**移除 32 位 x86 端口（JEP 503）**

Linux / 其他平台的 32 位 x86 JDK 构建移除。仍在 32 位 x86 环境运行的应用无法直接升级。

### 正式特性

**JEP 506: Scoped Values（正式版）**

自 JDK 21 预览以来历经多轮迭代，在 JDK 25 定稿。不可变、层次化传播的线程绑定值，适合虚拟线程场景替代 `ThreadLocal`：

```java
public static final ScopedValue<String> USER = ScopedValue.newInstance();

ScopedValue.where(USER, "alice").run(() -> {
    System.out.println(USER.get()); // "alice"
});
```

**JEP 513: Flexible Constructor Bodies（正式版）**

子类构造函数中可在调用 `super(...)` 或 `this(...)` 之前执行语句（校验、日志等），不再强制将逻辑拆到静态工厂或辅助方法：

```java
class B extends A {
    B(int x) {
        if (x < 0)
            throw new IllegalArgumentException();
        super(x); // 校验语句可写在 super/this 之前
    }
}
```

**JEP 512: Compact Source Files and Instance Main Methods（正式版）**

简化单文件程序与 `main` 入口，降低入门门槛（由 JEP 463/477/495 演进而来）：

```java
void main() {
    IO.println("Hello");
}
```

**JEP 511: Module Import Declarations（正式版）**

模块可声明导入其他模块的包，简化 `module-info.java`：

```java
module com.example.app {
    import module java.base;
    // 或 import module java.sql;
}
```

**JEP 510: Key Derivation Function API（正式版）**

标准 KDF API（如 HKDF），用于从密钥材料派生加密密钥。

**JEP 521: Generational Shenandoah（正式版）**

Shenandoah GC 的分代模式从实验状态毕业，改善吞吐与延迟平衡。

### 预览 / 实验特性（LTS 中可用，API 可能变化）

| JEP | 内容 |
| --- | ---- |
| JEP 507 | 原语类型模式匹配（第三次预览） |
| JEP 505 | Structured Concurrency（第五次预览） |
| JEP 470 | PEM 加密对象编解码（预览） |
| JEP 502 | Stable Values / 惰性常量（预览，JDK 26 更名为 Lazy Constants） |
| JEP 508 | Vector API（第十次孵化） |
| JEP 514 | AOT 命令行工效学 |
| JEP 515 | AOT 方法剖析 |
| JEP 519 | Compact Object Headers（实验） |
| JEP 509 | JFR CPU-Time Profiling（实验） |
| JEP 518 | JFR Cooperative Sampling |
| JEP 520 | JFR Method Timing & Tracing |

### 语言与库亮点速览

- **AOT 启动优化**（JEP 514/515）：配合 JDK 24 的 AOT 类加载（JEP 483），显著缩短 Spring Boot 等框架的冷启动时间
- **JFR 增强**：CPU 时间剖析、协作采样、方法计时与追踪，生产可观测性更强
- **Compact Object Headers**（实验）：在支持的 GC 上缩小对象头，降低堆内存占用

### LTS 支持周期

| 阶段 | 截止时间（Oracle 路线图） |
| ---- | ------------------------- |
| Premier Support | 2030 年 9 月 |
| Extended Support | 2033 年 9 月 |

NFTC 许可下的免费更新计划至 JDK 29 LTS 发布后一年（约 2028 年 9 月），详见 [Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)。

---

## 变更汇总对照表

| 类别 | 变更项 | 引入版本 | 影响 |
| ---- | ------ | -------- | ---- |
| Breaking | Security Manager 永久禁用 | JDK 24 | 启动参数或运行时安装 SM 失败 |
| Breaking | 移除 32 位 x86 端口 | JDK 25 | 32 位 x86 环境无法升级 |
| Breaking | 移除 Windows 32 位 x86 | JDK 24 | Windows x86 32 位无构建 |
| Breaking | ZGC 仅保留分代模式 | JDK 24 | 非分代 ZGC 调优失效 |
| Breaking | `sun.misc.Unsafe` 内存访问废弃/警告 | JDK 23/24 | 需迁移到 FFM API |
| 新特性 | Foreign Function & Memory API | JDK 22（正式） | 替代 JNI 的本地互操作方案 |
| 新特性 | Unnamed Variables `_` | JDK 22（正式） | 简化忽略绑定的写法 |
| 新特性 | Class-File API | JDK 24（正式） | 标准字节码读写 |
| 新特性 | Stream Gatherers | JDK 24（正式） | Stream 自定义中间操作 |
| 新特性 | Scoped Values | JDK 25（正式） | 虚拟线程友好的上下文传递 |
| 新特性 | Flexible Constructor Bodies | JDK 25（正式） | 构造函数体更灵活 |
| 新特性 | Compact Source Files | JDK 25（正式） | 简化单文件程序 |
| 新特性 | Module Import Declarations | JDK 25（正式） | 简化模块声明 |
| 新特性 | Generational Shenandoah | JDK 25（正式） | Shenandoah 分代 GC |
| 新特性 | 虚拟线程 `synchronized` 不 pin | JDK 24 | 高并发场景性能提升 |
| 新特性 | AOT 类加载与启动优化 | JDK 24/25 | 冷启动加速 |
| 预览 | 原语类型模式匹配 | JDK 23 起 | `switch` 匹配 `int` 等 |
| 预览 | Structured Concurrency | 持续预览 | 结构化并发任务管理 |

## 升级建议（21 → 25）

1. **先升到 JDK 24 做验证**：Security Manager、ZGC、Unsafe 警告等 breaking change 集中在 24，便于分步排查。
2. **排查 Security Manager**：搜索 `-Djava.security.manager`、`policy` 文件、`System.setSecurityManager`。
3. **JNI / Unsafe 迁移**：新本地互操作用 FFM API；堆外内存访问从 `Unsafe` 迁到 `MemorySegment`。
4. **虚拟线程**：JDK 24 后可在 `synchronized` 中更放心使用虚拟线程，但仍建议 I/O 密集路径优先用 `ReentrantLock` 或异步 API。
5. **生产选型**：JDK 25 为当前推荐 LTS；无需逐版经过 22/23/24，可直接从 21 跳到 25，但需覆盖上述 breaking change 的回归测试。

## 参考

- [OpenJDK JDK 22](https://openjdk.org/projects/jdk/22/)
- [OpenJDK JDK 23](https://openjdk.org/projects/jdk/23/)
- [OpenJDK JDK 24](https://openjdk.org/projects/jdk/24/)
- [OpenJDK JDK 25](https://openjdk.org/projects/jdk/25/)
- [JEP 486: Permanently Disable the Security Manager](https://openjdk.org/jeps/486)
- [Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)
- 本站：[JDK 17 → 21 变更](./jdk21-changes-from-jdk17.md)、[JDK 26 相对 25 变更](./java/jdk-26.md)
