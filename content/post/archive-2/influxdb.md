---
title: InfluxDB
author: "-"
date: 2017-07-12T15:09:01+00:00
url: /?p=10825
categories:
  - DataBase

tags:
  - reprint
---
## InfluxDB
时间序列数据库 InfluxDB
  
基于 Go 语言开发,社区非常活跃,项目更新速度很快,日新月异,关注度高。

特点
  
可以设置metric的保存时间。
  
支持通过条件过滤以及正则表达式删除数据。
  
支持类似 sql 的语法。
  
可以设置数据在集群中的副本数。
  
支持定期采样数据,写入另外的measurement,方便分粒度存储数据。

概念
  
数据格式 Line Protocol

measurement[,tag_key1=tag_value1...] field_key=field_value[,field_key2=field_value2] [timestamp]

cpu_load,host_id=1 value=0.1 1434055562000000000
  
相比于 JSON 格式,无需序列化,更加高效。

measurement: metric name,例如 cpu_load。
  
field-key, field-value: 通常用来存储数据,类似 opentsdb 中的 value=0.6,但是支持各种类型,数据存储时不会进行索引,每条数据必须拥有一个 field-key,如果使用 field-key 进行过滤,需要遍历一遍所有数据。
  
tags-key, tags-value: 和 field-key 类似,但是会进行索引,方便查询时用于过滤条件。

Series
  
measurement, tag set, retention policy 相同的数据集合算做一个 series。

假设 cpu_load 有两个 tags,host_id 和 name,host_id 的数量为 100,name 的数量为 200,则 series 基数为 100 * 200 = 20000。

数据存储
  
measurements, tag keys, field keys,tag values 全局存一份。
  
field values 和 timestamps 每条数据存一份。

Retention Policy
  
保留策略包括设置数据保存的时间以及在集群中的副本个数。
  
默认的 RP 为 default,保存时间不限制,副本个数为 1,默认 RP 是可以修改的,并且我们可以创建新的 RP。

Continuous Query
  
CQ 是预先配置好的一些查询命令,SELECT 语句必须包含 GROUP BY time(),influxdb 会定期自动执行这些命令并将查询结果写入指定的另外的 measurement 中。
  
利用这个特性并结合 RP 我们可以方便地保存不同粒度的数据,根据数据粒度的不同设置不同的保存时间,这样不仅节约了存储空间,而且加速了时间间隔较长的数据查询效率,避免查询时再进行聚合计算。

Shard
  
Shard 这个概念并不对普通用户开放,实际上是 InfluxDB 将连续一段时间内的数据作为一个 shard 存储,根据数据保存策略来决定,通常是保存1天或者7天的数据。例如如果保存策略 RP 是无限制的话,shard 将会保存7天的数据。这样方便之后的删除操作,直接关闭下层对应的一个数据库即可。

存储引擎
  
从 LevelDB (LSM Tree) ,到 BoltDB (mmap B+树) ,现在是自己实现的 TSM Tree 的算法,类似 LSM Tree,针对 InfluxDB 的使用做了特殊优化。

LevelDB
  
LevelDB 底层使用了 LSM Tree 作为数据结构,用于存储大量的 key 值有序的 K-V 数据,鉴于时序数据的特点,只要将时间戳放入 key 中,就可以非常快速的遍历指定时间范围内的数据。LSM Tree 将大量随机写变成顺序写,所以拥有很高的写吞吐量,并且 LevelDB 内置了压缩功能。

数据操作被先顺序写入 WAL 日志中,成功之后写入内存中的 MemTable,当 MemTable 中的数据量达到一定阀值后,会转换为 Immutable MemTable,只读,之后写入 SSTable。SSTable 是磁盘上只读的用于存储有序键值对的文件,并且会持续进行合并,生成新的 SSTable。在 LevelDB 中是分了不同层级的 SSTable 用于存储数据。

LevelDB 不支持热备份,它的变种 RocksDB 和 HyperLevelDB 实现了这个功能。

最严重的问题是由于 InfluxDB 通过 shard 来组织数据,每一个 shard 对应的就是一个 LevelDB 数据库,而由于 LevelDB 的底层存储是大量 SSTable 文件,所以当用户需要存储长时间的数据,例如几个月或者一年的时候,会产生大量的 shard,从而消耗大量文件描述符,将系统资源耗尽。

## BoltDB
  
之后 InfluxDB 采用了 BoltDB 作为数据存储引擎。BoltDB 是基于 LMDB 使用 Go 语言开发的数据库。同 LevelDB 类似的是,都可以用于存储 key 有序的 K-V 数据。

虽然采用 BoltDB 的写效率有所下降,但是考虑到用于生产环境需要更高的稳定性,BoltDB 是一个合适的选择,而且 BoltDB 使用纯 Go 编写,更易于跨平台编译部署。

最重要的是 BoltDB 的一个数据库存储只使用一个单独的文件。Bolt 还解决了热备的问题,很容易将一个 shard 从一台机器转移到另外一台。

但是当数据库容量达到数GB级别时,同时往大量 series 中写入数据,相当于是大量随机写,会造成 IOPS 上升。

TSM Tree
  
TSM Tree 是 InfluxDB 根据实际需求在 LSM Tree 的基础上稍作修改优化而来。

WAL
  
每一个 shard 对应底层的一个数据库。每一个数据库有自己的 WAL 文件,压缩后的元数据文件,索引文件。
  
WAL 文件名类似 _000001.wal,数字递增,每达到 2MB 时,会关闭此文件并创建新的文件,有一个写锁用于处理多协程并发写入的问题。
  
可以指定将 WAL 从内存刷新到磁盘上的时间,例如30s,这样会提高写入性能,同时有可能会丢失这30s内的数据。
  
每一个 WAL 中的条目遵循 TLV 的格式,1字节用于表示类型 (points,new fields,new series,delete) ,4字节表示 block 的长度,后面则是具体压缩后的 block 内容。WAL 文件中得内容在内存中会进行缓存,并且不会压缩,每一个 point 的 key 为 measurement, tagset 以及 unique field,每一个 field 按照自己的时间顺序排列。

查询操作将会去 WAL 以及索引中查询,WAL 在内存中缓存有一个读写锁进行控制。删除操作会将缓存中的key删除,同时在 WAL 文件中进行记录并且在内存的索引中进行删除标记。

Data Files(SSTables)
  
这部分 InfluxDB 自己定义了特定的数据结构,将时间戳编码到了 DataFiles 中,进行了相对于时间序列数据的优化。

API
  
通过 HTTP 访问 influxdb。

语法上是一种类似于 SQL 的命令,官方称为 InfluxQL。

创建数据库

curl -POST http://localhost:8086/query -data-urlencode "q=CREATE DATABASE mydb"
  
插入数据

curl -i -XPOST 'http://localhost:8086/write?db=mydb' -data-binary 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'
  
cpu_load_short 是 measurement,host 和 region 是 tags-key,value 是 field-key。

多条数据时,用换行区分每条数据

curl -i -XPOST 'http://localhost:8086/write?db=mydb' -data-binary 'cpu_load_short,host=server02 value=0.67
  
cpu_load_short,host=server02,region=us-west value=0.55 1422568543702900257
  
cpu_load_short,direction=in,host=server01,region=us-west value=2.0 1422568543702900257'
  
读取数据

curl -GET 'http://localhost:8086/query' -data-urlencode "db=mydb" -data-urlencode "epoch=s" -data-urlencode "q=SELECT value FROM cpu_load_short WHERE region='us-west'"
  
同时查询多条数据时,以分号分隔

curl -G 'http://localhost:8086/query' -data-urlencode "db=mydb" -data-urlencode "epoch=s" -data-urlencode "q=SELECT value FROM cpu_load_short WHERE region='us-west';SELECT count(value) FROM cpu_load_short WHERE region='us-west'"
  
这里 -data-urlencode "epoch=s" 会使返回的时间戳为 unix 时间戳格式。

创建 RP

CREATE RETENTION POLICY two_hours ON food_data DURATION 2h REPLICATION 1 DEFAULT
  
这里将 two_hours 设置成了默认保存策略,存入 food_data 中的数据如果没有明确指定 RP 将会默认采用此策略,数据保存时间为 2 小时,副本数为 1。

创建 CQ

CREATE CONTINUOUS QUERY cq_5m ON food_data BEGIN SELECT mean(website) AS mean_website,mean(phone) AS mean_phone INTO food_data."default".downsampled_orders FROM orders GROUP BY time(5m) END
  
这里创建了一个 CQ,每个5分钟将 two_hours.orders 中的数据计算5分钟的平均值后存入 default.downsampled_orders 中,default 这个 RP 中的数据是永久保存的。

WHERE

查询时指定查询的限制条件,例如查询最近1小时内 host_id=1 的机器的 cpu 数据。

SELECT value FROM cpu_load WHERE time > now() - 1h and host_id = 1
  
GROUP BY

类似于 SQL 中的语法,可以对细粒度数据进行聚合计算,例如查询最近1小时内 host_id=1 的机器的 cpu 的数据,并且采样为每5分钟的平均值。

SELECT mean(value) FROM cpu_load WHERE time > now() - 1h and host_id = 1 GROUP BY time(5m)
  
官方推荐硬件配置

单节点

Load Writes per second Queries per second Unique series
  
Low < 5 thousand < 5 < 100 thousand
  
Moderate < 100 thousand < 25 < 1 million
  
High > 100 thousand > 25 > 1 million
  
Probably infeasible > 500 thousand > 100 > 10 million
  
Low: CPU 2-4, RAM 2-4GB, IOPS 500
  
Moderate: CPU 4-6, RAM 8-32GB, IOPS 500-1000
  
High: CPU CPU 8+, RAM 32GB+, IOPS 1000+
  
Probably infeasible: 可能单机无法支持,需要集群环境
  
集群

InfluxDB 从 0.12 版本开始将不再开源其 cluster 源码,而是被用做提供商业服务。

如果考虑到以后的扩展,需要自己在前端做代理分片或者类似的开发工作。

已知七牛是采用了 InfluxDB 作为时间序列数据的存储,自研了调度器以及高可用模块,具有横向扩展的能力。

总结

目前最火热的时间序列数据库项目,社区开发活跃,迭代更新较快,存储引擎经常变化,网上的一些资料都比较过时,例如最新的 TSM 存储引擎只能看到官方的文档简介,还没有详细的原理说明的文章。

就单机来说,在磁盘占用、cpu使用率、读写速度方面都让人眼前一亮。如果数据量级不是非常大的情况下,单节点的 InfluxDB 就可以承载数十万每秒的写入,是一个比较合适的选择。

另一方面,从 0.12 版本开始不再开源其集群代码 (虽然之前的集群部分就比较烂) ,如果考虑到之后进行扩展的话,需要进行二次开发。

作者: fatedier
  
本文出处: http://blog.fatedier.com/2016/07/05/research-of-time-series-database-influxdb/
  
文章版权归本人所有,欢迎转载,但未经作者同意必须保留此段声明,且在文章页面明显位置给出原文链接,否则保留追究法律责任的权利。

http://blog.fatedier.com/2016/07/05/research-of-time-series-database-influxdb/
>https://zhuanlan.zhihu.com/p/97247465
