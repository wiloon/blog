---
title: redis hash
author: "-"
date: 2015-07-28T02:43:59+00:00
url: redis/hash
categories:
  - database
tags:
  - Redis

---
## redis hash

Redis hash 是一个 string 类型的 field和 value的映射表.一个 key可对应多个 field, 一个 field对应一个 value。将一个对象存储为 hash类型,较于每个字段都存储成string类型更能节省内存。新建一个 hash对象时开始是用 zipmap(又称为small hash)来存储的。这个 zipmap其实并不是 hash table,但是zipmap 相比正常的 hash实现可以节省不少 hash本身需要的一些元数据存储开销。尽管 zipmap的添加, 删除,查找都是O(n),但是由于一般对象的field数量都不太多。所以使用zipmap也是很快的,也就是说添加删除平均还是O(1)。如果field或者value的大小超出一定限制后,Redis会在内部自动将zipmap替换成正常的hash实现。

hash操作命令如下:

### 删除 key

```bash
    del key
```

### hset

向名称为 key 的 hash 中添加元素

```bash
    hset key field value
```

### hget

hget(key, field) 返回名称为key的hash中field对应的value 
hsetnx HSETNX key field value 将哈希表key中的域field的值设置为value,当且仅当域field不存在。若域field已经存在,该操作无效。
如果key不存在,一个新哈希表被创建并执行h#setnx命令。

### hmget

```bash
    hmget(key, field1, …,field N)
```

返回名称为key的hash中field i对应的value

### hmset

```bash
    hmset(key, field1, value1,…,field N, value N)
```

向名称为key的hash中添加元素field i<—>value i

### hincrby

```bash
    hincrby(key, field, integer)
```
  
将名称为key的hash中field的value增加integer

### hexists

```bash
    hexists(key, field)
```
  
名称为key的hash中是否存在键为field的域

### hdel, 删除字段

```bash
hdel key0, field0
```
  
删除名称为key的hash中键为field的域

## hlen

hash 中 key 的数量

```bash
hlen key0
```

## hkeys

返回名称为 key 的 hash 中所有键

```bash
hkeys key0
```

hvals

hvals(key)

返回名称为key的hash中所有键对应的value

## hgetall

```bash
hgetall key0
```

返回名称为key的hash中所有的键 (field) 及其对应的value

### 内部编码

ziplist (压缩列表)
当 哈希类型 元素个数 小于 hash-max-ziplist-entries 配置 (默认 512 个) 、同时 所有值 都 小于 hash-max-ziplist-value 配置 (默认 64 字节) 时,Redis 会使用 ziplist 作为 哈希 的 内部实现,ziplist 使用更加 紧凑的结构 实现多个元素的 连续存储,所以在 节省内存 方面比 hashtable 更加优秀。

hashtable (哈希表)
当 哈希类型 无法满足 ziplist 的条件时,Redis 会使用 hashtable 作为 哈希 的 内部实现,因为此时 ziplist 的 读写效率 会下降,而 hashtable 的读写 时间复杂度 为 O (1) 。

作者: 零壹技术栈
链接: [https://juejin.cn/post/6844903693075103757](https://juejin.cn/post/6844903693075103757)
来源: 掘金
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

[http://blog.csdn.net/shamohua/article/details/7001501](http://blog.csdn.net/shamohua/article/details/7001501)

[http://blog.csdn.net/enson16855/article/details/13298841](http://blog.csdn.net/enson16855/article/details/13298841)  
