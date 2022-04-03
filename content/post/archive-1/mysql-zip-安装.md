---
title: MySQL install
author: "-"
date: 2015-04-04T03:31:16+00:00
url: /?p=7434
categories:
  - Uncategorized
tags:
  - MySQL

---
## MySQL install

## debian install MySQL server
```bash

sudo apt-get install MySQL-server

```


**一、下载MySQL安装包**

安装包名称: MySQL-5.6.12-win32.zip

下载地址: <http://dev.MySQL.com/downloads/MySQL/>

**二、安装MySQL**

**2.1 修改配置文件my.ini**

将MySQL-5.6.12-win32.zip解压拷贝到F:\

修改F:\MySQL-5.6.12-win32.zip目录下的配置文件my.ini如下: 

[client]
  
port = 3306

[MySQL]

[MySQLd]
  
bind-address = 0.0.0.0
  
basedir=D:/apps/MySQL-5.6.23-winx64
  
datadir=D:/apps/MySQL-5.6.23-winx64/data
  
max_connections=200
  
character-set-server=utf8
  
port=3306


-

try to start MySQL with console

```bash
  
MySQLd -console
  
```

**2.2 安装MySQL为windows系统服务**

以管理员身份(Run as administrator)启动cmd，切换到目录F:/MySQL-5.6.12-win32/bin

```bash
  
MySQLd.exe -install

```

如果以普通用户执行该命令会提示Install/Remove of the Service Denied!

**三、启动MySQL服务**

**3.1 启动MySQL服务**

以管理员身份启动cmd，切换到目录F:/MySQL-5.6.12-win32/bin

启动MySQL服务: net start MySQL

**四、执行命令**

**4.1 登录MySQL**

MySQL -u root -p

输入密码(密码为空，直接回车)，即可登录。

**4.2 执行MySQL命令**

**五、卸载MySQL**

**4.1 停止MySQL服务**

net stop MySQL

**4.2 卸载MySQL**

MySQLd.exe -removehttp://blog.csdn.net/guowenyan001/article/details/9665803

http://serverfault.com/questions/214435/error-1067-the-process-terminated-unexpectedly-when-trying-to-install-MySQL-o/214846#214846


http://tinypig.iteye.com/blog/368379

