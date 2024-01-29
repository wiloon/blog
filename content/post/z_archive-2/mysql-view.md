---
title: MySQL view, MERGE, TEMPTABLE
author: "-"
date: 2018-02-11T01:42:00+00:00
url: /?p=11863
categories:
  - Inbox
tags:
  - reprint
---
## MySQL view, MERGE, TEMPTABLE
数据库视图
  
数据库视图的创建是基于SQL SELECT query和JOIN的。视图和表很相似,它也包含行和列,所以可以直接对它进行查询操作。另外大多数的数据库同样允许进行UPADTE操作,但必须满足一定的条件。

MySQL View
  
MySQL从5.x版本支持视图,并且基本符合SQL: 2003标准。
  
MySQL中执行查询视图的方式有一下两种: 

MySQL会合并输入的查询语句和视图的查询声明然后执行合并后的语句并返回结果。
  
MySQL会基于视图的查询声明创建一个temporary table, 当执行查询语句时会查询这张temporary table
  
如果创建视图的时候并未指定查询方式,MySQL会默认优先使用第一种,但如果视图的查询声明中的SELECT使用了聚合函数(MIN, MAX, SUM, COUNT, AVG, etc., or DISTINCT, GROUP BY, HAVING, LIMIT, UNION, UNION ALL, subquery.),那么视图查询会使用第二种方式。

Create View
  
创建MySQL视图可以使用CREATE VIEW声明: 

CREATE
     
[ALGORITHM = {MERGE | TEMPTABLE | UNDEFINED}]
  
VIEW [database_name].[view_name]
  
AS
  
[SELECT statement]
  
ALGORITHM: 
  
MySQL有三种视图执行策略, 分别是MERGE, TEMPTABLE, UNDEFINED.

使用MERGE策略,MySQL会先将输入的查询语句和视图的声明语句进行合并,然后执行合并后的语句并返回。但是如果输入的查询语句中不允许包含一些聚合函数如: MIN, MAX, SUM, COUNT, AVG, etc., or DISTINCT, GROUP BY, HAVING, LIMIT, UNION, UNION ALL, subquery。同样如果视图声明没有指向任何数据表,也是不允许的。如果出现以上任意情况, MySQL默认会使用UNDEFINED策略。
  
使用TEMPTABLE策略,MySQL先基于视图的声明创建一张temporary table,当输入查询语句时会直接查询这张temporary table。由于需要创建temporary table来存储视图的结果集, TEMPTABLE的效率要比MERGE策略低,另外使用temporary table策略的视图是无法更新的。
  
使用UNDEFINED策略,如果创建视图的时候不指定策略,MySQL默认使用此策略。UNDEFINED策略会自动选择使用上述两种策略中的一个,优先选择MERGE策略,无法使用则转为TEMPTABLE策略。

作者: 孙进不后退
  
链接: https://www.jianshu.com/p/b11430bc4fba
  
來源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

If the MERGE algorithm cannot be used, a temporary table must be used instead. MERGE cannot be used if the view contains any of the following constructs:

Aggregate functions (SUM(), MIN(), MAX(), COUNT(), and so forth)

DISTINCT

GROUP BY

HAVING

LIMIT

UNION or UNION ALL

Subquery in the select list

Assignment to user variables

Refers only to literal values (in this case, there is no underlying table)

https://www.jianshu.com/p/b11430bc4fba
  
https://dev.MySQL.com/doc/refman/5.6/en/view-algorithms.html