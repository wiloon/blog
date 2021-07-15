---
title: redis string
author: "-"
type: post
date: 2018-11-06T02:19:24+00:00
url: redis-string

---
Redis 字符串数据类型的相关命令用于管理 redis 字符串值

### template
    SET key value [EX seconds] [PX milliseconds] [NX|XX]

    EX second ：设置键的过期时间为 second 秒。 SET key value EX second 效果等同于 SETEX key second value 。
    PX millisecond ：设置键的过期时间为 millisecond 毫秒。 SET key value PX millisecond 效果等同于 PSETEX key millisecond value 。
    NX: 只在键不存在时，才对键进行设置操作。 SET key value NX 效果等同于 SETNX key value 。
    XX: 只在键已经存在时，才对键进行设置操作。

```bash
SET KEY_NAME VALUE

# 将值value关联到key，并将key的生存时间设为seconds(以秒为单位)。
SETEX KEY_NAME seconds VALUE

GET KEY_NAME
```

INCR key
将key中储存的数字值增一。


### 内部编码
字符串 类型的 内部编码 有 3 种：

int：8 个字节的 长整型。

embstr：小于等于 39 个字节的字符串。

raw：大于 39 个字节的字符串。

