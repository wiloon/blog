---
title: influxdb basic
author: "-"
date: 2017-08-02T06:50:39+00:00
url: influxdb
categories:
  - db
tags:
  - reprint
---
## influxdb basic

### http api

```bash
# http api
curl -G 'http://localhost:8086/query?pretty=true'  --data-urlencode "q=show databases"
curl -i -XPOST http://localhost:8086/query --data-urlencode "db=mydb" --data-urlencode "q=CREATE DATABASE db0"

curl -i -XPOST "http://192.168.97.1:8086/write?db=monitor" --data-binary 'measurement_0,location=us-midwest temperature=82 1594349970000000000'
```

### 
    curl -x http://127.0.0.1:8899/ -i -XPOST "http://192.168.97.1:8086/write?db=monitor" --data-binary 'measurement_0,location=us-midwest temperature=86 1594349970000000000'

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

### 安装, influxdb install & config
### dnf

```bash
sudo tee  /etc/yum.repos.d/influxdb.repo<<EOF
[influxdb]
name = InfluxDB Repository
baseurl = https://repos.influxdata.com/rhel/7/x86_64/stable/
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
EOF
dnf install influxdb
vim /etc/influxdb/influxdb.conf
systemctl enable influxdb

```

```bash
# install
# archlinux
yay -S influxdb

# centos
# https://www.influxdata.com/blog/package-repository-for-linux/
sudo yum install influxdb
sudo yum localinstall influxdb-1.2.4.x86_64.rpm

# for Linux Binaries (64-bit)
tar xvfz influxdb-1.3.1_linux_amd64.tar.gz
rsync -r /path/to/influxdb-1.2.4-1/ /

#edit config file
emacs /etc/influxdb/influxdb.conf
```

### /etc/influxdb/influxdb.conf
    #reporting-disabled = false

    [meta]
      
    dir = "/var/lib/influxdb/meta"
      
    #retention-autocreate = true

    [data]
      
    dir = "/var/lib/influxdb/data"
    wal-dir = "/var/lib/influxdb/wal"
    wal-fsync-delay = "100ms"

    # index-version = "inmem"

    index-version = "tsi1"

    trace-logging-enabled = false
      
    query-log-enabled = true
      
    cache-max-memory-size = "512m"
      
    cache-snapshot-memory-size = "32m"

    # 超过10分钟没有写入, 把cache写到新的TSM文件

    cache-snapshot-write-cold-duration = "10m"

    [coordinator]
      
    #慢查询
      
    log-queries-after = "10s"

    [retention]

    #edit file /etc/default/influxdb
      
    STDERR=/data/logs/influxdb/influxdb.log

    #edit logrotate config, modify log path
      
    /etc/logrotate.d/influxdb

```bash
# chown
chown influxdb:influxdb /data/influxdb/
chown influxdb:influxdb /data/logs/influxdb/

#start
systemctl start influxdb
#or
sudo influxd

#connect via cli, rfc3339: 日期格式YYYY-MM-DDTHH:MM:SS.nnnnnnnnnZ
influx -precision rfc3339


```
### docker
```bash
# docker
docker run -d \
--name influxdb \
--net net0 \
--ip 192.168.1.xxx \
-p 8086:8086 \
-p 8083:8083 \
-v influxdb-config:/etc/influxdb:ro \
-v influxdb-storage:/var/lib/influxdb \
-v /etc/localtime:/etc/localtime:ro \
influxdb

# podman
podman run -d \
--name influxdb \
-p 8086:8086 \
-p 8083:8083 \
-p 25826:25826 \
-v influxdb-config:/etc/influxdb:ro \
-v influxdb-storage:/var/lib/influxdb \
-v /etc/localtime:/etc/localtime:ro \
influxdb:1.8.6-alpine

# in pod
podman run -d \
--name influxdb \
--pod monitor \
-v influxdb-config:/etc/influxdb:ro \
-v influxdb-storage:/var/lib/influxdb \
-v /etc/localtime:/etc/localtime:ro \
influxdb

```

### chronograf
    podman run -d \
    --name chronograf \
    --pod monitor \
    -v chronograf:/var/lib/chronograf \
    -v /etc/localtime:/etc/localtime:ro \
    chronograf --influxdb-url=http://monitor:8086

#### run influx
    sudo podman exec -it influxdb influx
    sudo podman run -it --rm influxdb influx -host influxdb.wiloon.com

### retention policies

```bash
show retention policies
show retention policies on db0
CREATE RETENTION POLICY "default" ON db0 DURATION 30d REPLICATION 1 SHARD DURATION 1d DEFAULT

# ALTER  RETENTION POLICY "<policy name>" ON <database> DURATION <duration> REPLICATION 1 SHARD DURATION <shard group duration> DEFAULT
ALTER  RETENTION POLICY "default" ON db0 DURATION 3h REPLICATION 1 SHARD DURATION 1h DEFAULT

# policy name: retention policy 名: default 
# database: 库名
# duration 3h: 保留3个小时的数据
# shard group duration 1h: 每1个小时的数据一个分片
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
DROP MEASUREMENT "kernel"
```

### select
```sql
select * from ping where time > now()-1s

select average_response_ms from ping where time > now()-1s and url='192.168.53.8'

select "database",id,retentionPolicy,seriesCreate,writeReq from "shard" WHERE time>now()-20s AND "database"='database0' AND retentionPolicy='default' AND writeReq>0

select * from "database0"."rentention-policies-0"."measurement0"

```

#### influx

    influx -execute 'select * from "database0"."retention_policies_0"."measurement0" order by time desc limit 1'

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