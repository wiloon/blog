---
title: kafka config, server, producer
author: "-"
date: 2017-05-04T09:27:25+00:00
url: /?p=10207
categories:
  - Kafka
tags:
  - reprint
---
## kafka config, server, producer

大体上来说,用户首先构建待发送的消息对象ProducerRecord,然后调用KafkaProducer#send方法进行发送。KafkaProducer接收到消息后首先对其进行序列化,然后结合本地缓存的元数据信息一起发送给partitioner去确定目标分区,最后追加写入到内存中的消息缓冲池(accumulator)。此时KafkaProducer#send方法成功返回。

KafkaProducer中还有一个专门的Sender IO线程负责将缓冲池中的消息分批次发送给对应的broker,完成真正的消息发送逻辑。

基本设计特点
  
结合源代码,笔者认为新版本的producer从设计上来说具有以下几个特点(或者说是优势):

总共创建两个线程: 执行KafkaPrducer#send逻辑的线程——我们称之为"用户主线程"；执行发送逻辑的IO线程——我们称之为"Sender线程"
  
不同于Scala老版本的producer,新版本producer完全异步发送消息,并提供了回调机制(callback)供用户判断消息是否成功发送
  
batching机制——"分批发送"机制。每个批次(batch)中包含了若干个PRODUCE请求,因此具有更高的吞吐量
  
更加合理的默认分区策略: 对于无key消息而言,Scala版本分区策略是一段时间内(默认是10分钟)将消息发往固定的目标分区,这容易造成消息分布的不均匀,而新版本的producer采用轮询的方式均匀地将消息分发到不同的分区
  
底层统一使用基于Selector的网络客户端实现,结合Java提供的Future实现完整地提供了更加健壮和优雅的生命周期管理。

其实,新版本producer的设计优势还有很多,诸如监控指标更加完善等这样的就不一一细说了。总之,新版本producer更加地健壮,性能更好~

```java
properties props = new Properties();
 props.put("bootstrap.servers", "localhost:9092");
 props.put("acks", "all");
 props.put("retries", 0);
 props.put("batch.size", 16384);
 props.put("linger.ms", 1);
 props.put("buffer.memory", 33554432);
 props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
 props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

 Producer<String, String> producer = new KafkaProducer<>(props);
 for(int i = 0; i < 100; i++)
     producer.send(new ProducerRecord<String, String>("my-topic", Integer.toString(i), Integer.toString(i)));

 producer.close();
```

### bootstrap.servers

配置kafka 查询集群 metadata 服务的地址, 建立连接时,kafa producer向 bootstrap.servers 发 metadata 请求, 从 返回 的metadata response里得到kafka 集群的地址,再建立连接

### batch.size

单位: 字节
batch.size是 producer 批量发送的基本单位,默认是 16384 Bytes, 即16kB

发往每个分区 (Partition) 的消息缓存量 (消息内容的字节数之和,不是条数) 。达到设置的数值时,就会触发一次网络请求,然后Producer客户端把消息批量发往服务器。

#### linger.ms

单位: 毫秒
lingger.ms是sender线程在检查batch是否ready时候,判断有没有过期的参数,默认大小是0ms
producer会等待 buffer 的 messages 数目达到指定值或时间超过 x 毫秒, 才发送数据。减少网络 IO, 节省带宽之用。原理就是把原本需要多次发送的小 batch, 通过引入延时的方式合并成大 batch 发送,减少了网络传输的压力, 从而提升吞吐量。当然, 也会引入延时.

那么producer是按照batch.size大小批量发送消息呢,还是按照linger.ms的时间间隔批量发送消息呢？这里先说结论: 其实满足batch.size和ling.ms之一,producer便开始发送消息。

一个Batch被创建之后,最多过多久,不管这个Batch有没有写满,都必须发送出去了。

比如说batch.size是16KB,但是现在某个低峰时间段,发送消息量很小。这会导致可能Batch被创建之后,有消息进来,但是迟迟无法凑够16KB,难道此时就一直等着吗？

当然不是,假设设置“linger.ms”是50ms,那么只要这个Batch从创建开始到现在已经过了50ms了,哪怕他还没满16KB,也会被发送出去。

所以“linger.ms”决定了消息一旦写入一个Batch,最多等待这么多时间,他一定会跟着Batch一起发送出去。

linger.ms配合batch.size一起来设置,可避免一个Batch迟迟凑不满,导致消息一直积压在内存里发送不出去的情况。

### buffer.memory 缓冲区大小

Kafka的客户端发送数据到服务器,不是来一条就发一条,而是经过缓冲的,也就是说,通过KafkaProducer发送出去的消息都是先进入到客户端本地的内存缓冲里,然后把很多消息收集成一个一个的Batch,再发送到Broker上去的,这样性能才可能高。

buffer.memory的本质就是用来约束KafkaProducer能够使用的内存缓冲的大小的,默认值32MB。

如果buffer.memory设置的太小,可能导致的问题是: 消息快速的写入内存缓冲里,但Sender线程来不及把Request发送到Kafka服务器,会造成内存缓冲很快就被写满。而一旦被写满,就会阻塞用户线程,不让继续往Kafka写消息了。

所以“buffer.memory”参数需要结合实际业务情况压测,需要测算在生产环境中用户线程会以每秒多少消息的频率来写入内存缓冲。经过压测,调试出来一个合理值。

#### buffer.memory与batch.size的区别

batch.size Kafka producers attempt to collect sent messages into
batches to improve throughput. With the Java client, you can use
batch.size to control the maximum size in bytes of each message batch.

buffer.memory Use buffer.memory to limit the total memory that is
available to the Java client for collecting unsent messages. When this
limit is hit, the producer will block on additional sends for as long
as max.block.ms before raising an exception.
————————————————
版权声明: 本文为CSDN博主「鸭梨山大哎」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/u010711495/article/details/113250402>

### max.block.ms

buffer.memory 写满之后x毫秒抛异常 TimeoutException

配置控制了KafkaProducer.send () 和KafkaProducer.partitionsFor () 的阻塞时间,这些方法可以由于缓冲区已满或元数据不可用而被阻塞,用户提供的序列化器或分区器中的阻塞将不计入此超时时间 。

The buffer.memory controls the total amount of memory available to the producer for buffering. If records are sent faster than they can be transmitted to the server then this buffer space will be exhausted. When the buffer space is exhausted additional send calls will block. The threshold for time to block is determined by max.block.ms after which it throws a TimeoutException.

buffer.memory设置决定了Producer缓存区整个可用的内存。如果记录记录发送速度总是比推送到集群速度快,那么缓存区将被耗尽。当缓存区资源耗尽,消息发送send方法调用将被阻塞,阻塞的时间由max.block.ms设定,阻塞超过限定时间会抛出TimeoutException异常。

默认值:  33554432 (32MB)

二、max.block.ms 参数
The configuration controls how long KafkaProducer.send() and KafkaProducer.partitionsFor() will block.These methods can be blocked either because the buffer is full or metadata unavailable.

Blocking in the user-supplied serializers or partitioner will not be counted against this timeout.

max.block.ms 参数决定KafkaProducer.send() 和 KafkaProducer.partitionsFor() 方法被阻塞的时间。当缓存区满了或者元数据不可用的时间将产生阻塞。用户提供的序列化器或分区器中的阻塞将不计入此超时。

#### acks

关乎到消息持久性(durability)的一个参数。高吞吐量和高持久性很多时候是相矛盾的,需要先明确我们的目标是什么？ 高吞吐量？高持久性？亦或是中等？因此该参数也有对应的三个取值: 0, -1和1

acks用来控制一个produce请求怎样才能算完成,准确的说,是有多少broker必须已经提交数据到log文件,并向leader发送ack,可以设置如下的值:
  
- 0, 意味着producer永远不会等待一个来自broker的ack继续发送下一条 (批) 消息。,这就是0.7版本的行为。这个选项提供了最低的延迟,但是持久化的保证是最弱的,当server挂掉的时候会丢失一些数据。
- 1, 意味着在leader replica已经接收到数据后,producer会得到一个ack。这个选项提供了更好的持久性,因为在server确认请求成功处理后,client才会返回。如果刚写到leader上,还没来得及复制leader就挂了,那么消息才可能会丢失。
- -1 ("all"),意味着在所有的ISR都接收到数据后,producer才得到一个ack。这个选项提供了最好的持久性,只要还有一个replica存活,那么数据就不会丢失。

#### compression.type

producer所使用的压缩器,目前支持gzip, snappy和lz4。压缩是在用户主线程完成的,通常都需要花费大量的CPU时间,但对于减少网络IO来说确实利器。生产环境中可以结合压力测试进行适当配置

#### retries

重试机制,对于瞬时失败的消息发送,开启重试后KafkaProducer会尝试再次发送消息。对于有强烈无消息丢失需求的用户来说,开启重试机制是必选项。
  
### max.in.flight.requests.per.connection

关乎消息乱序的一个配置参数。它指定了Sender线程在单个Socket连接上能够发送未应答PRODUCE请求的最大请求数。适当增加此值通常会增大吞吐量,从而整体上提升producer的性能。不过笔者始终觉得其效果不如调节batch.size来得明显,所以请谨慎使用。另外如果开启了重试机制,配置该参数大于1可能造成消息发送的乱序(先发送A,然后发送B,但B却先行被broker接收)

### kafka server config
<https://stackoverflow.com/questions/53039752/kafka-how-to-calculate-the-value-of-log-retention-byte>

### max.request.size

The maximum size of a request in bytes. This setting will limit the number of record batches the producer will send in a single request to avoid sending huge requests. This is also effectively a cap on the maximum uncompressed record batch size. Note that the server has its own cap on the record batch size (after compression if compression is enabled) which may be different from this.

Type:    int
Default:    1048576
Valid Values:    [0,...]
Importance:    medium

## kafka server, topic config

### max.message.bytes

max.message.bytes 参数校验的是批次大小,而不是消息大小。

### broker

#### message.max.bytes

Kafka 允许的最大 record batch size,什么是 record batch size ？简单来说就是 Kafka 的消息集合批次,一个批次当中会包含多条消息,生产者中有个参数 batch.size,指的是生产者可以进行消息批次发送,提高吞吐量
以上源码可以看出 message.max.bytes 并不是限制消息体大小的,而是限制一个批次的消息大小,所以我们需要注意生产端对于 batch.size 的参数设置需要小于 message.max.bytes。

### request.timeout.ms

默认值:  30秒  
这个参数容易和上面的max.block.ms 参数相混淆,这里也一同说明一下。

生产者producer发送消息后等待响应的最大时间,如果在配置时间内没有得到响应,生产者会重试。

Step 1:  序列化+计算目标分区
  
这是KafkaProducer#send逻辑的第一步,即为待发送消息进行序列化并计算目标分区

Step 2: 追加写入消息缓冲区(accumulator)
  
producer 创建时会创建一个默认32MB(由buffer.memory参数指定)的accumulator缓冲区,专门保存待发送的消息。除了之前在"关键参数"段落中提到的linger.ms和batch.size等参数之外,该数据结构中还包含了一个特别重要的集合信息: 消息批次信息(batches)。该集合本质上是一个HashMap,里面分别保存了每个topic分区下的batch队列,即前面说的批次是按照topic分区进行分组的。这样发往不同分区的消息保存在对应分区下的batch队列中。举个简单的例子,假设消息M1, M2被发送到test的0分区但属于不同的batch,M3分送到test的1分区,那么batches中包含的信息就是: {"test-0" -> [batch1, batch2], "test-1" -> [batch3]}

单个topic分区下的batch队列中保存的是若干个消息批次。每个batch中最重要的3个组件包括:

compressor: 负责执行追加写入操作
  
batch缓冲区: 由batch.size参数控制,消息被真正追加写入到的地方
  
thunks: 保存消息回调逻辑的集合
  
这一步的目的就是将待发送的消息写入消息缓冲池中

        //当所有 broker 全部挂掉的时候,此时 send 的方法会 block 住60秒(max.block.ms参数控制),但并不抛出异常,因此failover策略失效。
        //block 在 KafkaProducer.doSend() 中的 long waitedOnMetadataMs = waitOnMetadata(record.topic(), this.maxBlockTimeMs);
        //如果项目启动并且取得 waitOnMetaData 之后全部broker再挂掉的话,不会block应用

---

<https://zhuanlan.zhihu.com/p/142139663>
<http://www.cnblogs.com/huxi2b/p/6364613.html>
  
<http://blog.csdn.net/itleochen/article/details/18352797>
  
<http://www.cnblogs.com/huxi2b/p/6637425.html>
  
<http://apache.mirrors.tds.net/kafka/0.10.2.1/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html>
