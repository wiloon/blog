---
title: Netty 堆外内存
author: "-"
date: 2018-03-23T09:57:05+00:00
lastmod: 2026-06-03T17:28:38+08:00
url: netty-memory
categories:
  - cs
tags:
  - netty
  - java
  - memory
  - remix
  - AI-assisted
---

## 为什么使用堆外内存

Java 堆内存（Heap）受 JVM GC 管理，分配和释放都有 GC 开销，且在 GC 发生时对象地址可能移动（Compacting GC）。进行 I/O 操作时，JVM 必须先把堆内数据拷贝到一块固定地址的堆外缓冲区，再交给内核。

堆外内存（Direct Memory / Off-Heap）直接由操作系统管理，有以下优势：

- **零拷贝**：内核可以直接读写堆外内存，省掉堆内 → 堆外的一次拷贝
- **不受 GC 暂停影响**：地址固定，内核持有指针不会因 GC 而失效
- **更可预测的延迟**：不参与 Young/Old GC，减少 STW（Stop-The-World）概率

代价是分配/释放成本更高，且不会被 GC 自动回收，需要手动管理生命周期。

## ByteBuf：Netty 的核心缓冲区抽象

Netty 用 `ByteBuf` 替代 JDK 的 `ByteBuffer`，消除了 `flip()`/`rewind()` 的使用负担，并同时支持堆内和堆外两种底层存储。

### 分类

```
ByteBuf
├── HeapByteBuf          堆内，byte[] 存储，GC 管理
├── DirectByteBuf        堆外，java.nio.DirectByteBuffer 存储
└── CompositeByteBuf     零拷贝组合多个 ByteBuf（可混合堆内/堆外）
```

每种又分 Pooled（池化）和 Unpooled（非池化）两个版本：

| 类型                    | 分配方式          | 适用场景                 |
| ----------------------- | ----------------- | ------------------------ |
| `PooledDirectByteBuf`   | 从内存池取        | 高频、短生命周期 I/O     |
| `UnpooledDirectByteBuf` | 每次调用 `malloc` | 低频、大块、长期持有     |
| `PooledHeapByteBuf`     | 从内存池取        | 不需要 native I/O 的场景 |
| `UnpooledHeapByteBuf`   | 每次 `new byte[]` | 简单测试/工具代码        |

## 零拷贝（Zero-copy）

OS 层面的 Zero-copy 指避免在用户态（User-space）与内核态（Kernel-space）之间拷贝数据，例如 Linux 的 `mmap`、`sendfile`。Netty 的 Zero-copy 完全在用户态（Java 层面），核心目标是减少 ByteBuf 之间不必要的内存拷贝。

### CompositeByteBuf

将多个 ByteBuf 合并为一个逻辑上的 ByteBuf，避免数据复制。传统做法需要两次额外拷贝：

```java
ByteBuf allBuf = Unpooled.buffer(header.readableBytes() + body.readableBytes());
allBuf.writeBytes(header);
allBuf.writeBytes(body);
```

用 `CompositeByteBuf` 则没有拷贝：

```java
CompositeByteBuf compositeByteBuf = Unpooled.compositeBuffer();
// true 表示自动递增 writeIndex，否则 writeIndex 仍为 0，读不到数据
compositeByteBuf.addComponents(true, header, body);
```

也可以直接用 `Unpooled.wrappedBuffer`，底层同样封装了 `CompositeByteBuf`：

```java
ByteBuf allByteBuf = Unpooled.wrappedBuffer(header, body);
```

`CompositeByteBuf` 内部两个 ByteBuf 仍独立存在，只是逻辑上视为整体，不发生数据拷贝。

### wrap 操作

将 `byte[]`、`ByteBuffer` 等包装成 `ByteBuf`，不拷贝数据：

```java
byte[] bytes = ...;
ByteBuf byteBuf = Unpooled.wrappedBuffer(bytes);
// byteBuf 与 bytes 共用同一块内存，对 bytes 的修改会反映到 byteBuf
```

`Unpooled` 提供多个 `wrappedBuffer` 重载，支持 `byte[]`、`ByteBuffer`、`ByteBuf` 等类型，一个或多个均可。

### slice 操作

将一个 ByteBuf 切片为多个共享同一存储区域的子 ByteBuf：

```java
ByteBuf header = byteBuf.slice(0, 5);
ByteBuf body   = byteBuf.slice(5, 10);
// header 和 body 共享 byteBuf 的底层存储，无数据拷贝
```

无参的 `slice()` 等价于 `buf.slice(buf.readerIndex(), buf.readableBytes())`，返回当前可读部分的切片。slice 与 wrap 方向相反：wrap 是多合一，slice 是一拆多。

### FileRegion

通过 `FileRegion` 包装 `FileChannel.transferTo()` 实现文件传输零拷贝，底层依赖操作系统的 `sendfile`，内核直接将文件数据传输到目标 Channel，无需先拷贝到用户态缓冲区：

```java
if (ctx.pipeline().get(SslHandler.class) == null) {
    // 未启用 SSL，使用零拷贝
    ctx.write(new DefaultFileRegion(raf.getChannel(), 0, length));
} else {
    // 启用 SSL 后无法使用零拷贝，退回到 ChunkedFile
    ctx.write(new ChunkedFile(raf));
}
```

## 内存池（PooledByteBufAllocator）

直接内存的分配代价远高于堆内存，Netty 引入了类似 jemalloc 的分层内存池来复用堆外内存。

### 三层结构

```
PoolArena（每个线程独占一个）
  └── PoolChunkList（按使用率分组的 Chunk 链表）
        └── PoolChunk（默认 16 MB，向 OS 申请的最小单元）
              └── PoolSubpage（用于 < 8 KB 的小对象）
```

- **Arena**：线程本地，减少竞争
- **Chunk**：一次向 OS 申请 16 MB 连续内存，内部用二叉树管理空闲页
- **SubPage**：将一个内存页（8 KB）切分为等大小的槽，服务小对象分配

分配时先在线程本地 `PoolArena` 中找空闲块，找不到再向 `PoolChunkList` 申请新 Chunk，尽量避免系统调用。

### 默认分配器

```java
// Netty 默认使用 PooledByteBufAllocator
ByteBufAllocator alloc = PooledByteBufAllocator.DEFAULT;
ByteBuf buf = alloc.directBuffer(1024);
```

`PooledByteBufAllocator.DEFAULT` 在支持 `sun.misc.Unsafe` 的平台上优先选择堆外内存；可通过启动参数覆盖：

```bash
-Dio.netty.allocator.type=unpooled   # 关闭池化
-Dio.netty.noPreferDirect=true       # 优先堆内
```

## 引用计数（ReferenceCounting）

堆外内存不受 GC 管理，Netty 通过引用计数来确定何时释放。

```java
ByteBuf buf = alloc.directBuffer(256);
// buf.refCnt() == 1

buf.retain();        // refCnt == 2
buf.release();       // refCnt == 1
buf.release();       // refCnt == 0 → 内存归还到内存池（或 munmap）
```

**规则**：谁是最后一个使用者，谁负责调用 `release()`。在 Netty Pipeline 中，`TailHandler` 会自动释放未被处理的消息。

常见泄漏根因：

- 忘记 `release()`，或者在异常路径上跳过了 `release()`
- `ByteBuf` 被 `retain()` 多次但只 `release()` 一次

## 内存泄漏检测

Netty 内置基于弱引用的泄漏检测器 `ResourceLeakDetector`：

```bash
# 检测级别（默认 SIMPLE，生产建议 SIMPLE，调试用 PARANOID）
-Dio.netty.leakDetection.level=PARANOID
```

| 级别       | 采样率          | 性能开销       |
| ---------- | --------------- | -------------- |
| `DISABLED` | 0%              | 无             |
| `SIMPLE`   | ~1%             | 极低           |
| `ADVANCED` | ~1%（含调用栈） | 低             |
| `PARANOID` | 100%            | 高，仅用于调试 |

发生泄漏时，日志会打印类似：

```
LEAK: ByteBuf.release() was not called before it's garbage-collected.
```

## 堆外内存上限配置

堆外内存不受 `-Xmx` 限制，需单独指定：

```bash
-XX:MaxDirectMemorySize=512m
```

Netty 的 `PooledByteBufAllocator` 还有自己的上限参数：

```bash
-Dio.netty.allocator.maxOrder=11          # Chunk 大小 = 8K << maxOrder，默认 11 → 16MB
-Dio.netty.allocator.numDirectArenas=16   # 堆外 Arena 数量
```

## 哪些数据放在堆外内存

### I/O 读写缓冲区（最核心）

**网络收发的字节流**是放在堆外的主体。

- `Channel.read()` 时，Netty 直接把内核 socket 缓冲区的数据 DMA 到堆外 `DirectByteBuf`，无需经过堆内
- `Channel.write()` 时，堆外缓冲区直接交给 `sendfile`/`writev`，内核无需再做一次拷贝

如果业务代码写入的是堆内 `HeapByteBuf`，Netty 在真正发送前会自动转换为堆外（`AbstractNioChannel#filterOutboundMessage`），保证最终发送路径上始终走直接内存。

### PoolChunk 本身的内存块

`PooledByteBufAllocator` 向 OS 申请的每个 **16 MB Chunk** 是堆外的连续内存块，业务申请的 `DirectByteBuf` 都是从这些 Chunk 上切出来的子区间。

### 不放堆外的数据

| 数据                                                        | 位置   | 原因                 |
| ----------------------------------------------------------- | ------ | -------------------- |
| Handler 的业务对象（POJO、String 等）                       | JVM 堆 | 正常对象，走 GC      |
| `PooledByteBufAllocator` 自身的元数据（Chunk 树、引用计数） | JVM 堆 | 管理结构，量小       |
| `HeapByteBuf` 的 `byte[]`                                   | JVM 堆 | 显式选择堆内分配器时 |
| Encoder/Decoder 的中间状态                                  | JVM 堆 | 解码状态机等业务逻辑 |

**一句话总结**：Netty 只把需要和内核直接交换的**字节流缓冲区**放在堆外，其余业务对象、元数据、解码状态全在 JVM 堆上。

## 消费速率不足时的堆外内存积压

### 结合协议解析服务的 OOM 场景

对应的生产事故复盘可见 [物联网平台协议解析服务生产环境 OOM：MySQL 迁移 InfluxDB](../career/iot-protocol-oom-mysql-influxdb.md)。

可以把问题抽象成吞吐失衡：当入口速率 $\lambda_{in}$ 长时间大于处理速率 $\mu_{out}$ 时，积压量会持续增长，近似满足 $\Delta backlog \approx (\lambda_{in} - \mu_{out}) \times t$。

在协议解析服务里，典型路径是：EventLoop 读 socket 数据并解码成 `ByteBuf`，然后投递到业务线程做后续写库。若下游 MySQL 写入延迟上升，业务线程处理变慢，消息在业务队列中排队；与此同时 EventLoop 仍在持续 read，新的 `DirectByteBuf` 继续分配。

只要 `ByteBuf` 关联的处理链路没有走完，对应 direct memory 就不会释放。结果就是“分配速度 > 释放速度”，堆外内存占用不断抬升，最终触发 `OutOfDirectMemoryError`，或者被系统 OOM Killer 杀进程。

如果此时节点重启并回放上游积压流量，单节点瞬时入口速率会进一步升高，`\lambda_{in}` 与 `\mu_{out}` 的差值被放大，因而容易出现短时间内连续 OOM 的滚动故障。

### 入方向（Inbound）

Netty EventLoop 从 socket 读数据 → 创建 `DirectByteBuf` → 依次经过 Pipeline 的各个 Handler。

**场景一：Handler 在 EventLoop 线程里阻塞**

```
EventLoop 线程被卡住 → 无法继续 read → socket 内核缓冲区堆满 → TCP 窗口收缩为 0 → 对端停止发送
```

这种情况堆外内存反而不会无限增长，TCP 流控兜底了。

**场景二：Handler 把数据扔到业务线程池异步处理**

```
EventLoop 继续疯狂 read → 不断创建 DirectByteBuf → 扔进线程池队列
→ 线程池积压 → DirectByteBuf 在堆外内存中堆积
```

这才是真正危险的积压，堆外内存会持续增长直到 OOM 或 `MaxDirectMemorySize` 耗尽。

正确做法是消费跟不上时主动关闭 `autoRead`：

```java
// 消费积压时
ctx.channel().config().setAutoRead(false);

// 消费恢复后
ctx.channel().config().setAutoRead(true);
```

### 出方向（Outbound）

业务代码疯狂调用 `channel.write()` 但网络速率跟不上，数据会积压在 Netty 的 `ChannelOutboundBuffer` 里（ByteBuf 内容在堆外）。

Netty 提供水位线机制：

```java
// 超过 high 水位，channel.isWritable() 返回 false
channel.config().setWriteBufferWaterMark(
    new WriteBufferWaterMark(32 * 1024, 64 * 1024)
);

// 业务代码写出前应检查
if (ctx.channel().isWritable()) {
    ctx.writeAndFlush(msg);
} else {
    // 触发背压，通知上游降速
}
```

### 积压场景汇总

| 方向                 | 积压位置                     | 兜底机制       | 主动控制手段         |
| -------------------- | ---------------------------- | -------------- | -------------------- |
| 入方向（同步处理）   | socket 内核缓冲区            | TCP 流控       | 无需额外处理         |
| 入方向（异步线程池） | 堆外 `DirectByteBuf`         | **无自动兜底** | `setAutoRead(false)` |
| 出方向               | 堆外 `ChannelOutboundBuffer` | 水位线告警     | 检查 `isWritable()`  |

异步线程池 + 不控 `autoRead` 是生产中最常见的堆外内存 OOM 根因。

## 关键要点总结

- Netty 默认使用**池化堆外内存**（`PooledDirectByteBuf`）进行 I/O，减少拷贝和 GC 压力
- 堆外内存只存放**字节流缓冲区**，业务对象、解码状态等仍在 JVM 堆
- 堆外内存通过**引用计数**管理生命周期，必须成对调用 `retain()`/`release()`
- 内存池分为 Arena → Chunk → SubPage 三层，尽量复用已分配的内存
- 异步消费时必须配合 `setAutoRead(false)` 做背压，否则堆外内存会无限积压
- 出方向用 `isWritable()` + 水位线控制写出速率
- 生产环境用 `SIMPLE` 泄漏检测；怀疑泄漏时切换到 `PARANOID`
- 堆外内存不受 `-Xmx` 约束，需通过 `-XX:MaxDirectMemorySize` 单独限制
