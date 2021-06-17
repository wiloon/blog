---
title: redis config
author: w1100n
type: post
date: 2019-02-22T11:26:25+00:00
url: /?p=13678

---

https://raw.githubusercontent.com/redis/redis/6.0/redis.conf

```bash
bind 0.0.0.0
#参数是为了禁止外网访问redis，如果启用了，则只能够通过lookback ip（127.0.0.1）访问Redis
protected-mode no
port 6379
#tcp-backlog, 此参数确定了TCP连接中已完成队列(完成三次握手之后)的长度，当然此值必须不大于Linux系统定义的/proc/sys/net/core/somaxconn值，默认是511，而Linux的默认参数值是128。当系统并发量大并且客户端速度缓慢的时候，可以将这二个参数一起参考设定,了解了下tcp的三次握手进行中的一些queue的知识. 参考下图我们可以看到在server接收到syn的时候会进入到一个syn queue队列, 当server端最终收到ack时转换到accept queue队列. 上面终端显示在listen状态下的连接, 其Send-Q就是这个accept queue队列的最大值. 只有server端执行了accept后才会从这个队列中移除这个连接. 这个值的大小是受somaxconn影响的, 因为是取的它们两者的最小值, 所以如果要调大的话必需修改内核的somaxconn值.建议修改为 2048
tcp-backlog 511

# 设置客户端连接时的超时时间，单位为秒。当客户端在这段时间内没有发出任何指令，那么关闭该连接
# 0是关闭此设置
timeout
#tcp keepalive参数。如果设置不为0，就使用配置tcp的SO_KEEPALIVE值，使用keepalive有两个好处:检测挂掉的对端。降低中间设备出问题而导致网络看似连接却已经与对端端口的问题。在Linux内核中，设置了keepalive，redis会定时给对端发送ack。检测到对端关闭需要两倍的设置值。
tcp-keepalive 0

#是否守护线程
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
# notice (moderately verbose, what you want in production probably)
# warning (only very important / critical messages are logged)
loglevel notice

# Set the number of databases. The default database is DB 0, you can select
# a different one on a per-connection basis using SELECT <dbid> where
# dbid is a number between 0 and 'databases'-1
# 
# 设置数据库数量。默认会使用 0 数据库，也可以使用  SELECT <dbid> 指令为每个连接选择不同的数据库，
# 其中 dbid 的取值在 0 和 （'databases' 设置值）-1 之间
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
#   900秒（15分钟）内至少1个key值改变（则进行数据库保存--持久化）  
#   300秒（5分钟）内至少10个key值改变（则进行数据库保存--持久化）  
#   60秒（1分钟）内至少10000个key值改变（则进行数据库保存--持久化）  
#  
#   注释: 注释掉"save"这一行配置项就可以让保存数据库功能失效。  
#  
#   你也可以通过增加一个只有一个空字符串的配置项（如下面的实例）来去掉前面的"save"配置。  
#  
#   save ""  

save 900 1  
save 300 10  
save 60 10000 

# 配置redis 数据文件的目录, 配置了dir之后, node.conf, rdb, aof文件都 会保存到这个目录 下.
dir
# 缺省情况下，如果 RDB 快照被启用（至少有一个存储点）时，若后台保存快照失败，Redis 将拒绝接受写入。
# 这将会促使用户发现（以一种强硬的方式）数据持久化到磁盘出问题了，否则，很有可能没人会注意到这一点，最终带来灾难性的后果。
stop-writes-on-bgsave-error yes

# 当导出 .rdb 数据库时，是否对字符串对象采用 LZF 进行压缩。
# 由于进行压缩在多数情况下效果都比较好，所以，该配置的缺省值为 'yes' 。
# 如果你想要节省点 CPU ，可以将其改为  'no' ，相应地，如果你的数据集里面包含较多可压缩的键或值时，保存的数据集很有可能会比较大。
rdbcompression yes

# 从 RDB 5 版开始，CRC64 和校验被添加到了 .rdb 文件的末尾。
# 这样做可以使 .rdb 文件变得更加不容易损坏，但相应地，在文件保存和加载的时候也会消耗更多服务器性能（大概10%）。
# 所以，如果你想要追求最佳的服务器性能，你可以将它关闭掉。
#
# RDB files created with checksum disabled have a checksum of zero that will
# tell the loading code to skip the check.
rdbchecksum yes

# The filename where to dump the DB
# 导出的 .rdb 文件名称
dbfilename dump.rdb

# 当一个从节点与主节点失去连接时，或者当复制还在进行时，从节点可以有以下两种表现方式: 
#
# 1) 当 slave-serve-stale-data 被设置为 'yes' (默认值) ，从节点将仍然能够回复客户端的请求，
#    但有可能回复的是过期的数据，亦或者如果这是第一次数据同步的话将只会返回空值。
#
# 2) 当 slave-serve-stale-data 被设置为 'no' ，从节点对于除 INFO 和 SLAVEOF 之外的所有请求命令，
#    都将返回一个 "SYNC with master in progress" 错误。
#
slave-serve-stale-data yes

slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5

# 当 repl-disable-tcp-nodelay 被设置为 "yes" ，Redis 将使用更小的 TCP 包和更少的带宽向从节点发送数据。
# 但是这样做会使得数据在从节点中的出现增加一定延迟时间，在 Linux 内核缺省配置下延迟可达 40 毫秒。
#
# If you select "no" the delay for data to appear on the slave side will
# be reduced but more bandwidth will be used for replication.
#
# By default we optimize for low latency, but in very high traffic conditions
# or when the master and slaves are many hops away, turning this to "yes" may
# be a good idea.
repl-disable-tcp-nodelay no

# 优先级数字越小的从节点会被认为是更应被提拔，
# 所以如果有三个优先级数字分别为 10 、100、25的从节点的话，将会选择提拔优先级数字为 10 的从节点，
# 将会选择提拔优先级数字为 10 的从节点。
#
# However a special priority of 0 marks the slave as not able to perform the
# role of master, so a slave with priority of 0 will never be selected by
# Redis Sentinel for promotion.
#
# By default the priority is 100.
slave-priority 100

appendonly no
appendfilename "xxx.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000

cluster-enabled yes
cluster-config-file cluster.conf
cluster-node-timeout 15000
cluster-slave-validity-factor 10
cluster-migration-barrier 1
cluster-require-full-coverage no

slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""

hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
```

---

https://blog.csdn.net/pengjunlee/article/details/81269596