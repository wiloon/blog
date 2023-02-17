---
title: redis windows
author: "-"
date: 2015-12-01T04:39:59+00:00
url: /?p=8485
categories:
  - Inbox
tags:
  - reprint
---
## redis windows

启动redis 服务

```bash

redis-server.exe

redis-server.exe  redis.windows.conf

```

<https://github.com/MSOpenTech/redis/releases>

修改配置文件

redis.windows.conf ,搜索 maxheap , 然后直接指定好内容即可.

```bash
maxheap <bytes>
```

maxheap 1024000000
