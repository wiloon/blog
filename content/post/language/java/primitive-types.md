---
title: Java 基本数据类型（Primitive Types）
author: "-"
date: 2012-09-19T08:44:40+00:00
lastmod: 2026-06-19T17:02:22+08:00
url: primitive-types
categories:
  - Java
tags:
  - java
  - primitive
  - remix
  - AI-assisted
aliases:
  - /java/primitive
---

Java 提供 8 种基本数据类型（primitive type）：4 种整数型、2 种浮点型、1 种字符型、1 种布尔型。它们不是对象，直接存数值；与之相对的是引用类型（如 `String`、自定义类），详见 [Java 引用类型与基本类型](./reference-vs-primitive-types.md)。

## 类型一览

| 类型 | 字节 | 位数 | 取值范围 / 说明 | 默认值 |
| --- | --- | --- | --- | --- |
| `byte` | 1 | 8 | -128 ~ 127 | `0` |
| `short` | 2 | 16 | -32,768 ~ 32,767 | `0` |
| `int` | 4 | 32 | -2,147,483,648 ~ 2,147,483,647 | `0` |
| `long` | 8 | 64 | -2^63 ~ 2^63 - 1 | `0L` |
| `float` | 4 | 32 | 约 ±3.4E38（7 位有效数字） | `0.0f` |
| `double` | 8 | 64 | 约 ±1.7E308（15 位有效数字） | `0.0d` |
| `char` | 2 | 16 | `\u0000` ~ `\uffff`（0 ~ 65,535） | `\u0000` |
| `boolean` | — | — | `true` / `false`（JVM 规范未规定精确字节数） | `false` |

未显式声明时，整型字面量默认为 `int`，浮点字面量默认为 `double`。

## 整数类型

### byte

8 位有符号整数，采用二进制补码表示。

- 8 位中最高位为符号位
- `0000 0001` 表示 1，`1000 0000` 表示 -1
- 正数最大 `0111 1111`（127），负数最小 `1111 1111`（-128）

```java
byte b = 127;
```

### short

16 位有符号整数，补码表示。相比 `int` 可节省空间（占 `int` 的一半）。

```java
short s = 1000;
short r = -20000;
```

### int

32 位有符号整数，补码表示。一般整型字面量和变量默认类型为 `int`。

```java
int a = 100_000;
int b = -200_000;
```

### long

64 位有符号整数，用于较大整数值。字面量后缀 `L` 或 `l`（推荐大写，避免与数字 1 混淆）。

```java
long a = 100_000L;
long b = -9_223_372_036_854_775_808L;
```

## 浮点类型

`float` 和 `double` 均符合 IEEE 754 标准，**不能精确表示货币等需要高精度的十进制小数**。

### float

32 位单精度浮点数。声明时必须加 `f` 后缀，或显式强转，否则字面量会被当作 `double`：

```java
float f1 = 234.5f;
float pi = (float) 3.14;
```

### double

64 位双精度浮点数，浮点字面量的默认类型。

机内以指数形式存储，分解为数符、尾数、指数符、指数四部分。`float` 与 `double` 的尾数、指数占位不同，因此数值范围和精度不同；在两种类型间转换时，即使不溢出，也可能损失精度。

```java
double d1 = 123.4;
```

## char

16 位 Unicode 字符，可存储 BMP（基本多语言平面）内的单个字符。

```java
char letter = 'A';
char zero = '\u0000';
```

Java 内部字符以 UTF-16 编码。单个 `char` 只能表示 U+0000 ~ U+FFFF（基本平面）；扩展平面（U+10000 ~ U+10FFFF）的字符由一对 `char`（surrogate pair）表示。`String` 是 `char[]` 的封装，与 `char` 一样涉及字符编码问题。

## boolean

表示真/假，只有两个取值：`true` 和 `false`。通常用作条件标志，而非算术运算。

```java
boolean flag = true;
```

## 与 String 的区别

`String` **不是**基本数据类型，而是 `final` 引用类型。基本类型列表为：`byte`、`short`、`int`、`long`、`float`、`double`、`char`、`boolean`。

基本类型与包装类的装箱拆箱见 [自动装箱拆箱](./java-wrapper.md)。

## 字符编码补充

Java 遵循 Unicode 标准，内部 `char` 以 UTF-16 编码。`String.getBytes()` 按指定编码返回字节序列；中文系统在 Linux/macOS 上常用 UTF-8（中文通常 3 字节），Windows 上常用 GBK/GB18030（中文通常 2 字节）。

## 参考来源

- [Java 基本数据类型 - CSDN](https://blog.csdn.net/yulei_qq/article/details/8992664)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-19 | 文件重命名为 `primitive-types.md`；整理结构与表格；修正 `int` 最大值笔误；`url` 改为 `primitive-types` 并保留 `/java/primitive` 别名 | 文件名含中文不符合规范；原文排版混乱 |
