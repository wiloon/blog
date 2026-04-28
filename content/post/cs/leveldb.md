---
title: LevelDB
author: "-"
date: 2026-04-28T11:01:32+08:00
url: leveldb
categories:
  - Database
tags:
  - leveldb
  - lsm-tree
  - database
  - remix
  - AI-assisted
---

## 简介

LevelDB 是由 Google 工程师 Jeff Dean 和 Sanjay Ghemawat 开发的开源 KV 存储引擎，两人同时也是 Bigtable 和 MapReduce 的主要设计者。LevelDB 可以理解为单机版的 Bigtable Tablet Server，能够处理十亿级别规模的 Key-Value 数据持久性存储。

**主要特性：**

- 数据按 Key 有序存储，支持自定义比较函数
- 提供 Put / Get / Delete 以及原子批量操作接口
- 支持 Snapshot 快照读，读操作不受并发写影响
- 支持 Snappy 数据压缩
- 写性能极高：随机写约 40 万条/秒，随机读约 6～10 万条/秒（4核机器）
- 写速度远大于读速度；顺序读写远快于随机读写

LevelDB 是单进程嵌入式库，不提供网络服务，适合作为其他系统的本地存储引擎。Chrome 浏览器用它存储 IndexedDB 数据，比特币/以太坊节点用它存储区块链状态。

---

## LSM-Tree

LevelDB 的核心数据结构是 **LSM-Tree（Log-Structured Merge-Tree）**，一种针对写入密集型场景优化的存储结构。

**核心思想：** 将随机写转化为顺序写，以牺牲部分读性能换取极高的写入吞吐量。

### 写入流程

```
写入请求
   ↓
WAL（预写日志，顺序写磁盘）
   ↓
MemTable（内存，有序跳表 SkipList）
   ↓ 满了之后
Immutable MemTable（只读，等待 flush）
   ↓ flush（minor compaction）
L0（SSTable 文件，磁盘）
   ↓ compaction（major compaction）
L1 → L2 → ... Ln
```

### 三大放大问题

| 问题 | 说明 |
| --- | --- |
| 写放大 | 数据会被反复 compaction，实际写磁盘量远大于原始数据量，通常 10x～30x |
| 读放大 | 读时需要依次查 MemTable → Immutable MemTable → L0 → L1 → ... |
| 空间放大 | 同一 key 可能存在多个版本，直到 compaction 才合并清理 |

### 为什么写快

- 所有写入都是**顺序 I/O**（追加 WAL、批量 flush）
- 没有 B-Tree 那样的随机写和页分裂开销
- 一次写入只涉及一次磁盘顺序追加写 + 一次内存 SkipList 插入

### 使用 LSM-Tree 的系统

- **LevelDB / RocksDB** — 经典实现（RocksDB 是 LevelDB 的增强版）
- **Cassandra、HBase** — 分布式存储
- **ClickHouse MergeTree** — 列式存储引擎

---

## 静态结构

LevelDB 的数据存储在内存和磁盘两部分，主要由六个组件构成：

| 组件 | 位置 | 说明 |
| --- | --- | --- |
| MemTable | 内存 | 当前可读写的有序跳表，最新数据在此 |
| Immutable MemTable | 内存 | 已满、等待 flush 到磁盘的只读 MemTable |
| SSTable (.sst) | 磁盘 | 按层组织的有序 KV 文件，L0～Ln |
| Log (WAL) | 磁盘 | 预写日志，用于崩溃恢复 |
| Manifest | 磁盘 | 记录每个 SSTable 文件属于哪层、Key 范围等元数据 |
| Current | 磁盘 | 记录当前生效的 Manifest 文件名 |

### MemTable 与 SkipList

MemTable 内部使用**跳表（SkipList）** 维护 Key 有序性。SkipList 是平衡树的随机化替代，插入时无需频繁调整节点，写入效率高。Redis 也使用 SkipList 作为有序集合的底层结构。

**删除操作在 MemTable 中并不立即删除数据**，而是插入一条带删除标记的记录，真正的物理删除在后续 Compaction 时完成（Lazy Delete）。

### SSTable 文件结构

所有 `.sst` 文件内部布局相同，分为数据区和管理区：

- **Data Block**：存储实际的有序 KV 记录，相邻 Key 使用前缀压缩节省空间
- **Meta Block**：预留接口（1.2 版本暂未使用）
- **Index Block**：每个 Data Block 的索引，记录起始位置、大小和最大 Key
- **Footer**：文件末尾，指向 Index Block 和 Meta Index Block 的位置

**L0 的特殊性：** L0 的 SSTable 文件之间 Key 范围可能重叠（直接由 MemTable flush 产生）；L1 及以上各层内文件 Key 范围不重叠。

### Log 文件（WAL）

Log 文件以 32KB 为单位划分物理 Block，每条记录由记录头（CheckSum + 长度 + 类型）和数据组成。记录类型分为 FULL / FIRST / MIDDLE / LAST，用于处理跨 Block 的大记录。

---

## 写入流程

对于 `Put(Key, Value)`：

1. 将 KV 记录**顺序追加**到 Log 文件末尾（磁盘顺序写）
2. 将 KV 记录插入内存中的 MemTable（SkipList 插入）

写入完成。整个过程只有一次磁盘顺序写 + 一次内存写，速度极快。

对于 `Delete(Key)`：与写入相同，只是写入的是「Key + 删除标记」，不立即删除数据。

---

## 读取流程

读取按数据新鲜度从高到低依次查找：

```
MemTable（最新）
   ↓ 未找到
Immutable MemTable
   ↓ 未找到
L0 SSTable（可能多个文件，按新鲜度排序）
   ↓ 未找到
L1 SSTable（只需查一个文件，Key 不重叠）
   ↓ 未找到
L2 ... Ln
```

**L0 需要特殊处理：** L0 文件 Key 范围可能重叠，需先找出所有包含该 Key 的文件，再按新鲜度依次查找。L1 及以上只需查一个文件。

**Cache 加速：** LevelDB 维护两级 Cache：

- **Table Cache**：缓存 SSTable 文件句柄和 Index，避免重复打开文件和读取索引
- **Block Cache**（可配置）：缓存 Data Block 内容，减少磁盘读次数

最优情况下（L0 命中），一次读取只需 2 次磁盘 I/O：读 Index + 读 Block。

---

## Compaction

### 两种类型

**Minor Compaction：** 将 Immutable MemTable 按 Key 顺序写入 L0 的新 SSTable 文件。此阶段不做物理删除，删除标记原样写入文件。

**Major Compaction：** 当某层文件数量或大小超过阈值，选取该层一个文件与下层 Key 范围有重叠的文件进行多路归并排序，生成新的下层文件，同时丢弃无效数据（被新版本覆盖的旧值、已标记删除的记录）。

文件选择采用**轮转策略**，每次选 Key 范围紧邻上次的文件，保证所有文件都有机会参与合并。

### Compaction 期间的磁盘 I/O

Compaction 是 LevelDB 读写放大的主要来源：

**读盘：** 读取参与合并的所有 SSTable 文件内容（L 层 + L+1 层），一次 major compaction 可能涉及数十个文件。

**写盘：** 将多路归并排序后的结果写入新的 SSTable 文件，写完后更新 Manifest。

**删除：** 合并完成后删除旧的 SSTable 文件。

**对业务的影响：**

- Compaction 和正常读写**争抢磁盘 I/O**，可能导致写入延迟抖动
- L0 文件积压过多时，LevelDB 会主动限速甚至暂停写入（write stall），等待 compaction 赶上
- 频繁删除数据会触发 Compaction，建议批量删除

**RocksDB 的改进：**

- 多线程并发 compaction
- Rate limiter 限制 compaction I/O 速率，降低对前台读写的影响
- 支持 Leveled / Universal 等多种 compaction 策略

---

## 版本管理

LevelDB 用三个概念管理文件版本：

- **Version**：保存某一时刻所有 SSTable 文件的快照。一般只有一个 current version，但被 Iterator 引用的旧版本会保持存活，因此 Iterator 用完要及时释放。
- **VersionEdit**：两个 Version 之间的增量变化（新增/删除了哪些文件），持久化到 Manifest 文件。
- **VersionSet**：管理所有存活 Version 的集合。

```
Version0 + VersionEdit → Version1
```

崩溃恢复时从 Manifest 读取 VersionEdit 重建状态，类似数据库的 redo log。这种设计类似图形学中的双缓冲切换：新版本生成后切换指针，旧版本在没有引用时才释放。

---

## 使用场景

### 持久化缓冲队列（削峰）

LevelDB 可以作为**持久化写缓冲**使用，实现「一边写入、一边读出」的管道模式：

- **写入端（Producer）**：将数据以递增的序列号或时间戳作为 Key 写入 LevelDB，得益于 LSM-Tree 架构，写入速度极快（顺序写磁盘），可以吸收突发流量峰值
- **读取端（Consumer）**：按 Key 顺序扫描读取，处理完毕后删除对应记录，以自身能处理的速率消费数据
- **数据持久化到磁盘**：与纯内存队列不同，LevelDB 的数据落盘，进程崩溃后数据不丢失，重启后可继续消费

这种模式可以起到**削峰填谷**的作用：写入端的流量高峰被 LevelDB 缓冲到磁盘，读取端按匀速消费，避免下游系统因瞬间流量过大而崩溃。

#### 适合此场景的条件

- 数据量超出内存容量，需要落盘缓冲
- 对消息顺序有要求（LevelDB Key 有序）
- 单机嵌入式场景，不想引入 Kafka/RabbitMQ 等重量级中间件
- 可以接受 LevelDB 不提供原生队列语义（需要自行管理消费位点和删除逻辑）

#### 注意事项

- LevelDB 不是消息队列，没有 ACK、重试、多消费者等内置机制，需要自行实现
- 频繁删除已消费数据会触发 Compaction，建议批量删除
- 如果对高吞吐、多消费者、分布式有需求，优先考虑 Kafka 等专用消息队列

### 其他典型场景

- **本地缓存层**：缓存热点数据到本地磁盘，减少远端数据库访问
- **索引存储**：存储倒排索引、元数据索引等有序 KV 数据
- **嵌入式数据库**：Chrome 浏览器使用 LevelDB 存储 IndexedDB 数据
- **区块链节点**：比特币、以太坊节点使用 LevelDB 存储区块链状态数据

---

## Maven 依赖（Java）

```xml
<dependency>
    <groupId>org.fusesource.leveldbjni</groupId>
    <artifactId>leveldbjni-linux64</artifactId>
    <version>1.8</version>
</dependency>
<dependency>
    <groupId>org.iq80.leveldb</groupId>
    <artifactId>leveldb-api</artifactId>
    <version>0.12</version>
</dependency>
```

---

## 参考资料

- [google/leveldb](https://github.com/google/leveldb)
- [fusesource/leveldbjni](https://github.com/fusesource/leveldbjni)（JNI 绑定）
- [dain/leveldb](https://github.com/dain/leveldb)（Pure Java 实现）
- [庖丁解 LevelDB 之数据存储](https://catkang.github.io/2017/01/17/leveldb-data.html)
- [WiscKey: Separating Keys from Values in SSD-Conscious Storage](https://www.scienjus.com/wisckey/)
