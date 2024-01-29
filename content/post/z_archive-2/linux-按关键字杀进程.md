---
title: linux 按关键字杀进程
author: "-"
date: 2018-12-17T04:40:43+00:00
url: /?p=13121
categories:
  - Linux
tags:
  - reprint
---
## linux 按关键字杀进程

```bash
kill -9 $(ps -ef | grep process0 | grep -v grep | awk '{print $2}')
```
