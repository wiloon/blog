---
title: Backpressure, 背压
author: "-"
date: 2026-03-20T17:51:42+08:00
url: backpressure
categories:
  - network
tags:
  - reprint
  - remix
  - AI-assisted
---

## 什么是背压

背压 (Backpressure, back-pressure), 又称负压。

Backpressure 并不是响应式编程 (Reactive Programming) 独有的概念, 也不是一种「机制」或「策略」。

**Backpressure 是一种现象**: 在数据流从上游生产者向下游消费者传输的过程中, 上游生产速度大于下游消费速度, 导致下游的 Buffer 溢出, 这种现象就叫做 Backpressure。

## 背压的本质

可以用水管来类比:

- **上游** = 水源 (生产者, Producer)
- **下游** = 水龙头 / 水桶 (消费者, Consumer)
- **管道** = 消息队列 / Buffer

当水源出水速度远远大于水桶的接收速度时, 管道中的水压就会升高。如果不加以控制, 水桶会溢出, 即数据丢失或系统崩溃。这个"升高的压力"就是背压。

## 背压出现的场景

背压广泛存在于各类系统中:

- **消息队列**: 生产者发送消息的速率超过消费者消费速率, 队列积压
- **流式计算**: Kafka、Flink 等处理管道中, 上游数据涌入速度超过下游处理能力
- **网络传输**: TCP 协议中, 发送方速率超过接收方处理能力时, 接收窗口收缩
- **响应式编程**: RxJava、Project Reactor 等框架需要显式处理背压
- **微服务调用链**: 下游服务响应慢, 上游请求积压导致线程池耗尽

## 背压的处理策略

背压本身是现象, 应对背压才是策略。常见的应对方式有以下几种:

### 1. 控制生产速率 (Flow Control)

主动降低上游的生产速度, 使其与下游消费能力匹配。典型实现是 TCP 的滑动窗口机制: 接收方通过 ACK 报文中的窗口大小字段, 告知发送方当前可接收的数据量。

### 2. 缓冲 (Buffering)

在上下游之间加入缓冲区, 吸收短期的速率不均。但缓冲只能解决短暂的峰值问题, 无法解决长期速率差异, 且会引入延迟和内存压力。

### 3. 丢弃 (Drop)

当 Buffer 已满时, 丢弃新到来的数据。适用于对数据完整性要求不高的场景, 如日志上报、监控指标采集。

### 4. 采样 (Sampling)

不处理全部数据, 只处理其中的一个子集。例如每 N 条处理 1 条。

### 5. 批处理 (Batching)

将多条消息合并为一批一起处理, 提升单次处理的吞吐量, 从而提升整体消费速率。

### 6. 熔断与限流

在微服务场景下, 通过熔断器 (Circuit Breaker) 和限流器快速失败, 保护下游服务不被压垮。

## 响应式编程中的背压

在响应式编程规范 (Reactive Streams) 中, 背压被设计为一等公民。Reactive Streams 定义了四个核心接口:

- `Publisher` — 数据生产者
- `Subscriber` — 数据消费者
- `Subscription` — 连接生产者与消费者, 消费者通过 `request(n)` 告知生产者最多发送 n 条数据
- `Processor` — 同时充当 Publisher 和 Subscriber

`request(n)` 正是背压的核心机制: 消费者主动拉取 (pull) 数据, 而非被动接收 (push), 从而将控制权交给消费者端。

### RxJava 中的背压策略

RxJava 2.x 引入了 `Flowable` 类型专门处理背压, 并提供了多种策略:

```java
// 缓冲策略: 缓存所有未消费的数据
Flowable.range(1, 1000)
    .onBackpressureBuffer()
    .subscribe(...);

// 丢弃策略: 丢弃无法立即消费的数据
Flowable.range(1, 1000)
    .onBackpressureDrop()
    .subscribe(...);

// 保留最新策略: 只保留最新的一条数据
Flowable.range(1, 1000)
    .onBackpressureLatest()
    .subscribe(...);
```

## TCP 中的背压

TCP 协议在传输层天然实现了背压机制:

1. 接收方维护一个接收缓冲区 (Receive Buffer)
2. 每次 ACK 时, 接收方在报头中携带 **Window Size** 字段, 告知发送方当前缓冲区剩余空间
3. 发送方根据 Window Size 调整发送速率
4. 当 Window Size 为 0 时, 发送方停止发送, 等待接收方处理完缓冲区数据后再重新通知

这就是 TCP 滑动窗口 (Sliding Window) 机制, 本质上是一种标准的背压实现。

## 相关概念对比

### Push 模型 vs Pull 模型

背压只在 **Push 模型**下才会出现。两种数据传输模型的对比:

| 模型 | 驱动方 | 描述 | 是否有背压风险 |
|------|--------|------|----------------|
| **Push 模型** (推模型) | 生产者 | 生产者以自己的节奏发送数据, 消费者被动接收 | ✅ 有, 消费者容易被压垮 |
| **Pull 模型** (拉模型) | 消费者 | 消费者按需请求数据, 生产者按需生产 | ❌ 无, 天然具备背压能力 |

背压是 Push 模型固有的问题。Reactive Streams 的 `request(n)` 本质上把 Push 模型改造成了受控的 Pull 模型, 从而从根本上解决了背压问题。

> 注意: 有人会用「正压」来类比物理水管中顺流方向的压力, 但这不是计算机科学的标准术语, 对应的准确说法就是 Push 模型或生产者驱动 (producer-driven)。

### 饥饿 (Starvation / Underflow)

与背压完全相反的现象: **消费速率 > 生产速率**。

- 背压: 生产太快 → 下游撑不住 → Buffer 溢出
- 饥饿: 消费太快 → 上游供不上 → 消费者空转等待

饥饿通常不会导致崩溃, 但会造成资源浪费和处理延迟。常见的例子:

- 线程池中的工作线程没有任务可处理, 一直轮询
- Kafka Consumer 的消费速率远高于 Producer 的生产速率, 消费者频繁 poll 到空结果
- 数据库连接池中的连接被频繁申请但没有实际 SQL 执行

### 拥塞 (Congestion)

在网络领域, 背压更常见的术语是**拥塞 (Congestion)**。TCP 拥塞控制 (Congestion Control) 和流量控制 (Flow Control) 是两个相关但不同的机制:

| 机制 | 控制目标 | 信号来源 |
|------|----------|----------|
| **流量控制 (Flow Control)** | 防止接收方 Buffer 溢出 | 接收方 Window Size |
| **拥塞控制 (Congestion Control)** | 防止网络链路本身拥堵 | 丢包、延迟增大 |

两者都是背压思想的体现, 只是作用层面不同。

### 节流 (Throttling) vs 限流 (Rate Limiting)

这两个概念都是主动施加"阻力"来应对背压:

- **节流 (Throttling)**: 平滑化请求速率, 在时间窗口内均匀分配处理量。例如每秒最多处理 100 个请求, 超出的请求延迟处理而非拒绝。
- **限流 (Rate Limiting)**: 超出阈值直接拒绝或丢弃。例如 API Gateway 对单个 IP 每分钟最多 60 次调用, 超出直接返回 429。

### 概念全景图

```text
生产者 (Producer)
    │
    │  ← 正常: Push 数据
    │  ← 过快: 产生背压 (Backpressure)
    │  ← 过慢: 消费者饥饿 (Starvation)
    ▼
  Buffer / Queue
    │
    │  拥塞时触发: 流量控制 / 拥塞控制
    │  超限时触发: 节流 / 限流 / 丢弃
    ▼
消费者 (Consumer)
    │
    └─ Pull 模型: request(n) 主动拉取, 从根本上避免背压
```

## 总结

| 维度 | 说明 |
|------|------|
| 本质 | 生产速率 > 消费速率导致的现象 |
| 层次 | 存在于网络、消息队列、流处理、响应式编程等各层 |
| 应对方式 | 流控、缓冲、丢弃、采样、批处理、熔断限流 |
| 核心思路 | 让消费者控制节奏 (pull 模型优于 push 模型) |

背压问题的根源是速率不匹配, 解决思路要么提升消费速度, 要么降低生产速度, 要么在中间加入合理的缓冲与降级策略。

---

> 参考:
>
> - 扔物线, 知乎回答: https://www.zhihu.com/question/49618581/answer/237078934
> - Reactive Streams 规范: https://www.reactive-streams.org/
> - TCP RFC 793 滑动窗口机制
