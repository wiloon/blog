---
title: Calendar compareTo
author: "-"
date: 2016-04-07T10:47:30+00:00
url: /?p=8859
categories:
  - Inbox
tags:
  - reprint
---
## Calendar compareTo
http://www.pocketdigi.com/20110712/383.html

Calendar类的compareTo方法可以比较两个Calendar表示的时间的早晚:

Calendar a= Calendar.getInstance();
  
a.set(2011, 05,28, 19,50, 2);
  
//参数为年 月 日 时 分 秒
  
a.set(Calendar.MILLISECOND, 0);
  
//设置毫秒
  
Calendar c= Calendar.getInstance();
  
c.set(2011, 05,28, 19,50, 3);
  
c.set(Calendar.MILLISECOND, 0);
  
System.out.println(a.compareTo(c));
  
//a比c早,返回-1,
  
//a与c相同,返回0
  
//a比c晚,返回1

compareTo只能比较两个时间的早晚,并不能比较时差,如果需要得到时差,可以使用getTimeInMillis方法,得到的是距格林威治标准时间的毫秒值,两个值相减,就是时差.

© 2011, 冰冻鱼. 请尊重作者劳动成果,复制转载保留本站链接! 应用