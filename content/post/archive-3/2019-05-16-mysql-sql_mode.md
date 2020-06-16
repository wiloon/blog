---
title: mysql, sql_mode
author: wiloon
type: post
date: 2019-05-16T05:26:24+00:00
url: /?p=14344
categories:
  - Uncategorized

---
http://xstarcd.github.io/wiki/MySQL/MySQL-sql-mode.html

mysql的sql_mode合理设置
  
目录
  
http://dev.mysql.com/doc/refman/5.7/en/sql-mode.html
  
http://blog.csdn.net/wyzxg/article/details/8787878
  
当前sql-mode设置
  
查看当前sql-mode
  
1
  
2
  
SELECT @@GLOBAL.sql_mode;
  
SELECT @@SESSION.sql_mode;
  
mysql> SELECT @@GLOBAL.sql_mode;
  
+--------------&#8211;+
  
| @@GLOBAL.sql_mode |
  
+--------------&#8211;+
  
| STRICT\_TRANS\_TABLES,NO\_ENGINE\_SUBSTITUTION |
  
+--------------&#8211;+
  
1 row in set (0.00 sec)

mysql> SELECT @@SESSION.sql_mode;
  
+--------------&#8211;+
  
| @@SESSION.sql_mode |
  
+--------------&#8211;+
  
| STRICT\_TRANS\_TABLES,NO\_ENGINE\_SUBSTITUTION |
  
+--------------&#8211;+
  
1 row in set (0.00 sec)
  
设置当前sql-mode
  
1
  
2
  
SET GLOBAL sql_mode = 'modes&#8230;';
  
SET SESSION sql_mode = 'modes&#8230;';
  
my.cnf中配置sql-mode
  
1
  
2
  
3
  
4
  
[mysqld]
  
#set the SQL mode to strict
  
#sql-mode="modes&#8230;"
  
sql-mode = "STRICT\_TRANS\_TABLES,NO\_AUTO\_CREATE\_USER,NO\_ENGINE_SUBSTITUTION"
  
sql_mode常用值
  
ONLY\_FULL\_GROUP_BY：
  
对于GROUP BY聚合操作，如果在SELECT中的列，没有在GROUP BY中出现，那么这个SQL是不合法的，因为列不在GROUP BY从句中

NO\_AUTO\_VALUE\_ON\_ZERO：
  
该值影响自增长列的插入。默认设置下，插入0或NULL代表生成下一个自增长值。如果用户 希望插入的值为0，而该列又是自增长的，那么这个选项就有用了。

STRICT\_TRANS\_TABLES：
  
在该模式下，如果一个值不能插入到一个事务表中，则中断当前的操作，对非事务表不做限制

NO\_ZERO\_IN_DATE：
  
在严格模式下，不允许日期和月份为零

NO\_ZERO\_DATE：
  
设置该值，mysql数据库不允许插入零日期，插入零日期会抛出错误而不是警告。

ERROR\_FOR\_DIVISION\_BY\_ZERO：
  
在INSERT或UPDATE过程中，如果数据被零除，则产生错误而非警告。如 果未给出该模式，那么数据被零除时MySQL返回NULL

NO\_AUTO\_CREATE_USER：
  
禁止GRANT创建密码为空的用户

NO\_ENGINE\_SUBSTITUTION：
  
如果需要的存储引擎被禁用或未编译，那么抛出错误。不设置此值时，用默认的存储引擎替代，并抛出一个异常

PIPES\_AS\_CONCAT：
  
将"||"视为字符串的连接操作符而非或运算符，这和Oracle数据库是一样的，也和字符串的拼接函数Concat相类似
  
ANSI_QUOTES：
  
启用ANSI_QUOTES后，不能用双引号来引用字符串，因为它被解释为识别符

ORACLE的sql\_mode设置等同：PIPES\_AS\_CONCAT, ANSI\_QUOTES, IGNORE\_SPACE, NO\_KEY\_OPTIONS, NO\_TABLE\_OPTIONS, NO\_FIELD\_OPTIONS, NO\_AUTO\_CREATE\_USER.

如果使用mysql，为了继续保留大家使用oracle的习惯，可以对mysql的sql_mode设置如下：在my.cnf添加如下配置

[mysqld]
  
sql\_mode='ONLY\_FULL\_GROUP\_BY,NO\_AUTO\_VALUE\_ON\_ZERO,STRICT\_TRANS\_TABLES,NO\_ZERO\_IN\_DATE,NO\_ZERO_DATE,
  
ERROR\_FOR\_DIVISION\_BY\_ZERO,NO\_AUTO\_CREATE\_USER,NO\_ENGINE_SUBSTITU