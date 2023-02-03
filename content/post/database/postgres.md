---
title: postgres
author: "-"
date: 2022-11-08 15:04:37
url: postgres
categories:
  - database
tags:
  - reprint
---
## postgres

## version

- local: 14.5
- dev: 11.2
- test: 11.2
- prod: 11.14

## install

```bash
podman run --name postgres \
-p 5432:5432 \
-e POSTGRES_PASSWORD=password0 \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v postgres-data:/var/lib/postgresql/data \
-d postgres:14.5

psql -h 127.0.0.1 -p 5432 -U postgres
# password: password0
```

## commands

```bash
# 查看版本
select version();

pacman -S postgresql
psql -h 127.0.0.1 -p 5432 -d database0 -U user0

# create database
CREATE DATABASE foo;

# create table
create table table0(field0 json);

# delete table
DROP TABLE table0;
# 查看字段类型
select column_name, data_type from information_schema.columns where table_name='table0';

\l 或 \list meta-command 列出所有数据库
sudo -u postgres psql -c "\l"
用 \c + 数据库名 来进入数据库：
\dt 列出所有数据库表：

# 查看表结构
\d table0

select * length( "abc"::TEXT)
```

## psql 直接执行 sql

```sql
PGPASSWORD=postgres psql -h 127.0.0.1 -p 5432 -d database0 -U user0  --command 'select version();'
```

## psql 执行sql 文件

```bash
PGPASSWORD=postgres psql -h 127.0.0.1 -p 5432 -d database0 -U user0 -f /path/to/foo.sql
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

## 字符串连接

```sql
string||string
```

## 转义

```sql
-- 单引号转义 ''
UPDATE user SET username = 'Peter''s Name' WHERE id = 1;
```

## to_number

```sql
SELECT to_number('12345', '9999999999999999999')//12345
SELECT to_number('12345', '99999')//12345
SELECT to_number(''||12345, '9999')//1234，由于模式是4位，结果忽略最后一位；
SELECT to_number('    12345', '9999999999999999999')//12345
SELECT to_number('  ab  ,1,2a3,4b5', '9999999999999999999')//12345，会忽略所有字符串中非数字字符

```

## 导出, 备份

```bash
# -h, host 127.0.0.1
# -p, port 5432
# -t, table: table0, 不加 -t 参数时会导出所有表结构
# -s, 不导出数据
# database: database0
pg_dump -h 127.0.0.1 -p 5432 -t table0 -U postgres database0 > foo.sql
pg_dump -h 127.0.0.1 -p 5432 -s -t table0 -U postgres database0 > foo.sql

# 导出并压缩
pg_dump -d db_name | gzip > db.gz
```

## 导入

```bash
psql -h 127.0.0.1 -p 5432 -t table0 -U postgres -d database0 -f foo.sql
```

```sql
CREATE SEQUENCE shipments_ship_id_seq MINVALUE 0;

```

## PostgreSQL 如何删除外键限制

首先找出数据库表的外键名称：

```sql
\d [tablename]
"table_name_id_fkey" FOREIGN KEY (id) REFERENCES other_table(id) ....
-- 然后使用下面的命令删除外键：

ALTER TABLE [tablename] DROP CONSTRAINT table_name_id_fkey;
```

版权声明：本文为CSDN博主「亮子介」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/henryhu712/article/details/104092141>

## 查看外键

查看表结构的时候能看到外键 \d table0

```sql
SELECT
     tc.constraint_name, tc.table_name, kcu.column_name, 
     ccu.table_name AS foreign_table_name,
     ccu.column_name AS foreign_column_name,
     tc.is_deferrable,tc.initially_deferred
FROM
     information_schema.table_constraints AS tc 
     JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
     JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name = 'table0';
```

## postgresql 数据类型

```sql
名字                        别名             描述
character varying [ (n) ]  varchar [ (n) ]  可变长字符串
character [ (n) ]          char [ (n) ]     定长字符串
timestamp                                   SQL标准要求仅仅将timestamp类型等于timestamp without time zone 类型
timestamp with time zone   TIMESTAMPTZ       PostgreSQL遵守这个行为。timestamptz 作为 timestamp with time zone 的缩写被接受；这是PostgreSQL 的一个扩展。
```

## 时区

```sql
show timezone;
select * from pg_timezone_names where abbrev='+04';
set time zone "Asia/Dubai";

select now();
```

## substring

```sql
substring(string [from <str_pos>] [for <ext_char>])
-- str_pos 
```

## table owner

```sql
select * from pg_tables where tablename = 'my_tbl';
```

## lock

```sql
-- 查看锁
SELECT locker.pid,
       pc.relname,
       locker.mode,
       locker_act.application_name,
       least(query_start, xact_start)                        start_time,
       locker_act.state,
       CASE
           WHEN granted = 'f' THEN
               'wait_lock'
           WHEN granted = 't' THEN
               'get_lock'
           END                                               lock_satus,
       current_timestamp - least(query_start, xact_start) AS runtime,
       locker_act.query
FROM pg_locks locker,
     pg_stat_activity locker_act,
     pg_class pc
WHERE locker.pid = locker_act.pid
  AND NOT locker.pid = pg_backend_pid()
  AND application_name <> 'pg_statsinfod'
  AND locker.relation = pc.oid
  AND pc.reltype <> 0 --and pc.relname='t'
ORDER BY runtime desc;

```

```sql
--查看PostgreSQL正在执行的SQL  
SELECT procpid,
       start,
       now() - start AS lap,
       current_query
FROM (SELECT backendid,
             pg_stat_get_backend_pid(S.backendid)            AS procpid,
             pg_stat_get_backend_activity_start(S.backendid) AS start,
             pg_stat_get_backend_activity(S.backendid)       AS current_query
      FROM (SELECT pg_stat_get_backend_idset() AS backendid) AS S) AS S,
     pg_stat_activity pa
WHERE current_query <> '<IDLE>'
  and procpid <> pg_backend_pid()
  and pa.pid = s.procpid
  and pa.state <> 'idle'
ORDER BY lap DESC;

```

```bash
--查找是否有waiting  
ps -ef|grep postgres | grep wait  
```

```sql
--查看当前库表和索引的的大小并排序显示前20条  
SELECT nspname,
       relname,
       relkind                                       as "type",
       pg_size_pretty(pg_table_size(C.oid))          AS size,
       pg_size_pretty(pg_indexes_size(C.oid))        AS idxsize,
       pg_size_pretty(pg_total_relation_size(C.oid)) as "total"
FROM pg_class C
         LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
WHERE nspname NOT IN ('pg_catalog', 'information_schema')
  AND nspname !~ '^pg_toast'
  AND relkind IN ('r', 'i')
ORDER BY pg_total_relation_size(C.oid) DESC
LIMIT 20;

```
