---
title: jodatime date
author: wiloon
type: post
date: 2012-09-16T11:01:30+00:00
url: /?p=4056
categories:
  - Uncategorized

---
function currentTime(){
  
var d = new Date(),str = ";
  
str += d.getFullYear()+&#8217;年&#8217;;
  
str  += d.getMonth() + 1+&#8217;月&#8217;;
  
str  += d.getDate()+&#8217;日&#8217;;
  
str += d.getHours()+&#8217;时&#8217;;
  
str  += d.getMinutes()+&#8217;分&#8217;;
  
str+= d.getSeconds()+&#8217;秒&#8217;;
  
return str;
  
}