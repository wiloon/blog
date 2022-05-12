---
title: apache basic
author: "-"
date: 2011-05-29T08:55:08+00:00
url: /?p=206
categories:
  - Linux
tags:
  - reprint
---
## apache basic
### apache path
    /etc/apache2/apache2.conf

    /etc/apache2/httpd.conf

    /var/log/apache2
### linux  apache 版本
linux 自动安装的 apache: sudo apachectl -v

### 启动/重启/停止apache服务器
    Task: Start Apache 2 Server /启动apache服务
      
    # /etc/init.d/apache2 start
      
    or
      
    $ sudo /etc/init.d/apache2 start

    Task: Restart Apache 2 Server /重启apache服务
      
    # /etc/init.d/apache2 restart
      
    or
      
    $ sudo /etc/init.d/apache2 restart

    Task: Stop Apache 2 Server /停止apache服务
      
    # /etc/init.d/apache2 stop
      
    or
      
    $ sudo /etc/init.d/apache2 stop
