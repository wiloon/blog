---
title: "redis, memcache"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "redis, memcache"

Redis 和 Memcached 都是基于内存的数据存储系统。Memcached是高性能分布式内存缓存服务，其本质上就是一个内存key-value数据库。Redis是一个开源的key-value存储系统。与Memcached类似，Redis将大部分数据存储在内存中，支持的数据类型包括: 字符串、哈希表、链表、集合、有序集合以及基于这些数据类型的相关操作。那么，Memcached与Redis有什么区别呢？

1. 数据操作不同, Redis支持的数据类型要丰富得多
与Memcached仅支持简单的key-value结构的数据记录不同，Redis支持的数据类型要丰富得多。
Memcached基本只支持简单的key-value存储，不支持枚举，不支持持久化和复制等功能。
Redis支持服务器端的数据操作相比Memcached来说，拥有更多的数据结构和并支持更丰富的数据操作，支持list、set、sorted set、hash等众多数据结构，还同时提供了持久化和复制等功能。而通常在Memcached里，使用者需要将数据拿到客户端来进行类似的修改再set回去，这大大增加了网络IO的次数和数据体积。在Redis中，这些复杂的操作通常和一般的GET/SET一样高效。所以，如果需要缓存能够支持更复杂的结构和操作， Redis会是更好的选择。

2. 内存管理机制不同
在Redis中，并不是所有的数据都一直存储在内存中的。这是和Memcached相比一个最大的区别。当物理内存用完时，Redis可以将一些很久没用到的value交换到磁盘。Redis只会缓存所有的key的信息，如果Redis发现内存的使用量超过了某一个阀值，将触发swap的操作，Redis根据“swappability = age*log(size_in_memory)”计算出哪些key对应的value需要swap到磁盘。然后再将这些key对应的value持久化到磁盘中，同时在内存中清除。这种特性使得Redis可以保持超过其机器本身内存大小的数据。

而Memcached默认使用Slab Allocation机制管理内存，其主要思想是按照预先规定的大小，将分配的内存分割成特定长度的块以存储相应长度的key-value数据记录，以完全解决内存碎片问题。

从内存利用率来讲，使用简单的key-value存储的话，Memcached的内存利用率更高。而如果Redis采用hash结构来做key-value存储，由于其组合式的压缩，其内存利用率会高于Memcached。

3. 性能不同
由于Redis只使用单核，而Memcached可以使用多核，所以平均每一个核上Redis在存储小数据时比Memcached性能更高。而在100k以上的数据中，Memcached性能要高于Redis，虽然Redis也在存储大数据的性能上进行了优化，但是比起Memcached，还是稍有逊色。

4. 集群管理不同
Memcached是全内存的数据缓冲系统，Redis虽然支持数据的持久化，但是全内存毕竟才是其高性能的本质。作为基于内存的存储系统来说，机器物理内存的大小就是系统能够容纳的最大数据量。如果需要处理的数据量超过了单台机器的物理内存大小，就需要构建分布式集群来扩展存储能力。

Memcached本身并不支持分布式，因此只能在客户端通过像一致性哈希这样的分布式算法来实现Memcached的分布式存储。相较于Memcached只能采用客户端实现分布式存储，Redis更偏向于在服务器端构建分布式存储。

### 持久性
redis支持数据落地持久化存储,可以将内存中的数据保持在磁盘中，重启的时候可以再次加载进行使用。 
memcache不支持数据持久存储 

小结: Redis和Memcached哪个更好？

Redis更多场景是作为Memcached的替代者来使用，当需要除key-value之外的更多数据类型支持或存储的数据不能被剔除时，使用Redis更合适。如果只做缓存的话，Memcached已经足够应付绝大部分的需求，Redis 的出现只是提供了一个更加好的选择。总的来说，根据使用者自身的需求去选择才是最合适的。

It’s not uncommon to hear Redis compared to memcached, which is a very high-
performance, key-value cache server. Like memcached, Redis can also store a mapping
of keys to values and can even achieve similar performance levels as memcached. But the similarities end quickly—Redis supports the writing of its data to disk automatically
in two different ways, and can store data in four structures in addition to plain string keys
as memcached does. These and other differences allow Redis to solve a wider range of
problems, and allow Redis to be used either as a primary database or as an auxiliary data-
base with other storage systems.


数据类型
Redis支持的数据类型要丰富得多,Redis不仅仅支持简单的k/v类型的数据，同时还提供String，List,Set,Hash,Sorted Set,pub/sub,Transactions数据结构的存储。其中Set是HashMap实现的，value永远为null而已
memcache支持简单数据类型，需要客户端自己处理复杂对象 


分布式存储
redis支持master-slave复制模式
memcache可以使用一致性hash做分布式
 
 
value大小不同
memcache是一个内存缓存，key的长度小于250字符，单个item存储要小于1M，不适合虚拟机使用
 
数据一致性不同
Redis只使用单核，而Memcached可以使用多核，所以平均每一个核上Redis在存储小数据时比Memcached性能更高。而在100k以上的数据中，Memcached性能要高于Redis，虽然Redis最近也在存储大数据的性能上进行优化，但是比起Memcached，还是稍有逊色。 
redis使用的是单线程模型，保证了数据按顺序提交。
memcache需要使用cas保证数据一致性。CAS (Check and Set) 是一个确保并发一致性的机制，属于“乐观锁”范畴；原理很简单: 拿版本号，操作，对比版本号，如果一致就操作，不一致就放弃任何操作 
cpu利用
redis单线程模型只能使用一个cpu，可以开启多个redis进程

---

https://segmentfault.com/a/1190000023217491
