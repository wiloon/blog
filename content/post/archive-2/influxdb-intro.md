---
title: 时间序列数据库
author: "-"
date: 2017-08-02T02:45:50+00:00
url: /?p=10977
categories:
  - Database
tags:
  - reprint
---
## 时间序列数据库

存储大量时间相关的数据(如日志，用户行为等)
创造了一种新型的数据库分类——时间序列数据库(Time Series Database).
时间序列数据库主要用于指处理带时间标签 (按照时间的顺序变化，即时间序列化）的数据，带时间标签的数据也称为时间序列数据。

### influxdb

influxdb是最新的一个时间序列数据库,最新一两年才产生,但已经拥有极高的人气。influxdb 是用Go写的,现在v0.9正在开发中,之前开源出来的最稳定的版本是0.88的,但是0.8X是没有集群方案的,但在0.9中会加入进来。

0.9版本的influxdb对于之前会有很大的改变,后端存储有LevelDB换成了BoltDB,读写的API也是有了很大的变化,也将支持集群化,continuous query,支持retention policy,读写性能也是哇哇的,可以说是时间序列存储的完美方案,但是由于还很年轻,可能还会存在诸多的问题,就像现在正在开发的0.9一样,发布一拖再拖,就是由于还有些技术壁垒没有攻陷。

对于influxdb我不想多说些什么,之后打算开一个专题,专门详细来说一说这个玩意,因为我看国内几乎没有详细的文章来讲influxdb的。

<http://www.opscoder.info/tsdb.html>

对于时间序列的存储,一般会采用专门的时间序列数据库,而不会去使用MySQL或是mongo(但zabbix就是用的MySQL,所以它在IO上面遇到了瓶颈)。现在时间序列的数据库是有很多的,比如graphite、opentsdb以及新生的influxdb。最近也相继研究了一下这三个数据库,现在把研究所得记录下来。

特性：

高效的时间序列数据写入性能。自定义TSM引擎，快速数据写入和高效数据压缩。
无额外存储依赖。
简单，高性能的HTTP查询和写入API。
以插件方式支持许多不同协议的数据摄入，如：graphite，collectd，和openTSDB
SQL-like查询语言，简化查询和聚合操作。
索引Tags，支持快速有效的查询时间序列。
保留策略有效去除过期数据。
连续查询自动计算聚合数据，使频繁查询更有效。

influxDB 不支持数据库的更新操作，毕竟时间数据只能随着时间产生新数据，肯定无法对过去的数据修改。

适合于写多读少的场景

### graphite
  
graphite算是一个老牌的时间序列存储解决方案了,graphite由三个部分组成,分别是carbon、whisper和graphite web

carbon:实际上是一系列守护进程,这些守护进程用Twisted的事件驱动网络引擎监听时间序列数据。Twisted框架让Carbon守护进程能够以很低的开销处理大量的客户端和流量。
  
whisper:是一个用于存储时间序列数据的数据库,之后应用程序可以用create,update和fetch操作获取并操作这些数据。
  
graphite web:使用django开发的一套web,提供一些常用的聚合函数,可以界面友好的展示出图形。再盗图:

whisper支持RRD,可以很方便的定义retention,以及定义storage scheme,不需要手动做,graphite会自动帮你按照不同的scheme实现aggregation。这样每个metric的大小就是固定的了,所以理论上可以永久存储数据。graphite的集群方案主要有两种,分别是使用graphite自带的relay或是使用第三方的工具。

当使用自带的relay时,只需要在配置文件中配置要relay到哪些机器即可,这样在数据写入的时候,被写入的节点会relay一份到这些机器中。在读取的时候,在graphite web的settings中配置HOSTS的列表,这样在django的web中会依次从这些HOSTS中读出数据。

另一种是需用第三方的relay工具,Booking公司开源出来了他们所用的用C写得 carbon-c-relay,以及用GO写得carbon-relay-ng。其基本的思想是运用一致性哈希,可以将不同的metric发到不同的机器,以来达到集群的目的,据Booking称他们的graphite集群的规模达到了百台机器,而mertic也达到了百万的级别.

以上的两种方式都会遇到了一个共同的问题,就是集群扩容的问题,我不知道Booking是怎么来解决这个问题的,但是我这边目前是想到了几种方式,这个在我前一篇的文章中已经阐述了: graphite集群扩容方案探究,在这里就先不赘述了。

最后说一下,除了集群问题以外,graphite的还有一性能问题就是读的性能稍差,这决定于其存储的方式,其实在读的时候会去读whisper文件(虽然在django层做了缓存,但是缓存的功能比较弱),通过seek的方式来获取数据的位置,在将数据取出。

### opentsdb

Opentsdb是一个基于Hbase的时间序列数据库 (新版也支持Cassandra）。
其基于Hbase的分布式列存储特性实现了数据高可用，高性能写的特性。受限于Hbase，存储空间较大，压缩不足。依赖整套 HBase, ZooKeeper
采用无模式的tagset数据结构(sys.cpu.user 1436333416 23 host=web01 user=10001)
结构简单，多value查询不友好
HTTP-DSL查询
opentsdb是一个比较重的时间序列解决方案,为什么说他重呢？因为它的组成是这样的:

可以看到opentsdb所依赖的存储是Hbase集群。TSD在其中担任的责任是IO部分,TSD其实就是一个后台的daemon,一般我会会用一组TSD达成一个TSD的集群 (其实不能算是集群) ,没有master/slave之分,也没有共享状态,然后在之前用LB设备来做负载均衡,官方比较推荐的是用varnish。

当让后端的存储也可以用其他的例如hadoop,但是官方还是建议用Hbase,因为opentsdb就是Hbase社区孵化出来的产品。那么问题来了,Hbase的运维将是一个艰巨的任务,这个依赖于 zookeeper 搭建的集群的坑还是很多的,我看了一下官方文档就有上千页。这里面的优化维护需要有专业的Hbase专家才能完成。

另外opentsdb做不到graphite那样自动做downsample,也就是做不到RRD那样地去存储数据,需要在外面自己做一层手动干这活,再把聚合后的数据写入Hbase,唉,还真是一个费时费力的活。

除此之外opentsdb还是很不错的,读写性能挺高,而且支持tag,支持ttl,支持各种聚合函数。现在很多的监控的metric的存储都是用的opentsdb,嗯,是的,只要有能力玩转还是个不错的选择。

### Timescale

基于传统关系型数据库postgresql改造的时间序列数据库
一款兼容sql的时序数据库， 底层存储架构在postgresql上。 作为一个postgresql的扩展提供服务。

PostgreSQL原生支持的所有SQL,包含完整SQL接口 (包括辅助索引，非时间聚合，子查询，JOIN，窗口函数）
用PostgreSQL的客户端或工具，可以直接应用到该数据库，不需要更改。
时间为导向的特性，API功能和相应的优化。
可靠的数据存储。
扩展：

透明时间/空间分区，用于放大 (单个节点）和扩展
高数据写入速率 (包括批量提交，内存中索引，事务支持，数据备份支持)
单个节点上的大小合适的块 (二维数据分区），以确保即使在大数据量时即可快速读取。
块之间和服务器之间的并行操作
劣势：

因为TimescaleDB没有使用列存技术，它对时序数据的压缩效果不太好，压缩比最高在4X左右
目前暂时不完全支持分布式的扩展 (正在开发相关功能），所以会对服务器单机性能要求较高

### Elasticsearch

Elasticsearch 是一个分布式的开源搜索和分析引擎，适用于所有类型的数据，包括文本、数字、地理空间、结构化和非结构化数据。Elasticsearch 在 Apache Lucene 的基础上开发而成，由 Elasticsearch N.V. (即现在的 Elastic）于 2010 年首次发布。Elasticsearch 以其简单的 REST 风格 API、分布式特性、速度和可扩展性而闻名。

Elasticsearch以ELK stack被人所熟知。许多公司基于ELK搭建日志分析系统和实时搜索系统。之前我们在ELK的基础上开始开发metric监控系统。即想到了使用Elasticsearch来存储时间序列数据库。对Elasticserach的mapping做相应的优化，使其更适合存储时间序列数据模型，收获了不错的效果，完全满足了业务的需求。后期发现Elasticsearch新版本竟然也开始发布Metrics组件和APM组件，并大量的推广其全文检索外，对时间序列的存储能力。真是和我们当时的想法不谋而合。

><https://blog.csdn.net/weixin_33584986/article/details/113386980>
><https://zhuanlan.zhihu.com/p/111511463>
