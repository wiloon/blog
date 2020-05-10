---
title: OPTION SQL_SELECT_LIMIT
author: wiloon
type: post
date: 2016-12-28T08:54:04+00:00
url: /?p=9629
categories:
  - Uncategorized

---
http://lucifer119.blog.51cto.com/2914308/1344253

You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near &#8216;OPTION SQL\_SELECT\_LIMIT=DEFAULT&#8217; at line 1

You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near &#8216;OPTION SQL\_SELECT\_LIMIT=DEFAULT&#8217; at line 1

原因：

项目中我用的jdbc驱动版本

mysql-connector-java-5.1.15.jar

mysql数据库版本为5.6

jdbc在连接数据库时候会发送测试语句SET OPTION SQL\_SELECT\_LIMIT=DEFAULT

这在mysql5.6以下版本是可以的 ，但是5.6不再支持SET&#8230;
  
解决：

升级驱动版本,我改成了mysql-connector-java-5.1.25.jar  问题解决

&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211;

注意：版本要匹配才行，否则会出错。