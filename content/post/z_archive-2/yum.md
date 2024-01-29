---
title: yum
author: "-"
date: 2017-07-21T01:42:58+00:00
url: yum
categories:
  - Inbox
tags:
  - remix
---
## yum

## yum command

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

#只升级所有包,不升级软件和系统内核
yum -y upgrade 

#check installed package
rpm -qa|grep jdk

#安装
yum install httpd
yum -y install httpd

## yum 安装 本地 rpm 包, local install
sudo yum localinstall influxdb-1.2.4.x86_64.rpm

#yum mirror
/etc/yum.repos.d
#Yum更新中排除特定的包
yum update --exclude=kernel* --exclude=php*
https://www.howtoing.com/exclude-packages-from-yum-update
```

## 卸载

```bash
# 默认会卸载依赖包
yum remove httpd
yum -y remove httpd

# 不卸载依赖
rpm -e --nodeps foo
```

### Delta RPMs disabled because /usr/bin/applydeltarpm not installed

```bash
    # 查看哪个包提供 applydeltarpm
    yum provides '*/applydeltarpm'  
    # 安装 deltarpm
    yum install deltarpm -y
```

### 清除metadata

```bash
    run yum --enablerepo=updates clean metadata
```

### yum 安装报错“rpmdb: BDB0113”

```r
error: rpmdb: BDB0113 Thread/process ****/************* failed: BDB1507 Thread died in Berkeley DB library
error: db5 error(-30973) from dbenv->failchk: BDB0087 DB_RUNRECOVERY: Fatal error, run database recovery
error: cannot open Packages index using db5 -  (-30973)
error: cannot open Packages database in /var/lib/rpm
```

```bash
rm -f /var/lib/rpm/__db*
rpm --rebuilddb
```

[https://my.oschina.net/andyfeng/blog/601291](https://my.oschina.net/andyfeng/blog/601291)
  
[http://gzmaster.blog.51cto.com/299556/72278](http://gzmaster.blog.51cto.com/299556/72278)
  
[http://www.cnblogs.com/kevingrace/p/6252659.html](http://www.cnblogs.com/kevingrace/p/6252659.html)

### rpm repo

>[https://www.rpmfind.net/linux/RPM/index.html](https://www.rpmfind.net/linux/RPM/index.html)

## yum 安装报错The GPG keys listed for the "CentOS-7 - Base - 163.com" repository are already installed but they are not correct for this package.

安装现有的 gpg 公钥，在 /etc/pki/rpm-gpg/ 下，可以 sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY*，直接把所有的都安装。。。
还是不行的话，就通过参数指定不检查数字签名，sudo yum -y install * --nogpgcheck