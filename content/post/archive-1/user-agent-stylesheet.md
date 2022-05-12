---
title: User Agent Stylesheet
author: "-"
date: 2013-02-28T02:10:22+00:00
url: /?p=5282
categories:
  - Web
tags:
  - reprint
---
## User Agent Stylesheet
大家通常看到一个没有带任何CSS样式文件的HTML却带有不错的样式，这是由于在W3C的HTML标准里，一些HTML标签自带一些CSS样式。

不同的浏览器把实现这些HTML自带样式的模块称作User Agent Stylesheet。
  
不同的浏览器实现的User Agent Stylesheet不一，但大部分都能遵循W3C的标准。
  
个人认为chrome实现的User Agent Stylesheet是最符合人们阅读习惯，例如p前后都有1em的外边距等。

在chrome里的User Agent Stylesheet如下图所示。
  
从上图中还可以看出浏览器的User Agent Stylesheet的优先级是很低的，经常被其他样式覆盖，这也是设置了CSS样式文件后能够起作用的原因。

从CSS的英文全称 Cascading Style Sheet，中文译作"层叠样式表单"， 其中cascading取义为层叠，即不同层级的样式表单叠加覆盖的意思。

其实W3C的CSS标准中有一套完整的CSS样式的优先级规则，高优先级的样式覆盖低优先级，后面将逐步剖析这些优先级的规则，讲解怎样能做出高效能的CSS样式表。