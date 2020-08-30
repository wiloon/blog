+++
author = "w1100n"
date = "2020-07-08 13:04:06"
title = "apisix"

+++

### Create a network apisix
    podman network create \
    --driver=bridge \
    --subnet=172.18.0.0/16 \
    --ip-range=172.18.5.0/24 \
    --gateway=172.18.5.254 \
    apisix

### apisix
    podman run -d \
    --name apisix \
    -v apisix-logs:/usr/local/apisix/logs \
    -v apisix-conf:/usr/local/apisix/conf \
    -p 9180:9180 \
    -p 9080:9080 \
    -p 9443:9443 \
    apache/apisix

#### 修改etcd 地址
        etcd:
        host: 
            - "http://192.168.50.101:2379"

### build apisix-dashboard
    buildah bud -f Dockerfile -t apisix-dashboard:1.5 .

### run apisix dashboard
        podman run -d \
        --name apisix-dashboard \
        -p 80:80 \
        -v apisix-dashboard-config:/etc/nginx/conf.d/ \
        -v /etc/localtime:/etc/localtime:ro \
        nginx