---
title: redis string
author: "-"
date: 2018-11-06T02:19:24+00:00
url: redis-string
categories:
  - inbox
tags:
  - reprint
---
## redis string

Redis 字符串数据类型的相关命令用于管理 redis 字符串值

### template

```r
    SET key value [EX seconds] [PX milliseconds] [NX|XX]

    EX second : 设置键的过期时间为 second 秒。 SET key value EX second 效果等同于 SETEX key second value 。
    PX millisecond : 设置键的过期时间为 millisecond 毫秒。 SET key value PX millisecond 效果等同于 PSETEX key millisecond value 。
    NX: 只在键不存在时,才对键进行设置操作。 SET key value NX 效果等同于 SETNX key value
    XX: 只在键已经存在时,才对键进行设置操作。
```

```bash
SET KEY_NAME VALUE

# 将值value关联到key,并将key的生存时间设为seconds(以秒为单位)。
SETEX KEY_NAME seconds VALUE

GET KEY_NAME
```

INCR key
将key中储存的数字值增一。

### 内部编码

字符串 类型的 内部编码 有 3 种:

int: 8 个字节的 长整型。

embstr: 小于等于 39 个字节的字符串。

raw: 大于 39 个字节的字符串。

### embstr

如果字符串对象保存的是一个字符串值,并且这个字符串值的长度小于等于44字节 (44这个值并不会一直保持不变,例如redis3.2版本之前是39) ,则使用embstr编码,embstr即embedded string,“嵌入式的字符串,将SDS结构体嵌入RedisObject对象中”,是专门用于保存短字符串的一种编码方式,与raw的差别在于,raw会调用两次内存分配函数来创建redisObject结构和sdshdr结构,而embstr编码则通过调用一次内存分配函数来分配一块连续的空间,空间内一次包含了redisObject和sdshdr两个结构。
embstr有以下好处:

embstr编码将创建字符串对象所需的内存分配次数从raw编码的两次降低为一次,内存释放函数也是从两次降低为一次。
因为embstr编码的字符串对象的所有数据都保存在一块连续的内存里面,所以这些编码的字符串对象比起raw编码的对象字符串,能够更好地利用缓存 (CPU缓存/缓存行) 带来的优势。
embstr的缺点:

如果字符串的长度增加需要重新分配内存时,sds需要重新分配空间,所以embstr编码的字符串对象实际上是只读的,redis没有为embstr编码的字符串对象编写任何相应的修改程序。当我们对embstr编码的字符串对象执行任何修改命令 (例如append) 时,程序会先将对象的编码从embstr转换成raw,然后再执行修改命令。

### sds

Sds  (Simple Dynamic String,简单动态字符串) 是 Redis 底层所使用的字符串表示, 几乎所有的 Redis 模块中都用了 sds
为什么redis string 要使用sds字符串？
O(1)获取长度,c语言的字符串本身不记录长度,而是通过末尾的\0作为结束标志,而sds本身记录了字符串的长度所以获取直接变为O(1)的时间复杂度、同时,长度的维护操作由sds的本身api实现
防止缓冲区溢出bufferoverflow: 由于c不记录字符串长度,相邻字符串容易发生缓存溢出。sds在进行添加之前会检查长度是否足够,并且不足够会自动根据api扩容
减少字符串修改的内存分配次数: 使用动态扩容的机制,根据字符串的大小选择合适的header类型存储并且根据实际情况动态扩展。
使用空间预分配和惰性空间释放,其实就是在扩容的时候,根据大小额外扩容2倍或者1M的空间,方面字符串修改的时候进行伸缩
使用二进制保护,数据的读写不受特殊的限制,写入的时候什么样读取就是什么样
支持兼容部分的c字符串函数,可以减少部分API的开发

### embstr vs sds

    https://www.cnblogs.com/sunchong/p/11924295.html
