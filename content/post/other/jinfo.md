---
title: jinfo
author: "-"
date: 2011-11-11T08:53:02+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: jinfo
categories:
  - Java
tags:
  - java
  - jvm
  - remix
  - AI-assisted
aliases:
  - /vbscript-逻辑运算符/
---
## jinfo
jinfo可以输出并修改运行时的java 进程的opts。用处比较简单，用于输出JAVA系统参数及命令行参数。用法是jinfo -opt pid 如: 查看2788的MaxPerm大小可以用 jinfo -flag MaxPermSize 2788
  
jinfo -flag MaxHeapSize 13112

`<no option>`
  
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

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `jinfo.md`；url 改为 `jinfo`；旧 url 加入 aliases；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
