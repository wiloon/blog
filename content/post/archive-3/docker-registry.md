---
title: docker registry
author: "-"
date: 2019-03-25T15:01:06+00:00
url: docker/registry
categories:
  - container
tags:
  - reprint
---
## docker registry

## 删除镜像与空间回收

<https://zhuanlan.zhihu.com/p/33324217>

```bash
mkdir -p /data/docker-registry/

vim  /data/docker-registry/config.yml

# content
version: 0.1
log:
  fields:
    service: registry
storage:
    delete:
        enabled: true  cache:
        blobdescriptor: inmemory
    filesystem:
        rootdirectory: /var/lib/registry
http:
    addr: :5000
    headers:
        X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true  interval: 10s
    threshold: 3
# EOF
# sample, https://docs.docker.com/registry/configuration/

podman run -d \
-v /data/docker-registry/config.yml:/etc/docker/registry/config.yml \
-p 5000:5000 \
--name registry \
-v docker-registry:/var/lib/registry \
registry:2.8.0

buildah tag de3ebb1b260b registry.wiloon.com/pingd-proxy:v0.0.1
buildah push registry.wiloon.com/pingd-proxy:v0.0.1
podman pull registry.wiloon.com/pingd-proxy:v0.0.1

registry.wiloon.com/pingd-proxy
registry.wiloon.com/ping-proxy
```

### nginx config

```
server {
    listen              443 ssl;
    server_name         registry.wiloon.com;
    ssl_certificate     /etc/letsencrypt/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/privkey.pem;
    ssl_protocols       TLSv1.2;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH'; 
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    client_max_body_size 0;
    chunked_transfer_encoding on;
    location /v2/ {
      if ($http_user_agent ~ "^(docker/1.(3|4|5(?!.[0-9]-dev))|Go ).*$" ) {
        return 404;
      }

      proxy_pass                          http://192.168.50.90:5000;
      proxy_set_header  Host              $http_host;   # required for docker client's sake
      proxy_set_header  X-Real-IP         $remote_addr; # pass on real client's IP
      proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header  X-Forwarded-Proto $scheme;
      proxy_read_timeout                  900;
    }
}

```

https://docs.docker.com/registry/recipes/nginx/