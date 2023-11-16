---
title: MySQL 索引
author: "-"
date: 2014-01-20T10:43:03+00:00
url: /?p=6243
categories:
  - Inbox
tags:
  - MySQL

---
## MySQL 索引

```sql
  
- 显示索引信息
  
SHOW INDEX FROM table_name;
  
SHOW keys FROM table_name;

- create index
  
CREATE INDEX indexName ON mytable(username(length));

- 该语句添加一个主键,这意味着索引值必须是唯一的,且不能为NULL。
  
ALTER TABLE tbl_name ADD PRIMARY KEY (column_list);

- 这条语句创建索引的值必须是唯一的 (除了NULL外,NULL可能会出现多次) 。
  
ALTER TABLE tbl_name ADD UNIQUE index_name (column_list): 

- 添加普通索引,索引值可出现多次。
  
ALTER TABLE tbl_name ADD INDEX index_name (column_list): 

- 该语句指定了索引为 FULLTEXT ,用于全文索引。
  
ALTER TABLE tbl_name ADD FULLTEXT index_name (column_list):

ALTER TABLE testalter_tbl DROP PRIMARY KEY;
  
ALTER TABLE testalter_tbl DROP INDEX c;
  
```

SHOW INDEX FROM table_name;
  
Table: 表的名称
  
Non_unique: 如果索引不能包括重复词,则为0。如果可以,则为1
  
Key_name: 索引的名称
  
Seq_in_index: 索引中的列序列号,从1开始
  
Column_name: 列名称
  
Collation: 列以什么方式存储在索引中。在MySQL中,有值'A' (升序) 或NULL (无分类) 。
  
Cardinality: 索引中唯一值的数目的估计值。通过运行ANALYZE TABLE或myisamchk -a可以更新。基数根据被存储为整数的统计数据来计数,所以即使对于小型表,该值也没有必要是精确的。基数越大,当进行联合时,MySQL使用该索引的机会就越大。
  
Sub_part: 如果列只是被部分地编入索引,则为被编入索引的字符的数目。如果整列被编入索引,则为NULL。
  
Packed: 指示关键字如何被压缩。如果没有被压缩,则为NULL。
  
Null: 如果列含有NULL,则含有YES。如果没有,则该列含有NO。
  
Index_type: 用过的索引方法 (BTREE, FULLTEXT, HASH, RTREE) 。
  
Comment: 更多评注。

索引的存储分类
  
索引是在MySQL的存储引擎层中实现的,而不是在服务层实现的。所以每种存储引擎的索引都不一定完全相同,也不是所有的存储引擎都支持所有的索引类型。MySQL目前提供了一下4种索引。

### B-Tree 索引

B-Tree 索引: MYISAM和InnoDB存储引擎只支持BTREE索引；
如果使用 b-tree 索引形式，有序 id 比无需 id 好
主要原因是索引在磁盘上存储的形式，常用的 b-tree 索引如果 id 是连续的，那么数据存储在相邻的磁盘上，如果查询和写入操作的 id 连续，那么减少随机读写硬盘的几率，提升读写效率。

### HASH 索引

HASH 索引: MEMORY和HEAP存储引擎可以支持HASH和BTREE索引
  
R-Tree 索引(空间索引): 空间索引是MyISAM的一种特殊索引类型,主要用于地理空间数据类型。
  
Full-text (全文索引): 全文索引也是MyISAM的一种特殊索引类型,主要用于全文索引,InnoDB从MySQL5.6版本提供对全文索引的支持。

一般的应用系统,读写比例在10:1左右,而且插入操作和一般的更新操作很少出现性能问题,遇到最多的,也是最容易出问题的,还是一些复杂的查询操作,所以查询语句的优化显然是重中之重。

数据库查询: 等值查询,还有范围查询(>、<、between、in)、模糊查询(like)、并集查询(or)

## 磁盘IO与预读
  
前面提到了访问磁盘,那么这里先简单介绍一下磁盘IO和预读,磁盘读取数据靠的是机械运动,每次读取数据花费的时间可以分为寻道时间、旋转延迟、传输时间三个部分,寻道时间指的是磁臂移动到指定磁道所需要的时间,主流磁盘一般在5ms以下；旋转延迟就是我们经常听说的磁盘转速,比如一个磁盘7200转,表示每分钟能转7200次,也就是说1秒钟能转120次,旋转延迟就是1/120/2 = 4.17ms；传输时间指的是从磁盘读出或将数据写入磁盘的时间,一般在零点几毫秒,相对于前两个时间可以忽略不计。那么访问一次磁盘的时间,即一次磁盘IO的时间约等于5+4.17 = 9ms左右,听起来还挺不错的,但要知道一台500 -MIPS的机器每秒可以执行5亿条指令,因为指令依靠的是电的性质,换句话说执行一次IO的时间可以执行40万条指令,数据库动辄十万百万乃至千万级数据,每次9毫秒的时间,显然是个灾难。

建索引的几大原则
  
1.最左前缀匹配原则,非常重要的原则,MySQL会一直向右匹配直到遇到范围查询(>、<、between、like)就停止匹配,比如a = 1 and b = 2 and c > 3 and d = 4 如果建立(a,b,c,d)顺序的索引,d是用不到索引的,如果建立(a,b,d,c)的索引则都可以用到,a,b,d的顺序可以任意调整。
  
2.=和in可以乱序,比如a = 1 and b = 2 and c = 3 建立(a,b,c)索引可以任意顺序,MySQL的查询优化器会帮你优化成索引可以识别的形式
  
3.尽量选择区分度高的列作为索引,区分度的公式是count(distinct col)/count(*),表示字段不重复的比例,比例越大我们扫描的记录数越少,唯一键的区分度是1,而一些状态、性别字段可能在大数据面前区分度就是0,那可能有人会问,这个比例有什么经验值吗？使用场景不同,这个值也很难确定,一般需要join的字段我们都要求是0.1以上,即平均1条扫描10条记录
  
4.索引列不能参与计算,保持列"干净",比如from_unixtime(create_time) = '2014-05-29'就不能使用到索引,原因很简单,b+树中存的都是数据表中的字段值,但进行检索时,需要把所有元素都应用函数才能比较,显然成本太大。所以语句应该写成create_time = unix_timestamp('2014-05-29');
  
5.尽量的扩展索引,不要新建索引。比如表中已经有a的索引,现在要加(a,b)的索引,那么只需要修改原来的索引即可

* * *

本文介绍了七种MySQL索引类型。在数据库表中,对字段建立索引可以大大提高查询速度。通过善用这些索引,可以令MySQL的查询和运行更加高效。

索引是快速搜索的关键。MySQL索引的建立对于MySQL的高效运行是很重要的。下面介绍几种常见的MySQL索引类型。

在数据库表中,对字段建立索引可以大大提高查询速度。假如我们创建了一个 mytable表:

CREATE TABLE mytable(
  
ID INT NOT NULL,
  
username VARCHAR(16) NOT NULL
  
);

我们随机向里面插入了10000条记录,其中有一条: 5555, admin。

在查找username="admin"的记录 SELECT * FROM mytable WHERE username='admin';时,如果在username上已经建立了索引,MySQL无须任何扫描,即准确可找到该记录。相反,MySQL会扫描所有记录,即要查询10000条记录。

索引分单列索引和组合索引。单列索引,即一个索引只包含单个列,一个表可以有多个单列索引,但这不是组合索引。组合索引,即一个索引包含多个列。

MySQL索引类型包括:
  
 (1) 普通索引
  
这是最基本的索引,它没有任何限制。它有以下几种创建方式:
  
◆创建索引
  
CREATE INDEX indexName ON mytable(username(length));

如果是CHAR,VARCHAR类型,length可以小于字段实际长度；如果是BLOB和TEXT类型,必须指定 length,下同。

◆修改表结构
  
ALTER mytable ADD INDEX [indexName] ON (username(length))

◆创建表的时候直接指定
  
CREATE TABLE mytable(
  
ID INT NOT NULL,
  
username VARCHAR(16) NOT NULL,
  
INDEX [indexName] (username(length))
  
);

删除索引的语法:
  
DROP INDEX [indexName] ON mytable;

 (2) 唯一索引
  
它与前面的普通索引类似,不同的就是: 索引列的值必须唯一,但允许有空值。如果是组合索引,则列值的组合必须唯一。它有以下几种创建方式:
  
◆创建索引
  
CREATE UNIQUE INDEX indexName ON mytable(username(length))

◆修改表结构
  
ALTER mytable ADD UNIQUE [indexName] ON (username(length))

◆创建表的时候直接指定
  
CREATE TABLE mytable(
  
ID INT NOT NULL,
  
username VARCHAR(16) NOT NULL,
  
UNIQUE [indexName] (username(length))
  
);

 (3) 主键索引
  
它是一种特殊的唯一索引,不允许有空值。一般是在建表的时候同时创建主键索引:

CREATE TABLE mytable(
  
ID INT NOT NULL,
  
username VARCHAR(16) NOT NULL,
  
PRIMARY KEY(ID)
  
);

当然也可以用 ALTER 命令。记住: 一个表只能有一个主键。

 (4) 组合索引
  
为了形象地对比单列索引和组合索引,为表添加多个字段:

CREATE TABLE mytable(
  
ID INT NOT NULL,
  
username VARCHAR(16) NOT NULL,
  
city VARCHAR(50) NOT NULL,
  
age INT NOT NULL
  
);

为了进一步榨取MySQL的效率,就要考虑建立组合索引。就是将 name, city, age建到一个索引里:
  
ALTER TABLE mytable ADD INDEX name_city_age (name(10),city,age);

建表时,usernname长度为 16,这里用 10。这是因为一般情况下名字的长度不会超过10,这样会加速索引查询速度,还会减少索引文件的大小,提高INSERT的更新速度。

如果分别在 usernname,city,age上建立单列索引,让该表有3个单列索引,查询时和上述的组合索引效率也会大不一样,远远低于我们的组合索引。虽然此时有了三个索引,但MySQL只能用到其中的那个它认为似乎是最有效率的单列索引。

建立这样的组合索引,其实是相当于分别建立了下面三组组合索引:
  
usernname,city,age
  
usernname,city
  
usernname

为什么没有 city,age这样的组合索引呢？这是因为MySQL组合索引"最左前缀"的结果。简单的理解就是只从最左面的开始组合。并不是只要包含这三列的查询都会用到该组合索引,下面的几个SQL就会用到这个组合索引:
  
SELECT * FROM mytable WHREE username="admin" AND city="郑州"
  
SELECT * FROM mytable WHREE username="admin"

而下面几个则不会用到:
  
SELECT * FROM mytable WHREE age=20 AND city="郑州"
  
SELECT * FROM mytable WHREE city="郑州"

 (5) 建立索引的时机
  
到这里我们已经学会了建立索引,那么我们需要在什么情况下建立索引呢？一般来说,在WHERE和JOIN中出现的列需要建立索引,但也不完全如此,因为MySQL只对<,<=,=,>,>=,BETWEEN,IN,以及某些时候的LIKE才会使用索引。例如:

SELECT t.Name
  
FROM mytable t LEFT JOIN mytable m
  
ON t.Name=m.username WHERE m.age=20 AND m.city='郑州'

此时就需要对city和age建立索引,由于mytable表的userame也出现在了JOIN子句中,也有对它建立索引的必要。
  
刚才提到只有某些时候的LIKE才需建立索引。因为在以通配符%和_开头作查询时,MySQL不会使用索引。例如下句会使用索引:
  
SELECT * FROM mytable WHERE username like'admin%'

而下句就不会使用:
  
SELECT * FROM mytable WHEREt Name like'%admin'
  
因此,在使用LIKE时应注意以上的区别。

 (6) 索引的不足之处
  
上面都在说使用索引的好处,但过多的使用索引将会造成滥用。因此索引也会有它的缺点:
  
◆虽然索引大大提高了查询速度,同时却会降低更新表的速度,如对表进行INSERT、UPDATE和DELETE。因为更新表时,MySQL不仅要保存数据,还要保存一下索引文件。
  
◆建立索引会占用磁盘空间的索引文件。一般情况这个问题不太严重,但如果你在一个大表上创建了多种组合索引,索引文件的会膨胀很快。
  
索引只是提高效率的一个因素,如果你的MySQL有大数据量的表,就需要花时间研究建立最优秀的索引,或优化查询语句。

 (7) 使用索引的注意事项
  
使用索引时,有以下一些技巧和注意事项:
  
◆索引不会包含有NULL值的列
  
只要列中包含有NULL值都将不会被包含在索引中,复合索引中只要有一列含有NULL值,那么这一列对于此复合索引就是无效的。所以我们在数据库设计时不要让字段的默认值为NULL。

◆使用短索引
  
对串列进行索引,如果可能应该指定一个前缀长度。例如,如果有一个CHAR(255)的列,如果在前10个或20个字符内,多数值是惟一的,那么就不要对整个列进行索引。短索引不仅可以提高查询速度而且可以节省磁盘空间和I/O操作。

◆索引列排序
  
MySQL查询只使用一个索引,因此如果where子句中已经使用了索引的话,那么order by中的列是不会使用索引的。因此数据库默认排序可以符合要求的情况下不要使用排序操作；尽量不要包含多个列的排序,如果需要最好给这些列创建复合索引。

◆like语句操作
  
一般情况下不鼓励使用like操作,如果非使用不可,如何使用也是一个问题。like "%aaa%" 不会使用索引而like "aaa%"可以使用索引。

◆不要在列上进行运算
  
select * from users where YEAR(adddate)<2007;
  
将在每个行上进行运算,这将导致索引失效而进行全表扫描,因此我们可以改成
  
select * from users where adddate<'2007-01-01';

◆不使用NOT IN和<>操作
  
以上,就对其中MySQL索引类型进行了介绍。

[https://tech.meituan.com/MySQL-index.html](https://tech.meituan.com/MySQL-index.html)
  
[http://www.cnblogs.com/hustcat/archive/2009/10/28/1591648.html](http://www.cnblogs.com/hustcat/archive/2009/10/28/1591648.html)
  
[https://segmentfault.com/a/1190000003072424](https://segmentfault.com/a/1190000003072424)
