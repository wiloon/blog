---
title: 解决JQuery.trim()函数ie下报错的问题
author: wiloon
type: post
date: 2013-08-10T10:34:07+00:00
url: /?p=5769
categories:
  - Web

---
经常碰到JQuery里的trim()函数在firefox支持，但是在IE里不支持
  
其主要原因是写法不对，下面是错误的写法

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" /></a>
    
  
  
  <ol start="1">
    <li>
      var content = $('#content').val();
    </li>
    <li>
      if(content.trim() == ")
    </li>
    <li>
         alert('空');
    </li>
  </ol>


上面的写法在firefox下不会报错，但在ie下确会报错
  
正确的写法应该为

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" /></a>
    
  
  
  <ol start="1">
    <li>
      var content = $('#content').val();
    </li>
    <li>
      if($.trim(content) == ")
    </li>
    <li>
        alert('空');
    </li>
  </ol>


或者为:

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" /></a>
    
  
  
  <ol start="1">
    <li>
      var content = $('#content').val();
    </li>
    <li>
      if(jQuery.trim(content) == ")
    </li>
    <li>
       alert('空');
    </li>
  </ol>
  
  
    <a href="http://vsp.iteye.com/blog/1262441">http://vsp.iteye.com/blog/1262441</a>
  
