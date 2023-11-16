---
title: 内存数据库
author: "-"
date: 2014-01-15T05:05:46+00:00
url: mem-db
categories:
  - database
tags:
  - reprint
---
## 内存数据库

内存数据库,顾名思义就是将数据放在内存中直接操作的数据库。相对于磁盘,内存的数据读写速度要高出几个数量级,将数据保存在内存中相比从磁盘上访问能够极大地提高应用的性能。

内存数据库抛弃了磁盘数据管理的传统方式,基于全部数据都在内存中重新设计了体系结构,并且在数据缓存、快速算法、并行操作方面也进行了相应的改进,所以数据处理速度比传统数据库的数据处理速度要快很多,一般都在10倍以上。内存数据库的最大特点是其"主拷贝"或"工作版本"常驻内存,即活动事务只与实时内存数据库的内存拷贝打交道。
  
定义:设有数据库系统DBS,DB为DBS中的数据库,DBM(t)为在时刻t,DB在内存的数据集,DBM(t)属于DB。TS为DBS中所有可能的事务构成的集合。AT(t)为在时刻t处于活动状态的事务集,AT(t)属于TS。Dt(T)为事务T在时刻t所操作的数据集,
  
Dt(T)属于DB。若在任意时刻t,均有:
  
任意T属于AT(t) Dt(T)属于DBM(t)
  
成立,则称DBS为一个内存数据库系统,简称为MMDBS;DB为一个内存数据库,简称为MMDB。
  
常见的例子有MySQL的MEMORY存储引擎、eXtremeDB、TT、FastDB、SQLite、Microsoft SQL Server Compact,Redis

[http://baike.baidu.com/view/1210875.htm](http://baike.baidu.com/view/1210875.htm)
