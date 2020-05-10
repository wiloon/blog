---
title: joda time, time zone
author: wiloon
type: post
date: 2012-06-13T05:09:31+00:00
url: /?p=3523
categories:
  - Java

---
[java]

DateTime dt = new DateTime(DateTimeZone.forOffsetHours(8));
   
dt=dt.withZone(DateTimeZone.forOffsetHours(-5));
   
DateTimeFormatter dtf = DateTimeFormat.forPattern("yyyy-MM-dd&#8217;T&#8217;HH:mm:ssZZ");
   
System.out.println(dtf.print(dt));
   
String s="2012-06-27T20:00:00+08:00";
   
DateTime dt2= dtf.parseDateTime(s) ;
   
System.out.println(dtf.print(dt2));

[/java]