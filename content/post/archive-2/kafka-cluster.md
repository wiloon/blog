---
title: kafka cluster
author: "-"
date: 2018-05-07T04:16:07+00:00
url: kafka/cluster
categories:
  - Kafka
tags:
  - reprint
---

## kafka cluster

version: 3.0.0

```bash
# net
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

podman run -d --name kafka1 \
  -e ALLOW_PLAINTEXT_LISTENER=yes \
  -e KAFKA_CFG_ZOOKEEPER_CONNECT=192.168.50.169:2181 \
  -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://192.168.50.169:9092 \
  -p 9092:9092 \
  bitnami/kafka:3.2.0

podman run -d --name kafka2 \
  -e ALLOW_PLAINTEXT_LISTENER=yes \
  -e KAFKA_CFG_ZOOKEEPER_CONNECT=192.168.50.169:2181 \
  -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://192.168.50.169:9093 \
  -p 9093:9092 \
  bitnami/kafka:3.2.0

podman run -d --name kafka3 \
  -e ALLOW_PLAINTEXT_LISTENER=yes \
  -e KAFKA_CFG_ZOOKEEPER_CONNECT=192.168.50.169:2181 \
  -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://192.168.50.169:9094 \
  -p 9094:9092 \
  bitnami/kafka:3.2.0
```

[https://github.com/bitnami/bitnami-docker-kafka/blob/master/README.md](https://github.com/bitnami/bitnami-docker-kafka/blob/master/README.md)

[https://blog.csdn.net/isea533/article/details/73727485](https://blog.csdn.net/isea533/article/details/73727485)
  
[https://my.oschina.net/sniperLi/blog/741565](https://my.oschina.net/sniperLi/blog/741565)
  
[https://gist.github.com/vipmax/9ceeaa02932ba276fa810c923dbcbd4f](https://gist.github.com/vipmax/9ceeaa02932ba276fa810c923dbcbd4f)
  
[https://blog.csdn.net/cysdxy/article/details/52337364](https://blog.csdn.net/cysdxy/article/details/52337364)
