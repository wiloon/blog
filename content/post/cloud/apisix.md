---
title: "apisix"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "apisix"

### 启动etcd

### apisix

    podman run -d \
    --name apisix \
    -v apisix-logs:/usr/local/apisix/logs \
    -v apisix-conf:/usr/local/apisix/conf \
    -v /etc/letsencrypt/live/wiloon.com-0001:/usr/local/apisix/cert \
    -p 9180:9180 \
    -p 9080:9080 \
    -p 443:9443 \
    apache/apisix

### allow admin

 allow_admin:                  # [http://nginx.org/en/docs/http/ngx_http_access_module.html#allow](http://nginx.org/en/docs/http/ngx_http_access_module.html#allow)
        - 192.168.50.116/24              # If we don't set any IP list, then any IP access is allowed by default.

#### 修改etcd 地址

        etcd:
        host: 
            - "http://192.168.50.101:2379"

### test

    curl "http://192.168.50.101:9080/apisix/admin/services/" -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'

### build apisix-dashboard

    buildah bud -f Dockerfile -t apisix-dashboard:1.5 .

### run apisix dashboard

        podman run -d \
        --name apisix-dashboard \
        -p 80:80 \
        -v apisix-dashboard-config:/etc/nginx/conf.d/ \
        -v /etc/localtime:/etc/localtime:ro \
        nginx

### 设置 Upstream

创建 id 为 50 的上游信息

    curl "http://192.168.50.101:9080/apisix/admin/upstreams/50" -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X PUT -d '
{
    "type": "roundrobin",
    "nodes": {
        "192.168.50.114:3000": 1
    }
}'

### config host and upstrem

curl "http://192.168.50.101:9080/apisix/admin/routes/5" -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X PUT -d '
{
    "uri": "/*",
    "host": "foo.wiloon.com",
    "plugins": {
    },
    "upstream_id": 50
}'

### config tls cert

convert multi line pem to single line pem with following command

    awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' cert-name.pem

    curl http://127.0.0.1:9080/apisix/admin/ssl/1 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X PUT -d '
    {
        "cert": "-----BEGIN CERTIFICATE-----\n<base64 pem cert>\n-----END CERTIFICATE-----\n",
        "key": "-----BEGIN PRIVATE KEY-----\nM<base64 pem private key>\n-----END PRIVATE KEY-----\n",
        "sni": "wiloon.com"
    }'

    curl http://127.0.0.1:9080/apisix/admin/ssl/2 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X PUT -d '
    {
        "cert": "-----BEGIN CERTIFICATE-----\n<base64 pem cert>\n-----END CERTIFICATE-----\n",
        "key": "-----BEGIN PRIVATE KEY-----\nM<base64 pem private key>\n-----END PRIVATE KEY-----\n",
        "sni": "*.wiloon.com"
    }'

### get route config

    curl "http://127.0.0.1:9080/apisix/admin/upstreams/53" -H 'X-API-KEY: 'edd1c9f034335f136f87ad84b625c8f1 -X GET
