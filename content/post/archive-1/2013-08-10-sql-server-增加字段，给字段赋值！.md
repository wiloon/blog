---
title: SQL server 增加字段，给字段赋值！
author: wiloon
type: post
date: 2013-08-10T10:36:45+00:00
url: /?p=5772
categories:
  - DataBase

---
2修改数据库和表的字符集
  
alter database maildb default character set utf8;//修改数据库的字符集
  
alter table mailtable default character set utf8;//修改表的字符集

增加字段
  
ALTER TABLE wap\_lenovo\_bookmark ADD free BIT NOT NULL DEFAULT 0

alter table MemailNodeDefine add action varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL default 'admin';

给一个字段赋值
  
UPDATE "表格名" SET "栏位1" = [新值] WHERE {条件}

UPDATE wap\_lenovo\_bookmark set type = 'other'

ALTER TABLE wap\_lenovo\_bookmark ADD groupid INT NOT NULL DEFAULT 0

mysql 修改字段
  
alter   table   employee   change   column   employeeID   empID   int;

修改
  
ALTER   TABLE   TableName   CHANGE   Field\_name\_tobe\_change   new\_Name   VARCHAR   (32);
  
删除
  
ALTER   TABLE   TableName   DROP   Field\_name\_tobe_delete
  
重命名
  
ALTER   TABLE   TableName   rename   as   newTableName

alter   table   语句好像不能对表实行字段删除操作，可以用create   table   tablename(field1,field2,field3&#8230;&#8230;)   (select   field1,field2,field3&#8230;&#8230;from   orgtablename);
  
或者用ALTER   TABLE   TableName   DROP   [COLUMN]   col_name；
  
---------------------
  
mysql alter 语句用法,添加、修改、删除字段等

//主键549830479

alter table tabelname add new\_field\_id int(5) unsigned default 0 not null auto\_increment ,add primary key (new\_field_id);
  
//增加一个新列549830479

alter table t2 add d timestamp;
  
alter table infos add ex tinyint not null default '0';
  
//删除列549830479

alter table t2 drop column c;
  
//重命名列549830479

alter table t1 change a b integer;

//改变列的类型549830479

alter table t1 change b b bigint not null;
  
alter table infos change list list tinyint not null default '0';

//重命名表549830479

alter table t1 rename t2;
  
加索引549830479

mysql> alter table tablename change depno depno int(5) not null;
  
mysql> alter table tablename add index 索引名 (字段名1[，字段名2 …]);
  
mysql> alter table tablename add index emp_name (name);
  
加主关键字的索引549830479

mysql> alter table tablename add primary key(id);
  
加唯一限制条件的索引549830479

mysql> alter table tablename add unique emp_name2(cardnumber);
  
删除某个索引549830479

mysql>alter table tablename drop index emp_name;
  
修改表：549830479

增加字段：549830479

mysql> ALTER TABLE table\_name ADD field\_name field_type;
  
修改原字段名称及类型：549830479

mysql> ALTER TABLE table\_name CHANGE old\_field\_name new\_field\_name field\_type;
  
删除字段：549830479

mysql> ALTER TABLE table\_name DROP field\_name;