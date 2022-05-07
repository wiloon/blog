---
title: nc 命令检查远程端口是否打开
author: "-"
date: 2017-12-16T08:33:52+00:00
url: /?p=11614
categories:
  - Inbox
tags:
  - reprint
---
## nc 命令检查远程端口是否打开

https://linux.cn/article-8186-1.html

使用 nc 命令检查远程端口是否打开
  
编译自: http://www.tecmint.com/check-remote-port-in-linux/作者:  Aaron Kili
  
原创: LCTT https://linux.cn/article-8186-1.html译者:  geekpi
  
本文地址: https://linux.cn/article-8186-1.html
  
2017-02-09 11:50 评论: 4 收藏: 5

端口是与 Linux 操作系统上的应用或进程的通讯端点的逻辑实体。在使用之前,了解目标机器上哪些端口是打开并正在运行服务是非常有用的。

我们可以使用 netstat 或其他几个 Linux 命令如 NMAP 在本地机器上轻松地列出 Linux 中的打开端口。

在本指南中,我们将向你展示如何使用简单的 netcat (简称 nc) 命令来确定远程主机上的端口是否可访问/打开。

netcat (或简称 nc) 是一个功能强大且易于使用的程序,可用于 Linux 中与 TCP、UDP 或 UNIX 域 socket 相关的任何事情。

# yum install nc [在 CentOS/RHEL 中]

# dnf install nc [在 Fedora 22+ 中]

$ sudo apt-get install netcat [在 Debian/Ubuntu 中]
  
我们可以使用它: 打开 TCP 连接、侦听任意 TCP 和 UDP 端口、发送 UDP 数据包、在 IPv4 和 IPv6 进行端口扫描。

使用 netcat,你可以检查单个或多个或一段打开的端口范围,如下所示。下面的命令将帮助我们查看端口 22 是否在主机 192.168.56.10 上打开: 

$ nc -zv 192.168.1.15 22
  
上面的命令中,这些标志是: 

-z – 设置 nc 只是扫描侦听守护进程,实际上不向它们发送任何数据。
  
-v – 启用详细模式
  
下面的命令会检查远程主机 192.168.5.10 上是否打开了端口 80、22 和 21 (我们也可以使用主机名) : 

nc -zv 192.168.56.10 80 22 21
  
也可以指定端口扫描的范围: 

$ nc -zv 192.168.56.10 20-80
  
更多关于 netcat 命令的例子和使用,阅读我们下面的文章。

使用 netcat 命令在 Linux 服务器间传输文件
   
Linux 网络配置及排障调试命令