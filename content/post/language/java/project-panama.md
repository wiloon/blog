---
title: Project Panama 与 Foreign Function & Memory API
author: "-"
date: 2026-06-19T19:12:54+08:00
lastmod: 2026-06-19T19:12:54+08:00
url: project-panama
categories:
  - language
tags:
  - java
  - jni
  - panama
  - remix
  - AI-assisted
---

Project Panama 是 OpenJDK 下的长期项目，目标是在 JVM 与 C 等本地代码之间建立更安全、更符合 Java 习惯互操作层。其交付物中最核心、与 [JNI](./java-jni.md) 直接对标的是 **Foreign Function & Memory API**（下称 FFM API，包名 `java.lang.foreign`），在 **JDK 22** 随 [JEP 454](https://openjdk.org/jeps/454) 正式定稿。

发音：英语读作 /ˈpænəmɑː/，音节大致为「帕-nuh-马」，与中美洲国家 Panama（巴拿马）相同。OpenJDK 以地峡（isthmus）比喻 JVM 与本地代码之间的桥梁，故取此名。

本文说明 Panama 解决什么问题、核心概念怎么用，以及与 JNI 的取舍。JDK 版本层面的变更见 [JDK 21 升级到 JDK 25 的变更汇总](../jdk25-changes-from-jdk21.md)。

## Panama 是什么

[Project Panama](https://openjdk.org/projects/panama/) 不只 FFM API，还包括：

| 组件 | 作用 |
| ---- | ---- |
| Foreign Function & Memory API | 调用 C 函数、读写堆外内存 |
| Vector API | SIMD 向量计算（另一 JEP 线，本文不展开） |
| jextract | 从 C 头文件生成 Java 绑定 |

日常说的「用 Panama 替代 JNI」，通常指 FFM API：用纯 Java + 标准库完成原本需要 `native` 方法、`javah` 头文件和 C/C++ 胶水代码的工作。

## 为什么需要替代 JNI

传统 [JNI](./java-jni.md) 流程大致是：

1. Java 声明 `native` 方法
2. `javac` / `javah` 生成 C 头文件
3. 手写 C/C++ 实现，手动处理 `jstring`、`jobject`、类型签名
4. 编译 `.so` / `.dll`，`System.loadLibrary` 加载

常见问题：

| 痛点 | 说明 |
| ---- | ---- |
| 开发成本高 | 每种类型都要查 JNI 签名（`J`、`Ljava/lang/String;` 等） |
| 易出错 | `FindClass`、`GetMethodID` 失败常在运行时才暴露 |
| 内存安全 | 本地堆与 Java 堆边界靠人工 `ReleaseStringUTFChars` 等配对 |
| 与 Java 模型割裂 | 不能自然地用 `MethodHandle`、布局描述符表达 C 结构体 |
| 演进方向 | JDK 24 起 [限制 JNI](https://openjdk.org/jeps/472)、废弃 `sun.misc.Unsafe` 内存访问，官方推荐迁到 FFM |

FFM API 把「函数签名」和「内存布局」变成 Java 里的第一类对象，由 JVM 做边界检查与生命周期管理（配合 `Arena`）。

## 核心概念

```text
SymbolLookup          在已加载的本地库中查找符号（如 strlen）
       ↓
FunctionDescriptor    描述 C 函数参数与返回值类型
       ↓
Linker.downcallHandle  生成可调用的 MethodHandle（Java → C）
       ↓
MemorySegment         一块连续内存（堆内或堆外），传给 C 指针
       ↓
Arena                 统一释放该作用域内分配的所有段
```

| 类型 | 职责 |
| ---- | ---- |
| `Arena` | 内存作用域；`ofConfined()` 单线程、`ofShared()` 可跨线程，关闭时释放其分配 |
| `MemorySegment` | 可读写的内存视图，可映射为 C 指针（`address()`） |
| `ValueLayout` | 标量布局，如 `JAVA_INT`、`ADDRESS`、`JAVA_LONG` |
| `MemoryLayout` / `StructLayout` | 结构体、数组等复合布局 |
| `Linker` | 在 Java `MethodHandle` 与本地函数间搭桥 |
| `FunctionDescriptor` | C 函数原型 |
| `SymbolLookup` | 查符号：`nativeLinker().defaultLookup()`（libc）、`loaderLookup()`（当前类加载器可见的库）、`LibraryLookup.of(path)` |

## 示例一：调用 C 标准库 `strlen`

等价于 JNI 里写一小段 C 胶水去调 `strlen`；FFM 直接在 Java 里完成。

```java
import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;

public class StrLen {
    public static void main(String[] args) throws Throwable {
        Linker linker = Linker.nativeLinker();
        SymbolLookup stdlib = linker.defaultLookup();

        MethodHandle strlen = linker.downcallHandle(
            stdlib.find("strlen").orElseThrow(),
            FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
        );

        try (Arena arena = Arena.ofConfined()) {
            MemorySegment cString = arena.allocateFrom("hello");
            long len = (long) strlen.invoke(cString);
            System.out.println(len); // 5
        }
    }
}
```

要点：

- `allocateFrom("hello")` 在堆外分配以 `\0` 结尾的 C 字符串
- `ADDRESS` 对应 C 的指针参数
- `Arena` 在 try-with-resources 结束时释放内存，无需手动 `free`

## 示例二：加载自定义动态库

假设有 C 函数 `int add(int a, int b)`，编译为 `libmath.so`：

```c
// math.c
int add(int a, int b) {
    return a + b;
}
```

```bash
gcc -shared -fPIC -o libmath.so math.c
```

Java 侧：

```java
import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;
import java.nio.file.Path;

public class CallAdd {
    public static void main(String[] args) throws Throwable {
        Linker linker = Linker.nativeLinker();

        try (Arena arena = Arena.ofConfined()) {
            SymbolLookup lookup = SymbolLookup.libraryLookup(
                Path.of("libmath.so"), arena
            );

            MethodHandle add = linker.downcallHandle(
                lookup.find("add").orElseThrow(),
                FunctionDescriptor.of(
                    ValueLayout.JAVA_INT,
                    ValueLayout.JAVA_INT,
                    ValueLayout.JAVA_INT
                )
            );

            int sum = (int) add.invoke(3, 4);
            System.out.println(sum); // 7
        }
    }
}
```

`LibraryLookup` 把库加载与符号查找绑在 `Arena` 生命周期上，库在 arena 关闭时卸载。

## 示例三：结构体与堆外布局

C 侧常见 `struct Point { int x; int y; }`。Java 用 `StructLayout` 描述内存布局，保证与 C 一致：

```java
import java.lang.foreign.*;

public class PointDemo {
    static final StructLayout POINT = MemoryLayout.structLayout(
        ValueLayout.JAVA_INT.withName("x"),
        ValueLayout.JAVA_INT.withName("y")
    );

    public static void main(String[] args) {
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment p = arena.allocate(POINT);
            POINT.set(MemoryLayout.PathElement.groupElement("x"), p, 0L, 10);
            POINT.set(MemoryLayout.PathElement.groupElement("y"), p, 0L, 20);

            int x = POINT.get(MemoryLayout.PathElement.groupElement("x"), p, 0L);
            int y = POINT.get(MemoryLayout.PathElement.groupElement("y"), p, 0L);
            System.out.println(x + ", " + y);
        }
    }
}
```

把 `p` 作为 `ADDRESS` 传给接受 `Point*` 的 C 函数即可。复杂头文件可配合 [jextract](https://github.com/openjdk/jextract) 从头文件生成 `MemoryLayout` 与包装类，减少手写布局。

## 示例四：读写字节缓冲区

FFM 可替代部分 `ByteBuffer.allocateDirect` + `Unsafe` 用法：

```java
try (Arena arena = Arena.ofConfined()) {
    MemorySegment seg = arena.allocate(64);
    seg.set(ValueLayout.JAVA_BYTE, 0, (byte) 42);
    byte b = seg.get(ValueLayout.JAVA_BYTE, 0);
}
```

`MemorySegment` 支持切片（`asSlice`）、按布局批量读写，并与 `FileChannel.map` 等 API 集成，用于零拷贝 I/O 场景。

## C 回调 Java（upcall）

FFM 也支持 upcall：把 Java 方法暴露为 C 函数指针，供本地代码回调。典型步骤：

1. 用 `Linker.upcallStub` 根据 `FunctionDescriptor` 生成函数指针（`MemorySegment`）
2. 将指针传给 C 库注册回调

比 JNI 的 `RegisterNatives` 更声明式，但样板代码仍不少；简单场景优先 downcall，复杂框架再考虑 upcall 或 jextract 生成代码。

## jextract

[jextract](https://github.com/openjdk/jextract) 是 Panama 配套工具（独立仓库，非 JDK 内置），读取 C 头文件，生成：

- 与 C `struct` 对应的 `MemoryLayout`
- 包装类或静态方法，简化 `downcallHandle` 创建

适合绑定大型 C API（如 SQLite、libcurl）。小型库手写几个 `FunctionDescriptor` 往往更直观。

## FFM API 与 JNI 对比

| 维度 | JNI | FFM API |
| ---- | --- | ------- |
| 语言边界 | 必须写 C/C++ 实现 | 多数场景纯 Java |
| 类型映射 | 手工查 JNI 签名 | `ValueLayout` / `FunctionDescriptor` |
| 字符串 / 对象 | `jstring`、`jobject` 手动转换 | `allocateFrom`、布局访问，或仍通过 JNI 处理复杂对象图 |
| 内存生命周期 | 手动 `Release*`、`DeleteGlobalRef` | `Arena` 统一释放 |
| 性能 | 成熟，调用开销低 | 多数 downcall 接近 JNI；极短函数可用 `Linker.Option.critical()` |
| JDK 要求 | 所有版本 | JDK 22+ 正式 API；17–21 为孵化/预览，包名与 API 有变动 |
| 复杂 Java 对象 | 成熟 | 传 `jobject` 仍常走 JNI；FFM 擅长标量、指针、结构体、缓冲区 |
| 官方态度 | 维护但不扩展；JNI 限制趋严 | 新互操作首选 |

## 何时仍用 JNI

以下情况 JNI 或混合方案仍合理：

- 需要频繁操作 Java 对象图（大量 `jobject` 字段读写）
- 已有大量 JNI 投资，迁移收益不明显
- 目标 JDK &lt; 22，且无法升级
- Android NDK：目前仍以 JNI 为主，Panama FFM 不在 Android 运行时上

新项目的 C 库互操作、堆外内存、替代 `Unsafe` 访问，在 JDK 22+ 上应优先评估 FFM API。

## 版本演进

| JDK | JEP | 状态 |
| --- | --- | ---- |
| 17 | 412 / 414 | 孵化（Foreign Memory Access + Incubator Foreign Function） |
| 18–21 | 419 / 424 / 434 等 | 多次孵化/预览，API 迭代 |
| 22 | 454 | 正式版（`java.lang.foreign`） |
| 23–24 | 471 / 498 | 推动从 `Unsafe` 迁出；JNI 限制准备 |
| 25+ | — | FFM 为 LTS 中的标准能力 |

## 延伸阅读

- [Project Panama 官网](https://openjdk.org/projects/panama/)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [Java JNI 入门](./java-jni.md)
- [JDK 21 → 25 变更（FFM 定稿）](../jdk25-changes-from-jdk21.md)
- [JNI 类型签名 `[B` `[C` 等](../../cs/jni左中括号bcc等.md)
