---
title: influxdb lsm tsm
author: "-"
date: 2012-01-13T15:46:12+00:00
url: /?p=2141
categories:
  - inbox

---
## influxdb lsm tsm
底层采用自研的TSM存储引擎，TSM也是基于LSM的思想，提供极强的写能力以及高压缩率。

### 数据库
数据库的本质上是完成四件事情，1. 插入数据， 2. 删除数据， 3. 修改数据 ， 4. 查询数据。 也就是我们常说的CURD。
市面上现在流行的数据库大致有两类， 1. 基于日志结构的储存引擎。大部分的Nosql 数据库都是此类， 面向页的存储引擎， Mysql
### 极简key-value型数据库
第一版需要实现的功能： 1. 插入数据 2. 查询数据

#！/bin/hash
db_set() {
	echo "$1,$2" >> database
}
db_get() {
	grep "^$1, "database | sed -e "s/^$1,//" | tail -n 1
}
上面我们用两个Bash 函数实现了一个Key-value型数据库，用文件读写的方式将数据记录到磁盘上。 每行是用逗号分割的key，value 形式。 （这种存储方式也叫CSV文件格式）

db_set() ： 追加到文件尾
db_get() ： 遍历所有匹配key 的行， 用sed 命令把key， 替换成空字符串， 并输出最后一行。 


至于删除， 我们可以再写入一条数据， 在key，value 后面追加一个墓碑标记。 查询的时候，如果最新的一条数据有墓碑标记， 则代表该数据已被删除。

考虑下这个数据库的性能：

1. 空间上： 当我们修改key 对应的值， 是采用追加写入文件的方式， 会造成存在很多重复的键， 过于占用磁盘空间， 当使用一段时间，磁盘空间可能就会被耗尽。

2. 时间上： 读数据需要整体遍历一遍文件， 当我们数据量非常大的时候查询速度将会变得非常慢。 对于一个数据库， 我们认为查询数据的时候O(logn) 或者O(1)的时间复杂度是可接受的。

hashmap索引的分段式数据库
空间耗尽问题 的解决方案：

将日志分解成一定大小的段（文件）， 为每个文件设一个固定大小的阈值， 还是追加写入文件， 当文件大小超过阈值， 就关闭当前文件， 把数据写入新的文件。

在后台开启一个线程， 定期对旧的文件进行合并， 每个key 上只保留最新的value ， 如果最新的key，value 上发现了墓碑标记， 则删除 该标记。

检索时间问题 的解决方案：

在内存中建立hashmap ， 因为内存比硬盘的访问速度要更快。 hash 表的key 存数据的key ，hashmap 的值存 在文件中的偏移量。
每个段文件都维持自己的hash 表。
检索流程：首先检查最新的段的hashmap ， 如果键不存在， 检查第二最新的段，以此类推。

上面为了方便理解， 用的是CSV 格式讲解， 真实存储的时候使用二进制格式， 字符串长度 + 原始字符串。
崩溃恢复： 内存中的索引断电可能会丢失， 可以将每个段的hash map 的快照存在磁盘上。
至此我们的实现方式可以总结为： 追加写 + 分段合并 + 分段hash索引 + 标记删除

SSTable 和 LSM-Tree
SSTable 全称叫做排序字符串表， 对于我们上面的解决方案， 还有一个问题， 就是文件中每个段的key 我们都要存到内存中，虽然每个段都可以进行压缩，但占用的内存空间还是太大了。

解决方案： 我们可以简单的改变文件的格式， 要求key - value 对的顺序按键进行排序。

注意前提条件： 每个段经过压缩之后， 每个键在每个段文件只能出现一次。

SSTable 的优势：

因为键已经进行过排序了， 所以在后台进程进行段合并的时候更加高效， 类似于大数据多路归并排序问题。文件的大小可以大于可用内存。
内存中不需要保存所有键的索引。 内存索引可以是稀疏的。 比如 有三个键， handwork ， handbag 和 handsome ， 内存中可以只保存两个键 handbag 和 hand some ， 搜索的时候先跳到handbag ， 然后开始扫描直到找到handwork。
五. SSTable 的实现
下面我们来想一下如何高效的实现key 的排序结构 。

现在已经有了很多成熟的数据结构可以进行数据高效的动态排序， 例如红黑树。 我们可以在内存中进行排序之后再写入数据库。


sstables 的基本工作流程
写入到内存中的平衡二叉树中（内存表）
当内存表大于某个阈值， 将其写入磁盘并创建新的sstable。
查找的时候先查找内存， 然后查找最新的磁盘段文件， 然后次新， 直到找到目标。
后台周期型的执行段合并和压缩（多路归并）。
写入日志预防崩溃。
六. 总结
上面所描述的算法流程正式levelDB 和RocksDB 所使用的。 它的名字叫做日志结构合并树（LSM-Tree）。

在它落地的过程中， 还有一些细节进行了输入的优化。

例如： 查找每个不存在的键， LSM-Tree 会变得很慢。 优化方案： 布隆过滤器。

关于SStables 的压缩和合并式的具体顺序和时机。 各个存储引擎也有所不同， 常见的有分层压缩（LevelDB） 和大小分级（HBase）。

LSM-Tree 基本思想：

顺序写入， 支持高吞度量。
key 按字典序排序， 稀疏存储，使数据集可以远大于可用内存。


LSM 的局限性

在官方文档上有写， 为了解决高写入吞吐量的问题， Influxdb 一开始选择了LevelDB 作为其存储引擎。 然而，随着更多地了解人们对时间序列数据的需求，influxdb遇到了一些无法克服的挑战。

LSM （日志结构合并树）为 LevelDB的引擎原理， 具体细节可以参考。 LSM 树原理详解

levelDB 不支持热备份。 对数据库进行安全备份必须关闭后才能复制。LevelDB的RocksDB和HyperLevelDB变体可以解决此问题。
时序数据库需要提供一种自动管理数据保存的方式。 即删除过期数据， 而在levelDB 中，删除的代价过高。（通过添加墓碑的方式， 段结构合并的时候才会真正物理性的删除）。


InfluxDB 的解决方案 - TSM
按不同的时间范围划分为不同的分区（Shard），因为时序数据写入都是按时间线性产生的，所以分区的产生也是按时间线性增长的，写入通常是在最新的分区，而不会散列到多个分区。分区的优点是数据回收的物理删除非常简单，直接把整个分区删除即可。

在最开始的时候， influxdb 采用的方案每个shard都是一个独立的数据库实例，底层都是一套独立的LevelDB存储引擎。 这时带来的问题是，LevelDB底层采用level compaction策略，每个存储引擎都会打开比较多的文件，随着shard的增多，最终进程打开的文件句柄会很快触及到上限。
由于遇到大量的客户反馈文件句柄过多的问题，InfluxDB在新版本的存储引擎选型中选择了BoltDB替换LevelDB。BoltDB底层数据结构是mmap B+树。 但由于B+ 树会产生大量的随机写。 所以写入性能较差。
之后Influxdb 最终决定仿照LSM 的思想自研TSM ，主要改进点是基于时序数据库的特性作出一些优化，包含Cache、WAL以及Data File等各个组件，也会有flush、compaction等这类数据操作。


>https://zhuanlan.zhihu.com/p/65483906
>https://zhuanlan.zhihu.com/p/97247465