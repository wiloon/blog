---
title: Debian/Ubuntu 系统 Update-rc.d
author: "-"
date: 2011-11-18T22:36:08+00:00
url: /?p=1523
categories:
  - Linux
tags:
  - reprint
---
## Debian/Ubuntu 系统 Update-rc.d
https://wangyan.org/blog/ubuntu-update-rc-d.html

Ubuntu或者Debian系统中update-rc.d命令，是用来更新系统启动项的脚本。这些脚本的链接位于/etc/rcN.d/目录，对应脚本位于/etc/init.d/目录。在了解update-rc.d命令之前，你需要知道的是有关Linux 系统主要启动步骤，以及Ubuntu中运行级别的知识。
  
一、Linux 系统主要启动步骤

读取 MBR 的信息，启动 Boot Manager。
  
加载系统内核，启动 init 进程， init 进程是 Linux 的根进程，所有的系统进程都是它的子进程。
  
init 进程读取 /etc/inittab 文件中的信息，并进入预设的运行级别。通常情况下 /etc/rcS.d/ 目录下的启动脚本首先被执行，然后是/etc/rcN.d/ 目录。
  
根据 /etc/rcS.d/ 文件夹中对应的脚本启动 Xwindow 服务器 xorg，Xwindow 为 Linux 下的图形用户界面系统。
  
启动登录管理器，等待用户登录。
  
二、运行级别

Ubuntu中的运行级别

0 (关闭系统) 
  
1 (单用户模式，只允许root用户对系统进行维护。) 
  
2 到 5 (多用户模式，其中3为字符界面，5为图形界面。) 
  
6 (重启系统) 
  
切换运行级别

init [0123456Ss]
  
例如: init 0 命令关机； init 6 命令重新启动
  
启动项管理工具

```bash
  
sudo apt-get install sysv-rc-conf //或者使用带gui的工具bum
  
sudo sysv-rc-conf
  
```

三、update-rc.d命令详解

从所有的运行级别中删除指定启动项

update-rc.d -f ＜basename＞ remove
  
按指定顺序、在指定运行级别中启动或关闭

update-rc.d ＜basename＞ start|stop ＜order＞ ＜runlevels＞
  
实例: update-rc.d apachectl start 20 2 3 4 5 . stop 20 0 1 6 .
  
解析: 表示在2、3、4、5这五个运行级别中，由小到大，第20个开始运行apachectl；在 0 1 6这3个运行级别中，第20个关闭apachectl。这是合并起来的写法，注意它有2个点号，效果等于下面方法: 

update-rc.d apachectl defaults
  
A启动后B才能启动，B关闭后A才关闭

update-rc.d A defaults 80 20
  
update-rc.d B defaults 90 10
  
启动和关闭顺序为90，级别默认

update-rc.d ＜basename＞ defaults 90