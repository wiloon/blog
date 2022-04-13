---
title: javascript Location
author: "-"
date: 2012-10-31T07:51:02+00:00
url: /?p=4595
categories:
  - Development
tags:
  - JavaScript

---
## javascript Location

location.href 返回整个当前url,若对其赋值:
  
location.href="http://www.highya.com" 则跳转其url
  
location.host 返回域名和端口号，如: www.highya.com:80
  
lcation.hostname 返回域名
  
location.port 返回端口
  
location.pathname 返回域名后第一个斜框后的字符串
  
location.hash 跳到本页的某个锚
  
location.search 取url?后的部分

location对象:

location提供了关于当前打开窗口或者特定框架的url信息。一个多框架的窗口对象在location属性显示的是父窗口的URL，每个框架也有一个与之相伴的location对象。

hash属性: hash标注是一个url很好的习惯用法，它指定浏览器到一个位于文档中的anchor位置，相当于一个书签儿。

host属性: 描述渔歌url的主机名和端口，只有端口号是url的一个明确部分时，值中才包括端口号。

hostname属性: 一个典型的url的主机名是网络上服务器的名字，该网络存储有你的浏览器上可以查看的文档。对大多数Web站点来说，服务器名不仅包括域名，也包括www前缀，如果端口号是在url中特有的话，主机名并不包括，而是包括在host属性中。

href属性: 该属性提供一个指定窗口对象的整个url的字符串。

pathname属性: url的路径名部分由与服务器root (根) 卷相关的目录结构组成。根不是目录的一部分，如果url的路径是通向根目录中的一个文件，那么location.pathname属性就是 (/) 。

port属性: 端口号很少用到。当指向一个没有赋给域名的的站点的url中，可以用location.port属性获取该值，如果从一个url获取值并想用那个组建创建一个url，一定要包括服务器IP地址和段口号，IP地址和段口号之间用 (:) 分界。

protocol属性: 包括协议名，且后面紧跟着 (:) 分节目。

assign方法: assign("url")通过这个方法可以实现把一个新的url赋给location对象。当然你也可以采用直接赋值的方法来实现，或者location.href来导航到一个新的网页。采用assign的方法会使代码易维护。

reload方法: 这个方法可以把浏览器可能保存在内存中的元素 (在一段记录中) 的文档设置全部忽略掉，重新打开该文档，和浏览器上的刷新可不一样。它的效果好像是你选择了file菜单open file一样。当然如果你不想这样，不想这么做，有一个和这个方法比较类似的方法，就是history.go () 方法。

replace方法: 当用户从当前网页，跳转到别的网页，有时候是不是想让不能用后退按钮(Back)看到前一个网页，告诉你一个方法，就是采用location.replace("url")就可以实现这个功能。
