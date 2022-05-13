---
title: redis set
author: "-"
date: 2015-12-01T08:01:16+00:00
url: redis-set
categories:
  - inbox
tags:
  - reprint
---
## redis set

```bash
# 删除集合
del set_name_0
```

redis set 是string类型对象的无序集合,set不管存储多少对象,对存储对象的add,remove和test操作的时间复杂度是O(1)。set最多能包含 232 – 1 个member。  

### 增加, sadd  
语法: sadd key member[member…]     
解释: 对特定key的set增加一个或多个值,返回是增加元素的个数。注意: 对同一个member多次add,set中只会保留一份。    
### 查询 smembers, sismember, scard, srandmember
#### smembers
语法: smembers key  
解释: 获取set中的所有member  
### sismember
语法: sismember key member   
解释: 判断值是否是set的member。如果值是set的member返回1,否则,返回0  
### scard
语法: scard key  
解释: 返回set的member个数,如果set不存在,返回0  
### srandmember
语法: srandmember key  
解释: 从set中返回一个随机member  
## 删除 
### spop
语法: spop key  
解释: 移除并返回一个随机member  
### srem
语法: srem key member [member …]  
解释: 移除一个或多个member  
### smove
  
语法: smove source destination member
  
解释: 将source中的member移动到destination

4. 其他

### 并集
    sunion key[key…]
  
解释: 多个set的并集

b) 把并集结果存储到set
  
语法: sunionstore destination key [key …]

解释: 求多个set并集,并把结果存储到destination

### 交集
    sinter key[key…]
  
解释: 多个set的交集

d) 把交集结果存储到指定set

语法: sinterstore destination key [key …]

解释: 把多个set的交集结果存储到destination

e) set中在其他set中不存在member

语法: sdiff key[key …]

f) 把set中在其他set中不存在的member存储到新的set

语法: sdiffstore key[key…]

内部编码
集合类型 的 内部编码 有两种: 
intset (整数集合) 
当集合中的元素都是 整数 且 元素个数 小于 set-max-intset-entries 配置 (默认 512 个) 时,Redis 会选用 intset 来作为 集合 的 内部实现,从而 减少内存 的使用。

hashtable (哈希表) 
当集合类型 无法满足 intset 的条件时,Redis 会使用 hashtable 作为集合的 内部实现。




http://redis.io/commands#set
  
http://redis.io/topics/data-types