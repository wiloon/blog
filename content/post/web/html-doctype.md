---
title: html DOCTYPE
author: "-"
date: 2012-12-08T12:36:54+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: html-doctype
categories:
  - Web
tags:
  - HTML
  - remix
  - AI-assisted
aliases:
  - /p4868/
---
## html DOCTYPE
`<!DOCTYPE>` 声明必须是 HTML 文档的第一行，位于 `<html>` 标签之前。

`<!DOCTYPE>` 声明不是 HTML 标签；它是指示 web 浏览器关于页面使用哪个 HTML 版本进行编写的指令。

在 HTML 4.01 中，`<!DOCTYPE>` 声明引用 DTD，因为 HTML 4.01 基于 SGML。DTD 规定了标记语言的规则，这样浏览器才能正确地呈现内容。

HTML5 不基于 SGML，所以不需要引用 DTD。

添加 `<!DOCTYPE>` 声明，这样浏览器才能获知文档类型。

HTML Transitional DTD

Transitional DTD 可包含 W3C 所期望移入样式表的呈现属性和元素。如果您的读者使用了不支持层叠样式表 (CSS) 的浏览器以至于您不得不使用 HTML 的呈现特性时，请使用此类型:

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
```

html5 只有一种 DOCTYPE 声明

```html
<!DOCTYPE html>
```

`<!DOCTYPE>` 声明没有结束标签。

`<!DOCTYPE>` 声明对大小写不敏感。

http://www.w3school.com.cn/tags/tag_doctype.asp
  

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码 | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
