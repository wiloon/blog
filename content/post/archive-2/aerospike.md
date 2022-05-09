---
title: Aerospike
author: "-"
date: 2019-02-16T10:35:04+00:00
url: /?p=13602
categories:
  - Inbox
tags:
  - reprint
---
## Aerospike
什么是Aerospike (AS)         Aerospike是一个分布式,高可用的 K-V类型的Nosql数据库。提供类似传统数据库的ACID操作。二、为什么要用AS          K-V类型的数据库必须要提的就是redis,redis数据完全存储在内存虽然保证了查询性能,但是成本太高。AS最大的卖点就是可以存储在SSD上,并且保证和redis相同的查询性能。AS内部在访问SSD屏蔽了文件系统层级,直接访问地址,保证了数据的读取速度。 AS同时支持二级索引与聚合,支持简单的sql操作,相比于其他nosql数据库,有一定优势。

https://www.jianshu.com/p/8d843d7a6a27