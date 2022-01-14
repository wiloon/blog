---
title: MySQL 里的IFNULL、NULLIF和ISNULL用法
author: "-"
date: 2014-01-16T05:03:08+00:00
url: /?p=6219
categories:
  - Uncategorized
tags:
  - MySQL

---
## MySQL 里的IFNULL、NULLIF和ISNULL用法
今天用到了MySQL里的isnull才发现他和MSSQL里的还是有点区别,现在简单总结一下: 

**MySQL中isnull,ifnull,nullif的用法如下: **

**isnull(expr) 的用法: **
  
如expr 为null,那么isnull() 的返回值为 1,否则返回值为 0。
  
MySQL> select isnull(1+1);
  
-> 0
  
MySQL> select isnull(1/0);
  
-> 1
  
使用= 的null 值对比通常是错误的。

isnull() 函数同 is null比较操作符具有一些相同的特性。请参见有关is null 的说明。

**IFNULL(expr1,expr2)的用法: **

假如expr1   不为   **NULL**,则   IFNULL()   的返回值为   expr1;
  
否则其返回值为   expr2。IFNULL()的返回值是数字或是字符串,具体情况取决于其所使用的语境。

**MySQL**>   SELECT   IFNULL(1,0);
  
->   1
  
**MySQL**>   SELECT   IFNULL(**NULL**,10);
  
->   10
  
**MySQL**>   SELECT   IFNULL(1/0,10);
  
->   10
  
**MySQL**>   SELECT
  
IFNULL(1/0,'yes');

->   'yes'

IFNULL(expr1,expr2)的默认结果值为两个表达式中更加"通用"的一个,顺序为STRING、   REAL或
  
INTEGER。假设一个基于表达式的表的情况,     或**MySQL**必须在内存储器中储存一个临时表中IFNULL()的返回值: 
  
CREATE   TABLE   tmp   SELECT   IFNULL(1,'test')   AS   test；
  
在这个例子中,测试列的类型为   CHAR(4)。
  
**NULLIF(expr1,expr2)  的用法:   **
  
如果expr1
  
=   expr2     成立,那么返回值为**NULL**,否则返回值为   expr1。这和CASE   WHEN   expr1   =   expr2
  
THEN   **NULL**   ELSE   expr1   END相同。
  
**MySQL**>   SELECT
  
NULLIF(1,1);

->   **NULL**
  
**MySQL**>   SELECT   NULLIF(1,2);
  
->   1
  
如果参数不相等,则   **MySQL**   两次求得的值为     expr1   。

http://www.cnblogs.com/JuneZhang/archive/2010/08/26/1809306.html