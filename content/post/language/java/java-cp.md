---
title: java -cp / -classpath
author: "-"
date: 2012-04-17T13:24:22+00:00
lastmod: 2026-06-28T07:12:53+08:00
url: java-cp
categories:
  - language
tags:
  - java
  - jvm
  - classloader
  - remix
  - AI-assisted
aliases:
  - /p2951/
---

## 作用

`-cp` 与 `-classpath` 等价，用来指定运行时查找类和 JAR 的 **classpath**（类路径）。classpath 的概念、与依赖管理工具和 module path 的关系，见 [Java Classpath 与 Module Path](./classpath.md)。

## 语法

```bash
java -cp <类路径> <主类全限定名> [应用参数...]
```

- 条目之间的分隔符：**Linux/macOS 用冒号 `:`**，**Windows 用分号 `;`**
- 条目可以是**目录**或 **JAR/ZIP 文件**
- `.` 代表当前目录
- 支持通配符 `lib/*`（匹配目录下所有 JAR，**不递归**子目录），但不能写 `lib/*.jar`
- 一旦显式指定 `-cp`，默认的当前目录 `.` 不再自动加入，需要时要显式写上

## 示例

```bash
# 当前目录 + 一个 jar（Linux/macOS）
java -cp .:lib/hsqldb.jar org.hsqldb.Server -database mydb

# Windows 用分号分隔
java -cp .;lib\hsqldb.jar org.hsqldb.Server -database mydb

# 用通配符引入一个目录下所有 jar
java -cp "app.jar:lib/*" com.example.Main
```

> 现在大多用 Maven/Gradle 或 IDE 自动拼装 classpath，手写 `-cp` 多见于命令行手动编译运行、排查问题等场景。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-28 | 重写为结构化说明，修正原文缺失的路径分隔符示例；链到新建 classpath.md；分类 Java→language，删除 reprint | 原文为转载且示例残缺、信息过时 |
