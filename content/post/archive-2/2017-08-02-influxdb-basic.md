---
title: influxdb basic,command, docker
author: wiloon
type: post
date: 2017-08-02T06:50:39+00:00
url: /?p=10979
categories:
  - Uncategorized

---
### http api

```bash
# http api
curl -G 'http://localhost:8086/query?pretty=true'  --data-urlencode "q=show databases"
curl -i -XPOST http://10.60.0.62:8086/query --data-urlencode "db=mydb" --data-urlencode "q=CREATE DATABASE db0"

```

### database management

```bash
#show db
show databases

# 创建数据库，同时配置retention policy
# DURATION: 数据生命周期 30天
# SHARD DURATION: 分片周期 1小时
# NAME: retention policies 名
CREATE DATABASE "database0" WITH DURATION 30d REPLICATION 1 SHARD DURATION 1h NAME "default"

# create db
# 数据库名不能包含"-", 可以用"_"
create database db0
drop database db0
```

### insert

```sql
-- float value
INSERT measurement0,tag0=tag_value0 field0=1,field1=field_value1
-- int value
INSERT measurement0,tag0=tag_value0 field0=1i,field1=field_value1
-- with time
INSERT measurement0,tag0=tag_value0 field0=1,field1=field_value1 1570611600000000000
```

### delete

```sql
DELETE FROM measurement0 WHERE tag0=tag_value0
```

### 导出

```sql
influx -database 'db0' -execute "select field0,\"field1\" from measurement0 where tag-name0='tag-value0' and time>'2018-05-05 02:00:00' and time<'2018-05-07 11:00:00' order by time tz('Etc/GMT-8')" -format 'csv' -precision 'rfc3339' > xxx.csv

# 使用 tz('Etc/GMT-8') 后,过滤条件中的time>'xxx' 填写东8区时间.
```

### 安装

```bash
# podman
podman run -d \
--name influxdb \
-p 8086:8086 \
-p 8083:8083 \
-v influxdb-config:/etc/influxdb:ro \
-v influxdb-storage:/var/lib/influxdb \
-v /etc/localtime:/etc/localtime:ro \
influxdb

podman run -d \
--name influxdb \
--pod monitor \
-v influxdb-config:/etc/influxdb:ro \
-v influxdb-storage:/var/lib/influxdb \
-v /etc/localtime:/etc/localtime:ro \
influxdb

```
#### run influx
    sudo podman exec -it influxdb influx
    sudo podman run -it --rm influxdb influx -host influxdb.wiloon.com

### retention policies

```bash
show retention policies
show retention policies on db0
CREATE RETENTION POLICY "default" ON db0 DURATION 30d REPLICATION 1 SHARD DURATION 1d DEFAULT
ALTER  RETENTION POLICY "default" ON db0 DURATION 3h REPLICATION 1 SHARD DURATION 1h DEFAULT

# duration 3h: 保留3个小时的数据
# shard duration 1h: 每1个小时的数据一个分片
# policy "default": retention policy 名: default
# DEFAULT: 设置此策略为默认策略
```

### shard

#### list shard id

```sql
show shards
DROP SHARD <shard_id_number>
```

### measurement

```sql
show measurements
DROP MEASUREMENT <measurement_name>
```

```sql
select "database",id,retentionPolicy,seriesCreate,writeReq from "shard" WHERE time>now()-20s AND "database"='database0' AND retentionPolicy='default' AND writeReq>0
```

```bash

# show tag keys
SHOW TAG KEYS [ON <database_name>] [FROM_clause] [WHERE <tag_key> <operator> ['<tag_value>' | <regular_expression>]] [LIMIT_clause] [OFFSET_clause]

show tag keys
show tag keys on db0 from measurements0
show tag values on db0 from measure0 with key="host"

SHOW FIELD KEYS [ON <database_name>] [FROM <measurement_name>]
show tag values from cpu with key=host where service_name=~/xxx/

influx -precision rfc3339


select * from m0 where tag0='tag-value0' and time > '2018-05-16 13:00:00' and time < '2018-05-16 13:01:00' tz('Etc/GMT-8')

# http api
curl -G 'http://localhost:8086/query?pretty=true'  --data-urlencode "q=show databases"
curl -i -XPOST http://10.60.0.62:8086/query --data-urlencode "db=mydb" --data-urlencode "q=CREATE DATABASE db0"

#use
use db0

drop series from series_name

select f0,f1  from s0 where t0=~/xxx.*/ 
ERR: error parsing query: found /, expected regex at line 1, char 56

# =~和后面的正则表达式之间要有空格T_T
select f0,f1  from s0 where t0=~ /xxx.*/ 

```

### select

```bash
sELECT mean(m1) * 10 FROM metric0."default".m0 WHERE time >= now() - 10m  AND host='host0'  GROUP BY time(10s), host

```