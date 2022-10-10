---
title: redis config
author: "-"
date: 2019-02-22T11:26:25+00:00
url: redis/config
categories:
  - inbox
tags:
  - reprint
---
## redis config

<https://raw.githubusercontent.com/redis/redis/6.0/redis.conf>

```bash
bind 0.0.0.0
# bind 参数是为了禁止外网访问redis,如果启用了,则只能够通过lookback ip (127.0.0.1) 访问Redis

protected-mode no
# protected mode 是 Redis的安全特性, 开启之后 redis 不会响应 loopback interfaces 以外的请求.
port 6379
#tcp-backlog, 此参数确定了TCP连接中已完成队列(完成三次握手之后)的长度, 当然此值必须不大于Linux系统定义的/proc/sys/net/core/somaxconn值,默认是511,而Linux的默认参数值是128。当系统并发量大并且客户端速度缓慢的时候,可以将这二个参数一起参考设定,了解了下tcp的三次握手进行中的一些queue的知识. 参考下图我们可以看到在server接收到syn的时候会进入到一个syn queue队列, 当server端最终收到ack时转换到accept queue队列. 上面终端显示在listen状态下的连接, 其 Send-Q 就是这个 accept queue 队列的最大值. 只有 server 端执行了 accept 后才会从这个队列中移除这个连接. 这个值的大小是受 somaxconn 影响的, 因为是取的它们两者的最小值, 所以如果要调大的话必需修改内核的 somaxconn 值.建议修改为 2048
tcp-backlog 511

# timeout, 设置客户端连接时的超时时间,单位为秒。当客户端在这段时间内没有发出任何指令,那么关闭该连接
# 0 是关闭此设置
timeout 0
#tcp keepalive参数。如果设置不为0, 就使用配置tcp的SO_KEEPALIVE值, 使用keepalive有两个好处: 检测挂掉的对端。降低中间设备出问题而导致网络看似连接却已经与对端断开的问题。在Linux内核中,设置了keepalive, redis会定时给对端发送ack。检测到对端关闭需要两倍的设置值。
tcp-keepalive 0

# 是否守护线程
daemonize yes

# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd

pidfile /path/to/redis.pid

# Specify the server verbosity level.
# This can be one of:
# debug (a lot of information, useful for development/testing)
# verbose (many rarely useful info, but not a mess like the debug level)
# notice (moderately verbose, what you want in production probably), 适用于生产环境
# warning (only very important / critical messages are logged)
loglevel notice

# Specify the log file name. Also the empty string can be used to force
# Redis to log on the standard output. Note that if you use standard
# output for logging but daemonize, logs will be sent to /dev/null
logfile /var/log/redis/redis.log

# Set the number of databases. The default database is DB 0, you can select
# a different one on a per-connection basis using SELECT <dbid> where
# dbid is a number between 0 and 'databases'-1
# 
# 设置数据库数量。默认会使用 0 数据库, 也可以使用  SELECT <dbid> 指令为每个连接选择不同的数据库,
# 其中 dbid 的取值在 0 和  ('databases' 设置值) -1 之间
# 不同的数据库使用不同的内存空间, 互不影响, 不同的库里可以有相同的key
# 在redis 集群模式, 不支持多库.
databases 16

#   save <seconds> <changes>
#
#   Will save the DB if both the given number of seconds and the given
#   number of write operations against the DB occurred.

# Save the DB on disk:保存数据库到磁盘  
#  
#   save <秒> <更新>  
#  
#   如果指定的秒数和数据库写操作次数都满足了就将数据库保存。  
#  
#   下面是保存操作的实例:   
#   900秒 (15分钟) 内至少1个key值改变 (则进行数据库保存--持久化)   
#   300秒 (5分钟) 内至少10个key值改变 (则进行数据库保存--持久化)   
#   60秒 (1分钟) 内至少10000个key值改变 (则进行数据库保存--持久化)   
#  
#   注释: 注释掉"save"这一行配置项就可以让保存数据库功能失效。  
#  
#   你也可以通过增加一个只有一个空字符串的配置项 (如下面的实例) 来去掉前面的"save"配置。  
#  
#   save ""  
# Snapshotting can be completely disabled with a single empty string argument
# as in following example:

# 关闭 RDB
# save ""

# 开启 RDB
save 900 1  
save 300 10  
save 60 10000 

# 配置redis 数据文件的目录, 配置了dir之后, node.conf, rdb, aof文件都 会保存到这个目录 下.
dir /var/lib/redis

# 缺省情况下,如果 RDB 快照被启用 (至少有一个存储点) 时,若后台保存快照失败,Redis 将拒绝接受写入。
# 这将会促使用户发现 (以一种强硬的方式) 数据持久化到磁盘出问题了,否则,很有可能没人会注意到这一点,最终带来灾难性的后果。
stop-writes-on-bgsave-error yes

# 当导出 .rdb 数据库时,是否对字符串对象采用 LZF 进行压缩。
# 由于进行压缩在多数情况下效果都比较好,所以,该配置的缺省值为 'yes' 。
# 如果你想要节省点 CPU ,可以将其改为  'no' ,相应地,如果你的数据集里面包含较多可压缩的键或值时,保存的数据集很有可能会比较大。
rdbcompression yes

# 从 RDB 5 版开始,CRC64 和校验被添加到了 .rdb 文件的末尾。
# 这样做可以使 .rdb 文件变得更加不容易损坏,但相应地,在文件保存和加载的时候也会消耗更多服务器性能 (大概10%) 。
# 所以,如果你想要追求最佳的服务器性能,你可以将它关闭掉。
#
# RDB files created with checksum disabled have a checksum of zero that will
# tell the loading code to skip the check.
rdbchecksum yes

# The filename where to dump the DB
# 导出的 .rdb 文件名称
dbfilename dump.rdb

# 当一个从节点与主节点失去连接时,或者当复制还在进行时,从节点可以有以下两种表现方式: 
#
# 1) 当 slave-serve-stale-data 被设置为 'yes' (默认值) ,从节点将仍然能够回复客户端的请求,
#    但有可能回复的是过期的数据,亦或者如果这是第一次数据同步的话将只会返回空值。
#
# 2) 当 slave-serve-stale-data 被设置为 'no' ,从节点对于除 INFO 和 SLAVEOF 之外的所有请求命令,
#    都将返回一个 "SYNC with master in progress" 错误。
#
slave-serve-stale-data yes

# slave-read-only 
# 如果为 yes,代表为只读状态,但并不表示客户端用集群方式以从节点为入口连入集群时,不可以进行 set 操作,且 set 操作的数据不会被放在从节点的槽上,会被放到某主节点的槽上
slave-read-only yes
# 无硬盘复制
repl-diskless-sync no
# 无硬盘复制, 配置当收到第一个请求时,等待多个slave一起来请求之间的间隔时间
repl-diskless-sync-delay 5

# 当 repl-disable-tcp-nodelay 被设置为 "yes" ,Redis 将使用更小的 TCP 包和更少的带宽向从节点发送数据。
# 但是这样做会使得数据在从节点中的出现增加一定延迟时间,在 Linux 内核缺省配置下延迟可达 40 毫秒。
#
# If you select "no" the delay for data to appear on the slave side will
# be reduced but more bandwidth will be used for replication.
#
# By default we optimize for low latency, but in very high traffic conditions
# or when the master and slaves are many hops away, turning this to "yes" may
# be a good idea.
repl-disable-tcp-nodelay no 

# 优先级数字越小的从节点会被认为是更应被提拔,
# 所以如果有三个优先级数字分别为 10 、100、25的从节点的话,将会选择提拔优先级数字为 10 的从节点,
# 将会选择提拔优先级数字为 10 的从节点。
#
# However a special priority of 0 marks the slave as not able to perform the
# role of master, so a slave with priority of 0 will never be selected by
# Redis Sentinel for promotion.
#
# By default the priority is 100.

#当master不可用,Sentinel会根据slave的优先级选举一个master。最低的优先级的slave,当选master。而配置成0,永远不会被选举。
slave-priority 100

# 是否开启 AOF
appendonly no
appendfilename "foo.aof"

# appendfsync
# always    将 aof_buf 缓冲区中的所有内容写入并同步到 AOF 文件。
# everysec    将 aof_buf 缓冲区中的所有内容写入到 AOF 文件, 如果上次同步 AOF 文件的时间距离现在超过一秒钟, 那么再次对 AOF 文件进行同步, 并且这个同步操作是由一个线程专门负责执行的。
# no        将 aof_buf 缓冲区中的所有内容写入到 AOF 文件, 但并不对 AOF 文件进行同步, 何时同步由操作系统来决定。
appendfsync everysec
# no-appendfsync-on-rewrite
# no,是最安全的方式,不会丢失数据,但是要忍受阻塞的问题。
# yes, 这就相当于将appendfsync设置为no,这说明并没有执行磁盘操作,只是写入了缓冲区,因此这样并不会造成阻塞 (因为没有竞争磁盘) ,但是如果这个时候redis挂掉,就会丢失数据。丢失多少数据呢？在linux的操作系统的默认设置下,最多会丢失30s的数据。
no-appendfsync-on-rewrite no
# 当AOF文件大小的增长率大于该配置项时自动开启重写 (这里指超过原大小的100%) 。
auto-aof-rewrite-percentage 100
# 当AOF文件大小大于该配置项时自动开启重写
auto-aof-rewrite-min-size 64mb
# 指定当发生AOF文件末尾截断时,加载文件还是报错退出,Redis启动并加载AOF时,可能发现AOF文件的末尾被截断了。如果Redis所在的机器运行崩溃,就可能导致该现象。特别是在不使用 data=ordered 选项挂载ext4文件系统时。 (但是Redis本身崩溃而操作系统正常运行则不会出现该情况) 当发生了末尾截断,Redis可以选择直接报错退出,或者继续执行并恢复尽量多的数据 (默认选项) 。配置项 aof-load-truncated 用于控制此行为。

#yes : 末尾被截断的 AOF 文件将会被加载,并打印日志通知用户。
#no : 服务器将报错并拒绝启动。

#这时用户需要使用redis-check-aof 工具修复AOF文件,再重新启动。

aof-load-truncated yes
# 为了防止某个脚本执行时间过长导致Redis无法提供服务 (比如陷入死循环) ,Redis提供了lua-time-limit参数限制脚本的最长运行时间,默认为5秒钟。当脚本运行时间超过这一限制后,Redis将开始接受其他命令但不会执行 (以确保脚本的原子性,因为此时脚本并没有被终止) ,而是会返回“BUSY”错误。
lua-time-limit 5000
# 开实例的集群模式
cluster-enabled yes
# 设定了保存节点配置文件的路径, 默认值为 nodes.conf 。
cluster-config-file cluster.conf
# 集群节点的超时时限
cluster-node-timeout 15000
# cluster-slave-validity-factor <factor>: 每个从节点都要检查最后与主节点断线时间,判断其是否有资格替换故障的主节点。如果从节点与主节点断线时间超过cluster-node-time*cluster-slave-validity-factor,则当前从节点不具备故障转移资格。
cluster-slave-validity-factor 10
# cluster-migration-barrier <count>: 主节点需要的最小从节点数,只有达到这个数,才会将多余的从节点迁移给其它孤立的主节点使用。
cluster-migration-barrier 1
# 默认情况下当集群中16384个槽,有任何一个没有指派到节点时,整个集群是不可用的。对应在线上,如果某个主节点宕机,而又没有从节点的话,是不允许对外提供服务的。建议将该参数设置为no,避免某个主节点的故障导致其它主节点不可用。
# yes: 默认情况下,其中一台主 (如果没有做slave)  down 机后,集群会显示不可用状态。
# no: 当 cluster-require-full-coverage 配置成 no 的时候,表示当负责一个槽的主库下线且没有相应的从库进行故障恢复时,集群仍然可用。
cluster-require-full-coverage no
# slowlog-log-slower-than, 对执行时间大于多少微秒(microsecond,1秒 = 1,000,000 微秒)的查询进行记录。
slowlog-log-slower-than 10000
# slow log 最多能保存多少条日志, slow log 本身是一个 FIFO 队列, 当队列大小超过 slowlog-max-len 时,最旧的一条日志将被删除,而最新的一条日志加入到 slow log 
slowlog-max-len 128
# 延迟监控, latency monitor, 单位: 毫秒, 需要注意的是:latency-monitor的阈值不能大于slowlog的值, 如果将 latency-monitor-threshold 的值设置为 0,则表示关闭延迟监控。
latency-monitor-threshold 0
# KEA: 开启所有的事件, KA: 开启keyspace Events, Kl: 开启keyspace 所有List 操作的 Events
notify-keyspace-events ""
# 当哈希表的项不超过 hash-max-ziplist-entries,并且每一项的长度不超过 hash-max-ziplist-value 使用 ziplist 保存数据。
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
# list-max-ziplist-size 就是用于配置 quicklist 中的每个节点的 ziplist 的大小,  list-max-ziplist-size 为负数时表示限制每个 ziplist 的大小, -2: 最大 8 kb <--- 不错, 默认值为 -2,也是官方最推荐的值
list-max-ziplist-size -2
#  list-compress-depth 选项用于控制 quicklist 中压缩的节点的深度, 0 表示不对节点进行压缩,这是默认的值
list-compress-depth 0
# 当 Redis 的集合类型保存的数据均为数字,并且元素个数不超过 set-max-intset-entries 的时候。 Redis 将使用特殊的 intset 结构来保存这个集合。
set-max-intset-entries 512
# 类似哈希表和列表,当排序集合的元素个数不超过 zset-max-ziplist-entries 并且每个元素的长度不超过 zset-max-ziplist-value 时,Redis 将使用 ziplist 保存这个排序集合。
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
# HyperLogLog 稀疏模式的字节限制,包括了 16 字节的头,默认值为 3000。 当超出这个限制后 HyperLogLog 将有稀疏模式转为稠密模式。将这个值设置为超过 16000 是没必要的,因为这时使用稠密模式更省空间。
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10

```

### activerehashing yes

默认值为 yes。

当启用这个功能后,Redis 对哈希表的 rehash 操作会在每 100 毫秒 CPU 时间中的 1 毫秒进行。 Redis 的哈希表实现的 rehash 策略是一个惰性策略: 就是说你对这个哈希表进行越多操作,你将有更多的 rehash 机会, 若你的服务器处于空闲状态则不会有机会完成 rehash 操作,这时哈希表会占用更多内存。

默认情况下会在每一秒中用 10 毫秒来对主哈希表进行 rehash。

如果在你的环境中需要有严格的延迟要求,则需要使用将 activerehashing 配置为 no,比如说需要在 2 毫秒内相应查询操作。 否则你应该将这个选项设置诶 yes,这样可以更及时地释放空闲的内存。

### client-output-buffer-limit normal 0 0 0

### client-output-buffer-limit replica 256mb 64mb 60

### client-output-buffer-limit pubsub 32mb 8mb 60

客户端输出缓冲区限制可用于强制断开从服务器读取数据的速度不够快的客户端 (一个常见的原因是 Pub/Sub 客户端处理发布者的消息不够快)。

可以为每种客户端设置不同的限制:

normal -> 普通客户端,包括 MONITOR 客户端
replica -> 复制客户端
pubsub -> 订阅了至少一个频道的客户端
client-output-buffer-limit 选项的语法为:

```bash
client-output-buffer-limit <class> <hard limit> <soft limit> <soft seconds>
```

当一个客户端到达 hard limit 后会马上被断开,或者在到达 soft limit 并持续 soft seconds 秒后会被断开。

默认情况下,普通客户端不会有限制,因为除非主动请求否则他们不会收到信息, 只有异步的客户端才可能发生发送请求的速度比读取响应的速度快的情况。

默认情况下 pubsub 和 replica 客户端会有默认的限制,因为这些客户端是以 Redis 服务端 push 的方式接收数据的。

soft limit 或者 hard limit 都可以设置为 0,这表示不启用此限制。

### hz

默认值是 10,范围是 1 到 500,超过 100 一般都不是一个好主意。 Redis 会通过调用内部函数来完成很多后台任务,比如关闭超时的客户端的连接,清除过期的 key,等等。

Redis 通过 hz 设置的值来决定执行这些任务的频繁程度。

hz 的默认值是 10,可以通过提高这个值来使得 CPU 在空闲的时候使用更多的 CPU 时间来处理后台任务。 但同时这会使得当有很多 key 在同一时间过期时,过期处理会更精确。

很多客户只有在一些需要很低延迟的环境中才会将这个值从 10 提升到 100。

### aof-rewrite-incremental-fsync yes

当子进程进行 AOF 的重写时, 如果启用了 aof-rewrite-incremental-fsync, 子进程会每生成 32 MB 数据就进行一次 fsync 操作。 通过这种方式将数据分批提交到硬盘可以避免高延迟峰值。

### vm-enabled yes

开启VM, 虚拟内存

---

<https://blog.csdn.net/pengjunlee/article/details/81269596>

<https://juejin.cn/post/6858901608361787400>

<http://cs-cjl.com/2019/04_11_redis_configuration_5>

masterauth passwd123  指定密码passwd123
requirepass passwd123 指定密码passwd123
