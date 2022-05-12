---
title: linux ftp
author: "-"
date: 2012-01-07T10:45:15+00:00
url: /?p=2100
categories:
  - Linux
tags:$
  - reprint
---
## linux ftp
安装:

apt-get install vsftpd

默认设置:

  * 家目录/srv/ftp ......在/etc/password 中可以查到.
  * 允许匿名访问.
  * /etc/ftpusers 记录着不允许访问FTP服务器的用户名单.默认排除了root

启动服务 /etc/init.d/./vsftpd start

重启服务 /etc/init.d/./vsftpd restart

停止服务 /etc/init.d/./vsftpd stop


修改/etc/vsftpd.conf


listen=yes  (独立的VSFTPD服务器) 


anonymous_enable=yes (允许匿名登陆)


local_enable=NO (禁止本地系统用户)


write_enable=NO (不开放本地用户写权限)


anon_upload_enable=NO (匿名用户上传权限)


anon_mkdir_write_enable=NO (关闭可上传目录并关闭在此目录上传权限)


anon_other_write_enable=NO (关闭匿名帐户的删除权限)


anon_world_readable_only=YES (禁止匿名拥护下载具有全局读取权限的文件)


hide_ids=YES (目录中用户和组信息列取都显示为ftp)


ls_recurse_enable=NO  (禁止ls -R 递归查询) 
dirmessage_enable=yes  (切换目录时，显示目录下.message的内容) 


local_umask=022 (FTP上本地的文件权限，默认是077)


connect_form_port_20=yes  (启用FTP数据端口的数据连接) *


xferlog_enable=yes  (激活上传和下传的日志) 


xferlog_std_format=yes (使用标准的日志格式)


ftpd_banner=XXXXX  (欢迎信息) 


pam_service_name=vsftpd  (验证方式) 

