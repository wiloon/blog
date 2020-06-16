---
title: Oracle-Sql 语句中 Case When 的应用
author: wiloon
type: post
date: 2012-12-29T09:08:07+00:00
url: /?p=4957
categories:
  - DataBase

---
http://blog.csdn.net/zm1313/article/details/875700

分类： Oracle&#8211;Sql 2006-07-04 16:19 12869人阅读 评论(1) 收藏 举报

// 如果column\_4 = 'IT\_PROG' 那么 输出 1.10 * column_3

// 如果column\_4 = 'ST\_CLERK' 那么 输出 1.15 * column_4

// 否则 输出 column\_3 使用别名 "REVISED\_SALARY"

SELECT column\_1,column\_2,column_3

CASE column_4

WHEN 'IT\_PROG' THEN 1.10*column\_3

WHEN 'ST\_CLERK' THEN 1.15*column\_3

WHEN 'SA\_REP' THEN 1.20*column\_3

ELSE column\_3 END "REVISED\_SALARY"

FROM table_name;

//

SELECT column\_1,column\_2,

SUM(CASE WHEN column\_3 = '100' THEN column\_4 ELSE 0 END) AS cost_100

FROM table_name

GROUP BY column\_1,column\_2;

// 如果 f\_this\_price = 0 或 f\_last\_price = 0 则结果为 0 ，如果都不为 0 时， 取两列差的合计

SELECT f_wzbm,

CASE WHEN SUM(f\_this\_price) = 0 OR SUM(f\_last\_price) = 0

THEN 0

ELSE SUM(f\_this\_price - f\_last\_price)

END f\_markup\_price

FROM table_name

GROUP BY f_wzbm;