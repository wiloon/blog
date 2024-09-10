---
title: MySQL 函数
author: "-"
date: 2011-04-16T09:33:27+00:00
url: /?p=59
categories:
  - DataBase
tags:
  - MySQL

---
## MySQL 函数
```sql
MySQL> select date_format(now(),'%Y-%m-%d');
MySQL> select time_format(now(),'%H-%i-%S');

-- 连接字符串, CONCAT
select CONCAT('My', 'S', 'QL');

```