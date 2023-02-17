---
title: redis 集群/cluster
author: "-"
date: 2016-12-16T02:55:44+00:00
url: /redis-cluster
categories:
  - Redis
tags:
  - reprint
---
## redis 集群/cluster

redis 工作在集群模式的时候除了常规的 tcp 端口 6379, 还需要一个额外的 TCP 端口跟集群内的其它节点通信, 端口号是在 tcp 端口基础上加一个固定的偏移量 10000, `6379 + 10000 = 16379`

<https://rajivsharma-2205.medium.com/enable-tcp-keepalive-on-redis-cluster-bus-153128e412fa>

redis5.0.x 上 redis-trib.rb 工具不再可用，redis-trib.rb 相关的全部功能，已迁移到 redis-cli --cluster 命令上了。

```bash
# 创建集群主节点

redis-cli --cluster create 192.168.163.132:6379 192.168.163.132:6380 192.168.163.132:6381

# 创建集群主从节点
/redis-cli --cluster create 192.168.163.132:6379 192.168.163.132:6380 192.168.163.132:6381 192.168.163.132:6382 192.168.163.132:6383 192.168.163.132:6384 --cluster-replicas 1

# 集群信息查看
redis-cli --cluster info 192.168.163.132:6384

# 检查集群状态
redis-cli --cluster check 192.168.163.132:6379

# 检查集群, 检查是否有槽同时被分配给了多个节点
redis-cli --cluster check 192.168.163.132:6384 --cluster-search-multiple-owners

# 修复集群
redis-cli --cluster fix 192.168.163.132:6384 --cluster-search-multiple-owners

# 添加集群主节点
redis-cli --cluster add-node 192.168.163.132:6382 192.168.163.132:6379 
# 说明: 为一个指定集群添加节点，需要先连到该集群的任意一个节点IP (192.168.163.132:6379) ，再把新节点加入。这两个参数的顺序有要求: 新加入的节点放前面

# 添加集群从节点
redis-cli --cluster add-node 192.168.163.132:6382 192.168.163.132:6379 --cluster-slave --cluster-master-id 117457eab5071954faab5e81c3170600d5192270
说明: 把6382节点加入到6379节点的集群中，并且当做node_id为 117457eab5071954faab5e81c3170600d5192270 的从节点。如果不指定 --cluster-master-id 会随机分配到任意一个主节点。

# 删除节点
redis-cli --cluster del-node 192.168.163.132:6384 f6a6957421b00009106cb36be3c7ba41f3b603ff
# 说明: 指定 IP, 端口和 node_id 来删除一个节点，从节点可以直接删除，主节点不能直接删除，删除之后，该节点会被shutdown。

# 修复集群 
redis-cli --cluster fix 192.168.163.132:6379
```

## cluster

```bash
# 当前连接节点所属集群的配置信息
./redis-cli -p 7000 cluster nodes

# 人工故障切换, 该命令只能在群集slave节点执行
redis-cli -p 7000 CLUSTER FAILOVER
# http://www.redis.cn/commands/cluster-failover.html

redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000
redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000 --cluster-slave
redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000 --cluster-slave --cluster-master-id 3c3a0c74aae0b56170ccb03a76b60cfe7dc1912e
./redis-cli -p 7006> cluster replicate 3c3a0c74aae0b56170ccb03a76b60cfe7dc1912e
redis-cli --cluster del-node 127.0.0.1:7000 3c3a0c74aae0b56170ccb03a76b60cfe7dc1912e
./redis-cli --cluster check 127.0.0.1:7000
```

```bash
# 查看集群状态
cluster info

```

## 返回值

- cluster_state：状态是ok节点是否能够接收查询。fail状态表示有哈希槽没有被绑定到任意一个节点或者节点可以提供服务但是带有fail标记，或者该节点无法连续到多数master节点
- cluster_slots_assigned：与某个节点关联的槽数（不是未绑定的）。这个数字应该是16384，节点才能正常工作，这意味着每个散列槽应该映射到一个节点。
- cluster_slots_ok：哈希槽状态不是Fail和PFail的数量
- cluster_slots_pfail：哈希槽状态是PFAIL的数量。请注意，只要PFAIL状态不由FAIL故障检测算法提升，这些散列槽仍可正常工作。PFAIL仅意味着我们目前无法与节点通话，但可能只是一个暂时的错误。
- cluster_slots_fail：哈希槽状态是FAIL的数量。如果此数字不为零，则该节点无法提供查询，除非在配置中cluster-require-full-coverage设置为no。
- cluster_known_nodes：群集中已知节点的总数，包括处于握手（HANDSHAKE）状态还没有称为集群正式成员的节点
- cluster_size：至少包含一个哈希槽而且能够提供服务的master节点数量
- cluster_current_epoch：集群本地Current Epoch变量的值，这个值在节点故障转移期间创建的独特的自增版本号
- cluster_my_epoch：我们正在与之交谈的Config Epoch节点。这是分配给此节点的当前配置版本。
- cluster_stats_messages_sent：通过node-to-node二进制总线发送的消息数量
- cluster_stats_messages_received：通过node-to-node二进制总线接收的消息数量

### redis cluster哈希槽数量

16348=16k, 用 bitmap 来压缩心跳包的话, 就相当于使用 2_8_10=2KB 大小的心跳包。而如果用 crc16 算法( redis使用这个而不是用哈希一致性算法)来确定哈希槽的分配。他的最大值是是2的16次方。用上面的算法换算需要8KB的心跳包来传输, 作者自己认为这样不划算。而一个redis节点一般不会有超过 1000 个master(这个是作者自己说的), 用16k 来划分是比较合适的

<https://www.zhihu.com/question/54817522>

<https://github.com/antirez/redis/issues/2576>

```bash
wget <https://download.redis.io/releases/redis-6.2.4.tar.gz>
tar xzf redis-6.2.4.tar.gz
cd redis-6.2.4
make

mkdir cluster-test
cd cluster-test
mkdir 7000 7001 7002 7003 7004 7005

vim 7000/redis.conf

port 7000
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly no

cd 7000
../redis-server ./redis.conf

redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 \
127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
--cluster-replicas 1

./redis-cli -p 7000 cluster nodes | grep master
```

在文件夹 7000 至 7005 中, 各创建一个 redis.conf 文件, 文件的内容可以使用上面的示例配置文件, 但记得将配置中的端口号从 7000 改为与文件夹名字相同的号码。

port 7000
  
cluster-enabled yes
  
cluster-config-file nodes.conf
  
cluster-node-timeout 5000
  
appendonly no

cd 7000
  
../redis-server ./redis.conf

搭建集群
  
现在我们已经有了六个正在运行中的 Redis 实例, 接下来我们需要使用这些实例来创建集群, 并为每个节点编写配置文件。

通过使用 Redis 集群命令行工具 redis-trib , 编写节点配置文件的工作可以非常容易地完成:  redis-trib 位于 Redis 源码的 src 文件夹中, 它是一个 Ruby 程序, 这个程序通过向实例发送特殊命令来完成创建新集群, 检查集群, 或者对集群进行重新分片 (reshared) 等工作。

```bash
./redis-trib.rb create --replicas 1 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005
```

redis requires Ruby version >= 2.2.2
  
<https://blog.csdn.net/FengYe_YuLu/article/details/77628094>

这个命令在这里用于创建一个新的集群, 选项–replicas 1 表示我们希望为集群中的每个主节点创建一个从节点。

之后跟着的其他参数则是这个集群实例的地址列表,3个master3个slave redis-trib 会打印出一份预想中的配置给你看, 如果你觉得没问题的话, 就可以输入 yes , redis-trib 就会将这份配置应用到集群当中,让各个节点开始互相通讯,最后可以得到如下信息:

[OK] All 16384 slots covered

/System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/rubygems/core_ext/kernel_require.rb:55:in `require': cannot load such file — redis (LoadError)

注意 : kernel_require.rb:55:in`require': cannot load such file — redis
  
这里就是缺什么,安装什么

我这里用命令:
  
gem intall redis

一、节点失效检测

1.集群中当一个节点向另一个节点发送PING命令,但是目标节点未在给定的时限内返回PING命令的回复时,那么发送命令的节点会将目标节点标记为PFAIL(possible failuer,可能已失效)；
等待节点回复的时限称为节点超时时限 (node timeout) ,是一个节点选项 (node-wise setting) ;

2.每次节点发送对其它节点的PING命令的时候,它都会随机的广播三个它所知道的节点信息,这些信息里面的其中一项就是说明节点是否已经被标记为PFAIL或者FAIL;

3.当节点接收到其它节点发送来的信息时,它会记下哪些被其它节点标记为失效的节点,这称之为失效报告 (failure report) ;

4.如果节点已经将某个节点标记为PFAIL,并且根据节点所收到的失效报告显示,集群中的大部分其它主节点也认为哪个主节点进入了失效状态,那么节点将会把哪个节点标记为失效状态FAIL;

5.一旦某个节点被标记为FAIL,关于这个节点已失效的信息就会广播到整个集群中取,所有接收到这条信息的节点都会将失效信息标记为FAIL;

简单来说一个节点要将另外一个节点标记为失效,必须要询问其它节点的意见,并且得到大部分主节点的同意才行；

因为过期的失效报告会被移除,所以主节点要将某个节点标记为失效FAIL的话,必须以最近接收到的失效报告为根据；

在一下两种情况中失效FAIL状态会被移除:

1.如果被标记为FAIL的是从节点,那么这个节点重新上线时,FAIL标记就会被移除；

保持 (retaining) 从节点的FAIL失效状态是没有意义的,因为它不处理任何槽,一个节点是否处于FAIL状态,决定了这个从节点在有需要的时候能否被提升为主节点；

2.如果一个主节点被打上FAIL标记之后,经过了节点超时时限的四倍时间,在加上10秒中之后,针对这个主节点槽的故障转移操作仍未完成,并且这个主节点已经重新上线的话,那么移除针对这个节点的FAIL标记；

在第二种情况中,如果故障转移未能顺利完成,并且主节点重新上线,那么集群就继续使用原来的主节点,从而免去管理员介入的必要；

二、集群状态检测

每当集群发生配置变化时 (可能是哈希槽更新,也可能是某个节点进入失效状态) ,集群中的每个节点都会对它所知道的节点进行扫描 (scan) ;

一旦配置完毕,集群就会进入两种状态中的一种:

FAIL: 集群不能正常工作,当集群中有某个节点进入失效状态时,集群不能处理任何命令请求,对于每个命令请求,集群节点都返回错误回复；

OK: 集群可以正常工作,负责处理全部16384个槽节点中,没有一个被标记为FAIL状态；

这说明即使集群中只有一部分哈希槽不可以正常使用,整个集群也会停止处理任何命令；

不过节点从出现问题到被标记为FAIL状态这段时间里,集群仍然会正常运行,所以集群在某些时候,仍然可能只能处理针对16384个槽的其中的一个子集的命令；

以下是集群进入FAIL状态的两种情况:

(1) 至少有一个哈希槽不可以用,因为因为负责处理这个槽的节点进入了FAIL装填；

(2) 集群中大部分主节点都进入下线状态,当大部分主节点都进入FAIL状态是,集群也会进入FAIL状态；

第二个检查是必须的,因为要将一个节点从PFAIL状态改变为FAIL状态,必须要有大部分主节点进行投票决定,但是,当集群中大部分主节点进入失效状态时,单凭一两个节点是没有办法将一个节点标记为FAIL状态的；

因此,有了第二个检查条件,只要集群中的大部分主节点进入了下线状态,那么集群就可以在不请求主节点意见的情况下,将某个节点判断为FAIL状态,从而让整个集群停止命令请求；

三、从节点选举

一旦某个主节点进入了FAIL状态,如果这个主节点有一个或者多个从节点存在,那么其中一个从节点会被升级为主节点,而其它从节点会开始对这个新主节点进行复制；

新主节点由已下线的主节点的树下所有从节点自行选举产生,一下是选举条件:

1. 这个节点是已下线主节点的从节点；
2. 已下线主节点处理槽数非空；
3. 从节点的数据被认为是可靠的,也即时,主从节点之间的复制链接 (repliaction link) 的断线时长不能超过超时时限 (node timeout) 乘以REDIS_CLUSTER_SLAVE_VALIDITY_MULT 常量得出的值；

如果一个从节点满足了以上所有条件,那么这个从节点将会向集群中的其它主节点发送授权请求,询问它们,是否允许自己 (从节点) 升级为主节点。

如果发送授权请求的从节点满足一下属性,那么主节点将向从节点返回FAILOVER_AUTH_GRANTED授权,同意从节点的升级要求:

1. 发送授权请求的是一个从节点,并且它所属的主节点处于FAIL状态；
2. 在已下线的主节点的所有从节点中,这个从节点的节点ID在排序中是最小的；
3. 这个从节点处于正常运行状态,它没有被标记为FAIL状态,也没有被标记为PFAIL状态；

一旦某个从节点在给定的时间内得到大部分主节点的授权,它就会执行以下故障转移操作:

 (1) 通过PONG数据包 (package) 告知其它节点,这个节点现在是主节点了；

 (2) 通过PONG数据包告知其它节点,这个节点是一个已经升级的从节点 (promoted salve) ;

 (3) 接管 (claming) 所有由已下线主节点负责处理的哈希槽；

 (4) 显式的向所有的节点广播一个PONG数据包,加速其它节点识别这个节点的速度,而不是等待定时的PING/PONG数据包；

所有其它节点都会根据新的主节点对配置进行相应的更新,特别的:

 (1) 所有被新主节点接管的槽会被更新；

 (2) 已下线主节点的所有从节点会察觉到 PROMOTED 标志, 并开始对新的主节点进行复制；

 (3) 如果已下线的主节点重新回到上线状态, 那么它会察觉到 PROMOTED 标志, 并将自身调整为现任主节点的从节点。

在集群的生命周期中, 如果一个带有 PROMOTED 标识的主节点因为某些原因转变成了从节点, 那么该节点将丢失它所带有的 PROMOTED 标识。
————————————————
版权声明: 本文为CSDN博主「艾米莉Emily」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/yaomingyang/article/details/79081299>

<https://redis.io/topics/cluster-spec>

<http://greemranqq.iteye.com/blog/2229640>

<http://redis.cn/topics/cluster-tutorial.html>

## redis-cli --cluster help

```r
redis-cli --cluster help
Cluster Manager Commands:
  create         host1:port1 ... hostN:portN   #创建集群
                 --cluster-replicas <arg>      #从节点个数
  check          host:port                     #检查集群
                 --cluster-search-multiple-owners #检查是否有槽同时被分配给了多个节点
  info           host:port                     #查看集群状态
  fix            host:port                     #修复集群
                 --cluster-search-multiple-owners #修复槽的重复分配问题
  reshard        host:port                     #指定集群的任意一节点进行迁移slot，重新分slots
                 --cluster-from <arg>          #需要从哪些源节点上迁移slot，可从多个源节点完成迁移，以逗号隔开，传递的是节点的node id，还可以直接传递--from all，这样源节点就是集群的所有节点，不传递该参数的话，则会在迁移过程中提示用户输入
                 --cluster-to <arg>            #slot需要迁移的目的节点的node id，目的节点只能填写一个，不传递该参数的话，则会在迁移过程中提示用户输入
                 --cluster-slots <arg>         #需要迁移的slot数量，不传递该参数的话，则会在迁移过程中提示用户输入。
                 --cluster-yes                 #指定迁移时的确认输入
                 --cluster-timeout <arg>       #设置migrate命令的超时时间
                 --cluster-pipeline <arg>      #定义cluster getkeysinslot命令一次取出的key数量，不传的话使用默认值为10
                 --cluster-replace             #是否直接replace到目标节点
  rebalance      host:port                                      #指定集群的任意一节点进行平衡集群节点slot数量 
                 --cluster-weight <node1=w1...nodeN=wN>         #指定集群节点的权重
                 --cluster-use-empty-masters                    #设置可以让没有分配slot的主节点参与，默认不允许
                 --cluster-timeout <arg>                        #设置migrate命令的超时时间
                 --cluster-simulate                             #模拟rebalance操作，不会真正执行迁移操作
                 --cluster-pipeline <arg>                       #定义cluster getkeysinslot命令一次取出的key数量，默认值为10
                 --cluster-threshold <arg>                      #迁移的slot阈值超过threshold，执行rebalance操作
                 --cluster-replace                              #是否直接replace到目标节点
  add-node       new_host:new_port existing_host:existing_port  #添加节点，把新节点加入到指定的集群，默认添加主节点
                 --cluster-slave                                #新节点作为从节点，默认随机一个主节点
                 --cluster-master-id <arg>                      #给新节点指定主节点
  del-node       host:port node_id                              #删除给定的一个节点，成功后关闭该节点服务
  call           host:port command arg arg .. arg               #在集群的所有节点执行相关命令
  set-timeout    host:port milliseconds                         #设置cluster-node-timeout
  import         host:port                                      #将外部redis数据导入集群
                 --cluster-from <arg>                           #将指定实例的数据导入到集群
                 --cluster-copy                                 #migrate时指定copy
                 --cluster-replace                              #migrate时指定replace


```

<https://redis.io/docs/manual/scaling/>

## k8s, redis-cluster

