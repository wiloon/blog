---
title: form表单target的用法
author: wiloon
type: post
date: 2013-11-06T04:31:07+00:00
url: /?p=5901
categories:
  - Web

---
偶然有一机会发现form表单的target的用法，可以实现当前页表单提交而不进行跳转刷新。代码如下，首页在页面里准备一form表单和一iframe

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" /></a>
    
  
  
  <ol start="1">
    <li>
      <form action="提交的action" method="post" target="theID">
    </li>
    <li>
      &#8230;&#8230;&#8230;&#8230;&#8230;&#8230;&#8230;
    </li>
    <li>
      </form>
    </li>
    <li>
      <iframe name="theID" style="display: none;"></iframe>
    </li>
  </ol>


提交到action后，action返回一串javascript语句

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img alt="收藏代码" src="http://vsp.iteye.com/images/icon_star.png" /></a>
    
  
  
  <ol start="1">
    <li>
      String script = "<script>alert(&#8216;ok!&#8217;);</script>";
    </li>
    <li>
              response.getOutputStream().write(script.getBytes("utf-8"));
    </li>
  </ol>


alert(&#8216;ok&#8217;)将在当前页执行。原理是form提交后的结果在target指定的iframe里执行
  
而iframe将其隐藏。这样提交后的效果就和无刷新的效果一样。

<http://vsp.iteye.com/blog/1570466>