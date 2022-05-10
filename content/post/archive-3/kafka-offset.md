---
title: Kafka, offset
author: "-"
date: 2019-05-13T02:32:29+00:00
url: /?p=14328
categories:
  - Kafka
tags:
  - reprint
---
## Kafka, offset

offset的保存
  
一个消费组消费partition，需要保存offset记录消费到哪，以前保存在zk中，由于zk的写性能不好，以前的解决方法都是consumer每隔一分钟上报一次。这里zk的性能严重影响了消费的速度，而且很容易出现重复消费。
  
在0.10版本后，kafka把这个offset的保存，从zk总剥离，保存在一个名叫__consumeroffsets topic的topic中。写进消息的key由groupid、topic、partition组成，value是偏移量offset。topic配置的清理策略是compact。总是保留最新的key，其余删掉。一般情况下，每个key的offset都是缓存在内存中，查询的时候不用遍历partition，如果没有缓存，第一次就会遍历partition建立缓存，然后查询返回。

作者: 123archu
  
链接: <https://www.jianshu.com/p/d3e963ff8b70>
  
来源: 简书
  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。

<https://blog.csdn.net/u012129558/article/details/80075270>

对Kafka offset的管理，一直没有进行系统的总结，这篇文章对它进行分析。

什么是offset

offset是consumer position，Topic的每个Partition都有各自的offset.

Keeping track of what has been consumed, is, surprisingly, one of the key performance points of a messaging system.

Most messaging systems keep metadata about what messages have been consumed on the broker. That is, as a message is handed out to a consumer, the broker either records that fact locally immediately or it may wait for acknowledgement from the consumer. This is a fairly intuitive choice, and indeed for a single machine server it is not clear where else this state could go. Since the data structure used for storage in many messaging systems scale poorly, this is also a pragmatic choice-since the broker knows what is consumed it can immediately delete it, keeping the data size small.

What is perhaps not obvious, is that getting the broker and consumer to come into agreement about what has been consumed is not a trivial problem. If the broker records a message as consumed immediately every time it is handed out over the network, then if the consumer fails to process the message (say because it crashes or the request times out or whatever) that message will be lost. To solve this problem, many messaging systems add an acknowledgement feature which means that messages are only marked as sent not consumed when they are sent; the broker waits for a specific acknowledgement from the consumer to record the message as consumed. This strategy fixes the problem of losing messages, but creates new problems. First of all, if the consumer processes the message but fails before it can send an acknowledgement then the message will be consumed twice. The second problem is around performance, now the broker must keep multiple states about every single message (first to lock it so it is not given out a second time, and then to mark it as permanently consumed so that it can be removed). Tricky problems must be dealt with, like what to do with messages that are sent but never acknowledged.

Kafka handles this differently. Our topic is divided into a set of totally ordered partitions, each of which is consumed by one consumer at any given time. This means that the position of consumer in each partition is just a single integer, the offset of the next message to consume. This makes the state about what has been consumed very small, just one number for each partition. This state can be periodically checkpointed. This makes the equivalent of message acknowledgements very cheap.

There is a side benefit of this decision. A consumer can deliberately rewind back to an old offset and re-consume data. This violates the common contract of a queue, but turns out to be an essential feature for many consumers. For example, if the consumer code has a bug and is discovered after some messages are consumed, the consumer can re-consume those messages once the bug is fixed.
  
消费者需要自己保留一个offset，从kafka 获取消息时，只拉去当前offset 以后的消息。Kafka 的scala/java 版的client 已经实现了这部分的逻辑，将offset 保存到zookeeper 上

### auto.offset.reset值含义解释

#### earliest

当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，从头开始消费

#### latest

当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，消费新产生的该分区下的数据

#### none

topic各分区都存在已提交的offset时，从offset后开始消费；只要有一个分区不存在已提交的offset，则抛出异常

    auto.commit.enable (例如true，表示offset自动提交到Zookeeper) 
 If true, periodically commit to ZooKeeper the offset of messages already fetched by the consumer. This committed offset will be used when the process fails as the position from which the new consumer will begin
  
    auto.commit.interval.ms(例如60000,每隔1分钟offset提交到Zookeeper)
 The frequency in ms that the consumer offsets are committed to zookeeper.
  
问题: 如果在一个时间间隔内，没有提交offset，岂不是要重复读了？

4. offsets.storage
  
Select where offsets should be stored (zookeeper or kafka).默认是Zookeeper

    基于offset的重复读
 The Kafka consumer works by issuing "fetch" requests to the brokers leading the partitions it wants to consume. The consumer specifies its offset in the log with each request and receives back a chunk of log beginning from that position. The consumer thus has significant control over this position and can rewind it to re-consume data if need be.
  
    Kafka的可靠性保证(消息消费和Offset提交的时机决定了At most once和At least once语义)
  
At Most Once:

At Least Once:

Kafka默认实现了At least once语义

Last Committed Offset：consumer group 最新一次 commit 的 offset，表示这个 group 已经把 Last Committed Offset 之前的数据都消费成功了。
Current Position：consumer group 当前消费数据的 offset，也就是说，Last Committed Offset 到 Current Position 之间的数据已经拉取成功，可能正在处理，但是还未 commit。
Log End Offset(LEO)：记录底层日志 (log) 中的下一条消息的 offset。, 对 producer 来说，就是即将插入下一条消息的 offset。
High Watermark(HW)：已经成功备份到其他 replicas 中的最新一条数据的 offset，也就是说 Log End Offset 与 High Watermark 之间的数据已经写入到该 partition 的 leader 中，但是还未完全备份到其他的 replicas 中，consumer 是无法消费这部分消息 (未提交消息)。

作者: will的猜想
  
来源: CSDN
  
原文: <https://blog.csdn.net/u012129558/article/details/80075270>
  
版权声明: 本文为博主原创文章，转载请附上博文链接！

<https://blog.csdn.net/lishuangzhe7047/article/details/74530417>
