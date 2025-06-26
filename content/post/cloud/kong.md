---
title: kong
author: "-"
date: 2025-06-17 21:37:38
url: kong
categories:
  - network
tags:
  - reprint
  - remix
---
## kong

run postgresql

```Bash
docker network create kong-net

# 创建 postgresql, 并创建一个实例 kong-db
# KONG_DATABASE 数据库类型，必须是 postgres

# 初始化 kong 数据库
nerdctl run --rm \
  -e KONG_DATABASE=postgres \
  -e KONG_PG_HOST=postgresql \
  -e KONG_PG_PORT=5432 \
  -e KONG_PG_USER=user_0 \
  -e KONG_PG_PASSWORD=password_0 \
  -e KONG_PG_DATABASE=kong_db \
  -e KONG_PASSWORD=password_0 \
  kong:3.9.1 kong migrations bootstrap

# kong OSS + kong manager OOS
nerdctl run -d --name kong \
--network=kong-net \
-e "KONG_DATABASE=postgres" \
-e "KONG_PG_HOST=postgresql" \
-e "KONG_PG_PORT=5432" \
-e "KONG_PG_USER=user_0" \
-e "KONG_PG_PASSWORD=password_0" \
-e "KONG_PG_DATABASE=kong_db" \
-e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
-e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
-e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
-e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
-e "KONG_ADMIN_LISTEN=0.0.0.0:8001,0.0.0.0:8443 ssl" \
-e KONG_ADMIN_GUI_LISTEN=0.0.0.0:8002 \
-p 8000:8000 \
-p 8001:8001 \
-p 8443:8443 \
-p 8002:8002 \
-p 8444:8444 \
kong:3.9.1

curl -i -X GET --url http://localhost:8001/services

# Kong Manager OSS
http://kong:8002/

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

## kong manager

### add route

- upstreams
  - name: enx-api
  - targets
    - target address: enx:8080
- gateway service
  - new gateway service
    - name: enx-api-service
    - service endpoint
      - protocol: https
      - host: enx-api-upstream
- ca certificate
  - cert: past the content of ca-cert.crt
- certificates
  - cert: the content of wiloon.crt
  - key: wiloon.key