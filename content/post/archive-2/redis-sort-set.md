---
title: redis sort set, 有序集, zset
author: "-"
date: 2017-02-13T08:48:39+00:00
url: redis/sort-set
categories:
  - redis
tags:
  - reprint
---
## redis sort set, 有序集, zset

sort set, zset

Sorted-Sets和Sets类型极为相似,它们都是字符串的集合,都不允许重复的成员出现在一个Set中。它们之间的主要差别是Sorted-Sets中的每一个成员都会有一个分数(score)与之关联,Redis正是通过分数来为集合中的成员进行从小到大的排序。然而需要额外指出的是,尽管Sorted-Sets中的成员必须是唯一的,但是分数(score)却是可以重复的
  
在Sorted-Set中添加、删除或更新一个成员都是非常快速的操作,其时间复杂度为集合中成员数量的对数。由于Sorted-Sets中的成员在集合中的位置是有序的,因此,即便是访问位于集合中部的成员也仍然非常高效。事实上,Redis所具有的这一特征在很多其它类型的数据库中是很难实现的,换句话说,在该点上要想达到和Redis同样的高效,在其它数据库中进行建模会非常困难。

## 相关命令列表

命令原型,时间复杂度,命令描述,返回值

### 添加, ZADD

```bash
zADD key score member [score] [member]
```

将一个或多个member元素及其score值加入到有序集key当中。

O(log(N)), 时间复杂度中的N表示Sorted-Sets中成员的数量。
  
添加参数中指定的所有成员及其分数到指定key的Sorted-Set中,在该命令中我们可以指定多组score/member作为参数。如果在添加时参数中的某一成员已经存在,该命令将更新此成员的分数为新值,同时再将该成员基于新值重新排序。如果键不存在,该命令将为该键创建一个新的Sorted-Sets Value,并将score/member对插入其中。如果该键已经存在,但是与其关联的Value不是Sorted-Sets类型,相关的错误信息将被返回。
  
返回值: 本次操作实际插入的成员数量。
  
分数的范围
  
Redis的Sorted Set的分数范围从-(2^53)到+(2^53)。或者说是-9007199254740992 到 9007199254740992。更大的整数在内部用指数表示。

### 删除, ZREM

* ZREM key member [member …]
  
    移除有序集key中的一个或多个成员,不存在的成员将被忽略。

O(M log(N))
  
时间复杂度中N表示Sorted-Set中成员的数量,M则表示被删除的成员数量。该命令将移除参数中指定的成员,其中不存在的成员将被忽略。如果与该Key关联的Value不是Sorted-Set,相应的错误信息将被返回。
  
返回值: 实际被删除的成员数量。

### ZCARD, 计算集合中元素的数量

* ZCARD key
  
    返回有序集key的基数。

O(1)
  
成员数量。获取与该Key相关联的Sorted-Sets中包含的成员数量。
  
返回值: 返回Sorted-Sets中的成员数量,如果该Key不存在,返回0。

### ZCOUNT,score值在min和max之间的成员数量

* ZCOUNT key min max
  
    返回有序集key中,score值在min和max之间(默认包括score值等于min或max)的成员。

O(log(N)+M)
  
时间复杂度中的N表示Sorted-Sets中成员的数量,M则表示min和max之间元素的数量。该命令用于获取分数(score)在min和max之间的成员数量。针对min和max参数需要额外说明的是,-inf和+inf分别表示Sorted-Sets中分数的最高值和最低值。缺省情况下,min和max表示的范围是闭区间范围,即min <= score <= max内的成员将被返回。然而我们可以通过在min和max的前面添加"("字符来表示开区间,如(min max表示min < score <= max,而(min (max表示min < score < max。
  
返回值: 分数指定范围内成员的数量。

### ZSCORE, 成员member的score值

* ZSCORE key member
  
    返回有序集key中,成员member的score值。

O(1)
  
获取指定Key的指定成员的分数。
  
如果该成员存在,以字符串的形式返回其分数,否则返回nil。

### ZINCRBY, 为有序集key的成员member的score值加上增量increment

* ZINCRBY key increment member
  
    为有序集key的成员member的score值加上增量increment。

O(log(N))
  
时间复杂度中的N表示Sorted-Sets中成员的数量。

该命令将为指定Key中的指定成员增加指定的分数。如果成员不存在,该命令将添加该成员并假设其初始分数为0,此后再将其分数加上increment。如果Key不存,该命令将创建该Key及其关联的Sorted-Sets,并包含参数指定的成员,其分数为increment参数。如果与该Key关联的不是Sorted-Sets类型,相关的错误信息将被返回。
  
返回值: 以字符串形式表示的新分数。

### ZRANGE, 返回指定区间内的成员 - 正序

* ZRANGE key start stop [WITHSCORES]
  
    返回有序集key中,指定区间内的成员。
  
    其中成员的位置按score值递增(从小到大)来排序。
  
    具有相同score值的成员按字典序(lexicographical order)来排列。

O(log(N)+M)
  
时间复杂度中的N表示Sorted-Set中成员的数量,M则表示返回的成员数量。

该命令返回顺序在参数start和stop指定范围内的成员,这里start和stop参数都是0-based,即0表示第一个成员,-1表示最后一个成员。如果start大于该Sorted-Set中的最大索引值,或start > stop,此时一个空集合将被返回。如果stop大于最大索引值,该命令将返回从start到集合的最后一个成员。如果命令中带有可选参数WITHSCORES选项,该命令在返回的结果中将包含每个成员的分数值,如value1,score1,value2,score2…。
  
返回值: 返回索引在start和stop之间的成员列表。

### ZREVRANGE, 返回指定区间内的成员 - 倒序

* ZREVRANGE key start stop [WITHSCORES]
  
    返回有序集key中,指定区间内的成员。
  
    其中成员的位置按score值递减(从大到小)来排列。
  
    具有相同score值的成员按字典序的反序(reverse lexicographical order)排列。

O(log(N)+M)
  
时间复杂度中的N表示Sorted-Set中成员的数量,M则表示返回的成员数量。该命令的功能和ZRANGE基本相同,唯一的差别在于该命令是通过反向排序获取指定位置的成员,即从高到低的顺序。如果成员具有相同的分数,则按降序字典顺序排序。
  
返回值: 返回指定的成员列表。

### ZRANGEBYSCORE, 返回有序集合中指定分数区间的成员列表 - 正序, O(log(N)+M)

ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
返回有序集key中,所有score值介于min和max之间(包括等于min或max)的成员。有序集成员按score值递增(从小到大)次序排列。

时间复杂度中的N表示Sorted-Set中成员的数量,M则表示返回的成员数量。

该命令将返回分数在min和max之间的所有成员,即满足表达式min <= score <= max的成员,其中返回的成员是按照其分数从低到高的顺序返回,如果成员具有相同的分数,则按成员的字典顺序返回。可选参数LIMIT用于限制返回成员的数量范围。可选参数offset表示从符合条件的第offset个成员开始返回,同时返回count个成员。

WITHSCORES 参数决定结果集是单单返回有序集的成员,还是将有序集成员及其 score 值一起返回。

最后需要说明的是参数中min和max的规则可参照命令ZCOUNT。
  
返回值: 返回分数在指定范围内的成员列表。

### ZREVRANGEBYSCORE, 返回分数在指定范围内的成员列表 - 倒序

    ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]
  
    返回有序集key中,score值介于max和min之间(默认包括等于max或min)的所有的成员。有序集成员按score值递减(从大到小)的次序排列。

O(log(N)+M)
  
时间复杂度中的N表示Sorted-Set中成员的数量,M则表示返回的成员数量。该命令除了排序方式是基于从高到低的分数排序之外,其它功能和参数含义均与ZRANGEBYSCORE相同。
  
返回值: 返回分数在指定范围内的成员列表。

### ZRANK, 返回指定成员的排名 (位置值, 0表示第一个成员) - 正序

    ZRANK key member
    返回有序集 key 中成员 member 的排名。其中有序集成员按 score 值递增(从小到大)顺序排列。
    O(log(N))
    时间复杂度中的 N 表示 Sorted-Set 中成员的数量。

Sorted-Set 中的成员都是按照分数从低到高的顺序存储, 该命令将返回参数中指定成员的位置值, 其中 0 表示第一个成员, 它是 Sorted-Set中分数最低的成员。
  
返回值: 如果该成员存在,则返回它的位置索引值。否则返回 nil。

### ZREVRANK, 返回指定成员的排名(位置值,0表示第一个成员) - 倒序

* ZREVRANK key member
  
    返回有序集key中成员member的排名。其中有序集成员按score值递减(从大到小)排序。
  
    O(log(N))
  
    时间复杂度中的N表示Sorted-Set中成员的数量。该命令的功能和ZRANK基本相同,唯一的差别在于该命令获取的索引是从高到低排序后的位置,同样0表示第一个元素,即分数最高的成员。
  
    返回值: 如果该成员存在,则返回它的位置索引值。否则返回nil。

### ZREMRANGEBYRANK, 移除有序集中,指定排名(rank)区间内的所有成员

* ZREMRANGEBYRANK key start stop
  
    O(log(N)+M)
  
    时间复杂度中的N表示Sorted-Set中成员的数量,M则表示被删除的成员数量。删除索引位置位于start和stop之间的成员,start和stop都是0-based,即0表示分数最低的成员,-1表示最后一个成员,即分数最高的成员。
  
    返回值: 被删除的成员数量。

### ZREMRANGEBYSCORE, 移除有序集中,指定分数 (score) 区间内的所有成员

* ZREMRANGEBYSCORE key min max
  
    O(log(N)+M)
  
    时间复杂度中的N表示Sorted-Set中成员的数量,M则表示被删除的成员数量。删除分数在min和max之间的所有成员,即满足表达式min <= score <= max的所有成员。对于min和max参数,可以采用开区间的方式表示,具体规则参照ZCOUNT。
  
    返回值: 被删除的成员数量。

### 交集

* ZINTERSTORE
  
    计算给定的一个或多个有序集的交集,其中给定key的数量必须以numkeys参数指定,并将该交集(结果集)储存到destination。

### 并集

* ZUNIONSTORE
  
    计算给定的一个或多个有序集的并集,其中给定key的数量必须以numkeys参数指定,并将该并集(结果集)储存到destination。

### ziplist, skiplist

sorted set 和 ziplist 的关系
Redis中的sorted set, 是在 skiplist、dict 和 ziplist 基础上构建起来的:

当数据较少时, sorted set 是由一个 ziplist 来实现的。
当数据多的时候, sorted set 是由一个叫 zset 的数据结构来实现的, 这个 zset 包含一个 dict 加一个 skiplist。 dict 用来查询数据(member) 到分数 (score) 的对应关系, 而 skiplist 用来根据分数或者 (分数or排名) 范围查询数据。这样 skiplist 中只需要通过指针来获取对应分数的键 member, 而不用管键到底占了多大空间, 把它交给dict去存储。

><https://redis.readthedocs.io/en/2.4/sorted_set.html>
><http://www.cnblogs.com/stephen-liu74/archive/2012/02/16/2354994.html>
><https://elsef.com/2019/12/06/%E5%85%B3%E4%BA%8EZipList/>
