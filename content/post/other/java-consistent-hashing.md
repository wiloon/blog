---
title: 一致性哈希算法与Java实现
author: "-"
date: 2012-05-28T07:05:44+00:00
url: /?p=3276
categories:
  - Algorithm
tags:
  - reprint
  - Java
---
## 一致性哈希算法与Java实现

## 一致性哈希算法, consistent hashing

  1. 概述
  2. 引出
  3. 登场
  4. 改进-虚节点
  5. 另一种改进
  
    参考链接: 

  6. 概述
  
    在维基百科中，是这么定义的
  
    一致哈希是一种特殊的哈希算法。在使用一致哈希算法后，哈希表槽位数 (大小) 的改变平均只需要对 K/n个关键字重新映射，其中K是关键字的数量， n是槽位数量。然而在传统的哈希表中，添加或删除一个槽位的几乎需要对所有关键字进行重新映射。

  7. 引出
  
    我们在上文中已经介绍了一致性Hash算法的基本优势，我们看到了该算法主要解决的问题是: 当slot数发生变化时，能够尽量少的移动数据。那么，我们思考一下，普通的Hash算法是如何实现？又存在什么问题呢？
  
    那么我们引出一个问题: 
  
    假设有1000w个数据项，100个存储节点，请设计一种算法合理地将他们存储在这些节点上。
  
    看一看普通Hash算法的原理: 
  
    normal_hash
  
    算法的核心计算如下
  
    1
  
    2
  
    3
  
    4
  
    5
  
    6
  
    for item in range(ITEMS):
  
    k = md5(str(item)).digest()
  
    h = unpack_from(">I", k)[0]
  
    # 通过取余的方式进行映射
  
    n = h % NODES
  
    node_stat[n] += 1
  
    具体的完整实现请参考normal_hash.py，输出是这样的: 
  
    Ave: 100000
  
    Max: 100695 (0.69%)
  
    Min: 99073 (0.93%)
  
    从上述结果可以发现，普通的Hash算法均匀地将这些数据项打散到了这些节点上，并且分布最少和最多的存储节点数据项数目小于1%。之所以分布均匀，主要是依赖Hash算法 (实现使用的MD5算法) 能够比较随机的分布。
  
    然而，我们看看存在一个问题，由于该算法使用节点数取余的方法，强依赖node的数目，因此，当是node数发生变化的时候，item所对应的node发生剧烈变化，而发生变化的成本就是我们需要在node数发生变化的时候，数据需要迁移，这对存储产品来说显然是不能忍的，我们观察一下增加node后，数据项移动的情况: 
  
    1
  
    2
  
    3
  
    4
  
    5
  
    6
  
    7
  
    8
  
    9
  
    for item in range(ITEMS):
  
    k = md5(str(item)).digest()
  
    h = unpack_from(">I", k)[0]
  
    # 原映射结果
  
    n = h % NODES
  
    # 现映射结果
  
    n_new = h % NEW_NODES
  
    if n_new != n:
      
    change += 1
  
    详细实现代码在normal_hash_add.py输出是这样的: 
  
    Change: 9900989 (99.01%)
  
    翻译一下就是，如果有100个item，当增加一个node，之前99%的数据都需要重新移动。
  
    这显然是不能忍的，普通哈希算法的问题我们已经发现了，如何对其进行改进呢？没错，我们的一致性哈希算法闪亮登场。

  8. 登场
  
    我们上节介绍了普通Hash算法的劣势，即当node数发生变化 (增加、移除) 后，数据项会被重新"打散"，导致大部分数据项不能落到原来的节点上，从而导致大量数据需要迁移。
  
    那么，一个亟待解决的问题就变成了: 当node数发生变化时，如何保证尽量少引起迁移呢？即当增加或者删除节点时，对于大多数item，保证原来分配到的某个node，现在仍然应该分配到那个node，将数据迁移量的降到最低。
  
    一致性Hash算法的原理是这样的: 
  
    consist_hash
  
    1
  
    2
  
    3
  
    4
  
    5
  
    6
  
    7
  
    8
  
    9
  
    10
  
    for n in range(NODES):
  
    h = _hash(n)
  
    ring.append(h)
  
    ring.sort()
  
    hash2node[h] = n

for item in range(ITEMS):

h = _hash(item)

n = bisect_left(ring, h) % NODES

node_stat[hash2node[ring[n]]] += 1
  
我们依然对其进行了实现consist_hash_add.py，并且观察了数据迁移的结果:
  
Change: 235603 (2.36%)
  
虽然一致性Hash算法解决了节点变化导致的数据迁移问题，但是，我们回过头来再看看数据项分布的均匀性，进行了一致性Hash算法的实现consist_hash.py:
  
Ave: 100000
  
Max: 596413 (496.41%)
  
Min: 103 (99.90%)
  
这结果简直是简直了，确实非常结果差，分配的很不均匀。我们思考一下，一致性哈希算法分布不均匀的原因是什么？从最初的1000w个数据项经过一般的哈希算法的模拟来看，这些数据项"打散"后，是可以比较均匀分布的。但是引入一致性哈希算法后，为什么就不均匀呢？数据项本身的哈希值并未发生变化，变化的是判断数据项哈希应该落到哪个节点的算法变了。
  
consist_hash_1
  
因此，主要是因为这100个节点Hash后，在环上分布不均匀，导致了每个节点实际占据环上的区间大小不一造成的。
  
3. 改进-虚节点
  
当我们将node进行哈希后，这些值并没有均匀地落在环上，因此，最终会导致，这些节点所管辖的范围并不均匀，最终导致了数据分布的不均匀。
  
consist_hash_virtual
  
详细实现请见virtual_consist_hash.py
  
for n in range(NODES):

for v in range(VNODES):

h = _hash(str(n) + str(v))

# 构造ring

ring.append(h)

# 记录hash所对应节点

hash2node[h] = n
  
ring.sort()

for item in range(ITEMS):

h = _hash(str(item))

# 搜索ring上最近的hash

n = bisect_left(ring, h) % (NODES*VNODES)

node_stat[hash2node[ring[n]]] += 1
  
输出结果是这样的:
  
Ave: 100000
  
Max: 116902 (16.90%)
  
Min: 9492 (90.51%)
  
因此，通过增加虚节点的方法，使得每个节点在环上所"管辖"更加均匀。这样就既保证了在节点变化时，尽可能小的影响数据分布的变化，而同时又保证了数据分布的均匀。也就是靠增加"节点数量"加强管辖区间的均匀。
  
同时，观察增加节点后数据变动情况，详细的代码请见virtual_consist_hash_add.py:
  
for item in range(ITEMS):

h = _hash(str(item))

n = bisect_left(ring, h) % (NODES*VNODES)

n2 = bisect_left(ring2, h) % (NODES2*VNODES)

if hash2node[ring[n]] != hash2node2[ring2[n2]]:

change += 1
  
100000
  
101000
  
Change: 104871 (1.05%)
  
3. 另一种改进
  
然而，虚节点这种靠数量取胜的策略增加了存储这些虚节点信息所需要的空间。在OpenStack的Swift组件中，使用了一种比较特殊的方法来解决分布不均的问题，改进了这些数据分布的算法，将环上的空间均匀的映射到一个线性空间，这样，就保证分布的均匀性。
  
consist_hash_ring
  
代码实现见part_consist_hash.py
  
for part in range(2 ** LOG_NODE):

ring.append(part)

part2node[part] = part % NODES

for item in range(ITEMS):

h = _hash(item) >> PARTITION

part = bisect_left(ring, h)

n = part % NODES

node_stat[n] += 1
  
Ave: 100000
  
Max: 157298 (57.30%)
  
Min: 77405 (22.59%)
  
可以看到，数据分布是比较理想的。如果节点数刚好和分区数相等，理论上是可以均匀分布的。而观察下增加节点后的数据移动比例，代码实现见part_consist_hash.py
  
15

for part in range(2 ** LOG_NODE):

ring.append(part)

part2node[part] = part % NODES

part2node2[part] = part % NODES2

change = 0
  
for item in range(ITEMS):

h = _hash(item) >> PARTITION

p = bisect_left(ring, h)

p2 = bisect_left(ring, h)

n = part2node[p] % NODES

n2 = part2node2[p] % NODES2

if n2 != n:

change += 1
  
结果如下所示:
  
Change: 2190208 (21.90%)
  
可以看到，移动也是比较理想的。
  
参考链接:
  
深入云存储系统Swift核心组件: Ring实现原理剖析
  
Basic Hash Ring
  
Partition Ring vs. Hash Ring

    一致性哈希算法是分布式系统中常用的算法。比如，一个分布式的存储系统，要将数据存储到具体的节点上，如果采用普通的hash方法，将数据映射到具体的节点上，如key%N，key是数据的key，N是机器节点数，如果有一个机器加入或退出这个集群，则所有的数据映射都无效了，如果是持久化存储则要做数据迁移，如果是分布式缓存，则其他缓存就失效了。
    因此，引入了一致性哈希算法: 

把数据用hash函数 (如MD5) ，映射到一个很大的空间里，如图所示。数据的存储时，先得到一个hash值，对应到这个环中的每个位置，如k1对应到了图中所示的位置，然后沿顺时针找到一个机器节点B，将k1存储到B这个节点中。
  
如果B节点宕机了，则B上的数据就会落到C节点上，如下图所示:

这样，只会影响C节点，对其他的节点A，D的数据不会造成影响。然而，这又会造成一个"雪崩"的情况，即C节点由于承担了B节点的数据，所以C节点的负载会变高，C节点很容易也宕机，这样依次下去，这样造成整个集群都挂了。

为此，引入了"虚拟节点"的概念: 即把想象在这个环上有很多"虚拟节点"，数据的存储是沿着环的顺时针方向找一个虚拟节点，每个虚拟节点都会关联到一个真实节点，如下图所使用:

图中的A1、A2、B1、B2、C1、C2、D1、D2都是虚拟节点，机器A负载存储A1、A2的数据，机器B负载存储B1、B2的数据，机器C负载存储C1、C2的数据。由于这些虚拟节点数量很多，均匀分布，因此不会造成"雪崩"现象。
  
Java实现:

```java
  
public class Shard<S> { // S类封装了机器节点的信息 ，如name、password、ip、port等 

private TreeMap<Long, S> nodes; // 虚拟节点
      
private List<S> shards; // 真实机器节点
      
private final int NODE_NUM = 100; // 每个机器节点关联的虚拟节点个数 

public Shard(List<S> shards) {
          
super();
          
this.shards = shards;
          
init();
      
} 

private void init() { // 初始化一致性hash环
          
nodes = new TreeMap<Long, S>();
          
for (int i = 0; i != shards.size(); ++i) { // 每个真实机器节点都需要关联虚拟节点
              
final S shardInfo = shards.get(i); 

for (int n = 0; n < NODE_NUM; n++)
                  
// 一个真实机器节点关联NODE_NUM个虚拟节点
                  
nodes.put(hash("SHARD-" + i + "-NODE-" + n), shardInfo); 

}
      
} 

public S getShardInfo(String key) {
          
SortedMap<Long, S> tail = nodes.tailMap(hash(key)); // 沿环的顺时针找到一个虚拟节点
          
if (tail.size() == 0) {
              
return nodes.get(nodes.firstKey());
          
}
          
return tail.get(tail.firstKey()); // 返回该虚拟节点对应的真实机器节点的信息
      
} 

/**
       
* MurMurHash算法，是非加密HASH算法，性能很高，
       
* 比传统的CRC32,MD5，SHA-1 (这两个算法都是加密HASH算法，复杂度本身就很高，带来的性能上的损害也不可避免) 
       
* 等HASH算法要快很多，而且据说这个算法的碰撞率很低.
       
* http://murmurhash.googlepages.com/
       
*/
      
private Long hash(String key) { 

ByteBuffer buf = ByteBuffer.wrap(key.getBytes());
          
int seed = 0x1234ABCD; 

ByteOrder byteOrder = buf.order();
          
buf.order(ByteOrder.LITTLE_ENDIAN); 

long m = 0xc6a4a7935bd1e995L;
          
int r = 47; 

long h = seed ^ (buf.remaining() * m); 

long k;
          
while (buf.remaining() >= 8) {
              
k = buf.getLong(); 

k *= m;
              
k ^= k >>> r;
              
k *= m; 

h ^= k;
              
h *= m;
          
} 

if (buf.remaining() > 0) {
              
ByteBuffer finish = ByteBuffer.allocate(8).order(
                      
ByteOrder.LITTLE_ENDIAN);
              
// for big-endian version, do this first:
              
// finish.position(8-buf.remaining());
              
finish.put(buf).rewind();
              
h ^= finish.getLong();
              
h *= m;
          
} 

h ^= h >>> r;
          
h *= m;
          
h ^= h >>> r; 

buf.order(byteOrder);
          
return h;
      
} 

}
  
```

[http://yikun.github.io/2016/06/09/%E4%B8%80%E8%87%B4%E6%80%A7%E5%93%88%E5%B8%8C%E7%AE%97%E6%B3%95%E7%9A%84%E7%90%86%E8%A7%A3%E4%B8%8E%E5%AE%9E%E8%B7%B5/](http://yikun.github.io/2016/06/09/%E4%B8%80%E8%87%B4%E6%80%A7%E5%93%88%E5%B8%8C%E7%AE%97%E6%B3%95%E7%9A%84%E7%90%86%E8%A7%A3%E4%B8%8E%E5%AE%9E%E8%B7%B5/)
  
[http://blog.csdn.net/wuhuan_wp/article/details/7010071](http://blog.csdn.net/wuhuan_wp/article/details/7010071)

[https://segmentfault.com/a/1190000021199728](https://segmentfault.com/a/1190000021199728)  
[https://blog.csdn.net/suifeng629/article/details/81567777](https://blog.csdn.net/suifeng629/article/details/81567777)
