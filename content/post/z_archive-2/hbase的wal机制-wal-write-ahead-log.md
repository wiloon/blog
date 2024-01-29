---
title: HBase的WAL机制 WAL (Write-Ahead-Log)
author: "-"
date: 2017-05-09T02:03:37+00:00
url: /?p=10265
categories:
  - Inbox
tags:
  - reprint
---
## HBase的WAL机制 WAL (Write-Ahead-Log)
WAL机制解析

WAL(Write-Ahead Logging)是一种高效的日志算法,几乎是所有非内存数据库提升写性能的不二法门,基本原理是在数据写入之前首先顺序写入日志,然后再写入缓存,等到缓存写满之后统一落盘。之所以能够提升写性能,是因为WAL将一次随机写转化为了一次顺序写加一次内存写。提升写性能的同时,WAL可以保证数据的可靠性,即在任何情况下数据不丢失。假如一次写入完成之后发生了宕机,即使所有缓存中的数据丢失,也可以通过恢复日志还原出丢失的数据。

WAL持久化等级

HBase中可以通过设置WAL的持久化等级决定是否开启WAL机制、以及HLog的落盘方式。WAL的持久化等级分为如下四个等级: 

1. SKIP_WAL: 只写缓存,不写HLog日志。这种方式因为只写内存,因此可以极大的提升写入性能,但是数据有丢失的风险。在实际应用过程中并不建议设置此等级,除非确认不要求数据的可靠性。 
2. ASYNC_WAL: 异步将数据写入HLog日志中。
3. SYNC_WAL: 同步将数据写入日志文件中,需要注意的是数据只是被写入文件系统中,并没有真正落盘。
4. FSYNC_WAL: 同步将数据写入日志文件并强制落盘。最严格的日志写入等级,可以保证数据不会丢失,但是性能相对比较差。
5. USER_DEFAULT: 默认如果用户没有指定持久化等级,HBase使用SYNC_WAL等级持久化数据。

用户可以通过客户端设置WAL持久化等级,代码: put.setDurability(Durability. SYNC_WAL );

HLog数据结构

HBase中,WAL的实现类为HLog,每个Region Server拥有一个HLog日志,所有region的写入都是写到同一个HLog。下图表示同一个Region Server中的3个 region 共享一个HLog。当数据写入时,是将数据对<HLogKey,WALEdit>按照顺序追加到HLog中,以获取最好的写入性能。

WAL(Write-Ahead-Log)预写日志是HBase的RegionServer在处理数据插入和删除的过程中用来记录操作内容的一种日志。在每次Put、Delete等一条记录时,首先将其数据写入到RegionServer对应的HLog文件的过程。

客户端往RegionServer端提交数据的时候,会先写WAL日志,只有当WAL日志写成功以后,客户端才会被告诉提交数据成功,如果写WAL失败会告知客户端提交失败,换句话说这其实是一个数据落地的过程。
  
在一个RegionServer上的所有的Region都共享一个HLog,一次数据的提交是先写WAL,写入成功后,再写memstore。当memstore值到达一定是,就会形成一个个StoreFile (理解为HFile格式的封装,本质上还是以HFile的形式存储的) 。

HLog类

RegionServer内WAL文件与Region的关系图
  
WAL的实现类是HLog,当一个Region被初始化的时候,一个HLog的实例会作为构造函数的参数传进去。
  
当Region在处理Put、Delete等更新操作时,可以直接使用该共享的HLog的append方法来落地数据。
  
Put、Delete在客户端上可以通过setWriteToWAL(false)方法来关闭该操作的日志,这么做虽然可以提升入库速度,但最好别这么做,因为有数据丢失的风险存在。

http://www.zkread.com/article/69288.html

http://hbasefly.com/2016/03/23/hbase_writer/