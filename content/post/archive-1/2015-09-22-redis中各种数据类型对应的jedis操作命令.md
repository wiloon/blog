---
title: redis中各种数据类型对应的jedis操作命令,placeholder
author: w1100n
type: post
date: 2015-09-22T10:06:45+00:00
url: /?p=8333
categories:
  - Uncategorized

---
redis中各种数据类型对应的jedis操作命令
  
发表于4个月前(2015-05-28 16:28)   阅读（662） | 评论（1） 12人收藏此文章, 我要收藏
  
赞0
  
［听云 Python探针公测］送瑞士军刀背包 送雷蛇键鼠套装！
  
一、常用数据类型简介: 

redis常用五种数据类型:string,hash,list,set,zset(sorted set).

1.String类型

String是最简单的类型，一个key对应一个value

String类型的数据最大1G。
  
String类型的值可以被视作integer，从而可以让"INCR"命令族操作(incrby、decr、decrby),这种情况下，该integer的值限制在64位有符号数。在list、set和zset中包含的独立的元素类型都是Redis String类型。
  
2.List类型

链表类型，主要功能是push、pop、获取一个范围的所有值等。其中的key可以理解为链表的名字。

在Redis中，list就是Redis String的列表，按照插入顺序排序。比如使用LPUSH命令在list头插入一个元素，使用RPUSH命令在list的尾插入一个元素。当这两个命令之一作用于一个空的key时，一个新的list就创建出来了。

List的最大长度是2^32-1个元素。（2^32 = 4 294 967 296） 42亿啊
  
3.Set类型

集合，和数学中的集合概念相似。操作中的key理解为集合的名字。

在Redis中，set就是Redis String的无序集合，不允许有重复元素。

Set的最大元素数是2^32-1。（2^32 = 4 294 967 296） 42亿啊

Redis中对set的操作还有交集、并集、差集等。
  
4.ZSet(Sorted Set)类型

Zset是set的一个升级版本，在set的基础上增加了一个顺序属性，这一属性在添加修改元素时可以指定，每次指定后zset会自动安装指定值重新调整顺序。可以理解为一张表，一列存value，一列存顺序。操作中的key理解为zset的名字。

Zset的最大元素数是2^32-1。（2^32 = 4 294 967 296） 42亿啊

对于已经有序的zset，仍然可以使用SORT命令，通过指定ASC|DESC参数对其进行排序。
  
5.hash类型

hash是最接近关系数据库结构的数据类型，可以将数据库一条记录或程序中一个对象转换成hashmap存放在redis中。
  
二、jedis操作命令: 

1.对value操作的命令

exists(key): 确认一个key是否存在

del(key): 删除一个key

type(key): 返回值的类型

keys(pattern): 返回满足给定pattern的所有key

randomkey: 随机返回key空间的一个key

rename(oldname, newname): 将key由oldname重命名为newname，若newname存在则删除newname表示的key

dbsize: 返回当前数据库中key的数目

expire: 设定一个key的活动时间（s）

ttl: 获得一个key的活动时间

select(index): 按索引查询

move(key, dbindex): 将当前数据库中的key转移到有dbindex索引的数据库

flushdb: 删除当前选择数据库中的所有key

flushall: 删除所有数据库中的所有key

2.对String操作的命令

set(key, value): 给数据库中名称为key的string赋予值value

get(key): 返回数据库中名称为key的string的value

getset(key, value): 给名称为key的string赋予上一次的value

mget(key1, key2,…, key N): 返回库中多个string（它们的名称为key1，key2…）的value

setnx(key, value): 如果不存在名称为key的string，则向库中添加string，名称为key，值为value

setex(key, time, value): 向库中添加string（名称为key，值为value）同时，设定过期时间time

mset(key1, value1, key2, value2,…key N, value N): 同时给多个string赋值，名称为key i的string赋值value i

msetnx(key1, value1, key2, value2,…key N, value N): 如果所有名称为key i的string都不存在，则向库中添加string，名称           key i赋值为value i

incr(key): 名称为key的string增1操作

incrby(key, integer): 名称为key的string增加integer

decr(key): 名称为key的string减1操作

decrby(key, integer): 名称为key的string减少integer

append(key, value): 名称为key的string的值附加value

substr(key, start, end): 返回名称为key的string的value的子串

3.对List操作的命令

rpush(key, value): 在名称为key的list尾添加一个值为value的元素

lpush(key, value): 在名称为key的list头添加一个值为value的 元素

llen(key): 返回名称为key的list的长度

lrange(key, start, end): 返回名称为key的list中start至end之间的元素（下标从0开始，下同）

ltrim(key, start, end): 截取名称为key的list，保留start至end之间的元素

lindex(key, index): 返回名称为key的list中index位置的元素

lset(key, index, value): 给名称为key的list中index位置的元素赋值为value

lrem(key, count, value): 删除count个名称为key的list中值为value的元素。count为0，删除所有值为value的元素，count>0      从头至尾删除count个值为value的元素，count<0从尾到头删除|count|个值为value的元素。

lpop(key): 返回并删除名称为key的list中的首元素

rpop(key): 返回并删除名称为key的list中的尾元素

blpop(key1, key2,… key N, timeout): lpop 命令的block版本。即当timeout为0时，若遇到名称为key i的list不存在或该list为空，则命令结束。如果 timeout>0，则遇到上述情况时，等待timeout秒，如果问题没有解决，则对key i+1开始的list执行pop操作。

brpop(key1, key2,… key N, timeout): rpop的block版本。参考上一命令。

rpoplpush(srckey, dstkey): 返回并删除名称为srckey的list的尾元素，并将该元素添加到名称为dstkey的list的头部

4.对Set操作的命令

sadd(key, member): 向名称为key的set中添加元素member

srem(key, member) : 删除名称为key的set中的元素member

spop(key) : 随机返回并删除名称为key的set中一个元素

smove(srckey, dstkey, member) : 将member元素从名称为srckey的集合移到名称为dstkey的集合

scard(key) : 返回名称为key的set的基数

sismember(key, member) : 测试member是否是名称为key的set的元素

sinter(key1, key2,…key N) : 求交集

sinterstore(dstkey, key1, key2,…key N) : 求交集并将交集保存到dstkey的集合

sunion(key1, key2,…key N) : 求并集

sunionstore(dstkey, key1, key2,…key N) : 求并集并将并集保存到dstkey的集合

sdiff(key1, key2,…key N) : 求差集

sdiffstore(dstkey, key1, key2,…key N) : 求差集并将差集保存到dstkey的集合

smembers(key) : 返回名称为key的set的所有元素

srandmember(key) : 随机返回名称为key的set的一个元素

5.对zset（sorted set）操作的命令

zadd(key, score, member): 向名称为key的zset中添加元素member，score用于排序。如果该元素已经存在，则根据score更新该元素的顺序。

zrem(key, member) : 删除名称为key的zset中的元素member

zincrby(key, increment, member) : 如果在名称为key的zset中已经存在元素member，则该元素的score增加increment；否则向集合中添加该元素，其score的值为increment

zrank(key, member) : 返回名称为key的zset（元素已按score从小到大排序）中member元素的rank（即index，从0开始），若没有member元素，返回"nil"

zrevrank(key, member) : 返回名称为key的zset（元素已按score从大到小排序）中member元素的rank（即index，从0开始），若没有member元素，返回"nil"

zrange(key, start, end): 返回名称为key的zset（元素已按score从小到大排序）中的index从start到end的所有元素

zrevrange(key, start, end): 返回名称为key的zset（元素已按score从大到小排序）中的index从start到end的所有元素

zrangebyscore(key, min, max): 返回名称为key的zset中score >= min且score <= max的所有元素

zcard(key): 返回名称为key的zset的基数

zscore(key, element): 返回名称为key的zset中元素element的score

zremrangebyrank(key, min, max): 删除名称为key的zset中rank >= min且rank <= max的所有元素

zremrangebyscore(key, min, max) : 删除名称为key的zset中score >= min且score <= max的所有元素

zunionstore / zinterstore(dstkeyN, key1,…,keyN, WEIGHTS w1,…wN, AGGREGATE SUM|MIN|MAX): 对N个zset求并集和交集，并将最后的集合保存在dstkeyN中。对于集合中每一个元素的score，在进行AGGREGATE运算前，都要乘以对于的WEIGHT参数。如果没有提供WEIGHT，默认为1。默认的AGGREGATE是SUM，即结果集合中元素的score是所有集合对应元素进行 SUM运算的值，而MIN和MAX是指，结果集合中元素的score是所有集合对应元素中最小值和最大值。

三、各种数据类型所对应的应用场景

1.String类型的应用场景

String是最常用的一种数据类型,普通的key/value存储.

2.list类型的应用场景

比较适用于列表式存储且顺序相对比较固定，例如: 

省份、城市列表

品牌、厂商、车系、车型等列表

拆车坊专题列表...
  
3.set类型的应用场景

Set对外提供的功能与list类似,当需要存储一个列表数据,又不希望出现重复数据时,可选用set

4.zset(sorted set)类型的应用场景

zset的使用场景与set类似,区别是set不是自动有序的,而zset可以通过用户额外提供一个优先级(score)的参数来为成员排序,并且是插入有序的,即自动排序.当你需要一个有序的并且不重复的集合列表,那么可以选择zset数据结构。例如:

根据PV排序的热门车系车型列表

根据时间排序的新闻列表
  
5.hash类型的应用场景

类似于表记录的存储

页面视图所需数据的存储
  
四、具体使用参考示例: 

?
  
private void testKey() {
  
System.out.println("=============key==========================");
  
// 清空数据
  
System.out.println(jedis.flushDB());
  
System.out.println(jedis.echo("foo"));
  
// 判断key否存在
  
System.out.println(shardedJedis.exists("foo"));
  
shardedJedis.set("key", "values");
  
System.out.println(shardedJedis.exists("key"));
  
}

private void testString() {
  
System.out.println("=============String==========================");
  
// 清空数据
  
System.out.println(jedis.flushDB());
  
// 存储数据
  
shardedJedis.set("foo", "bar");
  
System.out.println(shardedJedis.get("foo"));
  
// 若key不存在，则存储
  
shardedJedis.setnx("foo", "foo not exits");
  
System.out.println(shardedJedis.get("foo"));
  
// 覆盖数据
  
shardedJedis.set("foo", "foo update");
  
System.out.println(shardedJedis.get("foo"));
  
// 追加数据
  
shardedJedis.append("foo", " hello, world");
  
System.out.println(shardedJedis.get("foo"));
  
// 设置key的有效期，并存储数据
  
shardedJedis.setex("foo", 2, "foo not exits");
  
System.out.println(shardedJedis.get("foo"));
  
try {
  
Thread.sleep(3000);
  
} catch (InterruptedException e) {
  
}
  
System.out.println(shardedJedis.get("foo"));
  
// 获取并更改数据
  
shardedJedis.set("foo", "foo update");
  
System.out.println(shardedJedis.getSet("foo", "foo modify"));
  
// 截取value的值
  
System.out.println(shardedJedis.getrange("foo", 1, 3));
  
System.out.println(jedis.mset("mset1", "mvalue1", "mset2", "mvalue2", "mset3", "mvalue3", "mset4", "mvalue4"));
  
System.out.println(jedis.mget("mset1", "mset2", "mset3", "mset4"));
  
System.out.println(jedis.del(new String[] { "foo", "foo1", "foo3" }));
  
}

private void testList() {
  
System.out.println("=============list==========================");
  
// 清空数据
  
System.out.println(jedis.flushDB());
  
// 添加数据
  
shardedJedis.lpush("lists", "vector");
  
shardedJedis.lpush("lists", "ArrayList");
  
shardedJedis.lpush("lists", "LinkedList");
  
// 数组长度
  
System.out.println(shardedJedis.llen("lists"));
  
// 排序
  
System.out.println(shardedJedis.sort("lists"));
  
// 字串
  
System.out.println(shardedJedis.lrange("lists", 0, 3));
  
// 修改列表中单个值
  
shardedJedis.lset("lists", 0, "hello list!");
  
// 获取列表指定下标的值
  
System.out.println(shardedJedis.lindex("lists", 1));
  
// 删除列表指定下标的值
  
System.out.println(shardedJedis.lrem("lists", 1, "vector"));
  
// 删除区间以外的数据
  
System.out.println(shardedJedis.ltrim("lists", 0, 1));
  
// 列表出栈
  
System.out.println(shardedJedis.lpop("lists"));
  
// 整个列表值
  
System.out.println(shardedJedis.lrange("lists", 0, -1));

}

private void testSet() {
  
System.out.println("=============set==========================");
  
// 清空数据
  
System.out.println(jedis.flushDB());
  
// 添加数据
  
shardedJedis.sadd("sets", "HashSet");

  
// 判断value是否在列表中
  
System.out.println(shardedJedis.sismember("sets", "TreeSet"));
  
;
  
// 整个列表值
  
System.out.println(shardedJedis.smembers("sets"));
  
// 删除指定元素
  
System.out.println(shardedJedis.srem("sets", "SortedSet"));
  
// 出栈
  
System.out.println(shardedJedis.spop("sets"));
  
System.out.println(shardedJedis.smembers("sets"));
  
//
  
shardedJedis.sadd("sets1", "HashSet1");
  
shardedJedis.sadd("sets1", "SortedSet1");
  
shardedJedis.sadd("sets1", "TreeSet");
  
shardedJedis.sadd("sets2", "HashSet2");
  
shardedJedis.sadd("sets2", "SortedSet1");
  
shardedJedis.sadd("sets2", "TreeSet1");
  
// 交集
  
System.out.println(jedis.sinter("sets1", "sets2"));
  
// 并集
  
System.out.println(jedis.sunion("sets1", "sets2"));
  
// 差集
  
System.out.println(jedis.sdiff("sets1", "sets2"));
  
}

private void testSortedSet() {
  
System.out.println("=============zset==========================");
  
// 清空数据
  
System.out.println(jedis.flushDB());
  
// 添加数据
  
shardedJedis.zadd("zset", 10.1, "hello");
  
shardedJedis.zadd("zset", 10.0, ":");
  
shardedJedis.zadd("zset", 9.0, "zset");
  
shardedJedis.zadd("zset", 11.0, "zset!");
  
// 元素个数
  
System.out.println(shardedJedis.zcard("zset"));
  
// 元素下标
  
System.out.println(shardedJedis.zscore("zset", "zset"));
  
// 集合子集
  
System.out.println(shardedJedis.zrange("zset", 0, -1));
  
// 删除元素
  
System.out.println(shardedJedis.zrem("zset", "zset!"));
  
System.out.println(shardedJedis.zcount("zset", 9.5, 10.5));
  
// 整个集合值
  
System.out.println(shardedJedis.zrange("zset", 0, -1));
  
}

private void testHash() {
  
System.out.println("=============hash==========================");
  
// 清空数据
  
System.out.println(jedis.flushDB());
  
// 添加数据
  
shardedJedis.hset("hashs", "entryKey", "entryValue");
  
shardedJedis.hset("hashs", "entryKey1", "entryValue1");
  
shardedJedis.hset("hashs", "entryKey2", "entryValue2");
  
// 判断某个值是否存在
  
System.out.println(shardedJedis.hexists("hashs", "entryKey"));
  
// 获取指定的值
  
System.out.println(shardedJedis.hget("hashs", "entryKey"));        // 批量获取指定的值
  
System.out.println(shardedJedis.hmget("hashs", "entryKey", "entryKey1"));
  
// 删除指定的值
  
System.out.println(shardedJedis.hdel("hashs", "entryKey"));
  
// 为key中的域 field 的值加上增量 increment
  
System.out.println(shardedJedis.hincrBy("hashs", "entryKey", 123l));
  
// 获取所有的keys
  
System.out.println(shardedJedis.hkeys("hashs"));
  
// 获取所有的values
  
System.out.println(shardedJedis.hvals("hashs"));
  
}
  
分享到:  0赞
  
原文地址: http://www.open-open.com/lib/view/open1385173126448.html