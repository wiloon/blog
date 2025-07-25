---
title: PostgreSQL
author: "-"
date: 2022-11-08 15:04:37
url: PostgreSQL
categories:
  - database
tags:
  - reprint
---
## PostgreSQL

## commands

```
\l 或 \list meta-command 列出所有数据库
sudo -u postgres psql -c "\l"
用 \c + 数据库名 来进入数据库：
\dt 列出所有数据库表：

# 查看表结构
\d table0

# 比上面多几个字段 Storage  | Stats target | Description
\d+ table0

# Turn off printing of column names and result row count footers, etc. This is equivalent to \t or \pset tuples_only.
\t tuples only on/off, tuples only on 的时候 select 语句的输出不带 header

\h
\?

\du 列出所有的用户
```

```bash
# 创建用户 
CREATE USER user_0 WITH PASSWORD 'password_0';
# create database, 所有者 user_0
create database database_0 OWNER user_0;
psql -h 192.168.1.100 -p 5432 -U user_0 -d database_0

PGPASSWORD=password_0 psql -h 192.168.1.100 -p 5432 -U user_0 -d database_0 --command 'select version();'

#当表没有其他关系时
TRUNCATE TABLE tablename;
#当表中有外键时，要用级联方式删所有关联的数据
TRUNCATE TABLE tablename CASCADE;

# 查看 表大小
select pg_size_pretty(pg_relation_size('table0'));

# 查看配置文件路径, 切换到 postgres 用户执行
psql -c "show config_file"

# 查看版本
select version();

pacman -S postgresql
psql -h 127.0.0.1 -p 5432 -d database0 -U user0



# create table
create table test(id int, c1 int);
create table table0(field0 json);

# delete table
DROP TABLE table0;
# 查看字段类型
select column_name, data_type from information_schema.columns where table_name='table0';


select * length( "abc"::TEXT)
insert into test select generate_series(1,10000), random()*10;
```


## 导入/导出

### export, 导出, 备份

```Bash
# https://www.postgresql.org/download/linux/ubuntu/
# install pg_dump
sudo apt install -y postgresql-common

# This script will enable the PostgreSQL APT repository on apt.postgresql.org
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh

# ubuntu install pg_dump
sudo apt-get install postgresql-client-17
```

```bash

# -h, host 127.0.0.1
# -p, port 5432
# -t, table: table0, 不加 -t 参数时会导出所有表结构
# -s, 不导出数据
# database: database0
# -F : 指定输出文件的格式，它可以是以下格式之一： c: 自定义格式 d: 目录格式存档 t: tar 文件包 p: SQL 脚本文件
# -W 命令执行时提示输入用户密码（不会直接在命令中写密码）。
pg_dump -h 127.0.0.1 -U username -W -F t db_name > foo.tar

# 导入
# -c --clean	创建数据库对象前先清理（删除）它们。
pg_restore -h 127.0.0.1 -U username -W -d db_name -c foo.tar

pg_dump -h 127.0.0.1 -p 5432 -t table_0 -U postgres database0 > foo.sql
pg_dump -h 127.0.0.1 -p 5432 -s -t table_0 -U postgres database0 > foo.sql

# 导出并压缩
pg_dump -d db_name | gzip > db.gz

pg_dump -a -t table_0 "host=127.0.0.1 hostaddr=127.0.0.1 port=5432 user=user_0 password=password_0 dbname=db_0"
# export insert sql
pg_dump -a -t table_0 "host=127.0.0.1 hostaddr=127.0.0.1 port=5432 user=user_0 password=password_0 dbname=db_0" --inserts
```

### 导入

```bash
# sql
psql -h 127.0.0.1 -p 5432 -t table0 -U postgres -d database0 -f foo.sql

# csv, https://stackoverflow.com/questions/26701735/extra-data-after-last-expected-column-while-trying-to-import-a-csv-file-into-p
\COPY agency (agency_name, agency_url, agency_timezone) FROM 'myFile.txt' CSV HEADER DELIMITER ',';

```

### 导出指定的行

https://stackoverflow.com/questions/12815496/export-specific-rows-from-a-postgresql-table-as-insert-sql-script

```Bash
# 按过滤条件导出成 csv, 注意: copy 里面的 select SQL 结尾不能有分号
COPY (
SELECT * FROM nyummy.cimory WHERE city = 'tokio'
) TO '/tmp/foo.csv';

# 导入 csv
COPY table_0 FROM '/tmp/foo.csv';
```


## create user

```Bash
CREATE USER user_0 WITH PASSWORD 'password_0';
CREATE DATABASE db_0 OWNER user_0;
GRANT ALL PRIVILEGES ON DATABASE db_0 TO user_0;
```

## postgresql.conf, postgresql log, 日志, sql 历史

```bash
# 查看配置文件路径, ubuntu 24.04 apt 安装的 postgresql
sudo -u postgres psql -c "SHOW config_file;"
```

[https://www.cnblogs.com/qianxunman/p/12149586.html](https://www.cnblogs.com/qianxunman/p/12149586.html)

default log path: /var/lib/postgresql/data/pgdata/log/

PG 安装完成后默认不会记录日志，必须修改对应的 `${PGDATA}/postgresql.conf` 配置才可以

`${PGDATA}` 的值取自 docker 或系统的环境变量 `PGDATA`

```Bash
# 默认值: off, 改成 on 之后重启 postgresql 就开始写日志了, 日志目录会是 /var/lib/postgresql/data/pgdata/log/
logging_collector = on

# none, ddl, mod, all ---- 控制记录哪些 SQL 语句。
# none 不记录，(默认值)
# ddl 记录所有数据定义命令，比如 CREATE, ALTER, 和 DROP 语句。
# mod 记录所有 ddl 语句, 加上数据修改语句 INSERT,UPDATE等,
# all 记录所有执行的语句，将此配置设置为all可跟踪整个数据库执行的SQL语句。
log_statement = 'all'

# 日志目录名, 默认值: log, 使用默认值, 不需要修改
# log_directory = 'log'

# 默认文件名, 使用默认值, 不需要修改
#log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'

log_rotation_age = 1d ----  单个日志文件的生存期，默认 1 天，在日志文件大小没有达到 log_rotation_size 时，一天只生成一个日志文件
log_rotation_size = 10MB  ---- 单个日志文件的大小，如果时间没有超过 log_rotation_age，一个日志文件最大只能到 10M，否则将新生成一个日志文件。
log_truncate_on_rotation = off ---- 当日志文件已存在时，该配置如果为off，新生成的日志将在文件尾部追加，如果为on，则会覆盖原来的日志。
log_duration = off ---- 记录每条SQL语句执行完成消耗的时间，将此配置设置为 on, 用于统计哪些 SQL 语句耗时较长。

10.log_min_duration_statement = -1 # -1 is disabled, 0 logs all statements and their durations, > 0 logs only statements running at least this number of milliseconds

# -1表示不可用，0将记录所有SQL语句和它们的耗时，>0只记录那些耗时超过（或等于）这个值（ms）的SQL语句。个人更喜欢使用该配置来跟踪那些耗时较长，可能存在性能问题的SQL语句。虽然使用log_statement和log_duration也能够统计SQL语句及耗时，但是SQL语句和耗时统计结果可能相差很多行，或在不同的文件中，但是log_min_duration_statement会将SQL语句和耗时在同一行记录，更方便阅读。

11.log_connections = off ----是否记录连接日志
12.log_disconnections = off ---- 是否记录连接断开日志

13.log_line_prefix = '%m %p %u %d %r ' ---- 日志输出格式（%m,%p实际意义配置文件中有解释）,可根据自己需要设置（能够记录时间，用户名称，数据库名称，客户端IP和端口，方便定位问题）
14.log_timezone = 'Asia/Shanghai' ---- 日志时区，最好和服务器设置同一个时区，方便问题定位
```

### timezone

```Bash
timezone = 'Asia/Shanghai'
```

### 重新加载配置文件

```Bash
pg_ctl reload
```

[https://www.cnblogs.com/alianbog/p/5596921.html](https://www.cnblogs.com/alianbog/p/5596921.html)

log_statement = 'none' to log_statement = 'all'

Optional: SELECT set_config('log_statement', 'all', true);

sudo /etc/init.d/postgresql restart or sudo service postgresql restart

Fire query in postgresql select 2+2

Find current log in /var/lib/pgsql/9.2/data/pg_log/

The log files tend to grow a lot over a time, and might kill your machine. For your safety, write a bash script that'll delete logs and restart postgresql server.

## version

- local: 14.5
- dev: 11.2
- test: 11.2
- prod: 11.14

## TO_DATE, to_timestamp

YYYY	year (4 and more digits)
MM	month number (01-12)
DD	day of month (01-31)
HH24	hour of day (00-23)

```SQL
-- TO_DATE(text,format);
SELECT TO_DATE('20170103','YYYYMMDD');

-- to_timestamp(text, text)
to_timestamp('2018-03-12 18:47:35','yyyy-MM-dd hh24:mi:ss')
SELECT to_timestamp('05 Dec 2000', 'DD Mon YYYY');
SELECT to_timestamp('10:49 2023/01/20', 'HH24:MI YYYY/MM/DD');
```

## 时间差

```SQL
SELECT round(cast(date_part('epoch', start_time - end_time)/60/60 as numeric ),1) as time_diff_hours
FROM table0
```

## install

```bash
# archlinux, 没有把 服务端和客户端分成不同的包
sudo pacman -S postgresql
```

### ubuntu install postgresql

```bash
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh

# Import the repository signing key:
sudo apt install curl ca-certificates
sudo install -d /usr/share/postgresql-common/pgdg
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc

# Create the repository configuration file:
. /etc/os-release
sudo sh -c "echo 'deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $VERSION_CODENAME-pgdg main' > /etc/apt/sources.list.d/pgdg.list"

# Update the package lists:
sudo apt update

# Install the latest version of PostgreSQL:
# If you want a specific version, use 'postgresql-17' or similar instead of 'postgresql'
sudo apt -y install postgresql
sudo -u postgres psql
CREATE USER user_0 WITH PASSWORD 'password_0';

# 用 systemctl 启动 postgresql 服务
sudo systemctl restart  postgresql

# 默认配置文件位置 
 /etc/postgresql/17/main/postgresql.conf

# 日志 路径 
/var/lib/postgresql/17/main/log

```

https://hub.docker.com/_/postgres

```bash
nerdctl pull postgres:17.5
sudo mkdir -p /var/lib/postgresql/17/data
sudo chown -R 777 /var/lib/postgresql/17/data

# 默认用户名 POSTGRES_USER=postgres
nerdctl run \
  --name postgres \
  -e POSTGRES_PASSWORD=password_0 \
  -p 5432:5432 \
  -v /var/lib/postgresql/17/data:/var/lib/postgresql/data \
  -d postgres:17.5

###
docker pull postgres:16.4

# 修改配置文件
log_timezone = 'UTC'
timezone = 'Asia/Shanghai'

# docker
# 默认用户名 postgres
docker run --name postgres \
--restart=always \
-p 5432:5432 \
-e POSTGRES_PASSWORD=password0 \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v postgres-data:/var/lib/postgresql/data \
-d postgres:16.4

# podman
podman run --name postgres \
-p 5432:5432 \
-e POSTGRES_PASSWORD=password0 \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v postgres-data:/var/lib/postgresql/data \
-d postgres:14.5

psql -h 127.0.0.1 -p 5432 -U postgres
# password: password0

# 重启服务
su -l postgres -c '/opt/pg9.6/bin/pg_ctl -D /mnt/pgdata start'

# 重载配置
su -l postgres -c '/opt/pg9.6/bin/pg_ctl -D /mnt/pgdata reload'

docker run -i --rm postgres:16.4 cat /usr/share/postgresql/postgresql.conf.sample > postgresql.conf
```

## sql

```sql
alter table foo
    rename to bar;

alter table foo
    add time0 timestamptz;
```

```sql
-- create table
create table table0(
  field0 json,
  create_time             timestamp with time zone default now(),
  );
 
-- rename column
alter table table_0
    rename column column_foo to column_bar;

```

## psql 命令行直接执行 sql

```sql
PGPASSWORD=postgres psql -h 127.0.0.1 -p 5432 -d database0 -U user0  --command 'select version();'
```

## psql 执行 sql 文件

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

## `bigserial`

postgresql 序列号（SERIAL）类型包括 `smallserial`（smallint,short）, serial(int)和 `bigserial(bigint,long long int)`, 
不管是 `smallserial`, serial 还是 `bigserial`，其范围都是(1,9223372036854775807)，但是序列号类型其实不是真正的类型，
当声明一个字段为序列号类型时其实是创建了一个序列，INSERT时如果没有给该字段赋值会默认获取对应序列的下一个值。

## 日期格式化

```sql
SELECT to_char(NOW(), 'YYYY-MM-DD HH24:MI:SS')
-- 时区
to_char(NOW() AT TIME ZONE 'Asia/Dubai','YYYY-MM-DD HH24:MI:SS')

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

## postgresql single quote 转义

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

## sequence, 序列

```sql
CREATE SEQUENCE seq_0 START 1;
CREATE SEQUENCE seq_0 INCREMENT 1 MINVALUE 1 START 1 CACHE 1;  
```

- INCREMENT, 步长
- max/MINVALUE, 最大/小值
- START, 初始值
- CACHE, 缓存, 某个客户端调用 `nextval()` 之后, 服务端为其预分配的 seq 值的缓存, 如果客户端挂掉或重启缓存里的数据都会被丢弃.
- cycle, 循环产生

```SQL
-- 查看 seq 定义
\d+ seq_0

-- 查看 seq 的当前值, 查询不会导致 sequence 值变化 , 每次查都 是一样的, 如果 没有其它客户端调用 nextval()
SELECT last_value FROM sequence_name;

-- 查看 seq 的下一个值, 每查一次 seq 值 会加 1
SELECT nextval('seq_0')

-- 更新 seq 的值 
select setval('seq_0 ', 88);
```

## 删除外键限制

首先找出数据库表的外键名称：

```sql
\d [tablename]
"table_name_id_fkey" FOREIGN KEY (id) REFERENCES other_table(id) ....
-- 然后使用下面的命令删除外键：

ALTER TABLE [tablename] DROP CONSTRAINT table_name_id_fkey;
```

版权声明：本文为CSDN博主「亮子介」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/henryhu712/article/details/104092141](https://blog.csdn.net/henryhu712/article/details/104092141)

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

- smallint, 2 字节, 小范围整数, -32768 到 +32767
- timestamp, without time zone
- timestamp with time zone
- timestampz
- BOOLEAN
- json
- jsonb

```sql
名字                        别名             描述
character varying [(n)]  varchar [ (n) ]  可变长字符串
character [(n)]          char [ (n) ]     定长字符串
timestamp                                   SQL标准要求仅仅将timestamp类型等于timestamp without time zone 类型
timestamp with time zone   TIMESTAMPTZ       PostgreSQL遵守这个行为。timestamptz 作为 timestamp with time zone 的缩写被接受；这是PostgreSQL 的一个扩展。
```

## 时区

```sql
show timezone;
select * from pg_timezone_names where abbrev='+04';

# 临时设置时区, 退出 psql 之后失效
set time zone "Asia/Shanghai";

select now();
# 查看数据库可供选择的时区:
select * from pg_timezone_names;
```

## substring

```sql
SUBSTRING(string, start_position, length)
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
--查看 PostgreSQL 正在执行的SQL  
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
# 查找是否有 waiting  
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

## 空闲连接

```sql
-- 最大连接数
show max_connections;
-- 当前连接
select * from pg_stat_activity;
select datname from pg_stat_activity group by datname;
select state from pg_stat_activity group by state;
select * from pg_stat_activity where datname='database0' limit 1;
select pid, query_start,query from pg_stat_activity where datname='database0' and state='idle';
-- 释放空闲连接
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state='idle';
```

## GUI

- pgAdmin

[https://www.postgresql.org/docs/current/app-psql.html](https://www.postgresql.org/docs/current/app-psql.html)

## export csv, 导出 csv

sql 后面不要加分号

```sql
COPY (
  SELECT foo, bar FROM table0
)
TO '/tmp/foo.csv'
WITH csv header;
```

————————————————
版权声明：本文为CSDN博主「df0128」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/df0128/article/details/89673596](https://blog.csdn.net/df0128/article/details/89673596)

## 导入 csv

```Bash
psql
\c database0
\copy table0(field0,field1,field2,"field3") from '/home/wiloon/tmp/foo.csv' delimiter ',' csv header;
```


## PostgreSQL 中统计指定字符或者单词或者字符串在一个长字符串中出现总次数，PostgreSQL 统计字符串中某字符出现次数

[https://blog.csdn.net/sunny_day_day/article/details/109183521](https://blog.csdn.net/sunny_day_day/article/details/109183521)

```sql
select array_length(regexp_split_to_array(config,'"id":'),1)-1 from xxx;
```

## postgres 判断主备/主从角色

```bash
### 操作系统上查看 WAL 发送进程或 WAL 接收进程
ps -ef | grep "wal" | grep -v "grep"
# 主库会有 postgres: walwriter, postgres: walsender 进程
# 从库只有 postgres: walreceiver 进程

# 通过 pg_controldata 命令查看数据库控制信息，内容包含 WAL 日志信息、checkpoint、数据块等信息，通过 Databasecluster state 信息可判断是主库还是备库
pg_controldata | grep cluster
```

```sql
-- psql 连接到 DB 之后, 可以这样判断
SELECT pg_is_in_recovery();
-- You can use pg_is_in_recovery() which returns True if recovery is still in progress(so the server is running in standby mode). Check the System Administration Functions for further informations.
-- 如果返回 t 说明是备库，返回 f 是主库
```

[https://blog.csdn.net/m15217321304/article/details/88845353](https://blog.csdn.net/m15217321304/article/details/88845353)

[https://www.postgresql.org/docs/15/functions-admin.html](https://www.postgresql.org/docs/15/functions-admin.html)

## filter

```sql
create table test(id int, c1 int);  
insert into test select generate_series(1,10000), random()*10;
select * from test limit 10;
select c1,count(*)  from test group by c1;
select c1,count(*), count(*) filter (where id<1000) from test group by c1;
```

[https://blog.csdn.net/wuyujin1997/article/details/125904177](https://blog.csdn.net/wuyujin1997/article/details/125904177)

## `regclass`

`regclass` 是 oid 的别名，postgresql 自动的为每一个系统表都建立了一个 OId，其中有一个系统表叫做：pg_class，
这个表里记录了数据表、索引 (仍然需要参阅pg_index)、序列、视图、复合类型和一些特殊关系类型的元数据

[https://blog.csdn.net/shiyibodec/article/details/52447755](https://blog.csdn.net/shiyibodec/article/details/52447755)

## postgresql中如何Kill掉正在执行的SQL语句

--查询任务进展
select query_id,query from pg_stat_activity where state='active';

--kill有两种方式
--第一种是：
SELECT pg_cancel_backend(PID);
这种方式只能kill select查询，对update、delete 及DML不生效)

--第二种是：
SELECT pg_terminate_backend(PID);
这种可以kill掉各种操作(select、update、delete、drop等)操作
————————————————
版权声明：本文为CSDN博主「SunWuKong_Hadoop」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/SunWuKong_Hadoop/article/details/89448075](https://blog.csdn.net/SunWuKong_Hadoop/article/details/89448075)


## 为什么where子句中无法使用到字段别名作为筛选条件呢

这就涉及到了SQL语句的整个执行顺序，如下表：

(1) FROM <left_table>
(3) <join_type> JOIN <right_table>
(2) ON <join_condition>
(4) WHERE <where_condition>
(5) GROUP BY <group_by_list>
(6) HAVING <having_condition>
(7) SELECT
(8) DISTINCT <select_list>
(9) ORDER BY <order_by_condition>
(10) LIMIT <limit_number>

执行顺序依次为：

from ：先确定查询范围
ON：确定多表联合查询的条件
JOIN：指定联合哪些数据表
WHERE ：全表查询的筛选条件，生成第一个结果集
GROUP BY：分组条件，对第一个结果集进行分组，得到第二个结果集
HAVING ：过滤条件，与 group by 连用，对第二个结果集中的每组数据，进行筛选过滤，得到第三个结果集
SELECT：指定获取的列项，得到第四个结果集
DISTINCT ：对指定列进行去重操作
ORDER BY：对结果集按照指定字段进行排序整理
LIMIT：对最终结果集进行截取，一般和offset连用，可用于分页
所以，以此可以看出，为什么在where语句中没法使用查询列的别名进行过滤了，因为调用where子句的时候，select子句还没有开始执行，所以不识别，同理，order by子句中是可以使用

在查询mysql的字段别名使用的时候，翻到了mysql的官方文档，里面对别名的使用场景进行了简要的介绍：

意思就是别名可以使在 order by、having、group by 子句中，但是根据上面的SQL执行过程，很明显group by 和 having都在select之前啊，这里值得注意的是，mysql对group by 进行了优化加强，所以在group by子句中可以使用别名进行分类，但是其他数据库还是遵循着SQL的执行顺序
————————————————
版权声明：本文为CSDN博主`「shenzhou_yh」`的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/shenzhou_yh/article/details/103185772

## ESCAPE

## string to int

```sql
--把'1234'转成整数

select cast('1234' as integer ) ;

--用substring截取字符串，从第8个字符开始截取2个字符：结果是12

select cast(substring('1234abc12',8,2) as integer)

---使用to_number函数来转换成整数

---to_number(text, text)  返回的类型 numeric     把字串转换成numeric   to_number('12,454.8-', '99G999D9S')

select to_number('12121','999999999')
————————————————

                            版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。
                        
原文链接：https://blog.csdn.net/xingxiupaioxue/article/details/78295118
```

## 字符串分割函数

1. SPLIT_PART
   SPLIT_PART() 函数通过指定分隔符分割字符串，并返回第N个子串。语法：

SPLIT_PART(string, delimiter, position)
1
string : 待分割的字符串
delimiter：指定分割字符串
position：返回第几个字串，从1开始，该参数必须是正数。如果参数值大于分割后字符串的数量，函数返回空串。
示例：

SELECT SPLIT_PART('A,B,C', ',', 2);  -- 返回B
1
下面我们利用该函数分割日期，获取年月日：

select split_part( current_date::text,'-',1) as year ,
split_part( current_date::text,'-',2) as  month,
split_part( current_date::text,'-',3) as day
————————————————

版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

原文链接：https://blog.csdn.net/neweastsun/article/details/120243524

## like, `ilike`

```SQL
-- 模糊查询，并且不区分大小写
select * from student where name ilike '%tom%'
```

字符串转bytea:

select cast('\000' as bytea) as name from nt_member limit 1;

bytea转字符串：

select encode('\x00','escape') from nt_member limit 1;

## 索引

```SQL
CREATE INDEX index_0 ON table_0 (column_0);

select * from pg_indexes where tablename='network_discovery_routing_data';
select * from pg_statio_all_indexes where relname='network_discovery_routing_data';

select pg_relation_size('network_discovery_routing_data_time_stamp_idx');
select pg_relation_size('constraint_routing_id_time_stamp');
```

## 临时改变执行计划

```SQL
set enable_seqscan=off;set enable_bitmapscan = off;set enable_tidscan = off;explain (analyze,buffers,verbose) select count(*) from aken01;
```

类似 oracle 的 hint 干预执行计划，pg也有 pg_hint 插件，后期再研究。
通常情况下，pg 不会走错执行计划，走错大都是因为统计信息收集不及时导致的，可通过更频繁地运行 analyze 来解决这个问题，更改下列参数只是一个临时方法。（如下参数值均为布尔类型）

```Bash
set enable_seqscan = off;
```

`enable_seqscan`：是否选择全表顺序扫描，这个变量关闭会让优化器存在其他方法时，优先选择其他方法。
`enable_indexscan`：是否选择索引扫描。
`enable_bitmapscan`：是否选择位图扫描。
`enable_tidscan`：是否选择 TID 扫描。
`enable_nestloop`：多表连接时，是否选择嵌套循环连接。
`enable_hashjoin`：多表连接时，是否选择 hash 连接。
`enable_mergejoin`：多表连接时，是否选择 merge 连接。
`enable_hashagg`：是否使用 hash 聚合。
`enable_sort`：是否选择排序。

执行计划路径方式
全表扫描（顺序扫描）：seq scan，所有数据块，从头扫到尾。
索引扫描：index scan，在索引中找到数据行的位置，然后到表的数据块中把对应的数据读出。
位图索引扫描：bitmap index scan，把满足条件的行或块在内存中建一个位图，扫描完索引后，再根据位图把表的数据文件中相应的数据读取出来。
条件过滤：filter
嵌套循环连接：`nestloop` join，外表（驱动表）小，内表（被驱动表）大
散列连接：hash join，用较小的表在内存中建立散列表，再去扫描较大的表，连接的表均为小表。
合并连接：merge join，通常散列连接比合并连接性能好，当有索引或结果已经被排序时，合并连接性能好。

版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。  
原文链接：https://blog.csdn.net/songyundong1993/article/details/122844254

