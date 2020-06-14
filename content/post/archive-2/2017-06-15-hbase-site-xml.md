---
title: hbase config
author: wiloon
type: post
date: 2017-06-15T01:36:28+00:00
url: /?p=10537
categories:
  - Uncategorized

---
hbase.rootdir
  
这个目录是region server的共享目录，用来持久化HBase。URL需要是&#8217;完全正确&#8217;的，还要包含文件系统的scheme。例如，要表示hdfs中的&#8217;/hbase&#8217;目录，namenode 运行在namenode.example.org的9090端口。则需要设置为hdfs://namenode.example.org:9000/hbase。默认情况下HBase是写到/tmp的。不改这个配置，数据会在重启的时候丢失。
  
默认: file:///tmp/hbase-${user.name}/hbase
  
hbase.master.port
  
HBase的Master的端口.
  
默认: 60000
  
hbase.cluster.distributed
  
HBase的运行模式。false是单机模式，true是分布式模式。若为false,HBase和Zookeeper会运行在同一个JVM里面。
  
默认: false
  
hbase.tmp.dir
  
本地文件系统的临时文件夹。可以修改到一个更为持久的目录上。(/tmp会在重启时清楚)
  
默认:${Java.io.tmpdir}/hbase-${user.name}
  
hbase.local.dir
  
作为本地存储，位于本地文件系统的路径。
  
默认: ${hbase.tmp.dir}/local/
  
hbase.master.info.port
  
HBase Master web 界面端口. 设置为-1 意味着你不想让他运行。
  
0.98 版本以后默认: 16010 以前是 60010
  
hbase.master.info.bindAddress
  
HBase Master web 界面绑定的端口
  
默认: 0.0.0.0
  
hbase.client.write.buffer
  
HTable客户端的写缓冲的默认大小。这个值越大，需要消耗的内存越大。因为缓冲在客户端和服务端都有实例，所以需要消耗客户端和服务端两个地方的内存。得到的好处是，可以减少RPC的次数。可以这样估算服务器端被占用的内存： hbase.client.write.buffer * hbase.regionserver.handler.count
  
默认: 2097152
  
hbase.regionserver.port
  
HBase RegionServer绑定的端口
  
0.98 以前默认: 60020 以后默认是：16020
  
hbase.regionserver.info.port
  
HBase RegionServer web 界面绑定的端口 设置为 -1 意味这你不想与运行 RegionServer 界面.
  
0.98 以前默认: 60030 以后默认是：16030
  
hbase.regionserver.info.port.auto
  
Master或RegionServer是否要动态搜一个可以用的端口来绑定界面。当hbase.regionserver.info.port已经被占用的时候，可以搜一个空闲的端口绑定。这个功能在测试的时候很有用。默认关闭。
  
默认: false
  
hbase.regionserver.info.bindAddress
  
HBase RegionServer web 界面的IP地址
  
默认: 0.0.0.0
  
hbase.regionserver.class
  
RegionServer 使用的接口。客户端打开代理来连接region server的时候会使用到。
  
默认: org.apache.Hadoop.hbase.ipc.HRegionInterface
  
hbase.client.pause
  
通常的客户端暂停时间。最多的用法是客户端在重试前的等待时间。比如失败的get操作和region查询操作等都很可能用到。
  
默认: 1000
  
hbase.client.retries.number
  
最大重试次数。所有需重试操作的最大值。例如从root region服务器获取root region，Get单元值，行Update操作等等。这是最大重试错误的值。 Default: 10.
  
0.98 以前默认: 10 以后默认是：35
  
hbase.bulkload.retries.number
  
最大重试次数。 原子批加载尝试的迭代最大次数。 0 永不放弃。默认: 0.
  
默认: 0

hbase.client.scanner.caching
  
当调用Scanner的next方法，而值又不在缓存里的时候，从服务端一次获取的行数。越大的值意味着Scanner会快一些，但是会占用更多的内存。当缓冲被占满的时候，next方法调用会越来越慢。慢到一定程度，可能会导致超时。例如超过了hbase.regionserver.lease.period。
  
默认: 100
  
hbase.client.keyvalue.maxsize
  
一个KeyValue实例的最大size.这个是用来设置存储文件中的单个entry的大小上界。因为一个KeyValue是不能分割的，所以可以避免因为数据过大导致region不可分割。明智的做法是把它设为可以被最大region size整除的数。如果设置为0或者更小，就会禁用这个检查。默认10MB。
  
默认: 10485760
  
hbase.regionserver.lease.period
  
客户端租用HRegion server 期限，即超时阀值。单位是毫秒。默认情况下，客户端必须在这个时间内发一条信息，否则视为死掉。
  
默认: 60000
  
hbase.regionserver.handler.count
  
RegionServers受理的RPC Server实例数量。对于Master来说，这个属性是Master受理的handler数量
  
默认: 10
  
hbase.regionserver.msginterval
  
RegionServer 发消息给 Master 时间间隔，单位是毫秒
  
默认: 3000
  
hbase.regionserver.optionallogflushinterval
  
将Hlog同步到HDFS的间隔。如果Hlog没有积累到一定的数量，到了时间，也会触发同步。默认是1秒，单位毫秒。
  
默认: 1000
  
hbase.regionserver.regionSplitLimit
  
region的数量到了这个值后就不会在分裂了。这不是一个region数量的硬性限制。但是起到了一定指导性的作用，到了这个值就该停止分裂了。默认是MAX_INT.就是说不阻止分裂。
  
默认: 2147483647
  
hbase.regionserver.logroll.period
  
提交commit log的间隔，不管有没有写足够的值。
  
默认: 3600000
  
hbase.regionserver.hlog.reader.impl
  
HLog file reader 的实现.
  
默认: org.apache.hadoop.hbase.regionserver.wal.SequenceFileLogReader
  
hbase.regionserver.hlog.writer.impl
  
HLog file writer 的实现.
  
默认: org.apache.hadoop.hbase.regionserver.wal.SequenceFileLogWriter

hbase.regionserver.nbreservationblocks
  
储备的内存block的数量(译者注:就像石油储备一样)。当发生out of memory 异常的时候，我们可以用这些内存在RegionServer停止之前做清理操作。
  
默认: 4
  
hbase.zookeeper.dns.interface
  
当使用DNS的时候，Zookeeper用来上报的IP地址的网络接口名字。
  
默认: default
  
hbase.zookeeper.dns.nameserver
  
当使用DNS的时候，Zookeepr使用的DNS的域名或者IP 地址，Zookeeper用它来确定和master用来进行通讯的域名.
  
默认: default
  
hbase.regionserver.dns.interface
  
当使用DNS的时候，RegionServer用来上报的IP地址的网络接口名字。
  
默认: default
  
hbase.regionserver.dns.nameserver
  
当使用DNS的时候，RegionServer使用的DNS的域名或者IP 地址，RegionServer用它来确定和master用来进行通讯的域名.
  
默认: default
  
hbase.master.dns.interface
  
当使用DNS的时候，Master用来上报的IP地址的网络接口名字。
  
默认: default
  
hbase.master.dns.nameserver
  
当使用DNS的时候，RegionServer使用的DNS的域名或者IP 地址，Master用它来确定用来进行通讯的域名.
  
默认: default
  
hbase.balancer.period
  
Master执行region balancer的间隔。
  
默认: 300000
  
hbase.regions.slop
  
当任一区域服务器有average + (average * slop)个分区，将会执行重新均衡。默认 20% slop .
  
默认:0.2
  
hbase.master.logcleaner.ttl
  
Hlog存在于.oldlogdir 文件夹的最长时间, 超过了就会被 Master 的线程清理掉.
  
默认: 600000
  
hbase.master.logcleaner.plugins
  
LogsCleaner服务会执行的一组LogCleanerDelegat。值用逗号间隔的文本表示。这些WAL/HLog cleaners会按顺序调用。可以把先调用的放在前面。你可以实现自己的LogCleanerDelegat，加到Classpath下，然后在这里写下类的全称。一般都是加在默认值的前面。
  
默认: org.apache.hadoop.hbase.master.TimeToLiveLogCleaner
  
hbase.regionserver.global.memstore.upperLimit
  
单个region server的全部memtores的最大值。超过这个值，一个新的update操作会被挂起，强制执行flush操作。
  
默认: 0.4
  
hbase.regionserver.global.memstore.lowerLimit
  
当强制执行flush操作的时候，当低于这个值的时候，flush会停止。默认是堆大小的 35% . 如果这个值和 hbase.regionserver.global.memstore.upperLimit 相同就意味着当update操作因为内存限制被挂起时，会尽量少的执行flush(译者注:一旦执行flush，值就会比下限要低，不再执行)
  
默认: 0.35
  
hbase.server.thread.wakefrequency
  
service工作的sleep间隔，单位毫秒。 可以作为service线程的sleep间隔，比如log roller.
  
默认: 10000
  
hbase.server.versionfile.writeattempts
  
退出前尝试写版本文件的次数。每次尝试由 hbase.server.thread.wakefrequency 毫秒数间隔。
  
默认: 3

hbase.hregion.memstore.flush.size
  
当memstore的大小超过这个值的时候，会flush到磁盘。这个值被一个线程每隔hbase.server.thread.wakefrequency检查一下。
  
默认:134217728
  
hbase.hregion.preclose.flush.size
  
当一个region中的memstore的大小大于这个值的时候，我们又触发了close.会先运行“pre-flush”操作，清理这个需要关闭的memstore，然后将这个region下线。当一个region下线了，我们无法再进行任何写操作。如果一个memstore很大的时候，flush操作会消耗很多时间。&#8221;pre-flush&#8221;操作意味着在region下线之前，会先把memstore清空。这样在最终执行close操作的时候，flush操作会很快。
  
默认: 5242880
  
hbase.hregion.memstore.block.multiplier
  
如果memstore有hbase.hregion.memstore.block.multiplier倍数的hbase.hregion.flush.size的大小，就会阻塞update操作。这是为了预防在update高峰期会导致的失控。如果不设上界，flush的时候会花很长的时间来合并或者分割，最坏的情况就是引发out of memory异常。(译者注:内存操作的速度和磁盘不匹配，需要等一等。原文似乎有误)
  
默认: 2
  
hbase.hregion.memstore.mslab.enabled
  
体验特性：启用memStore分配本地缓冲区。这个特性是为了防止在大量写负载的时候堆的碎片过多。这可以减少GC操作的频率。(GC有可能会Stop the world)(译者注：实现的原理相当于预分配内存，而不是每一个值都要从堆里分配)
  
默认: true
  
hbase.hregion.max.filesize
  
最大HStoreFile大小。若某个列族的HStoreFile增长达到这个值，这个Hegion会被切割成两个。 默认: 10G.
  
默认:10737418240
  
hbase.hstore.compactionThreshold
  
当一个HStore含有多于这个值的HStoreFiles(每一个memstore flush产生一个HStoreFile)的时候，会执行一个合并操作，把这HStoreFiles写成一个。这个值越大，需要合并的时间就越长。
  
默认: 3
  
hbase.hstore.blockingStoreFiles
  
当一个HStore含有多于这个值的HStoreFiles(每一个memstore flush产生一个HStoreFile)的时候，会执行一个合并操作，update会阻塞直到合并完成，直到超过了hbase.hstore.blockingWaitTime的值
  
默认: 7
  
hbase.hstore.blockingWaitTime
  
hbase.hstore.blockingStoreFiles所限制的StoreFile数量会导致update阻塞，这个时间是来限制阻塞时间的。当超过了这个时间，HRegion会停止阻塞update操作，不过合并还有没有完成。默认为90s.
  
默认: 90000
  
hbase.hstore.compaction.max
  
每个“小”合并的HStoreFiles最大数量。
  
默认: 10
  
hbase.hregion.majorcompaction
  
一个Region中的所有HStoreFile的major compactions的时间间隔。默认是1天。 设置为0就是禁用这个功能。
  
默认: 86400000
  
hbase.storescanner.parallel.seek.enable
  
允许 StoreFileScanner 并行搜索 StoreScanner, 一个在特定条件下降低延迟的特性。
  
默认: false

hbase.storescanner.parallel.seek.threads
  
并行搜索特性打开后，默认线程池大小。
  
默认: 10

hbase.mapreduce.hfileoutputformat.blocksize
  
MapReduce中HFileOutputFormat可以写 storefiles/hfiles. 这个值是hfile的blocksize的最小值。通常在HBase写Hfile的时候，bloocksize是由table schema(HColumnDescriptor)决定的，但是在mapreduce写的时候，我们无法获取schema中blocksize。这个值越小，你的索引就越大，你随机访问需要获取的数据就越小。如果你的cell都很小，而且你需要更快的随机访问，可以把这个值调低。
  
默认: 65536
  
hfile.block.cache.size
  
分配给HFile/StoreFile的block cache占最大堆(-Xmx setting)的比例。默认0.25意思是分配25%，设置为0就是禁用，但不推荐。
  
默认:0.25
  
hbase.hash.type
  
哈希函数使用的哈希算法。可以选择两个值:: murmur (MurmurHash) 和 jenkins (JenkinsHash). 这个哈希是给 bloom filters用的.
  
默认: murmur
  
hfile.block.index.cacheonwrite
          
在index写入的时候允许put无根（non-root）的多级索引块到block cache里，默认是false；

     hfile.index.block.max.size：在多级索引的树形结构里，如果任何一层的block index达到这个配置大小，则block写出，同时         
    
     替换上新的block，默认是131072；
    

hfile.format.version
  
新文件的HFile 格式版本，设置为1来测试向后兼容，默认是2；
  
io.storefile.bloom.block.size
  
一个联合布隆过滤器的单一块（chunk）的大小，这个值是一个逼近值，默认是131072；
  
hfile.block.bloom.cacheonwrite
  
对于组合布隆过滤器的内联block开启cache-on-write，默认是false
  
hbase.rs.cacheblocksonwrite
  
当一个HFile block完成时是否写入block cache，默认是false
  
hbase.rpc.server.engine
  
hbase 做rpc server的调度管理类，实现自org.apache.hadoop.ipc.RpcServerEngine，默认是org.apache.hadoop.hbase.ipc.ProtobufRpcServerEngine
  
hbase.ipc.client.tcpnodelay
  
默认是true，具体就是在tcp socket连接时设置 no delay

hbase.master.keytab.file
  
HMaster server验证登录使用的kerberos keytab 文件路径。(译者注：HBase使用Kerberos实现安全)
  
默认:
  
hbase.master.kerberos.principal
  
例如. "hbase/\_HOST@EXAMPLE.COM&#8221;. HMaster运行需要使用 kerberos principal name. principal name 可以在: user/hostname@DOMAIN 中获取. 如果 "\_HOST&#8221; 被用做hostname portion，需要使用实际运行的hostname来替代它。
  
默认:
  
hbase.regionserver.keytab.file
  
HRegionServer验证登录使用的kerberos keytab 文件路径。
  
默认:
  
hbase.regionserver.kerberos.principal
  
例如. "hbase/\_HOST@EXAMPLE.COM&#8221;. HRegionServer运行需要使用 kerberos principal name. principal name 可以在: user/hostname@DOMAIN 中获取. 如果 "\_HOST&#8221; 被用做hostname portion，需要使用实际运行的hostname来替代它。在这个文件中必须要有一个entry来描述 hbase.regionserver.keytab.file
  
默认:
  
hadoop.policy.file
  
RPC服务器做权限认证时需要的安全策略配置文件，在Hbase security开启后使用，默认是habse-policy.xml；
  
hbase.superuser
  
Hbase security 开启后的超级用户配置，一系列由逗号隔开的user或者group；
  
hbase.auth.key.update.interval
  
Hbase security开启后服务端更新认证key的间隔时间：默认是86400000毫秒；
  
hbase.auth.token.max.lifetime
  
Hbase security开启后，认证token下发后的生存周期，默认是604800000毫秒

zookeeper.session.timeout
  
ZooKeeper 会话超时.HBase把这个值传递改zk集群，向他推荐一个会话的最大超时时间。详见http://hadoop.apache.org/zookeeper/docs/current/zookeeperProgrammers.html#ch_zkSessions "The client sends a requested timeout, the server responds with the timeout that it can give the client. "。 单位是毫秒
  
默认: 180000
  
zookeeper.znode.parent
  
ZooKeeper中的HBase的根ZNode。所有的HBase的ZooKeeper会用这个目录配置相对路径。默认情况下，所有的HBase的ZooKeeper文件路径是用相对路径，所以他们会都去这个目录下面。
  
默认: /hbase
  
zookeeper.znode.rootserver
  
ZNode 保存的 根region的路径. 这个值是由Master来写，client和regionserver 来读的。如果设为一个相对地址，父目录就是 ${zookeeper.znode.parent}.默认情形下，意味着根region的路径存储在/hbase/root-region-server.
  
默认: root-region-server

zookeeper.znode.acl.parent
  
root znode的acl，默认acl；
  
hbase.coprocessor.region.classes
  
逗号分隔的Coprocessores列表，会被加载到默认所有表上。在自己实现了一个Coprocessor后，将其添加到Hbase的classpath并加入全限定名。也可以延迟加载，由HTableDescriptor指定；
  
hbase.coprocessor.master.classes
  
由HMaster进程加载的coprocessors，逗号分隔，全部实现org.apache.hadoop.hbase.coprocessor.MasterObserver，同coprocessor类似，加入classpath及全限定名；

hbase.zookeeper.quorum
  
Zookeeper集群的地址列表，用逗号分割。例如：&#8221;host1.mydomain.com,host2.mydomain.com,host3.mydomain.com&#8221;.默认是localhost,是给伪分布式用的。要修改才能在完全分布式的情况下使用。如果在hbase-env.sh设置了HBASE\_MANAGES\_ZK，这些ZooKeeper节点就会和HBase一起启动。
  
默认: localhost
  
hbase.zookeeper.peerport
  
ZooKeeper节点使用的端口。详细参见：http://hadoop.apache.org/zookeeper/docs/r3.1.1/zookeeperStarted.html#sc_RunningReplicatedZooKeeper
  
默认: 2888
  
hbase.zookeeper.leaderport
  
ZooKeeper用来选择Leader的端口，详细参见：http://hadoop.apache.org/zookeeper/docs/r3.1.1/zookeeperStarted.html#sc_RunningReplicatedZooKeeper
  
默认: 3888
  
hbase.zookeeper.useMulti
  
Instructs HBase to make use of ZooKeeper&#8217;s multi-update functionality. This allows certain ZooKeeper operations to complete more quickly and prevents some issues with rare Replication failure scenarios (see the release note of HBASE-2611 for an example). IMPORTANT: only set this to true if all ZooKeeper servers in the cluster are on version 3.4+ and will not be downgraded. ZooKeeper versions before 3.4 do not support multi-update and will not fail gracefully if multi-update is invoked (see ZOOKEEPER-1495).
  
Default: false

hbase.zookeeper.property.initLimit
  
ZooKeeper的zoo.conf中的配置。 初始化synchronization阶段的ticks数量限制
  
默认: 10
  
hbase.zookeeper.property.syncLimit
  
ZooKeeper的zoo.conf中的配置。 发送一个请求到获得承认之间的ticks的数量限制
  
默认: 5
  
hbase.zookeeper.property.dataDir
  
ZooKeeper的zoo.conf中的配置。 快照的存储位置
  
默认: ${hbase.tmp.dir}/zookeeper
  
hbase.zookeeper.property.clientPort
  
ZooKeeper的zoo.conf中的配置。 客户端连接的端口
  
默认: 2181
  
hbase.zookeeper.property.maxClientCnxns
  
ZooKeeper的zoo.conf中的配置。 ZooKeeper集群中的单个节点接受的单个Client(以IP区分)的请求的并发数。这个值可以调高一点，防止在单机和伪分布式模式中出问题。
  
默认: 300
  
hbase.rest.port
  
HBase REST server的端口
  
默认: 8080
  
hbase.rest.readonly
  
定义REST server的运行模式。可以设置成如下的值： false: 所有的HTTP请求都是被允许的 &#8211; GET/PUT/POST/DELETE. true:只有GET请求是被允许的
  
默认: false
  
hbase.defaults.for.version.skip
  
Set to true to skip the &#8216;hbase.defaults.for.version&#8217; check. Setting this to true can be useful in contexts other than the other side of a maven generation; i.e. running in an ide. You&#8217;ll want to set this boolean to true to avoid seeing the RuntimException complaint: "hbase-default.xml file seems to be for and old version of HBase (${hbase.version}), this version is X.X.X-SNAPSHOT&#8221;
  
Default: false
  
是否跳过hbase.defaults.for.version的检查，默认是false；
  
hbase.coprocessor.abortonerror
  
Set to true to cause the hosting server (master or regionserver) to abort if a coprocessor throws a Throwable object that is not IOException or a subclass of IOException. Setting it to true might be useful in development environments where one wants to terminate the server as soon as possible to simplify coprocessor failure analysis.
  
Default: false
  
如果coprocessor加载失败或者初始化失败或者抛出Throwable对象，则主机退出。设置为false会让系统继续运行，但是coprocessor的状态会不一致，所以一般debug时才会设置为false，默认是true；
  
hbase.online.schema.update.enable
  
Set true to enable online schema changes. This is an experimental feature. There are known issues modifying table schemas at the same time a region split is happening so your table needs to be quiescent or else you have to be running with splits disabled.
  
Default: false
  
设置true来允许在线schema变更，默认是true；
  
hbase.table.lock.enable
  
Set to true to enable locking the table in zookeeper for schema change operations. Table locking from master prevents concurrent schema modifications to corrupt table state.
  
Default: true
  
设置为true来允许在schema变更时zk锁表，锁表可以组织并发的schema变更导致的表状态不一致，默认是true；
  
dfs.support.append
  
Does HDFS allow appends to files? This is an hdfs config. set in here so the hdfs client will do append support. You must ensure that this config. is true serverside too when running hbase (You will have to restart your cluster after setting it).
  
Default: true
  
hbase.thrift.minWorkerThreads
  
The "core size&#8221; of the thread pool. New threads are created on every connection until this many threads are created.
  
Default: 16
  
线程池的core size，在达到这里配置的量级后，新线程才会再新的连接创立时创建，默认是16；
  
hbase.thrift.maxWorkerThreads
  
The maximum size of the thread pool. When the pending request queue overflows, new threads are created until their number reaches this number. After that, the server starts dropping connections.
  
Default: 1000
  
顾名思义，最大线程数，达到这个数字后，服务器开始drop连接，默认是1000；
  
hbase.thrift.maxQueuedRequests
  
The maximum number of pending Thrift connections waiting in the queue. If there are no idle threads in the pool, the server queues requests. Only when the queue overflows, new threads are added, up to hbase.thrift.maxQueuedRequests threads.
  
Default: 1000
  
Thrift连接队列的最大数，如果线程池满，会先在这个队列中缓存请求，缓存上限就是该配置，默认是1000；
  
hbase.offheapcache.percentage
  
The amount of off heap space to be allocated towards the experimental off heap cache. If you desire the cache to be disabled, simply set this value to 0.
  
Default: 0
  
JVM参数-XX:MaxDirectMemorySize的百分比值，默认是0，即不开启堆外分配；
  
hbase.data.umask.enable
  
Enable, if true, that file permissions should be assigned to the files written by the regionserver
  
Default: false
  
开启后，文件在regionserver写入时会 有权限相关设定，默认是false不开启；
  
hbase.data.umask
  
File permissions that should be used to write data files when hbase.data.umask.enable is true
  
Default: 000
  
开启上面一项配置后，文件的权限umask，默认是000
  
hbase.metrics.showTableName
  
Whether to include the prefix "tbl.tablename&#8221; in per-column family metrics. If true, for each metric M, per-cf metrics will be reported for tbl.T.cf.CF.M, if false, per-cf metrics will be aggregated by column-family across tables, and reported for cf.CF.M. In both cases, the aggregated metric M across tables and cfs will be reported.
  
Default: true
  
是否为每个指标显示表名前缀，默认是true；
  
hbase.metrics.exposeOperationTimes
  
Whether to report metrics about time taken performing an operation on the region server. Get, Put, Delete, Increment, and Append can all have their times exposed through Hadoop metrics per CF and per region.
  
Default: true
  
是否进行关于操作在使用时间维度的指标报告，比如GET PUT DELETE INCREMENT等，默认是true；
  
hbase.master.hfilecleaner.plugins
  
A comma-separated list of HFileCleanerDelegate invoked by the HFileCleaner service. These HFiles cleaners are called in order, so put the cleaner that prunes the most files in front. To implement your own HFileCleanerDelegate, just put it in HBase&#8217;s classpath and add the fully qualified class name here. Always add the above default log cleaners in the list as they will be overwritten in hbase-site.xml.
  
Default: org.apache.hadoop.hbase.master.cleaner.TimeToLiveHFileCleaner
  
HFile的清理插件列表，逗号分隔，被HFileService调用，可以自定义，默认org.apache.hadoop.hbase.master.cleaner.TimeToLiveHFileCleaner
  
hbase.regionserver.catalog.timeout
  
Timeout value for the Catalog Janitor from the regionserver to META.
  
Default: 600000
  
regionserver的Catalog Janitor访问META的超时时间，默认是600000；
  
hbase.master.catalog.timeout
  
Timeout value for the Catalog Janitor from the master to META.
  
Default: 600000
  
Catalog Janitor从master到META的超时时间，我们知道这个Janitor是定时的去META扫描表目录，来决定回收无用的regions，默认是600000；
  
hbase.config.read.zookeeper.config
  
Set to true to allow HBaseConfiguration to read the zoo.cfg file for ZooKeeper properties. Switching this to true is not recommended, since the functionality of reading ZK properties from a zoo.cfg file has been deprecated.
  
Default: false
  
让hbaseconfig去读zk的config，默认false，也不支持开启，这个功能很搞笑~~个人观点；
  
hbase.snapshot.enabled
  
Set to true to allow snapshots to be taken / restored / cloned.
  
Default: true
  
是否允许snapshot被使用、存储和克隆，默认是true；
  
hbase.rest.threads.max
  
The maximum number of threads of the REST server thread pool. Threads in the pool are reused to process REST requests. This controls the maximum number of requests processed concurrently. It may help to control the memory used by the REST server to avoid OOM issues. If the thread pool is full, incoming requests will be queued up and wait for some free threads. The default is 100.
  
Default: 100
  
REST服务器线程池的最大线程数，池满的话新请求会自动排队，限制这个配置可以控制服务器的内存量，预防OOM，默认是100；
  
hbase.rest.threads.min
  
The minimum number of threads of the REST server thread pool. The thread pool always has at least these number of threads so the REST server is ready to serve incoming requests. The default is 2.
  
Default: 2
  
同上类似，最小线程数，为了确保服务器的服务状态，默认是2；

hbase.client.write.buffer：htable客户端写缓冲区大小，默认是2097152BYTE，这个缓冲区就是为了写数据的临时存放，设置大了，浪费客户端和服务端的存储，设置小了，如果写的数据多，太多的RPC又带来网络开销，官方给的一个服务端存储耗费评估计算是：hbase.client.write.buffer*hbase.regionserver.handler.count，服务端的rs的处理handler个数也很关键；

hbase.client.pause：pause时长，在hbase发生get或其他操作fail掉的时候进行pause的时间长度，默认是100；

hbase.client.retries.number：发生操作fail时的重试次数，结合上一个指标一起来控制总的重试时间，默认是35；

hbase.client.max.total.tasks：一个HTable实例可以提交给集群的最大并发任务数，默认是100；

hbase.client.max.perserver.tasks：一个HTable实例给一台regionserver提交的最大并发任务数，默认是5；

hbase.client.max.perregion.tasks：客户端连接一台region的最大连接数，换句话说，当你有这么多个连接在region时，新的操作不被发送直到有操作完成，默认是1；

hbase.client.scanner.caching：做scanner的next操作时（如果再本地client没找到）缓存的数据行数，这个值的设置也需要权衡，缓存的多则快，但吃内存，缓存的少则需要多的拉数据， 需要注意的事项是如果两次调用的时间差大于scanner的timeout，则不要设置该值，默认是100；

hbase.client.keyvalue.maxsize：一个KeyValue实例的最大大小，这是存储文件中一个entry的容量上限，合理的设置这个值可以控制regionserver的split，split不会拆keyvalue，所以把keyvalue的大小设置为regionserver大小的一个比例分数（可除）是个不错的选择，默认是10485760；

hbase.client.scanner.timeout.period：结合刚才的caching做的一个，scanner的超时时间，默认是60000毫秒；

hbase.client.localityCheck.threadPoolSize：做localityCheck的线程池大小，默认是2；

hbase.bulkload.retries.number：做bulk load的最大重试次数，默认是0，即代表不断重试；

hbase.balancer.period：Master运行balancer的周期，默认是300000毫秒；

hbase.regions.slop：如果有regionserver的region数目超过average+(average*slop)，则rebalance，默认是0.2；

hbase.server.thread.wakefrequency：服务线程的sleep时间，默认10000毫秒，比如log roller；

hbase.server.versionfile.writeattempts：退出前写 version file的重试次数，默认3，每次尝试的间隔由上一个参数控制；

hbase.hregion.memstore.flush.size：Memstore写磁盘的flush阈值，超过这个大小就flush，默认是134217728；

hbase.hregion.preclose.flush.size：如果一个region的memstore的大小等于或超过这个参数的量，在关闭region时（放置关闭flag），要提前flush，然后region关闭下线，默认大小是5242880；

hbase.hregion.memstore.block.multiplier：如果memstore的大小满足hbase.hregion.block.memstore * hbase.hregion.flush.size个byte，那么阻塞update，这个配置可以避免不必要的长时间split或者compact，甚至是OOME，默认是2；

hbase.hregion.memstore.mslab.enabled：开启MemStore-Local Allocation Buffer，这个配置可以避免在高写入的情况下的堆内存碎片，可以降低在大堆情况下的stop-the-world GC频率，默认是true；

hbase.hregion.max.filesize：HStoreFile的最大尺寸，换句话说，当一个region里的列族的任意一个HStoreFile超过这个大小，那么region进行split，默认是10737418240；

hbase.hregion.majorcompaction：一个region的所有HStoreFile进行major compact的时间周期，默认是604800000 毫秒（7天）；

hbase.hregion.majorcompaction.jitter：major compaction的发生抖动范围，这么理解比较容易，就是说上一个参数不是一个严格周期，会有个抖动，这个参数就是这个抖动的比例，默认是0.5；

hbase.hstore.compactionThreshold：一个HStore存储HStoreFile的个数阈值，超过这个阈值则所有的HStoreFile会被写到一个新的HStore，需要平衡取舍，默认是3；

hbase.hstore.blockingStoreFiles：一个HStore存储HStoreFile阻塞update的阈值，超过这个阈值，HStore就进行compaction，直到做完才允许update，默认是10；

hbase.hstore.blockingWaitTime：一个更强力的配置，配合上一个参数，当HStore阻塞update时，超过这个时间限制，阻塞取消，就算compaction没有完成，update也不会再被阻塞，默认是90000毫秒；

hbase.hstore.compaction.max：每个minor compaction的HStoreFile个数上限，默认是10；

hbase.hstore.compaction.kv.max：在flushing或者compacting时允许的最大keyvalue个数，如果有大的KeyValue或者OOME的话则配置一个小的值，如果行数多且小则配置大值，默认是10；

hbase.storescanner.parallel.seek.threads：如果并行查找开启的线程池大小，默认是10；

hfile.block.cache.size：一个配置比例，允许最大堆的对应比例的内存作为HFile和HStoreFile的block cache，默认是0.4，即40%，设置为0则disable这个比例，不推荐这么做；

hfile.block.index.cacheonwrite：在index写入的时候允许put无根（non-root）的多级索引块到block cache里，默认是false；

hfile.index.block.max.size：在多级索引的树形结构里，如果任何一层的block index达到这个配置大小，则block写出，同时替换上新的block，默认是131072；

hfile.format.version：新文件的HFile 格式版本，设置为1来测试向后兼容，默认是2；

hfile.block.bloom.cacheonwrite：对于组合布隆过滤器的内联block开启cache-on-write，默认是false；

io.storefile.bloom.block.size：一个联合布隆过滤器的单一块（chunk）的大小，这个值是一个逼近值，默认是131072；

hbase.rs.cacheblocksonwrite：当一个HFile block完成时是否写入block cache，默认是false；

http://www.blogjava.net/changedi/archive/2014/01/03/408449.html