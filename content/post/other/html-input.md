---
title: html input
author: "-"
date: 2015-06-10T03:56:12+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: html-input
categories:
  - Web
tags:
  - html
  - remix
  - AI-assisted
aliases:
  - /p4740/
  - /p7785/
---
## html input
```xml
<input type="value0">
``` 

hidden 定义隐藏的输入字段。
  
Hidden 对象代表一个 HTML 表单中的某个隐藏输入域。

这种类型的输入元素实际上是隐藏的。这个不可见的表单元素的 value 属性保存了一个要提交给 Web 服务器的任意字符串。如果想要提交并非用户直接输入的数据的话,就是用这种类型的元素。

在 HTML 表单中 `<input type="hidden">` 标签每出现一次,一个 Hidden 对象就会被创建。

您可通过遍历表单的 elements[] 数组来访问某个隐藏输入域,或者通过使用document.getElementById()。

http://www.w3school.com.cn/jsref/dom_obj_hidden.asp

http://www.wiloon.com/?p=6529

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Web | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
