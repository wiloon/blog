---
title: JavaScript window.onload
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=6854
categories:
  - Inbox
tags:
  - reprint
---
## JavaScript window.onload
avaScript的window.onload使用: 
  
window.onload方法，可以定义html中的onload方法例如: 
  
window.onload=function(){
  
var a = document.getElementById("loading");
  
a.parentNode.removeChild(a);
  
}
  
这样就可以通过js代码直接定义这个方法，而不需要象这样定义了<body onload="aaa()">

  
window.onload方法，可以定义html中的onload方法例如: 
  
window.onload=function(){
  
var a = document.getElementById("loading");
  
a.parentNode.removeChild(a);
  
}
  
这样就可以通过js代码直接定义这个方法，而不需要象这样定义了<body onload="aaa()">


如果<body>标签原来已经定义了onload方法，则可以通过下面的方法，再追加自己的方法: 

if(window.onload==null){
  
window.onload=function(){dvwait1.style.display = "none";}
  
}else{
  
eval("wtempfunction="+window.onload.toString());
  
window.onload=function(){wtempfunction();dvwait1.style.display = "none";}
  
}