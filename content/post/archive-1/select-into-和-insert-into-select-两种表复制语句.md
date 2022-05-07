---
title: SELECT INTO 和 INSERT INTO SELECT 两种表复制语句
author: "-"
date: 2013-07-22T07:53:38+00:00
url: /?p=5692
categories:
  - DataBase

tags:
  - reprint
---
## SELECT INTO 和 INSERT INTO SELECT 两种表复制语句

Insert是T-sql中常用语句，Insert INTO table(field1,field2,...) values(value1,value2,...)这种形式的在应用程序开发中必不可少。但我们在开发、测试过程中，经常会遇到需要表复制的情况，如将一个table1的数据的部分字段复制到table2中，或者将整个table1复制到table2中，这时候我们就要使用SELECT INTO 和 INSERT INTO SELECT 表复制语句了。

1.INSERT INTO SELECT语句

语句形式为: Insert into Table2(field1,field2,...) select value1,value2,... from Table1

要求目标表Table2必须存在，由于目标表Table2已经存在，所以我们除了插入源表Table1的字段外，还可以插入常量。示例如下:

-1.创建测试表

create TABLE Table1

(

a varchar(10),

b varchar(10),

c varchar(10),

CONSTRAINT [PK_Table1] PRIMARY KEY CLUSTERED

(

a ASC

)

) ON [PRIMARY]

create TABLE Table2

(

a varchar(10),

c varchar(10),

d int,

CONSTRAINT [PK_Table2] PRIMARY KEY CLUSTERED

(

a ASC

)

) ON [PRIMARY]

GO

-2.创建测试数据

Insert into Table1 values('赵','asds','90')

Insert into Table1 values('钱','asds','100')

Insert into Table1 values('孙','asds','80')

Insert into Table1 values('李','asds',null)

GO

select * from Table2

-3.INSERT INTO SELECT语句复制表数据

Insert into Table2(a, c, d) select a,c,5 from Table1

GO

-4.显示更新后的结果

select * from Table2

GO

-5.删除测试表

drop TABLE Table1

drop TABLE Table2

2.SELECT INTO FROM语句

语句形式为: SELECT vale1, value2 into Table2 from Table1

要求目标表Table2不存在，因为在插入时会自动创建表Table2，并将Table1中指定字段数据复制到Table2中。示例如下:

-1.创建测试表

create TABLE Table1

(

a varchar(10),

b varchar(10),

c varchar(10),

CONSTRAINT [PK_Table1] PRIMARY KEY CLUSTERED

(

a ASC

)

) ON [PRIMARY]

GO

-2.创建测试数据

Insert into Table1 values('赵','asds','90')

Insert into Table1 values('钱','asds','100')

Insert into Table1 values('孙','asds','80')

Insert into Table1 values('李','asds',null)

GO

-3.SELECT INTO FROM语句创建表Table2并复制数据

select a,c INTO Table2 from Table1

GO

-4.显示更新后的结果

select * from Table2

GO

-5.删除测试表

drop TABLE Table1

drop TABLE Table2
