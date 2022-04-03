---
title: "CR3控制寄存器"
author: "-"
date: "2021-09-08 17:38:54"
url: "cr3"
categories:
  - inbox
tags:
  - inbox
---
## "CR3控制寄存器"

CR3用来存放页目录表物理内存基地址，每当进程切换时，Linux 就会把下一个将要运行进程的页目录表物理内存基地址等信息存放到CR3寄存器中。

>https://blog.csdn.net/SweeNeil/article/details/106171361