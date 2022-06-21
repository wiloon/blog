---
title: nexus docker repo
author: "-"
date: 2020-03-14T17:55:29+00:00
url: nexus/docker
categories:
  - container
tags:
  - reprint
---
## nexus docker proxy

create repository

- Name: dockerhub-proxy
- Remote storage 配置成 https://registry-1.docker.io
- Docker Index 选择 Use Docker Hub

保存

创建一个 Docker Group Repository

勾选 :  HTTP, Create an HTTP connector at specified port. Normally used if the server is behind a secure proxy 并填写端口 8083

勾选: Allow anonymous docker pull ( Docker Bearer Token Realm required )，允许不登录执行 docker pull。

Administration>Security>Anonymous Access 勾选 Allow anonymous users to access the server, Realm: 选择 Docker Bearer Token Realm
  
Administration>Security>Realms: 把Docker bearer token realm 加入 Active

<https://www.iszy.cc/posts/14/>

## client config

```conf
{
        "insecure-registries": ["192.168.50.13:30083"],
        "registry-mirrors": ["http://192.168.50.13:30083"]
}
```
