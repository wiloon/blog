---
title: js check platform
author: "-"
date: 2014-02-27T01:31:58+00:00
url: /?p=6293
categories:
  - JavaScript
tags:
  - JavaScript

---
## js check platform

```javascript

<script type="text/javascript">
   
<!-
   
//平台、设备和操作系统
   
var system ={
   
win : false,
   
mac : false,
   
xll : false
   
};
   
//检测平台
   
var p = navigator.platform;
   
alert(p);
   
system.win = p.indexOf("Win") == 0;
   
system.mac = p.indexOf("Mac") == 0;
   
system.x11 = (p == "X11") || (p.indexOf("Linux") == 0);
   
//跳转语句
   
if(system.win||system.mac||system.xll){//转向后台登陆页面
   
window.location.href="login.jsp";
   
}else{
   
window.location.href="wapLojin.jsp";
   
}
   
->
  
</script>

```

```
  
var isMobile = {
      
Android: function() {
          
return navigator.userAgent.match(/Android/i) ? true : false;
      
},
      
BlackBerry: function() {
          
return navigator.userAgent.match(/BlackBerry/i) ? true : false;
      
},
      
iOS: function() {
          
return navigator.userAgent.match(/iPhone|iPad|iPod/i) ? true : false;
      
},
      
Windows: function() {
          
return navigator.userAgent.match(/IEMobile/i) ? true : false;
      
},
      
any: function() {
          
return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Windows());
      
}
  
};
  
```

http://blog.csdn.net/yakson/article/details/9390863

http://stackoverflow.com/questions/12606245/detect-if-browser-is-running-on-an-android-or-ios-device