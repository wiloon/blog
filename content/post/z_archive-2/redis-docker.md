---
title: redis docker
author: "-"
date: 2018-09-21T05:14:43+00:00
url: /?p=12652
categories:
  - Inbox
tags:
  - reprint
---
## redis docker

```bash
podman run \
-d \
--name redis \
-p 6379:6379 \
-v /etc/localtime:/etc/localtime:ro \
redis

docker run -it --rm redis redis-cli -c -h 192.168.1.xxx

#创建并启动容器
sudo docker run --name redis-x -p 6379:6379 -d redis

#启动
sudo docker start redis-x

sudo docker exec -it redis-x redis-cli
```

[http://www.runoob.com/docker/docker-install-redis.html](http://www.runoob.com/docker/docker-install-redis.html)
