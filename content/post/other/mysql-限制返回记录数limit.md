---
title: MySQL limit
author: "-"
date: 2013-02-03T05:07:23+00:00
url: /?p=5117
categories:
  - DataBase
tags:
  - MySQL

---
## MySQL limit

     SELECT * FROM table  LIMIT [offset,] rows | rows OFFSET offset
  
  
    SELECT 语句返回指定的记录数
  
  
    LIMIT 接受一个或两个数字参数。参数必须是整数常量。如果输入两个参数,第一个参数指定返回记录的偏移量,第二个参数指定返回记录行的最大数目。第一条记录行的偏移量是 0(不是 1):  为了与 PostgreSQL 兼容,MySQL 也支持语法:  LIMIT # OFFSET #。
  
  
    SELECT  * FROM  table  LIMIT 2,1; //从第2条开始读,读取1条信息。
  
  
    MySQL> SELECT * FROM table LIMIT 5,10;  // 检索 6-15 行
  
//为了检索从某一个偏移量到记录集的结束所有的记录行,可以指定第二个参数为 -1:
SELECT *FROM table LIMIT 95,-1; // 检索记录行 96-last.
//如果只给定一个参数,它表示返回最大的记录行数目:
SELECT* FROM table LIMIT 5;     //检索前 5 个记录行
//换句话说,LIMIT n 等价于 LIMIT 0,n。
如果是oracle 可以用rownum实现相同的功能。

---

[http://www.phpweblog.net/peiyinjin/archive/2008/04/15/3199.html](http://www.phpweblog.net/peiyinjin/archive/2008/04/15/3199.html)
  