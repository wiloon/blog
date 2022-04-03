---
title: JQuery 获得绝对,相对位置的坐标
author: "-"
date: 2015-03-03T15:17:56+00:00
url: /?p=7366
categories:
  - Uncategorized

tags:
  - reprint
---
## JQuery 获得绝对,相对位置的坐标

  http://www.jb51.net/article/22081.htm


  获取页面某一元素的绝对X,Y坐标,可以用offset()方法:  (body属性设置margin :0;padding:0;) 






  var X = $('#DivID').offset().top;
 var Y = $('#DivID').offset().left;
 获取相对(父元素)位置:
 var X = $('#DivID').position().top;
 var Y = $('#DivID').position().left;
