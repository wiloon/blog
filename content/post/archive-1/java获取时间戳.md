---
title: JAVA获取时间戳
author: "-"
date: 2014-04-01T06:13:24+00:00
url: /?p=6461
categories:
  - Uncategorized
tags:
  - Java

---
## JAVA获取时间戳

http://tangmingjie2009.iteye.com/blog/1543166


JAVA时间戳

目前获取毫秒值大概有下面三种方法


Java代码 收藏代码

//方法 一

System.currentTimeMillis();

//方法 二

Calendar.getInstance().getTimeInMillis();

//方法 三

new Date().getTime();

最近做监控系统,发现代码中有前两种方法,然后突然有了一个想法,到底哪个更快呢？

然后做了如下实验: 


Java代码 收藏代码

import java.util.Calendar;

import java.util.Date;


public class TimeTest {

private static long _TEN_THOUSAND=10000;

public static void main(String[] args) {

long times=1000*_TEN_THOUSAND;

long t1=System.currentTimeMillis();

testSystem(times);

long t2=System.currentTimeMillis();

System.out.println(t2-t1);

testCalander(times);

long t3=System.currentTimeMillis();

System.out.println(t3-t2);

testDate(times);

long t4=System.currentTimeMillis();

System.out.println(t4-t3);

}


public static void testSystem(long times){//use 188

for(int i=0;i<times;i++){

long currentTime=System.currentTimeMillis();

}

}


public static void testCalander(long times){//use 6299

for(int i=0;i<times;i++){

long currentTime=Calendar.getInstance().getTimeInMillis();

}

}


public static void testDate(long times){

for(int i=0;i<times;i++){

long currentTime=new Date().getTime();

}


}


}

因为很简单我就不加注释了,每种方法都运行1千万次,然后查看运行结果

Java代码 收藏代码

187

7032

297


结果发现 System.currentTimeMillis() 这种方式速度最快

Calendar.getInstance().getTimeInMillis() 这种方式速度最慢,看看源码会发现,Canlendar因为要处理时区问题会耗费很多的时间。

所以建议多使用第一种方式。


另,System 类中有很多高效的方法,比如,arrayCopy 之类的