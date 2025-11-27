---
title: 分布式ID, 雪花算法
author: "-"
date: 2011-11-12T08:12:59+00:00
url: /?p=1512
categories:
  - Emacs
tags:
  - reprint
---
## 分布式ID, 雪花算法
>https://zhuanlan.zhihu.com/p/85837641

雪花算法这一在分布式架构中很常见的玩意，但一般也不需要怎么去深入了解，一方面一般个人项目用不到分布式之类的大型架构，另一方面，就算要用到，市面上很多ID生成器也帮我们完成了这项工作。

分布式ID的特点
全局唯一性
不能出现有重复的ID标识，这是基本要求。

递增性
确保生成ID对于用户或业务是递增的。

高可用性
确保任何时候都能生成正确的ID。

高性能性
在高并发的环境下依然表现良好。

分布式ID的常见解决方案
UUID
Java自带的生成一串唯一随机36位字符串 (32个字符串+4个“-”）的算法。它可以保证唯一性，且据说够用N亿年，但是其业务可读性差，无法有序递增。

SnowFlake
今天的主角雪花算法，它是Twitter开源的由64位整数组成分布式ID，性能较高，并且在单机上递增。 具体参考：

https://github.com/twitter-archive/snowflake
UidGenerator
UidGenerator是百度开源的分布式ID生成器，其基于雪花算法实现。 具体参考：

https://github.com/baidu/uid-generator/blob/master/README.zh_cn.md
Leaf
Leaf是美团开源的分布式ID生成器，能保证全局唯一，趋势递增，但需要依赖关系数据库、Zookeeper等中间件。 具体参考：

https://tech.meituan.com/MT_Leaf.html
雪花算法的概要
SnowFlake是Twitter公司采用的一种算法，目的是在分布式系统中产生全局唯一且趋势递增的ID。

组成部分 (64bit）
1.第一位 占用1bit，其值始终是0，没有实际作用。 2.时间戳 占用41bit，精确到毫秒，总共可以容纳约69年的时间。 3.工作机器id 占用10bit，其中高位5bit是数据中心ID，低位5bit是工作节点ID，做多可以容纳1024个节点。 4.序列号 占用12bit，每个节点每毫秒0开始不断累加，最多可以累加到4095，一共可以产生4096个ID。

SnowFlake算法在同一毫秒内最多可以生成多少个全局唯一ID呢：： 同一毫秒的ID数量 = 1024 X 4096 = 4194304
