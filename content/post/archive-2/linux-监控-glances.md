---
title: 'linux  监控  glances'
author: "-"
date: 2016-10-18T09:02:31+00:00
url: /?p=9312
categories:
  - Inbox
tags:
  - reprint
---
## 'linux  监控  glances'
[http://glances.readthedocs.io/en/latest/index.html](http://glances.readthedocs.io/en/latest/index.html)

```bash
  
#filter process
  
glances -f process-name

#server mode
  
glances -s

#client
  
glances -c xxx.xxx.xxx.xxx:xxxx
  
```

Glances 还是有些值得关注的,和那些常用的老牌监控工具比起来,比如 top/vmstat/iostat 只能监控本机系统,Glances 可以监控本机也可以通过客户端服务器模式监控其他机器；Glances 提供了基于 XML/RPC 的 API 便于其他程序调用,可编程；Glances 可以将数据输出保存到 csv 或 html 格式的文件方便其他程序处理 (报告或绘制图形) 。

Glances 是用 Python 开发的,使用 psutil 库来采集系统数据,在用户的终端上实时动态的显示重要的系统数据和变化。显示的数据包括: CPU、内存、磁盘、网络等使用情况,内核、运行队列、负载、I/O 状态、消耗资源最多的进程等等。

安装
  
Glance 支持 Linux, Mac OS X, FreeBSD, Windows 等多个系统,安装也很方便。在 Ubuntu 上安装:

$ sudo apt-get update
  
$ sudo apt-get install python-pip build-essential python-dev

$ sudo pip install glances

在 CentOS 6.x 上安装:

$ su root

# rpm -ivh [http://fr2.rpmfind.net/linux/epel/6/x86_64/epel-release-6-7.noarch.rpm](http://fr2.rpmfind.net/linux/epel/6/x86_64/epel-release-6-7.noarch.rpm)

# yum install python-pip python-devel

# pip-python install glances

在 FreeBSD 上安装:

# pkg_add -r py27-glances

或者

# cd /usr/ports/sysutils/py-glances/

# make install clean

使用
  
Glances 可以单机使用,也可以客户端－服务器模式多机使用。单机使用很简单,直接运行就可以了:

$ glances

客户端－服务器模式稍微复杂一点,需要在一台机器上以服务器模式启动 glances -s,另外一台机器以客户端模式连接 glances -c. 比如在有两台机器 A 和 B 都装了 glances,要想在 A 上看 B 上的 glances 的话需要事先在 B 上用服务器模式启动 glances (假设 B 的 IP 地址是 192.168.2.22) :

$ glances -s

然后再从 A (客户端) 用 Glances 访问 B (服务器) :

$ glances -c 192.168.2.22

编程
  
Glances 和其他一堆老牌系统监控工具相比其突出优点在于提供 XML-RPC API,可编程。使用 Glances 提供的 API,我们可以通过编程轻松获取 (我们想要的) 数据。比如下面的是一个打印系统信息的简单 Python 脚本:

$ vi test.py
  
# !/usr/bin/python
  
import xmlrpclib

s = xmlrpclib.ServerProxy('http://192.168.2.22:61209')
  
print s.getSystem()

运行上面这个脚本:

$ python test.py
  
{"linux_distro": "Ubuntu 12.04", "platform": "64bit", "os_name": "Linux", "hostname": "vpsee.com", "os_version": "3.2.0-23-virtual"}

[http://www.vpsee.com/2013/07/a-new-system-monitoring-tool-glances-installation-and-usage/](http://www.vpsee.com/2013/07/a-new-system-monitoring-tool-glances-installation-and-usage/)
