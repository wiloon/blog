---
title: kafka basic, command
author: "-"
date: 2022-10-11 22:02:39
url: "kafka"
categories:
  - Kafka
tags:
  - remix
  - command
---
## kafka basic, command

### consumer

```bash
bin/kafka-console-consumer.sh --topic topic0 --bootstrap-server 127.0.0.1:9092
# 指定 group
bin/kafka-console-consumer.sh --topic topic0 --bootstrap-server 127.0.0.1:9092 --group group0
# ssl
bin/kafka-console-consumer.sh --topic topic0 --bootstrap-server 127.0.0.1:9092 --consumer.config config.json
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

### kafka package

<https://mirrors.bfsu.edu.cn/apache/kafka/2.6.0/kafka_2.13-2.6.0.tgz>

### group

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

### group detail, offset

```bash
# list group detail, offset
bin/kafka-consumer-groups.sh \
--bootstrap-server 127.0.0.1:9092 \
--describe \
--group group0
```

## offset

CURRENT-OFFSET = LOG-END-OFFSET 说明当前消费组已经全部消费了;

- CURRENT-OFFSET：该分区当前消费到的offset
- LOG-END-OFFSET(LEO)：日志最后的偏移量, 该分区当前latest offset, 记录底层日志 (log) 中的下一条消息的 offset。, 对 producer 来说，就是即将插入下一条消息的 offset。
- LAG：消费滞后区间，为 `LOG-END-OFFSET - CURRENT-OFFSET`，具体大小需要看应用消费速度和生产者速度，一般过大则可能出现消费跟不上，需要引起注意
- CONSUMER-ID：server端给该分区分配的consumer编号
- HOST：消费者所在主机
- CLIENT-ID：消费者id，一般由应用指定

### 命令行手动调整 offset

```bash
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --topic topic0 --to-offset 500000
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --topic topic0 --to-offset 500000 --execute

# 
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --reset-offsets --topic topic0 --shift-by 1

```

## topic

### list topic, 查看 kafka topic 列表, 使用 --list 参数

```bash
# kafka 3.0
bin/kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092
bin/kafka-topics.sh --list --bootstrap-server 192.168.50.169:9092

bin/kafka-topics.sh --list --zookeeper localhost:2181

~/apps/kafka_2.13-3.2.1/bin/kafka-topics.sh --list --bootstrap-server 127.0.0.1:9093 --command-config ~/projects/project0/kafka.config

# kafka.config
security.protocol=SSL
ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=password0
ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=password0
# 是否校验服务端主机名, 默认检验主机名, 值是: https, 赋空值禁用主机名校验
ssl.endpoint.identification.algorithm=
```

#### 可用的配置项

<https://kafka.apache.org/090/documentation.html>

ssl.endpoint.identification.algorithm 默认值问题

<https://docs.confluent.io/platform/current/kafka/authentication_ssl.html>

生成证书 keystore trust store...

<https://www.cnblogs.com/huxi2b/p/7427815.html>

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
topic名中有. 或 _会提示:  WARNING: Due to limitations in metric names, topics with a period ('.') or underscore ('_') could collide. To avoid issues it is best to use either, but not both.

### create topic

```bash
# kafka 3.0.0
# 个人习惯, topic 名字用下划线分隔, 鼠标双击能选中...
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

<https://cloud.tencent.com/developer/article/1436988>

### 调整分区数

kafka topic 可以动态增加分区数。  
注意该命令分区数 partitions 只能增加, 不能减少, --partitions 5: 调整之后的分区数.

```bash
# kafka >3.0
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

### 重置offset

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

# 到kafka/libs 目录下查看kafka包的文件名, where 2.13 is Scala version and 3.1.0 is Kafka version.
kafka_2.13-3.1.0.jar
```

### config kafka server

edit config/server.properties

broker.id=0

listeners=PLAINTEXT://:9092

zookeeper.connect=localhost:2181

## kafka 删除 topic

- 停掉 topic 对应的 producer 和 consumer 或者设置 auto.create.topics.enable = false
- server.properties 设置 delete.topic.enable=true, 1.0.0 版本以后的 kafka 默认是 true, <https://issues.apache.org/jira/browse/KAFKA-5384>
- 删除 topic

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic topic0
./bin/kafka-topics --delete --zookeeper 【zookeeper server:port】 --topic 【topic name】
```

- 删除kafka存储目录

上一步删除 topic之后 kafka 会把对应的 topic 的存储目录改名成 foo-delete, 然后删掉, kafka 2.5 是这样的, 不需要手动删除.

（server.properties文件log.dirs配置，默认为"/data/kafka-logs"）相关topic的数据目录

- 删除 zookeeper 里的数据

kafka 2.5 会自动删除 zk 里的 topic数据, 不需要手动操作.

```bash
./zkCli.sh

ls /brokers/topics/
deleteall /brokers/topics/topic0
```

```bash
#edit bin/kafka-server-start.sh, change memory setting KAFKA_HEAP_OPTS
#start kafka server
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

# 会只消费 N 条数据,如果配合 --from-beginning,就会消费最早 N 条数据。
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

### install

download <http://kafka.apache.org/downloads.html>

#### kraft

```bash
bin/kafka-storage.sh format --config config/kraft/server.properties --cluster-id $(./bin/kafka-storage.sh random-uuid)
bin/kafka-server-start.sh config/kraft/server.properties
```

#### kraft podmann

<https://github.com/bitnami/bitnami-docker-kafka/issues/159>
<https://github.com/bitnami/bitnami-docker-kafka/blob/master/README.md>

##### create volume

```bash
podman volume create kafka-config
```

##### server.properies

可以复制 kafka_2.13-3.0.0.tgz 里的 config/kraft/server.properties 文件改造一下.

vim /var/lib/containers/storage/volumes/kafka-config/_data/server.properties

```bash
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@localhost:9093
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
inter.broker.listener.name=PLAINTEXT
advertised.listeners=PLAINTEXT://192.168.50.169:9092
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
# 格式化storage, 先格式化 storage 再启动 kafka
podman run --rm --name kafka \
-e ALLOW_PLAINTEXT_LISTENER=yes \
-p 9092:9092 \
-v kafka-config:/bitnami/kafka/config \
-v kafka-storage:/data/kafka \
bitnami/kafka:3.2 kafka-storage.sh format --config /bitnami/kafka/config/server.properties --cluster-id eVW-QkMeS8CeY1Bcuj4S-g --ignore-formatted

# 创建单节点 kafka 容器
podman run -d --name kafka \
-e ALLOW_PLAINTEXT_LISTENER=yes \
-p 9092:9092 \
-v kafka-config:/bitnami/kafka/config \
-v kafka-storage:/data/kafka \
bitnami/kafka:3.2
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

<https://www.jianshu.com/p/25a7b0ceb78a>  
<https://github.com/wurstmeister/kafka-docker>  
<https://juejin.im/entry/5cbfe36b6fb9a032036187aa>  
<https://my.oschina.net/u/218540/blog/223501>  
<https://www.cnblogs.com/AcAc-t/p/kafka_topic_consumer_group_command.html>  
<https://blog.csdn.net/lzufeng/article/details/81743521>  
><https://www.jianshu.com/p/26495e334613>

### kafka producer, consumer api doc

<https://kafka.apache.org/30/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html>

<https://kafka.apache.org/30/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html>

## kafka SSL

<https://www.cnblogs.com/huxi2b/p/7427815.html>

<https://www.cnblogs.com/huxi2b/p/7427815.html>

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

<https://www.cnblogs.com/tortoise512/articles/16347191.html>
