---
title: MySQL SQL_NO_CACHE,sql_cache,RESET QUERY CACHE
author: "-"
date: 2017-11-24T06:51:17+00:00
url: /?p=11488
categories:
  - Inbox
tags:
  - reprint
---
## MySQL SQL_NO_CACHE,sql_cache,RESET QUERY CACHE

[http://blog.csdn.net/xlgen157387/article/details/50767725](http://blog.csdn.net/xlgen157387/article/details/50767725)
  
[http://blog.51cto.com/janephp/1318705](http://blog.51cto.com/janephp/1318705)

减少碎片:
  
合适的query_cache_min_res_unit可以减少碎片,这个参数最合适的大小和应用程序查询结果的平均大小直接相关,可以通过内存实际消耗 (query_cache_size - Qcache_free_memory) 除以Qcache_queries_in_cache计算平均缓存大小。
  
可以通过Qcache_free_blocks来观察碎片,这个值反应了剩余的空闲块,如果这个值很多,但是
  
Qcache_lowmem_prunes却不断增加,则说明碎片太多了。可以使用flush query cache整理碎片,重新排序,但不会清楚,清空命令是reset query cache。整理碎片期间,查询缓存无法被访问,可能导致服务器僵死一段时间,所以查询缓存不宜太大

场景

产品中有一张图片表pics,数据量将近100万条,有一条相关的查询语句,由于执行频次较高,想针对此语句进行优化

表结构很简单,主要字段:

user_id 用户ID
  
picname 图片名称
  
smallimg 小图名称
  
一个用户会有多条图片记录,现在有一个根据user_id建立的索引: uid,查询语句也很简单: 取得某用户的图片集合:

select picname, smallimg from pics where user_id = xxx;
  
优化前

执行查询语句 (为了查看真实执行时间,强制不使用缓存,为了防止在测试时因为读取了缓存造成对时间上的差别)

select SQL_NO_CACHE picname, smallimg from pics where user_id=17853;
  
执行了10次,平均耗时在40ms左右

使用explain进行分析:

explain select SQL_NO_CACHE picname, smallimg from pics where user_id=17853
  
这里写图片描述

使用了user_id的索引,并且是const常数查找,表示性能已经很好了

优化后

因为这个语句太简单,sql本身没有什么优化空间,就考虑了索引

修改索引结构,建立一个(user_id,picname,smallimg)的联合索引: uid_pic

重新执行10次,平均耗时降到了30ms左右

使用explain进行分析

这里写图片描述

看到使用的索引变成了刚刚建立的联合索引,并且Extra部分显示使用了'Using Index'

总结

'Using Index'的意思是"覆盖索引",它是使上面sql性能提升的关键

一个包含查询所需字段的索引称为"覆盖索引"

MySQL只需要通过索引就可以返回查询所需要的数据,而不必在查到索引之后进行回表操作,减少IO,提高了效率

例如上面的sql,查询条件是user_id,可以使用联合索引,要查询的字段是picname smallimg,这两个字段也在联合索引中,这就实现了"覆盖索引",可以根据这个联合索引一次性完成查询工作,所以提升了性能。

扩展研究

一、MySQL缓存,SQL_NO_CACHE和SQL_CACHE 的区别

上边在进行测试的时候,为了防止读取缓存造成对实验结果的影响使用到了SQL_NO_CACHE这个功能,对于SQL_NO_CACHE的介绍官网如下:

SQL_NO_CACHE means that the query result is not cached. It does not mean that the cache is not used to answer the query.

You may use RESET QUERY CACHE to remove all queries from the cache and then your next query should be slow again. Same effect if you change the table, because this makes all cached queries invalid.
  
当我们想用SQL_NO_CACHE来禁止结果缓存时发现结果和我们的预期不一样,查询执行的结果仍然是缓存后的结果。其实,SQL_NO_CACHE的真正作用是禁止缓存查询结果,但并不意味着cache不作为结果返回给query。

在说白点就是,不是本次查询不使用缓存,而是本次查询结果不做为下次查询的缓存。

还有就是,MySQL本身是有对sql语句缓存的机制的,合理设置我们的MySQL缓存可以降低数据库的io资源,因此,这里我们有必要再看一下如何控制这个比较安逸的功能。

看图如下:

这里写图片描述

其中各项的含义为:

have_query_cache
  
是否支持查询缓存区 "YES"表是支持查询缓存区

query_cache_limit
  
可缓存的Select查询结果的最大值 1048576 byte /1024 = 1024kB 即最大可缓存的select查询结果必须小于 1024KB

query_cache_min_res_unit
  
每次给query cache结果分配内存的大小 默认是 4096 byte 也即 4kB

query_cache_size
  
如果你希望禁用查询缓存,设置 query_cache_size=0。禁用了查询缓存,将没有明显的开销

query_cache_type
  
查询缓存的方式(默认是 ON)

1. 完整查询的过程如下

当查询进行的时候,MySQL把查询结果保存在qurey cache中,但是有时候要保存的结果比较大,超过了query_cache_min_res_unit的值 ,这时候MySQL将一边检索结果,一边进行慢慢保存结果,所以,有时候并不是把所有结果全部得到后再进行一次性保存,而是每次分配一块query_cache_min_res_unit 大小的内存空间保存结果集,使用完后,接着再分配一个这样的块,如果还不不够,接着再分配一个块,依此类推,也就是说,有可能在一次查询中,MySQL要进行多次内存分配的操作,而我们应该知道,频繁操作内存都是要耗费时间的。

2. 内存碎片的产生

当一块分配的内存没有完全使用时,MySQL会把这块内存Trim掉,把没有使用的那部分归还以重复利用。比如,第一次分配4KB,只用了3KB,剩1KB,第二次连续操作,分配4KB,用了2KB,剩2KB,这两次连续操作共剩下的1KB+2KB=3KB,不足以做个一个内存单元分配,这时候,内存碎片便产生了。

3.内存块的概念

先看下这个:

这里写图片描述

Qcache_total_blocks 表示所有的块

Qcache_free_blocks 表示未使用的块
  
这个值比较大,那意味着,内存碎片比较多,用flush query cache清理后,为被使用的块其值应该为1或0 ,因为这时候所有的内存都做为一个连续的快在一起了.

Qcache_free_memory 表示查询缓存区现在还有多少的可用内存

Qcache_hits 表示查询缓存区的命中个数,也就是直接从查询缓存区作出响应处理的查询个数

Qcache_inserts 表示查询缓存区此前总过缓存过多少条查询命令的结果

Qcache_lowmem_prunes 表示查询缓存区已满而从其中溢出和删除的查询结果的个数

Qcache_not_cached 表示没有进入查询缓存区的查询命令个数

Qcache_queries_in_cache 查询缓存区当前缓存着多少条查询命令的结果

优化提示:

如果Qcache_lowmem_prunes 值比较大,表示查询缓存区大小设置太小,需要增大。

如果Qcache_free_blocks 较多,表示内存碎片较多,需要清理,flush query cache

关于query_cache_min_res_unit大小的调优,书中给出了一个计算公式,可以供调优设置参考:

query_cache_min_res_unit = (query_cache_size - Qcache_free_memory) /Qcache_queries_in_cache
  
还要注意一点的是,FLUSH QUERY CACHE 命令可以用来整理查询缓存区的碎片,改善内存使用状况,但不会清理查询缓存区的内容,这个要和RESET QUERY CACHE相区别,不要混淆,后者才是清除查询缓存区中的所有的内容。
  
可以在 SELECT 语句中指定查询缓存的选项,对于那些肯定要实时的从表中获取数据的查询,或者对于那些一天只执行一次的查询,我们都可以指定不进行查询缓存,使用 SQL_NO_CACHE 选项。
  
对于那些变化不频繁的表,查询操作很固定,我们可以将该查询操作缓存起来,这样每次执行的时候不实际访问表和执行查询,只是从缓存获得结果,可以有效地改善查询的性能,使用 SQL_CACHE 选项。
  
下面是使用 SQL_NO_CACHE 和 SQL_CACHE 的例子:

MySQL> select sql_no_cache id,name from test3 where id < 2;
  
MySQL> select sql_cache id,name from test3 where id < 2;
  
注意: 查询缓存的使用还需要配合相应得服务器参数的设置。

二、覆盖索引 (偷懒整理一下,来自百度百科)

理解方式一: 就是select的数据列只用从索引中就能够取得,不必读取数据行,换句话说查询列要被所建的索引覆盖。

理解方式二: 索引是高效找到行的一个方法,但是一般数据库也能使用索引找到一个列的数据,因此它不必读取整个行。毕竟索引叶子节点存储了它们索引的数据；当能通过读取索引就可以得到想要的数据,那就不需要读取行了。一个索引包含了 (或覆盖了) 满足查询结果的数据就叫做覆盖索引。

理解方式三: 是非聚集复合索引的一种形式,它包括在查询里的Select、Join和Where子句用到的所有列 (即建索引的字段正好是覆盖查询条件中所涉及的字段,也即,索引包含了查询正在查找的数据) 。

作用:

如果你想要通过索引覆盖select多列,那么需要给需要的列建立一个多列索引,当然如果带查询条件,where条件要求满足最左前缀原则。

Innodb的辅助索引叶子节点包含的是主键列,所以主键一定是被索引覆盖的。

 (1) 例如,在sakila的inventory表中,有一个组合索引(store_id,film_id),对于只需要访问这两列的查 询,MySQL就可以使用索引,如下:

MySQL> EXPLAIN SELECT store_id, film_id FROM sakila.inventory\G
  
 (2) 再比如说在文章系统里分页显示的时候,一般的查询是这样的:

SELECT id, title, content FROM article ORDER BY created DESC LIMIT 10000, 10;
  
通常这样的查询会把索引建在created字段 (其中id是主键) ,不过当LIMIT偏移很大时,查询效率仍然很低,改变一下查询:

SELECT id, title, content FROM article
  
INNER JOIN (
  
SELECT id FROM article ORDER BY created DESC LIMIT 10000, 10
  
) AS page USING(id)
  
此时,建立复合索引"created, id" (只要建立created索引就可以吧,Innodb是会在辅助索引里面存储主键值的) ,就可以在子查询里利用上Covering Index,快速定位id,查询效率嗷嗷的

注: 本文是参考《MySQL性能优化案例 - 覆盖索引》 的一篇文章借题发挥,参考了原文的知识点,自己做了一点的发挥和研究,原文被多次转载,不知作者何许人也,也不知出处在哪个,如需原文请自行搜索。
