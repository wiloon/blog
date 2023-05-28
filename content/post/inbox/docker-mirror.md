---
title: docker mirror
author: "-"
date: 2018-07-15T07:50:12+00:00
url: /?p=12430
categories:
  - container
tags:
  - reprint
---
## docker mirror
登录容器Hub服务的控制台,左侧的加速器帮助页面就会显示为你独立分配的加速地址。
  
https://yq.aliyun.com/articles/29941

https://www.docker-cn.com/registry-mirror

永久性保留更改,您可以修改 /etc/docker/daemon.json 文件并添加上 registry-mirrors 键值。

```bash
vim /etc/docker/daemon.json #(create it if it does not exist)

{
  "registry-mirrors": ["https://registry.docker-cn.com"],
  "insecure-registries": [
        "registry.wiloon.com"
    ]
}

### restart docker service
# 修改保存后重启 Docker 以使配置生效。
sudo systemctl daemon-reload
sudo systemctl restart docker.service

### 查看
sudo docker info
```

### daemon.json

```json
{ 
"registry-mirrors": ["https://registry.docker-cn.com", "http://hub-mirror.c.163.com","https://docker.mirrors.ustc.edu.cn"] 
}
```
