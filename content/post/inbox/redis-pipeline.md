---
title: "redis pipeline"
author: "-"
date: "2021-07-24 22:00:22"
url: "redis-pipeline"
categories:
  - redis
tags:
  - redis
---
## "redis pipeline"

why pipeline ?
Redis客户端与server的请求/响应模型
前面的文章 Redis底层协议RESP详解 ，介绍到redis客户端与redis-server交互通信，采用的TCP请求/响应模型；
我们通过Redis客户端执行命令，如set key value，客户端遵循RESP协议，将命令的协议串发送给redis-server执行，redis-server执行完成后再同步返回结果。
手写Redis客户端-实现自己的Jedis 对这一过程进行了重点分析，并遵循RESP实现了自己简易版的Redis客户端。

Redis客户端与server通信，使用的是客户端-服务器 (CS) 模式；每次交互，都是完整的请求/响应模式。
这意味着通常情况下一个请求会遵循以下步骤: 

客户端连接服务端，基于特定的端口，发送一个命令，并监听Socket返回，通常是以阻塞模式，等待服务端响应。
服务端处理命令，并将结果返回给客户端。
很显然，我们使用jedis或lettuce执行Redis命令，每次都是建立socket连接，并等待返回。

每个命令底层建立TCP连接的时间是省不掉的，即使我们都是在内网使用Redis，内网快但请求/响应的往返时间是不会减少的。
当需要对一组kv进行批量操作时，这组命令的耗时=sum(N*(建立连接时间+发送命令、返回结果的往返时间RTT))，随批量操作的key越多，时间累加呈线性增长。

顺理成章的，就出现了像数据库连接池等池化思想的衍生，redis连接也进行“池化”，如JedisPool。

JedisPool就足够了？
池化connection后，每次执行命令都从池子里“借”，用完之后再将connection“还”到池子。只是节省了创建TCP连接的时间；
当需要对一组kv进行批量操作时，JedisPool池子里的connection连接、极端情况都被用完了，怎么办？
——需要等待JedisPool池里有可复用的connection才能继续执行；

redis.clients.jedis.exceptions.JedisConnectionException: Could not get a resource from the pool
…
Caused by: java.util.NoSuchElementException: Timeout waiting for idle object
at org.apache.commons.pool2.impl.GenericObjectPool.borrowObject(GenericObjectPool.java:449)
如果在指定的等待时间内没有等到idle空闲连接，就报异常了。

尽管使用了池化、将connection进行复用，但不可避免的带来其他问题: 
https://jjlu521016.github.io/2018/12/09/JedisPool常见问题.html

除了池化的connection会被瞬间用完，Redis官网还给出了另外一个性能损耗的原因: 

It's not just a matter of RTT
https://redis.io/topics/pipelining
虽然池化的connection，节省了建立连接的时间，但多条命令(发送命令到sever、server返回结果)分别执行多次socket网络IO，涉及到read()和write() syscall系统调用，这意味着从用户态到内核态。上下文切换是巨大的速度损失。

如果能将多条命令“合并”到一起，进行一次网络IO，性能会提高不少吧。
有没有一种方式，占用极少的connection连接，且不浪费请求/响应的往返时间，提高整体吞吐量呢？
这就是今天的主角——Redis pipeline。

pipeline不仅是一种减少往返时间的延迟成本的方法，它实际上还可以极大地提高Redis服务器中每秒可执行的总操作量。

由于网络开销延迟，就算redis-server端有很强的处理能力，也会由于收到的client命令少，而造成吞吐量小。
当client 使用pipeline 发送命令时，redis-server必须将部分请求放到队列中 (使用内存) ，执行完毕后一次性发送结果。

对pipeline的支持
pipeline(管道)功能在命令行CLI客户端redis-cli中没有提供，也就是我们不能通过终端交互的方式使用pipeline；
redis的客户端，如jedis，lettuce等都实现了对pipeline的支持。

pipeline为我们节省了哪部分时间？
pipeline在某些场景下非常有用，比如有多个command需要被“及时的”提交，而且他们对相应结果没有互相依赖，对结果响应也无需立即获得，那么pipeline就可以充当这种“批处理”的工具；而且在一定程度上，可以较大的提升性能: 

我们使用JedisPool连接池，节省了建立连接connection的时间；
pipeline节省了多条命令的(发送命令到server、server返回结果)往返时间RTT，包括多次网络IO、系统调用的消耗。
pipeline是万金油？
1. pipeline“独占”connection，直到pipeline结束
pipeline期间将“独占”connection，此期间将不能进行非“管道”类型的其他操作，直到pipeline关闭；如果你的pipeline的指令集很庞大，为了不干扰链接中的其他操作，你可以为pipeline操作新建Client连接，让pipeline和其他正常操作分离在2个client连接中。

2. 使用pipeline，如果发送的命令很多的话，建议对返回的结果加标签，当然这也会增加使用的内存；

pipeline实现原理

管道 (pipeline) 可以一次性发送多条命令并在执行完后一次性将结果返回，pipeline通过减少客户端与redis的通信次数来实现降低往返延时时间。
pipeline 底层实现是队列，队列的先进先出特性，保证了数据的顺序性。 pipeline 的默认的同步的个数为53个，也就是说arges中累加到53条数据时会把数据提交。

需要注意到是用 pipeline方式打包命令发送，redis必须在处理完所有命令前先缓存起所有命令的处理结果。打包的命令越多，缓存消耗内存也越多。所以并不是打包的命令越多越好。具体多少合适需要根据具体情况测试。

pipeline“打包命令”
客户端将多个命令缓存起来，缓冲区满了就发送(将多条命令打包发送)；有点像“请求合并”。
服务端 接受一组命令集合，切分后逐个执行返回。

从Redis的RESP协议上看，pipeline并没有什么特殊的地方，只是把多个命令连续的发送给redis-server，然后一一解析返回结果。
手写Redis客户端-实现自己的Jedis 我们自己实现的Redis客户端，遵循RESP协议拼装了协议串，用socket将协议串发送给redis-server，以此实现和redis-server的通信。
pipeline并没有什么特殊的地方，只是一次性append追加了多条RESP指令，然后一次性发送出去而已。

1.pipeline减少了RTT，也减少了IO调用次数 (IO调用涉及到用户态到内核态之间的切换) 
2.需要控制pipeline的大小，否则会消耗Redis的内存
Jedis客户端缓存是8192，超过该大小则刷新缓存，或者直接发送。

当客户端使用pipeline发送很多请求时，服务器将在内存中使用队列存储这些指令的响应。
所以批量发送的指令数量，最好在一个合理的范围内，比如每次发1万条指令，读取完响应后再发送另外1万条指令。2万条指令，一次性发送和分2次发送，对客户端来说速度是差不多的，但是对服务器来说，内存占用差了1万条响应的大小。

pipeline 的局限性
pipeline 只能用于执行连续且无相关性的命令，当某个命令的生成需要依赖于前一个命令的返回时(或需要一起执行时)，就无法使用 pipeline 了。通过 scripting 功能，可以规避这一局限性。

有些系统可能对可靠性要求很高，每次操作都需要立马知道这次操作是否成功，是否数据已经写进redis了，如Redis实现分布式锁等，那这种场景就不适合了。

批量执行命令的其他方式
Redis事务
Scripting lua脚本
Redis支持使用multi命令，使用Redis事务。
但Redis事务属于弱事务，并不像RDBMS一样ACID的特性，详见Redis事务,你真的了解吗

pipeline与Redis事务(multi)
multi: 标记一个事务块的开始。 事务块内的多条命令会按照先后顺序被放进一个队列当中，最后由 EXEC 命令原子性(atomic)地执行。
pipeline: 客户端将执行的命令写入到缓冲中，最后由exec命令一次性发送给redis执行返回。

multi 是redis服务端一次性返回所有命令执行返回结果。
pipeline管道操作是需要客户端与服务端的支持，客户端将命令写入缓冲，最后再通过exec命令发送给服务端，服务端通过命令拆分，逐个执行返回结果。

两者的区别

pipeline选择客户端缓冲，multi选择服务端队列缓冲；
请求次数的不一致，multi需要每个命令都发送一次给服务端，pipeline最后一次性发送给服务端，请求次数相对于multi减少
multi/exec可以保证原子性，而pipeline不保证原子性
pipeline和“事务”是两个完全不同的概念，pipeline只是表达“交互”中操作的传递的方向性，pipeline也可以在事务中运行，也可以不在。
无论如何，pipeline中发送的每个command都会被server立即执行，如果执行失败，将会在此后的相应中得到信息；也就是pipeline并不是表达“所有command都一起成功”的语义；
但是如果pipeline的操作被封装在事务中，那么将有事务来确保操作的成功与失败。

Scripting lua脚本
Redis 从 2.6 开始内嵌了 Lua 环境来支持用户扩展功能. 通过 Lua 脚本, 我们可以原子化地执行多条 Redis 命令.
在 Redis 中执行 Lua 脚本需要用到 eval 和 evalsha 和 script 这几个命令。

Redis官方文档: https://redis.io/topics/pipelin

---

https://zhuanlan.zhihu.com/p/102045642