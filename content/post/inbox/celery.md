---
title: "celery"
author: "-"
date: "2021-08-16 09:26:03"
url: ""
categories:
  - "Inbox"
tags:
  - "Inbox"
  - "reprint"
  - "remix"
---
## celery

<https://github.com/celery/celery>

celery是一个基于分布式消息传输的异步任务队列，它专注于实时处理，同时也支持任务调度。它的执行单元为任务（task），利用多线程，如Eventlet，gevent等，它们能被并发地执行在单个或多个职程服务器（worker servers）上。任务能异步执行（后台运行）或同步执行（等待任务完成）。

```bash
# install rabbitmq

# install celery
pip install celery

# run celery server
celery -A tasks worker --loglevel=INFO
```
