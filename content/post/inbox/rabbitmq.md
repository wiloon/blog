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
podman run -d --hostname host0 --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3.11.10-management

rabbitmqctl list_connections
rabbitmqctl list_queues
rabbitmqctl list_channels
rabbitmqctl list_users

rabbitmqctl cluster_status
```

## 管理页面

使用：`http://宿主ip:15672` 访问管理页面，默认用户名密码：guest/guest
