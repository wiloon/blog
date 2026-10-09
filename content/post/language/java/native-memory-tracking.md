---
title: NMT, Native Memory Tracking
author: "-"
date: 2017-02-06T05:15:44+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: java-native-memory-tracking
categories:
  - Java
tags:
  - java
  - jvm
  - remix
  - AI-assisted
aliases:
  - /p9726/
---
## NMT, Native Memory Tracking

NMT for Hotspot VM is turned off by default. Turn this feature on using JVM command line option
  
-XX:NativeMemoryTracking=[off | summary | detail]
  
注意,根据Java官方文档,开启NMT会有5%－10%的性能损耗；

访问NMT数据

JDK提供了jcmd命令来访问NMT数据:

```bash
jcmd <pid> VM.native_memory [summary | detail | baseline | summary.diff | detail.diff | shutdown] [scale= KB | MB | GB]
```
  
配置项 说明
  
summary 只打印打印按分类汇总的内存
  
detail 打印按分类汇总的内存用法、virtual memory map和每次内存分配调用
  
baseline 创建内存快照,以比较不同时间的内存差异
  
summary.diff 打印自上次baseline到现在的内存差异,显示汇总信息
  
detail.diff 打印自上次baseline到现在的内存差异, 显示详细信息
  
shutdown 关闭NMT功能,NMT can be shutdown using jcmd utility, but can not start/restart using jcmd
  
scale 指定内存单位,默认为KB

```bash
  
./jcmd PID VM.native_memory baseline
  
```

[http://www.voidcn.com/blog/jicahoo/article/p-5727258.html](http://www.voidcn.com/blog/jicahoo/article/p-5727258.html)
  
[http://blog.csdn.net/jicahoo/article/details/50933469](http://blog.csdn.net/jicahoo/article/details/50933469)
  
[https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr007.html](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr007.html)
  
[http://www.jianshu.com/p/7fce29433171](http://www.jianshu.com/p/7fce29433171)
  
[https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr022.html#BABHIFJC](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr022.html#BABHIFJC)
  
[http://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr.html](http://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `native-memory-tracking.md`；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
