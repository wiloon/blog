---
title: grafana
author: "-"
date: 2019-02-17T12:35:14+00:00
url: /?p=13621
categories:
  - inbox
tags:
  - reprint
---
## grafana

```bash
# podman
podman run \
-d \
--name=grafana \
-e "GF_SERVER_ROOT_URL=http://grafana.wiloon.com" \
-e "GF_SECURITY_ADMIN_PASSWORD=password0" \
-p 3100:3000 \
-v grafana-storage:/var/lib/grafana \
-v /etc/localtime:/etc/localtime:ro \
grafana/grafana:8.5.6

# in pod
podman run \
-d \
--name=grafana \
-e "GF_SERVER_ROOT_URL=http://grafana.wiloon.com" \
-e "GF_SECURITY_ADMIN_PASSWORD=password0" \
--pod monitor \
-v grafana-storage:/var/lib/grafana \
-v /etc/localtime:/etc/localtime:ro \
grafana/grafana

```

### variable for host

```sql
SHOW TAG VALUES ON "telegraf" FROM "system" WITH KEY = "host"
```

Q. How do I use the second y axis, secondYAxis function does not work

A. You can switch any series to the second y axis by clicking on the colored line to left of the series name in the legend below the graph. Alternately, use the "Display Styles" > "Series Specific overrides" to define an alias or regex + "Y-axis: 2" to move metrics to the right Axis

[https://github.com/grafana/grafana/wiki/FAQ](https://github.com/grafana/grafana/wiki/FAQ)

## reset password

```bash
sqlite3 /var/lib/grafana/grafana.db
#查看数据库中包含的表
.tables

#查看user表内容
select * from user;

#重置admin用户的密码为默认admin
update user set password = '59acf18b94d7eb0694c61e60ce44c110c7a683ac6a8f09580d626f90f4a242000746579358d77dd9e570e83fa24faa88a8a6', salt = 'F3FAxVm33R' where login = 'admin';

# 退出
.exit
```
