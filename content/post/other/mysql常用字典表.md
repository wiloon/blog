---
title: MySQL 字典表
author: "-"
date: 2015-05-25T08:29:18+00:00
url: /?p=7710
categories:
  - Uncategorized
tags:
  - MySQL

---
## MySQL 字典表

```sql
select column_key,COLUMN_NAME,column_type,is_nullable,column_comment from INFORMATION_SCHEMA.Columns where
 table_name=" and table_schema="
```
  
### 显示数据库列表
```sql
MySQL>show databases;
-- 说明: 其中字典库是: information_schema，其中常用字典表: 
INFORMATION_SCHEMA.SCHEMATA  -数据库中所有数据库信息
INFORMATION_SCHEMA.TABLES  -存放数据库中所有数据库表信息
INFORMATION_SCHEMA.COLUMNS  -所有数据库表的列信息
INFORMATION_SCHEMA.STATISTICS  -存放索引信息
INFORMATION_SCHEMA.USER_PRIVILEGES  -
INFORMATION_SCHEMA.SCHEMA_PRIVILEGES
INFORMATION_SCHEMA.TABLE_PRIVILEGES
INFORMATION_SCHEMA.COLUMN_PRIVILEGES
INFORMATION_SCHEMA.CHARACTER_SETS
INFORMATION_SCHEMA.COLLATIONS
INFORMATION_SCHEMA.COLLATION_CHARACTER_SET_APPLICABILITY
INFORMATION_SCHEMA.TABLE_CONSTRAINTS
INFORMATION_SCHEMA.KEY_COLUMN_USAGE -存放数据库里所有具有约束的键信息
INFORMATION_SCHEMA.ROUTINES
INFORMATION_SCHEMA.VIEWS  -存放所有视图信息
INFORMATION_SCHEMA.TRIGGERS  -触发器信息
```
    
    
    
      2、显示当前连接的数据库
 MySQL>select database();
    
    
    
      3、显示库中的数据表: 
 MySQL>use MySQL；(指定MySQL库)
 MySQL>show tables;
    
    
    
      4、显示数据表的结构: 
 MySQL>describe yourtablename;
 说明: describe 可以简写成desc
    
    
    
      5、建库: 
 MySQL>create database yourdbname;
    
    
    
      6、建表: 
 MySQL>create table yourtablename (columnname colunmtype, ...)；
    
    
    
      6、删库和删表:
 MySQL>drop database yourdbname;
 MySQL>drop table yourtablename；
    
    
    
      7、退出
 MySQL>exit
 或
 MySQL>quit
    
    
    
      8、连接数据库
 MySQL -h主机地址 -u用户名 -p密码
 如: 
 C:\Users\Administrator>MySQL -hlocalhost -uroot -proot
 Welcome to the MySQL monitor.  Commands end with ; or \g.
 Your MySQL connection id is 7
 Server version: 5.5.17 MySQL Community Server (GPL)
    
    
    
      Copyright (c) 2000, 2011, Oracle and/or its affiliates. All rights reserved.
    
    
    
      Oracle is a registered trademark of Oracle Corporation and/or its
 affiliates. Other names may be trademarks of their respective
 owners.
    
    
    
      Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
 MySQL>
    
    
    
      
    
    
    
      9、字段类型
 1．INT[(M)] 型:  正常大小整数类型
 2．DOUBLE[(M,D)] [ZEROFILL] 型:  正常大小(双精密)浮点数字类型
 3．DATE 日期类型: 支持的范围是1000-01-01到9999-12-31。MySQL以YYYY-MM-DD格式来显示DATE值，但是允许你使用字符串或数字把值赋给DATE列
 4．CHAR(M) 型: 定长字符串类型，当存储时，总是是用空格填满右边到指定的长度
 5．BLOB TEXT类型，最大长度为65535(2^16-1)个字符。
 6．VARCHAR型: 变长字符串类型
    
    
    
      
    
    
    
      10、启用、禁用外键约束
    
    
    
      SET FOREIGN_KEY_CHECKS='OFF';
 SET FOREIGN_KEY_CHECKS='ON';
    
    
    
      
    
    
    
      11、显示建表SQL
    
    
    
      SHOW CREATE TABLE  
    
    
    
      
    
    
    
      12、显示当前数据库版本
    
    
    
      select version();
    
    
    
      
    
    
    
      13、显示当前登录用户
    
    
    
      select user();
    
    
    
      
    
    
    
      14、查看指定表的索引信息
    
    
    
      SHOW INDEX FROM 表名称
    
    
    
      
    
    
    
      补充说明: MySQL5中，关于索引的字典表是STATISTICS，其中列COLLATION表示索引的排序方式，值有2种，A表示升序，NULL表示无分类。MySQL5中，索引存储的排序方式是ASC的，没有DESC的索引。虽然索引是ASC的，但是也可以反向进行检索，就相当于DESC了。如果您在ORDER BY 语句中使用了 DESC排序，MySQL确实会反向进行检索。在理论上，反向检索与正向检索的速度一样的快。但是在某些操作系统上面，并不支持反向的read-ahead预读，所以反向检索会略慢。由于设计的原因，在myisam引擎中，反向的检索速度比正向检索要慢得多。
    
    
    
      
    
    
    
      
    
    
    
      其他
    
    
    
      1、CREATE table cc_weibo_bak (select * from cc_weibo)
    
    
    
      2、INSERT into cc_weibo_bak(uid,content) select uid ,concat('hello1 ',nick_name) from uc_users;
    
    
    
      3、select  fid  ,count(fid) as fans_count from uc_follow where fid in(select uid from uc_users where user_type=22) group by fid order by fans_count desc ;
    
    
    
      4、show full processlist
    
    
    
      5、SHOW STATUS
    
    
    
      
  

http://huangqiqing123.iteye.com/blog/1465990