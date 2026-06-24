---
title: "JLS: Java Language Specification"
author: "-"
date: 2026-06-23T21:07:11+08:00
lastmod: 2026-06-23T21:07:11+08:00
url: java-language-specification
categories:
  - language
tags:
  - java
  - JLS
  - remix
  - AI-assisted
---

## 什么是 JLS

**JLS**（Java Language Specification，Java 语言规范）是 Oracle 官方发布的权威文档，完整定义了 Java 编程语言的语法、语义和行为。

可以把它理解为 Java 语言的"宪法"——编译器、JVM 实现者以及语言特性设计者，都必须以 JLS 为准。

官方地址：[Java SE 规范](https://docs.oracle.com/javase/specs/)

---

## JLS 的主要内容

JLS 按章节组织，每章覆盖语言的一个核心方面：

| 章节 | 主题 |
| ---- | ---- |
| 第 2 章 | 词法结构（关键字、字面量、标识符） |
| 第 3 章 | 类型、值与变量 |
| 第 6 章 | 名称（作用域、遮蔽、访问控制） |
| 第 8 章 | 类声明 |
| 第 9 章 | 接口声明（含注解类型） |
| 第 14 章 | 语句 |
| 第 15 章 | 表达式 |
| 第 17 章 | 线程与锁（Java 内存模型） |

---

## 为什么要了解 JLS

大多数开发者日常不需要阅读 JLS，但以下场景中它非常有用：

- **理解边界行为**：遇到语言"奇怪"行为时（如整数溢出、字符串 `==` 比较、自动装箱陷阱），JLS 给出权威解释。
- **注解与反射**：JLS 第 9 章详细定义注解类型声明（`@interface`）的语法和语义，是理解注解底层的基础。
- **Java 内存模型**：JLS 第 17 章定义了可见性、有序性保证，是理解 `volatile`、`synchronized`、`happens-before` 的权威来源。
- **框架/工具开发**：编写编译器插件、注解处理器（APT）、字节码工具时，需要精确理解语言规范。

---

## JLS 与 JVM 规范的区别

JLS 和 JVMS（Java Virtual Machine Specification，Java 虚拟机规范）经常被混淆：

| 规范 | 定义的内容 | 关注对象 |
| ---- | ---------- | -------- |
| **JLS** | Java **语言**的语法与语义 | Java 源代码 |
| **JVMS** | Java **虚拟机**的指令集与运行时行为 | 字节码（`.class` 文件） |

举例：`int` 类型在 JLS 里定义为 32 位有符号整数；在 JVMS 里则对应 `iload`、`iadd` 等字节码指令。

---

## @interface 与 JLS

在 JLS 第 9.6 节，注解类型的声明语法定义如下：

```text
AnnotationTypeDeclaration:
    {InterfaceModifier} @ interface Identifier AnnotationTypeBody
```

`@interface` 并不是 JLS 关键字列表（第 3.9 节）里的单独条目——`@` 是注解符号，`interface` 是普通关键字，两者在注解类型声明中组合使用。这也是为什么 `@ interface`（中间加空格）在语法上也是合法的。

---

## 延伸阅读

- [Java 注解](./annotation.md)
