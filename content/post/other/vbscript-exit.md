---
title: MySQL index
author: "-"
date: 2012-03-01T10:37:42+00:00
url: /?p=2511
categories:
  - Development
tags:
  - reprint
---
## MySQL index
http://book.51cto.com/art/201012/240956.htm


7.2  创建索引

创建索引是指在某个表的一列或多列上建立一个索引，以便提高对表的访问速度。创建索引有3种方式，这3种方式分别是创建表的时候创建索引、在已经存在的表上创建索引和使用ALTER TABLE语句来创建索引。本节将详细讲解这3种创建索引的方法。

7.2.1  创建表的时候创建索引 (1) 

创建表时可以直接创建索引，这种方式最简单、方便。其基本形式如下: 

CREATE TABLE  表名 ( 属性名 数据类型 [完整性约束条件],
  
属性名 数据类型 [完整性约束条件],
  
......
  
属性名 数据类型
  
[ UNIQUE | FULLTEXT | SPATIAL ]  INDEX | KEY
  
[ 别名 ]  ( 属性名1  [(长度)]  [ ASC | DESC] )
  
);
  
其中，UNIQUE是可选参数，表示索引为唯一性索引；FULLTEXT是可选参数，表示索引为全文索引；SPATIAL也是可选参数，表示索引为空间索引；INDEX和KEY参数用来指定字段为索引的，两者选择其中之一就可以了，作用是一样的；"别名"是可选参数，用来给创建的索引取的新名称；"属性1"参数指定索引对应的字段的名称，该字段必须为前面定义好的字段；"长度"是可选参数，其指索引的长度，必须是字符串类型才可以使用；"ASC"和"DESC"都是可选参数，"ASC"参数表示升序排列，"DESC"参数表示降序排列。

1．创建普通索引

创建一个普通索引时，不需要加任何UNIQUE、FULLTEXT或者SPATIAL参数。

【示例7-1】 下面创建一个表名为index1的表，在表中的id字段上建立索引。SQL代码如下: 

CREATE  TABLE  index1 (id    INT ,
  
name   VARCHAR(20) ,
  
sex    BOOLEAN ,
  
INDEX ( id)
  
);
  
运行结果显示创建成功，使用SHOW CREATE TABLE语句查看表的结构。显示如下: 

MySQL> SHOW CREATE TABLE index1 \G
  
\***\***\***\***\***\***\***\***\*\\*\* 1. row \*\*\***\***\***\***\***\***\***\****
  
Table: index1
  
Create Table: CREATE TABLE \`index1\` (
  
\`id\` int(11) DEFAULT NULL,
  
\`name\` varchar(20) DEFAULT NULL,
  
\`sex\` tinyint(1) DEFAULT NULL,
  
KEY \`index1_id\` (\`id\`)
  
) ENGINE=InnoDB DEFAULT CHARSET=utf8
  
1 row in set (0.00 sec)
  
结果可以看到，id字段上已经建立了一个名为index1_id的索引。使用EXPLAIN语句可以查看索引是否被使用，SQL代码如下: 

MySQL> EXPLAIN SELECT * FROM index1 where id=1 \G
  
\***\***\***\***\***\***\***\***\*\\*\* 1. row \*\*\***\***\***\***\***\***\***\****
  
id: 1
  
select_type: SIMPLE
  
table: index1
  
type: ref
  
possible_keys: index1_id
  
key: index1_id
  
key_len: 5
  
ref: const
  
rows: 1
  
Extra:
  
1 row in set (0.00 sec)
  
上面结果显示，possible_keys和key处的值都为index1_id。说明index1_id索引已经存在，而且已经开始起作用。

2．创建唯一性索引

创建唯一性索引时，需要使用UNIQUE参数进行约束。

【示例7-2】 下面创建一个表名为index2的表，在表中的id字段上建立名为index2_id的唯一性索引，且以升序的形式排列。SQL代码如下: 

CREATE  TABLE  index2 (id    INT  UNIQUE ,
  
name   VARCHAR(20) ,
  
UNIQUE  INDEX  index2_id ( id  ASC)
  
);
  
运行结果显示创建成功，使用SHOW CREATE TABLE语句查看表的结构。显示如下: 

MySQL> SHOW CREATE TABLE index2 \G
  
\***\***\***\***\***\***\***\***\*\\*\* 1. row \*\*\***\***\***\***\***\***\***\****
  
Table: index2
  
Create Table: CREATE TABLE \`index2\` (
  
\`id\` int(11) DEFAULT NULL,
  
\`name\` varchar(20) DEFAULT NULL,
  
UNIQUE KEY \`id\` (\`id\`),
  
UNIQUE KEY \`index2_id\` (\`id\`)
  
) ENGINE=InnoDB DEFAULT CHARSET=utf8
  
1 row in set (0.00 sec)
  
结果可以看到，id字段上已经建立了一个名为index2_id的唯一性索引。这里的id字段可以没有进行唯一性约束，也可以在该字段上成功创建唯一性索引。但是，这样可能达不到提高查询速度的目的。