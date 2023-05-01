---
title: linux 进程启动时间
author: "-"
date: 2017-10-15T04:55:47+00:00
url: /?p=11273
categories:
  - Inbox
tags:
  - reprint
---
## linux 进程启动时间

```bash
ps -p PID -o lstart
```

<http://www.linuxidc.com/Linux/2012-12/76143.htm>

在Linux下,如果需要查看进程的启动时间, 常用 ps aux 命令,但是 ps aux 命令的缺陷在于只能显示时间到年、日期、或者时间, 无法具体到年月日时分秒。如果需要查看某个进程的具体启动时间, 使用 ps -p PID -o lstart, 其中,PID为某个进程的进程ID号。

如下所示, 显示系统中所有httpd进程的具体启动时间。

for pid in $(pgrep httpd); do echo -n "${pid} " ; ps -p ${pid} -o lstart | grep -v "START" ; done
  
301 Mon Aug 27 11:21:59 2012
  
344 Mon Aug 27 11:33:13 2012
  
25065 Sun Aug 26 03:27:03 2012
  
25066 Sun Aug 26 03:27:03 2012
  
25067 Sun Aug 26 03:27:03 2012
  
25068 Sun Aug 26 03:27:03 2012
  
25069 Sun Aug 26 03:27:03 2012
  
25070 Sun Aug 26 03:27:03 2012
  
25071 Sun Aug 26 03:27:03 2012
  
25072 Sun Aug 26 03:27:03 2012
  
27903 Wed Jun 20 22:50:47 2012
  
32767 Mon Aug 27 11:21:48 2012
