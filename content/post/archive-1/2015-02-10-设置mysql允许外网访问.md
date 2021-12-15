---
title: 设置MySQL允许外网访问
author: "-"
date: 2015-02-10T15:21:59+00:00
url: /?p=7344
categories:
  - Uncategorized
tags:
  - MySQL

---
## 设置MySQL允许外网访问

  1.修改配置文件


  
    
      sudo vim /etc/MySQL/my.cnf
 把bind-address参数的值改成你的内/外网IP或0.0.0.0,或者直接注释掉这行.
    
    
    
      
    
    
    
      解决MySQL不允许从远程访问的方法
    
    
    
      解决方法: 
 1。改表法。可能是你的帐号不允许从远程登陆，只能在localhost。这个时候只要在localhost的那台电脑，登入MySQL后，更改 "MySQL" 数据库里的 "user" 表里的 "host" 项，从"localhost"改称"%"
    
    
    
      MySQL -u root -pvmwareMySQL>use MySQL;
 MySQL>update user set host = '%' where user = 'root';
 MySQL>select host, user from user;
    
    
    
      
    
    
    
      
    
    
    
      MySQL>FLUSH   PRIVILEGES
 使修改生效.就可以了
  
