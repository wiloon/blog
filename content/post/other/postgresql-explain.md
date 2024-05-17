---
title: PostgreSQL execution plan, explain, 执行计划
author: "-"
date: 2015-09-17T10:42:01+00:00
url: postgresql/explain
categories:
  - DB
tags:
  - reprint
  - remix
---
## PostgreSQL execution plan, explain, 执行计划

## Seq Scan, 全表扫描，顺序扫描

全表扫描，也叫顺序扫描，扫描时把表中所有的数据块从头到尾遍历一边，找到复合条件的数据块。全表扫描在在explain中使用Seq Scan表示

## IndexOnly Scan

IndexOnly Scan 是覆盖索引扫描，所需的返回结果能被所扫描的索引全部覆盖

https://www.jianshu.com/p/682d798aee1f

了解 PostgreSQL 执行计划对于开发人员来说是一项关键技能，执行计划是我们优化查询，验证我们的优化查询是否确实按照我们期望的方式运行的重要方式。

## PostgreSQL 数据库中的查询生命周期

每个查询都会经历不同的阶段，了解每个阶段对数据库的意义很重要。


查询生命周期
第一阶段是通过Postgres 的客户端连接到数据库。

第二阶段是将查询转换为称为解析树的中间格式。

第三阶段就是我们所说的重写系统/规则系统。它采用从第二阶段生成的解析树，并以规划器/优化器可以开始在其中工作的方式重新编写它。

第四阶段是最重要的阶段。如果没有规划器，执行器将在如何执行查询、使用什么索引、是否扫描较小的表以消除更多不必要的行等问题上一头雾水。

第五个也是最后一个阶段是执行器，它实际执行并返回结果。

## 数据准备

用假数据设置一些表来为后面的测试做准备。

```SQL
--建表
create table users
(
    id         serial PRIMARY KEY,
    name       varchar(255)            not null,
    mobile     varchar(255)            not null,
    age        integer,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null
);

--导入1000000数据
insert into users(name,mobile,age) select gen_random_zh(2,3), floor(random()*(13799999999-13700000000)+ 13700000000) as mobile, random()*(30-20)+20 from generate_series(1,1000000) as id;

```


--建表
create table comments
(
id serial PRIMARY KEY,
article_id bigint not null,
user_id bigint not null,
content varchar(255) not null,
created_at timestamp default now() not null,
updated_at timestamp default now() not null
);

--导入1000000数据
insert into comments(article_id,user_id,content) select floor((select min(id) from articles)  + RANDOM() * ((select max(id) from articles)- (select min(id) from articles))) as article_id, floor((select min(id) from users)  + RANDOM() * ((select max(id) from users)- (select min(id) from users))) as article_id, gen_random_zh(1,10) from generate_series(1,1000000) as id;
3、执行计划参数
PostgreSQL 和许多其他数据库系统一样，可以在数据库实际执行查询之前查看它们运行的计划。我们可以通过运行所谓的EXPLAIN命令来做到这一点。

3.1、解释一个查询
EXPLAIN SELECT * FROM users LIMIT 10;
EXPLAIN 查询的输出内容
3.2、解释并执行
EXPLAIN ANALYSE SELECT * FROM users LIMIT 10;
将 ANALYZE 参数添加到查询会产生计时
与EXPLAIN不同的是，EXPLAIN ANALYSE会在数据库中运行查询。

3.3、缓存
加上参数BUFFERS，可以显示有多少数据来自 PostgreSQL 缓存，多少来自磁盘。

EXPLAIN (ANALYSE,BUFFERS) SELECT * FROM users LIMIT 10 OFFSET 200
包含 BUFFERS
Buffers : shared hit=5表示从 PostgreSQL 缓存中获取了五个页，如果是shared read=5，则意味着数据来自磁盘而不是缓存。我们调整查询的行偏移再试一下。

EXPLAIN (ANALYSE,BUFFERS) SELECT * FROM users LIMIT 10 OFFSET 500
更改偏移量会产生不同的hit和read
Buffers: shared hit=7 read=5显示有 5 页来自磁盘。如果我们再次执行相同的查询，那么所有数据现在都来自缓存。


所有查询都来自缓存
PostgreSQL 使用一种称为 LRU（最近最少使用）缓存的机制将经常使用的数据存储在内存中。

3.4、VERBOSE 参数
EXPLAIN (ANALYSE,BUFFERS,VERBOSE) SELECT * FROM users LIMIT 10 OFFSET 500
Verbose是一个提供额外信息的参数，用于获取有关查询的详细信息和其他信息。。


VERBOSE 命令参数将为复杂查询提供更多信息
请注意，Output: id, name, mobile等是额外的字段信息。

4、执行计划的结构
任何执行计划，无论其复杂性如何，都有一些基本结构。

查询的节点
EXPLAIN SELECT * FROM users LIMIT 10 OFFSET 500;
节点是执行查询的关键部分
一个节点可以被认为是数据库执行的一个阶段。节点大多是嵌套的，如上图；先完成 Seq Scan，然后在进行Limit。添加一个Where子句来理解进一步的嵌套。

EXPLAIN SELECT * FROM users where NAME = '张三' LIMIT 10
查询

执行是由内而外进行的：

筛选name = '张三' 的行
使用上述过滤器进行顺序扫描
在顶部应用limit
5、扫描
PostgreSQL 执行计划中有几种节点类型，包括Scans、Joins、Sort等，本次将说一下Scans。
在本文中，将主要探讨Scan节点类型。为了便于理解，禁用了并行扫描。

SET max_parallel_workers_per_gather = 0;

## 顺序扫描（seq scan）

让我们搜索一下 user_id=20001 的数据。


顺序扫描.png
如果没有索引或行数较少，则 Planner 会扫描所有的行。通常情况下我们不应该使用顺序扫描，因为它非常慢并且随着数据的增加而变慢。当表太小或顺序扫描足够快时，也会出现例外情况。

5.2索引扫描 Index Scan
让我们在列上创建一个简单的 BTree 索引来加速上述查询。

CREATE INDEX id_idx ON comments USING BTREE(user_id)
创建索引后，Planner 现在使用索引来执行索引扫描。


021-索引扫描.png
它比Seq Scan扫描快得多。

5.3仅索引扫描 Index Only Scan
Index Only Scan 与 Index Scan 非常相似，仅当SELECT查询的字段在WHERE子句中都包含索引列时，才能使用。


仅索引扫描
5.4Bitmap Heap Scan 和 Bitmap Index Scan
即 位图堆扫描 和 位图索引扫描


位图堆和位图索引扫描
普通的索引扫描一次读一条索引项，而BitMap Heap Scan一次性将满足条件的索引项全部取出，并在内存中进行排序, 然后根据取出的索引项访问表数据。BitMap Heap Scan 针对有多个索引项满足条件时，通过饱和式的索引页读取结合排序大幅减少随机读取，提升I/O效率。

但在某些情况下Bitmap And或Bitmap Or将不起作用，我们将不得不创建复合索引。在许多情况下，Planner 可以非常有效地组合两个单独的索引。

5.5并行扫描
顺序扫描是迄今为止我们看到的所有计划中最慢的。计划器按顺序检查数据并尝试找到结果。PostgreSQL 通过在查询中添加并行查询优化了一些性能。


并行顺序扫描
并行查询默认配置是2，一般建议是让并行查询的数量与 CPU 中的核心数量相等，以获最高的效率。

6、EXPLAIN 成本
在查看EXPLAIN命令的输出时，首先会注意到成本统计信息，因此很自然地想知道它们的含义、它们是如何计算的，以及它们是如何使用的。
执行计划解释
6.1成本的单位是什么
成本是任意单位。常见的误解是把它们认为是以毫秒或其他时间单位为单位，但事实并非如此。
默认情况下，成本单位锚定到成本为 1.0 单位的单个顺序页面读取seq_page_cost。
常用开销的配置

配置及说明：
seq_page_cost: 1 连续块扫描操作的单个块的cost，例如全表扫描
random_page_cost: 4 随机块扫描操作的单个块的cost，例如索引扫描
cpu_tuple_cost: 0.01 处理每条记录的cpu开销（tuple：关系中的一行记录）
cpu_index_tuple_cost: 0.005 扫描每个索引条目带来的CPU开销
cpu_operator_cost: 0.0025 操作符或函数带来的cpu开销
6.2启动成本
您看到的第一个数字cost=被称为“启动成本”。这是获取第一行所需时间的估计值。因此，一个节点的启动成本包括其子项的成本。
对于顺序扫描，启动成本通常接近于零，因为它可以立即开始获取行。对于排序操作，它会更高，因为在开始返回行之前需要完成大部分工作。

6.3总成本
在启动成本和两个点之后，被称为“总成本”。这是对返回所有行所需时间的估计。

7、如何计算成本
7.1顺序扫描
顺序扫描的成本由函数 cost_seqscan()来估算。
顺序扫描，由于是扫描所有数据页，不需要准备工作，start-up的成本为0，run的成本计算公式为：
run cost = cpu run cost + disk run cost
=(cpu_tuple_cost + cpu_operator_cost) * Ntuple + seq_page_cost * Npage
Ntuple，Npage可在pg_class中查询出来。

postgres=# select relpages, reltuples FROM pg_class WHERE relname='users';
relpages | reltuples
----------+-----------
9346 |    1e+06
最终开销是：(0.01 + 0.0025)* 1000000 + 1 * 9346 = 21846.0


顺序扫描成本计算
7.2索引扫描
以查询语句 select * from users where id < 999;来估算索引扫描成本。
由查询条件id<999，可走users_pkey索引，查询pg_class可得Nindex,page=2745，Nindex,tuple=1000000。

postgres=# SELECT relpages, reltuples FROM pg_class WHERE relname = 'users_pkey';
relpages | reltuples
----------+-----------
2745 |    1e+06
(1 row)
7.2.1 start-up成本
索引扫描start-up成本指读取索引页拿到目标表第一个tuple的成本，其估算公式为：
start-up cost={ceil(log2(Nindex,tuple)) + (Hindex + 1) * 50} * cpu_operator_cost
其中Hindex为索引树的高度。

# 用pageinspect插件查询索引高度，level为2，高度为2
postgres=# select * from bt_metap('test_idx');
magic  | version | root | level | fastroot | fastlevel | oldest_xact | last_cleanup_num_tuples
--------+---------+--------+-------+------------+-----------+-------------+-------------------------
340322 |       4 |    412 |     2 |        412 |         2 |           0 |                      -1
start-up cost={ceil(log2(1000000)) + (2+1) * 50} * 0.0025= 0.425。

7.2.2 run成本
索引扫描的run成本指表和索引cpu成本、IO成本之和：
run cost=(index cpu cost + table cpu cost) + (index IO cost + table IO cost)
注：仅索引扫描的话不需估算 table cpu cost 和 table IO cost。
其中三个成本估算公式如下：

index cpu cost=Selectivity * Nindex,tuple * (cpu_index_tuple_cost+qual_op_cost);
table cpu cost=Selectivity * Ntuple * cpu_tuple_cost;
index IO cost= ceil(Selectivity * Nindex,page) * random_page_cost;
table IO cost=max_IO_cost+indexCorrelation2*(min_IO_cost-max_IO_cost);

qual_op_cost，评估索引的成本，默认为0.0025。
Selectivity：
权重因子，表明I/O到CPU的相关性，又称为选择率，指where子句的索引的搜索范围的比例，它是从0到1的浮点数。如 (Selectivity * Ntuple) 指读取表中行的数量， (Selectivity * Nindex,page) 指读取索引页的数量。
Selectivity使用 histogram_bounds 或 MCV(Most Common Value) 来估算，这两者可在pg_stats中查询出来。
表的每个字段的MCV存储在pg_stats的most_common_vals 和 most_common_freqs字段，如查询语句：

select * from users where id < 999;
SELECT most_common_vals, most_common_freqs FROM pg_stats where tablename='users' and attname='id';
可查出表 users 字段 id 值 999 对应的频率，将该频率作为Selectivity值。
如果 MCV 没有查询出结果，则使用 histogram_bounds 来估算。
histogram_bounds：将字段的值分成近似相等的级别的值列表。
查看表users字段id的histogram_bounds：

postgres=# SELECT histogram_bounds  FROM pg_stats where tablename='users' and attname='id';
histogram_bounds
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
{24,9948,20772,31475,41663,50095,60571,70420,79825,89302,99882,109310,119327,129438,139089,149055,158695,168809,179415,189557,198869,208360,218839,229109,238739,249205,259831,269518,279599,289155,298695,308020,317203,327240,337306,347137,357224,366999,377090,387940,397380,408293,419071,428211,438488,448486,458984,469359,478653,488477,499100,508761,518178,529688,539247,549696,559948,569816,580518,591073,602060,611942,622714,632301,643046,654112,665432,675455,685635,695258,705031,715577,724843,735068,744714,753645,763120,772899,782906,791836,802342,811931,821667,830875,840692,850233,860378,869772,879845,889899,898914,909238,918837,929341,938615,949433,959099,968353,978552,989834,999909}
histogram_bounds默认分为100个桶(采样组)，桶的编号从0开始，histogram_bounds的值是桶的边界值，如第0个桶的histogram_bounds为24，则存储在0号桶的最小值为24，第1个桶的histogram_bounds为9948，则存储在1号桶的最小值为9948，则桶0存储的数据为 24 <= value < 9948。
查询条件 id < 999，999 存储在第0个桶，然后用公式可计算：


max_IO_cost是IO成本的最坏情况，即随机扫描所有表页的成本，公式如下 ：
max_IO_cost=Npage * random_page_cost=9346 * 4.0 = 37384.0
min_IO_cost是IO成本的最佳情况，即顺序扫描所选表页的成本，公式如下：
min_IO_cost=1 * random_page_cost + (ceil(Selectivity * Npage) - 1) * seq_page_cost=1 * 4.0 + (ceil(0.0009824667472793228* 9346) - 1) * 1.0 = 13.0
indexCorrelation，从pg_stats可查到，等于 1。

postgres=# SELECT tablename,attname, correlation FROM pg_stats WHERE tablename = 'users' and attname='id';
tablename | attname | correlation
------------+--------+-------------
users      | id     |           1
所以：

index cpu cost = 0.0009824667472793228* 1000000 * (0.005 + 0.0025) = 7.368500604594921
table cpu cost = 0.0009824667472793228* 1000000 * 0.01 = 9.824667472793228
index IO cost = ceil(0.0009824667472793228* 2745) * 4.0 = 12.0
table IO cost = 37384.0 + 12 * (13.0 - 37384.0) = 13.0

最后：
run cost = (7.368500604594921 + 9.824667472793228) + (12.0 +13.0) = 42.19316807738815

total cost = 0.425 + 42.19316807738815 = 42.61816807738815
索引扫描成本
成本计算的源码：https://github.com/postgres/postgres/blob/ab72716778128fb63d54ac256adf7fe6820a1185/src/backend/optimizer/path/costsize.c

作者：GALAXY_ZMY
链接：https://www.jianshu.com/p/682d798aee1f
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

