---
title: postgresql
author: "-"
date: 2017-12-31T06:25:26+00:00
url: postgresql
categories:
  - database
tags:
  - reprint
---
## postgresql

```bash
pacman -S postgresql
psql -h 127.0.0.1 -p 5432 -d database0 -U user0
```

## 查主键

```sql
--查询主键名称
SELECT
    pg_constraint.conname AS pk_name
FROM
    pg_constraint
INNER JOIN pg_class ON pg_constraint.conrelid = pg_class.oid
WHERE
    pg_class.relname = 'table_name_0'
AND pg_constraint.contype = 'p';
--查询主键的详细信息
SELECT
    pg_constraint.conname AS pk_name,
    pg_attribute.attname AS colname,
    pg_type.typname AS typename
FROM
    pg_constraint
INNER JOIN pg_class ON pg_constraint.conrelid = pg_class.oid
INNER JOIN pg_attribute ON pg_attribute.attrelid = pg_class.oid
AND pg_attribute.attnum = pg_constraint.conkey [ 1 ]
INNER JOIN pg_type ON pg_type.oid = pg_attribute.atttypid
WHERE
    pg_class.relname = 'table_name_0'
AND pg_constraint.contype = 'p';


```
