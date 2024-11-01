---
title: win10 onedrive cpu
author: "-"
date: 2019-04-11T10:42:28+00:00
url: /?p=14137
categories:
  - Inbox
tags:
  - reprint
---
## win10 onedrive cpu

[https://mingjiejian.github.io/2017/09/15/onedrive/](https://mingjiejian.github.io/2017/09/15/onedrive/)

推荐且不怎么伤的办法
  
从解决方法来说原因应该是Onedrive的log出错了，一直以为没有更新所以卡在更新/安装上，所以一个比较简单的解决办法就是删掉错误的log。这两个log是

C:\Users\用户名\AppData\Local\Microsoft\OneDrive\setup\logs\userTelemetryCache.otc C:\Users\用户名\AppData\Local\Microsoft\OneDrive\setup\logs\userTelemetryCache.otc.session

在Onedrive打开而且用户没有注销登录的情况下在任务管理器中结束OneDriveSetup.exe进程
  
将上述的两个log文件删除
  
运行C:\Users\用户名\AppData\Local\Microsoft\OneDrive\Update\OneDriveSetup.exe
  
应该就可以了
  
有的时候可能自己觉得太烦想重装，已经将Onedrive卸载了 (我就是这么做的) ；这个时候只需要做上面的第2步然后双击安装文件就行了，不会再卡在安装那。不过之后要重新登录一下自己的账户。
