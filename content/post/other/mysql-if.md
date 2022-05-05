---
title: MySQL if
author: "-"
date: 2014-01-16T05:04:33+00:00
url: mysql/if
categories:
  - Uncategorized
tags:
  - MySQL

---
## MySQL if
### IF表达式
`IF(expr1,expr2,expr3)`

如果 expr1 是TRUE (expr1 <> 0 and expr1 <> NULL)，则 IF()的返回值为expr2; 否则返回值则为 expr3。IF() 的返回值为数字值或字符串值，具体情况视其所在语境而定。
```sql
select *,if(sva=1,"男","女") as ssva from taname where sva != ""
```

## 作为表达式的if也可以用CASE when来实现: 
```sql
select CASE sva WHEN 1 THEN '男' ELSE '女' END as ssva from taname where sva != ''
```

在第一个方案的返回结果中， value=compare-value 而第二个方案的返回结果是第一种情况的真实结果。如果没有匹配的结果值，则返回结果为ELSE后的结果，如果没有ELSE 部分，则返回值为 NULL。
 
```sql
SELECT CASE 1 WHEN 1 THEN 'one'
  WHEN 2 THEN 'two' 
   ELSE 'more' END
as testCol
-- 将输出one
```


http://outofmemory.cn/code-snippet/1149/MySQL-if-case-statement-usage-summary