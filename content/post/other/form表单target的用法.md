---
title: form表单target的用法
author: "-"
date: 2013-11-06T04:31:07+00:00
url: /?p=5901
categories:
  - Web

tags:
  - reprint
---
## form表单target的用法
偶然有一机会发现form表单的target的用法,可以实现当前页表单提交而不进行跳转刷新。代码如下,首页在页面里准备一form表单和一iframe


  
    
      Java代码  <img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" />
  
  
  
    
      <form action="提交的action" method="post" target="theID">
    
    
      .....................
    
    
      </form>
    
    
      
    
  

提交到action后,action返回一串javascript语句


  
    
      Java代码  <img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" />
  
  
  
    
      String script = "<script>alert('ok!');</script>";
    
    
              response.getOutputStream().write(script.getBytes("utf-8"));
    
  

alert('ok')将在当前页执行。原理是form提交后的结果在target指定的iframe里执行
  
而iframe将其隐藏。这样提交后的效果就和无刷新的效果一样。

<http://vsp.iteye.com/blog/1570466>