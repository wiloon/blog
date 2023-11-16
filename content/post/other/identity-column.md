---
title: IDENTITY COLUMN
author: "-"
date: 2013-07-10T07:28:46+00:00
url: /?p=5632
categories:
  - Inbox
tags:
  - reprint
---
## IDENTITY COLUMN
一、标识列的定义以及特点

SQL Server中的标识列又称标识符列,习惯上又叫自增列。
  
该种列具有以下三种特点: 

1. 列的数据类型为不带小数的数值类型
  
2. 在进行插入(Insert)操作时,该列的值是由系统按一定规律生成,不允许空值
  
3. 列值不重复,具有标识表中每一行的作用,每个表只能有一个标识列。

由于以上特点,使得标识列在数据库的设计中得到广泛的使用。

二、标识列的组成
  
创建一个标识列,通常要指定三个内容:
  
1. 类型 (type) 
  
在SQL Server 2000中,标识列类型必须是数值类型,如下: 
  
decimal、int、numeric、smallint、bigint 、tinyint
  
其中要注意的是,当选择decimal和numeric时,小数位数必须为零
  
另外还要注意每种数据类型所有表示的数值范围

2. 种子(seed)
  
是指派给表中第一行的值,默认为1

3. 递增量(increment)
  
相邻两个标识值之间的增量,默认为1。

三、标识列的创建与修改
  
标识列的创建与修改,通常在企业管理器和用Transact-SQL语句都可实现,使用企业管理管理器比较简单,请参考SQL Server的联机帮助,这

里只讨论使用Transact-SQL的方法

1. 创建表时指定标识列
  
标识列可用 IDENTITY 属性建立,因此在SQL Server中,又称标识列为具有IDENTITY属性的列或IDENTITY列。
  
下面的例子创建一个包含名为ID,类型为int,种子为1,递增量为1的标识列
  
CREATE TABLE T_test
  
(ID int IDENTITY(1,1),
  
Name varchar(50)
  
)

2. 在现有表中添加标识列
  
下面的例子向表T_test中添加一个名为ID,类型为int,种子为1,递增量为1的标识列
  
-创建表
  
CREATE TABLE T_test
  
(Name varchar(50)
  
)

-插入数据
  
INSERT T_test(Name) VALUES('张三')

-增加标识列
  
ALTER TABLE T_test
  
ADD ID int IDENTITY(1,1)

3. 判段一个表是否具有标识列

可以使用 OBJECTPROPERTY 函数确定一个表是否具有 IDENTITY (标识) 列,用法:
  
Select OBJECTPROPERTY(OBJECT_ID('表名'),'TableHasIdentity')
  
如果有,则返回1,否则返回0

4. 判断某列是否是标识列

可使用 COLUMNPROPERTY 函数确定 某列是否具有IDENTITY 属性,用法
  
SELECT COLUMNPROPERTY( OBJECT_ID('表名'),'列名','IsIdentity')
  
如果该列为标识列,则返回1,否则返回0

4. 查询某表标识列的列名
  
SQL Server中没有现成的函数实现此功能,实现的SQL语句如下
  
SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns
  
WHERE TABLE_NAME='表名' AND  COLUMNPROPERTY(
  
OBJECT_ID('表名'),COLUMN_NAME,'IsIdentity')=1

5. 标识列的引用

如果在SQL语句中引用标识列,可用关键字IDENTITYCOL代替
  
例如,若要查询上例中ID等于1的行,
  
以下两条查询语句是等价的
  
SELECT * FROM T_test WHERE IDENTITYCOL=1
  
SELECT * FROM T_test WHERE ID=1

6. 获取标识列的种子值

可使用函数IDENT_SEED,用法: 
  
SELECT IDENT_SEED ('表名')

7. 获取标识列的递增量

可使用函数IDENT_INCR ,用法: 
  
SELECT IDENT_INCR('表名')

8. 获取指定表中最后生成的标识值

可使用函数IDENT_CURRENT,用法:
  
SELECT IDENT_CURRENT('表名')
  
注意事项: 当包含标识列的表刚刚创建,为经过任何插入操作时,使用IDENT_CURRENT函数得到的值为标识列的种子值,这一点在开发数据库应用程序的时候尤其应该注意。

9.[SQL Server]关于标识列从1开始计数的问题
  
在SQL Server中,  我们有时需要在清空数据表之后,重新添加记录时,标识列重新从1开始计数。
  
我们只需要在插入记录之前,执行下面的命令: 
  
DBCC CHECKIDENT (表名,  RESEED, 0)
  
执行 TRUNCATE TABLE 也可以做到,而且效率高因为:

用delete将会把每个操作记录到日志中,所以效率低 ,truncate table则一次过,效率快很多。
  
但是,Truncate Table有限制,比如说这个标识列是另外一个表的外键,而且标识列当前值为1,插入行从2开始,

而DBCC CHECKIDENT (表名, RESEED, 0)可以用于即使有外键的情况下。

[http://bingdian2001.blog.hexun.com/33157398_d.html](http://bingdian2001.blog.hexun.com/33157398_d.html)