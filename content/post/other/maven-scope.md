---
title: maven Scope
author: "-"
date: 2015-08-24T01:47:50+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: maven-scope
categories:
  - Java
tags:
  - maven
  - remix
  - AI-assisted
aliases:
  - /p949/
  - /p6564/
  - /p6672/
  - /p8117/
  - /p8146/
  - /p8234/
---
## maven Scope
maven依赖关系中Scope的作用

Dependency Scope

在 POM 4 中，`<dependency>` 中还引入了 `<scope>`，它主要管理依赖的部署。目前 `<scope>` 可以使用 5 个值:

* compile，缺省值，适用于所有阶段，会随着项目一起发布。
  
* provided，类似compile，期望JDK、容器或使用者会提供这个依赖。如servlet.jar。
  
* runtime，只在运行时使用，如JDBC驱动，适用运行和测试阶段。
  
* test，只在测试时使用，用于编译和运行测试代码。不会随项目发布。
  
* system，类似provided，需要显式提供包含依赖的jar，Maven不会在Repository中查找它。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
