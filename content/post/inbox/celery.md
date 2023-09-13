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

celery 是一个基于分布式消息传输的异步任务队列，它专注于实时处理，同时也支持任务调度。它的执行单元为任务（task），利用多线程，如Eventlet，gevent等，它们能被并发地执行在单个或多个职程服务器（worker servers）上。任务能异步执行（后台运行）或同步执行（等待任务完成）。

```bash
# install rabbitmq
https://wangyue.dev/rabbitmq

# install celery
pip install celery

# 添加用户跟密码, rabbitmqctl add_user test test123
rabbitmqctl add_user user0 password0
# 添加虚拟主机 rabbitmqctl add_vhost test_vhost
rabbitmqctl add_vhost vhost0
# 为用户添加标签, rabbitmqctl set_user_tags test test_tag
rabbitmqctl set_user_tags user0 tag0
# 设置用户权限, rabbitmqctl set_permissions -p test_vhost test ".*" ".*" ".*"
rabbitmqctl set_permissions -p vhost0 user0 ".*" ".*" ".*"

# run celery server
celery -A tasks worker --loglevel=INFO
```

————————————————
版权声明：本文为CSDN博主「吴秋霖」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/qiulin_wu/article/details/106119757>

 django-admin startproject HelloWorld

## pycharm celery

start rabbitmq

run api

```bash
python manage.py runserver 0.0.0.0:8000
```

run celery

```bash
celery -A app0 worker -c 1 --workdir=/path/to/celery_app/root/
```

### pycharm debug

add new python script

script: /home/wiloon/apps/venv-36/bin/celery
script parameters: worker -A app0 -c 1 --workdir=/path/to/celery_app/root/
working directory is celery path: /home/wiloon/apps/venv-36/bin/
environment variables: import appropriate variables

<https://stackoverflow.com/questions/29312809/how-do-i-enable-remote-celery-debugging-in-pycharm>