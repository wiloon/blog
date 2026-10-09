---
title: 关于 XML standalone 的解释
author: "-"
date: 2011-11-08T05:44:54+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: xml-standalone
categories:
  - CS
tags:
  - xml
  - remix
  - AI-assisted
aliases:
  - /关于-xml-standalone-的解释/
---
## 关于 XML standalone 的解释

  http://www.blogjava.net/javafuns/articles/257525.html

XML standalone 定义了外部定义的 DTD 文件的存在性. standalone element 有效值是 yes 和 no. 如下是一个例子:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE s1 PUBLIC "http://www.ibm.com/example.dtd" "example.dtd">
<s1>.........</s1>
```

值 no 表示这个 XML 文档不是独立的而是依赖于外部所定义的一个 DTD.  值 yes 表示这个 XML 文档是自包含的(self-contained).

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `xml-standalone.md`；url 改为 `xml-standalone`；旧 url 加入 aliases；categories 改为 CS | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
