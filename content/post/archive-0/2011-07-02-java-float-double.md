---
title: java float double
author: wiloon
type: post
date: 2011-07-02T12:59:21+00:00
url: /?p=261
bot_views:
  - 6
categories:
  - Java

---
float是32位的
  
double是64位的
  
都是浮点型但是表示范围是不一样的，转换的时候当然会提示精度损失，虽然这个数字在两个类型中都是不溢出的。

当你不声明时，默认为double的，要声明float该写为
   
float PI=3.14f；//这样才可以哦~
  
或者float PI = （float）3.14；