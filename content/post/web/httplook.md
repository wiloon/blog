---
title: httplook
author: "-"
date: 2012-01-08T05:09:32+00:00
url: /?p=2108
categories:
  - Network
tags:$
  - reprint
---
## httplook
HTTPLook 是一个 HTTP 的嗅探器，它能捕捉本机与其它任何主机的 HTTP 通讯 (不是 HTTPS 哦 ) ，然后显示详细的 HTTP 操作 (如 GET/POST) 、访问资源的 URL 、字节数大小等，这个软件简单易用，不用对 Internet Explorer 做任何其它设置 (有的软件通过在 IE 中设置代理来监控数据) ，也不需要其它任何软件的支持，是一款较为绿色的、轻量级的软件。


  
  
    HTTPLook 的应用场景: 
  
  
  
    1、程序开发及调试
  
  
  
    在 CGI、ASP/PHP/JSP、ASP.NET、Web Service 的开发中，经常要查看 GET 或 POST 的数据是否正确，用这个工具能很好地协助完成此工作。
  
  
  
    2、复杂页面分析
  
  
  
    上网有时会碰到的很复杂的页面，查看源码也不能了解它的工作原理，这一般是作者为了保护 Web 在页面而加上了一些保护机制 (如使用 Frame/IFrame、捕捉键盘或 Mouse 事件、使用 Script 来访问资源等) ，使用 HTTPLook 有助于对此页面进行分析，进而破解其保护机制。
  
  
  
    比较典型的一个例子就是 SharePoint Team Services 中使用了 WebBot ，查看源码根本不知道它调用了那些 ASP/Script/CSS 文件，但使用 HTTPLook 之后，一目了然，非常有效，可以据此来自定义原有页面风格，如色彩，字体等。
  
  
  
    3、获得被保护的 Web 资源
  
  
  
    在很多网站上，尤其是 Microsoft 的网站上，经常见到一些制做精美的 Flash ，但是由于 Flash 不是一个单一文件，而是在最先启动的 FLASH 中再调用其它 Flash 资源文件，由于无法获得这些文件的 URL ，所以下载到本地，但如果使用 HTTPLook ，通过对整个播放过程的监视，就可以完全侦测出所有在程序中访问的资源的地址，进而保存到本地，可以离线浏览。当然也可以保存其它资源，如图片等。
  
  
  
    4、学习 HTTP 协议
  
  
  
    可以详细地了解 HTTP 通讯的细节，如 GET/POST、User-Agent、Cookie、Proxy 设置及验证、HTTP 协议出错代码及意义等。
  
