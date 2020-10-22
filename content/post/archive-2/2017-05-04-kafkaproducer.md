---
title: kafka config, server, producer
author: wiloon
type: post
date: 2017-05-04T09:27:25+00:00
url: /?p=10207
categories:
  - Uncategorized

---
大体上来说，用户首先构建待发送的消息对象ProducerRecord，然后调用KafkaProducer#send方法进行发送。KafkaProducer接收到消息后首先对其进行序列化，然后结合本地缓存的元数据信息一起发送给partitioner去确定目标分区，最后追加写入到内存中的消息缓冲池(accumulator)。此时KafkaProducer#send方法成功返回。

KafkaProducer中还有一个专门的Sender IO线程负责将缓冲池中的消息分批次发送给对应的broker，完成真正的消息发送逻辑。

基本设计特点
  
结合源代码，笔者认为新版本的producer从设计上来说具有以下几个特点(或者说是优势)：

总共创建两个线程：执行KafkaPrducer#send逻辑的线程——我们称之为"用户主线程"；执行发送逻辑的IO线程——我们称之为"Sender线程"
  
不同于Scala老版本的producer，新版本producer完全异步发送消息，并提供了回调机制(callback)供用户判断消息是否成功发送
  
batching机制——"分批发送"机制。每个批次(batch)中包含了若干个PRODUCE请求，因此具有更高的吞吐量
  
更加合理的默认分区策略：对于无key消息而言，Scala版本分区策略是一段时间内(默认是10分钟)将消息发往固定的目标分区，这容易造成消息分布的不均匀，而新版本的producer采用轮询的方式均匀地将消息分发到不同的分区
  
底层统一使用基于Selector的网络客户端实现，结合Java提供的Future实现完整地提供了更加健壮和优雅的生命周期管理。
   
其实，新版本producer的设计优势还有很多，诸如监控指标更加完善等这样的就不一一细说了。总之，新版本producer更加地健壮，性能更好~

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

### batch.size
单位：字节
该参数对于调优producer至关重要。新版producer(o.a.k.clients.producer.KafkaProducer)采用分批发送机制，该参数即控制一个batch的大小。默认是16KB

#### acks:
关乎到消息持久性(durability)的一个参数。高吞吐量和高持久性很多时候是相矛盾的，需要先明确我们的目标是什么？ 高吞吐量？高持久性？亦或是中等？因此该参数也有对应的三个取值：0， -1和1

acks用来控制一个produce请求怎样才能算完成，准确的说，是有多少broker必须已经提交数据到log文件，并向leader发送ack，可以设置如下的值：
  
- 0，意味着producer永远不会等待一个来自broker的ack继续发送下一条（批）消息。，这就是0.7版本的行为。这个选项提供了最低的延迟，但是持久化的保证是最弱的，当server挂掉的时候会丢失一些数据。
- 1，意味着在leader replica已经接收到数据后，producer会得到一个ack。这个选项提供了更好的持久性，因为在server确认请求成功处理后，client才会返回。如果刚写到leader上，还没来得及复制leader就挂了，那么消息才可能会丢失。
- -1，意味着在所有的ISR都接收到数据后，producer才得到一个ack。这个选项提供了最好的持久性，只要还有一个replica存活，那么数据就不会丢失。

#### linger.ms
单位：毫秒
producer会等待buffer的messages数目达到指定值或时间超过x毫秒，才发送数据。减少网络IO，节省带宽之用。原理就是把原本需要多次发送的小batch，通过引入延时的方式合并成大batch发送，减少了网络传输的压力，从而提升吞吐量。当然，也会引入延时.

#### compression.type

producer所使用的压缩器，目前支持gzip, snappy和lz4。压缩是在用户主线程完成的，通常都需要花费大量的CPU时间，但对于减少网络IO来说确实利器。生产环境中可以结合压力测试进行适当配置

#### retries

重试机制，对于瞬时失败的消息发送，开启重试后KafkaProducer会尝试再次发送消息。对于有强烈无消息丢失需求的用户来说，开启重试机制是必选项。
  
**buffer.memory:** 缓冲区大小
  
**max.in.flight.requests.per.connection** 关乎消息乱序的一个配置参数。它指定了Sender线程在单个Socket连接上能够发送未应答PRODUCE请求的最大请求数。适当增加此值通常会增大吞吐量，从而整体上提升producer的性能。不过笔者始终觉得其效果不如调节batch.size来得明显，所以请谨慎使用。另外如果开启了重试机制，配置该参数大于1可能造成消息发送的乱序(先发送A，然后发送B，但B却先行被broker接收)

**max.block.ms**
  
buffer.memory 写满之后x毫秒抛异常TimeoutException

Step 1： 序列化+计算目标分区
  
这是KafkaProducer#send逻辑的第一步，即为待发送消息进行序列化并计算目标分区

Step 2：追加写入消息缓冲区(accumulator)
  
producer创建时会创建一个默认32MB(由buffer.memory参数指定)的accumulator缓冲区，专门保存待发送的消息。除了之前在"关键参数"段落中提到的linger.ms和batch.size等参数之外，该数据结构中还包含了一个特别重要的集合信息：消息批次信息(batches)。该集合本质上是一个HashMap，里面分别保存了每个topic分区下的batch队列，即前面说的批次是按照topic分区进行分组的。这样发往不同分区的消息保存在对应分区下的batch队列中。举个简单的例子，假设消息M1, M2被发送到test的0分区但属于不同的batch，M3分送到test的1分区，那么batches中包含的信息就是：{"test-0" -> [batch1, batch2], "test-1" -> [batch3]}

单个topic分区下的batch队列中保存的是若干个消息批次。每个batch中最重要的3个组件包括：

compressor: 负责执行追加写入操作
  
batch缓冲区：由batch.size参数控制，消息被真正追加写入到的地方
  
thunks：保存消息回调逻辑的集合
  
这一步的目的就是将待发送的消息写入消息缓冲池中

        //当所有 broker 全部挂掉的时候，此时 send 的方法会 block 住60秒(max.block.ms参数控制)，但并不抛出异常，因此failover策略失效。
        //block 在 KafkaProducer.doSend() 中的 long waitedOnMetadataMs = waitOnMetadata(record.topic(), this.maxBlockTimeMs);
        //如果项目启动并且取得 waitOnMetaData 之后全部broker再挂掉的话,不会block应用
    

### kafka server config
https://stackoverflow.com/questions/53039752/kafka-how-to-calculate-the-value-of-log-retention-byte


http://www.cnblogs.com/huxi2b/p/6364613.html
  
http://blog.csdn.net/itleochen/article/details/18352797
  
http://www.cnblogs.com/huxi2b/p/6637425.html
  
http://apache.mirrors.tds.net/kafka/0.10.2.1/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html