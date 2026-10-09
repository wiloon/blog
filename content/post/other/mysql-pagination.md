---
title: MySQL 分页
author: lcf
date: 2012-11-15T08:22:40+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: mysql-pagination
categories:
  - Database
tags:
  - mysql
  - remix
  - AI-assisted
aliases:
  - /mysql高效分页/
---
## MySQL 分页
一般MySQL最基本的分页方式: 

select * from content order by id desc limit 0, 10

在中小数据量的情况下，这样的SQL足够用了，唯一需要注意的问题就是确保使用了索引。随着数据量的增加，页数会越来越多，查看后几页的SQL就可能类似: 

select * from content order by id desc limit 10000, 10

一言以蔽之，就是越往后分页，LIMIT语句的偏移量就会越大，速度也会明显变慢。

此时，我们可以通过2种方式: 
  
一，子查询的分页方式来提高分页效率，SQL语句如下: 
  
SELECT * FROM `content` WHERE id <=
  
(SELECT id FROM `content` ORDER BY id desc LIMIT ".($page-1)*$pagesize.", 1) ORDER BY id desc LIMIT $pagesize

为什么会这样呢？因为子查询是在索引上完成的，而普通的查询时在数据文件上完成的，通常来说，索引文件要比数据文件小得多，所以操作起来也会更有效率。 (via) 通过explain SQL语句发现: 子查询使用了索引！

id select_type table type possible_keys key key_len ref rows Extra
  
1 PRIMARY content range PRIMARY PRIMARY 4 NULL 6264 Using where
  
2 SUBQUERY content index NULL PRIMARY 4 NULL 27085 Using index

经实测，使用子查询的分页方式的效率比纯LIMIT提高了14-20倍！

二，JOIN分页方式
  
SELECT * FROM `content` AS t1
  
JOIN (SELECT id FROM `content` ORDER BY id desc LIMIT ".($page-1)*$pagesize.", 1) AS t2
  
WHERE t1.id <= t2.id ORDER BY t1.id desc LIMIT $pagesize;
  
经过我的测试，join分页和子查询分页的效率基本在一个等级上，消耗的时间也基本一致。explain SQL语句: 

```text
id select_type table type possible_keys key key_len ref rows Extra
1 PRIMARY <derived2> system NULL NULL NULL NULL 1
1 PRIMARY t1 range PRIMARY PRIMARY 4 NULL 6264 Using where
2 DERIVED content index NULL PRIMARY 4 NULL 27085 Using index
```

https://leo108.com/pid-1914/

MySQL order by与limit混用陷阱
  
http://www.jianshu.com/p/ead491db9749
  
https://dev.MySQL.com/doc/refman/5.7/en/limit-optimization.html

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `mysql-pagination.md`；url 改为 `mysql-pagination`；旧 url 加入 aliases | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
