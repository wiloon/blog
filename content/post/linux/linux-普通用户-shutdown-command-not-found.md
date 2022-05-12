---
title: 'linux  shutdown'
author: "-"
date: 2011-11-24T07:54:50+00:00
url: /?p=1590
categories:
  - Linux
tags:$
  - reprint
---
## 'linux  shutdown'
shutdown是最安全的关机和重启命令，平时使用时推荐使用shutdown命令关机和重启。
  
shutdown

【语法】shutdown [选项] [参数]
  
【详解】shutdown是最安全的关机和重启命令，平时使用时推荐使用shutdown命令关机。而且该命令支持定时操作。
  
【选项】

选项 相应功能
  
-a 指定权限
  
-r 重启计算器 (和reboot) 命令一样
  
-k 模拟关机 (只向用户发出警告信息，但不关机) 
  
-h 关闭计算机并关闭电源 (常用) 
  
-n 不调用init进程关闭计算机 (不推荐) 
  
-c 取消正在执行的关机命令
  
-f 重启计算机，但不进行磁盘检测
  
-F 重启计算机，进行磁盘检测
  
-t(秒) 指定发出警告信息与删除信息时要延迟的秒数
  
【附加参数】

参数
  
相应介绍

时间 指关闭计算机的时间。
  
可以为详细时间，如22: 00，晚上10点关闭计算机
  
也可以作为详细分钟，如"+5"，则5分钟后关机。
  
警告信息 可以是任意文本，信息，需要引号括起来才能使用。
  
例子: 

(1)、通过shutdown命令重启计算机 (加now则是立即重启) 

shutdown -r now

(2)、设置1分钟以后关闭计算机，并在SSH中提示"1 minute after shutdown"

shutdown -h +1 "1 minute after shutdown"

shutdown1.jpg

(3)、取消关机

若需要取消关机、重启操作，在SSH中可按Ctrl+C快捷键取消正在执行的命令。当然若重新登陆了SSH或其它情况，可通过一下代码取消 (定时) 关机。
  
http://www.kwx.gd/LinuxBase/Linux-shutdown.html

http://blog.csdn.net/aloie/article/details/3141336

有点linux基础知识的，或者是系统的学习过计算机知识的人，没用过也能猜到，关机命令十有八九可能是shutdown。没错，实际上shutdown确实是liunx的关机命令，再配合各种选项，实现不同的关机效果。
  
然而在此之前，我却从没成功运行过shutdown。我是用普通用户登录，在终端下输入shutdown命令，结果显示 command not found。这就奇怪了，难道我的linux不支持这个命令？man了一下shutdown，大篇幅的说明告诉我，我的linux中是有这个命令的。但是什么执行无效呢？
  
开始怀疑普通用户无权使用关机命令，于是su——password——shutdown/sudo shutdown -r now.

结果还是 command not found。百思不得其解。
  
知道昨天，我才找到了解决方法: 普通用户确实没有关机的权限，因此要关机，必须得到管理员的授权，su是必须的，但是，向我之前那样是不可以的，必须指定su的用户，即: 
  
su – root(－前后各有一个空格)
  
password
  
shutdown -h now
  
这样就可以成功关机了.