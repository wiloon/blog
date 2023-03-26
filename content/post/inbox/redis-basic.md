---
title: redis basic
author: "-"
date: "2021-05-07 14:38:02"
url: "redis"
categories:
  - redis
tags:
  - inbox
---
## redis basic

### commands

```bash
redis-cli -h 127.0.0.1 -p 6379
# -a 使用认证密码登录
redis-cli -h 127.0.0.1 -p 6379 -a password0
# OBJECT ENCODING 命令可以查看一个数据库键的值对象的编码
OBJECT ENCODING key0

# 分析 redis key 大小
debug object key0
# Value at:0x7f6bffc22a00 refcount:1 encoding:raw serializedlength:7164 lru:12841785 lru_seconds_idle:95
```

#### 延迟时间

```bash
redis-cli --latency -h 192.168.50.100 -p 6379
```

### sort

<https://segmentfault.com/a/1190000002806846>

基本使用
命令格式:  SORT key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC|DESC] [ALPHA] [STORE destination]

默认情况下，排序是基于数字的，各个元素将会被转化成双精度浮点数来进行大小比较，这是SORT命令最简单的形式，也就是下面这种形式:

SORT mylist

如果mylist是一个包含了数字元素的列表，那么上面的命令将会返回升序排列的一个列表。如果想要降序排序，要使用DESC描述符，如下所示:

SORT mylist DESC

如果mylist包含的元素是string类型的，想要按字典顺序排列这个列表，那么就要用到ALPHA描述符，如下所示:

#### watchdog

```bash
CONFIG SET watchdog-period 500
```

用户通过命令 CONFIG SET 开启软件看门狗

Redis 启动监测程序监测自己的状态

如果 Redis 检测到服务器被某些操作阻塞了，并运行速度不够快，也许是因为延迟导致的，Redis 就会在 log 文件中写入一份关于被阻塞服务器的底层监测数据报表

用户通过 Redis Google Group 发送消息给开发人员，消息包括看门狗报表。
时间间隔以毫秒为单位。在上面的例子中，我指定了，当服务器检测到 500 毫秒或更大的延迟的时候，才记录延迟事件。最小的时间间隔是 200 毫秒。

### DEBUG SEGFAULT

Redis Debug Segfault 命令执行一个非法的内存访问从而让 Redis 崩溃，仅在开发时用于 BUG 调试。制造一次服务器当机。

```bash
redis 127.0.0.1:6379> DEBUG SEGFAULT 
redis-cli -p 7002 debug segfault
```

### java sdk

- redisson
- jedis

### 查看版本等信息

```bash
info
```

### version

```o
current: 5.0.5
latest: 6.2
```

### URLs

```o
https://redis.io/
https://github.com/redis/redis
```

## install

### centos

```bash
sudo yum install epel-release
sudo yum install snapd
sudo systemctl enable --now snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
sudo snap install redis
```

### ubuntu

```bash
sudo apt install redis
```

### rpm

download redis rpm from <https://pkgs.org/download/redis>

<https://rpms.remirepo.net/enterprise/7/remi/x86_64/redis-7.0.0-1.el7.remi.x86_64.rpm>

下载Redis的依赖包: libjemalloc

下载地址: <https://pkgs.org/centos-6/atomic-x86_64/jemalloc-3.6.0-1.el6.art.x86_64.rpm.html>

```bash
rpm -ivh jemalloc-3.6.0-1.el6.art.x86_64.rpm
rpm -ivh redis-2.8.20-3.el6.art.x86_64.rpm
```

### podman, 单机 redis

```bash
# default config
podman run \
-d \
--name redis \
-p 6379:6379 \
-v /etc/localtime:/etc/localtime:ro \
redis:7.0.9

# client
podman run -it --rm redis redis-cli -h redis.wiloon.com

# customized config file and data volume
podman run \
-d \
--name redis \
-p 6379:6379 \
-v /etc/localtime:/etc/localtime:ro \
-v redis-conf:/etc/redis \
-v redis-data:/data/redis \
redis:6.2.6 redis-server /etc/redis/redis.conf
```

```bash
redis-server --version
```

### list all keys

```bash
keys *
```

### delete key

del key1 key2

### unlink

```bash
    unlink key [key ...]
```

### 判断 key 是否存在

exists key_name

### 查看 key 的类型

```bash
type key0
```

### 删除 key

```bash
    DEL key [key ...]
```

### 设置过期时间

EXPIRE key0 10

### ttl: 返回给定 key 的剩余生存时间(TTL, time to live)

```bash
    TTL key
```

### 查看各个库的key数量

```bash
    info keyspace
```

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

### unlink 命令

```bash
    unlink key [key ...]
```

该命令和 DEL 十分相似: 删除指定的key(s), 若key不存在则该 key 被跳过。但是，相比DEL会产生阻塞，该命令会在另一个线程中回收内存，因此它是非阻塞的。 这也是该命令名字的由来: 仅将keys从keyspace元数据中删除，真正的删除会在后续异步操作。

释放 key 代价计算函数 lazyfreeGetFreeEffort()，集合类型键，且满足对应编码，cost就是集合键的元数个数，否则cost就是1.
    List: 4.0只有一种编码，quicklist，所以编码无限制，直接返回element个数。
    Set: 非hash table编码，即intset编码时返回1.当一个集合只包含整数值元素， 并且这个集合的元素数量不多时， Redis 就会使用intset作为集合键的底层实现。
    Hash: 同上。
        当hash键值满足下面任意条件编码为hash table:
    ->element count > "hash-max-ziplist-entries",default 512. ->value length > "hash-max-ziplist-value",default 64
    Zset: 非skiplist编码，返回1.
       当zset键值满足下面任意条件编码为hash table:
    ->element count >"zset-max-ziplist-entries"，default 128 ->value length > "zset-max-ziplist-value", default 64
     举例:  1 一个包含100元素的list key, 它的free cost就是100 2 一个512MB的string key, 它的free cost是

总结:
    不管是del还是unlink，key都是同步删除的。
    使用unlink命令时，如果value分配的空间不大，使用异步删除反而会降低效率，所以redis会先评估一下free value的effort，根据 effort 的值来决定是否做异步删除。
    使用unlink命令时，由于string类型的effort一直返回的是1，z所以string类型不会做异步删除。

作者: willcat
链接: <https://juejin.cn/post/6844903810792423432>
来源: 掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

### FLUSHALL

可用版本:  >= 1.0.0
时间复杂度:  O(N)
清空整个 Redis 服务器的数据(删除所有数据库的所有 key )。

### FLUSHALL [ASYNC]

(Redis 4.0.0 or greater)  
删除 所有DB 中的 所有数据, 默认是同步操作，选项 ASYNC 表示异步，即清空操作在一个新的线程中进行，不会阻塞主线程。

Redis is now able to delete keys in the background in a different thread without blocking the server. An ASYNC option was added to FLUSHALL and FLUSHDB in order to let the entire dataset or a single database to be freed asynchronously.

```bash
redis-cli -h 127.0.0.1 -p 6379 FLUSHALL ASYNC
```

### FLUSHDB [ASYNC]

表示删除 当前DB 中的 所有数据 。默认是同步操作，和 FLUSHall 一样，支持选项ASYNC ，表示异步。要删除指定DB中的所有数据，可以使用 SELECT 命令先选中DB，然后使用 FLUSHDB 命令清空数据

```bash
redis-cli -h 127.0.0.1 -p 6379 SELECT 0
redis-cli -h 127.0.0.1 -p 6379 FLUSHDB
```

### module

```bash
     https://redis.io/modules
```

#### 下载编译好的 redis module

```bash
     https://app.redislabs.com/
```

#### redis.conf 中使用 模块有两种加载方式，一是在配置文件 redis.conf 中使用

```bash
    loadmodule /path/to/mymodule.so 在 Redis 启动时加载。
```

#### load a module at runtime

```bash
    module load /data/redis/redisbloom.so
```

#### list modules

```bash
    module list
```

### 卸载

   MODULE UNLOAD bf

### RedisBloom

```bash
    https://oss.redislabs.com/redisbloom/

    podman run -d -p 6379:6379 --name redis-redisbloom redislabs/rebloom:latest
    BF.ADD newFilter foo
    BF.EXISTS newFilter foo
    BF.EXISTS newFilter bar
    BF.MADD myFilter foo bar baz
    BF.MEXISTS myFilter foo nonexist bar
```

---

<https://github.com/redis/redis>

### Redis 响应延时问题排查

<https://xie.infoq.cn/article/1ccbd30d94ab781a4f85ab2fc?utm_source=rss&utm_medium=article>

### RESP协议

什么是 RESP？
是基于TCP的应用层协议 RESP(REdis Serialization Protocol)；
RESP底层采用的是TCP的连接方式，通过tcp进行数据传输，然后根据解析规则解析相应信息,

Redis 的客户端和服务端之间采取了一种独立名为 RESP(REdis Serialization Protocol) 的协议，作者主要考虑了以下几个点:

容易实现

解析快

人类可读
RESP可以序列化不同的数据类型，如整数，字符串，数组。还有一种特定的错误类型。请求从客户端发送到Redis服务器，作为表示要执行的命令的参数的字符串数组。Redis使用特定于命令的数据类型进行回复。
RESP是二进制安全的，不需要处理从一个进程传输到另一个进程的批量数据，因为它使用前缀长度来传输批量数据。
注意: RESP 虽然是为 Redis 设计的，但是同样也可以用于其他 C/S 的软件。Redis Cluster使用不同的二进制协议(gossip)，以便在节点之间交换消息。

关于协议的具体描述，官方文档 <https://redis.io/topics/protocol>

### pipeline

可以将多次IO往返的时间缩减为一次，前提是pipeline执行的指令之间没有因果相关性。

## redis 切换 db

```bash
select 10
```

<https://mp.weixin.qq.com/s/MtvEf_jWWDb6yCXPqvqF0w>

<https://mp.weixin.qq.com/s/aOiadiWG2nNaZowmoDQPMQ>

<https://blog.csdn.net/AlbertFly/article/details/80169717>

## k8s redis

### redis-config.yaml

```yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: redis-config
  namespace: default
  labels:
    app: redis
data:
  redis.conf: |-
    dir /data
    port 6379
    bind 0.0.0.0
    appendonly yes
    protected-mode no
    pidfile /data/redis.pid

```

```bash
kubectl apply -f redis-config.yaml
```

### redis-deployment.yml

```yaml
## Service
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: default
  labels:
    app: redis
spec:
  type: NodePort
  ports:
  - name: redis
    port: 6379
    nodePort: 30379
    targetPort: 6379
  selector:
    app: redis
---
## Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: default
  labels:
    app: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      initContainers:
        - name: system-init 
          image: busybox:1.32
          imagePullPolicy: IfNotPresent
          command: 
            - "sh"
            - "-c"
            - "echo 2000 > /proc/sys/net/core/somaxconn && echo never > /sys/kernel/mm/transparent_hugepage/enabled"
          securityContext:
            privileged: true
            runAsUser: 0
          volumeMounts:
            - name: sys
              mountPath: /sys
      containers:
        - name: redis
          image: redis:5.0.8
          command: 
            - "sh"
            - "-c"
            - "redis-server /usr/local/etc/redis/redis.conf"
          ports:
            - containerPort: 6379
          resources:
          limits:
              cpu: 1000m
              memory: 300Mi
          requests:
              cpu: 1000m
              memory: 200Mi
          livenessProbe:
          tcpSocket:
              port: 6379
          initialDelaySeconds: 300
          timeoutSeconds: 1
          periodSeconds: 10
          successThreshold: 1
          failureThreshold: 3
          readinessProbe:
          tcpSocket:
              port: 6379
          initialDelaySeconds: 5
          timeoutSeconds: 1
          periodSeconds: 10
          successThreshold: 1
          failureThreshold: 3
          volumeMounts:
          - name: data
          mountPath: /data
          - name: config
          mountPath:  /usr/local/etc/redis/redis.conf
          subPath: redis.conf
      volumes:
        - name: data
            persistentVolumeClaim:
            claimName: pvc0
        - name: config      
            configMap:
            name: redis-config
        - name: sys
            hostPath: 
            path: /sys
```

```bash
kubectl create -f redis-deployment.yml
```
