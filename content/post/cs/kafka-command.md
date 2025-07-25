---
title: kafka basic, command
author: "-"
date: 2025-05-22 09:24:19
url: kafka
categories:
  - Kafka
tags:
  - reprint
  - remix
  - command
---
## kafka basic, command

kafka_2.13-3.4.0.tgz

scala 版本 2.13
kafka 版本 3.4.0

## TLS kafka

todo

## commands

```Bash
# list topic
/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092
# create topic
/opt/kafka/bin/kafka-topics.sh --create --partitions 1 --replication-factor 1 --topic topic_0 --bootstrap-server 127.0.0.1:9092
# consumer
/opt/kafka/bin/kafka-console-consumer.sh --topic topic_0 --bootstrap-server 127.0.0.1:9092
# producer
/opt/kafka/bin/kafka-console-producer.sh --bootstrap-server 127.0.0.1:9092 --topic topic_0
# list group name
/opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server 127.0.0.1:9092 --list

# 查看 consumer group offset
/opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server 127.0.0.1:9092 --describe --group group0

# tls
./kafka-topics.sh --list --bootstrap-server 127.0.0.1:9093 --command-config /tmp/kafka.conf
```

content of kafka.conf

```bash
# kafka.config
# kafka 启用了 TLS, 配置文件如果不配置 security.protocol=SSL, 客户端会默认用 PLAINTEXT 连接 9093, 然后 报异常 OutOfMemoryError: Java heap space
security.protocol=SSL
ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=password_0
ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=password_0
# 是否校验服务端主机名, 默认检验主机名, 值是: https, 赋空值禁用主机名校验
ssl.endpoint.identification.algorithm=
```

### consumer

```bash
# 打印 key
bin/kafka-console-consumer.sh --topic du_fwa_commit --property print.key=true --property key.separator="-" --bootstrap-server 127.0.0.1:9092

bin/kafka-console-consumer.sh --topic topic0 --bootstrap-server 127.0.0.1:9092
# 指定 consumer group
bin/kafka-console-consumer.sh --topic topic0 --bootstrap-server 127.0.0.1:9092 --group group0
# ssl
bin/kafka-console-consumer.sh --topic topic0 --bootstrap-server 127.0.0.1:9092 --consumer.config config.json
# auto_offset_reset="earliest"
bin/kafka-console-consumer.sh --topic topic0 --from-beginning --bootstrap-server localhost:9092

bin/kafka-console-consumer.sh \
--bootstrap-server kafka.wiloon.com:9092 \
--topic topic0 \
--from-beginning \
--property "parse.key=true" \
--property "key.separator=:"

bin/kafka-console-consumer.sh \
--bootstrap-server kafka.wiloon.com:9092 \
--topic topic0 \
--from-beginning
```

### producer

```bash
bin/kafka-console-producer.sh \
--bootstrap-server 127.0.0.1:9092 \
--topic topic0

bin/kafka-console-producer.sh \
--bootstrap-server kafka.wiloon.com:9092 \
--topic topic0

bin/kafka-console-producer.sh \
--bootstrap-server kafka.wiloon.com:9092 \
--topic topic0
--property "parse.key=true" --property "key.separator=@"
```

### kafka download

[https://mirrors.bfsu.edu.cn/apache/kafka/2.6.0/kafka_2.13-2.6.0.tgz](https://mirrors.bfsu.edu.cn/apache/kafka/2.6.0/kafka_2.13-2.6.0.tgz)

## group

### group detail, offset

查看 group detail

```bash
# list group detail, partition, offset, lag
bin/kafka-consumer-groups.sh \
--bootstrap-server 127.0.0.1:9092 \
--describe \
--group group0

bin/kafka-consumer-groups.sh \
--bootstrap-server local-lab:9092 \
--describe \
--group group0
```

```bash
# list all group
bin/kafka-consumer-groups.sh \
--bootstrap-server kafka.wiloon.com:9092 --list

bin/kafka-consumer-groups.sh \
--bootstrap-server kafka.wiloon.com:9092 \
--describe \
--group my-group \
--command-config /path/to/kafka.conf

bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
--describe \
--group my-group
--members

bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
--describe \
--group my-group
--state
```

## offset

CURRENT-OFFSET = LOG-END-OFFSET 说明当前消费组已经全部消费了;

- CURRENT-OFFSET：该分区当前消费到的 offset
- LOG-END-OFFSET(LEO)： 日志最后的偏移量, 该分区当前latest offset, 记录底层日志 (log) 中的下一条消息的 offset, 对 producer 来说，就是即将插入下一条消息的 offset。
- LAG：消费滞后区间，为 `LOG-END-OFFSET - CURRENT-OFFSET`，具体大小需要看应用消费速度和生产者速度，一般过大则可能出现消费跟不上，需要引起注意
- CONSUMER-ID：server端给该分区分配的consumer编号
- HOST：消费者所在主机
- CLIENT-ID：消费者id，一般由应用指定

### 命令行手动调整 offset

```bash
# 不加 --execute 只是打印出位移调整方案，不具体执行
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --topic topic0 --to-offset 500000

# 加 --execute 参数: 执行位移调整
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --topic topic0 --to-offset 500000 --execute

# shift by
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --topic topic0 --shift-by 1

bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --topic topic0 --to-current --execute
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --all-topics --to-earliest --execute

bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --all-topics --to-latest --dry-run
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --all-topics --to-latest --execute 
```

## topic

### list topic, 查看 kafka topic 列表, 使用 --list 参数

```bash
# kafka 3.0
bin/kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092
bin/kafka-topics.sh --list --bootstrap-server 192.168.50.169:9092

bin/kafka-topics.sh --list --zookeeper localhost:2181

~/apps/kafka_2.13-3.2.1/bin/kafka-topics.sh --list --bootstrap-server 127.0.0.1:9093 --command-config ~/projects/project0/kafka.config
```



#### 可用的配置项

[https://kafka.apache.org/090/documentation.html](https://kafka.apache.org/090/documentation.html)

ssl.endpoint.identification.algorithm 默认值问题

[https://docs.confluent.io/platform/current/kafka/authentication_ssl.html](https://docs.confluent.io/platform/current/kafka/authentication_ssl.html)

生成证书 keystore trust store...

[https://www.cnblogs.com/huxi2b/p/7427815.html](https://www.cnblogs.com/huxi2b/p/7427815.html)

### 查看 topic 详细信息, 如: 分区数, replication

```bash
# kafka 3.0.0
bin/kafka-topics.sh --describe --topic topic0 --bootstrap-server 192.168.50.169:9092

# kafka old version
bin/kafka-topics.sh \
--zookeeper zookeeper.wiloon.com:2181 \
--topic topic0 \
--describe
```

replication-factor: 副本数, partitions: 分区数
topic 名中有`.` 或 `_` 会提示:  WARNING: Due to limitations in metric names, topics with a period ('.') or underscore ('_') could collide. To avoid issues it is best to use either, but not both.

### create topic

```bash
# kafka 3.0.0
# 个人习惯, topic 名字用下划线分隔, 鼠标双击能选中...
bin/kafka-topics.sh --create --partitions 1 --replication-factor 1 --topic topic_0 --bootstrap-server 192.168.50.169:9092
bin/kafka-topics.sh --create --partitions 3 --replication-factor 3 --topic topic_0 --bootstrap-server 192.168.50.169:9092

# cloudera kafka
/opt/cloudera/parcels/KAFKA/bin/kafka-topics --create \
--zookeeper 127.0.0.1:2181 \
--replication-factor 3 \
--partitions 30 \
--topic topic_0 \
--config retention.ms=1296000000 \
--config retention.bytes=10737418240
    
# kafka
bin/kafka-topics.sh --create \
--zookeeper test-zookeeper-1,test-zookeeper-2 \
--replication-factor 3 \
--partitions 5 \
--topic topic0

# kafka
bin/kafka-topics.sh --create \
--zookeeper zookeeper.wiloon.com:2181 \
--replication-factor 1 \
--partitions 1 \
--topic topic0
```

[https://cloud.tencent.com/developer/article/1436988](https://cloud.tencent.com/developer/article/1436988)

### 调整分区数, add partition

kafka topic 可以动态增加分区数。  
注意该命令分区数 partitions 只能增加, 不能减少, --partitions 5: 调整之后的分区数.

```bash
# kafka >3.0
# 如果重复执行这个命令而且分区数相同, 会提示 topic already has x partitions.
bin/kafka-topics.sh \
--bootstrap-server 127.0.0.1:9092 \
--alter \
--topic topic0 \
--partitions 3

# kafka <3.0
bin/kafka-topics.sh \
--zookeeper ip0:2181 \
--alter \
--topic topic0 \
--partitions 5
```

### 重置 offset

```bash
./kafka-consumer-groups.sh \
--bootstrap-server broker_ip_0:9092 \
--reset-offsets --group <group id> \
--topic topic0:partition0 \
--to-offset 20 --execute

bin/kafka-consumer-groups.sh \
--bootstrap-server localhost:9092 \
--group test-group --reset-offsets \
--all-topics --to-offset 500000 --execute

bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
--group test-group --reset-offsets --all-topics \
--to-datetime 2017-08-04T14:30:00.000
```

### 查看 kafka 版本, kafka version

```bash
# kafka 客户端的版本
bin/kafka-topics.sh --version

# 到 kafka/libs 目录下查看 kafka 包的文件名, 比如:kafka_2.13-3.1.0.jar,  where 2.13 is Scala version and 3.1.0 is Kafka version.

```

## kafka 删除 topic

- 停掉 topic 对应的 producer 和 consumer 或者设置 auto.create.topics.enable = false
- server.properties 设置 delete.topic.enable=true, 1.0.0 版本以后的 kafka 默认是 true, [https://issues.apache.org/jira/browse/KAFKA-5384](https://issues.apache.org/jira/browse/KAFKA-5384)
- 删除 topic

## kafka.conf

```Bash
security.protocol=SSL
ssl.keystore.location=/home/top/KZ/kafka_2.13-2.6.3/cert/server.keystore.jks
ssl.keystore.password=123456
ssl.truststore.location=/home/top/KZ/kafka_2.13-2.6.3/cert/server.truststore.jks
ssl.truststore.password=1q2w3e4r5t6y
ssl.key.password=123456

ssl.enabled.protocols=TLSv1.2
enable.ssl.certificate.verification=false
ssl.endpoint.identification.algorithm=
```

```bash
# normal kafka
bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic topic0

# tls kafka
bin/kafka-topics.sh --bootstrap-server 127.0.0.1:9093 --delete --topic topic0  --command-config /root/tmp/kafka.conf

# old version
bin/kafka-topics.sh --topic t0 --delete --zookeeper test-zookeeper-1
```

- 删除kafka存储目录

上一步删除 topic之后 kafka 会把对应的 topic 的存储目录改名成 foo-delete, 然后删掉, kafka 2.5 是这样的, 不需要手动删除.

（server.properties文件log.dirs配置，默认为"/data/kafka-logs"）相关topic的数据目录

- 删除 zookeeper 里的数据

kafka 2.5 会自动删除 zk 里的 topic 数据, 不需要手动操作.

```bash
./zkCli.sh

ls /brokers/topics/
deleteall /brokers/topics/topic0
```

```bash
# edit bin/kafka-server-start.sh, change memory setting KAFKA_HEAP_OPTS
# start kafka server
bin/kafka-server-start.sh config/server.properties

#start kafka server as daemon
bin/kafka-server-start.sh -daemon config/server.properties

bin/kafka-console-producer.sh --broker-list localhost:9092 --topic topic0
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic0 --from-beginning --property "parse.key=true" --property "key.separator=:"

./bin/kafka-server-start.sh config/server.properties

# 查看不可用分区 ./kafka-topics.sh --topic test --describe --unavailable-partitions --zookeeper
bin/kafka-console-producer.sh --broker-list test-kafka-1:9092 --topic t0
bin/kafka-console-consumer.sh --bootstrap-server --zookeeper xxx:2181 test-kafka-1:9092 --topic t0 --from-beginning

bin/kafka-console-consumer.sh --bootstrap-server test-kafka-1:9092 --topic t0 --from-beginning

# 会只消费 N 条数据,如果配合 --from-beginning,就会消费最早 N 条数据
bin/kafka-console-consumer.sh --bootstrap-server test-kafka-1:9092 --topic t0 --max-messages 10
```

### 调整 ReplicationFactor

```bash
cat increase-replication-factor.json
    
    {"version":1,
    "partitions":[{"topic":"connect-configs","partition":0,"replicas":[0,1,2]}]
    }
    
bin/kafka-reassign-partitions.sh --zookeeper localhost:2182 --reassignment-json-file increase-replication-factor.json --execute
```

## install

ubuntu install kafka, no docker kafka 4.0

```bash
sudo apt update
sudo apt install default-jdk
sudo adduser --system --no-create-home --group kafka

cd /opt
sudo wget https://dlcdn.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz
sudo tar -xvzf kafka_2.13-4.0.0.tgz
ssudo ln -s kafka_2.13-4.0.0 kafka
sudo chown -R kafka:kafka /opt/kafka
sudo chown -R kafka:kafka /opt/kafka_2.13-4.0.0

# create log.dir
mkdir /var/lib/kafka
sudo chown -R kafka:kafka /var/lib/kafka

# create config dir
sudo mkdir -p /etc/kafka
sudo chown -R kafka:kafka /etc/kafka

```

kafka 4.0 配置
/etc/kafka/server.properties

修改 log dir: log.dirs=/var/lib/kafka


```bash
KAFKA_CLUSTER_ID="$(/opt/kafka/bin/kafka-storage.sh random-uuid)"
/opt/kafka/bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c /etc/kafka/server.properties

sudo chown -R kafka:kafka /var/lib/kafka
/opt/kafka/bin/kafka-server-start.sh /etc/kafka/server.properties


```

/etc/systemd/system/kafka.service

```bash
[Unit]
Description=Apache Kafka (KRaft mode)
After=network.target

[Service]
Type=simple
ExecStart=/opt/kafka/bin/kafka-server-start.sh /etc/kafka/server.properties
Restart=on-failure
User=kafka
Group=kafka
LimitNOFILE=100000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable kafka
sudo systemctl start kafka
```

### kafka 3.9 kraft

```bash
# create log.dir
mkdir /var/lib/kafka/data
mkdir /var/lib/kafka/meta-logs
sudo chown -R kafka:kafka /var/lib/kafka
```

kafka 3.9 kraft 配置

```bash
# Kafka Broker ID
#broker.id=0
node.id=1

# 启用 KRaft 模式
process.roles=broker,controller

# 控制器节点列表
controller.quorum.voters=1@localhost:9093

# Kafka 网络配置
listeners=PLAINTEXT://localhost:9092,CONTROLLER://localhost:9093
listener.security.protocol.map=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
inter.broker.listener.name=PLAINTEXT
controller.listener.names=CONTROLLER

# 数据目录（metadata logs 是 KRaft 的关键）
log.dirs=/data/kafka/data
metadata.log.dir=/data/kafka/meta-logs
```

Kafka KRaft 模式必须在第一次启动前执行一次元数据格式化：


```bash
/opt/kafka/bin/kafka-storage.sh format \
  --config /etc/kafka/server.properties \
  --cluster-id $(/opt/kafka/bin/kafka-storage.sh random-uuid)


systemctl start kafka

journalctl -u kafka.service -f
# Started kafka.service - Apache Kafka (KRaft mode)
```


---

安装一个只有单 broker 节点的集群（也被称为伪集群）

download [http://kafka.apache.org/downloads.html](http://kafka.apache.org/downloads.html)

### kraft

不用 docker 直接启动

```bash
bin/kafka-storage.sh format --config config/kraft/server.properties --cluster-id $(./bin/kafka-storage.sh random-uuid)
bin/kafka-server-start.sh config/kraft/server.properties
```

### kafka docker

```bash
# create volume
docker volume create kafka-config
docker volume create kafka-storage

docker info | grep "Docker Root Dir"

# server.properties 见下文
vim /var/lib/docker/volumes/kafka-config/_data/server.properties
chmod 777 -R /var/lib/docker/volumes/kafka-config
chmod 777 -R /var/lib/docker/volumes/kafka-storage

# 格式化 storage, 先格式化 storage 再启动 kafka
docker run --rm --name kafka \
-e ALLOW_PLAINTEXT_LISTENER=yes \
-v kafka-config:/bitnami/kafka/config \
-v kafka-storage:/data/kafka \
bitnami/kafka:3.6.2 kafka-storage.sh format --config /bitnami/kafka/config/server.properties \
--cluster-id eVW-QkMeS8CeY1Bcuj4S-g --ignore-formatted

docker run -d --name kafka \
-e ALLOW_PLAINTEXT_LISTENER=yes \
-p 9092:9092 \
-v kafka-config:/bitnami/kafka/config \
-v kafka-storage:/dat/kafka \
bitnami/kafka:3.5.2
```

#### kraft podmann

[https://github.com/bitnami/bitnami-docker-kafka/issues/159](https://github.com/bitnami/bitnami-docker-kafka/issues/159)
[https://github.com/bitnami/bitnami-docker-kafka/blob/master/README.md](https://github.com/bitnami/bitnami-docker-kafka/blob/master/README.md)

```bash
# create volume
docker volume create kafka-config

# 查看 volume 目录
docker info | grep "Docker Root Dir"

vim /var/lib/docker/volumes/kafka-config/_data/server.properties

# 格式化storage, 先格式化 storage 再启动 kafka-config
docker run --rm --name kafka \
-e ALLOW_PLAINTEXT_LISTENER=yes \
-p 9092:9092 \
-v kafka-config:/bitnami/kafka/config \
-v kafka-storage:/data/kafka \
bitnami/kafka:3.3.2 kafka-storage.sh format --config /bitnami/kafka/config/server.properties --cluster-id eVW-QkMeS8CeY1Bcuj4S-g --ignore-formatted


docker run -d --name kafka \
-e ALLOW_PLAINTEXT_LISTENER=yes \
-p 9092:9092 \
-v kafka-config:/bitnami/kafka/config \
-v kafka-storage:/data/kafka \
bitnami/kafka:3.4.0

```

##### kafka server.properties

可以复制 kafka_2.13-3.0.0.tgz 里的 config/kraft/server.properties 文件改造一下.

vim /var/lib/containers/storage/volumes/kafka-config/_data/server.properties

- process.roles: 标识该节点所承担的角色，在 KRaft 模式下需要设置这个值
- node.id: 节点的ID，和节点所承担的角色相关联
- controller.quorum.voters: 系统中的所有节点都必须设置 `controller.quorum.voters` 配置。这个配置标识有哪些节点是 Quorum 的投票者节点。所有想成为控制器的节点都需要包含在这个配置里面。这类似于在使用ZooKeeper时，使用ZooKeeper.connect配置时必须包含所有的ZooKeeper服务器。
- advertised.listeners: 对外发布的 listener 地址

```server.properties
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@localhost:9093
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
inter.broker.listener.name=PLAINTEXT
advertised.listeners=PLAINTEXT://10.xxx.xxx.xxx:9092
controller.listener.names=CONTROLLER
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
log.dirs=/data/kafka
num.partitions=1
num.recovery.threads.per.data.dir=1
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000
```

```bash
# 格式化 storage, 先格式化 storage 再启动 kafka
podman run --rm --name kafka \
-e ALLOW_PLAINTEXT_LISTENER=yes \
-p 9092:9092 \
-v kafka-config:/bitnami/kafka/config \
-v kafka-storage:/data/kafka \
bitnami/kafka:3.4.0 kafka-storage.sh format --config /bitnami/kafka/config/server.properties --cluster-id eVW-QkMeS8CeY1Bcuj4S-g --ignore-formatted

# 创建单节点 kafka 容器
podman run -d --name kafka \
-e ALLOW_PLAINTEXT_LISTENER=yes \
-p 9092:9092 \
-v kafka-config:/bitnami/kafka/config \
-v kafka-storage:/data/kafka \
bitnami/kafka:3.4.0
```

### install kafka with zookeeper

[http://blog.wiloon.com/?p=7242](http://blog.wiloon.com/?p=7242)

- docker

```bash
docker run  -d --name kafka \
-p 9092:9092 \
--net docker_net1 \
--ip 192.168.xxx.xxx \
-e KAFKA_BROKER_ID=0 \
-e KAFKA_ZOOKEEPER_CONNECT=192.168.xxx.xxx:2181 \
-e KAFKA_ADVERTISED_HOST_NAME=192.168.xxx.xxx \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.xxx.xxx:9092 \
-e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
-e KAFKA_AUTO_CREATE_TOPICS_ENABLE=false \
-v kafka-data:/kafka \
-t wurstmeister/kafka
```

- podman

```bash
podman run  -d --name kafka \
-p 9092:9092 \
-e KAFKA_BROKER_ID=0 \
-e KAFKA_ZOOKEEPER_CONNECT=zookeeper.wiloon.com:2181 \
-e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
-e KAFKA_ADVERTISED_HOST_NAME=kafka-0 \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka.wiloon.com:9092 \
-e KAFKA_AUTO_CREATE_TOPICS_ENABLE=false \
-v kafka-data:/kafka \
-t wurstmeister/kafka

# kafka 的监听地址
# KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092
# kafka对外发布的连接地址
# KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka.wiloon.com:9092

# docker pull bitnami/kafka:3.0.0

```

### server.properties

advertised.host.name: 是注册到zookeeper,client要访问的broker地址。 (可能producer也是拿这个值,没有验证)

如果advertised.host.name没有设,会用host.name的值注册到zookeeper,如果host.name也没有设,则会使用JVM拿到的本机hostname注册到zk。

这里有两个坑要注意:

如果advertised.host.name没有设,host.name不能设为0.0.0.0,否则client通过zk拿到的broker地址就是0.0.0.0。

如果指定要bind到所有interface,host.name不设就可以。

如果host.name和advertised.host.name都不设,client通过zk拿到的就是JVM返回的本机hostname,如果这个hostname是client无法访问到的,client就会连不上broker。

所以如果要bind到所有interface,client又能访问,解决的办法是host.name不设或设置0.0.0.0,advertised.host.name一定要设置为一个client可以访问的地址,如直接设IP地址。

如果不需要bind到所有interface,也可以只在host.name设置IP地址。

简单的检查broker是否可以被client访问到的办法,就是在zookeeper中看broker信息,上面显示的hostname是否是client可以访问到的地址。

在zkCli中执行get `/brokers/<id>`

### Kafka 访问协议说明

Kafka当前支持四种协议类型的访问: PLAINTEXT、SSL、SASL_PLAINTEXT、SASL_SSL。

Kafka服务启动时,默认会启动PLAINTEXT和SASL_PLAINTEXT两种协议类型的访问监听。可通过设置Kafka服务配置"ssl.mode.enable"为"true",来启动SSL和SASL_SSL两种协议类型的访问监听。

下表是四中协议类型的简单说明:

协议类型

说明

支持的API

默认端口

PLAINTEXT
支持无认证的明文访问
新API和旧API

### kafka manager

```bash
podman run -d --name cmak\
     -p 9000:9000  \
     -e ZK_HOSTS="zookeeper.wiloon.com:2181" \
     hlebalbau/kafka-manager:stable
```

[https://www.jianshu.com/p/25a7b0ceb78a](https://www.jianshu.com/p/25a7b0ceb78a)  
[https://github.com/wurstmeister/kafka-docker](https://github.com/wurstmeister/kafka-docker)  
[https://juejin.im/entry/5cbfe36b6fb9a032036187aa](https://juejin.im/entry/5cbfe36b6fb9a032036187aa)  
[https://my.oschina.net/u/218540/blog/223501](https://my.oschina.net/u/218540/blog/223501)  
[https://www.cnblogs.com/AcAc-t/p/kafka_topic_consumer_group_command.html](https://www.cnblogs.com/AcAc-t/p/kafka_topic_consumer_group_command.html)  
[https://blog.csdn.net/lzufeng/article/details/81743521](https://blog.csdn.net/lzufeng/article/details/81743521)  
[https://www.jianshu.com/p/26495e334613](https://www.jianshu.com/p/26495e334613)  

### kafka producer, consumer api doc

[https://kafka.apache.org/30/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html](https://kafka.apache.org/30/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html)

[https://kafka.apache.org/30/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html](https://kafka.apache.org/30/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html)

## kafka SSL

[https://www.cnblogs.com/huxi2b/p/7427815.html](https://www.cnblogs.com/huxi2b/p/7427815.html)

[https://www.cnblogs.com/huxi2b/p/7427815.html](https://www.cnblogs.com/huxi2b/p/7427815.html)

## 生成 kafka 服务端, 客户端证书, jks

ssl_cafile (str): ca, optional filename of ca file to use in certificate veriication. default: none.
ssl_certfile (str): client certificate, optional filename of file in pem format containing the client certificate, as well as any ca certificates needed to
            establish the certificate's authenticity. default: none.
ssl_keyfile (str): client private key, optional filename containing the client private key. default: none.

```bash
# 生成ca证书
openssl req -new -x509 -keyout ~/tmp/ca-key -out ~/tmp/ca-cert -days 3650 -passout pass:123456 -subj "/C=cn/ST=beijing/L=beijing/O=aspire/OU=aspire/CN=cn0"
# 导入ca证书到 server.truststore.jks
keytool -keystore ~/tmp/server.truststore.jks -alias CARoot -import -file ~/tmp/ca-cert -storepass 123456
```

[https://www.cnblogs.com/tortoise512/articles/16347191.html](https://www.cnblogs.com/tortoise512/articles/16347191.html)

## TLS OOM

