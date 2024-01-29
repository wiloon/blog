---
title: OPTION SQL_SELECT_LIMIT
author: "-"
date: 2016-12-28T08:54:04+00:00
url: /?p=9629
categories:
  - Inbox
tags:
  - reprint
---
## OPTION SQL_SELECT_LIMIT
http://lucifer119.blog.51cto.com/2914308/1344253

You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'OPTION SQL_SELECT_LIMIT=DEFAULT' at line 1

You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'OPTION SQL_SELECT_LIMIT=DEFAULT' at line 1

原因: 

项目中我用的jdbc驱动版本

MySQL-connector-java-5.1.15.jar

MySQL数据库版本为5.6

jdbc在连接数据库时候会发送测试语句SET OPTION SQL_SELECT_LIMIT=DEFAULT

这在MySQL5.6以下版本是可以的 ,但是5.6不再支持SET...
  
解决: 

升级驱动版本,我改成了MySQL-connector-java-5.1.25.jar  问题解决

-------

注意: 版本要匹配才行,否则会出错。