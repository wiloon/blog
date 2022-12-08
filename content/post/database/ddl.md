---
title: Database – DDL,DML,DCL,TCL
author: "-"
date: 2012-07-01T09:20:48+00:00
url: /?p=3712
categories:
  - DataBase
tags:
  - Database

---
## Database – DDL,DML,DCL,TCL
### DDL (Data Definition Language) 

数据库定义语言statements are used to define the database structure or schema.

DDL是SQL语言的四大功能之一。
  
用于定义数据库的三级结构，包括外模式、概念模式、内模式及其相互之间的映像，定义数据的完整性、安全控制等约束
  
DDL不需要commit.
  
CREATE
  
ALTER
  
DROP
  
TRUNCATE
  
COMMENT
  
RENAME

### DML (Data Manipulation Language) 

数据操纵语言statements are used for managing data within schema objects.

由DBMS提供，用于让用户或程序员使用，实现对数据库中数据的操作。
  
DML分成交互型DML和嵌入型DML两类。
  
依据语言的级别，DML又可分成过程性DML和非过程性DML两种。
  
需要commit.
  
SELECT
  
INSERT
  
UPDATE
  
DELETE
  
MERGE
  
CALL
  
EXPLAIN PLAN
  
LOCK TABLE

3.DCL (Data Control Language) 
  
数据库控制语言 授权，角色控制等
  
GRANT 授权
  
REVOKE 取消授权

4.TCL (Transaction Control Language) 
  
事务控制语言
  
SAVEPOINT 设置保存点
  
ROLLBACK 回滚
  
SET TRANSACTION

SQL主要分成四部分: 
  
 (1) 数据定义。 (SQL DDL) 用于定义SQL模式、基本表、视图和索引的创建和撤消操作。
  
 (2) 数据操纵。 (SQL DML) 数据操纵分成数据查询和数据更新两类。数据更新又分成插入、删除、和修改三种操作。
  
 (3) 数据控制。包括对基本表和视图的授权，完整性规则的描述，事务控制等内容。
  
 (4) 嵌入式SQL的使用规定。涉及到SQL语句嵌入在宿主语言程序中使用的规则。

1.数据定义语言

DDL

数据库模式定义语言DDL(Data Definition Language)，是用于描述数据库中要存储的现实世界实体的语言。一个数据库模式包含该数据库中所有实体的描述定义。这些定义包括结构定义、操作方法定义等。

数据库模式定义语言并非程序设计语言，DDL数据库模式定义语言是SQL语言 (结构化程序设计语言) 的组成部分。SQL语言包括三种主要程序设计语言类别的语句: 数据定义语言(DDL)，数据操作语言(DML)及数据控制语言(DCL)。

DDL描述的模式，必须由计算机软件进行编译，转换为便于计算机存储、查询和操纵的格式，完成这个转换工作的程序称为模式编译器。

模式编译器处理模式定义主要产生两种类型的数据: 数据字典以及数据类型和结构定义。

数据字典和数据库内部结构信息是创建该模式所对应的数据库的依据，根据这些信息创建每个数据库对应的逻辑结构；对数据库数据的访问、查询也根据模式信息决定数据存取的方式和类型，以及数据之间的关系和对数据的完整性约束。

数据字典是模式的内部信息表示，数据字典的存储方式对不同的DBMS各不相同。

数据类型和结构的定义，是指当应用程序与数据库连接操作时，应用程序需要了解产生和提取的数据类型和结构。是为各种宿主语言提供的用户工作区的数据类型和结构定义，使用户工作区和数据库的逻辑结构相一致，减少数据的转换过程，这种数据类型和结构的定义通常用一个头文件来实现。

数据库模式的定义通常有两种方式: 交互方式定义模式和通过数据描述语言DDL 描述文本定义模式。

常见的DDL语句

CREATE DATABASE

创建数据库

CREATE {DATABASE | SCHEMA} db_name

[create_specification [, create_specification] …]

create_specification:

[DEFAULT] CHARACTER SET charset_name

| [DEFAULT] COLLATE collation_name

CREATE TABLE

创建数据库表格

CREATE [TEMPORARY] TABLE tbl_name

[(create_definition,…)]

[table_options] [select_statement]

ALTER TABLE

修改数据库表格

ALTER TABLE tbl_name

alter_specification [, alter_specification] …

alter_specification:

ADD [COLUMN] column_definition [FIRST | AFTER col_name ]

| ADD [COLUMN] (column_definition,…)

| ADD INDEX (index_col_name,…)

| ADD [CONSTRAINT [symbol]]

PRIMARY KEY (index_col_name,…)

| ADD [CONSTRAINT [symbol]]

UNIQUE (index_col_name,…)

| ADD (index_col_name,…)

| ADD [CONSTRAINT [symbol]]

FOREIGN KEY (index_col_name,…)

[reference_definition]

| ALTER [COLUMN] col_name {SET DEFAULT literal | DROP DEFAULT}

| CHANGE [COLUMN] old_col_name column_definition

[FIRST|AFTER col_name]

| MODIFY [COLUMN] column_definition [FIRST | AFTER col_name]

| DROP [COLUMN] col_name

| DROP PRIMARY KEY

| DROP INDEX index_name

| DROP FOREIGN KEY fk_symbol

| DISABLE KEYS

| ENABLE KEYS

| RENAME [TO] new_tbl_name

| ORDER BY col_name

| CONVERT TO CHARACTER SET charset_name [COLLATE collation_name]

| [DEFAULT] CHARACTER SET charset_name [COLLATE collation_name]

| DISCARD TABLESPACE

| IMPORT TABLESPACE

| table_options

DROP TABLE

删除数据库表格

DROP [TEMPORARY] TABLE

tbl_name [, tbl_name] …

[RESTRICT | CASCADE]

CREATE VIEW

创建查询命令

CREATE [OR REPLACE] [ALGORITHM = {UNDEFINED | MERGE | TEMPTABLE}]

VIEW view_name [(column_list)]

AS select_statement

[WITH [CASCADED | LOCAL] CHECK OPTION]

ALTER VIEW

修改查询命令

ALTER [ALGORITHM = {UNDEFINED | MERGE | TEMPTABLE}]

VIEW view_name [(column_list)]

AS select_statement

[WITH [CASCADED | LOCAL] CHECK OPTION]

DROP VIEW

删除查询命令

DROP VIEW

view_name [, view_name] …

[RESTRICT | CASCADE]

TRUNCATE TABLE

删除数据表内容

TRUNCATE TABLE name [DROP/REUSE STORAGE]

DROP STORAGE: 显式指明释放数据表和索引的空间

REUSE STORAGE: 显式指明不释放数据表和索引的空间

## on update cascade 和on delete cascade 的作用

on update cascade 和on delete cascade是数据库外键定义的可选项，用来设置当主键表中的被参考列的数据发生变化时，外键表中相应字段的变换规则。
update 是主键表中被参考字段的值更新，delete是指在主键表中删除一条记录可对应如下四个选项：

no action ， set null ， set default ，cascade
1
no action 表示 不做任何操作；
set null 表示在外键表中将相应字段设置为null；
set default 表示设置为默认值；
cascade 表示级联操作，就是说，如果为on update cascade，主键表中被参考字段更新，外键表中对应行相应更新；如果为on delete cascade，主键表中的记录被删除，外键表中对应行相应删除。
————————————————
版权声明：本文为CSDN博主「lszzzz」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/lszzzz/article/details/50544287