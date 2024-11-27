---
title: golang git server, gogs, gitea
author: "-"
date: 2018-01-17T05:54:40+00:00
url: git/gogs
categories:
  - git
tags:
  - reprint
---
## golang git server, gogs, gitea

gitea 的文档 只提到了docker compose的部署方式, 想改成podman 还需要折腾一下, gogs 的文档 更清晰一些方便使用podman

```bash
podman run --rm --name=gogs -p 10022:22 -p 10880:3000 -v gogs-data:/data gogs/gogs:latest
```

[http://192.168.50.13:10880](http://192.168.50.13:10880)

Database Type: sqlite3
Application Name: pingd
Domain: 192.168.50.13
SSH Port: 1022

```bash
  
  docker run --name=gogs -p 10022:22 -p 10880:3000 -v /var/gogs:/data gogs/gogs
  
# docker for gogs
  
sudo systemctl status docker
  
sudo systemctl start docker
  
sudo systemctl enable docker

sudo docker pull gogs/gogs
  
mkdir -p /data/gogs
  
sudo docker run -name=gogs -p 10022:22 -p 10080:3000 -v /data/gogs:/data gogs/gogs

sudo docker start gogs

sudo docker stop gogs
  
sudo docker rm gogs
  
```

Gogs 的目标是打造一个最简单、最快速和最轻松的方式搭建自助 Git 服务。使用 Go 语言开发使得 Gogs 能够通过独立的二进制分发,并且支持 Go 语言支持的 所有平台,包括 Linux、Mac OS X、Windows 以及 ARM 平台。

create user git and su git

install from source
  
[https://gogs.io/docs/installation/install_from_source](https://gogs.io/docs/installation/install_from_source)

MySQL /Mariadb error: max key length is 767 byte
  
[https://github.com/gogits/gogs/issues/4907](https://github.com/gogits/gogs/issues/4907)
  
gogs patch
  
[https://github.com/m2nlight/gogs/releases/tag/v0.11.34_patch](https://github.com/m2nlight/gogs/releases/tag/v0.11.34_patch)

>[https://hub.docker.com/r/gogs/gogs](https://hub.docker.com/r/gogs/gogs)
>[https://gogs.io/docs](https://gogs.io/docs)
