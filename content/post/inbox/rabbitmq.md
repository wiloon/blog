---
title: "rabbitmq"
author: "-"
date: ""
url: ""
categories:
  - "MQ"
tags:
  - "Inbox"
  - "reprint"
  - "remix"
---
## rabbitmq

```bash
podman run -d --hostname host0 --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3.10.6-management

使用：http://宿主ip:15672 访问，用户名密码使用默认：guest/guest.

rabbitmqctl list_connections
rabbitmqctl list_queues
rabbitmqctl list_channels
rabbitmqctl list_users

rabbitmqctl cluster_status
```
