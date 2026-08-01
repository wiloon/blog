---
title: "Compiled vs Interpreted: 编译型、解释型与脚本语言"
author: "-"
date: 2026-08-01T11:12:13+08:00
lastmod: 2026-08-01T11:12:13+08:00
url: compiled-vs-interpreted
aliases:
  - script-language
categories:
  - development
tags:
  - compiled
  - interpreted
  - script
  - aot
  - jit
  - java
  - python
  - rust
  - go
  - javascript
  - remix
  - AI-assisted
---

## 背景

教材里常把编程语言分成 **编译型（compiled）** 和 **解释型（interpreted）**。二者是一组相对概念，但现代语言大多落在光谱中间，不宜一刀切。

**脚本语言（scripting language）** 在日常说法里，往往就是解释型一侧的别名，或更窄一点：强调「缩短 edit-compile-link-run、以源码直接跑、做自动化 / 嵌入」的那一类解释型语言。下文先讲编译 / 解释，再单独说脚本。

## 两种执行路径

| 类型 | 典型流程 | 运行时依赖 |
| ---- | -------- | ---------- |
| 编译型 | 源码 → 编译器 → **机器码 / 本地二进制** → 直接由 OS 加载执行 | 一般不需要语言自带的解释器；可内嵌 runtime（如 GC） |
| 解释型 | 源码（或中间表示）由 **解释器** 边读边执行 | 必须安装对应解释器 / 运行时 |

对照：

```text
编译型（AOT）:  源码 ──compile──► 本地二进制 ──► 运行
解释型:         源码 ──► 解释器逐句执行
字节码 + VM:    源码 ──compile──► 字节码 ──► 解释 / JIT ──► 机器码
```

「预编译 / ahead-of-time（AOT）」说的是：**运行前**就编成可执行形态；日常口语里常与「编译型」混用。注意 C 里的「预编译」有时指 `#include` / `#define` 的**预处理**，那是编译流水线的一步，不是语言分类。

## 脚本语言：解释型的别名 / 子类

脚本语言最初是为了缩短传统的 **编写 → 编译 → 链接 → 运行**（edit-compile-link-run）周期：源码即交付物，由解释器（或宿主里的引擎）执行，不必先产出独立本地二进制。

和「解释型」的关系可以这样理解：

| 说法 | 含义 |
| ---- | ---- |
| 粗分 | 脚本 ≈ 解释型（相对 C/Go/Rust 等编译型） |
| 细分 | 脚本是解释型里偏 **自动化、胶水、嵌入、快速迭代** 的一类；强调用法与交付形态，而不只是「有没有解释器」 |

边界本来就模糊：Python、JavaScript 既写大型系统，也常被叫脚本语言；Go 语法像脚本，执行路径却是编译型。

### 常见特征

- 通常 **解释执行**（或引擎内字节码 + JIT），不单独部署「与运行时无关」的本地 exe
- 交付物多为 **文本源码**；改完即可跑，部署周期短
- 常用于 Shell 自动化、浏览器 / 游戏 / 应用内嵌、胶水层把已有组件串起来
- 可分 **独立型**（如 Python、Bash，完全依赖本语言解释器）与 **嵌入型**（如 Lua 嵌进游戏、JS 嵌进浏览器）

### 相对编译型的利弊（概括）

| | 说明 |
| ---- | ---- |
| 利 | 开发 / 部署快；易嵌入；可在运行时生成并执行代码 |
| 弊 | 依赖解释器或宿主；峰值性能与大型工程结构上通常不如系统级编译语言 |

具体语言见 [Shell 脚本](./shell-script.md)、[JavaScript](../web/javascript.md)、[Lua](../language/lua.md)。

## 常见语言落在哪

### 偏编译型（AOT 出本地代码）

- **C / C++**：`gcc` / `clang` 等到机器码
- **Go**：静态编译，产物是单一二进制（见 [go basic](./golang.md)）
- **Rust**：AOT 静态类型语言（见 [rust basic](../rust/rust-basic.md)）
- **Zig、Swift（多数场景）** 等

特点：启动快、部署常是「拷贝二进制」；跨平台要为每个目标再编一次（或交叉编译）。

### 偏解释型 / 脚本

- **Python（CPython）**：`.py` → 编译成 `.pyc` 字节码 → 解释器执行；近年还有实验性 JIT。日常仍常说「解释型 / 脚本」，因为交付物通常是源码，且强依赖 `python` 运行时。
- **Ruby、PHP（经典模式）、Shell、Lua** 等：多数也有字节码或中间表示，但用户感知仍是「装解释器再跑」。

### JavaScript：口语解释型 / 脚本，引擎里早已不是「逐行翻译」

**JavaScript** 在分类题里几乎总被归为 **解释型 / 脚本语言**：交付的是 `.js` 源码（或打包后的 JS），运行依赖浏览器或 Node 里的引擎，没有「先 `javac` 再部署 `.class`」那种独立编译产物。

现代引擎（如 V8）实际路径大致是：

```text
.js ──parse──► AST ──► 字节码 ──► 解释执行
                      └──热点──► JIT ──► 机器码
```

- 冷代码：解释（或廉价编译）起步，启动快
- 热点：JIT 编成机器码，长时间跑的循环可以很快
- 和 Rust/Go 不同：一般**不会**在部署前产出与引擎无关的本地二进制（除非另走特殊工具链）

因此：答题写「解释型 / 脚本」没问题；写实现细节时说 **「源码交付 + 引擎内字节码 / JIT」** 更准。相关：[JavaScript](../web/javascript.md)、[TypeScript](../web/typescript.md)（TS 先编译成 JS，再交给同一套引擎）。

### Java / C#：不要简单标成「解释型」或「脚本」

**Java** 的默认路径是：

```text
.java ──javac──► .class 字节码 ──► JVM（解释 + JIT）──► 机器码
```

- 有明确的**编译步骤**（到字节码），所以常说「编译型语言」也不算错
- 默认**不**直接生成本地可执行文件，运行依赖 JVM；早期以解释为主，现代 HotSpot 对热点做 **JIT**（见 [JVM](../language/java/jvm.md)、[HotSpot JIT](../language/java/hotspot-jit.md)）
- 若走 GraalVM Native Image，则可进一步 **AOT 成本地二进制**（见 [GraalVM Native Image](../language/java/graalvm-native-image.md)）

因此：**Java ≠ 典型解释型 / 脚本**，也 **≠ Rust/Go 那种默认 AOT 本地编译**；更准确是 **字节码 + 虚拟机（解释 / JIT，可选 AOT）**。

C# / .NET 类似：IL + CLR，另有 Native AOT 等路径。

## 一张对照表

| 语言 | 常见归类（口语） | 更准确的说法 |
| ---- | ---------------- | ------------ |
| C / Go / Rust | 编译型 | AOT → 本地机器码 |
| Python / Shell / Lua | 解释型 / 脚本 | 源码 →（常有字节码）→ 解释器 |
| JavaScript | 解释型 / 脚本 | 引擎内字节码 + JIT（V8 等） |
| Java | 常被误说成解释型 | 源码 → 字节码 → JVM 解释 / JIT（可选 Native AOT） |

## 和静态 / 动态类型不是一回事

| 维度 | 问的是什么 | 例子 |
| ---- | ---------- | ---- |
| 编译 vs 解释 | **何时、如何**变成可执行指令 | Go 编译；Python 解释 |
| 静态 vs 动态类型 | **类型检查**主要在编译期还是运行期 | Rust 静态；Python 动态 |
| 脚本 vs 系统语言 | **用法与交付**（自动化 / 嵌入 / 源码直跑） | Bash、Lua 偏脚本；C 偏系统 |

可以组合：Go 是静态 + 编译；Python 是动态 + 解释 / 脚本；Java 是静态 + 字节码/VM。

## 怎么选说法

1. 写教材对比时：用「编译型 / 解释型」作入门；需要强调自动化、胶水、嵌入时再用「脚本」
2. 脚本 ≈ 解释型的别名或子类，不要把脚本和解释型当成互斥的第三极
3. 写具体语言时：写清产物（本地二进制 / 字节码 / 源码直跑）和运行时（有无 VM、有无 JIT）
4. 避免：把 Java 简单等同于 Python 那种「解释型 / 脚本」；也避免把「有编译器」和「出本地 exe」当成一回事

## 相关文章

- [Shell 脚本](./shell-script.md)
- [JavaScript](../web/javascript.md)
- [TypeScript](../web/typescript.md)
- [Lua](../language/lua.md)
- [rust basic](../rust/rust-basic.md)
- [go basic](./golang.md)
- [Java 虚拟机](../language/java/jvm.md)
- [HotSpot JIT](../language/java/hotspot-jit.md)
- [GraalVM Native Image](../language/java/graalvm-native-image.md)
