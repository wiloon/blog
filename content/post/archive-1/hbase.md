---
title: HBase
author: "-"
date: 2015-01-07T06:55:32+00:00
url: /?p=7192
categories:
  - Uncategorized
tags:
  - Hbase

---
## HBase
HBase是一个开源的非关系型分布式数据库 (NoSQL) ，该技术来源于 Fay Chang 所撰写的Google论文"Bigtable: 一个结构化数据的分布式存储系统"。l就像Bigtable利用了Google文件系统 (File System) 所提供的分布式数据存储一样，HBase在Hadoop之上提供了类似于Bigtable的能力。HBase是Apache的Hadoop项目的子项目。HBase不同于一般的关系数据库，它是一个适合于非结构化数据存储的数据库。另一个不同的是HBase基于列的而不是基于行的模式。

HBase – Hadoop Database，是一个高可靠性、高性能、面向列、可伸缩的分布式存储系统，利用HBase技术可在廉价PC Server上搭建起大规模结构化存储集群。
  
与FUJITSU Cliq等商用大数据产品不同，HBase是Google Bigtable的开源实现，类似Google Bigtable利用GFS作为其文件存储系统，HBase利用Hadoop HDFS作为其文件存储系统；Google运行MapReduce来处理Bigtable中的海量数据，HBase同样利用Hadoop MapReduce来处理HBase中的海量数据；Google Bigtable利用 Chubby作为协同服务，HBase利用Zookeeper作为对应。
  
上图描述Hadoop EcoSystem中的各层系统。其中,HBase位于结构化存储层，Hadoop HDFS为HBase提供了高可靠性的底层存储支持，Hadoop MapReduce为HBase提供了高性能的计算能力，Zookeeper为HBase提供了稳定服务和 failover 机制。

此外，Pig和Hive还为HBase提供了高层语言支持，使得在HBase上进行数据统计处理变的非常简单。 Sqoop则为HBase提供了方便的RDBMS数据导入功能，使得传统数据库数据向HBase中迁移变的非常方便。

./hbase shell
  
get 'table name','row key'

https://www.ibm.com/developerworks/cn/analytics/library/ba-cn-bigdata-hbase/index.html
### bigtable
>https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf