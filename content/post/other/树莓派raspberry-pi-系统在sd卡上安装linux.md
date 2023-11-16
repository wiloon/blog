---
title: 树莓派(raspberry pi) 系统在SD卡上安装Linux
author: "-"
date: 2013-04-17T15:43:43+00:00
url: /?p=5408
categories:
  - Raspberry-Pi
tags:
  - reprint
---
## 树莓派(raspberry pi) 系统在SD卡上安装Linux
```bash

sudo dd bs=1M if=2012-12-16-wheezy-raspbian.img of=/dev/sdx

```

刚刚拿到一只Simon同学出借的树莓派(raspberry pi) ,准备一张4GB的SD卡,准备跑一下Linux。

在Windows 7上用 工具 Win32DiskImager写入img到SD卡上,报错,失败。

好在俺有Linux vmware虚拟机,在虚拟机上搞,执行命令 sudo dd bs=1M if=2012-12-16-wheezy-raspbian.img  of=/dev/sdb

tips:

错误: 接电启动树莓派,派上只有红色的Power灯亮,HDMI电视机上没有输出。

原因: 在Linux上执行dd命令的时候,应该是把操作系统镜像写到SD卡 (硬盘上) ,而不是写到某个硬盘分区上。of=/dev/sdb 误写成of=/dev/sdb1了。

当时写完后,我还纳闷呢,怎么Linux  fdisk上这个SD卡还显示只有一个vfat分区,而不是多个Linux分区呢。

解决办法: 首先fdisk /dev/sdb,删除vfat分区；然后执行dd命令写入镜像  sudo dd bs=1M if=2012-12-16-wheezy-raspbian.img of=/dev/sdb

#Raspian安装Chrome
  
1,wget http://goo.gl/go5yx -O install.sh
  
2,chmod a+x install.sh
  
3,./install.sh
  
4,chrome -disable-ipv6 & (& for running at background)
  
5,error loading libsmime3.so->try sudo apt-get update then redo step 3

#Raspian安装中文输入法SCIM (Smart Common Input Method)
  
1,sudo apt-get install scim-pinyin
  
2,if some packages can't be downloaded, try sudo apt-get update –-fix-missing
  
3,run scim and it will run wihle booting.

#切换到root
  
$ sudo -s

参考: 

官方下载和教程连接

[ http://www.raspberrypi.org/downloads][1]

树莓派Raspberry Pi上手报告 , 中文,Chrome浏览器

[http://www.leiphone.com/raspberry-pi-hands-on.html](http://www.leiphone.com/raspberry-pi-hands-on.html)

迷你Linux机器Raspberry Pi详解和关于其的用途 (一)  : 配置,图片,烧SD卡,Python编程

[http://blog.sina.com.cn/s/blog_a16ed9d601017q72.html](http://blog.sina.com.cn/s/blog_a16ed9d601017q72.html)

Raspberry Pi 初步体验: 配置,图片,连接

[http://archboy.org/2012/12/11/raspberry-pi-first-review/](http://archboy.org/2012/12/11/raspberry-pi-first-review/)

Raspberry Pi快速上手教程  : 配置,图片,

[http://www.eeboard.com/tutorials/raspberry-pi快速上手教程/][2]

树莓派(raspberry pi)学习5: 调整分区大小

blog.csdn.net/c80486/article/details/8460304

 [1]: http://www.raspberrypi.org/downloads
 [2]: http://www.eeboard.com/tutorials/raspberry-pi%E5%BF%AB%E9%80%9F%E4%B8%8A%E6%89%8B%E6%95%99%E7%A8%8B/