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

## bigserial

postgresql序列号（SERIAL）类型包括smallserial（smallint,short）,serial(int)和bigserial(bigint,long long int)，不管是smallserial,serial还是bigserial，其范围都是(1,9223372036854775807)，但是序列号类型其实不是真正的类型，当声明一个字段为序列号类型时其实是创建了一个序列，INSERT时如果没有给该字段赋值会默认获取对应序列的下一个值。

## psql 直接执行 sql

```sql
PGPASSWORD=postgres psql -h 127.0.0.1 -p 5432 -d database0 -U user0  --command 'select version();'
```

## 日期格式化

```sql
SELECT to_char(NOW(), 'YYYY-MM-DD HH24:MI:SS')

```

## 日期时间计算

```sql
select now() + interval '1 days'; 
select now() + interval '1 month'; 
select now() + interval '1 years'; 
select NOW(), NOW() - interval '1 hours 4 minutes';
```
