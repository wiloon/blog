---
title: Debian安装FTP服务器,使用vsftpd简单实现
author: "-"
date: 2016-07-17T15:05:03+00:00
url: /?p=9133
categories:
  - Inbox
tags:
  - reprint
---
## Debian安装FTP服务器,使用vsftpd简单实现

<http://wudixiaozi.com/1694.html>

Debian安装FTP服务器,使用vsftpd简单实现
  
June 27th, 2013无敌小子Leave a commentGo to comments
  
Debian自己安装的时候若没有勾选FTP服务器的话,那就需要在后期手动安装了！这里简单介绍一下debian如何安装和配置FTP服务器！

Debian下实现FTP的软件很多,我这里推荐vsftpd,因为他非常的短小精干,只要设置得当还是不错的！那我们就按照下面的命令一步步的来完成！

首先我们更新下软件源:
  
aptitude update

安装vsftpd
  
apt-get install vsftpd

安装完毕以后我们来配置vsftpd,使用nano编辑器打开
  
nano /etc/vsftpd.conf

打开后我们找到anonymous_enable=YES 替换成anonymous_enable=NO
  
找到local_enable=YES,将前面的#去掉
  
找到Write_enable=NO将前面的#去掉,改成YES
  
然后在配置文件的最后一行加上: chroot_local_user=YES 目的是让登陆用户锁定在指定目录里面！放置用户可以返回上层目录！

接下来创建用户组:
  
groupadd ftp
  
一般会提示用户组ftp已存在,我们忽略他！
  
创建用户
  
useradd -g ftp -d /var/www user
  
这里需要修改的就量个,/var/www是你想创建的用户登陆后锁定在哪个目录里面,上面的user是用户名,你这里可以改成你自己想要的！
  
然后我们给添加的ftp的user更改密码
  
passwd user
  
输入两次后就改好了！
  
重启vsftpd服务,让配置生效
  
invoke-rc.d vsftpd restart

为了让设定的/var/www可读写,我们还要设定下目录权限
  
chmod -R 777 /var/www/

大功告成,这时候可以使用类似flashFXP这种FTP客户端登陆测试看看！
