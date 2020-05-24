---
title: redis command
author: wiloon
type: post
date: 2015-09-24T08:09:01+00:00
url: /?p=8345
categories:
  - Uncategorized
tags:
  - Redis

---
### install

#### rpm

download redis rpm from https://pkgs.org/download/redis
  
下载Redis的依赖包：libjemalloc

下载地址：https://pkgs.org/centos-6/atomic-x86\_64/jemalloc-3.6.0-1.el6.art.x86\_64.rpm.html

```bashrpm -ivh jemalloc-3.6.0-1.el6.art.x86_64.rpm
rpm -ivh redis-2.8.20-3.el6.art.x86_64.rpm
```

### docker

```bashdocker run \
-d \
--name redis \
-p 6379:6379 \
-v /etc/localtime:/etc/localtime:ro \
--restart=always \
redis

docker run -it --rm redis redis-cli -h redis.wiloon.com

```

```bashredis-server --version
```

### delete key

del key1 key2

### 判断key是否存在

exists key_name

### 查看key的类型

type key0

### 删除 key

DEL key [key &#8230;]

### 设置过期时间

EXPIRE key0 10

### ttl: 返回给定 key 的剩余生存时间(TTL, time to live)

TTL key
  
以秒为单位，返回给定 key 的剩余生存时间(TTL, time to live)。
  
可用版本：>= 1.0.0
  
时间复杂度：O(1)
  
返回值：
  
当 key 不存在时，返回 -2 。
  
当 key 存在但没有设置剩余生存时间时，返回 -1 。
  
否则，以秒为单位，返回 key 的剩余生存时间。

O(N) where N is the number of keys that will be removed. When a key to remove holds a value other than a string, the individual complexity for this key is O(M) where M is the number of elements in the list, set, sorted set or hash. Removing a single key that holds a string value is O(1).

```bashredis-cli -h 127.0.0.1 -p 6379

#cluster
redis-cli -c -h 127.0.0.1 -p 6379

# 不进入交互模式,直接执行命令
redis-cli -h 127.0.0.1 -p 6379 hget key0 field0

client list
client kill ip:port

#查特定pattern的key 数量
redis-cli keys *xxx* |grep "" -c

批量删除Redis下特定pattern的keys
可以使用linux的xargs来做到如：
*/redis-cli keys "prefix*" | xargs */redis-cli del 

如果是访问特定的数据库，则可以：
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

```bash创建集群主节点

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
说明：为一个指定集群添加节点，需要先连到该集群的任意一个节点IP（192.168.163.132:6379），再把新节点加入。该2个参数的顺序有要求：新加入的节点放前
# 添加集群从节点

redis-cli --cluster add-node 192.168.163.132:6382 192.168.163.132:6379 --cluster-slave --cluster-master-id 117457eab5071954faab5e81c3170600d5192270
说明：把6382节点加入到6379节点的集群中，并且当做node_id为 117457eab5071954faab5e81c3170600d5192270 的从节点。如果不指定 --cluster-master-id 会随机分配到任意一个主节点。

删除节点

redis-cli --cluster del-node 192.168.163.132:6384 f6a6957421b80409106cb36be3c7ba41f3b603ff
说明：指定IP、端口和node_id 来删除一个节点，从节点可以直接删除，主节点不能直接删除，删除之后，该节点会被shutdown。

```

http://blog.csdn.net/rockstar541/article/details/30245493
  
https://www.zhihu.com/question/20698365
  
https://www.cnblogs.com/zhoujinyi/p/11606935.html
  
https://blog.51cto.com/zengestudy/1853801