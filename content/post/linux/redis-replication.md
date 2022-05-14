---
author: "-"
date: "2021-06-18 18:00:23" 
title: "Redis Replication, sentinel"
categories:
  - inbox
tags:
  - reprint
---
## "Redis Replication, sentinel"

Redis 主从 Replication 的配置

beanlam
发布于 2015-04-20
本专栏与Redis相关的文章

Redis Sentinel机制与用法 (一) 
Redis Sentinel机制与用法 (二) 
Jedis的JedisSentinelPool源代码分析
Jedis的Sharded源代码分析
Redis 主从 Replication 的配置
详解Redis SORT命令
JedisCommand接口说明

本文参考翻译自《Redis Replication documentation》
概述
Redis的replication机制允许slave从master那里通过网络传输拷贝到完整的数据备份。具有以下特点: 

异步复制。从2.8版本开始，slave能不时地从master那里获取到数据。
允许单个master配置多个slave
slave允许其它slave连接到自己。一个slave除了可以连接master外，它还可以连接其它的slave。形成一个图状的架构。
master在进行replication时是非阻塞的，这意味着在replication期间，master依然能够处理客户端的请求。
slave在replication期间也是非阻塞的，也可以接受来自客户端的请求，但是它用的是之前的旧数据。可以通过配置来决定slave是否在进行replication时用旧数据响应客户端的请求，如果配置为否，那么slave将会返回一个错误消息给客户端。不过当新的数据接收完全后，必须将新数据与旧数据替换，即删除旧数据，在替换数据的这个时间窗口内，slave将会拒绝客户端的请求和连接。
一般使用replication来可以实现扩展性，例如说，可以将多个slave配置为“只读”，或者是纯粹的数据冗余备份。
能够通过replication来避免master每次持久化时都将整个数据集持久化到硬盘中。只需把master配置为不进行save操作(把配置文件中save相关的配置项注释掉即可)，然后连接上一个slave，这个slave则被配置为不时地进行save操作的。不过需要注意的是，在这个用例中，必须确保master不会自动启动。更多详情请继续往下读。
Master持久化功能关闭时Replication的安全性
当有需要使用到replication机制时，一般都会强烈建议把master的持久化开关打开。即使为了避免持久化带来的延迟影响，不把持久化开关打开，那么也应该把master配置为不会自动启动的。

为了更好地理解当一个不进行持久化的master如果允许自动启动所带来的危险性。可以看看下面这种失败情形: 

假设我们有一个redis节点A，设置为master，并且关闭持久化功能，另外两个节点B和C是它的slave，并从A复制数据。
如果A节点崩溃了导致所有的数据都丢失了，它会有重启系统来重启进程。但是由于持久化功能被关闭了，所以即使它重启了，它的数据集是空的。
而B和C依然会通过replication机制从A复制数据，所以B和C会从A那里复制到一份空的数据集，并用这份空的数据集将自己本身的非空的数据集替换掉。于是就相当于丢失了所有的数据。
即使使用一些HA工具，比如说sentinel来监控master-slaves集群，也会发生上述的情形，因为master可能崩溃后迅速恢复。速度太快而导致sentinel无法察觉到一个failure的发生。

当数据的安全很重要、持久化开关被关闭并且有replication发生的时候，那么应该禁止实例的自启动。

replication工作原理
如果你为master配置了一个slave，不管这个slave是否是第一次连接上Master，它都会发送一个SYNC命令给master请求复制数据。

master收到SYNC命令后，会在后台进行数据持久化，持久化期间，master会继续接收客户端的请求，它会把这些可能修改数据集的请求缓存在内存中。当持久化进行完毕以后，master会把这份数据集发送给slave，slave会把接收到的数据进行持久化，然后再加载到内存中。然后，master再将之前缓存在内存中的命令发送给slave。

当master与slave之间的连接由于某些原因而断开时，slave能够自动重连Master，如果master收到了多个slave并发连接请求，它只会进行一次持久化，而不是一个连接一次，然后再把这一份持久化的数据发送给多个并发连接的slave。

当master和slave断开重连后，一般都会对整份数据进行复制。但从redis2.8版本开始，支持部分复制。

数据部分复制
从2.8版本开始，slave与master能够在网络连接断开重连后只进行部分数据复制。

master会在其内存中创建一个复制流的等待队列，master和它所有的slave都维护了复制的数据下标和master的进程id，因此，当网络连接断开后，slave会请求master继续进行未完成的复制，从所记录的数据下标开始。如果进程id变化了，或者数据下标不可用，那么将会进行一次全部数据的复制。

支持部分数据复制的命令是PSYNC

不需硬盘参与的Replication
一般情况下，一次复制需要将内存的数据写到硬盘中，再将数据从硬盘读进内存，再发送给slave。

对于速度比较慢的硬盘，这个操作会给master带来性能上的损失。Redis2.8版本开始，实验性地加上了无硬盘复制的功能。这个功能能将数据从内存中直接发送到slave，而不用经过硬盘的存储。

不过这个功能目前处于实验阶段，还未正式发布。
相关配置
与replication相关的配置比较简单，只需要把下面一行加到slave的配置文件中: 

slaveof 192.168.1.1 6379
你只需要把ip地址和端口号改一下。当然，你也可以通过客户端发送SLAVEOF命令给slave。

部分数据复制有一些可调的配置参数，请参考redis.conf文件。

无硬盘复制功能可以通过repl-diskless-sync来配置，另外一个配置项repl-diskless-sync-delay用来配置当收到第一个请求时，等待多个slave一起来请求之间的间隔时间。

只读的slave
从redis2.6版本开始，slave支持只读模式，而且是默认的。可以通过配置项slave-read-only来进行配置，并且支持客户端使用CONFIG SET命令来动态修改配置。

只读的slave会拒绝所有的写请求，只读的slave并不是为了防范不可信的客户端，毕竟一些管理命令例如DEBUG和CONFIG在只读模式下还是可以使用的。如果确实要确保安全性，那么可以在配置文件中将一些命令重新命名。

也许你会感到很奇怪，为什么能够将一个只读模式的slave恢复为可写的呢，尽管可写，但是只要slave一同步master的数据，就会丢失那些写在slave的数据。不过还是有一些合法的应用场景需要存储瞬时数据会用到这个特性。不过，之后可能会考虑废除掉这个特性。

Setting a slave to authenticate to a master

如果master通过requirepass配置项设置了密码，slave每次同步操作都需要验证密码，可以通过在slave的配置文件中添加以下配置项: 

masterauth <password>
也可以通过客户端在运行时发送以下命令: 

config set masterauth <password>
至少N个slave才允许向master写数据
从redis2.8版本开始，master可以被配置为，只有当master当前有至少N个slave连接着的时候才接受写数据的请求。

然而，由于redis是异步复制的，所以它并不能保证slave会受到一个写请求，所以总有一个数据丢失的时间窗口存在。

这个机制的工作原理如下所示: 

slave每秒发送ping心跳给master，询问当前复制了多少数据。
master会记录下它上次收到某个slave的ping心跳是什么时候。
使用者可以配置一个时间，来指定ping心跳的发送不应超过的一个超时时间
如果master有至少N个slave，并且ping心跳的超时不超过M秒，那么它就会接收写请求。

也许你会认为这情形好似CAP理论中弱化版的C(consistency)，因为写请求并不能保证数据的一致性，但这样做，至少数据丢失被限制在了限定的时间内。即M秒。

如果N和M的条件都无法达到，那么master会回复一个错误信息。写请求也不会被处理。

有两个配置项用来配置上文中提到的N和M: 

    min-slaves-to-write <number of slaves>
    min-slaves-max-lag <number of seconds>
如果需要了解更多，请查阅redis.conf配置文件。

---

https://segmentfault.com/a/1190000002692598  

https://segmentfault.com/a/1190000002680804

https://www.cnblogs.com/kevingrace/p/9004460.html