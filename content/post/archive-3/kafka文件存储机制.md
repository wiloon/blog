---
title: Kafka 文件存储机制
author: "-"
date: 2019-05-10T06:51:16+00:00
url: /?p=14317
categories:
  - Kafka
tags:
  - reprint
---
## Kafka 文件存储机制

Kafka 是什么
  
Kafka 是最初由Linkedin公司开发，是一个分布式、分区的、多副本的、多订阅者，基于zookeeper协调的分布式日志系统(也可以当做MQ系统)，常见可以用于web/nginx日志、访问日志，消息服务等等，Linkedin于2010年贡献给了Apache基金会并成为顶级开源项目。

1.前言
  
一个商业化消息队列的性能好坏，其文件存储机制设计是衡量一个消息队列服务技术水平和最关键指标之一。
  
下面将从Kafka文件存储机制和物理结构角度，分析Kafka是如何实现高效文件存储，及实际应用效果。

2.Kafka文件存储机制
  
Kafka部分名词解释如下:

Broker: 消息中间件处理结点，一个Kafka节点就是一个broker，多个broker可以组成一个Kafka集群。
  
Topic: 一类消息，例如page view日志、click日志等都可以以topic的形式存在，Kafka集群能够同时负责多个topic的分发。
  
Partition: topic物理上的分组，一个topic可以分为多个partition，每个partition是一个有序的队列。
  
Segment: partition物理上由多个segment组成，下面2.2和2.3有详细说明。
  
offset: 每个partition都由一系列有序的、不可变的消息组成，这些消息被连续的追加到partition中。partition中的每个消息都有一个连续的序列号叫做offset,用于partition唯一标识一条消息.
  
分析过程分为以下4个步骤:

topic中partition存储分布
  
partiton中文件存储方式
  
partiton中segment文件存储结构
  
在partition中如何通过offset查找message
  
通过上述4过程详细分析，我们就可以清楚认识到kafka文件存储机制的奥秘。

2.1 topic中partition存储分布
  
假设实验环境中Kafka集群只有一个broker，xxx/message-folder为数据文件存储根目录，在Kafka broker中server.properties文件配置(参数log.dirs=xxx/message-folder)，例如创建2个topic名称分别为report_push、launch_info, partitions数量都为partitions=4
  
存储路径和目录规则为:

复制代码
  
xxx/message-folder

              |--report_push-0
              |--report_push-1
              |--report_push-2
              |--report_push-3
              |--launch_info-0
              |--launch_info-1
              |--launch_info-2
              |--launch_info-3

复制代码

在Kafka文件存储中，同一个topic下有多个不同partition，每个partition为一个目录，partiton命名规则为topic名称+有序序号，第一个partiton序号从0开始，序号最大值为partitions数量减1。
  
如果是多broker分布情况，请参考kafka集群partition分布原理分析

2.2 partiton中文件存储方式
  
下面示意图形象说明了partition中文件存储方式:
  
image

                              图1

每个partion(目录)相当于一个巨型文件被平均分配到多个大小相等segment(段)数据文件中。但每个段segment file消息数量不一定相等，这种特性方便old segment file快速被删除。
  
每个partiton只需要支持顺序读写就行了，segment文件生命周期由服务端配置参数决定。
  
这样做的好处就是能快速删除无用文件，有效提高磁盘利用率。

2.3 partiton中segment文件存储结构
  
读者从2.2节了解到Kafka文件系统partition存储方式，本节深入分析partion中segment file组成和物理结构。

segment file组成: 由2大部分组成，分别为index file和data file，此2个文件一一对应，成对出现，后缀".index"和".log"分别表示为segment索引文件、数据文件.
  
segment文件命名规则: partion全局的第一个segment从0开始，后续每个segment文件名为上一个segment文件最后一条消息的offset值。数值最大为64位long大小，19位数字字符长度，没有数字用0填充。
  
下面文件列表是笔者在Kafka broker上做的一个实验，创建一个topicXXX包含1 partition，设置每个segment大小为500MB,并启动producer向Kafka broker写入大量数据,如下图2所示segment文件列表形象说明了上述2个规则:
  
image

            图2

以上述图2中一对segment file文件为例，说明segment中index<—->data file对应关系物理结构如下:
  
image

            图3

上述图3中索引文件存储大量元数据，数据文件存储大量消息，索引文件中元数据指向对应数据文件中message的物理偏移地址。
  
其中以索引文件中元数据3,497为例，依次在数据文件中表示第3个message(在全局partiton表示第368772个message)、以及该消息的物理偏移地址为497。

从上述图3了解到segment data file由许多message组成，下面详细说明message物理结构如下:
  
image

           图4

参数说明:
  
关键字 解释说明
  
8 byte offset 在parition(分区)内的每条消息都有一个有序的id号，这个id号被称为偏移(offset),它可以唯一确定每条消息在parition(分区)内的位置。即offset表示partiion的第多少message
  
4 byte message size message大小
  
4 byte CRC32 用crc32校验message
  
1 byte "magic" 表示本次发布Kafka服务程序协议版本号
  
1 byte "attributes" 表示为独立版本、或标识压缩类型、或编码类型。
  
4 byte key length 表示key的长度,当key为-1时，K byte key字段不填
  
K byte key 可选
  
value bytes payload 表示实际消息数据。
  
2.4 在partition中如何通过offset查找message
  
例如读取offset=368776的message，需要通过下面2个步骤查找。

第一步查找segment file
  
上述图2为例，其中00000000000000000000.index表示最开始的文件，起始偏移量(offset)为0.第二个文件00000000000000368769.index的消息量起始偏移量为368770 = 368769 + 1.同样，第三个文件00000000000000737337.index的起始偏移量为737338=737337 + 1，其他后续文件依次类推，以起始偏移量命名并排序这些文件，只要根据offset **二分查找**文件列表，就可以快速定位到具体文件。
  
当offset=368776时定位到00000000000000368769.index|log

第二步通过segment file查找message
  
通过第一步定位到segment file，当offset=368776时，依次定位到00000000000000368769.index的元数据物理位置和00000000000000368769.log的物理偏移地址，然后再通过00000000000000368769.log顺序查找直到offset=368776为止。

从上述图3可知这样做的优点，segment index file采取稀疏索引存储方式，它减少索引文件大小，通过mmap可以直接内存操作，稀疏索引为数据文件的每个对应message设置一个元数据指针,它比稠密索引节省了更多的存储空间，但查找起来需要消耗更多的时间。

3 Kafka文件存储机制–实际运行效果
  
实验环境:

Kafka集群: 由2台虚拟机组成
  
cpu: 4核
  
物理内存: 8GB
  
网卡: 千兆网卡
  
jvm heap: 4GB
  
详细Kafka服务端配置及其优化请参考: kafka server.properties配置详解
  
image

                              图5                                 

从上述图5可以看出，Kafka运行时很少有大量读磁盘的操作，主要是定期批量写磁盘操作，因此操作磁盘很高效。这跟Kafka文件存储中读写message的设计是息息相关的。Kafka中读写message有如下特点:

写message

消息从java堆转入page cache(即物理内存)。
  
由异步线程刷盘,消息从page cache刷入磁盘。
  
读message

消息直接从page cache转入socket发送出去。
  
当从page cache没有找到相应数据时，此时会产生磁盘IO,从磁
  
盘Load消息到page cache,然后直接从socket发出去
  
4.offset存储方式
  
1. 在kafka 0.9版本之后，kafka为了降低zookeeper的io读写，减少network data transfer，也自己实现了在kafka server上存储consumer，topic，partitions，offset信息将消费的 offset 迁入到了 Kafka 一个名为 __consumer_offsets 的Topic中。
  
2. 将消费的 offset 存放在 Zookeeper 集群中。
  
3. 将offset存放至第三方存储，如Redis, 为了严格实现不重复消费
  
下面分别说一下这三种存储方式的实现

4.1 __consumer_offsets [kafka]
  
下面的代码案例实现了test这一topic的数据连续消费

复制代码
  
from kafka import KafkaConsumer

class KafkaStreamTest:

"'

This class consume all external Kafka topics"'

    def __init__(self):
    
        self.appName = "kafkatest"
    
        self.kafkaHosts = "192.168.4.201:6667,192.168.4.231:6667"
        self.kafkaAutoOffsetReset = "largest"
        self._kafka_topic = "test"
    
    def start(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
        elogging.debug(self.appName, elogging.normalCID(), "receiver starting")
        consumer = KafkaConsumer('test',  bootstrap_servers=['192.168.4.201:6667','192.168.4.231:6667'], enable_auto_commit=True, auto_offset_reset='earliest')
        #consumer = KafkaConsumer('test', bootstrap_servers=['192.168.4.201:6667', '192.168.4.231:6667'], auto_offset_reset='earliest')
        while True:
            # The definition of KafkaMessage:
            # KafkaMessage = namedtuple("KafkaMessage",
            #     ["topic", "partition", "offset", "key", "value"])
            kafkaMsg = consumer.next()
    
            # for debug
            print kafkaMsg.topic, kafkaMsg.partition, kafkaMsg.offset, kafkaMsg.key, kafkaMsg.value

if **name** =="**main**":

test = KafkaStreamTest()

test.start()
  
enable_auto_commit (bool) – If True , the consumer's offset will be periodically committed in the background. Default: True设置为true，表示offset自动托管到kafka内部的一个特定名称为__consumer_offsets的topic

auto_offset_reset: What to do when there is no initial offset in Kafka or if the current offset does not exist any more on the server (e.g. because that data has been deleted):

earliest: automatically reset the offset to the earliest offset
  
latest: automatically reset the offset to the latest offset
  
只有当offset不存在的时候，才用latest或者earliest

其他详细内容请参看

[https://github.com/dpkp/kafka-python](https://github.com/dpkp/kafka-python)

[https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html)

[https://stackoverflow.com/questions/35432326/how-to-get-latest-offset-for-a-partition-for-a-kafka-topic](https://stackoverflow.com/questions/35432326/how-to-get-latest-offset-for-a-partition-for-a-kafka-topic)

Kafka 如何读取offset topic内容 (__consumer_offsets)
  
kafka 0.9.0.0 __consumer_offsets日志清理问题？

Kafka 0.10.2

4.2 zookeeper
  
请参考

spark createDirectStream保存kafka offset

修改kafka topic的offset几种方法

4.3 Redis[推荐]
  
import os
  
import sys
  
sys.path.append("..")
  
sys.path.append(sys.argv[0][:sys.argv[0].rfind(os.path.join('com','ericsson'))])

import copy
  
import traceback
  
import redis
  
from pyspark import SparkContext, SparkConf
  
from pyspark.streaming import StreamingContext, DStream
  
from pyspark.sql import SQLContext
  
import simplejson as json
  
from com.ericsson.analytics.fms.common.common import ELogForDistributedApp,getSqlContextInstance
  
from pyspark.streaming.kafka import KafkaUtils,TopicAndPartition
  
from com.ericsson.analytics.oamf.client.logging import elogging
  
from com.ericsson.analytics.fms.common.common import HDFSOperation

class KafkaStreamTest:

"'

This class consume all external Kafka topics, store the data into Parquet and send the data to internal Kafka topics

"'

    def __init__(self):
    
        self.appName = "kafkatest"
    
        self.kafkaHosts = "192.168.4.201:6667,192.168.4.231:6667"
        self.kafkaAutoOffsetReset = "largest"
        self.kafka_offset_redis_db = 6
        self._kafka_topic = "test"
        self.redisHost = "192.168.4.231"
        self.redisPort = 6379
    
        self.spark_batch_duration = 20
    
    def createStreamingContext(self, sc):
        ssc = StreamingContext(sc, self.spark_batch_duration)
        ds = self.getDStreamFromKafka(ssc)
        if ds is not None:
            elogging.info(self.appName, elogging.normalCID(), "Kafka succeeded to getting the data")
            return ssc, ds
        else:
            return None, None
    
    def getDStreamFromKafka(self, ssc):
        kafkaParams = {"metadata.broker.list": self.kafkaHosts}
        elogging.debug(self.appName, elogging.normalCID(), kafkaParams)
    
        sc = ssc.sparkContext
        dstream = None
        try:
            redisConn = self.getRedisConnection(self.kafka_offset_redis_db)
            if redisConn.exists(self.appName):
                elogging.debug(self.appName, elogging.normalCID(), "key " + self.appName + " exists in redis")
                fromOffset = {}
                offsetListStr = redisConn.get(self.appName)
                offsetList = eval(offsetListStr)
                for offset in offsetList:
                    elogging.debug(self.appName, elogging.normalCID(), str(offset))
                    topicPartion = TopicAndPartition(offset["topic"], offset["partition"])
                    fromOffset[topicPartion] = offset["untilOffset"]
                dstream = KafkaUtils.createDirectStream(ssc, [self._kafka_topic], kafkaParams, fromOffset)
            else:
                kafkaParams = {"metadata.broker.list": self.kafkaHosts, "auto.offset.reset": self.kafkaAutoOffsetReset}
                elogging.debug(self.appName, elogging.normalCID(), "key " + self.appName + " doesn't exist in redis")
                dstream = KafkaUtils.createDirectStream(ssc, [self._kafka_topic], kafkaParams)
        except:
            traceInfo = traceback.format_exc()
            elogging.error(self.appName, elogging.faultCID(), "failed to create DStream : " + traceInfo)
    
        return dstream
    
    def getRedisConnection(self, redisDB):
        try:
            pool = redis.ConnectionPool(host=self.redisHost, port=self.redisPort, db=redisDB)
            redisConn = redis.Redis(connection_pool=pool)
        except:
            traceInfo = traceback.format_exc()
            elogging.error(self.appName, elogging.faultCID(), "failed to create DStream : " + traceInfo)
            return None
    
        return redisConn
    
    def getOffSetRangesFromRDD(self, rdd):
        try:
            offsetRanges = rdd.offsetRanges()
        except:
            traceInfo = traceback.format_exc()
            elogging.error(self.appName, elogging.faultCID(), "failed to call rdd.offsetRanges() function : " + traceInfo)
            return None
    
        offsetList = []
        for offset in offsetRanges:
            offsetList.append({"topic": offset.topic, "partition": offset.partition, "fromOffset": offset.fromOffset,
                               "untilOffset": offset.untilOffset})
    
        elogging.info(self.appName, elogging.normalCID(), "getOffSetRangesFromRDD, offsetList: " + str(offsetList))
        return offsetList
    
    def saveOffSetRangesToRedis(self, offsetList):
        redisConn = self.getRedisConnection(self.kafka_offset_redis_db)
        if redisConn is not None:
            redisConn.set(self.appName, offsetList)
            elogging.info(self.appName, elogging.normalCID(), "saveOffSetRangesToRedis, offsetList : " + str(offsetList))
    
    def handleMessages(self, runTime, rdd):
        elogging.debug(self.appName, elogging.normalCID(), "========= %s =========" % str(runTime))
        offsetList = self.getOffSetRangesFromRDD(rdd)
        if offsetList is not None:
            self.saveOffSetRangesToRedis(offsetList)
    
        rddFilter = rdd.map(lambda p: p[1])
    
        counts = rddFilter.flatMap(lambda line: line.split(" ")) \
            .map(lambda word: (word, 1)) \
            .reduceByKey(lambda a, b: a + b)
        sqlContext = getSqlContextInstance(rddFilter.context)
        if counts is not None:
            df = sqlContext.createDataFrame(counts)
            df.show()
    
    def start(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        sc = SparkContext(appName=self.appName)
        eloggingConfig = None
        try:
            eloggingConfig = HDFSOperation.getConfigFromHDFS(ELogForDistributedApp.LOGHDFSPATH, sc)
            elogging.initLogFromDict(eloggingConfig)
        except StandardError, se:
            pass
    
        elogging.debug(self.appName, elogging.normalCID(), "receiver starting")
        configInfoStr = 'kafkaHosts:' + str(self.kafkaHosts) + ', kafkaAutoOffsetReset:' + str(self.kafkaAutoOffsetReset) + \
                        ', kafka_offset_redis_db:' + str(self.kafka_offset_redis_db) + ', spark_batch_duration:' + str(self.spark_batch_duration) + \
                        ', redisHost:' + str(self.redisHost) + ', redisPort:' + str(self.redisPort)
        elogging.info(self.appName, elogging.normalCID(), configInfoStr)
        ssc, newDS = self.createStreamingContext(sc)
        if newDS is not None:
            newDS.foreachRDD(self.handleMessages)
            ssc.start()
            elogging.debug(self.appName, elogging.normalCID(), "StreamingContext start")
            ssc.awaitTermination()
            elogging.debug(self.appName, elogging.normalCID(), "receiver end")
        else:
            traceInfo = traceback.format_exc()
            elogging.error(self.appName, elogging.faultCID(), "Failed to create DStream " + traceInfo)

if **name** =="**main**":

test = KafkaStreamTest()

test.start()

5.总结
  
Kafka高效文件存储设计特点

Kafka把topic中一个parition大文件分成多个小文件段，通过多个小文件段，就容易定期清除或删除已经消费完文件，减少磁盘占用。
  
通过索引信息可以快速定位message和确定response的最大大小。
  
通过index元数据全部映射到memory，可以避免segment file的IO磁盘操作。
  
通过索引文件稀疏存储，可以大幅降低index文件元数据占用空间大小。
  
参考
  
1.Linux Page Cache机制
  
2.Kafka官方文档
  
3.Kafka Offset Storage

[https://www.cnblogs.com/ITtangtang/p/8027217.html](https://www.cnblogs.com/ITtangtang/p/8027217.html)
  
[https://tech.meituan.com/2015/01/13/kafka-fs-design-theory.html](https://tech.meituan.com/2015/01/13/kafka-fs-design-theory.html)
