---
title: 开机自动运行
author: "-"
date: 2011-05-08T01:59:13+00:00
url: /?p=181
categories:
  - Linux

tags:
  - reprint
---
## 开机自动运行
用户登录时, bash会在用户目录下按顺序查找以下三个文件,执行最先找到的一个.
  
~/.bash_profile
  
~/.bash_login
  
~/.profile

在上述文件中加入相应命令可以启动某些程序.
  
如: sh /***/tomcat/bin/startup.sh