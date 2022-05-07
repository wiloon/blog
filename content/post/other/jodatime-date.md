---
title: jodatime date
author: "-"
date: 2012-09-16T11:01:30+00:00
url: /?p=4056
categories:
  - Inbox
tags:
  - reprint
---
## jodatime date
function currentTime(){
  
var d = new Date(),str = ";
  
str += d.getFullYear()+'年';
  
str  += d.getMonth() + 1+'月';
  
str  += d.getDate()+'日';
  
str += d.getHours()+'时';
  
str  += d.getMinutes()+'分';
  
str+= d.getSeconds()+'秒';
  
return str;
  
}