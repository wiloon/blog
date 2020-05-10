---
title: redis hash
author: wiloon
type: post
date: 2015-07-28T02:43:59+00:00
url: /?p=8040
categories:
  - Uncategorized
tags:
  - Redis

---
Redis hash是一个string类型的field和value的映射表.一个key可对应多个field，一个field对应一个value。将一个对象存储为hash类型，较于每个字段都存储成string类型更能节省内存。新建一个hash对象时开始是用zipmap(又称为small hash)来存储的。这个zipmap其实并不是hash table，但是zipmap相比正常的hash实现可以节省不少hash本身需要的一些元数据存储开销。尽管zipmap的添加，删除，查找都是O(n)，但是由于一般对象的field数量都不太多。所以使用zipmap也是很快的,也就是说添加删除平均还是O(1)。如果field或者value的大小超出一定限制后，Redis会在内部自动将zipmap替换成正常的hash实现。

hash操作命令如下：

### delete hash key

del key

### hset

向名称为key的hash中添加元素
  
hset key field value

### hget

hget(key, field) 返回名称为key的hash中field对应的value hsetnx HSETNX key field value 将哈希表key中的域field的值设置为value，当且仅当域field不存在。若域field已经存在，该操作无效。如果key不存在，一个新哈希表被创建并执行h#setnx命令。

### hmget

hmget(key, field1, …,field N)

返回名称为key的hash中field i对应的value

### hmset

hmset(key, field1, value1,…,field N, value N)

向名称为key的hash中添加元素field i<—>value i

### hincrby

hincrby(key, field, integer)
  
将名称为key的hash中field的value增加integer

### hexists

hexists(key, field)
  
名称为key的hash中是否存在键为field的域

### hdel

hdel(key, field)
  
删除名称为key的hash中键为field的域

### hlen

hlen(key)

返回名称为key的hash中元素个数

hkeys

hkeys(key)

返回名称为key的hash中所有键

hvals

hvals(key)

返回名称为key的hash中所有键对应的value

hgetall

hgetall(key)

返回名称为key的hash中所有的键（field）及其对应的value

http://blog.csdn.net/shamohua/article/details/7001501
  
http://blog.csdn.net/enson16855/article/details/13298841