---
title: golang git server, gogs, gitea
author: "-"
date: 2018-01-17T05:54:40+00:00
url: /?p=11735
categories:
  - Uncategorized

---
## golang git server, gogs, gitea
```bash
  
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
  
https://gogs.io/docs/installation/install_from_source

MySQL /Mariadb error: max key length is 767 byte
  
https://github.com/gogits/gogs/issues/4907
  
gogs patch
  
https://github.com/m2nlight/gogs/releases/tag/v0.11.34_patch