---
title: distributed lock 分布式锁
author: "-"
date: 2026-03-20T18:46:40+08:00
url: distributed-lock
categories:
  - CS
tags:
  - lock
  - remix
  - AI-assisted
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

Redis Cluster (集群模式) 与主从模式本质上面临**同样的问题**。

Redis Cluster 内部结构如下:

```text
Redis Cluster
├── Shard 1: Master A  →  Slave A'
├── Shard 2: Master B  →  Slave B'
└── Shard 3: Master C  →  Slave C'
```

当客户端对某个 key 加锁时, 该 key 会根据哈希槽 (Hash Slot) 路由到某一个 Shard 的 Master 上 (例如 Master A)。此时问题与主从模式完全相同:

1. 客户端在 Master A 上加锁成功
2. Master A 在将锁同步到 Slave A' 之前宕机
3. Slave A' 晋升为新 Master
4. 新 Master 上没有这把锁, 其他客户端可以再次加锁成功
5. **互斥性被破坏**

**为什么 Redis Cluster 无法解决这个问题?**

Redis 的主从复制是**异步**的。Master 写入成功后立即返回客户端 OK, 再异步将数据同步给 Slave。这个异步复制的窗口期决定了无论是单主从还是 Cluster, 都存在锁丢失的可能。

Redis Cluster 解决的是**水平扩展**和**部分节点故障时的可用性**问题, 而不是分布式锁的一致性问题。

**Redlock 与 Redis Cluster 的对比**

| 方案 | 高可用 | 锁一致性 | 原理 |
|------|--------|---------|------|
| 单节点 Redis | ❌ | ✅ (无故障时) | 单点 |
| Redis 主从 / Cluster | ✅ | ❌ (Failover 时可能丢锁) | 异步复制 |
| Redlock (5 独立节点) | ✅ | ✅ (概率上安全) | 多数派写入 |

> **结论**: 如果你的 Redis 是集群模式, 同样需要使用 Redlock (多个独立节点, 不是 Cluster 的不同 Shard) 或者换用 ZooKeeper/etcd 来保证分布式锁的严格互斥性。

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

- **Memcached**: 利用 Memcached 的 add 命令。此命令是原子性操作，只有在 key 不存在的情况下，才能 add 成功，也就意味着线程得到了锁。
- **Redis**: 和 Memcached 的方式类似，利用 Redis 的 setnx 命令。此命令同样是原子性操作，只有在 key 不存在的情况下，才能 set 成功。
- **Zookeeper**: 利用 Zookeeper 的顺序临时节点，来实现分布式锁和等待队列。Zookeeper 设计的初衷，就是为了实现分布式锁服务的。
- **Chubby**: Google 公司实现的粗粒度分布式锁服务，底层利用了 Paxos 一致性算法。

## Redlock 红锁

### 背景: 单节点 Redis 锁的不足

前面介绍的 Redis 分布式锁方案都基于**单个 Redis 节点**。单节点方案存在一个致命缺陷: 如果这个 Redis 节点发生故障 (宕机、网络分区等), 锁服务将完全不可用。

为了解决高可用问题, 很多人会想到用 Redis 主从复制 (Master-Slave)。但主从方案同样存在问题:

1. 客户端 A 在 Master 上加锁成功
2. Master 尚未将该 key 同步到 Slave 时发生宕机
3. Slave 晋升为新 Master, 但新 Master 上没有这把锁
4. 客户端 B 在新 Master 上加锁成功
5. 此时客户端 A 和客户端 B 同时持有锁, **互斥性被破坏**

正是为了解决这个问题, Redis 作者 Antirez 提出了 **Redlock 算法**。

### Redlock 算法

Redlock 要求部署**奇数个** (通常为 5 个) **完全独立**的 Redis 节点 (无主从关系, 互不通信)。

**加锁流程:**

1. 客户端获取当前时间戳 $t_1$ (毫秒级)
2. 依次向 N 个 Redis 节点发送加锁请求, 使用相同的 key 和唯一的随机 value (UUID), 并设置锁的过期时间 TTL
   - 每次请求设置较短的超时时间 (远小于 TTL), 若某个节点超时则立即跳过该节点
3. 获取当前时间戳 $t_2$, 计算加锁耗时 $\Delta t = t_2 - t_1$
4. **判断是否加锁成功**: 需同时满足两个条件:
   - 成功加锁的节点数 >= N/2 + 1 (即超过半数)
   - 锁的有效剩余时间 = TTL - Δt > 0
5. 如果加锁失败, 向所有节点发送解锁请求

**解锁流程:**

向所有 N 个节点发送解锁请求 (无论该节点是否加锁成功), 使用 Lua 脚本保证原子性。

以 5 个节点为例:

```text
Client
  │
  ├──► Redis Node 1  ✅ 加锁成功
  ├──► Redis Node 2  ✅ 加锁成功
  ├──► Redis Node 3  ✅ 加锁成功   ← 获得 3/5 多数, 加锁成功
  ├──► Redis Node 4  ❌ 超时/失败
  └──► Redis Node 5  ❌ 超时/失败
```

### Redlock 的争议: Martin vs Antirez

Redlock 提出后, 引发了分布式系统领域的一场著名论战。

**Martin Kleppmann 的批评 (2016)**

《Designing Data-Intensive Applications》的作者 Martin Kleppmann 发文指出 Redlock 存在根本性缺陷:

1. **时钟漂移问题**: Redlock 依赖各节点的系统时钟相对准确。如果某个节点的时钟发生跳跃 (NTP 同步、虚拟机暂停等), 会导致锁提前过期, 破坏互斥性。

2. **GC Stop-the-World 问题**: 客户端在成功获取锁后, 如果发生长时间 GC 暂停, 此时锁可能已经过期并被其他客户端持有, 而 GC 恢复后的客户端仍然以为自己持有锁。

   ```text
   Client A 获取锁 → GC 暂停 50s → 锁过期 → Client B 获取锁
                                              ↓
   Client A GC 恢复 → 仍以为持有锁 → 两个客户端同时操作共享资源 ❌
   ```

3. **Martin 的结论**: 如果只是为了效率 (避免重复工作), Redlock 太重了 (部署 5 个节点代价大); 如果是为了正确性 (强一致), Redlock 又不够安全 (时钟问题)。推荐使用 ZooKeeper 等基于共识算法的系统实现分布式锁。

**Antirez 的回应**

Redis 作者 Antirez 随后回应:

1. 时钟跳跃是运维问题, 正常配置下不会发生大幅跳跃, Redlock 只要求不发生大的时钟偏移, 而非绝对精确
2. GC 暂停的问题同样存在于其他分布式锁方案 (包括 ZooKeeper), 不是 Redlock 独有的问题

**Fencing Token 方案**

Martin 提出了 **Fencing Token** 的概念来彻底解决 GC 暂停导致的问题:

锁服务每次颁发锁时附带一个单调递增的 token (如 33, 34, 35...), 客户端操作共享资源时必须携带该 token, 服务端拒绝携带过期 token 的请求。

```text
Client 1: 获取锁, token=33 → GC 暂停
Client 2: 获取锁, token=34 → 操作资源 (token=34)
Client 1: GC 恢复 → 携带 token=33 操作资源 → 被服务端拒绝 ✅
```

这需要**资源服务端的配合**, 仅靠锁服务本身无法做到。

### Redlock 的适用场景

综合来看:

| 场景 | 建议方案 |
|------|---------|
| 单 Redis 节点, 追求简单 | `SET key value NX EX` |
| 需要高可用, 允许极低概率的安全问题 | Redlock |
| 强一致性要求, 不能容忍任何互斥性破坏 | ZooKeeper / etcd |
| Java 生态, 需要生产级实现 | Redisson (封装了 Redlock) |

> Redlock 适合对**效率**有要求、能容忍极低概率失败的场景。对于金融级强一致性场景, 应优先考虑基于 Raft/Paxos 的方案 (etcd、ZooKeeper)。

### Redlock 的实际部署成本

**Redlock 要求 5 个独立 Redis 节点**, 这意味着仅为了分布式锁就需要额外维护 5 台 Redis 实例。这个成本对于大多数中小规模系统来说是相当高昂的。

**实际上 Redlock 的使用场景相对有限:**

- 需要分布式锁的系统往往已经有了 Redis 集群用于缓存, 但这套缓存集群**不能直接复用**于 Redlock (Cluster 的 Shard 不等于独立节点)
- 专门为锁再部署 3~5 个独立 Redis 实例, 运维成本和资源成本都不低
- 而 Redlock 本身的安全性还受到时钟漂移、GC 等质疑

**大多数生产系统的实际选择:**

| 规模 | 常见选择 | 理由 |
|------|---------|------|
| 小型系统 | 单节点 Redis `SET NX EX` | 够用, 节点故障概率极低, 加业务幂等兜底 |
| 中型系统 | Redisson 单节点锁 + 看门狗 | 生产级封装, 自动续期, 无需自己维护 5 个节点 |
| 大型系统 (已有 etcd/ZK) | etcd / ZooKeeper | 利用已有基础设施, 一致性更强 |
| 确实需要高可用 Redis 锁 | Redisson RedLock (3 节点) | 3 个节点是可接受的最小多数派 |

**Martin 的原话实际上是一个有力的反驳:**

> 如果你只是为了提高效率, 使用单个 Redis 实例就足够了。节点偶发宕机导致锁失效的概率极低, 配合业务幂等完全可以接受。如果你需要更强的正确性保证, 那应该用 ZooKeeper 而不是 Redlock。

**结论**: Redlock 适合那些**已经在运维多套 Redis 独立实例**、同时对锁的可用性有较高要求、但又不想引入 ZooKeeper/etcd 的场景。如果从零开始选型, 大多数情况下 **单节点 Redisson + 业务幂等** 是更实用的选择。

### Redisson 的 Redlock 实现

Redisson 是 Redis 官方推荐的 Java 客户端, 提供了开箱即用的 Redlock 实现:

```java
RLock lock1 = redisson1.getLock("lock1");
RLock lock2 = redisson2.getLock("lock1");
RLock lock3 = redisson3.getLock("lock1");

// 使用 3 个独立 Redis 节点创建红锁
RedissonRedLock redLock = new RedissonRedLock(lock1, lock2, lock3);

try {
    // 尝试加锁, 最多等待 500ms, 锁持有时间 30s
    boolean isLocked = redLock.tryLock(500, 30000, TimeUnit.MILLISECONDS);
    if (isLocked) {
        // 执行业务逻辑
    }
} finally {
    redLock.unlock();
}
```

Redisson 还提供了**看门狗 (Watchdog)** 机制自动续期: 默认情况下, 锁的过期时间是 30s, 看门狗每 10s 检查一次业务是否还在执行, 如果是则自动续期, 避免锁提前过期的问题。

## PostgreSQL 实现分布式锁

### Redis 主从问题的根源

Redis 主从同步问题的根源是: **Redis 的复制永远是异步的**。Master 写入成功就立即返回客户端, 不等待 Slave 确认。这是 Redis 的架构设计决策, 无法通过配置改变。

### PostgreSQL 的两种锁实现方式

#### 方式一: Advisory Lock (咨询锁)

PostgreSQL 内置了 Advisory Lock 机制:

```sql
-- 获取锁 (阻塞)
SELECT pg_advisory_lock(12345);

-- 尝试获取锁 (非阻塞, 失败返回 false)
SELECT pg_try_advisory_lock(12345);

-- 释放锁
SELECT pg_advisory_unlock(12345);
```

**Advisory Lock 的特点:**
- 存储在**共享内存**中, **不写入 WAL**, 因此**不会复制**到 Standby
- Session 级别: 连接断开后自动释放 (天然防死锁)
- 性能极高, 无磁盘 I/O

**Advisory Lock 与 Redis 的对比:**

对于主从故障转移, Advisory Lock 和 Redis 锁面临**类似的问题**: Primary 宕机后, Standby 晋升为新 Primary, 内存中的 Advisory Lock 全部消失。但这里有一个微妙的区别: Redis 锁失效是因为异步复制导致锁记录丢失; Advisory Lock 则是根本就没有复制, 但同时也意味着崩溃后锁**必然**被清空 — 不存在"锁记录存在但实际持有者已崩溃"的状态不一致。

#### 方式二: 行级锁 (Lock Table)

用一张专门的锁表, 通过行记录来代表锁:

```sql
CREATE TABLE distributed_locks (
    lock_name TEXT PRIMARY KEY,
    locked_by TEXT NOT NULL,
    locked_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL
);

-- 加锁 (原子操作, 冲突则失败)
INSERT INTO distributed_locks (lock_name, locked_by, expires_at)
VALUES ('order:123', 'node-a-uuid', now() + interval '30 seconds')
ON CONFLICT (lock_name) DO NOTHING;

-- 检查是否加锁成功 (affected rows = 1 表示成功)

-- 解锁 (只能释放自己的锁)
DELETE FROM distributed_locks
WHERE lock_name = 'order:123' AND locked_by = 'node-a-uuid';

-- 清理过期锁 (防止死锁)
DELETE FROM distributed_locks WHERE expires_at < now();
```

### PostgreSQL 同步复制: 根本性的区别

这是 PostgreSQL 与 Redis 最关键的区别。**PostgreSQL 支持同步复制**, 可以通过配置要求 Primary 必须等待 Standby 确认写入后才返回事务提交成功:

```ini
# postgresql.conf on Primary
synchronous_commit = remote_apply     # 等待 Standby 应用 WAL 后才提交
synchronous_standby_names = 'standby1'
```

配置同步复制后, 行级锁的写入流程:

```text
Client
  │
  ▼
Primary: INSERT INTO distributed_locks ...
  │
  │── WAL 同步写入 ──► Standby: 应用 WAL ──► 确认
  │◄───────────────────────────────────────────
  │
  ▼
事务提交, 返回客户端成功
```

此时发生 Failover:

1. Primary 宕机
2. Standby 晋升为新 Primary
3. **新 Primary 上有完整的锁记录** (因为同步复制已确保)
4. 其他客户端尝试对同一 lock_name 加锁 → `ON CONFLICT DO NOTHING` → 加锁失败
5. **互斥性完好**

**这是 Redis 无论如何都做不到的。**

### 对比总结

| 维度 | Redis (Redlock) | PostgreSQL Advisory Lock | PostgreSQL 行级锁 + 同步复制 |
|------|-----------------|--------------------------|------------------------------|
| 复制方式 | 永远异步 | 不复制 (内存) | 可配置同步 |
| Failover 后锁是否安全 | ❌ 可能丢锁 | ⚠️ 锁消失 (但状态一致) | ✅ 锁记录保留 |
| 性能 | 极高 | 极高 | 中等 (有磁盘 I/O) |
| 部署复杂度 | 需 5 个独立节点 | 简单 | 简单 (利用现有 PG) |
| 适用场景 | 高并发, 允许极低概率失败 | 轻量级, 同库内协调 | 强一致性要求, 数据量不大 |

### 实践建议

如果系统**已经有 PostgreSQL 主从**, 且对锁的一致性有要求:

1. 开启 `synchronous_commit = remote_apply`
2. 用行级锁表实现分布式锁
3. 不需要额外部署任何中间件

代价是: 同步复制会增加写入延迟 (每次写要等 Standby 确认), 以及 Standby 不可用时 Primary 会等待超时。适合**对一致性要求高、并发量适中**的场景 (如后台任务调度、订单状态机控制等)。

> 高并发场景 (如秒杀) 仍然首选 Redis, 但需要配合业务幂等兜底。不要期望分布式锁能解决所有问题。



### 选型决策树

```text
需要分布式锁?
    │
    ├── 单 Redis 节点 (开发/测试环境)?
    │       └── SET key value NX EX ttl  ✅ 够用
    │
    ├── 生产环境, 只追求效率 (偶发重复执行可接受)?
    │       └── Redisson 单节点锁 + 看门狗  ✅ 推荐
    │
    ├── 生产环境, 需要高可用 + 较强一致性?
    │       └── Redisson RedLock (3~5 独立节点)  ✅ 推荐
    │
    └── 金融/核心交易, 不能容忍任何互斥性破坏?
            └── etcd / ZooKeeper  ✅ 推荐
```

### 正确加锁姿势

**必须使用原子命令, 一步完成 set + expire:**

```bash
# ✅ 正确: 原子操作
SET lock_key unique_value NX EX 30

# ❌ 错误: 两步操作, 中间可能崩溃导致死锁
SETNX lock_key unique_value
EXPIRE lock_key 30
```

**value 必须是唯一标识 (UUID), 防止误删他人的锁:**

```java
// ✅ 正确
String lockValue = UUID.randomUUID().toString();
jedis.set(lockKey, lockValue, "NX", "EX", 30);

// 解锁时先验证是否是自己的锁
String script = "if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end";
jedis.eval(script, List.of(lockKey), List.of(lockValue));

// ❌ 错误: 不校验直接删, 可能误删他人的锁
jedis.del(lockKey);
```

### TTL 设置原则

- TTL 应**大于**业务最大预期执行时间, 留出足够余量
- 不要把 TTL 设得过长 (节点宕机后其他节点要等 TTL 过期才能继续)
- 不确定执行时长时, 使用**看门狗自动续期**代替静态 TTL

```java
// Redisson 看门狗: 不指定 leaseTime 时自动启用 30s TTL + 自动续期
RLock lock = redisson.getLock("myLock");
lock.lock();  // 看门狗每 10s 续期一次
try {
    // 业务逻辑
} finally {
    lock.unlock();
}
```

### 解锁必须放在 finally 块

```java
RLock lock = redisson.getLock("myLock");
lock.lock();
try {
    // 业务逻辑
} finally {
    // ✅ 无论业务成功还是异常, 都要解锁
    if (lock.isHeldByCurrentThread()) {
        lock.unlock();
    }
}
```

### 锁粒度要尽量小

```java
// ❌ 粒度太粗: 锁住整个方法, 并发度低
public synchronized void processOrder(String orderId) { ... }

// ✅ 粒度精细: 只锁单个订单, 不同订单可以并行
String lockKey = "order:lock:" + orderId;
RLock lock = redisson.getLock(lockKey);
```

### 非阻塞加锁优于阻塞等待

```java
// ✅ 推荐: tryLock 快速失败, 避免线程积压
boolean locked = lock.tryLock(100, 30000, TimeUnit.MILLISECONDS);
if (!locked) {
    // 快速返回, 让客户端重试或降级处理
    throw new ServiceException("系统繁忙, 请稍后重试");
}

// ⚠️ 慎用: lock() 无限等待, 高并发下可能撑爆线程池
lock.lock();
```

### 不要在锁内做耗时操作

锁持有期间发生网络调用、数据库慢查询等耗时操作, 会导致锁持有时间过长, 严重影响并发性。

```java
// ❌ 锁内做慢操作
lock.lock();
try {
    callRemoteService();   // 网络调用, 可能超时
    queryDatabase();       // 慢查询
} finally {
    lock.unlock();
}

// ✅ 锁外准备好数据, 锁内只做最小操作
Data data = prepareData();   // 锁外
lock.lock();
try {
    writeSharedResource(data);  // 只写共享资源, 快速完成
} finally {
    lock.unlock();
}
```

### 幂等性是分布式锁的重要补充

分布式锁无法 100% 保证互斥 (GC、时钟等极端情况), 业务逻辑本身应具备**幂等性**作为最后一道防线:

```java
// 即使锁失效导致重复执行, 幂等检查也能保证正确性
lock.lock();
try {
    if (orderService.isAlreadyProcessed(orderId)) {
        return;  // 幂等: 已处理过, 直接返回
    }
    orderService.process(orderId);
} finally {
    lock.unlock();
}
```

### 最佳实践总结

| 实践 | 要点 |
|------|------|
| 加锁 | `SET key value NX EX ttl` 原子命令, value 用 UUID |
| 解锁 | Lua 脚本原子校验 + 删除, 放在 finally |
| TTL | 大于业务执行时间, 或用看门狗自动续期 |
| 粒度 | 尽量细粒度, 减少锁竞争范围 |
| 等待 | 用 tryLock 超时快速失败, 避免线程积压 |
| 锁内操作 | 只做最小必要操作, 不做耗时 I/O |
| 兜底 | 业务逻辑实现幂等性, 作为最后防线 |
| 高可用 | 生产环境用 Redisson, 强一致用 etcd/ZooKeeper |

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