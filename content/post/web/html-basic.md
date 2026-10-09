---
author: "-"
date: "2020-09-29 10:57:52" 
lastmod: 2026-10-09T21:22:13+08:00
url: html-basic
title: "HTML Basic"
categories:
  - Web
tags:
  - html
  - remix
  - AI-assisted
---
## html basic

### button

```xml
<button name="button0">button0</button>
```

## HTML Formatting Elements

- `<b>` - Bold text
- `<strong>` - Important text
- `<i>` - Italic text
- `<em>` - Emphasized text
- `<mark>` - Marked text
- `<small>` - Smaller text
- `<del>` - Deleted text
- `<ins>` - Inserted text
- `<sub>` - Subscript text
- `<sup>` - Superscript text
- `<br>` - line break

## node type

1. ELEMENT_NODE (元素节点)：值为 1
2. ATTRIBUTE_NODE (属性节点)：值为 2
3. TEXT_NODE (文本节点)：值为 3
4.	CDATA_SECTION_NODE (CDATA区段节点)：值为 4
5.	ENTITY_REFERENCE_NODE (实体引用节点)：值为 5 (在HTML中不常见)
6.	ENTITY_NODE (实体节点)：值为 6 (在HTML中不常见)
7.	PROCESSING_INSTRUCTION_NODE (处理指令节点)：值为 7
8.	COMMENT_NODE (注释节点)：值为 8
9.	DOCUMENT_NODE (文档节点)：值为 9
10.	DOCUMENT_TYPE_NODE (文档类型节点)：值为 10
11.	DOCUMENT_FRAGMENT_NODE (文档片段节点)：值为 11
12.	NOTATION_NODE (符号节点)：值为 12 (在HTML中不常见)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；title 改为「HTML Basic」；url 改为 `html-basic`；categories 改为 Web | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
