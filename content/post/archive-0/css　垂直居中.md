---
title: css垂直居中
author: "-"
date: 2012-02-25T04:01:39+00:00
url: /?p=2395
categories:
  - Web
tags:
  - CSS

---
## css垂直居中
**单行内容的居中**
  
只考虑单行是最简单的，无论是否给容器固定高度，只要给容器设置 line-height 和 height，并使两值相等，再加上 over-flow: hidden 就可以了

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
  
2. IE中不支持<img>等的居中
  
要注意的是: 
  
1. 使用相对高度定义你的 height 和 line-height
  
2. 不想毁了你的布局的话，overflow: hidden 一定要加上。