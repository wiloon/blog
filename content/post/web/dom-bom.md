---
title: DOM, BOM
author: "-"
date: 2012-10-08T09:13:39+00:00
url: /?p=4388
categories:
  - Web
tags:
  - reprint
---
## DOM, BOM
### BOM 浏览器对象模型
提供了独立于内容而与浏览器窗口进行交互的对象。描述了与浏览器进行交互的方法和接口，可以对浏览器窗口进行访问和操作，譬如可以弹出新的窗口，改变状态栏中的文本，对Cookie的支持，IE还扩展了BOM，加入了ActiveXObject类，可以通过js脚本实例化ActiveX对象等等) 

#### 文档结构图
BOM由以一系列相关的对象组成。下图展示了基本的BOM体系结构。

![][1]

图1 BOM体系结构

#### BOM中的对象
Window对象: 

是整个BOM的核心，所有对象和集合都以某种方式回接到window对象。Window对象表示整个浏览器窗口，但不必表示其中包含的内容。

Document对象: 

实际上是window对象的属性。这个对象的独特之处是唯一一个既属于BOM又属于DOM的对象。从BOM角度看，document对象由一系列集合构成，这些集合可以访问文档的各个部分。

Location对象: 

它是window对象和document对象的属性。Location对象表示载入窗口的URL，此外它还可以解析URI.

Navigator对象: 

Navigator包含大量Web浏览器相关的信息。各种浏览器支持该对象的属性和方法不尽相同。

Screen对象: 

通过其可以获取用户屏幕相关的信息

###  DOM 文档对象模型
DOM是针对XML的基于树的API。描述了处理网页内容的方法和接口，是HTML和XML的API，DOM把整个页面规划成由节点层级构成的文档。

DOM本身是与语言无关的API，它并不与Java，JavaScript或其他语言绑定。

#### 特定语言的DOM
针对XHTML和HTML的DOM。这个DOM定义了一个HTMLDocument和HTMLElement做为这种实现的基础。

其他的包括SVG的DOM

#### 对于DOM的支持
各种浏览器对于DOM的支持不一样。

Mozila支持最好，几乎所有的DOM Level 2以及部分DOM Level 3。在

Opera和Safrai支持所有的DOM Level1和大部分DOM Level2。

IE，支持大部分的DOM Level 1。

#### DOM的各种Level
DOM Level 1 包括DOM Core和DOM HTML。前者提供了基于XML的文档结构图。后者添加了一些HTML专用的对象和方法，从而扩展了DOM Core.

DOM Level 2 引入几个新模块: DOM视图，事件，样式，遍历和范围

DOM Level 3 引入了以统一的方式载入和保存文档的方法。DOM Core被扩展支持所有的XML1.0的特性

<http://titan.iteye.com/blog/60389>

 [1]: http://titan.iteye.com/upload/picture/pic/2538/c28d3025-2f39-403e-8727-56595aefea3f.gif


### DOM 事件
    onblur="hanshu(this)"

    获得焦点:
      
    onfocus="hanshu(this)"
