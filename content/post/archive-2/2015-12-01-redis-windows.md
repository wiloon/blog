---
title: redis windows
author: wiloon
type: post
date: 2015-12-01T04:39:59+00:00
url: /?p=8485
categories:
  - Uncategorized

---
启动redis 服务

[shell]

redis-server.exe

redis-server.exe  redis.windows.conf

[/shell]

https://github.com/MSOpenTech/redis/releases



修改配置文件

redis.windows.conf ,搜索 maxheap , 然后直接指定好内容即可.



\# maxheap <bytes>

maxheap 1024000000



