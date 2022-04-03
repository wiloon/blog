---
title: LSM-Tree
author: "-"
date: 2012-03-22T06:42:03+00:00
url: lsmtree
categories:
  - Linux
tags:
  - reprint
---
## LSM-Tree
## LSM-Tree, Log Structured Merge Tree
LSM-Tree 能将离散的随机写请求都转换成批量的顺序写请求 (WAL + Compaction），以此提高写性能。

十多年前，谷歌发布了大名鼎鼎的"三驾马车"的论文，分别是 GFS(2003年)，MapReduce (2004年），BigTable (2006年），为开源界在大数据领域带来了无数的灵感，其中在 “BigTable” 的论文中很多很酷的方面之一就是它所使用的文件组织方式，这个方法更一般的名字叫 Log Structured-Merge Tree。在面对亿级别之上的海量数据的存储和检索的场景下，我们选择的数据库通常都是各种强力的NoSQL，比如 Hbase, Cassandra, Leveldb, RocksDB 等等，这其中前两者是 Apache 下面的顶级开源项目数据库，后两者分别是 Google 和 Facebook 开源的数据库存储引擎。而这些强大的 NoSQL 数据库都有一个共性，就是其底层使用的数据结构，都是仿照 "BigTable" 中的文件组织方式来实现的，也就是我们今天要介绍的 LSM-Tree。

influxdb 使用的 TSM 存储引擎也是根据 LSM Tree 针对时间序列数据优化而来

### 什么是 LSM-Tree
LSM-Tree全称是 Log Structured Merge Tree，是一种分层，有序，面向磁盘的数据结构，其核心思想是充分了利用了磁盘**批量的顺序写**要远比**随机写**性能高出很多的特性

围绕这一原理进行设计和优化，以此让写性能达到最优，正如我们普通的 Log 的写入方式，这种结构的写入，全部都是以 **Append模式** 追加，不存在删除和修改。当然有得就有舍，这种结构虽然大大提升了数据的写入能力，却是以牺牲部分读取性能为代价，故此这种结构通常适合于写多读少的场景。故 LSM 被设计来提供比传统的 **B+树** 更好的写操作吞吐量，通过消去随机的本地更新操作来达到这个目标。这里面最典型的例子就是 Kakfa 了，把磁盘顺序写发挥到了极致，故而在大数据领域成为了互联网公司标配的分布式消息中间件组件。

虽然这种结构的写非常简单高效，但其缺点是对读取特别是**随机读**很不友好，这也是为什么日志通常用在下面的两种简单的场景：

1. 数据是被整体访问的，大多数数据库的 **WAL (write ahead log）** 也称 **预写log**，包括 mysql 的 Binlog 等
2. 数据是通过文件的偏移量offset访问的，比如 Kafka。

想要支持更复杂和高效的读取，比如按key查询和按range查询，就得需要做一步的设计，这也是LSM-Tree结构，除了利用磁盘顺序写之外，还划分了 **内存+磁盘** 多层的合并结构的原因，正是基于这种结构再加上不同的优化实现，才造就了在这之上的各种独具特点的 NoSQL 数据库，如 Hbase，Cassandra，Leveldb，RocksDB，MongoDB, TiDB 等。

### SSTable, Sorted String Table
提到 LSM-Tree 这种结构，就得提一下 LevelDB 这个存储引擎，我们知道 Bigtable 是谷歌开源的一篇论文，很难接触到它的源代码实现。如果说 Bigtable 是分布式闭源的一个高性能的KV系统，那么 LevelDB 就是这个KV系统开源的单机版实现，最为重要的是 LevelDB 是由 Bigtable 的原作者 Jeff Dean 和 Sanjay Ghemawat 共同完成，可以说高度复刻了Bigtable 论文中对于其实现的描述。

在 LSM-Tree 里面，核心的数据结构就是 SSTable, 全称是 **Sorted String Table**，SSTable 的概念其实也是来自于 Google 的 Bigtable 论文，论文中对 SSTable 的描述如下：

An SSTable provides a persistent, ordered immutable map from keys to values, where both keys and values are arbitrary byte strings. Operations are provided to look up the value associated with a specified key, and to iterate over all key/value pairs in a specified key range. Internally, each SSTable contains a sequence of blocks (typically each block is 64KB in size, but this is configurable). A block index (stored at the end of the SSTable) is used to locate blocks; the index is loaded into memory when the SSTable is opened. A lookup can be performed with a single disk seek: we first find the appropriate block by performing a binary search in the in-memory index, and then reading the appropriate block from disk. Optionally, an SSTable can be completely mapped into memory, which allows us to perform lookups and scans without touching disk.

如上所述, SSTable 是一种拥有持久化，有序且不可变的的键值存储结构，它的key和value都是任意的字节数组，并且了提供了按指定key 查找和指定范围的 key 区间迭代遍历的功能。SSTable 内部包含了一系列可配置大小的Block块，典型的大小是 64KB，关于这些Block 块的 index 存储在 SSTable 的尾部，用于帮助快速查找特定的Block。当一个SSTable被打开的时候，index会被加载到内存，然后根据key在内存index里面进行一个二分查找，查到该key对应的磁盘的offset之后，然后去磁盘把响应的块数据读取出来。当然如果内存足够大的话，可以直接把SSTable直接通过 MMap 的技术映射到内存中，从而提供更快的查找。 

每层SSTable文件到达一定条件后，进行合并操作，然后放置到更高层。
Level 0可以认为是MemTable的文件映射内存, 因此每个Level 0的SSTable之间的key range可能会有重叠。其他Level的SSTable key range不存在重叠。
Level 0的写入是简单的创建-->顺序写流程，因此理论上，写磁盘的速度可以接近磁盘的理论速度。

SSTable合并类似于简单的归并排序：根据key值确定要merge的文件，然后进行合并。因此，合并一个文件到更高层，可能会需要写多个文件。存在一定程度的写放大。是非常昂贵的I/O操作行为

在LSM-Tree里, SSTable 有一份在内存里面，其他的多级在磁盘上，如下图是一份完整的LSM-Tree图示：
[![7uvUJO.png](https://s4.ax1x.com/2022/01/12/7uvUJO.png)](https://imgtu.com/i/7uvUJO)
[![7uvALn.png](https://s4.ax1x.com/2022/01/12/7uvALn.png)](https://imgtu.com/i/7uvALn)
[![7uvuJU.jpg](https://s4.ax1x.com/2022/01/12/7uvuJU.jpg)](https://imgtu.com/i/7uvuJU)

我们总结下在在LSM-Tree里面如何写数据的？

1，当收到一个写请求时，会先把该条数据记录在WAL Log里面，用作故障恢复。

2，当写完WAL Log后，会把该条数据写入内存的SSTable里面 (删除是墓碑标记，更新是新记录一条的数据），也称 Memtable. 注意为了维持有序性在内存里面可以采用红黑树或者跳跃表相关的数据结构。

3，当Memtable超过一定的大小后，会在内存里面冻结，变成不可变的Memtable，同时为了不阻塞写操作需要新生成一个Memtable继续提供服务。

4，把内存里面不可变的Memtable给dump到到硬盘上的SSTable层中，此步骤也称为Minor Compaction，这里需要注意在L0层的SSTable是没有进行合并的，所以这里的key range在多个SSTable中可能会出现重叠，在层数大于0层之后的SSTable，不存在重叠key。

5，当每层的磁盘上的SSTable的体积超过一定的大小或者个数，也会周期的进行合并。此步骤也称为Major Compaction，这个阶段会真正 的清除掉被标记删除掉的数据以及多版本数据的合并，避免浪费空间，注意由于SSTable都是有序的，我们可以直接采用merge sort进行高效合并。

### MemTable
MemTable 对应的就是 WAL 文件，是该文件内容在内存中的存储结构，通常用 SkipList 来实现。

MemTable: LSM Tree的树节点可以分为两种，保存在内存中的称之为MemTable, 保存在磁盘上的称之为SSTable. 严格讲，MemTable与SSTable还有很多细节区别.


### Immutable Memtable
顾名思义，Immutable Memtable 就是在内存中只读的 MemTable，由于内存是有限的，通常我们会设置一个阀值，当 MemTable 占用的内存达到阀值后就自动转换为 Immutable Memtable，Immutable Memtable 和 MemTable 的区别就是它是只读的，系统此时会生成新的 MemTable 供写操作继续写入。

之所以要使用 Immutable Memtable，就是为了避免将 MemTable 中的内容序列化到磁盘中时会阻塞写操作。


接着我们总结下在LSM-Tree里面如何读数据的？

1，当收到一个读请求的时候，会直接先在内存里面查询，如果查询到就返回。

2，如果没有查询到就会依次下沉，知道把所有的Level层查询一遍得到最终结果。

思考查询步骤，我们会发现如果SSTable的分层越多，那么最坏的情况下要把所有的分层扫描一遍，对于这种情况肯定是需要优化的，如何优化？在 Bigtable 论文中提出了几种方式：

1，压缩

SSTable 是可以启用压缩功能的，并且这种压缩不是将整个 SSTable 一起压缩，而是根据 locality 将数据分组，每个组分别压缩，这样的好处当读取数据的时候，我们不需要解压缩整个文件而是解压缩部分 Group 就可以读取。

2，缓存

因为SSTable在写入磁盘后，除了Compaction之外，是不会变化的，所以我可以将Scan的Block进行缓存，从而提高检索的效率

3，索引，Bloom filters

正常情况下，一个读操作是需要读取所有的 SSTable 将结果合并后返回的，但是对于某些 key 而言，有些 SSTable 是根本不包含对应数据的，因此，我们可以对每一个 SSTable 添加 Bloom Filter，因为布隆过滤器在判断一个SSTable不存在某个key的时候，那么就一定不会存在，利用这个特性可以减少不必要的磁盘扫描。

4，合并

这个在前面的写入流程中已经介绍过，通过定期合并瘦身， 可以有效的清除无效数据，缩短读取路径，提高磁盘利用空间。但Compaction操作是非常消耗CPU和磁盘IO的，尤其是在业务高峰期，如果发生了Major Compaction，则会降低整个系统的吞吐量，这也是一些NoSQL数据库，比如Hbase里面常常会禁用Major Compaction，并在凌晨业务低峰期进行合并的原因。

最后有的同学可能会问道，为什么LSM不直接顺序写入磁盘，而是需要在内存中缓冲一下？ 这个问题其实很容易解答，单条写的性能肯定没有批量写来的块，这个原理其实在Kafka里面也是一样的，虽然kafka给我们的感觉是写入后就落地，但其实并不是，本身是 可以根据条数或者时间比如200ms刷入磁盘一次，这样能大大提升写入效率。此外在LSM中，在磁盘缓冲的另一个好处是，针对新增的数据，可以直接查询返回，能够避免一定的IO操作。

### B+Tree VS LSM-Tree
传统关系型数据采用的底层数据结构是B+树，那么同样是面向磁盘存储的数据结构LSM-Tree相比B+树有什么异同之处呢？

LSM-Tree的设计思路是，将数据拆分为几百M大小的Segments，并是顺序写入。

B+Tree则是将数据拆分为固定大小的Block或Page, 一般是4KB大小，和磁盘一个扇区的大小对应，Page是读写的最小单位。

在数据的更新和删除方面，B+Tree可以做到原地更新和删除，这种方式对数据库事务支持更加友好，因为一个key只会出现一个Page页里面，但由于LSM-Tree只能追加写，并且在L0层key的rang会重叠，所以对事务支持较弱，只能在Segment Compaction的时候进行真正地更新和删除。

因此LSM-Tree的优点是支持高吞吐的写 (可认为是O (1）），这个特点在分布式系统上更为看重，当然针对读取普通的LSM-Tree结构，读取是O (N）的复杂度，在使用索引或者缓存优化后的也可以达到O (logN）的复杂度。

而B+tree的优点是支持高效的读 (稳定的OlogN），但是在大规模的写请求下 (复杂度O(LogN)），效率会变得比较低，因为随着insert的操作，为了维护B+树结构，节点会不断的分裂和合并。操作磁盘的随机读写概率会变大，故导致性能降低。

还有一点需要提到的是基于LSM-Tree分层存储能够做到写的高吞吐，带来的副作用是整个系统必须频繁的进行compaction，写入量越大，Compaction的过程越频繁。而compaction是一个compare & merge的过程，非常消耗CPU和存储IO，在高吞吐的写入情形下，大量的compaction操作占用大量系统资源，必然带来整个系统性能断崖式下跌，对应用系统产生巨大影响，当然我们可以禁用自动Major Compaction，在每天系统低峰期定期触发合并，来避免这个问题。

阿里为了优化这个问题，在X-DB引入了异构硬件设备FPGA来代替CPU完成compaction操作，使系统整体性能维持在高水位并避免抖动，是存储引擎得以服务业务苛刻要求的关键。

总结
本文主要介绍了LSM-Tree的相关内容，简单的说，其牺牲了部分读取的性能，通过批量顺序写来换取了高吞吐的写性能，这种特性在大数据领域得到充分了体现，最直接的例子就各种NoSQL在大数据领域的应用，学习和了解LSM-Tree的结构将有助于我们更加深入的去理解相关NoSQL数据库的实现原理，掌握隐藏在这些框架下面的核心知识。

### 读放大 (Read Amplification）
LSM-Tree 的读操作需要从新到旧 (从上到下）一层一层查找，直到找到想要的数据。这个过程可能需要不止一次 I/O。特别是 range query 的情况，影响很明显。
### 空间放大 (Space Amplification）
因为所有的写入都是顺序写 (append-only）的，不是 in-place update ，所以过期数据不会马上被清理掉。
### 写放大 Write Amplification
RocksDB 和 LevelDB 通过后台的 compaction 来减少读放大 (减少 SST 文件数量）和空间放大 (清理过期数据），但也因此带来了写放大 (Write Amplification）的问题。

基于LSM树的KV系统的Merge操作造成的写放大
levelDB等KV存储广泛采用了LSM树等结构进行存储组织，其特点就是靠上的level的数据会最终被merge sort到下层，由于多数level在磁盘文件中，这也就导致了同一KV数据的总写放大，放大的倍数就是大约是level的数目。和前边4中写放大不同的是，这种写放大并非写操作时马上就会发生写放大，而是写操作发生时会潜在的导致“未来会发生”写放大，所以这种写放大只会导致整体写代价提升，不会影响实时的延迟性能，只可能会影响磁盘带宽或者在SSD做存储设备时影响闪存耐久。FAST 16上有篇论文也专门分析了这种写放大。[8]
>http://blog.jcix.top/2018-06-05/write_amplification/
>https://cloud.tencent.com/developer/article/1441835
>http://distributeddatastore.blogspot.com/2013/08/cassandra-sstable-storage-format.html
>https://liudanking.com/arch/lsm-tree-summary/
>https://blog.fatedier.com/2016/06/15/learn-lsm-tree/
