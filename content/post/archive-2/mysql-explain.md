---
title: MySQL explain, 执行计划, Query Execution Plan
author: "-"
date: 2016-11-28T02:24:33+00:00
url: /?p=9439
categories: 
  - database
tags:
  - reprint
---
## MySQL explain, 执行计划, Query Execution Plan

# 执行计划, Query Execution Plan, explain

关于explain命令相信大家并不陌生,具体用法和字段含义可以参考官网explain-output,这里需要强调rows是核心指标,绝大部分rows小的语句执行一定很快 (有例外,下面会讲到) 。所以优化语句基本上都是在优化rows。

在日常工作中,我们会有时会开慢查询去记录一些执行时间比较久的SQL语句,找出这些SQL语句并不意味着完事了,些时我们常常用到explain这个命令来查看一个这些SQL语句的执行计划,查看该SQL语句有没有使用上了索引,有没有做全表扫描,这都可以通过explain命令来查看。所以我们深入了解MySQL的基于开销的优化器,还可以获得很多可能被优化器考虑到的访问策略的细节,以及当运行SQL语句时哪种策略预计会被优化器采用。 (QEP: sql生成一个执行计划query Execution plan)
  
MySQL> explain select * from servers;
  
+—-+————-+———+——+—————+——+———+——+——+——-+
  
| id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra |
  
+—-+————-+———+——+—————+——+———+——+——+——-+
  
| 1 | SIMPLE | servers | ALL | NULL | NULL | NULL | NULL | 1 | NULL |
  
+—-+————-+———+——+—————+——+———+——+——+——-+
  
1 row in set (0.03 sec)

expain出来的信息有10列,分别是 id、select_type、table、type、possible_keys、key、key_len、ref、rows、Extra,下面对这些字段出现的可能进行解释:

### id

我的理解是SQL执行的顺序的标识,SQL从大到小的执行

1. id相同时,执行顺序由上至下
2. 如果是子查询,id的序号会递增,id值越大优先级越高,越先被执行
3. id如果相同,可以认为是一组,从上往下顺序执行；在所有组中,id值越大,优先级越高,越先执行

### select_type

示查询中每个select子句的类型

1. SIMPLE (简单SELECT,不使用UNION或子查询等)
2. PRIMARY (查询中若包含任何复杂的子部分, 最外层的select被标记为PRIMARY)
3. UNION (UNION中的第二个或后面的SELECT语句)
4. DEPENDENT UNION(UNION中的第二个或后面的SELECT语句,取决于外面的查询)
5. UNION RESULT(UNION的结果)
6. SUBQUERY(子查询中的第一个SELECT)
7. DEPENDENT SUBQUERY(子查询中的第一个SELECT,取决于外面的查询)
8. DERIVED(派生表的SELECT, FROM子句的子查询)
9. UNCACHEABLE SUBQUERY(一个子查询的结果不能被缓存,必须重新评估外链接的第一行)

### table

显示这一行的数据是关于哪张表的,有时不是真实的表名字,看到的是derivedx(x是个数字,我的理解是第几步执行的结果)
  
MySQL> explain select \* from (select \* from ( select * from t1 where id=2602) a) b;
  
    +—-+————-+————+——–+——————-+———+———+——+——+——-+
      
    | id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra |
      
    +—-+————-+————+——–+——————-+———+———+——+——+——-+
      
    | 1 | PRIMARY | <derived2> | system | NULL | NULL | NULL | NULL | 1 | |
      
    | 2 | DERIVED | <derived3> | system | NULL | NULL | NULL | NULL | 1 | |
      
    | 3 | DERIVED | t1 | const | PRIMARY,idx_t1_id | PRIMARY | 4 | | 1 | |
      
    +—-+————-+————+——–+——————-+———+———+——+——+——-+

### partitions

版本5.7以前,该项是explain partitions显示的选项,5.7以后成为了默认选项。该列显示的为分区表命中的分区情况。非分区表该字段为空 (null) 。

### type

表示MySQL在表中找到所需行的方式,又称"访问类型"。

依次从好到差:

    system, const, eq_ref, ref, fulltext, ref_or_null, index_merge, unique_subquery, index_subquery, range, index, ALL

除了all之外,其他的type都可以使用到索引,除了index_merge之外,其他的type只可以用到一个索引

- ALL: 这个就是全表扫描数据文件,然后再在server层进行过滤返回符合要求的记录。
- index: 索引全表扫描,把索引从头到尾扫一遍,常见于使用索引列就可以处理不需要读取数据文件的查询、可以使用索引排序或者分组的查询。
- index_merge: 表示查询使用了两个以上的索引,最后取交集或者并集,常见and, or的条件使用了不同的索引,官方排序这个在ref_or_null之后,但是实际上由于要读取所个索引,性能可能大部分时间都不如range
- range: 索引范围扫描,常见于使用>,<,is null,between ,in ,like等运算符的查询中。只检索给定范围的行,使用一个索引来选择行
- index_subquery: 用于in形式子查询使用到了辅助索引或者in常数列表,子查询可能返回重复值,可以使用索引将子查询去重。
- unique_subquery: 用于where中的in形式子查询,子查询返回不重复值唯一值
- ref_or_null: 与ref方法类似,只是增加了null值的比较。实际用的不多。
- fulltext: 全文索引检索,要注意,全文索引的优先级很高,若全文索引和普通索引同时存在时,MySQL不管代价,优先选择使用全文索引

#### ref

All rows with matching index values are read from this table for each combination of rows from the previous tables. ref is used if the join uses only a leftmost prefix of the key or if the key is not a PRIMARY KEY or UNIQUE index (in other words, if the join cannot select a single row based on the key value). If the key that is used matches only a few rows, this is a good join type.

第一句没理解透,先理解到多行匹配吧。

触发条件: 触发联合索引最左原则 (不知道的搜下) ,或者这个索引不是主键,也不是唯一索引 (换句话说,如果这个在这个索引基础之上查询的结果多于一行) 。

如果使用那个索引只匹配到非常少的行,也是不错的。

ref can be used for indexed columns that are compared using the = or <=> operator. In the following examples, MySQL can use a ref join to process ref_table:

在对已经建立索引列进行=或者<=>操作的时候,ref会被使用到。与eq_ref不同的是匹配到了多行

##### 根据索引 (非主键,非唯一索引) ,匹配到多行

SELECT * FROM ref_table WHERE key_column=expr;

##### 多表关联查询,单个索引,多行匹配

SELECT * FROM ref_table,other_table
  WHERE ref_table.key_column=other_table.column;

##### 多表关联查询,联合索引,多行匹配

SELECT * FROM ref_table,other_table
  WHERE ref_table.key_column_part1=other_table.column
  AND ref_table.key_column_part2=1;

#### eq_ref

One row is read from this table for each combination of rows from the previous tables. Other than the system and const types, this is the best possible join type. It is used when all parts of an index are used by the join and the index is a PRIMARY KEY or UNIQUE NOT NULL index.

触发条件: 只匹配到一行的时候。除了system和const之外,这是最好的连接类型了。当我们使用主键索引或者唯一索引的时候,且这个索引的所有组成部分都被用上,才能是该类型。

eq_ref can be used for indexed columns that are compared using the = operator. The comparison value can be a constant or an expression that uses columns from tables that are read before this table. In the following examples, MySQL can use an eq_ref join to process ref_table

在对已经建立索引列进行=操作的时候,eq_ref会被使用到。比较值可以使用一个常量也可以是一个表达式。这个表达示可以是其他的表的行。

##### 多表关联查询,单行匹配

SELECT * FROM ref_table,other_table
  WHERE ref_table.key_column=other_table.column;

##### 多表关联查询,联合索引,多行匹配

SELECT * FROM ref_table,other_table
  WHERE ref_table.key_column_part1=other_table.column
  AND ref_table.key_column_part2=1;

- eq_ref: 出现在要连接过个表的查询计划中,驱动表只返回一行数据,且这行数据是第二个表的主键或者唯一索引,且必须为not null,唯一索引和主键是多列时,只有所有的列都用作比较时才会出现eq_ref
- const: 使用唯一索引或者主键,返回记录一定是1行记录的等值where条件时,通常type是const。其他数据库也叫做唯一索引扫描
- system: 表中只有一行数据或者是空表,且只能用于myisam和memory表。如果是Innodb引擎表,type列在这个情况通常都是all或者index
- NULL: MySQL在优化过程中分解语句,执行时甚至不用访问表或索引,例如从一个索引列里选取最小值可以通过单独索引查找完成。

### possible_keys

查询可能使用到的索引都会在这里列出来, 指出MySQL能使用哪个索引在表中找到记录,查询涉及到的字段上若存在索引,则该索引将被列出,但不一定被查询使用
  
该列完全独立于EXPLAIN输出所示的表的次序。这意味着在possible_keys中的某些键实际上不能按生成的表次序使用。
  
如果该列是NULL,则没有相关的索引。在这种情况下,可以通过检查WHERE子句看是否它引用某些列或适合索引的列来提高你的查询性能。如果是这样,创造一个适当的索引并且再次用EXPLAIN检查查询

### Key

查询真正使用到的索引,select_type为index_merge时,这里可能出现两个以上的索引,其他的select_type这里只会出现一个。

key列显示MySQL实际决定使用的键 (索引)

如果没有选择索引,键是NULL。要想强制MySQL使用或忽视possible_keys列中的索引,在查询中使用FORCE INDEX、USE INDEX或者IGNORE INDEX。

### key_len

表示索引中使用的字节数,可通过该列计算查询中使用的索引的长度 (key_len显示的值为索引字段的最大可能长度,并非实际使用长度,即key_len是根据表定义计算而得,不是通过表内检索出的) , 不损失精确性的情况下,长度越短越好

### rows

表示MySQL根据表统计信息及索引选用情况,估算的找到所需的记录所需要读取的行数

### filtered

使用explain extended时会出现这个列,5.7之后的版本默认就有这个字段,不需要使用explain extended了。这个字段表示存储引擎返回的数据在server层过滤后,剩下多少满足查询的记录数量的比例,注意是百分比,不是具体记录数。

### Extra

该列包含MySQL解决查询的详细信息,有以下几种情况:
  
- Using where: 列数据是从仅仅使用了索引中的信息而没有读取实际的行动的表返回的,这发生在对表的全部的请求列都是同一个索引的部分的时候,表示MySQL服务器将在存储引擎检索行后再进行过滤
using where 则表示需要查询磁盘里存储的数据,速度会慢很多
- Using temporary: 表示MySQL需要使用临时表来存储结果集,常见于排序和分组查询
- Using filesort: MySQL中无法利用索引完成的排序操作称为"文件排序"
- Using join buffer: 改值强调了在获取连接条件时没有使用索引,并且需要连接缓冲区来存储中间结果。如果出现了这个值,那应该注意,根据查询的具体情况可能需要添加索引来改进能。
- Impossible where: 这个值强调了where语句会导致没有符合条件的行。
- Select tables optimized away: 这个值意味着仅通过使用索引,优化器可能仅从聚合函数结果中返回一行

#### Using index (JSON property: using_index)

Using index不读数据文件,只从索引文件获取数据  
The column information is retrieved from the table using only information in the index tree without having to do an additional seek to read the actual row. This strategy can be used when the query uses only columns that are part of a single index.

For InnoDB tables that have a user-defined clustered index, that index can be used even when Using index is absent from the Extra column. This is the case if type is index and key is PRIMARY.

从表中仅使用索引树中的信息就能获取查询语句的列的信息, 而不必进行其他额外查找 (seek) 去读取实际的行记录。当查询的列是单个索引的部分的列时, 可以使用此策略。 (简单的翻译就是: 使用索引来直接获取列的数据,而不需回表) 。对于具有用户定义的聚集索引的 InnoDB 表, 即使从Extra列中没有使用索引, 也可以使用该索引。如果type是index并且Key是主键, 则会出现这种情况。

#### const

constants,常量

#### func

函数的返回值

### 总结

- EXPLAIN不会告诉你关于触发器、存储过程的信息或用户自定义函数对查询的影响情况
- EXPLAIN不考虑各种Cache
- EXPLAIN不能显示MySQL在执行查询时所作的优化工作
- 部分统计信息是估算的,并非精确值
- EXPALIN只能解释SELECT操作,其他操作要重写为SELECT后查看执行计划。

<https://www.cnblogs.com/xiaoboluo768/p/5400990.html>
  
<http://dev.MySQL.com/doc/refman/5.5/en/explain-output.html>
  
<http://www.cnitblog.com/aliyiyi08/archive/2008/09/09/48878.html>
  
<http://www.cnblogs.com/goMySQL/p/3720123.html>
  
<http://www.cnblogs.com/xuanzhi201111>
  
<https://dev.MySQL.com/doc/refman/5.7/en/explain-output.html>
  
<http://www.cnblogs.com/xuanzhi201111/p/4175635.html>
  
<https://dev.MySQL.com/doc/refman/5.5/en/explain-output.html>
  
<https://tech.meituan.com/MySQL-index.html>
