---
title: 解决JQuery.trim()函数ie下报错的问题
author: "-"
date: 2013-08-10T10:34:07+00:00
url: /?p=5769
categories:
  - Web

tags:
  - reprint
---
## 解决JQuery.trim()函数ie下报错的问题
经常碰到JQuery里的trim()函数在firefox支持,但是在IE里不支持
  
其主要原因是写法不对,下面是错误的写法


  
    
      Java代码  <img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" />
  
  
  
    
      var content = $('#content').val();
    
    
      if(content.trim() == ")
    
    
         alert('空');
    
  

上面的写法在firefox下不会报错,但在ie下确会报错
  
正确的写法应该为


  
    
      Java代码  <img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" />
  
  
  
    
      var content = $('#content').val();
    
    
      if($.trim(content) == ")
    
    
        alert('空');
    
  

或者为:


  
    
      Java代码  <img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" />
  
  
  
    
      var content = $('#content').val();
    
    
      if(jQuery.trim(content) == ")
    
    
       alert('空');
    
  
  
    http://vsp.iteye.com/blog/1262441
  
