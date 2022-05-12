---
title: SIteMesh
author: "-"
date: 2012-12-07T08:08:32+00:00
url: /?p=4840
categories:
  - Java
  - Web
tags:$
  - reprint
---
## SIteMesh

转自:<http://javauu.com/thread-27-1-1.html>

## 一、SIteMesh介绍

  一、SiteMesh简介
 SiteMesh是由一个基于Web页面布局、装饰以及与现存Web应用整合的框架。它能帮助我们在由大量页面构成的项目中创建一致的页面布局和外观，如一致的导航条，一致的banner，一致的版权，等等。 它不仅仅能处理动态的内容，如jsp，php，asp等产生的内容，它也能处理静态的内容，如htm的内容，使得它的内容也符合你的页面结构的要求。甚至于它能将HTML文件象include那样将该文件作为一个面板的形式嵌入到别的文件中去。所有的这些，都是GOF的Decorator模式的最生动的实现。尽管它是由java语言来实现的，但它能与其他Web应用很好地集成。与传统区别如下图:
 <img src="http://javauu.com/attachments/forumid_19/20080909_6b24a2aa462d3f86bf8cfCBgkJs8uFPE.jpg" alt="" /> <img src="http://javauu.com/attachments/forumid_19/20080909_ba26d2494b9fc0dab76a1BCCKU7KiFLk.jpg" alt="" />
 SIteMesh官方地址: <http://www.opensymphony.com/sitemesh/index.html>
 SIteMesh官方下载: <http://www.opensymphony.com/sitemesh/download.html>
 SIteMesh 2.3下载: <http://www.javauu.com/downloads/resource/sitemesh-2.3.zip>
  
    二、SiteMesh原理
  
  
    
      SiteMesh框架是OpenSymphony团队开发的一个非常优秀的页面装饰器框架，它通过对用户请求进行过滤，并对服务器向客户端响应也进行过滤，然后给原始页面加入一定的装饰(header,footer等)，然后把结果返回给客户端。通过SiteMesh的页面装饰，可以提供更好的代码复用，所有的页面装饰效果耦合在目标页面中，无需再使用include指令来包含装饰效果，目标页与装饰页完全分离，如果所有页面使用相同的装饰器，可以是整个Web应用具有统一的风格。
