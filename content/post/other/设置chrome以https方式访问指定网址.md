---
title: 设置Chrome以https方式访问指定网址
author: "-"
date: 2012-08-30T04:37:57+00:00
url: /?p=3973
categories:
  - chrome
tags:
  - reprint
---
## 设置Chrome以https方式访问指定网址



  1、打开Chrome，在地址栏键入 chrome://net-internals 回车


  
    2、在HSTS选项卡下的Domain中输入你想要实现这个强制跳转的域名，如 google.com.hk
  
  
    3、勾选上Include subdomains，这样可以确保指定网址的所有二级域名都被重定向到https。
  
  
    4、点击Add按钮，完成。
  
