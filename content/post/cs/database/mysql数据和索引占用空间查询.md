---
title: MySQL数据和索引占用空间查询
author: "-"
date: 2017-11-24T08:42:42+00:00
url: /?p=11501
categories:
  - Inbox
tags:
  - reprint
---
## MySQL数据和索引占用空间查询
http://blog.csdn.net/light_language/article/details/70567962

关于查数据库和表中的数据和索引所占空间的大小的SQL方法: 
  
查询information_schema架构中的tables表。
  
代码: 
  
查询所有数据库占用磁盘空间大小的SQL语句: 

select table_schema,concat(truncate(sum(data_length)/1024/1024,2),'MB') as data_size,
  
concat(truncate(sum(index_length)/1024/1024,2),'MB') as index_size
  
from information_schema.tables
  
group by table_schema
  
order by sum(data_length) desc;
  
这里写图片描述

查询单个库中所有表磁盘占用大小的SQL语句: 

select table_name,concat(truncate(data_length/1024/1024,2),'MB') as data_size,
  
concat(truncate(index_length/1024/1024,2),'MB') as index_size
  
from information_schema.tables where table_schema='employees'
  
order by data_length desc;