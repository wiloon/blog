---
title: 'MySQL 索引  btree hash rtree'
author: "-"
date: 2016-12-03T12:46:15+00:00
url: /?p=9451
categories:
  - Inbox
tags:
  - reprint
---
## 'MySQL 索引  btree hash rtree'
一、MySQL索引类型

MySQL里目前只支持4种索引分别是: full-text,b-tree,hash,r-tree

b-tree索引应该是MySQL里最广泛的索引的了,除了archive基本所有的存储引擎都支持它.


1. full-text索引

full-text在MySQL里仅有myisam支持它,而且支持full-text的字段只有char、varchar、text数据类型。

full-text主要是用来代替like "%\***%"效率低下的问题

2. b-tree索引

b-tree在myisam里的形式和innodb稍有不同

在 innodb里,有两种形态: 一是primary key形态,其leaf node里存放的是数据,而且不仅存放了索引键的数据,还存放了其他字段的数据。二是secondary index,其leaf node和普通的b-tree差不多,只是还存放了指向主键的信息.

而在myisam里,主键和其他的并没有太大区别。不过和innodb不太一样的地方是在myisam里,leaf node里存放的不是主键的信息,而是指向数据文件里的对应数据行的信息.

3. hash索引

目前我所知道的就只有memory和ndb cluster支持这种索引.

hash索引由于其结构,所以在每次查询的时候直接一次到位,不像b-tree那样一点点的前进。所以hash索引的效率高于b-tree,但hash也有缺点,主要如下: 

(1)由于存放的是hash值,所以仅支持<=>以及in操作.

(2)hash索引无法通过操作索引来排序,这是因为存放的时候经过hash计算,但是计算的hash值和存放的不一定相等,所以无法排序.

(3)在组合所以里,无法对部分使用索引.

(4)不能避免全表扫描,只是由于在memory表里支持非唯一值hash索引,就是不同的索引键,可能存在相同的hash值.

(5)当存在大量相同hash值得时候,hash索引的效率会变低.

4. r-tree索引

r-tree在MySQL很少使用,仅支持geometry数据类型,支持该类型的存储引擎只有myisam、bdb、innodb、ndb、archive几种。

相对于b-tree,r-tree的优势在于范围查找.

二、MySQL里sql语句值得注意的地方

1. myisam里所有键的长度仅支持1000字节,innodb是767.

2. blob和text字段仅支持前缀索引.

3. 使用!=以及<>不等于的时候,MySQL不使用索引.

4. 当在字段时候函数的时候,MySQL无法使用索引；在join时条件字段类型不一致的时候,MySQL无法使用索引；在组合索引里使用非第一个索引时也不使用索引.

5. 在使用like的时候,以%开头,即"%\***"的时候无法使用索引；在使用or的时候,要求or前后字段都有索引.

有时候MySQL query optimizer会认为使用索引并不是最优计划,所以不使用索引。可以在sql语句里可以用use,force index,当然有时候使用也不会比不用快,所以需要忽略掉index方法是ignore index.

关闭查询缓存sql_no_cache

select sql_no_cache * from table_name;

这样可以让一些很少使用的语句不放在缓存里,查找的时候不会去缓存里找；对应的是强制缓存sql_cache

select sql_cache * from table_name;

另外,在my.cnf中如果设置query_cache_type=2的话,那么只有在使用sql_cache后才会使用缓存;

还有MySQL里的优先操作hight_priority让MySQL优先操作这个语句

select high_priority * fromtable_name;

与其对应的是low_priority;

MySQL里还有延时插入insert delayed

insert delayed into table_name....;

#当提交之后,MySQL返回ok,但不立即插入,而是当MySQL有空再插入。假如等待时服务器崩溃,那么所有数据丢失,并且插入不会返回自增id.

三、几个技巧

1. 强制连接顺序:  STRAIGHT_JOIN

SELECT TABLE1.FIELD1, TABLE2.FIELD2 FROM TABLE1 STRAIGHT_JOIN TABLE2 WHERE …

由上面的SQL语句可知,通过STRAIGHT_JOIN强迫MySQL按TABLE1、TABLE2的顺序连接表。如果你认为按自己的顺序比MySQL推荐的顺序进行连接的效率高的话,就可以通过STRAIGHT_JOIN来确定连接顺序。

2. 强制使用临时表:  SQL_BUFFER_RESULT

SELECT SQL_BUFFER_RESULT * FROM TABLE1 WHERE …

当我们查询的结果集中的数据比较多时,可以通过SQL_BUFFER_RESULT,选项强制将结果集放到临时表中,这样就可以很快地释放MySQL的表锁 (这样其它的SQL语句就可以对这些记录进行查询了) ,并且可以长时间地为客户端提供大记录集。

3. 分组使用临时表 SQL_BIG_RESULT和SQL_SMALL_RESULT

SELECT SQL_BUFFER_RESULT FIELD1, COUNT(*) FROM TABLE1 GROUP BY FIELD1;

一般用于分组或DISTINCT关键字,这个选项通知MySQL,如果有必要,就将查询结果放到临时表中,甚至在临时表中进行排序。SQL_SMALL_RESULT比起SQL_BIG_RESULT差不多,很少使用。

转载声明:  本文转自 http://apps.hi.baidu.com/share/detail/23985447