---
title: RHEL 5 vsftpd
author: "-"
date: 2012-01-30T06:07:10+00:00
url: /?p=2195
categories:
  - Linux
tags:$
  - reprint
---
## RHEL 5 vsftpd
vsftpd安装
  
[root@linux01 ~]# mkdir /media/cdrom
  
[root@linux01 ~]# mount -t iso9660 /dev/cdrom /media/cdrom # 挂载镜像
  
mount: block device /dev/cdrom is write-protected, mounting read-only
  
[root@linux01 ~]# cd /media/cdrom/Server # 进入软件包目录
  
[root@linux01 Server]#
  
[root@linux01 Server]# rpm -qa | grep ^vsftpd # 查询相关已经安装的软件包
  
[root@linux01 Server]# ls | grep vsftpd* # 查询当前路径下安装包
  
vsftpd-2.0.5-12.el5.i386.rpm
  
[root@linux01 Server]# rpm -ivh vsftpd-2.0.5-12.el5.i386.rpm # 安装软件包 i安装 v输出详细信息 h进度
  
warning: vsftpd-2.0.5-12.el5.i386.rpm: Header V3 DSA signature: NOKEY, key ID 37017186
  
Preparing... ########################################### [100%]
  
1:vsftpd ########################################### [100%]
  
[root@linux01 Server]# rpm -qa | grep ^vsftpd # 再次查询相关已经安装的软件包
  
vsftpd-2.0.5-12.el5
  
[root@linux01 Server]#cd
  
[root@linux01 ~]# rpm -ql vsftpd | grep etc # 查询etc中与vsftpd相关的文件
  
/etc/logrotate.d/vsftpd.log
  
/etc/pam.d/vsftpd
  
/etc/rc.d/init.d/vsftpd
  
/etc/vsftpd
  
/etc/vsftpd/ftpusers
  
/etc/vsftpd/user_list
  
/etc/vsftpd/vsftpd.conf
  
/etc/vsftpd/vsftpd_conf_migrate.sh
  
[root@linux01 ~]#