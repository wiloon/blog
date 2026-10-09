---
title: "CSS 垂直居中"
author: "-"
date: 2012-02-25T04:01:39+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: css-vertical-center
categories:
  - Web
tags:
  - CSS
  - remix
  - AI-assisted
aliases:
  - /css　垂直居中/
---
## css垂直居中
**单行内容的居中**
  
只考虑单行是最简单的，无论是否给容器固定高度，只要给容器设置 line-height 和 height，并使两值相等，再加上 over-flow: hidden 就可以了

[css]

.middle-demo-1{
  
height: 4em;
  
line-height: 4em;
  
overflow: hidden;
  
}

[/css]

优点: 
  
1. 同时支持块级和内联极元素
  
2. 支持所有浏览器
  
缺点: 
  
1. 只能显示一行
  
2. IE 中不支持 `<img>` 等的居中
  
要注意的是: 
  
1. 使用相对高度定义你的 height 和 line-height
  
2. 不想毁了你的布局的话，overflow: hidden 一定要加上。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `css-vertical-center.md`；title 改为「CSS 垂直居中」；url 改为 `css-vertical-center`；旧 url 加入 aliases | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
