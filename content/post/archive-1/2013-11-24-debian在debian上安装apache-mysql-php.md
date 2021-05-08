---
title: Debian/在Debian上安装Apache Mysql PHP
author: w1100n
type: post
date: 2013-11-24T03:39:29+00:00
url: /?p=5987
categories:
  - Uncategorized

---
## 安装Apache Mysql PHP

安装之前，保证你的版本是最新的。使用命令: （"#"表示你应该以root的身份来运行）。

# aptitude update && aptitude upgrade

  * mysql

使用下面的命令来安装mysql: 

# aptitude install mysql-server mysql-client

安装完mysql server后，你应该修改下root的密码。*此步骤对debian Lenny版本无效，因为在安装的时候你将会被要求输入mysql root用户的密码。

# /usr/bin/mysqladmin -u root password 'enter-your-good-new-password-here'

为了安全起见，你应该不使用root账户来运行数据库，而是新建一个账户来从一个PHP脚本来连接你的mysql数据库。

  * apache2

# aptitude install apache2 apache2-doc

  * PHP

# aptitude install php5 php5-mysql libapache2-mod-php5

## 配置Apache Mysql PHP

Apache2 配置文件: /etc/apache2/apache2.conf

当需要的时候，你可以编辑此配置文件。

## 测试PHP

为了测试php接口, 编辑文件 /var/www/apache2-default/test.php:

# nano /var/www/apache2-default/test.php

插入下面代码

<?php phpinfo(); ?>

http://www.zzbaike.com/wiki/Debian/%E5%9C%A8Debian%E4%B8%8A%E5%AE%89%E8%A3%85Apache_Mysql_PHP