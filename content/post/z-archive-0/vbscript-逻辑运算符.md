---
title: jinfo
author: "-"
date: 2011-11-11T08:53:02+00:00
url: /?p=1483
categories:
  - Development

tags:
  - reprint
---
## jinfo
jinfo可以输出并修改运行时的java 进程的opts。用处比较简单，用于输出JAVA系统参数及命令行参数。用法是jinfo -opt pid 如: 查看2788的MaxPerm大小可以用 jinfo -flag MaxPermSize 2788
  
jinfo -flag MaxHeapSize 13112

<no option>
  
打印命令行标识参数和系统属性键值对。
  
-flag name
  
打印指定的命令行标识参数的名称和值。
  
-flag [+|-]name
  
启用或禁用指定的boolean类型的命令行标识参数。
  
-flag name=value
  
为给定的命令行标识参数设置指定的值。
  
-flags
  
成对打印传递给JVM的命令行标识参数。
  
-sysprops
  
以键值对形式打印Java系统属性。
  
-h
  
打印帮助信息。
  
-help
  
打印帮助信息。
  
http://www.softown.cn/post/182.html