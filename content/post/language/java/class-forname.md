---
title: Class.forName
author: "-"
date: 2013-12-21T13:11:52+00:00
lastmod: 2026-06-21T11:46:40+08:00
url: class-forname
categories:
  - language
tags:
  - java
  - jvm
  - remix
  - AI-assisted
aliases:
  - /p6067/
---

`Class.forName` 是获取 [`java.lang.Class`](./lang-class.md) 对象的一种方式：用**字符串形式的完全限定类名**在运行时查找并加载类。类名来自配置、用户输入或 JDBC 驱动名等场景时，通常走这条路径。

## API 形式

```java
// 等价于 forName(name, true, 当前 ClassLoader)
Class<?> clazz = Class.forName("com.example.Foo");

// 显式控制是否初始化、使用哪个 ClassLoader
Class<?> clazz = Class.forName("com.example.Foo", false, classLoader);
```

第二个参数 `initialize`：

- `true`：加载后执行类初始化（静态代码块、静态字段赋值等）
- `false`：只加载并链接，暂不初始化

单参数 `Class.forName(name)` 相当于 `initialize = true`。

## 与 `.class`、`getClass()` 的区别

| 方式 | 类名来源 | 默认是否初始化 |
| --- | --- | --- |
| `Foo.class` | 编译期写死 | 否 |
| `obj.getClass()` | 已有实例 | 否 |
| `Class.forName("Foo")` | 运行期字符串 | **是** |

`Class` 对象本身的含义、唯一性等见专文 [java.lang.Class](./lang-class.md)。

## 典型用途

### JDBC 驱动加载（历史写法）

早期 JDBC 常用 `Class.forName` 触发驱动类静态块，向 `DriverManager` 注册：

```java
Class.forName("com.mysql.cj.jdbc.Driver");
Connection conn = DriverManager.getConnection(url, user, password);
```

驱动类静态块执行即可完成注册，一般**不必**再 `newInstance()`。现代 JDBC 4+ 驱动多通过 SPI 自动加载，此写法已较少见，但有助于理解 `forName` 与类初始化的关系。

### 按配置名实例化

```java
String className = config.get("handler");  // e.g. com.example.ExportHandler
Class<?> clazz = Class.forName(className);
Object handler = clazz.getDeclaredConstructor().newInstance();
```

类名来自外部输入时，应校验白名单，避免任意类加载风险。

## 类加载细节

`forName` 会走类加载流程（查找 `.class`、`defineClass` 等），详见 [java classloader](./classloader.md)。加载成功后返回该类型唯一的 `Class` 实例。

## 参考

- [java.lang.Class](./lang-class.md)
- [Class.forName（Oracle API）](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Class.html#forName(java.lang.String))

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-21 | 删去 Class 概念与 JDBC 长篇转载；保留 `forName` 专述并链至 `java-lang-class.md` | 与 Class 专文去重 |
