---
title: docker install
author: "-"
date: 2018-11-28T06:08:37+00:00
url: /?p=12943
categories:
  - container
tags:
  - reprint
---
## docker install
https://docs.docker.com/install/linux/docker-ce/centos/
  
https://yq.aliyun.com/articles/110806

```bash
# centos

# uninstall old version
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine

# install from repo
# step 1: 安装必要的一些系统工具
sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
# Step 2: 添加软件源信息
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
# Step 3: 更新并安装 Docker-CE
sudo yum install docker-ce docker-ce-cli containerd.io
# Step 4: 开启Docker服务

sudo systemctl start docker
sudo systemctl enable docker
```

https://yq.aliyun.com/articles/110806