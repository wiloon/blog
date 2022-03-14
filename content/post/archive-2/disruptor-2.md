---
title: disruptor
author: "-"
date: 2016-02-15T09:16:15+00:00
url: /?p=8738
categories:
  - Uncategorized

tags:
  - reprint
---
## disruptor
http://www.cnblogs.com/haiq/p/4112689.html

已经不记得最早接触到 Disruptor 是什么时候了,只记得发现它的时候它是以具有闪电般的速度被介绍的。于是在脑子里, Disruptor 和"闪电"一词关联了起来,然而却一直没有时间去探究一下。

最近正在进行一项对性能有很高要求的产品项目的研究,自然想起了闪电般的 Disruptor ,这必有它的用武之地,于是进行了一番探查,将成果和体会记录在案。

一、什么是 Disruptor

从功能上来看,Disruptor 是实现了"队列"的功能,而且是一个有界队列。那么它的应用场景自然就是"生产者-消费者"模型的应用场合了。

可以拿 JDK 的 BlockingQueue 做一个简单对比,以便更好地认识 Disruptor 是什么。

我们知道 BlockingQueue 是一个 FIFO 队列,生产者(Producer)往队列里发布(publish)一项事件(或称之为"消息"也可以)时,消费者(Consumer)能获得通知；如果没有事件时,消费者被堵塞,直到生产者发布了新的事件。

这些都是 Disruptor 能做到的,与之不同的是,Disruptor 能做更多: 

同一个"事件"可以有多个消费者,消费者之间既可以并行处理,也可以相互依赖形成处理的先后次序(形成一个依赖图)；
  
预分配用于存储事件内容的内存空间；
  
针对极高的性能目标而实现的极度优化和无锁的设计；
  
以上的描述虽然简单地指出了 Disruptor 是什么,但对于它"能做什么"还不是那么直截了当。一般性地来说,当你需要在两个独立的处理过程(两个线程)之间交换数据时,就可以使用 Disruptor 。当然使用队列 (如上面提到的 BlockingQueue) 也可以,只不过 Disruptor 做得更好。

拿队列来作比较的做法弱化了对 Disruptor 有多强大的认识,如果想要对此有更多的了解,可以仔细看看 Disruptor 在其东家 LMAX 交易平台(也是实现者) 是如何作为核心架构来使用的,这方面就不做详述了,问度娘或谷哥都能找到。

二、Disruptor 的核心概念

先从了解 Disruptor 的核心概念开始,来了解它是如何运作的。下面介绍的概念模型,既是领域对象,也是映射到代码实现上的核心对象。

Ring Buffer
  
如其名,环形的缓冲区。曾经 RingBuffer 是 Disruptor 中的最主要的对象,但从3.0版本开始,其职责被简化为仅仅负责对通过 Disruptor 进行交换的数据 (事件) 进行存储和更新。在一些更高级的应用场景中,Ring Buffer 可以由用户的自定义实现来完全替代。
  
Sequence  Disruptor
  
通过顺序递增的序号来编号管理通过其进行交换的数据 (事件) ,对数据(事件)的处理过程总是沿着序号逐个递增处理。一个 Sequence 用于跟踪标识某个特定的事件处理者( RingBuffer/Consumer )的处理进度。虽然一个 AtomicLong 也可以用于标识进度,但定义 Sequence 来负责该问题还有另一个目的,那就是防止不同的 Sequence 之间的CPU缓存伪共享(Flase Sharing)问题。
  
 (注: 这是 Disruptor 实现高性能的关键点之一,网上关于伪共享问题的介绍已经汗牛充栋,在此不再赘述) 。
  
Sequencer
  
Sequencer 是 Disruptor 的真正核心。此接口有两个实现类 SingleProducerSequencer、MultiProducerSequencer ,它们定义在生产者和消费者之间快速、正确地传递数据的并发算法。
  
Sequence Barrier
  
用于保持对RingBuffer的 main published Sequence 和Consumer依赖的其它Consumer的 Sequence 的引用。 Sequence Barrier 还定义了决定 Consumer 是否还有可处理的事件的逻辑。
  
Wait Strategy
  
定义 Consumer 如何进行等待下一个事件的策略。  (注: Disruptor 定义了多种不同的策略,针对不同的场景,提供了不一样的性能表现) 
  
Event
  
在 Disruptor 的语义中,生产者和消费者之间进行交换的数据被称为事件(Event)。它不是一个被 Disruptor 定义的特定类型,而是由 Disruptor 的使用者定义并指定。
  
EventProcessor
  
EventProcessor 持有特定消费者(Consumer)的 Sequence,并提供用于调用事件处理实现的事件循环(Event Loop)。
  
EventHandler
  
Disruptor 定义的事件处理接口,由用户实现,用于处理事件,是 Consumer 的真正实现。
  
Producer
  
即生产者,只是泛指调用 Disruptor 发布事件的用户代码,Disruptor 没有定义特定接口或类型。