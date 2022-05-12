---
title: 自适应网页设计 (Responsive Web Design) 
author: "-"
date: 2012-11-24T11:08:55+00:00
url: /?p=4751
categories:
  - Web
tags:
  - reprint
---
## 自适应网页设计 (Responsive Web Design)
[http://www.ruanyifeng.com/blog/2012/05/responsive_web_design.html][1]

作者:  [阮一峰][2]

日期:  [2012年5月 1日][3]

随着3G的普及，越来越多的人使用手机上网。

移动设备正超过桌面设备，成为访问互联网的最常见终端。于是，网页设计师不得不面对一个难题: 如何才能在不同大小的设备上呈现同样的网页？

手机的屏幕比较小，宽度通常在600像素以下；PC的屏幕宽度，一般都在1000像素以上 (目前主流宽度是1366×768) ，有的还达到了2000像素。同样的内容，要在大小迥异的屏幕上，都呈现出满意的效果，并不是一件容易的事。

很多网站的解决方法，是为不同的设备提供不同的网页，比如专门提供一个mobile版本，或者iPhone / iPad版本。这样做固然保证了效果，但是比较麻烦，同时要维护好几个版本，而且如果一个网站有多个portal (入口) ，会大大增加架构设计的复杂度。

于是，很早就有人设想，能不能"一次设计，普遍适用"，让同一张网页自动适应不同大小的屏幕，根据屏幕宽度，自动调整布局 (layout) ？

**一、"自适应网页设计"的概念**

2010年，Ethan Marcotte提出了"自适应网页设计" (Responsive Web Design) 这个名词，指可以自动识别屏幕宽度、并做出相应调整的网页设计。


 [1]: http://www.ruanyifeng.com/blog/2012/05/responsive_web_design.html
 [2]: http://www.ruanyifeng.com/
 [3]: http://www.ruanyifeng.com/blog/2012/05/