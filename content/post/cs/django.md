---
title: django
author: "-"
date: 2020-03-11T08:53:24+00:00
url: django
categories:
  - Python
tags:
  - reprint
  - remix
---
## django

```Bash
python manage.py startapp hello
```

## pytest-django

## runserver

```Bash
python manage.py runserver 0.0.0.0:1234
```

这个命令会启动两个进程

```
user0    542872  542712  2 16:47 pts/0    00:00:00 python manage.py runserver 0.0.0.0:1234
user0    543984  542872  8 16:47 pts/0    00:00:01 /path/to/venv-36/bin/python manage.py runserver 0.0.0.0:8888
```
本地修改代码之后第一个进程不变, 第二个进程会重启并应用新的代码
