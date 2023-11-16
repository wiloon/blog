---
title: '浏览器,F5 和 Ctrl+F5的区别'
author: "-"
date: 2013-05-09T00:53:53+00:00
url: /?p=5438
categories:
  - Web
tags:
  - reprint
---
## '浏览器,F5 和 Ctrl+F5的区别'
引:[http://morganchengmo.spaces.live.com/blog/cns!9950CE918939932E!2144.entry](http://morganchengmo.spaces.live.com/blog/cns!9950CE918939932E!2144.entry)

[http://www.cnblogs.com/cxd4321/archive/2009/03/11/1408425.html](http://www.cnblogs.com/cxd4321/archive/2009/03/11/1408425.html)

**Browser: F5 vs Ctrl+F5**

在浏览器里中,按F5键或者点击Toobar上的Refresh/Reload图标(简称F5),和做F5同时按住Ctrl键 (简称Ctrl+F5) ,效果是明显不一样的,通常Ctrl+F5明显要让网页Refresh慢一些,到底两者有什么区别呢？

在上一篇技术文章中,说到了Expires、Last-Modified/If-Modified-Since和ETag/If-None-Match这些HTTP Headers,F5/Ctrl+F5和这些有莫大关系。

假如我第一次访问过http://www.example.com,这个网页是个动态网页,每次访问都会去访问Server,但是它包含一个一个静态资源http://www.example.com/logo.gif,浏览器在显示这个网页之前需要发HTTP请求获取这个logo.gif文件,返回的HTTP response包含这样的Headers:

Expires: Thu 27 Nov 2008 07:00:00 GMT
  
Last-Modified: Fri 30 Nov 2007 00:00:00 GMT

那么浏览器就会cache住这个logo.gif文件,直到2008年11月27日7点整,或者直到用户有意清空cache。

下次我再通过bookmark或者通过在URI输入栏直接敲字的方法访问http://www.example.com的时候,浏览器一看本地有个logo.gif,而且它还没过期呢,就不会发HTTP request给server,而是直接把本地cache中的logo.gif显示了。

F5的作用和直接在URI输入栏中输入然后回车是不一样的,F5会让浏览器无论如何都发一个HTTP Request给Server,即使先前的Response中有Expires Header。所以,当我在当前http://www.example.com网页中按F5的时候,浏览器会发送一个HTTP Request给Server,但是包含这样的Headers:

If-Modified-Since: Fri 30 Nov 2007 00:00:00 GMT

实际上Server没有修改这个logo.gif文件,所以返回一个304 (Not Modified),这样的Response很小,所以round-trip耗时不多,网页很快就刷新了。

上面的例子中没有考虑ETag,如同在上一篇技术文章中所说,最好就不要用ETag,但是如果Response中包含ETag,F5引发的Http Request中也是会包含If-None-Match的。

那么Ctrl+F5呢？ Ctrl+F5要的是彻底的从Server拿一份新的资源过来,所以不光要发送HTTP request给Server,而且这个请求里面连If-Modified-Since/If-None-Match都没有,这样就逼着Server不能返回304,而是把整个资源原原本本地返回一份,这样,Ctrl+F5引发的传输时间变长了,自然网页Refresh的也慢一些。

实际上,为了保证拿到的是从Server上最新的,Ctrl+F5不只是去掉了If-Modified-Since/If-None-Match,还需要添加一些HTTP Headers。按照HTTP/1.1协议,Cache不光只是存在Browser终端,从Browser到Server之间的中间节点(比如Proxy)也可能扮演Cache的作用,为了防止获得的只是这些中间节点的Cache,需要告诉他们,别用自己的Cache敷衍我,往Upstream的节点要一个最新的copy吧。

在IE6中,Ctrl+F5会添加一个Header

Pragma: no-cache
  
在Firefox 2.0中,Ctrl+F5会添加两个
  
Pragma: no-cache
  
Cache-Control: max-age=0

作用就是让中间的Cache对这个请求失效,这样返回的绝对是新鲜的资源


## 浏览器中F5和CTRL F5的行为区别
浏览器中F5和CTRL F5的行为区别

作者: JeremyWei | 可以转载, 但必须以超链接形式标明文章原始出处和作者信息及版权声明
  
网址: http://weizhifeng.net/difference-between-f5-and-ctrl-f5.html
  
前言
  
在印象中，浏览器中的F5和刷新按钮是一样的效果，都是对当前页面进行刷新；Ctrl-F5的行为也是刷新页面，但是会清除浏览器缓存，这在前端调试时候会常用。二者真正的区别是什么呢？在stackoverflow上有人给出了很详细的解释，整理如下。

说明
  
在不同的浏览器中F5和CTRL-F5的行为是不一样的，但是他们的主要行为还是非常相似的，以下结果是在FF，IE，Opera和Chrome中进行过测试得出。

F5使用缓存，并且只有在资源内容发生变化的时候才会去更新资源。
  
当刷新一个页面的时候，浏览器会尝试使用各种类型的缓存，并且会发送If-Modified-Since头到服务器，如果服务器返回304 Not Modified，那么浏览器会使用本地的缓存；如果服务器返回200 OK和资源内容，那么浏览器会使用返回的资源内容，并把资源内容进行缓存，待下次使用。

CTRL-F5 强制更新页面资源的缓存。
  
MSIE会发送Cache-Control: no-cache头，Firefox和Chrome除了发送Cache-Control: no-cache头之外，还会发送Pragma: no-cache头。Opera比较另类，不发送任何和缓存相关的头。

以下表格很直观的表明了F5和CTRL-F5的行为，由于原文中测试的浏览器版本较低，所以进行了更新。

F5 and CTRL-F5
  
┌────────────┬───────────────────────────────────────────────┐
  
│ UPDATED │ Firefox 3.x 4.x │
  
│2011-04-24 │ ┌────────────────────────────────────────────┤
  
│ │ │ MSIE 7 8 │
  
│ │ │ ┌─────────────────────────────────────────┤
  
│ │ │ │ MSIE 9 │
  
│ │ │ │ ┌──────────────────────────────────────┤
  
│ │ │ │ │ Chrome 10 │
  
│ │ │ │ │ ┌───────────────────────────────────┤
  
│ │ │ │ │ │ Opera 11 │
  
│ │ │ │ │ │ ┌────────────────────────────────┤
  
│ │ │ │ │ │ │ I = "If─Modified─Since" │
  
├────────────┼──┼──┼──┼──┼──┤ P = "Pragma: No─cache" │
  
│ F5│IM│IM│I │IM│I │ C = "Cache─Control: no─cache" │
  
│ CTRL─F5│CP│C │C │CP│- │ M = "Cache─Control: max─age=0" │
  
│ Click Icon│IM│I │I │IM│I │ Click Icon= "a mouse click on │
  
│ │ │ │ │ │ │ refresh icon" │
  
└────────────┴──┴──┴──┴──┴──┴──-─────────────────────────────┘
  
HTTP协议说明
  
HTTP/1.1规范14.9.4中规定: 

End-to-end reload(即CTRL-F5强制刷新)会发送如下HTTP头: 
  
Cache-Control: no-cache
  
Pragma: no-cache

Specific end-to-end revalidation(即F5 刷新)会发送如下HTTP头: 
  
Cache-Control: max-age=0
  
If-Modified-Since: Fri, 15 Apr 2011 12:08:21 GMT

参考: 
  
http://stackoverflow.com/questions/385367/what-requests-do-browsers-f5-and-ctrl-f5-refreshes-generate

