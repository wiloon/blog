---
title: MySQL删除指定数据库中的表
author: "-"
date: 2015-01-08T02:33:36+00:00
url: /?p=7199
categories:
  - Uncategorized
tags:
  - MySQL

---
## MySQL删除指定数据库中的表
http://phpcode8.com/lamp/MySQL-lamp/MySQL-empty-tables.html

SELECT concat('DROP TABLE IF EXISTS ', table_name, ';')
  
FROM information_schema.tables
  
WHERE table_schema = 'pentaho0';