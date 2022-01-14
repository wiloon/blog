---
title: Oracle-Sql 语句中 Case When 的应用
author: "-"
date: 2012-12-29T09:08:07+00:00
url: /?p=4957
categories:
  - DataBase

---
## Oracle-Sql 语句中 Case When 的应用
http://blog.csdn.net/zm1313/article/details/875700

分类:  Oracle-Sql 2006-07-04 16:19 12869人阅读 评论(1) 收藏 举报

// 如果column_4 = 'IT_PROG' 那么 输出 1.10 * column_3

// 如果column_4 = 'ST_CLERK' 那么 输出 1.15 * column_4

// 否则 输出 column_3 使用别名 "REVISED_SALARY"

SELECT column_1,column_2,column_3

CASE column_4

WHEN 'IT_PROG' THEN 1.10*column_3

WHEN 'ST_CLERK' THEN 1.15*column_3

WHEN 'SA_REP' THEN 1.20*column_3

ELSE column_3 END "REVISED_SALARY"

FROM table_name;

//

SELECT column_1,column_2,

SUM(CASE WHEN column_3 = '100' THEN column_4 ELSE 0 END) AS cost_100

FROM table_name

GROUP BY column_1,column_2;

// 如果 f_this_price = 0 或 f_last_price = 0 则结果为 0 ，如果都不为 0 时， 取两列差的合计

SELECT f_wzbm,

CASE WHEN SUM(f_this_price) = 0 OR SUM(f_last_price) = 0

THEN 0

ELSE SUM(f_this_price - f_last_price)

END f_markup_price

FROM table_name

GROUP BY f_wzbm;