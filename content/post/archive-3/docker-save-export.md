---
title: docker save 与 docker export 的区别, docker 镜像 导出
author: "-"
date: 2020-04-13T05:24:16+00:00
url: docker/save
categories:
  - container
tags:
  - reprint
---
## docker save 与 docker export 的区别, docker 镜像 导出

### 导出

```bash
# save & load
docker save f1905dce9659 > kafka.tar
# 另外一种save语法
docker save -o images.tar postgres:9.6
# 从 tar 包加载镜像而不是 stdin, --input, -i: 指定导入的文件，代替 STDIN。
docker load -i foo.tar

docker load < kafka.tar
# docker load 之后repository和tag都是none,重新打一下tag
docker tag f1905dce9659 wurstmeister/kafka:latest

# export & import
docker export f299f501774c > hangger_server.tar
docker import - new_hangger_server < hangger_server.tar
```

docker save 和 docker export 的区别:
docker save 保存的是镜像 (image) ，docker export 保存的是容器 (container) ；
docker load 用来载入镜像包，docker import 用来载入容器包，但两者都会恢复为镜像；
docker load 不能对载入的镜像重命名，而 docker import 可以为镜像指定新名称。

[https://www.hangge.com/blog/cache/detail_2411.html](https://www.hangge.com/blog/cache/detail_2411.html)
[https://jingsam.github.io/2017/08/26/docker-save-and-docker-export.html](https://jingsam.github.io/2017/08/26/docker-save-and-docker-export.html)
