---
title: Zookeeper
author: "-"
date: 2015-12-23T02:46:04+00:00
url: zookeeper
categories:
  - Inbox
tags:
  - reprint
---
## Zookeeper

ZooKeeper 是 Hadoop 的一个子项目，一般用来管理较大规模、结构复杂的服务器集群，具有自己的配置文件语法、管理工具和部署模式

- 分布式的K/V存储
- 分布式协调系统
- 微服务注册中心
- 服务发现

zookeeper 起源于 Hadoop 生态系统
zookeeper 使用 ZAB 协议作为其一致性协议  

znode 只能存1M以内的数据  
写入性能低, 为保证一致性, 每次需要n/2+1的写入完成才算完成  
zookeeper 的数据是全部存储在内存, 只适合存元数据  
Zookeeper 的使用场景是有高一致性的  

### 集群模式

Zookeeper 不仅可以单机提供服务,同时也支持多机组成集群来提供服务。实际上 Zookeeper 还支持另外一种伪集群的方式,也就是可以在一台物理机上运行多个 Zookeeper 实例,下面将介绍集群模式的安装和配置。
  
Zookeeper 的集群模式的安装和配置也不是很复杂,所要做的就是增加几个配置项。集群模式除了上面的三个配置项还要增加下面几个配置项:

initLimit=5

syncLimit=2

server.1=192.168.211.1:2888:3888

server.2=192.168.211.2:2888:3888
  
initLimit: 这个配置项是用来配置 Zookeeper 接受客户端 (这里所说的客户端不是用户连接 Zookeeper 服务器的客户端,而是 Zookeeper 服务器集群中连接到 Leader 的 Follower 服务器) 初始化连接时最长能忍受多少个心跳时间间隔数。当已经超过 10 个心跳的时间 (也就是 tickTime) 长度后 Zookeeper 服务器还没有收到客户端的返回信息,那么表明这个客户端连接失败。总的时间长度就是 5_2000=10 秒
  
syncLimit: 这个配置项标识 Leader 与 Follower 之间发送消息,请求和应答时间长度,最长不能超过多少个 tickTime 的时间长度,总的时间长度就是 2_2000=4 秒
  
server.A=B: C: D: 其中 A 是一个数字,表示这个是第几号服务器；B 是这个服务器的 ip 地址；C 表示的是这个服务器与集群中的 Leader 服务器交换信息的端口；D 表示的是万一集群中的 Leader 服务器挂了,需要一个端口来重新进行选举,选出一个新的 Leader,而这个端口就是用来执行选举时服务器相互通信的端口。如果是伪集群的配置方式,由于 B 都是一样,所以不同的 Zookeeper 实例通信端口号不能一样,所以要给它们分配不同的端口号。
  
除了修改 zoo.cfg 配置文件,集群模式下还要配置一个文件 myid,这个文件在 dataDir 目录下,这个文件里面就有一个数据就是 A 的值,Zookeeper 启动时会读取这个文件,拿到里面的数据与 zoo.cfg 里面的配置信息比较从而判断到底是那个 server。

数据模型
  
Zookeeper 会维护一个具有层次关系的数据结构,它非常类似于一个标准的文件系统,

Zookeeper 这种数据结构有如下这些特点:
  
每个子目录项如 NameService 都被称作为 znode, 这个 znode 是被它所在的路径唯一标识, 如 Server1 这个 znode 的标识为 /NameService/Server1

## zookeeper znode

znode 的性质分为 ephemeral 和 persistent 两种。ephemeral 性质的 znode 在创建他的客户端的会话结束, 或者客户端以其他原因断开与服务器的连接时, 会被自动删除。而 persistent 性质的 znode 就不会被自动删除, 除非客户端主动删除, 而且不一定是创建它的客户端可以删除它,其他客户端也可以删除它。

znode 可以有子节点目录, 并且每个 znode 可以存储数据, EPHEMERAL 类型的目录节点不能有子节点目录
  
znode 是有版本的, 每个 znode 中存储的数据可以有多个版本, 也就是一个访问路径中可以存储多份数据
  
znode 可以是临时节点,一旦创建这个 znode 的客户端与服务器失去联系,这个 znode 也将自动删除,Zookeeper 的客户端和服务器通信采用长连接方式,每个客户端和服务器通过心跳来保持连接,这个连接状态称为 session,如果 znode 是临时节点,这个 session 失效,znode 也就删除了
  
znode 的目录名可以自动编号,如 App1 已经存在,再创建的话,将会自动命名为 App2
  
znode 可以被监控,包括这个目录节点中存储的数据的修改,子节点目录的变化等,一旦变化可以通知设置监控的客户端,这个是 Zookeeper 的核心特性,Zookeeper 的很多功能都是基于这个特性实现的,后面在典型的应用场景中会有实例介绍
  
znode 的存储限制最大不超过1M
  
可以通过path来定位 znode, 就像Unix系统定位文件一样, 使用斜杠来表示路径。但是, znode 的路径只能使用绝对路径, 而不能想 Unix 系统一样使用相对路径, 即 Zookeeper 不能识别../和./这样的路径。
  
节点的名称是由Unicode字符组成的,除了zookeeper这个字符串,我们可以任意命名节点。为什么不能使用zookeeper命名节点呢？因为ZooKeeper已经默认使用zookeeper来命名了一个根节点,用来存储一些管理数据。
  
Ephemeral znode绑定了客户端session,但是对任何其他客户端都是可见的,当然是在他们的ACL策略下允许访问的情况下。

Znode的序号

如果在创建znode时,我们使用排序标志的话,ZooKeeper会在我们指定的znode名字后面增加一个数字。我们继续加入相同名字的znode时,这个数字会不断增加。这个序号的计数器是由这些排序znode的父节点来维护的。
  
如果我们请求创建一个znode,指定命名为/a/b-,那么ZooKeeper会为我们创建一个名字为/a/b-3的znode。我们再请求创建一个名字为/a/b-的znode,ZooKeeper会为我们创建一个名字/a/b-5的znode。ZooKeeper给我们指定的序号是不断增长的。Java API中的create()的返回结果就是znode的实际名字。+

那么序号用来干什么呢？当然是用来排序用的！后面《A Lock Service》中我们将讲述如何使用znode的序号来构建一个share lock。

观察模式 Watches

观察模式可以使客户端在某一个znode发生变化时得到通知。观察模式有ZooKeeper服务的某些操作启动,并由其他的一些操作来触发。例如,一个客户端对一个znode进行了exists操作,来判断目标znode是否存在,同时在znode上开启了观察模式。如果znode不存在,这exists将返回false。如果稍后,另外一个客户端创建了这个znode,观察模式将被触发,将znode的创建事件通知之前开启观察模式的客户端。观察模式只能被触发一次。如果要一直获得znode的创建和删除的通知,那么就需要不断的在znode上开启观察模式。

如何使用
  
Zookeeper 作为一个分布式的服务框架,主要用来解决分布式集群中应用系统的一致性问题,它能提供基于类似于文件系统的目录节点树方式的数据存储,但是 Zookeeper 并不是用来专门存储数据的,它的作用主要是用来维护和监控你存储的数据的状态变化。通过监控这些数据状态的变化,从而可以达到基于数据的集群管理,后面将会详细介绍 Zookeeper 能够解决的一些典型问题

ZooKeeper 典型的应用场景
  
Zookeeper 从设计模式角度来看,是一个基于观察者模式设计的分布式服务管理框架,它负责存储和管理大家都关心的数据,然后接受观察者的注册,一旦这些数据的状态发生变化,Zookeeper 就将负责通知已经在 Zookeeper 上注册的那些观察者做出相应的反应,从而实现集群中类似 Master/Slave 管理模式

统一命名服务 (Name Service)
  
分布式应用中,通常需要有一套完整的命名规则,既能够产生唯一的名称又便于人识别和记住,通常情况下用树形的名称结构是一个理想的选择,树形的名称结构是一个有层次的目录结构,既对人友好又不会重复。说到这里你可能想到了 JNDI,没错 Zookeeper 的 Name Service 与 JNDI 能够完成的功能是差不多的,它们都是将有层次的目录结构关联到一定资源上,但是 Zookeeper 的 Name Service 更加是广泛意义上的关联,也许你并不需要将名称关联到特定资源上,你可能只需要一个不会重复名称,就像数据库中产生一个唯一的数字主键一样。
  
Name Service 已经是 Zookeeper 内置的功能,你只要调用 Zookeeper 的 API 就能实现。如调用 create 接口就可以很容易创建一个目录节点。

配置管理 (Configuration Management)
  
配置的管理在分布式应用环境中很常见,例如同一个应用系统需要多台 PC Server 运行,但是它们运行的应用系统的某些配置项是相同的,如果要修改这些相同的配置项,那么就必须同时修改每台运行这个应用系统的 PC Server,这样非常麻烦而且容易出错。
  
像这样的配置信息完全可以交给 Zookeeper 来管理,将配置信息保存在 Zookeeper 的某个目录节点中,然后将所有需要修改的应用机器监控配置信息的状态,一旦配置信息发生变化,每台应用机器就会收到 Zookeeper 的通知,然后从 Zookeeper 获取新的配置信息应用到系统中。

集群管理 (Group Membership)
  
Zookeeper 能够很容易的实现集群管理的功能,如有多台 Server 组成一个服务集群,那么必须要一个"总管"知道当前集群中每台机器的服务状态,一旦有机器不能提供服务,集群中其它集群必须知道,从而做出调整重新分配服务策略。同样当增加集群的服务能力时,就会增加一台或多台 Server,同样也必须让"总管"知道。
  
Zookeeper 不仅能够帮你维护当前的集群中机器的服务状态,而且能够帮你选出一个"总管",让这个总管来管理集群,这就是 Zookeeper 的另一个功能 Leader Election。
  
它们的实现方式都是在 Zookeeper 上创建一个 EPHEMERAL 类型的目录节点,然后每个 Server 在它们创建目录节点的父目录节点上调用 getChildren(String path, boolean watch) 方法并设置 watch 为 true,由于是 EPHEMERAL 目录节点,当创建它的 Server 死去,这个目录节点也随之被删除,所以 Children 将会变化,这时 getChildren上的 Watch 将会被调用,所以其它 Server 就知道已经有某台 Server 死去了。新增 Server 也是同样的原理。

## Zookeeper Leader Election

Zookeeper 如何实现 Leader Election, 也就是选出一个 Master Server。和前面的一样每台 Server 创建一个 EPHEMERAL 目录节点,不同的是它还是一个 SEQUENTIAL 目录节点, 所以它是个 EPHEMERAL_SEQUENTIAL 目录节点。之所以它是 EPHEMERAL_SEQUENTIAL 目录节点, 是因为我们可以给每台 Server 编号, 我们可以选择当前是最小编号的 Server 为 Master, 假如这个最小编号的 Server 死去,由于是 EPHEMERAL 节点, 死去的 Server 对应的节点也被删除, 所以当前的节点列表中又出现一个最小编号的节点,我们就选择这个节点为当前 Master。这样就实现了动态选择 Master,避免了传统意义上单 Master 容易出现单点故障的问题。

共享锁 (Locks)

共享锁在同一个进程中很容易实现,但是在跨进程或者在不同 Server 之间就不好实现了。Zookeeper 却很容易实现这个功能,实现方式也是需要获得锁的 Server 创建一个 EPHEMERAL_SEQUENTIAL 目录节点,然后调用 getChildren方法获取当前的目录节点列表中最小的目录节点是不是就是自己创建的目录节点,如果正是自己创建的,那么它就获得了这个锁,如果不是那么它就调用 exists(String path, boolean watch) 方法并监控 Zookeeper 上目录节点列表的变化,一直到自己创建的节点是列表中最小编号的目录节点,从而获得锁,释放锁很简单,只要删除前面它自己所创建的目录节点就行了。

队列管理

Zookeeper 可以处理两种类型的队列:

当一个队列的成员都聚齐时,这个队列才可用,否则一直等待所有成员到达,这种是同步队列。

队列按照 FIFO 方式进行入队和出队操作,例如实现生产者和消费者模型。

同步队列用 Zookeeper 实现的实现思路如下:

创建一个父目录 /synchronizing,每个成员都监控标志 (Set Watch) 位目录 /synchronizing/start 是否存在,然后每个成员都加入这个队列,加入队列的方式就是创建 /synchronizing/member_i 的临时目录节点,然后每个成员获取 / synchronizing 目录的所有目录节点,也就是 member_i。判断 i 的值是否已经是成员的个数,如果小于成员个数等待 /synchronizing/start 的出现,如果已经相等就创建 /synchronizing/start。

FIFO 队列用 Zookeeper 实现思路如下:

实现的思路也非常简单,就是在特定的目录下创建 SEQUENTIAL 类型的子目录 /queue_i,这样就能保证所有成员加入队列时都是有编号的,出队列时通过 getChildren( ) 方法可以返回当前所有的队列中的元素,然后消费其中最小的一个,这样就能保证 FIFO。

通过nc或者telnet命令访问2181端口,通过执行ruok (Are you OK?) 命令来检查zookeeper是否启动成功:
  
% echo ruok | nc localhost 2181
  
imok
  
那么我看见zookeeper回答我们"I'm OK"。下表中是所有的zookeeper的命名,都是由4个字符组成。

ZooKeeper在数据一致性上实现了如下几个方面:
  
顺序一直性
  
从客户端提交的更新操作是按照先后循序排序的。例如,如果一个客户端将一个znode z赋值为a,然后又将z的值改变成b,那么在这个过程中不会有客户端在z的值变为b后,取到的值是a。
  
原子性

更新操作的结果不是失败就是成功。即,如果更新操作失败,其他的客户端是不会知道的。
  
系统视图唯一性
  
无论客户端连接到哪个服务器,都将看见唯一的系统视图。如果客户端在同一个会话中去连接一个新的服务器,那么他所看见的视图的状态不会比之前服务器上看见的更旧。当ensemble中的一个服务器宕机,客户端去尝试连接另外一台服务器时,如果这台服务器的状态旧于之前宕机的服务器,那么服务器将不会接受客户端的连接请求,直到服务器的状态赶上之前宕机的服务器为止。
  
持久性

一旦更新操作成功,数据将被持久化到服务器上,并且不能撤销。所以服务器宕机重启,也不会影响数据。
  
时效性

系统视图的状态更新的延迟时间是有一个上限的,最多不过几十秒。如果服务器的状态落后于其他服务器太多,ZooKeeper会宁可关闭这个服务器上的服务,强制客户端去连接一个状态更新的服务器。
  
从执行效率上考虑,读操作的目标是内存中的缓存数据,并且读操作不会参与到写操作的全局排序中。这就会引起客户端在读取ZooKeeper的状态时产生不一致。例如,A客户端将znode z的值由$$a$$改变成$$a^{'}$$,然后通知客户端B去读取z的值,但是B读取到的值是$$a$$,而不是修改后的$$a^{'}$$。为了阻止这种情况出现,B在读取z的值之前,需要调用sync方法。sync方法会强制B连接的服务器状态与leader的状态同步,这样B在读取z的值就是A重新更改过的值了。

3.设置环境变量
  
在/etc/profile,/home/hadoop/.bashrc文件中添加如下红色信息
  
set java environment
  
ZOOKEEPER_HOME=/home/hadoop/zookeeper-3.4.3
  
MAHOUT_HOME=/home/hadoop/mahout-distribution-0.7
  
PIG_HOME=/home/hadoop/pig-0.9.2
  
HBASE_HOME=/home/hadoop/hbase-0.94.3
  
HIVE_HOME=/home/hadoop/hive-0.9.0
  
HADOOP_HOME=/home/hadoop/hadoop-1.1.1
  
JAVA_HOME=/home/hadoop/jdk1.7.0
  
PATH=$JAVA_HOME/bin:$ZOOKEEPER_HOME/bin:$PIG_HOME/bin:$MAHOUT_HOME/bin:$HBASE_HOME/bin:$HIVE_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/conf:$PATH
  
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$ZOOKEEPER_HOME/lib:$HBASE_HOME/lib:$MAHOUT_HOME/lib:$PIG_HOME/lib:$HIVE_HOME/lib:$JAVA_HOME/lib/tools.jar
  
export ZOOKEEPER_HOME
  
export MAHOUT_HOME
  
export PIG_HOME
  
export HBASE_HOME
  
export HADOOP_HOME
  
export JAVA_HOME
  
export HIVE_HOME
  
export PATH
  
export CLASSPATH

ZooKeeper是一个分布式的,开放源码的应用程序协调服务,为分布式应用提供一致性服务,是Google的Chubby一个开源的实现(根据google发表的The Chubby lock service for loosely-coupled distributed systems 论文实现),是开源的Hadoop项目中的一个子项目,是Hadoop和Hbase的重要组件。
  
提供的功能包括: 配置维护、名字服务、分布式同步、组服务等。
  
它主要是用来解决分布式应用中经常遇到的一些数据管理问题,如: 统一命名服务、状态同步服务、集群管理、分布式应用配置项的管理等。
  
Zookeeper 的典型的应用场景 (配置文件的管理、集群管理、同步锁、Leader 选举、队列管理等)

ZooKeeper的目标就是封装好复杂易出错的关键服务,将简单易用的接口和性能高效、功能稳定的系统提供给用户。
  
ZooKeeper包含一个简单的原语集,[1] 提供Java和C的接口。
  
ZooKeeper代码版本中,提供了分布式独享锁、选举、队列的接口,代码在zookeeper-3.4.3\src\recipes。其中分布锁和队列有Java和C两个版本,选举只有Java版本。ZooKeeper是以Fast Paxos算法为基础的,paxos算法存在活锁的问题,即当有多个proposer交错提交时,有可能互相排斥导致没有一个proposer能提交成功,而Fast Paxos作了一些优化,通过选举产生一个leader,只有leader才能提交propose,具体算法可见Fast Paxos。因此,要想弄懂ZooKeeper首先得对Fast Paxos有所了解。[3]
  
ZooKeeper的基本运转流程:
  
1. 选举Leader。
  
2. 同步数据。
  
3. 选举Leader过程中算法有很多,但要达到的选举标准是一致的。
  
4. Leader要具有最高的zxid。
  
5. 集群中大多数的机器得到响应并follow选出的Leader。[3] 在Zookeeper中,znode是一个跟Unix文件系统路径相似的节点,可以往这个节点存储或获取数据。如果在创建znode时Flag设置为EPHEMERAL,那么当创建这个znode的节点和Zookeeper失去连接后,这个znode将不再存在在Zookeeper里,Zookeeper使用Watcher察觉事件信息。当客户端接收到事件信息,比如连接超时、节点数据改变、子节点改变,可以调用相应的行为来处理数据。Zookeeper的Wiki页面展示了如何使用Zookeeper来处理事件通知,队列,优先队列,锁,共享锁,可撤销的共享锁,两阶段提交。
  
那么Zookeeper能作什么事情呢,简单的例子: 假设我们有20个搜索引擎的服务器(每个负责总索引中的一部分的搜索任务)和一个总服务器(负责向这20个搜索引擎的服务器发出搜索请求并合并结果集),一个备用的总服务器(负责当总服务器宕机时替换总服务器),一个web的cgi(向总服务器发出搜索请求)。搜索引擎的服务器中的15个服务器提供搜索服务,5个服务器正在生成索引。这20个搜索引擎的服务器经常要让正在提供搜索服务的服务器停止提供服务开始生成索引,或生成索引的服务器已经把索引生成完成可以搜索提供服务了。使用Zookeeper可以保证总服务器自动感知有多少提供搜索引擎的服务器并向这些服务器发出搜索请求,当总服务器宕机时自动启用备用的总服务器。[4] HBase和ZooKeeper
  
HBase内置有ZooKeeper,也可以使用外部ZooKeeper。
  
让HBase使用一个已有的不被HBase托管的Zookeep集群,需要设置 conf/hbase env sh文件中的HBASE_MANAGES_ZK 属性为 false
  
… # Tell HBase whether it should manage it's own instance of Zookeeper or not. export HBASE_MANAGES_ZK=false
  
接下来,指明Zookeeper的host和端口。可以在 hbase-site.xml中设置, 也可以在HBase的CLASSPATH下面加一个zoo.cfg配置文件。 HBase 会优先加载 zoo.cfg 里面的配置,把hbase-site.xml里面的覆盖掉.
  
当HBase托管ZooKeeper的时候,Zookeeper集群的启动是HBase启动脚本的一部分。但你需要自己去运行。你可以这样做
  
${HBASE_HOME}/bin/hbase-daemons sh {start,stop} zookeeper
  
你可以用这条命令启动ZooKeeper而不启动HBase. HBASE_MANAGES_ZK 的值是 false, 如果你想在HBase重启的时候不重启ZooKeeper,你可以这样做
  
对于独立Zoopkeeper的问题,你可以在 Zookeeper启动得到帮助.[5]

ZooKeeper 典型的应用场景

Zookeeper 从设计模式角度来看,是一个基于观察者模式设计的分布式服务管理框架,它负责存储和管理大家都关心的数据,然后接受观察者的注册,一旦这些数据的状态发生变化,Zookeeper 就将负责通知已经在 Zookeeper 上注册的那些观察者做出相应的反应,从而实现集群中类似 Master/Slave 管理模式,关于 Zookeeper 的详细架构等内部细节可以阅读 Zookeeper 的源码

下面详细介绍这些典型的应用场景,也就是 Zookeeper 到底能帮我们解决那些问题？下面将给出答案。

配置管理 (Configuration Management)

配置的管理在分布式应用环境中很常见,例如同一个应用系统需要多台 PC Server 运行,但是它们运行的应用系统的某些配置项是相同的,如果要修改这些相同的配置项,那么就必须同时修改每台运行这个应用系统的 PC Server,这样非常麻烦而且容易出错。

像这样的配置信息完全可以交给 Zookeeper 来管理,将配置信息保存在 Zookeeper 的某个目录节点中,然后将所有需要修改的应用机器监控配置信息的状态,一旦配置信息发生变化,每台应用机器就会收到 Zookeeper 的通知,然后从 Zookeeper 获取新的配置信息应用到系统中。

集群管理 (Group Membership)

Zookeeper 能够很容易的实现集群管理的功能,如有多台 Server 组成一个服务集群,那么必须要一个"总管"知道当前集群中每台机器的服务状态,一旦有机器不能提供服务,集群中其它集群必须知道,从而做出调整重新分配服务策略。同样当增加集群的服务能力时,就会增加一台或多台 Server,同样也必须让"总管"知道。

Zookeeper 不仅能够帮你维护当前的集群中机器的服务状态,而且能够帮你选出一个"总管",让这个总管来管理集群,这就是 Zookeeper 的另一个功能 Leader Election。

它们的实现方式都是在 Zookeeper 上创建一个 EPHEMERAL 类型的目录节点,然后每个 Server 在它们创建目录节点的父目录节点上调用getChildren(String path, boolean watch) 方法并设置 watch 为 true,由于是 EPHEMERAL 目录节点,当创建它的 Server 死去,这个目录节点也随之被删除,所以 Children 将会变化,这时 getChildren上的 Watch 将会被调用,所以其它 Server 就知道已经有某台 Server 死去了。新增 Server 也是同样的原理。

队列管理

Zookeeper 可以处理两种类型的队列:

当一个队列的成员都聚齐时,这个队列才可用,否则一直等待所有成员到达,这种是同步队列。
  
队列按照 FIFO 方式进行入队和出队操作,例如实现生产者和消费者模型。
  
同步队列用 Zookeeper 实现的实现思路如下:

创建一个父目录 /synchronizing,每个成员都监控标志 (Set Watch) 位目录 /synchronizing/start 是否存在,然后每个成员都加入这个队列,加入队列的方式就是创建 /synchronizing/member_i 的临时目录节点,然后每个成员获取 / synchronizing 目录的所有目录节点,也就是 member_i。判断 i 的值是否已经是成员的个数,如果小于成员个数等待 /synchronizing/start 的出现,如果已经相等就创建 /synchronizing/start。

Zookeeper 作为 Hadoop 项目中的一个子项目,是 Hadoop 集群管理的一个必不可少的模块,它主要用来控制集群中的数据,如它管理 Hadoop 集群中的 NameNode,还有 Hbase 中 Master Election、Server 之间状态同步等。

本文介绍的 Zookeeper 的基本知识,以及介绍了几个典型的应用场景。这些都是 Zookeeper 的基本功能,最重要的是 Zoopkeeper 提供了一套很好的分布式集群管理的机制,就是它这种基于层次型的目录树的数据结构,并对树中的节点进行有效管理,从而可以设计出多种多样的分布式的数据管理模型,而不仅仅局限于上面提到的几个常用应用场景。

><https://blog.csdn.net/zzhongcy/article/details/89401204>
><https://draveness.me/zookeeper-chubby/>
