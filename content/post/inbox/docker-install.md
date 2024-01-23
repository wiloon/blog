---
title: docker install
author: "-"
date: 2018-11-28T06:08:37+00:00
url: docker/install
categories:
  - container
tags:
  - reprint
  - remix
---
## docker install

## ubuntu

### apt 从仓库里安装, 落后两个小版本, 也算比较新了, 建议从官方源安装

sudo apt install docker.io

### curl, 配置官方源, 一般会高几个小版本

[https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

```bash
# 删掉旧版本的包, 有冲突的包
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
```

[https://docs.docker.com/install/linux/docker-ce/centos/](https://docs.docker.com/install/linux/docker-ce/centos/)
  
[https://yq.aliyun.com/articles/110806](https://yq.aliyun.com/articles/110806)

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

[https://yq.aliyun.com/articles/110806](https://yq.aliyun.com/articles/110806)
