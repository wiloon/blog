---
title: MySQL 实现 row_number() over(partition by) 分组排序功能
author: "-"
date: 2015-08-06T11:25:24.000+00:00
url: "/?p=8069"
categories:
- Uncategorized
tags:
  - reprint
---
## MySQL 实现 row_number() over(partition by) 分组排序功能

### mysql 8
MySQL ROW_NUMBER()从8.0版开始引入了功能。这ROW_NUMBER()是一个窗口函数或分析函数，它为从1开始应用的每一行分配一个序号。

### mysql 8 之前的替代方案

```sql
SELECT t.*,
       @rownum := @rownum + 1 AS rank
  FROM YOUR_TABLE t,
       (SELECT @rownum := 0) r
```

http://mrcelite.blog.51cto.com/2977858/745913

原创作品，允许转载，转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。http://mrcelite.blog.51cto.com/2977858/745913

由于MySQL没有提供类似ORACLE中OVER()这样丰富的分析函数. 所以在MySQL里需要实现这样的功能,我们只能用一些灵活的办法:

### 首先我们来创建实例数据:
```sql
drop table if exists c;

CREATE TABLE `heyf_t10` (
    `empid` INT(11) NULL DEFAULT NULL,
    `deptid` INT(11) NULL DEFAULT NULL,
    `line` DECIMAL(10,2) NULL DEFAULT NULL
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
;

INSERT INTO `heyf_t10` (`empid`, `deptid`, `line`) VALUES 
(1,10,5500.00),
(2,10,4500.00),
(3,20,1900.00),
(4,20,4800.00),
(5,40,6500.00),
(6,40,14500.00),
(7,40,44500.00),
(8,50,6500.00),
(9,50,7500.00);
```

### 确定需求: 根据部门来分组,显示各员工在部门里按薪水排名名次.

### 显示结果预期如下:
+-------+--------+----------+------+
| empid | deptid | line     | rank |
+-------+--------+----------+------+
|     1 |     10 |  5500.00 |    1 |
|     2 |     10 |  4500.00 |    2 |
|     3 |     20 |  1900.00 |    1 |
|     4 |     20 |  4800.00 |    2 |
|     5 |     40 |  6500.00 |    1 |
|     6 |     40 | 14500.00 |    2 |
|     7 |     40 | 44500.00 |    3 |
|     8 |     50 |  6500.00 |    1 |
|     9 |     50 |  7500.00 |    2 |
+-------+--------+----------+------+

### SQL 实现
```sql
SELECT empid,deptid,line,rank
FROM (
SELECT heyf_tmp.empid,heyf_tmp.deptid,heyf_tmp.line,@rownum:=@rownum+1,
 if(@pdept=heyf_tmp.deptid,@rank:=@rank+1,@rank:=1) AS rank,
 @pdept:=heyf_tmp.deptid
FROM (
SELECT empid,deptid,line
FROM heyf_t10
ORDER BY deptid ASC,line DESC
) heyf_tmp,(
SELECT @rownum :=0, @pdept := NULL,@rank:=0
) a 
) result
```

4\. 结果演示

MySQL> select empid,deptid,salary,rank from (

\-> select heyf_tmp.empid,heyf_tmp.deptid,heyf_tmp.salary,@rownum:=@rownum+1 ,

\-> if(@pdept=heyf_tmp.deptid,@rank:=@rank+1,@rank:=1) as rank,

\-> @pdept:=heyf_tmp.deptid

\-> from (

\-> select empid,deptid,salary from heyf_t10 order by deptid asc ,salary desc

\-> ) heyf_tmp ,(select @rownum :=0 , @pdept := null ,@rank:=0) a ) result

\-> ;

\+——-+——–+———-+——+

| empid | deptid | salary | rank |

\+——-+——–+———-+——+

| 1 | 10 | 5500.00 | 1 |

| 2 | 10 | 4500.00 | 2 |

| 4 | 20 | 4800.00 | 1 |

| 3 | 20 | 1900.00 | 2 |

| 7 | 40 | 44500.00 | 1 |

| 6 | 40 | 14500.00 | 2 |

| 5 | 40 | 6500.00 | 3 |

| 9 | 50 | 7500.00 | 1 |

| 8 | 50 | 6500.00 | 2 |

\+——-+——–+———-+——+

9 rows in set (0.00 sec)

MySQL中取出每个分组中的前N条记录

select a1.* from article a1

inner join

(select a.type,a.date from article a left join article b

on a.type=b.type and a.date<=b.date

group by a.type,a.date

having count(b.date)<=2

)b1

on a1.type=b1.type and a1.date=b1.date

order by a1.type,a1.date desc

>https://www.begtut.com/mysql/mysql-row-number-function.html