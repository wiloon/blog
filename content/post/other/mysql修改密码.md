---
title: MySQL修改密码
author: "-"
date: 2011-12-26T07:22:14+00:00
url: /?p=2013
categories:
  - DataBase
tags:
  - MySQL

---
## MySQL修改密码

```bash

/usr/bin/MySQLadmin -u root password 'haCahpro'

```

MySQL改root密码

MySQL -u root -p

    MySQL> SET PASSWORD FOR 'root'@'localhost'=PASSWORD('pa55word');
 MySQL> QUIT
  
    SQL Error (1130): Host '192.168.1.126' is not allowed to connect to this MySQL server
  
  
    通过HeidiSQL连接MySQL数据库报错: 
 SQL Error (1130): Host '192.168.1.126' is not allowed to connect to this MySQL server
 说明所连接的用户帐号没有远程连接的权限，只能在本机(localhost)登录。
 需更改 MySQL 数据库里的 user表里的 host项把localhost改称%
 首先按下面的步骤登录MySQL服务器
 登录MySQL需要切换到dos下的MySQL的bin目录，进行如下操作:
  
    MySQL>use MySQL;
  
  
    MySQL>update user set host = '%'  where user ='root';
 MariaDB [MySQL]> update user set host = '%' where host = 'localhost';
 Query OK, 0 rows affected (0.00 sec)
 Rows matched: 0  Changed: 0  Warnings: 0
  
    MySQL>flush privileges;
 MySQL> select host, user from user;
 MySQL>quit
  
    http://blog.csdn.net/rgb_rgb/article/details/38693075
  