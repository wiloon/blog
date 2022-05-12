---
title: robots.txt
author: "-"
date: 2011-12-11T03:36:26+00:00
url: /?p=1841
categories:
  - Web
tags:$
  - reprint
---
## robots.txt
**robots.txt** (统一小写) 是一种存放于网站根目录下的ASCII编码的文本文件，它通常告诉网络搜索引擎的漫游器 (又称网络蜘蛛) ，此网站中的哪些内容是不能被搜索引擎的漫游器获取的，哪些是可以被 (漫游器) 获取的。 因为一些系统中的URL是大小写敏感的，所以robots.txt的文件名应统一为小写。robots.txt应放置于网站的根目录下。如果想单独定义搜索引擎的漫游器访问子目录时的行为，那么可以将自定的设置合并到根目录下的robots.txt，或者使用robots元数据。

Robots.txt协议并不是一个规范，而只是约定俗成的，所以并不能保证网站的隐私。注意Robots.txt是用字符串比较来确定是否获取URL，所以目录末尾有和没有斜杠"/"这两种表示是不同的URL，也不能用"Disallow: *.gif"这样的通配符。

其他的影响搜索引擎的行为的方法包括使用robots元数据: 

<meta name="robots" content="noindex,nofollow" />

这个协议也不是一个规范，而只是约定俗成的，通常搜索引擎会识别这个元数据，不索引这个页面，以及这个页面的链出页面。