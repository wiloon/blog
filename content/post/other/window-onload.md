---
title: JavaScript window.onload
author: "-"
date: 2020-01-01T00:00:00+08:00
lastmod: 2026-10-09T21:22:13+08:00
url: window-onload
categories:
  - JavaScript
tags:
  - javascript
  - remix
  - AI-assisted
aliases:
  - /p6854/
---
## JavaScript window.onload
JavaScript的window.onload使用:
  
window.onload方法，可以定义html中的onload方法例如: 
  
```javascript
window.onload=function(){
    var a = document.getElementById("loading");
    a.parentNode.removeChild(a);
}
```
  
这样就可以通过js代码直接定义这个方法，而不需要象这样定义了`<body onload="aaa()">`

window.onload方法，可以定义html中的onload方法例如: 
  
```javascript
window.onload=function(){
    var a = document.getElementById("loading");
    a.parentNode.removeChild(a);
}
```
  
这样就可以通过js代码直接定义这个方法，而不需要象这样定义了`<body onload="aaa()">`

如果`<body>`标签原来已经定义了onload方法，则可以通过下面的方法，再追加自己的方法: 

```javascript
if(window.onload==null){
    window.onload=function(){dvwait1.style.display = "none";}
}else{
    eval("wtempfunction="+window.onload.toString());
    window.onload=function(){wtempfunction();dvwait1.style.display = "none";}
}
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `window-onload.md`；url 改为 `window-onload`；旧 url 加入 aliases；categories 改为 JavaScript | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
