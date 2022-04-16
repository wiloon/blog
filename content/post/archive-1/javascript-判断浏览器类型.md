---
title: javascript 判断浏览器类型
author: "-"
date: 2013-01-14T04:44:46+00:00
url: /?p=5008
categories:
  - JavaScript
tags:
  - reprint
---
## javascript 判断浏览器类型
```

var Sys = {};
   
var ua = navigator.userAgent.toLowerCase();
   
if (window.ActiveXObject)
   
Sys.ie = ua.match(/msie ([d.]+)/)[1]
   
else if (document.getBoxObjectFor)
   
Sys.firefox = ua.match(/firefox/([d.]+)/)[1]
   
else if (window.MessageEvent && !document.getBoxObjectFor)
   
Sys.chrome = ua.match(/chrome/([d.]+)/)[1]
   
else if (window.opera)
   
Sys.opera = ua.match(/opera.([d.]+)/)[1]
   
else if (window.openDatabase)
   
Sys.safari = ua.match(/version/([d.]+)/)[1];

//以下进行测试
   
if (Sys.ie) document.write('IE: ' + Sys.ie);
   
if (Sys.firefox) document.write('Firefox: ' + Sys.firefox);
   
if (Sys.chrome) document.write('Chrome: ' + Sys.chrome);
   
if (Sys.opera) document.write('Opera: ' + Sys.opera);
   
if (Sys.safari) document.write('Safari: ' + Sys.safari);

```