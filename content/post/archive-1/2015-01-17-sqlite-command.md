---
title: sqlite command
author: "-"
type: post
date: 2015-01-17T04:46:52+00:00
url: /?p=7250
categories:
  - Uncategorized
tags:
  - Sqlite

---
# sqlite command
```bash
sudo pacman -S sqlite
```

在列模式下，每条记录在一个单独的行中以数据列对齐的方式显示。列如: 

sqlite> .mode column

显示 列名.header on

查出所有的表: 
  
select name from sqlite_master where type='table' order by name;

通过以下语句可查询出某个表的所有字段信息
  
PRAGMA table_info([tablename])

cur.execute("PRAGMA table_info(table)")
  
print cur.fetchall()
  
http://duduhehe.iteye.com/blog/1344858
  
http://www.cnblogs.com/riskyer/p/3333809.html