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

[https://github.com/celery/celery](https://github.com/celery/celery)

celery 是一个基于分布式消息传输的异步任务队列，它专注于实时处理，同时也支持任务调度。它的执行单元为任务（task），利用多线程，
如 Eventlet，gevent等，它们能被并发地执行在单个或多个职程服务器（worker servers）上。任务能异步执行（后台运行）或同步执行（等待任务完成）。

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
原文链接：[https://blog.csdn.net/qiulin_wu/article/details/106119757](https://blog.csdn.net/qiulin_wu/article/details/106119757)

`django-admin startproject HelloWorld`

## django and celery

- start rabbitmq
- run api
- run celery

```bash
python manage.py runserver 0.0.0.0:8000
```

## run celery in CLI

```bash
celery -A app0 worker -c 1 --workdir=/path/to/celery_app/root/
```

## pycharm celery run/debug config

add new "Python" script

script/script path: /home/wiloon/apps/venv-36/bin/celery
parameters/script parameters: worker -A app0 -c 1 --workdir=/path/to/celery_app/root/
environment variables: import appropriate variables
working directory: /home/wiloon/apps/venv-36/bin/


[https://stackoverflow.com/questions/29312809/how-do-i-enable-remote-celery-debugging-in-pycharm](https://stackoverflow.com/questions/29312809/how-do-i-enable-remote-celery-debugging-in-pycharm)

## PRECONDITION_FAILED

https://docs.celeryq.dev/en/main/userguide/calling.html

Warning
When using RabbitMQ as a message broker when specifying a countdown over 15 minutes, you may encounter the problem that the worker terminates with an PreconditionFailed error will be raised:

amqp.exceptions.PreconditionFailed: (0, 0): (406) PRECONDITION_FAILED - consumer ack timed out on channel
In RabbitMQ since version 3.8.15 the default value for consumer_timeout is 15 minutes. 
Since version 3.8.17 it was increased to 30 minutes. 
If a consumer does not ack its delivery for more than the timeout value, 
its channel will be closed with a PRECONDITION_FAILED channel exception. 
See Delivery Acknowledgement Timeout for more information.

To solve the problem, in RabbitMQ configuration file rabbitmq.conf you should specify the consumer_timeout parameter 
greater than or equal to your countdown value. For example, you can specify a very large value of 
consumer_timeout = 31622400000, which is equal to 1 year in milliseconds, to avoid problems in the future.
