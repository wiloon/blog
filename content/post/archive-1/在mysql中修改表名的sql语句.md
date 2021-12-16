---
title: 在MySQL中修改表名的sql语句
author: "-"
date: 2014-04-09T02:12:14+00:00
url: /?p=6494
categories:
  - Uncategorized
tags:
  - MySQL

---
## 在MySQL中修改表名的sql语句
http://blog.csdn.net/xrt95050/article/details/2441458

在使用MySQL时,经常遇到表名不符合规范或标准,但是表里已经有大量的数据了,如何保留数据,只更改表名呢？

       可以通过建一个相同的表结构的表,把原来的数据导入到新表中,但是这样视乎很麻烦。

      能否简单使用一个SQL语句就搞定呢？当然可以,MySQL5.0下我们使用这样的SQL语句就可以了。

ALTER  TABLE table_name RENAME TO new_table_name

例如 ALTER  TABLE admin_user RENAME TO a_user