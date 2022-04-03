---
title: java 纳秒
author: "-"
date: 2018-11-13T10:45:44+00:00
url: /?p=12879
categories:
  - Uncategorized

tags:
  - reprint
---
## java 纳秒
http://hold-on.iteye.com/blog/1943436

前段时间项目中需要 统计接口连接时间,考虑到连接时间一般都是零点几毫秒级别的,为了拿到更精确地数值,没有使用System.currentTimeMillis(),而是贸然地使用System.nanoTime()来统计时间,后来分析服务器上的数据,发现 竟然有10-15%的数据数值竟然超过了 10的13次方。

     原因: 
    

System.currentTimeMillis() 起始时间是基于 1970.1.1 0:00:00 这个确定的时间的,而System.nanoTime()是基于cpu核心的时钟周期来计时,它的开始时间是不确定的。 (有篇文章说是更加cpu核心的启动时间开始计算的) 

但是在多核处理器上,由于每个核心的开始时间不确定,但是在多核处理器上,

Java代码 收藏代码
  
long start = System.nanoTime();
      
String ip = Utilities.getIpByUrl(url);
      
long cost = System.nanoTime() - start;

这段代码有可能会运行在两个不同的cpu核心上,从而导致得到的结果完全不符逻辑。

Returns the current timestamp of the most precise timer available on the local system, in nanoseconds. Equivalent to Linux's CLOCK_MONOTONIC.

This timestamp should only be used to measure a duration by comparing it against another timestamp from the same process on the same device. Values returned by this method do not have a defined correspondence to wall clock times; the zero value is typically whenever the device last booted. Use currentTimeMillis() if you want to know what time it is.