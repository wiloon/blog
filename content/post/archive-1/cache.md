---
title: 缓存
author: "-"
date: 2014-05-29T01:07:30+00:00
url: /?p=6682

---
## 缓存

https://xie.infoq.cn/article/0134f29b0c0895df548dd929b?utm_source=rss&utm_medium=article


缓存的存在,是为了调和差异。

差异有多种,比如处理器和存储之间的速度差异、用户对产品的使用体验和服务处理效率的差异等等。

CPU 缓存[2]。为了调和 CPU 和内存之间巨大的速度差异,设置了 L1/L2/L3 三级缓存,离 CPU 越近,速度越快。   

Ehcache[3]。是最流行了 Java 缓存框架之一。因为其开源属性,在 spring/Hibernate 等框架上被广泛使用。支持磁盘持久化和堆外内存。缓存功能齐全。

Guava cache。灵感来源于 ConcurrentHashMap,但具有更丰富的元素失效策略,功能没有 ehcache 齐全,如只支持 jvm 内存,但比较轻量简洁。

memcached。[5]  memcached 是一个高效的分布式内存 cache,搭建与操作使用都比较简单,整个缓存都是基于内存的,因此响应时间很快,但是没有持久化的能力。

Redis 以优秀的性能和丰富的数据结构,以及稳定性和数据一致性的支持,被业内越来越普遍的使用。
### 缓存预热
缓存预热就是系统上线后,将相关的缓存数据直接加载到缓存系统。这样就可以避免在用户请求的时候,先查询数据库,然后再将数据缓存的问题！用户直接查询事先被预热的缓存数据！

解决思路: 

1. 直接写个缓存刷新页面,上线时手工操作下；

2. 数据量不大,可以在项目启动的时候自动进行加载；

3. 定时刷新缓存；
### 缓存更新
除了缓存服务器自带的缓存失效策略之外（Redis默认的有6中策略可供选择) ,我们还可以根据具体的业务需求进行自定义的缓存淘汰,常见的策略有两种: 

（1) 定时去清理过期的缓存；

（2) 当有用户请求过来时,再判断这个请求所用到的缓存是否过期,过期的话就去底层系统得到新数据并更新缓存。

两者各有优劣,第一种的缺点是维护大量缓存的key是比较麻烦的,第二种的缺点就是每次用户请求过来都要判断缓存失效,逻辑相对比较复杂！具体用哪种方案,大家可以根据自己的应用场景来权衡。
 
### 缓存穿透 Cache Penetration
穿透形象一点就是: 请求过来了 转了一圈 一无所获 就像穿过透明地带一样。

在高并发系统中缓存穿透,其实是这样的如果一个req需要请求的key在缓存中没有,这时业务线程就会访问磁盘数据库系统,然而磁盘数据库也没有这个key,无奈业务线程只能返回null,白白处理一圈。

查询的是数据库中不存在的数据,没有命中缓存而数据库查询为空,也不会更新缓存。导致每次都查库,如果不加处理,遇到恶意攻击,会导致数据库承受巨大压力,直至崩溃。

解决方法
接口层实现 api 限流、防御 DDOS、接口频率限制、网关实现黑名单、用户授权、id 检查等

#### 缓存空对象: 
如果一个查询返回的数据为空（不管是数据不存在,还是系统故障) ,仍然把这个空结果进行缓存,但它的过期时间会很短,不超过 5 分钟。通过这个直接设置的默认值存放到缓存,这样第二次到缓存中获取就有值了,而不会继续访问数据库。当修改或者新增改 key 的数据信息的时候,需要删除或者更新 null 缓存值**

存在的问题: 
需要更多的键,所以通常设置较短过期时间

缓存层和存储层数据"短期"不一致

#### 布隆过滤器: 
对所有可能查询的参数以 hash 形式存储,在控制层先进行校验,不符合则丢弃,从而避免了对底层存储系统的查询压力。例如 Redis 可以使用 bitMap 来实现布隆过滤器。
>wiloon.com/bloom-filter

### 缓存击穿 Hotspot Invalid
单个热点 key 失效时,高并发查询数据库
一个存在的热点 key,在缓存过期的一刻,同时有大量的请求,这些请求都会击穿到数据库,造成瞬时数据库请求量大压力骤增。

解决方法
#### 使用分布式锁
保证在分布式情况下,使用分布式锁保证对于每个 key 同时只允许只有一个线程查询到后端服务,其他没有获取到锁的权限,只需要等待即可；这种高并发压力直接转移到分布式锁上,对分布式锁的压力非常大。获取到锁的请求将数据写入成功到 redis 中, 通知没有获取锁的请求直接从 Redis 获取数据即可

#### 使用本地缓存
二级缓存

#### 热点不过期
设置热点数据永不过期或者异步延长过期时间；

#### 到期前的续命
(在 value 设置一个比过期时间 t0 小的过期时间值 t1,当 t1 过期的时候,延长 t1 并做更新缓存操作。)


从字面意思看,缓存起初时起作用的。发生的场景是某些热点 key 的缓存失效导致大量热点请求打到数据库,导致数据库压力陡增,甚至宕机。

解决方案有两种: 

一种是热点 key 不过期。有的同学在这里提出了逻辑过期的方案,即物理上不设置过期时间,将期望的过期时间存在 value 中,在查询到 value 时,通过异步线程进行缓存重建。

第二种是从执行逻辑上进行限制,比如,起一个单一线程的线程池让热点 key 排队访问底层存储,以损失系统吞吐量的代价来维护系统稳定。


### 缓存雪崩 Cache Avalanche
缓存雪崩是指,由于缓存层承载着大量请求,有效的保护了存储层,但是如果缓存层由于某些原因整体不能提供服务（可能是机器宕机或大量的缓存(key)在同一时间失效 - 过期) ,于是所有的请求都会达到存储层,存储层的调用量会暴增,造成存储层也会挂掉的情况。

场景【多个 key 同时失效,高并发查询数据库】
缓存雪崩指缓存服务器重启（没有持久化) 或者大量的缓存集中在某个时间段失效,突然给数据库产生了巨大的压力,甚至击垮数据库的情况。

解决方案
对不用的数据使用随机动态分布的失效时间

使用集群化分摊部署我们 key

使用二级缓存

使用分布式锁

数据预热: 可以通过缓存 reload 机制,预先去更新缓存,再即将发生大并发访问前手动触发加载缓存不同的 key,设置不同的过期时间,让缓存失效的时间点尽量均匀

依赖隔离组件为后端限流并降级 在缓存失效后,通过加锁或者队列来控制读数据库写缓存的线程数量。比如对某个 key 只允许一个线程查询数据和写缓存,其他线程等待。


高并发系统,如果缓存系统故障,大量的请求无法从缓存完成数据请求,因此就全量汹涌冲向磁盘数据库系统,导致数据库被打死,整个系统彻底崩溃。

缓存雪崩我们可以简单的理解为: 由于原有缓存失效,新缓存未到期间(例如: 我们设置缓存时采用了相同的过期时间,在同一时刻出现大面积的缓存过期),所有原本应该访问缓存的请求都去查询数据库了,而对数据库CPU和内存造成巨大压力,严重的会造成数据库宕机。从而形成一系列连锁反应,造成整个系统崩溃。



鉴于缓存的作用,一般在数据存入时,会设置一个失效时间,如果插入操作是和用户操作同步进行,则该问题出现的可能性不大,因为用户的操作天然就是散列均匀的。

而另一些例如缓存预热的情况,依赖离线任务,定时批量的进行数据更新或存储,过期时间问题则要特别关注。

因为离线任务会在短时间内将大批数据操作完成,如果过期时间设置的一样,会在同一时间过期失效,后果则是上游请求会在同一时间将大量失效请求打到下游数据库,从而造成底层存储压力。同样的情况还发生在缓存宕机的时候。

解决方案: 

一是考虑热点数据不过期获取用上一节提到的逻辑过期。

二是让过期时间离散化,如,在固定的过期时间上额外增加一个随机数,这样会让缓存失效的时间分散在不同时间点,底层存储不至于瞬间飙升。

三是用集群主从的方式,保障缓存服务的高可用。防止全面崩溃。当然也要有相应的熔断和限流机制来应对可能的缓存宕机。

### 缓存降级
当访问量剧增、服务出现问题（如响应时间慢或不响应) 或非核心服务影响到核心流程的性能时,仍然需要保证服务还是可用的,即使是有损服务。系统可以根据一些关键数据进行自动降级,也可以配置开关实现人工降级。

降级的最终目的是保证核心服务可用,即使是有损的。而且有些服务是无法降级的（如加入购物车、结算) 。

在进行降级之前要对系统进行梳理,看看系统是不是可以丢卒保帅；从而梳理出哪些必须誓死保护,哪些可降级；比如可以参考日志级别设置预案: 

（1) 一般: 比如有些服务偶尔因为网络抖动或者服务正在上线而超时,可以自动降级；

（2) 警告: 有些服务在一段时间内成功率有波动（如在95~100%之间) ,可以自动降级或人工降级,并发送告警；

（3) 错误: 比如可用率低于90%,或者数据库连接池被打爆了,或者访问量突然猛增到系统能承受的最大阀值,此时可以根据情况自动降级或者人工降级；

（4) 严重错误: 比如因为特殊原因数据错误了,此时需要紧急人工降级。
 

2.4 数据漂移



### 缓存踩踏
缓存踩踏其实只是一种缓存失效场景的提法,底层原因是缓存为空或还未生效。关键是因为上游调用超时后唤起重试,引发恶性循环。

比如,当某一名人新发布了图片,而他们粉丝都会收到通知,大量的粉丝争先抢后的想去看发布了什么,但是,因为是新发布的图片,服务端还没有进行缓存,就会发生大量请求被打到底层存储,超过服务处理能力导致超时后,粉丝又会不停的刷新,造成恶性循环。

解决方案: 锁 和 Promise

发生这种踩踏的底层原因是对缓存这类公共资源拼抢,那么,就把公共资源加锁,消除并发拼抢。

但是,加锁在解决公共资源拼抢的同时,引发了另一个问题,即没有抢占到锁的线程会阻塞等待唤醒,当锁被释放时,所有线程被一同唤醒,大量线程的阻塞和唤醒是对服务器资源极大的消耗和浪费,即_惊群效应_。


promise 的工作原理

promise 的原理其实是一种_代理模式_,实际的缓存值被 promise 代替,所有的线程获取 promise 并等待 promise 返回给他们结果 , 而 promise 负责去底层存储获取数据,通过异步通知方式,最终将结果返回给各工作线程。

这样,就不会发生大量并发请求同时操作底层存储的情况。




https://segmentfault.com/a/1190000017375843


————————————————
版权声明: 本文为CSDN博主「徐刘根」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/xlgen157387/article/details/79530877


https://xie.infoq.cn/article/98bf087574f4c13fb3b5e8c23
