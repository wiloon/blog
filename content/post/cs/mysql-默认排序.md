---
title: MySQL 默认排序
author: "-"
date: 2019-10-29T09:50:52+00:00
url: /?p=15081
categories:
  - Inbox
tags:
  - reprint
---
## MySQL 默认排序
不加order by 的情况 下, 顺序 不能保证, 不同存储引擎, 有过增删改操作 都有可能 影响默认顺序, 默认排序只依赖于内部实现, 不同版本的MySQL也有可能 不同.
  
所以不能依赖默认排序.
  
https://my.oschina.net/alarm1673/blog/1814508
  
https://stackoverflow.com/questions/8746519/sql-what-is-the-default-order-by-of-queries