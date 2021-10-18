---
title: jquery outerhtml
author: "-"
type: post
date: 2013-11-08T04:54:37+00:00
url: /?p=5906
categories:
  - Uncategorized

---
# jquery outerhtml
# 

prop('outerHTML')


  
    1、今天获取元素的html,而firefox却不支持如下代码
  
  
    var elemstr = $("#" + name)[0].outerHTML;
  
  
    2、看到网上很多文章讨论Firefox如何使用outerHTML，给出的解决方案都颇为复杂。
  
  
    如果使用jQuery1.3,则问题变得简单多了！
  
  
    使用如下代码，IE和FF均支持！
  
  
    var elemstr = $("#" + name).parent().html();
  
  
    希望本文能对你有所帮助！
  
  
    http://www.cnblogs.com/cxd4321/archive/2011/11/01/2231063.html
  
