---
title: openJPA enhancement error
author: "-"
date: 2011-12-28T04:18:46+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: openjpa-enhancement-error
categories:
  - Java
tags:
  - openJPA
  - jpa
  - remix
  - AI-assisted
aliases:
  - /p2041/
  - /p6173/
---
## openJPA enhancement error

```text
<openjpa-2.1.1-r422266:1148538 nonfatal user error> org.apache.openjpa.persistence.ArgumentException: This configuration disallows runtime optimization, but the following listed types were not enhanced at build time or at class load time with a javaagent: "
com.wiloon.openjpa.entity.Animal".
```

add line :

```xml
<property name="openjpa.RuntimeUnenhancedClasses" value="supported" />
```

in persistence.xml

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
