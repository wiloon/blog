---
title: zookeeper
author: "-"
date: 2015-01-14T09:32:00+00:00
url: zookeeper
categories:
  - zookeeper
tags:
  - zookeeper
---
## zookeeper
### [16/11/21 03:20:30:030 CST] main-SendThread(192.168.50.100:2181)  WARN zookeeper.ClientCnxn: Session 0x0 for server 192.168.50.100/<unresolved>:2181, unexpected error, closing socket connection and attempting reconnect

检查zookeeper包版本和连接的服务端版本，有可能是版本不一致
>https://blog.csdn.net/richie696/article/details/112910751

### 向zookeeper 发送 stat命令 查询zookeeper版本

```bash
echo stat | socat - TCP:192.168.50.100:2181
```

## server

```bash
# docker
docker run \
--name zookeeper \
-p 2181:2181 \
-v /etc/localtime:/etc/localtime:ro \
-v zookeeper-conf:/conf \
-v zookeeper-data:/data \
-v zookeeper-datalog:/datalog \
-d \
zookeeper

# podman
podman run \
--name zookeeper \
-p 2181:2181 \
-v /etc/localtime:/etc/localtime:ro \
-e ZOO_4LW_COMMANDS_WHITELIST=*  \
-d \
zookeeper

# conf, data volume
podman run \
--name zookeeper \
-p 2181:2181 \
-v /etc/localtime:/etc/localtime:ro \
-v zookeeper-conf:/conf \
-v zookeeper-data:/data \
-v zookeeper-datalog:/datalog \
-e ZOO_4LW_COMMANDS_WHITELIST=*  \
-d \
zookeeper:3.7.0

# client
docker run -it --rm zookeeper zkCli.sh -server 127.0.0.1

```

```bash
#zkCli.sh
#连接zookeeper
bin/zkCli.sh -server localhost:2181

#创建节点
create /k0 v0

# 删除一个节点
delete /k0
```
### install
download zookeeper
cp zoo_sample.cfg zoo.cfg

### 配置， vim zoo.cfg
```bash
#zookeeper 服务器心跳时间，单位为ms
tickTime=2000
##Zookeeper最小时间单元，单位毫秒(ms)，默认值为2000, #投票选举新 leader 的初始化时间
initLimit=5
##Leader服务器等待Follower启动并完成数据同步的时间，默认值10，表示tickTime的10倍

# syncLimit, Leader服务器和Follower之间进行心跳检测的最大延时时间，默认值5，表示tickTime的5倍
#leader 与 follower 心跳检测最大容忍时间，响应超过 tickTime * syncLimit，认为 leader 丢失该 follower
syncLimit=2
#dataDir, 数据目录
##Zookeeper 服务器存储快照文件的目录，必须配置
dataDir=/data/server/zookeeper/data

dataLogDir=/data/logs/zookeeper
##Zookeeper服务器存储事务日志的目录，默认为dataDir

# clientPort, 服务器对外服务端口，一般设置为2181
clientPort=2181




autopurge.purgeInterval=1
```
从3.4.0开始，zookeeper提供了自动清理snapshot和事务日志的功能，通过配置 autopurge.snapRetainCount 和 autopurge.purgeInterval 这两个参数能够实现定时清理了。这两个参数都是在zoo.cfg中配置的: 

autopurge.purgeInterval 这个参数指定了清理频率，单位是小时，需要填写一个1或更大的整数，默认是0，表示不开启自己清理功能。

autopurge.snapRetainCount 这个参数和上面的参数搭配使用，这个参数指定了需要保留的文件数目。默认是保留3个。

http://www.importnew.com/23237.html
  
http://blog.51cto.com/nileader/932156

```bash
export ZOOKEEPER_HOME=~/sw/zookeeper-x.y.z
export PATH=$PATH:$ZOOKEEPER_HOME/bin
cd /home/xxx/apps/zookeeper-3.4.9/conf
mv zoo_sample.cfg zoo.cfg
mkdir /data/zookeeper
```

### 修改配置文件zoo.cfg
  
tickTime: 这个时间是作为 Zookeeper 服务器之间或客户端与服务器之间维持心跳的时间间隔，也就是每个 tickTime 时间就会发送一个心跳。
  
dataDir: datadir是zookeeper持久化数据存放的目录， 默认情况下，Zookeeper 将写数据的日志文件也保存在这个目录里。默认为/tmp/zookeeper， 改成/data/zookeeper
  
clientPort: clientPort是zookeeper监听客户端连接的端口，默认是2181.

```bash
#start zookeeper
zkServer.sh start
```

ZooKeeper确实对数据的大小有限制，默认就是1M，如果希望传输超过1M的数据，可以修改环境变量“jute.maxbuffer”
### 为什么要限制ZOOKEEPER中ZNODE的大小
ZooKeeper是一套高吞吐量的系统，为了提高系统的读取速度，ZooKeeper不允许从文件中读取需要的数据，而是直接从内存中查找。

还句话说，ZooKeeper集群中每一台服务器都包含全量的数据，并且这些数据都会加载到内存中。同时ZNode的数据并支持Append操作，全部都是Replace。

所以从上面分析可以看出，如果ZNode的过大，那么读写某一个ZNode将造成不确定的延时;同时ZNode过大，将过快地耗尽ZooKeeper服务器的内存。这也是为什么ZooKeeper不适合存储大量的数据的原因。

https://holynull.gitbooks.io/zookeeper/content/
  
http://www.cnblogs.com/linjiqin/archive/2013/03/16/2962597.html
  
https://www.ibm.com/developerworks/cn/opensource/os-cn-zookeeper/
  
<http://www.wiloon.com/?p=8594>
  
https://my.oschina.net/xianggao/blog/531613
>https://www.jianshu.com/p/30bcaf55f451