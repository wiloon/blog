---
title: busybox
author: "-"
date: 2017-05-27T04:22:18+00:00
url: /?p=10381
categories:
  - Uncategorized

tags:
  - reprint
---
## busybox
BusyBox 是一个提供了很多简化版的Unix 工具的一个可执行文件, busybox能在很多POSIX环境运行,比如Linux,Android,FreeBSD.

BusyBox最初是由布鲁斯·斐伦斯在1996年为Debian GNU/Linux安装光盘而编写
  
Busybox只提供每个工具程序的简化版 (例如: ls指令不提供排序功能) 。

BusyBox 是一个集成了一百多个最常用linux命令和工具的软件,他甚至还集成了一个http服务器和一个telnet服务器,而所有这一切功能却只有区区1M左右的大小。BusyBox 包含了一些简单的工具,比如: 我们平时用的那些linux命令就好比是分立式的电子元件,而busybox就好比是一个集成电路,把常用的工具和命令集成压缩在一个可执行文件里,功能基本不变,而大小却小很多倍,例如ls、 cat 和 echo等等,还包含了一些更大、更复杂的工具,例如 grep、find、mount 以及telnet。简单的说BusyBox就好像是个大工具箱,它集成压缩了 Linux 的许多工具和命令,也包含了 Android 系统自带的shell。BusyBox 将许多具有共性的小版本的UNIX工具结合到一个单一的可执行文件。这样的集合可以替代大部分常用工具比如: GNU 等工具,BusyBox提供了一个比较完善的环境,可以适用于任何小的或嵌入式系统。在嵌入式linux应用中,busybox有非常广的应用,另外,大多数linux发行版的安装程序中都有busybox的身影,安装linux的时候案ctrl+alt+F2可以切换物理终端,而这个物理终端中的所有命令都是指向busybox的链接.Busybox虽小,但作用确是惊人的,这样就可以基于Busybox制作一张软盘linux。

http://jilili.blog.51cto.com/6617089/1170368
  
https://busybox.net/
  
https://en.wikipedia.org/wiki/BusyBox