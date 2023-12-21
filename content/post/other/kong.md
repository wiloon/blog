---
title: kong
author: "-"
date: 2015-09-16T01:07:07+00:00
url: /?p=8263
categories:
  - Inbox
tags:
  - reprint
---
## kong

```Bash
docker network create kong-net

docker run -d --name kong-database \
 --network=kong-net \
 -p 5432:5432 \
 -e "POSTGRES_USER=kong" \
 -e "POSTGRES_DB=kong" \
 -e "POSTGRES_PASSWORD=kongpass" \
 postgres:13

docker run --rm --network=kong-net \
-e "KONG_DATABASE=postgres" \
-e "KONG_PG_HOST=kong-database" \
-e "KONG_PG_PASSWORD=kongpass" \
kong:3.5.0 kong migrations bootstrap

docker run -d --name kong-gateway \
--network=kong-net \
-e "KONG_DATABASE=postgres" \
-e "KONG_PG_HOST=kong-database" \
-e "KONG_PG_USER=kong" \
-e "KONG_PG_PASSWORD=kongpass" \
-e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
-e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
-e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
-e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
-e "KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl" \
-e "KONG_ADMIN_GUI_URL=http://192.168.50.31:8002" \
-p 8000:8000 \
-p 8443:8443 \
-p 8001:8001 \
-p 8002:8002 \
-p 8444:8444 \
kong:3.5.0

curl -i -X GET --url http://localhost:8001/services

```

## load balance

```Bash
# 创建一个 upstream
curl -X POST http://192.168.50.31:8001/upstreams --data "name=k8s"

# 添加两个 targets 到 upstream
curl -X POST http://192.168.50.31:8001/upstreams/k8s/targets \
    --data "target=192.168.50.80:6443" \
    --data "weight=100"
curl -X POST http://192.168.50.31:8001/upstreams/k8s/targets \
    --data "target=192.168.50.82:6443" \
    --data "weight=100"
    
# 创建一个Service 目标到 Blue upstream
# host: upstream name
curl -X POST http://192.168.50.31:8001/services/ \
    --data "name=k8s-service" \
    --data "host=k8s"
    
# 最后, 添加一个 Route 作为一个端点到 Service
curl -X POST http://192.168.50.31:8001/services/k8s-service/routes/ \
    --data "hosts[]=k8s.wiloon.com"
```

### commands

```Bash
curl -s localhost:8001 | jq '.configuration'

```