---
title: kafka cluster
author: wiloon
type: post
date: 2018-05-07T04:16:07+00:00
url: /?p=12190
categories:
  - Uncategorized

---
### download kafka

https://kafka.apache.org/downloads

### commands

<https://blog.wiloon.com/wp-admin/post.php?post=12205&action=edit>

config file:

# The id of the broker. This must be set to a unique integer for each broker.

broker.id=0

# 最好配内网dns, test-kafka-1

listeners=PLAINTEXT://test-kafka-1:9092

log.dirs=/data/logs/kafka-logs
  
zookeeper.connect=test-zookeeper-1:2181,test-zookeeper-2:2181,test-zookeeper-3:2181

replication策略是基于partition。kafka通过创建topic时可以通过 replication-factor配置partition副本数。配置副本之后, 每个partition都有一个唯一的leader，有0个或多个follower。

install kafka manager
  
https://blog.csdn.net/isea533/article/details/73727485
  
https://my.oschina.net/sniperLi/blog/741565
  
https://gist.github.com/vipmax/9ceeaa02932ba276fa810c923dbcbd4f
  
https://blog.csdn.net/cysdxy/article/details/52337364