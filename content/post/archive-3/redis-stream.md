---
title: redis stream
author: "-"
date: 2019-08-06T10:43:50+00:00
url: /?p=14772
categories:
  - redis
tags:
  - reprint
---
## redis stream
stream是一个看起来比pubsub可靠多的消息队列。pubsub不靠谱？ 很不靠谱，网络一断或buffer一大就会主动清理数据。stream的设计参考了kafka的消费组模型，redis作者antirez也专门写了篇短文描述了这个过程。

说起新鲜的redis streams，其实Antirez在几年前开了一个新项目叫做disque, 也是用来做消息队列的，奈何没怎么有人关注。我作为antirez的粉丝，肯定是用过了，还tmd改过disque python的库。现在redis5的stream里有一些disque的影子。 更多streams的信息 https://redis.io/topics/streams-intro
    

Redis5.0最近被作者突然放出来了，增加了很多新的特色功能。而Redis5.0最大的新特性就是多出了一个数据结构Stream，它是一个新的强大的支持多播的可持久化的消息队列，作者坦言Redis Stream狠狠地借鉴了Kafka的设计。

Redis Stream 有一个消息链表，将所有加入的消息都串起来，每个消息都有一个唯一的ID和对应的内容。消息是持久化的，Redis重启后，内容还在。

每个Stream都有唯一的名称，它就是Redis的key，在我们首次使用xadd指令追加消息时自动创建。

每个Stream都可以挂多个消费组，每个消费组会有个游标 last_delivered_id 在 Stream 数组之上往前移动，表示当前消费组已经消费到哪条消息了。每个消费组都有一个Stream内唯一的名称，消费组不会自动创建，它需要单独的指令 xgroup create进行创建，需要指定从Stream的某个消息ID开始消费，这个ID用来初始化last_delivered_id变量。

每个消费组(Consumer Group)的状态都是独立的，相互不受影响。也就是说同一份Stream内部的消息会被每个消费组都消费到。

同一个消费组(Consumer Group)可以挂接多个消费者(Consumer)，这些消费者之间是竞争关系，任意一个消费者读取了消息都会使游标last_delivered_id往前移动。每个消费者者有一个组内唯一名称。

消费者(Consumer)内部会有个状态变量pending_ids，它记录了当前已经被客户端读取的消息，但是还没有ack。如果客户端没有ack，这个变量里面的消息ID会越来越多，一旦某个消息被ack，它就开始减少。这个pending_ids变量在Redis官方被称之为PEL，也就是Pending Entries List，这是一个很核心的数据结构，它用来确保客户端至少消费了消息一次，而不会在网络传输的中途丢失了没处理。

    http://xiaorui.cc/2018/06/07/%E6%B5%85%E5%85%A5%E6%B5%85%E5%87%BAredis5-0%E7%9A%84streams%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/
    https://toutiao.io/posts/2agvp3/preview