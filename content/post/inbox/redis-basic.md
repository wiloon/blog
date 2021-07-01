+++
author = "-"
date = "2021-06-22 16:40:12" 
title = "redis basic"
url = "redis-basic"
+++

### java sdk
- redisson
- jedis

### 查看版本等信息
    info

### version
    current: 5.0.5
    latest: 6.2

### URLs
    https://redis.io/
    https://github.com/redis/redis

### install

#### rpm
download redis rpm from https://pkgs.org/download/redis
  
下载Redis的依赖包: libjemalloc

下载地址: https://pkgs.org/centos-6/atomic-x86_64/jemalloc-3.6.0-1.el6.art.x86_64.rpm.html

```bash
rpm -ivh jemalloc-3.6.0-1.el6.art.x86_64.rpm
rpm -ivh redis-2.8.20-3.el6.art.x86_64.rpm
```
### ubuntu
    sudo apt-get install redis-server
### podman, 单机redis
```bash
podman run \
-d \
--name redis \
-p 6379:6379 \
-v /etc/localtime:/etc/localtime:ro \
redis:6.2.4

podman run -it --rm redis redis-cli -h redis.wiloon.com


podman run \
-d \
--name redis \
-p 6379:6379 \
-v /etc/localtime:/etc/localtime:ro \
-v redis-conf:/usr/local/etc/redis \
-v redis-data:/data/redis \
redis:6.2.4 redis-server /usr/local/etc/redis/redis.conf

```

```bash
redis-server --version
```
### list all keys
    keys *
### delete key
del key1 key2

### unlink
    unlink key [key ...]
### 判断key是否存在
exists key_name

### 查看key的类型
    type key0

### 删除 key
    DEL key [key ...]

### 设置过期时间

EXPIRE key0 10

### ttl: 返回给定 key 的剩余生存时间(TTL, time to live)
    TTL key
### 查看各个库的key数量
    info keyspace

以秒为单位，返回给定 key 的剩余生存时间(TTL, time to live)。

可用版本: >= 1.0.0

时间复杂度: O(1)

返回值: 
  
当 key 不存在时，返回 -2 。
  
当 key 存在但没有设置剩余生存时间时，返回 -1 。
  
否则，以秒为单位，返回 key 的剩余生存时间。

O(N) where N is the number of keys that will be removed. When a key to remove holds a value other than a string, the individual complexity for this key is O(M) where M is the number of elements in the list, set, sorted set or hash. Removing a single key that holds a string value is O(1).

```bash
redis-cli -h 127.0.0.1 -p 6379

#cluster
redis-cli -c -h 127.0.0.1 -p 6379

# 不进入交互模式, 直接执行命令
redis-cli -h 127.0.0.1 -p 6379 hget key0 field0

client list
client kill ip:port

#查特定pattern的key 数量
redis-cli keys *xxx* |grep "" -c

批量删除Redis下特定pattern的keys
可以使用linux的xargs来做到如: 
*/redis-cli keys "prefix*" | xargs */redis-cli del 

如果是访问特定的数据库，则可以: 
*/redis-cli -n 0 keys "prefix*" | xargs */redis-cli -n 0 del

set set key0 value0 
get del key 
#delete key 

redis-server.exe 
redis.windows.conf 
redis-cli.exe

#当前数据库中key的数量 
DBSIZE

#清空当前数据库 
flushdb 

#info
# http://redisdoc.com/server/info.html
```

### cluster

```bash
创建集群主节点

redis-cli --cluster create 192.168.163.132:6379 192.168.163.132:6380 192.168.163.132:6381
创建集群主从节点

/redis-cli --cluster create 192.168.163.132:6379 192.168.163.132:6380 192.168.163.132:6381 192.168.163.132:6382 192.168.163.132:6383 192.168.163.132:6384 --cluster-replicas 1

#  检查集群
redis-cli --cluster check 192.168.163.132:6384 --cluster-search-multiple-owners

# 集群信息查看
redis-cli --cluster info 192.168.163.132:6384
# 修复集群
redis-cli --cluster fix 192.168.163.132:6384 --cluster-search-multiple-owners
# 添加集群主节点

redis-cli --cluster add-node 192.168.163.132:6382 192.168.163.132:6379 
说明: 为一个指定集群添加节点，需要先连到该集群的任意一个节点IP（192.168.163.132:6379），再把新节点加入。该2个参数的顺序有要求: 新加入的节点放前
# 添加集群从节点

redis-cli --cluster add-node 192.168.163.132:6382 192.168.163.132:6379 --cluster-slave --cluster-master-id 117457eab5071954faab5e81c3170600d5192270
说明: 把6382节点加入到6379节点的集群中，并且当做node_id为 117457eab5071954faab5e81c3170600d5192270 的从节点。如果不指定 --cluster-master-id 会随机分配到任意一个主节点。

删除节点

redis-cli --cluster del-node 192.168.163.132:6384 f6a6957421b00009106cb36be3c7ba41f3b603ff
说明: 指定IP、端口和node_id 来删除一个节点，从节点可以直接删除，主节点不能直接删除，删除之后，该节点会被shutdown。



```


### unlink 命令
    unlink key [key ...]
    该命令和DEL十分相似：删除指定的key(s),若key不存在则该key被跳过。但是，相比DEL会产生阻塞，该命令会在另一个线程中回收内存，因此它是非阻塞的。 这也是该命令名字的由来：仅将keys从keyspace元数据中删除，真正的删除会在后续异步操作。

释放key代价计算函数lazyfreeGetFreeEffort()，集合类型键，且满足对应编码，cost就是集合键的元数个数，否则cost就是1.
    List：4.0只有一种编码，quicklist，所以编码无限制，直接返回element个数。
    Set：非hash table编码，即intset编码时返回1.当一个集合只包含整数值元素， 并且这个集合的元素数量不多时， Redis 就会使用intset作为集合键的底层实现。
    Hash：同上。
        当hash键值满足下面任意条件编码为hash table：
    ->element count > "hash-max-ziplist-entries",default 512. ->value length > "hash-max-ziplist-value",default 64
    Zset：非skiplist编码，返回1.
       当zset键值满足下面任意条件编码为hash table：
    ->element count >"zset-max-ziplist-entries"，default 128 ->value length > "zset-max-ziplist-value", default 64
     举例： 1 一个包含100元素的list key, 它的free cost就是100 2 一个512MB的string key, 它的free cost是
     
    总结：
    
        不管是del还是unlink，key都是同步删除的。
        使用unlink命令时，如果value分配的空间不大，使用异步删除反而会降低效率，所以redis会先评估一下free value的effort，根据effort的值来决定是否做异步删除。
        使用unlink命令时，由于string类型的effort一直返回的是1，z所以string类型不会做异步删除。

作者：willcat
链接：https://juejin.cn/post/6844903810792423432
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


### FLUSHALL
可用版本： >= 1.0.0
时间复杂度： O(N)
清空整个 Redis 服务器的数据(删除所有数据库的所有 key )。

### FLUSHALL ASYNC (Redis 4.0.0 or greater)
Redis is now able to delete keys in the background in a different thread without blocking the server. An ASYNC option was added to FLUSHALL and FLUSHDB in order to let the entire dataset or a single database to be freed asynchronously.

### flushdb 
执行删除在某个db环境下执行的话，只删除当前db的数据
