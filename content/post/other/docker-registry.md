---
title: docker registry
author: "-"
date: 2022-10-10 11:54:09
url: docker/registry
categories:
  - container
tags:
  - reprint
  - remix
---
## docker registry

## install registry

```bash
mkdir -p /data/docker-registry/

# sample, https://docs.docker.com/registry/configuration/
cat > /data/docker-registry/config.yml << EOF
version: 0.1
log:
  fields:
    service: registry
storage:
    delete:
        enabled: true
        blobdescriptor: inmemory
    filesystem:
        rootdirectory: /var/lib/registry
http:
    addr: :5000
    headers:
        X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
EOF

podman run -d \
-v /data/docker-registry/config.yml:/etc/docker/registry/config.yml \
-p 5000:5000 \
--name registry \
-v docker-registry:/var/lib/registry \
registry:2.8.1

buildah tag de3ebb1b260b registry.wiloon.com/pingd-proxy:v0.0.1
buildah push registry.wiloon.com/pingd-proxy:v0.0.1
podman pull registry.wiloon.com/pingd-proxy:v0.0.1

registry.wiloon.com/pingd-proxy
registry.wiloon.com/ping-proxy
```

## docker 测试

```bash
sudo docker image tag hello-world registry.wiloon.com/myfirstimage
sudo docker image ls
sudo docker push registry.wiloon.com/myfirstimage
sudo docker image rm hello-world
sudo docker pull  registry.wiloon.com/myfirstimage
sudo docker image ls
```

### nginx config

```conf
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

      proxy_pass                          http://192.168.50.13:5000;
      proxy_set_header  Host              $http_host;   # required for docker client's sake
      proxy_set_header  X-Real-IP         $remote_addr; # pass on real client's IP
      proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header  X-Forwarded-Proto $scheme;
      proxy_read_timeout                  900;
    }
}
```

## 查看仓库镜像

```bash
curl https://registry.wiloon.com/v2/_catalog
# 查询镜像tag(版本)
curl  https://registry.wiloon.com/v2/rssx-api/tags/list

```

## 删除镜像与空间回收

<https://zhuanlan.zhihu.com/p/33324217>

<https://docs.docker.com/registry/>

<https://docs.docker.com/registry/recipes/nginx/>

## podman registry config

```bash
vim /etc/containers/registries.conf

# content
unqualified-search-registries = ["docker.io"]

[[registry]]
prefix = "docker.io"
location = "registry-1.docker.io"
```

## docker registry list

- registry-1.docker.io
