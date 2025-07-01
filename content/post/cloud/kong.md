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
-p 80:8000 \
-p 443:8443 \
-p 8001:8001 \
-p 8002:8002 \
-p 8444:8444 \
kong:3.9.1

# -p 80:8000 # HTTP 代理端口
# -p 443:8443 # HTTPS 代理端口
# -p 8001:8001 # Admin API HTTP 端口
# -p 8002:8002 # Admin GUI HTTP 端口
# -p 8444:8444 # Admin API HTTPS 端口


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

## upstreams

Upstream 是在 Kong 中管理后端服务的负载均衡机制。当请求到达 Service 时，Kong 会通过定义的 Upstream 来选择一个具体的后端实例（例如，一个微服务的多个副本）。
如果不使用负载均衡就不需要配置 upstreams 了, 直接在 gateway service 中配置 service endpoint 即可.

## gateway service

Service 是指一个后端的服务，它可以是一个 HTTP、HTTPS、gRPC 或 TCP 服务。Service 表示需要路由到的目标服务。

gateway service> service endpoint>protocol: http; 后端服务(upstream)的协议
gateway service> service endpoint>host: 后端服务 的 upstream name
gateway service> service endpoint>path: 设置转发到后端时请求 URL 的路径前缀, 比如 /api/v1/users?id=42 中的 "v1"

## Route

一个 route 对应一个 service
Route 是对请求的匹配规则，决定请求如何路由到具体的 Service。你可以根据请求的 URL 路径、HTTP 方法、头信息等来匹配 Route。

route> route configuration> protocols: http, https; 控制 客户端 到 Kong 的通信协议（入口）, protocols 决定了客户端使用什么协议才能命中这个 Route，是匹配协议的第一道门槛。
route> route configuration> host: enx-dev.wiloon.com; 控制 客户端 到 Kong 的通信协议（入口）, host 决定了客户端请求的域名是否能命中这个 Route.
route> route configuration> path: /api; 控制 客户端 到 Kong 的通信协议（入口）, path 决定了客户端请求的 URL 路径是否能命中这个 Route. 比如 前端资源(/static)的请求要发给其它的 route.

```bash
Client Request
     ↓
   Route
     ↓
  Service (host=my-upstream)
     ↓
  Upstream (name=my-upstream)
     ↓
Targets:
  - 192.168.1.101:8000
  - 192.168.1.102:8000
```


## health check

curl -s http://kong.wiloon.com:8001/upstreams/enx-api-upstream/health | jq

## kong add new loadbalance service

new gateway service
  general information
    name: kong-manager-service
  service endpoint
    protocol: http
    host: 192.168.50.64
    port: 8002
new route
  general information:
    name: kong-manager-route
    
