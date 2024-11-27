---
title: MySQL默认排序
author: "-"
date: 2016-01-12T03:14:03+00:00
url: /?p=8664
categories:
  - Inbox
tags:
  - reprint
---
## MySQL默认排序
SELECT * FROM tbl -- this will do a "table scan". If the table has never had any DELETEs/REPLACEs/UPDATEs, the records will happen to be in the insertion order, hence what you observed. 
大致意思为,一个myisam引擎表在没有任何的删除,修改操作下,执行 select 不带order by,那么会按照插入顺序进行排序。

If you had done the same statement with an InnoDB table, they would have been delivered in PRIMARY KEY order, not INSERT order. Again, this is an artifact of the underlying implementation, not something to depend on.
对于innodb引擎表来说,在相同的情况下,select 不带order by,会根据主键来排序,从小到大