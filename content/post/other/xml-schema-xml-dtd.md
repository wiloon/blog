---
title: XML Schema, XML DTD
author: lcf
date: 2012-09-25T02:48:35+00:00
url: /?p=4242
categories:
  - Java

tags:
  - reprint
---
## XML Schema, XML DTD
<http://www.ibm.com/developerworks/cn/xml/x-sd/index.html>

引言

XML DTD(XML的文档类型定义)是近几年来XML技术领域所使用的最广泛的一种模式。但是，由于XML DTD并不能完全满足XML自动化处理的要求，例如不能很好实现应用程序不同模块间的相互协调，缺乏对文档结构、属性、数据类型等约束的足够描述等等，所以W3C于2001年5月正式推荐XML Schema为XML 的标准模式。显然，W3C希望以XML Schema来作为XML模式描述语言的主流，并逐渐代替XML DTD。那么XML Schema与XML DTD相比到底有哪些优势呢，XML DTD是否真的会在XML的模式描述领域中逐渐消失呢？

回页首

XML模式与XML格式

XML模式是指用来描述XML结构、约束等因素的语言，例如XML Schema、XML DTD、XDR，SOX等等。XML格式则是XML文档本身所具有的格式。本文以XML Schema来代表W3C所推荐的XML Schema模式标准，而以"XML模式"来代表所有的XML模式描述语言。

从模式的描述语言来说，XML Schema和XML DTD都属于语法模式。与概念模式不同，语法模式在对同一事物描述时，可以采用不同的语法，例如在对关系模式描述时，无论是使用XML Schema还是XML DTD，都既可以用元素也可以用属性来描述关系模式的列。

模式必须以某种格式来表示，XML Schema的格式与XML DTD的格式有着非常明显的区别，XML Schema事实上也是XML的一种应用，也就是说XML Schema的格式与XML的格式是完全相同的，而作为SGML DTD的一个子集，XML DTD具有着与XML格式完全不同的格式。这种区别会给XML Schema的使用带来许多好处: 

XML用户在使用XML Schema的时候，不需要为了理解XML Schema而重新学习，节省了时间；

由于XML Schema本身也是一种XML，所以许多的XML编辑工具、API 开发包、XML语法分析器可以直接的应用到XML Schema，而不需要修改。

作为XML的一个应用，XML Schema理所当然的继承了XML的自描述性和可扩展性，这使得XML Schema 更具有可读性和灵活性。

由于格式完全与XML一样，XML Schema除了可以像XML一样处理外，也可以同它所描述的XML文档以同样的方式存储在一起，方便管理。

XML Schema与XML格式的一致性，使得以XML为数据交换的应用系统之间，也可以方便的进行模式交换。

XML有非常高的合法性要求，XML DTD对XML的描述，往往也被用作验证XML合法性的一个基础，但是XML DTD本身的合法性却缺少较好的验证机制，必需独立处理。XML Schema则不同，它与XML有着同样的合法性验证机制。