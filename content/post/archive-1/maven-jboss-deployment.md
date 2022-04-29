---
title: XPath
author: "-"
date: 2014-04-24T06:56:39+00:00
url: XPath
categories:
  - xml
tags:
  - reprint
---
## XPath

Xpath表达式
XPath（全称：XML Path Language）即 XML 路径语言，它是一门在 XML 文档中查找信息的语言，最初被用来搜寻 XML 文档，同时它也适用于搜索 HTML 文档。因此，在爬虫过程中可以使用 XPath 来提取相应的数据。
提示：XML 是一种遵守 W3C 标椎的标记语言，类似于 HTML，但两者的设计目的是不同，XML 通常被用来传输和存储数据，而 HTML 常用来显示数据。

您可以将 Xpath 理解为在XML/HTML文档中检索、匹配元素节点的工具。

Xpath 使用路径表达式来选取XML/HTML文档中的节点或者节点集。Xpath 的功能十分强大，它除了提供了简洁的路径表达式外，还提供了100 多个内建函数，包括了处理字符串、数值、日期以及时间的函数。因此 Xpath 路径表达式几乎可以匹配所有的元素节点。

Xpath基本语法
1) 基本语法使用
Xpath 使用路径表达式在文档中选取节点，下表列出了常用的表达式规则：

Xpath路径表达式
表达式	描述
node_name	选取此节点的所有子节点。
/	绝对路径匹配，从根节点选取。
//	相对路径匹配，从所有节点中查找当前选择的节点，包括子节点和后代节点，其第一个 / 表示根节点。
.	选取当前节点。
..	选取当前节点的父节点。
@	选取属性值，通过属性值选取数据。常用元素属性有 @id 、@name、@type、@class、@tittle、@href。

<http://c.biancheng.net/python_spider/xpath.html>
