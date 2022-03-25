---
title: IE下模拟css3中的box-shadow (阴影) 
author: "-"
date: 2013-03-04T09:25:20+00:00
url: /?p=5302
categories:
  - Web

tags:
  - reprint
---
## IE下模拟css3中的box-shadow (阴影)
css3中的box-shadow (阴影) 可以查看: http://www.css88.com/archives/2136或者http://www.css88.com/tool/css3Preview/Box-Shadow.html
  
在ie下模拟css3中的box-shadow (阴影) 可以使用ie的Shadow (阴影) 滤镜
  
基本语法: filter: progid:DXImageTransform.Microsoft.Shadow(color='颜色值', Direction=阴影角度 (数值) , Strength=阴影半径 (数值) );
  
注意: 该滤镜必须配合background属性一起使用,否则该滤镜失效。
  
IE下模拟css3中的box-shadow (阴影) 代码: 
  
.box-shadow{
  
02

filter: progid:DXImageTransform.Microsoft.Shadow(color='#969696', Direction=135, Strength=5);/_for ie6,7,8_/
  
04

background-color: #eee;
  
06

-moz-box-shadow:2px 2px 5px #969696;/_firefox_/
  
08

-webkit-box-shadow:2px 2px 5px #969696;/_webkit_/
  
10

box-shadow:2px 2px 5px #969696;/_opera或ie9_/
  
12

}
  
演示地址: http://www.css88.com/demo/box-shadow/