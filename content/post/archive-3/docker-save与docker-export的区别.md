---
title: docker save与docker export的区别, docker 镜像 导出
author: "-"
date: 2020-04-13T05:24:16+00:00
url: /?p=15930
categories:
  - Uncategorized

tags:
  - reprint
---
## docker save与docker export的区别, docker 镜像 导出
### 导出
```bash
# save & load
docker save f1905dce9659 > kafka.tar
# 另外一种save语法
docker save -o images.tar postgres:9.6
docker load < kafka.tar
# docker load 之后repository和tag都是none,重新打一下tag
docker tag f1905dce9659 wurstmeister/kafka:latest

# export & import
docker export f299f501774c > hangger_server.tar
docker import - new_hangger_server < hangger_server.tar
```

docker save和docker export的区别: 
docker save保存的是镜像（image) ，docker export保存的是容器（container) ；
docker load用来载入镜像包，docker import用来载入容器包，但两者都会恢复为镜像；
docker load不能对载入的镜像重命名，而docker import可以为镜像指定新名称。

https://www.hangge.com/blog/cache/detail_2411.html
https://jingsam.github.io/2017/08/26/docker-save-and-docker-export.html