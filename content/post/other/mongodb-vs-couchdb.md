---
title: MongoDB vs CouchDB
author: "-"
date: 2014-02-19T05:54:45+00:00
url: /?p=6257
categories:
  - Inbox
tags:
  - MongoDB
  - NoSQL

---
## MongoDB vs CouchDB

<http://database.51cto.com/art/201103/249990.htm>

本文见于MongoDB官方网站,MongoDB与CouchDB很相似,他们都是文档型存储,数据存储格式都是JSON型的,都使用Javascript进行操作,都支持Map/Reduce。但是其实二者有着很多本质的区别,本文透过现象追寻本质,让你更好的理解MongoDB与CouchDB。

**1.MVCC (Multiversion concurrency control)**

MongoDB与CouchDB的一大区别就是CouchDB是一个MVCC的系统,而MongoDB是一个update-in-place的系统。这二者的区别就是,MongoDB进行写操作时都是即时完成写操作,写操作成功则数据就写成功了,而CouchDB一个支持多版本控制的系统,此类系统通常支持多个结点写,而系统会检测到多个系统的写操作之间的冲突并以一定的算法规则予以解决。

**2.水平扩展性**

在扩展性方面,CouchDB使用replication去做,而MongoDB的replication仅仅用来增强数据的可靠性,MongoDB在实现水平扩展性方面使用的是Sharding。 (据说CouchDB也有开发分片功能的计划)

**3.数据查询操作**

这个区别在用户接口上了,MongoDB与传统的数据库系统类似,支持动态查询,即使在没有建立索引的行上,也能进行任意的查询。而CouchDB不同,CouchDB不支持动态查询,你必须为你的每一个查询模式建立相应的view,并在此view的基础上进行查询。

**4.原子性**

这一点上两者比较一致,都支持针对行的原子性修改 (concurrent modifications of single documents) ,但不支持更多的复杂事务操作。

**5.数据可靠性**

CouchDB是一个"crash-only"的系统,你可以在任何时候停掉CouchDB并能保证数据的一致性。而MongoDB在不正常的停掉后需要运repairDatabase()命令来修复数据文件,在1.7.5版本后支持单机可靠的–dur命令。

**6.Map/Reduce**

MongoDB和CouchDB都支持Map/Reduce,不同的是MongoDB只有在数据统计操作中会用到,而CouchDB在变通查询时也是使用Map/Reduce。

**7.使用 javascript**

MongoDB和CouchDB都支持javascript,CouchDb用javascript来创建view。MongoDB使用JSON作为普通数据库操作的表达式。当然你也可以在操作中包含javascript语句。MongoDB还支持服务端的javascript脚本 (running arbitrary javascript functions server-side) ,当然,MongoDB的Map/Reduce函数也是javascript格式的。

**8.REST**

CouchDB是一个RESTFul的数据库,其操作完全走HTTP协议,而MongoDB是走的自己的二进制协议。MongoDB Server在启动时可以开放一个HTTP的接口供状态监控。

**9.性能**

此处主要列举了MongoDB自己具有高性能的原因

采用二进制协议,而非CouchDB REST的HTTP协议

使用Momary Map内存映射的做法

collection-oriented,面向集合的存储,同一个collection的数据是连续存储的

update-in-place直接修改,而非使用MVCC的机制

使用C++编写

**10.适用场景**

如果你在构建一个 Lotus Notes型的应用,我们推荐使用CouchDB,主要是由于它的MVCC机制。另外如果我们需要master-master的架构,需要基于地理位置的数据分布,或者在数据结点可能不在线的情况下,我们推荐使用CouchDB。

如果你需要高性能的存储服务,那我们推荐MongoDB,比如用于存储大型网站的用户个人信息,比如用于构建在其它存储层之上的Cache层。

如果你的需求中有大量update操作,那么使用MongoDB吧。就像我们在例子updating real time analytics counters中的一样,对于那种经常变化的数据,比如浏览量,访问数之类的数据存储。
