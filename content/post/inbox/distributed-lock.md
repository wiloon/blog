---
title: distributed lock 分布式锁
author: "-"
date: "2021-07-11 08:27:49"
url: distributed-lock
categories:
  - lock
tags:
  - lock
---
## distributed lock 分布式锁

分布式是一种分布式协调技术，控制分布式系统不同进程共同访问共享资源的一种锁的实现。如果不同的系统或同一个系统的不同主机之间共享了某个临界资源，往往需要互斥来防止彼此干扰，以保证一致性。

分布式锁是由于单机锁无法满足分布式系统锁，在多进程/分布式环境下，需要分布式锁来控制共享内容，保证线程的安全。

### 为何需要分布式锁
Martin Kleppmann 是英国剑桥大学的分布式系统的研究员，之前和 Redis 之父 Antirez 进行过关于 RedLock (红锁，后续有讲到) 是否安全的激烈讨论。

Martin 认为一般我们使用分布式锁有两个场景: 
- 效率: 使用分布式锁可以避免不同节点重复相同的工作，这些工作会浪费资源。比如用户付了钱之后有可能不同节点会发出多封短信。
- 正确性: 加分布式锁同样可以避免破坏正确性的发生，如果两个节点在同一条数据上面操作，
         比如多个节点机器对同一个订单操作不同的流程有可能会导致该笔订单最后状态出现错误，造成损失。

### 分布式锁的一些特点
当我们确定了在不同节点上需要分布式锁，那么我们需要了解分布式锁到底应该有哪些特点？

分布式锁的特点如下: 
- 互斥性: 和本地锁一样互斥性是锁最基本的特性, 任意时刻，只有一个客户端能持有锁。
- 可重入性: 同一个节点上的同一个线程如果获取了锁之后那么也可以再次获取这个锁。
- 超时释放: 锁失效机制, 防止死锁。正常情况下，请求获取锁之后，处理任务，处理完成之后释放锁。
           但是如果在处理任务发生服务异常，或者网络异常时，导致锁无法释放。其他请求都无法获取锁，变成死锁。 
           为了防止锁变成死锁，需要设置锁的超时时间。过了超时时间后，锁自动释放，其他请求能正常获取锁。
- 自动续期: 锁设置了超时机制后，如果持有锁的节点处理任务的时候过长超过了超时时间，就会发生线程未处理完任务锁就被释放了，
           其他线程就能获取到该锁，导致多个节点同时访问共享资源。对此，就需要延长超时时间。 
           开启一个监听线程，定时监听任务，监听任务线程还存活就延长超时时间。当任务完成、或者任务发生异常就不继续延长超时时间。
- 高可用, 高性能: 加锁和解锁需要高效，同时也需要保证高可用防止分布式锁失效，可以增加降级。
- 安全性: 锁只能被持有锁的客户端释放, 不能被其它客户端释放.
- 支持阻塞和非阻塞: 和 ReentrantLock 一样支持 lock 和 trylock 以及 tryLock(long timeOut)。即没有获取到锁将直接返回获取锁失败
- 支持公平锁和非公平锁(可选): 公平锁的意思是按照请求加锁的顺序获得锁，非公平锁就相反是无序的。这个一般来说实现的比较少。

### 分布式锁一般有三种实现方式: 
1. 数据库乐观锁
2. 基于 Redis 的分布式锁
3. 基于 ZooKeeper 的分布式锁

### 可靠性
首先，为了确保分布式锁可用，我们至少要确保锁的实现同时满足以下四个条件: 
- 互斥性。在任意时刻，只有一个客户端能持有锁。
- 不会发生死锁。即使有一个客户端在持有锁的期间崩溃而没有主动解锁，也能保证后续其他客户端能加锁。
- 具有容错性。只要大部分的 Redis 节点正常运行，客户端就可以加锁和解锁。
- 解铃还须系铃人。加锁和解锁必须是同一个客户端，客户端自己不能把别人加的锁给解了。

## Redis 实现分布式锁

Redis 实现分布式锁，性能会比关系式数据库高一些.

### 加锁

```Bash
set key0 value0 EX 3600 NX
```

如果键不存在时，对键设值，返回 1。如果键存在，不做任何操作, 返回 0, 同时设置超时时间 3600 秒, 防止死锁.

### 锁续期

加锁之后在业务代码执行过期中给 key 续期, 防止执行时间过长, 业务代码执行完成之前锁过期.

如果设置的超时时间比较短，而业务执行的时间比较长。比如超时时间设置5s，而业务执行需要10s，此时业务还未执行完，其他请求就会获取到锁，两个请求同时请求业务数据，不满足分布式锁的互斥性，无法保证线程的安全

如果业务时间大于超时时间，业务代码在获取到锁之后开一个单独的线程定时给锁续期.

```Bash
expire key0 3600
```

### 解锁

```Bash
get key0
# 判断是不是自己加的锁
DEL key0
```

通过删除 key 释放锁，删除键之后，其他线程可以争夺锁。

### 锁误删除

线程 A 执行完业务代码后，执行释放锁操作，而此时线程 A 加的锁已经被超时释放，锁被线程 B 持有，此时释放锁，就把线程 B 的锁误删了。

首先要将超时时间设置的长一些，满足业务执行的时间。如果系统对吞吐量要求比较严格，根据具体的业务的执行时间来设置超时时间，
超时时间比业务执行时间长一些，超时时间不能设置太长也不能设置太短。

针对锁误删除的问题。每个线程在获取锁时，设置一个的线程标识，比如 UUID，作为唯一的标识，设置 value 值，在解锁时，先判断是是否是自己线程的标识，如果不是，就不做删除

### redis 集群模式下的锁一致性问题

## 代码实现

首先我们要通过 Maven 引入 Jedis 开源组件，在 pom.xml 文件加入下面的代码: 

```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>2.9.0</version>
</dependency>
```

加锁代码
```java
public class RedisTool {
    private static final String LOCK_SUCCESS = "OK";
    private static final String SET_IF_NOT_EXIST = "NX";
    private static final String SET_WITH_EXPIRE_TIME = "PX";

    /**
     * 尝试获取分布式锁
     * @param jedis Redis客户端
     * @param lockKey 锁
     * @param requestId 请求标识
     * @param expireTime 超期时间
     * @return 是否获取成功
     */
    public static boolean tryGetDistributedLock(Jedis jedis, String lockKey, String requestId, int expireTime) {
        String result = jedis.set(lockKey, requestId, SET_IF_NOT_EXIST, SET_WITH_EXPIRE_TIME, expireTime);
        if (LOCK_SUCCESS.equals(result)) {
            return true;
        }
        return false;
    }
}
```

可以看到，我们加锁就一行代码: jedis.set(String key, String value, String nxxx, String expx, int time)，这个set()方法一共有五个形参: 
- 第一个为key，我们使用key来当锁，因为key是唯一的。
- 第二个为value，我们传的是requestId，很多童鞋可能不明白，有key作为锁不就够了吗，为什么还要用到value？原因就是我们在上面讲到可靠性时，分布式锁要满足第四个条件解铃还须系铃人，通过给value赋值为requestId，我们就知道这把锁是哪个请求加的了，在解锁的时候就可以有依据。requestId可以使用UUID.randomUUID().toString()方法生成。
- 第三个为nxxx，这个参数我们填的是NX，意思是SET IF NOT EXIST，即当key不存在时，我们进行set操作；若key已经存在，则不做任何操作；
- 第四个为expx，这个参数我们传的是PX，意思是我们要给这个key加一个过期的设置，具体时间由第五个参数决定。
- 第五个为time，与第四个参数相呼应，代表key的过期时间。

总的来说，执行上面的set()方法就只会导致两种结果: 1. 当前没有锁 (key不存在) ，那么就进行加锁操作，并对锁设置个有效期，同时value表示加锁的客户端。2. 已有锁存在，不做任何操作。

我们的加锁代码满足我们可靠性里描述的三个条件。首先，set()加入了NX参数，可以保证如果已有key存在，则函数不会调用成功，也就是只有一个客户端能持有锁，满足互斥性。其次，由于我们对锁设置了过期时间，即使锁的持有者后续发生崩溃而没有解锁，锁也会因为到了过期时间而自动解锁 (即key被删除) ，不会发生死锁。最后，因为我们将value赋值为requestId，代表加锁的客户端请求标识，那么在客户端在解锁的时候就可以进行校验是否是同一个客户端。由于我们只考虑Redis单机部署的场景，所以容错性我们暂不考虑。

### 解锁
有加锁就得有解锁。当得到锁的线程执行完任务，需要释放锁，以便其他线程可以进入。释放锁的最简单方式是执行 del 指令，伪代码如下:

```bash
del (lock_sale_ID) 
```

释放锁之后，其他线程就可以继续执行 setnx 命令来获得锁。

### 错误示例1
比较常见的错误示例就是使用jedis.setnx()和jedis.expire()组合实现加锁，代码如下: 

```java
public static void wrongGetLock1(Jedis jedis, String lockKey, String requestId, int expireTime) {

    Long result = jedis.setnx(lockKey, requestId);

    if (result == 1) {

        // 若在这里程序突然崩溃，则无法设置过期时间，将发生死锁
        jedis.expire(lockKey, expireTime);
    }
}
```

setnx()方法作用就是SET IF NOT EXIST，expire()方法就是给锁加一个过期时间。乍一看好像和前面的set()方法结果一样，然而由于这是两条Redis命令，不具有原子性，如果程序在执行完setnx()之后突然崩溃，导致锁没有设置过期时间。那么将会发生死锁。网上之所以有人这样实现，是因为低版本的jedis并不支持多参数的set()方法。

### 错误示例2



这一种错误示例就比较难以发现问题，而且实现也比较复杂。实现思路: 使用jedis.setnx()命令实现加锁，其中key是锁，value是锁的过期时间。执行过程: 1. 通过setnx()方法尝试加锁，如果当前锁不存在，返回加锁成功。2. 如果锁已经存在则获取锁的过期时间，和当前时间比较，如果锁已经过期，则设置新的过期时间，返回加锁成功。代码如下: 



public static boolean wrongGetLock2(Jedis jedis, String lockKey, int expireTime) {

 

    long expires = System.currentTimeMillis() + expireTime;

    String expiresStr = String.valueOf(expires);

 

    // 如果当前锁不存在，返回加锁成功

    if (jedis.setnx(lockKey, expiresStr) == 1) {

        return true;

    }

 

    // 如果锁存在，获取锁的过期时间

    String currentValueStr = jedis.get(lockKey);

    if (currentValueStr != null && Long.parseLong(currentValueStr) < System.currentTimeMillis()) {

        // 锁已过期，获取上一个锁的过期时间，并设置现在锁的过期时间

        String oldValueStr = jedis.getSet(lockKey, expiresStr);

        if (oldValueStr != null && oldValueStr.equals(currentValueStr)) {

            // 考虑多线程并发的情况，只有一个线程的设置值和当前值相同，它才有权利加锁

            return true;

        }

    }

         

    // 其他情况，一律返回加锁失败

    return false;

 

}



那么这段代码问题在哪里？1. 由于是客户端自己生成过期时间，所以需要强制要求分布式下每个客户端的时间必须同步。 2. 当锁过期的时候，如果多个客户端同时执行jedis.getSet()方法，那么虽然最终只有一个客户端可以加锁，但是这个客户端的锁的过期时间可能被其他客户端覆盖。3. 锁不具备拥有者标识，即任何客户端都可以解锁。

### 解锁代码
还是先展示代码，再带大家慢慢解释为什么这样实现: 


```java
public class RedisTool {
    private static final Long RELEASE_SUCCESS = 1L;
    
    /**
     * 释放分布式锁
     * @param jedis Redis客户端
     * @param lockKey 锁
     * @param requestId 请求标识
     * @return 是否释放成功
     */

    public static boolean releaseDistributedLock(Jedis jedis, String lockKey, String requestId) {
        String script = "if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) else return 0 end";

        Object result = jedis.eval(script, Collections.singletonList(lockKey), Collections.singletonList(requestId));
        if (RELEASE_SUCCESS.equals(result)) {
            return true;
        }
        return false;
    }
}
```

可以看到，我们解锁只需要两行代码就搞定了！第一行代码，我们写了一个简单的Lua脚本代码，上一次见到这个编程语言还是在《黑客与画家》里，没想到这次居然用上了。第二行代码，我们将Lua代码传到jedis.eval()方法里，并使参数KEYS[1]赋值为lockKey，ARGV[1]赋值为requestId。eval()方法是将Lua代码交给Redis服务端执行。

那么这段Lua代码的功能是什么呢？其实很简单，首先获取锁对应的value值，检查是否与requestId相等，如果相等则删除锁 (解锁) 。那么为什么要使用Lua语言来实现呢？因为要确保上述操作是原子性的。关于非原子性会带来什么问题，可以阅读【解锁代码-错误示例2】 。那么为什么执行eval()方法可以确保原子性，源于Redis的特性，下面是官网对eval命令的部分解释: 

http://wudashan.cn/2017/10/23/Redis-Distributed-Lock-Implement/#releaseLock-wrongDemo2


简单来说，就是在eval命令执行Lua代码的时候，Lua代码将被当成一个命令去执行，并且直到eval命令执行完成，Redis才会执行其他命令。

错误示例1

最常见的解锁代码就是直接使用jedis.del()方法删除锁，这种不先判断锁的拥有者而直接解锁的方式，会导致任何客户端都可以随时进行解锁，即使这把锁不是它的。

public static void wrongReleaseLock1(Jedis jedis, String lockKey) {
    jedis.del(lockKey);
}

错误示例2
这种解锁代码乍一看也是没问题，甚至我之前也差点这样实现，与正确姿势差不多，唯一区别的是分成两条命令去执行，代码如下: 

public static void wrongReleaseLock2(Jedis jedis, String lockKey, String requestId) {
    // 判断加锁与解锁是不是同一个客户端

    if (requestId.equals(jedis.get(lockKey))) {

        // 若在此时，这把锁突然不是这个客户端的，则会误解锁

        jedis.del(lockKey);

    }

 

}



如代码注释，问题在于如果调用jedis.del()方法的时候，这把锁已经不属于当前客户端的时候会解除他人加的锁。那么是否真的有这种场景？答案是肯定的，比如客户端A加锁，一段时间之后客户端A解锁，在执行jedis.del()之前，锁突然过期了，此时客户端B尝试加锁成功，然后客户端A再执行del()方法，则将客户端B的锁给解除了。



总结



本文主要介绍了如何使用Java代码正确实现Redis分布式锁，对于加锁和解锁也分别给出了两个比较经典的错误示例。其实想要通过Redis实现分布式锁并不难，只要保证能满足可靠性里的四个条件。互联网虽然给我们带来了方便，只要有问题就可以google，然而网上的答案一定是对的吗？其实不然，所以我们更应该时刻保持着质疑精神，多想多验证。



如果你的项目中Redis是多机部署的，那么可以尝试使用Redisson实现分布式锁，这是Redis官方提供的Java组件，链接在参考阅读章节已经给出。

### 分布式锁的实现
Memcached: 利用 Memcached 的 add 命令。此命令是原子性操作，只有在 key 不存在的情况下，才能 add 成功，也就意味着线程得到了锁。
Redis: 和 Memcached 的方式类似，利用 Redis 的 setnx 命令。此命令同样是原子性操作，只有在 key 不存在的情况下，才能 set 成功。
Zookeeper: 利用 Zookeeper 的顺序临时节点，来实现分布式锁和等待队列。Zookeeper 设计的初衷，就是为了实现分布式锁服务的。
Chubby: Google 公司实现的粗粒度分布式锁服务，底层利用了 Paxos 一致性算法。


---
Distributed locks with Redis

https://redis.io/topics/distlock

EVAL command

https://redis.io/commands/eval

Redisson

https://github.com/redisson/redisson


https://mp.weixin.qq.com/s/qJK61ew0kCExvXrqb7-RSg

> https://mp.weixin.qq.com/s/hoZB0wdwXfG3ECKlzjtPdw
> https://xiaomi-info.github.io/2019/12/17/redis-distributed-lock/
> https://blog.csdn.net/qq_40722827/article/details/102993655
> https://xie.infoq.cn/article/d5d3f794a6f5866a7f4a0d082?utm_source=rss&utm_medium=article
> https://www.cnblogs.com/jeremylai7/p/17332101.html