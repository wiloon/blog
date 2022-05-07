---
title: linux tcp 连接建立时间
author: "-"
date: 2020-04-21T09:48:27+00:00
url: /?p=16022
categories:
  - Inbox
tags:
  - reprint
---
## linux tcp 连接建立时间
```bash
lsof -P -i tcp | awk '{print $2,$4}' | tr -d 'u' | sort -u
stat --printf "%z %N\n" /proc/$pid/fd/$fd
```