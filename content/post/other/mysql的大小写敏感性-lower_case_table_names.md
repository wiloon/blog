---
title: MySQL的大小写敏感性 lower_case_table_names
author: "-"
date: 2014-04-09T02:10:43+00:00
url: /?p=6491
categories:
  - Inbox
tags:
  - MySQL

---
## MySQL的大小写敏感性 lower_case_table_names

MySQL的大小写敏感性 lower_case_table_names

在 MySQL 中，数据库和表对就于那些目录下的目录和文件。因而，操作系统的敏感性决定数据库和表命名的大小写敏感。这就意味着数据库和表名在 Windows 中是大小写不敏感的，而在大多数类型的 Unix 系统中是大小写敏感的。

奇怪的是列名与列的别名在所有的情况下均是忽略大小写的，而表的别名又是区分大小写的。

要避免这个问题，你最好在定义数据库命名规则的时候就全部采用小写字母加下划线的组合，而不使用任何的大写字母。

或者也可以强制以 -O lower_case_table_names=1 参数启动 MySQLd (如果使用 -defaults-file=...\my.cnf 参数来读取指定的配置文件启动 MySQLd 的话，你需要在配置文件的 [MySQLd] 区段下增加一行 lower_case_table_names=1) 。这样MySQL 将在创建与查找时将所有的表名自动转换为小写字符 (这个选项缺省地在 Windows 中为 1 ，在 Unix 中为 0。从 MySQL 4.0.2 开始，这个选项同样适用于数据库名) 。

当你更改这个选项时，你必须在启动 MySQLd 前首先将老的表名转换为小写字母。

换句话说，如果你希望在数据库里面创建表的时候保留大小写字符状态，则应该把这个参数置:  lower_case_table_names=0 。否则的话你会发现同样的sqldump脚本在不同的操作系统下最终导入的结果不一样 (在Windows下所有的大写字符都变成小写了) 。

      值
    
    
    
      含义
    
  
  
  
    
    
    
    
      使用CREATE TABLE或CREATE DATABASE语句指定的大写和小写在硬盘上保存表名和数据库名。名称比较对大小写敏感。在Unix系统中的默认设置即如此。请注意如果在大小写不敏感的文件系统上用-lower-case-table-names=0强制设为0，并且使用不同的大小写访问MyISAM表名，会导致索引破坏。
    
  
  
  
    
      1
    
    
    
      表名在硬盘上以小写保存，名称比较对大小写敏感。MySQL将所有表名转换为小写以便存储和查找。该行为也适合数据库名和表的别名。该值为Windows和Mac OS X系统中的默认值。
    
  
  
  
    
      2
    
    
    
      表名和数据库名在硬盘上使用CREATE TABLE或CREATE DATABASE语句指定的大小写进行保存，但MySQL将它们转换为小写以便查找。名称比较对大小写敏感。注释:  只 在对大小写不敏感的文件系统上适用! InnoDB表名以小写保存，例如lower_case_tables_name=1。

MySQL的大小写敏感其实是根据用户的操作系统来的， 可以强制以 -O lower_case_table_names=1 参数启动 MySQLd (如果使用 -defaults-file=...\\my.cnf 参数来读取指定的配置文件启动 MySQLd 的话，你需要在配置文件的 [MySQLd] 区段下增加一行 lower_case_table_names=1) 。
  
这样MySQL 将在创建与查找时将所有的表名自动转换为小写字符 (这个选项缺省地在 Windows 中为 1 ，在 Unix 中为 0。从 MySQL 4.0.2 开始，这个选项同样适用于数据库名) 。
  
当你更改这个选项时，你必须在启动 MySQLd 前首先将老的表名转换为小写字母。
  
换句话说，如果你希望在数据库里面创建表的时候保留大小写字符状态，则应该把这个参数置0:  lower_case_table_names=1 。
  
否则的话你会发现同样的sqldump脚本在不同的操作系统下最终导入的结果不一样 (在Windows下所有的大写字符都变成小写了) 。
  
注意:
  
在Win32上，尽管数据库和表名是忽略MySQL大小写的，你不应该在同一个查询中使用不同的大小写来引用一个给定的数据库和表。下列查询将不工作，因为它作为my_table和作为MY_TABLE引用一个表:
  
代码如下 复制代码
  
1.MySQL> SELECT * FROM my_table WHERE MY_TABLE.col=1;
  
2. 列名
  
列名在所有情况下都是忽略大小写的。
  
3. 表的别名
  
表的别名是区分大小写的。下列查询将不工作，: 因为它用a和A引用别名:
  
代码如下 复制代码
  
1.MySQL> SELECT col_name FROM tbl_name AS a
  
2.WHERE a.col_name = 1 OR A.col_name = 2;
  
4. 列的别名
  
列的别名是忽略大小写的。
  
5. 字符串比较和模式匹配
  
缺省地，MySQL搜索是大小写不敏感的(尽管有一些字符集从来不是忽略MySQL大小写的，例如捷克语)。这意味着，如果你用col_name LIKE 'a%'搜寻，你将得到所有以A或a开始的列值。如果你想要使这个搜索大小写敏感，使用象INDEX(col_name, "A")=0检查一个前缀。或如果列值必须确切是"A"，使用STRCMP(col_name, "A") = 0。
  
简单的比较操作(>=、>、= 、< 、<=、排序和聚合)是基于每个字符的"排序值"。有同样排序值的字符(象E，e)被视为相同的字符!
  
LIKE比较在每个字符的大写值上进行("E"="e")。
  
如果你想要一个列总是被当作MySQL大小写敏感的方式，声明它为BINARY。
  
例如:
  
代码如下 复制代码

1.MySQL> SELECT "E"="e","E"=BINARY "e";
  
2.+---+------+| "E"="e" | "E"=BINARY "e"
  
|+---+------+| 1 | 0 |+---+------+
  
MySQL大小写

<http://www.111cn.net/database/MySQL/44937.htm>

<http://fygh6318.blog.51cto.com/390568/385507>

<http://blog.chinaunix.net/uid-26602509-id-4104999.html>
