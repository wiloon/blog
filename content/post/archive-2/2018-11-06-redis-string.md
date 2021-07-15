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

embstr: 小于等于 39 个字节的字符串。

raw：大于 39 个字节的字符串。


### embstr
embstr
如果字符串对象保存的是一个字符串值，并且这个字符粗值的长度小于等于44字节（44这个值并不会一直保持不变，例如redis3.2版本之前是39），则使用embstr编码，embstr即embedded string，“嵌入式的字符串，将SDS结构体嵌入RedisObject对象中”，是专门用于保存短字符串的一种编码方式，与raw的差别在于，raw会调用两次内存分配函数来创建redisObject结构和sdshdr结构，而embstr编码则通过调用一次内存分配函数来分配一块连续的空间，空间内一次包含了redisObject和sdshdr两个结构。
embstr有以下好处：

embstr编码将创建字符串对象所需的内存分配次数从raw编码的两次降低为一次，内存释放函数也是从两次降低为一次。
因为embstr编码的字符串对象的所有数据都保存在一块连续的内存里面，所以这些编码的字符串对象比起raw编码的对象字符串，能够更好地利用缓存（CPU缓存/缓存行）带来的优势。
embstr的缺点：

如果字符串的长度增加需要重新分配内存时，sds需要重新分配空间，所以embstr编码的字符串对象实际上是只读的，redis没有为embstr编码的字符串对象编写任何相应的修改程序。当我们对embstr编码的字符串对象执行任何修改命令（例如append）时，程序会先将对象的编码从embstr转换成raw，然后再执行修改命令。