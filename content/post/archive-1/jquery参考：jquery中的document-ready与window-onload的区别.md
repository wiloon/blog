---
title: jQuery参考,jquery中的$(document).ready()与window.onload的区别
author: "-"
date: 2013-02-02T11:06:02+00:00
url: /?p=5104
categories:
  - Web

tags:
  - reprint
---
## jQuery参考,jquery中的$(document).ready()与window.onload的区别
# 

  
    
      window.onload = function(){ alert("welcome"); }
 这样的写法,是希望在页面加载完,自动执行定义好的 js代码 (function) 。
    
    
    
      对于这样的需求,大部分的程序员都会这样做。
    
    
    
      学习jQuery核心函数时,讲$(document).ready(function(){.... })这个函数是用来取代页面中的window.onload;
    
    
    
      但是,今天在启动一采用了$(document).ready(function(){   })的页面时 (页面上使用了一张>3M的图片) ,发现图片尚未完全加载时,
    
    
    
      function () 中的代码已经执行。
    
    
    
      在网上收缩两者的区别,发现已经有人有类似的经历而产生疑问 (取代window.onload,意味着等价？) 。
    
    
    
      这让我想起了jQuery API中的一句话
    
    
    
      "Allows you to bind a function to be executed when the DOM document has finished loading. "
    
    
    
      其,中文意思也就是说: 
    
    
    
      "允许你绑定一个在DOM文档载入完成后,执行的函数。"
    
    
    
      DOM文档加载和页面加载,却是不同,也就直接说明了两者是有很大区别。
    
    
    
      页面加载 起码包含DOM文档加载 (也就是你书写的代码机构等) 和页面内容加载两个方面。
    
    
    
      这样来说,两者的区别和实质也就很明显了。
  
