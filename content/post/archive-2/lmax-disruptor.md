---
title: LMAX Disruptor
author: "-"
date: 2016-02-15T03:05:53+00:00
url: /?p=8734
categories:
  - Uncategorized

tags:
  - reprint
---
## LMAX Disruptor
LMAX Disruptor——一个高性能、低延迟且简单的框架
  
原文地址: LMAX Disruptor – High Performance, Low Latency and Simple Too 翻译: 杨帆 校对: 丁一

Disruptor是一个用于在线程间通信的高效低延时的消息组件,它像个增强的队列,并且它是让LMAX Exchange跑的如此之快的一个关键创新。关于什么是Disruptor、为何它很重要以及它的工作原理方面的信息都呈爆炸性增长 —— 这些文章很适合开始学习Disruptor,还可跟着LMAX BLOG深入学习。这里还有一份更详细的白皮书。


虽然disruptor模式使用起来很简单,但是建立多个消费者以及它们之间的依赖关系需要的样板代码太多了。为了能快速又简单适用于99%的场景,我为Disruptor模式准备了一个简单的领域特定语言。例如,为建立一个消费者的"四边形模式":

 (从Trisha Gee's excellent series explaining the disruptor pattern偷来的图片)

在这种情况下,只要生产者 (P1) 将元素放到ring buffer上,消费者C1和C2就可以并行处理这些元素。但是消费者C3必须一直等到C1和C2处理完之后,才可以处理。在现实世界中的对应的案例就像: 在处理实际的业务逻辑 (C3) 之前,需要校验数据 (C1) ,以及将数据写入磁盘 (C2) 。

用原生的Disruptor语法来创建这些消费者的话代码如下:

Executor executor = Executors.newCachedThreadPool();
  
BatchHandler handler1 = new MyBatchHandler1();
  
BatchHandler handler2 = new MyBatchHandler2();
  
BatchHandler handler3 = new MyBatchHandler3()
  
RingBuffer ringBuffer = new RingBuffer(ENTRY_FACTORY, RING_BUFFER_SIZE);
  
ConsumerBarrier consumerBarrier1 = ringBuffer.createConsumerBarrier();
  
BatchConsumer consumer1 = new BatchConsumer(consumerBarrier1, handler1);
  
BatchConsumer consumer2 = new BatchConsumer(consumerBarrier1, handler2);
  
ConsumerBarrier consumerBarrier2 =
  
ringBuffer.createConsumerBarrier(consumer1, consumer2);
  
BatchConsumer consumer3 = new BatchConsumer(consumerBarrier2, handler3);
  
executor.execute(consumer1);
  
executor.execute(consumer2);
  
executor.execute(consumer3);
  
ProducerBarrier producerBarrier =
  
ringBuffer.createProducerBarrier(consumer3);
  
在以上这段代码中,我们不得不创建那些个handler (就是那些个MyBatchHandler实例) ,外加消费者屏障,BatchConsumer实例,然后在他们各自的线程中处理这些消费者。DSL能帮我们完成很多创建工作,最终的结果如下:

Executor executor = Executors.newCachedThreadPool();
  
BatchHandler handler1 = new MyBatchHandler1();
  
BatchHandler handler2 = new MyBatchHandler2();
  
BatchHandler handler3 = new MyBatchHandler3();
  
DisruptorWizard dw = new DisruptorWizard(ENTRY_FACTORY,
  
RING_BUFFER_SIZE, executor);
  
dw.consumeWith(handler1, handler2).then(handler3);
  
ProducerBarrier producerBarrier = dw.createProducerBarrier();
  
我们甚至可以在一个更复杂的六边形模式中构建一个并行消费者链: 

查看源代码
  
打印帮助
  
dw.consumeWith(handler1a, handler2a);
  
dw.after(handler1a).consumeWith(handler1b);
  
dw.after(handler2a).consumeWith(handler2b);
  
dw.after(handler1b, handler2b).consumeWith(handler3);
  
ProducerBarrier producerBarrier = dw.createProducerBarrier();
  
这个领域特定语言刚刚诞生不久,欢迎任何反馈,也欢迎大家从github上fork并改进它。