---
title: "rabbitmq"
author: "-"
date: "2021-08-16 09:10:31"
url: "rabbitmq"
categories:
  - "MQ"
tags:
  - "Inbox"
  - "reprint"
  - "remix"
---
## rabbitmq

```bash
# docker with timeout config
docker run -d --hostname host0 --name rabbitmq -p 15672:15672 -p 5672:5672 -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbit consumer_timeout 50000" rabbitmq:3.8.18-management

# 查看 版本
rabbitmqctl status

docker run -d --hostname host0 --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3.11.10-management
docker run -d --hostname host0 --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3.8.18-management


podman run -d --hostname host0 --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3.11.10-management

rabbitmqctl list_connections
rabbitmqctl list_queues
rabbitmqctl list_channels
rabbitmqctl list_users

rabbitmqctl cluster_status

# 查看 consumer_timeout 的值
rabbitmqctl eval 'application:get_env(rabbit, consumer_timeout).'
```

## 管理页面

使用：`http://宿主ip:15672` 访问管理页面，默认用户名密码：guest/guest
