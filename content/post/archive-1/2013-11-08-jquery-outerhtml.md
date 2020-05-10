---
title: jquery outerhtml
author: wiloon
type: post
date: 2013-11-08T04:54:37+00:00
url: /?p=5906
categories:
  - Uncategorized

---
# 

prop(&#8216;outerHTML&#8217;)

<div id="cnblogs_post_body">
  <p>
    1、今天获取元素的html,而firefox却不支持如下代码
  </p>
  
  <p>
    var elemstr = $(&#8220;#&#8221; + name)[0].outerHTML;
  </p>
  
  <p>
    2、看到网上很多文章讨论Firefox如何使用outerHTML，给出的解决方案都颇为复杂。
  </p>
  
  <p>
    如果使用jQuery1.3,则问题变得简单多了！
  </p>
  
  <p>
    使用如下代码，IE和FF均支持！
  </p>
  
  <p>
    var elemstr = $(&#8220;#&#8221; + name).parent().html();
  </p>
  
  <p>
    希望本文能对你有所帮助！
  </p>
  
  <p>
    <a href="http://www.cnblogs.com/cxd4321/archive/2011/11/01/2231063.html">http://www.cnblogs.com/cxd4321/archive/2011/11/01/2231063.html</a>
  </p>
</div>