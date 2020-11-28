---
title: yum command
author: w1100n
type: post
date: 2017-07-21T01:42:58+00:00
url: /?p=10878
categories:
  - Uncategorized

---
### 按版本安装

```bash
yum list|grep filebeat

# 回显
filebeat.x86_64                         7.2.0-1                         @elastic
filebeat.i686                           7.2.1-1                         elastic
filebeat.x86_64                         7.2.1-1                         elastic

# 安装 指定版本7.2.0-1
yum install filebeat-7.2.0-1
```

```bash
#search
yum search iostat

#search
yum list java*

# HTTP Error 404 - Not Found
yum clean all
rpm --rebuilddb
yum update

#check package installed
yum list installed xxx

# 列出所有已安装的软件包 
yum list installed

#升级所有包同时也升级软件和系统内核
yum -y update 

#只升级所有包，不升级软件和系统内核
yum -y upgrade 

#check installed package
rpm -qa|grep jdk

#安装
yum install httpd
yum -y install httpd

#local install
sudo yum localinstall influxdb-1.2.4.x86_64.rpm

#卸载
yum remove httpd
yum -y remove httpd


#yum mirror
/etc/yum.repos.d
#Yum更新中排除特定的包
yum update --exclude=kernel* --exclude=php*
https://www.howtoing.com/exclude-packages-from-yum-update
```

https://my.oschina.net/andyfeng/blog/601291
  
http://gzmaster.blog.51cto.com/299556/72278
  
http://www.cnblogs.com/kevingrace/p/6252659.html