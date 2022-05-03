---
title: Js中的history.back()在FireFox和Chrome
author: "-"
date: 2013-07-15T11:11:59+00:00
url: /?p=5665
categories:
  - JavaScript
tags:
  - reprint
---
## Js中的history.back()在FireFox和Chrome
JavaScript中后退的写法: history.back()或者history.go(-1)。

这种写法在IE上即可实现我们想要的效果，但是在FireFox和Chrome就会变得很悲催了。

FireFox: 

只需要改成如下方式:  **返回**

**        **Chrome: 

Chrome比FireFox更难搞:  **返回**

本人分析: 对于Chrome来说，首先执行window.history.back()，执行完成之后再接着执行href="#"，所以无法返回。加上 return false之后将不再执行href="#"，便能正常返回。