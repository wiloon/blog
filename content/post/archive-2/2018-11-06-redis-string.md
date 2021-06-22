---
title: redis string
author: "-"
type: post
date: 2018-11-06T02:19:24+00:00
url: /?p=12863
categories:
  - Uncategorized

---
Redis 字符串数据类型的相关命令用于管理 redis 字符串值

```bash
SET KEY_NAME VALUE

# 将值value关联到key，并将key的生存时间设为seconds(以秒为单位)。
SETEX KEY_NAME seconds VALUE

GET KEY_NAME
```

INCR key
将key中储存的数字值增一。

