---
title: "redis list"
author: "-"
date: "2021-07-04 15:29:28"
url: "template"
categories:
  - inbox
tags:
  - inbox
---
## "redis list"
### linkedlist
每个node包含了三个部分，指向前一个节点和后一个节点的指针，以及一个数据值。而一个list包含了指向首尾的指针、整个list的长度，以及三个函数指针，用来复制节点的值、释放节点的值，以及比较节点内容。

### ziplist 压缩列表
ziplist是一种特殊编码的节省内存空间的双链表，能以O(1)的时间复杂度在两端push和pop数据
ziplist是redis中实现的一个地址连续的链表。  
每次操作都需要重新分配内存  
先看下官方对ziplist的整体描述

/* The ziplist is a specially encoded dually linked list that is designed

 * to be very memory efficient. It stores both strings and integer values,

 * where integers are encoded as actual integers instead of a series of

 * characters. It allows push and pop operations on either side of the list

 * in O(1) time. However, because every operation requires a reallocation of

 * the memory used by the ziplist, the actual complexity is related to the

 * amount of memory used by the ziplist.

 *

从上述的描述中，知道ziplist是一个经过特殊编码的双向链表，它的设计目标就是为了提高存储效率。ziplist可以用于存储字符串或整数，其中整数是按真正的二进制表示进行编码的，而不是编码成字符串序列。它能以O(1)的时间复杂度在表的两端提供push和pop操作。

一个普通的双向链表，链表中每一项都占用独立的一块内存，各项之间用地址指针 (或引用) 连接起来。这种方式会带来大量的内存碎片，而且地址指针也会占用额外的内存。而ziplist却是将表中每一项存放在前后连续的地址空间内。一个ziplist整体占用一大块内存，它是一个表 (list) ，但其实不是一个链表 (linked list) 。

ziplist为了节省内存，提高存储效率，对于值的存储采用了变长的编码方式，大概意思是说，对于大的整数，就多用一些字节来存储，而对于小的整数，就少用一些字节来存储。

二、ziplist数据结构定义

看下官方对ziplist整体布局

* ----------------------------------------------------------------------------

 *

 * ZIPLIST OVERALL LAYOUT:

 * The general layout of the ziplist is as follows:

 * <zlbytes><zltail><zllen><entry><entry><zlend>

 *

 * <zlbytes> is an unsigned integer to hold the number of bytes that the

 * ziplist occupies. This value needs to be stored to be able to resize the

 * entire structure without the need to traverse it first.

 *

 * <zltail> is the offset to the last entry in the list. This allows a pop

 * operation on the far side of the list without the need for full traversal.

 *

 * <zllen> is the number of entries.When this value is larger than 2**16-2,

 * we need to traverse the entire list to know how many items it holds.

 *

 * <zlend> is a single byte special value, equal to 255, which indicates the

 * end of the list.

 *

从以上的布局中，我们可以看到ziplist内存数据结构，由如下5部分构成: 



各个部分在内存上是前后相邻的并连续的，每一部分作用如下: 

zlbytes:  存储一个无符号整数，固定四个字节长度 (32bit) ，用于存储压缩列表所占用的字节 (也包括<zlbytes>本身占用的4个字节) ，当重新分配内存的时候使用，不需要遍历整个列表来计算内存大小。

zltail:  存储一个无符号整数，固定四个字节长度 (32bit) ，表示ziplist表中最后一项 (entry) 在ziplist中的偏移字节数。<zltail>的存在，使得我们可以很方便地找到最后一项 (不用遍历整个ziplist) ，从而可以在ziplist尾端快速地执行push或pop操作。

zllen:  压缩列表包含的节点个数，固定两个字节长度 (16bit) ， 表示ziplist中数据项 (entry) 的个数。由于zllen字段只有16bit，所以可以表达的最大值为2^16-1。

      注意点: 如果ziplist中数据项个数超过了16bit能表达的最大值，ziplist仍然可以表示。ziplist是如何做到的？

如果<zllen>小于等于2^16-2 (也就是不等于2^16-1) ，那么<zllen>就表示ziplist中数据项的个数；否则，也就是<zllen>等于16bit全为1的情况，那么<zllen>就不表示数据项个数了，这时候要想知道ziplist中数据项总数，那么必须对ziplist从头到尾遍历各个数据项，才能计数出来。

entry，表示真正存放数据的数据项，长度不定。一个数据项 (entry) 也有它自己的内部结构。

zlend， ziplist最后1个字节，值固定等于255，其是一个结束标记。


https://www.cnblogs.com/exceptioneye/p/7040815.html

### 连锁更新

前个节点的长度小于 254 的时候，用 1 个字节保存 prevlen
前个字节的长度大于等于 254 的时候，用 5 个字节保存 prevlen
现在我们来考虑一种情况: 假设一个压缩列表中，有多个长度 250 ~ 253 的节点，假设是 entry1 ~ entryN。
因为都是小于 254，所以都是用 1 个字节保存 prevlen。
如果此时，在压缩列表最前面，插入一个 254 长度的节点，此时它的长度需要 5 个字节。
也就是说 entry1.prevlen 会从 1 个字节变为 5 个字节，因为 prevlen 变长，entry1 的长度超过 254 了。
这下就糟糕了，entry2.prevlen 也会因为 entry1 而变长，entry2 长度也会超过 254 了。
然后接着 entry3 也会连锁更新。。。直到节点不超过 254， 噩梦终止。。。

这种由于一个节点的增删，后续节点变长而导致的连续重新分配内存的现象，就是连锁更新。最坏情况下，会导致整个压缩列表的所有节点都重新分配内存。

每次分配空间的最坏时间复杂度是 O(n)，所以连锁更新的最坏时间复杂度高达 O(n2) !

虽然说，连锁更新的时间复杂度高，但是它造成大的性能影响的概率很低，原因如下: 

压缩列表中需要需要有连续多个长度刚好为 250 ~ 253 的节点，才有可能发生连锁更新。实际上，这种情况并不多见。
即使有连续多个长度刚好为 250 ~ 253 的节点，连续的个数也不多，不会对性能造成很大影响
因此，压缩列表插入操作，平均复杂度还是 O(n).


ziplist其实是一个逻辑上的双向链表，可以快速找到头节点和尾节点，然后每个节点(entry)中也包含指向前/后节点的"指针"，但作者为了将内存节省到极致，摒弃了传统的链表设计(前后指针需要16字节的空间，而且会导致内存碎片化严重)，设计出了内存非常紧凑的存储格式。内存是省下来了，但操作复杂性也更新的复杂度上来了，当然Redis作者也考虑了这点，所以也设计出了ziplist和传统双向链表的折中——quicklist，我们将在下一篇博文中详细介绍quicklist。



### quicklist

Redis对外暴露的list数据类型，它底层实现所依赖的内部数据结构就是quicklist。

我们在讨论中还会涉及到两个Redis配置 (在redis.conf中的ADVANCED CONFIG部分) : 

list-max-ziplist-size -2
list-compress-depth 0
我们在讨论中会详细解释这两个配置的含义。

注: 本文讨论的quicklist实现基于Redis源码的3.2分支。

quicklist概述
Redis对外暴露的上层list数据类型，经常被用作队列使用。比如它支持的如下一些操作: 

lpush: 在左侧 (即列表头部) 插入数据。
rpop: 在右侧 (即列表尾部) 删除数据。
rpush: 在右侧 (即列表尾部) 插入数据。
lpop: 在左侧 (即列表头部) 删除数据。
这些操作都是O(1)时间复杂度的。

当然，list也支持在任意中间位置的存取操作，比如lindex和linsert，但它们都需要对list进行遍历，所以时间复杂度较高，为O(N)。

概况起来，list具有这样的一些特点: 它是一个能维持数据项先后顺序的列表 (各个数据项的先后顺序由插入位置决定) ，便于在表的两端追加和删除数据，而对于中间位置的存取具有O(N)的时间复杂度。这不正是一个双向链表所具有的特点吗？

list的内部实现quicklist正是一个双向链表。在quicklist.c的文件头部注释中，是这样描述quicklist的: 

A doubly linked list of ziplists

它确实是一个双向链表，而且是一个ziplist的双向链表。

这是什么意思呢？

我们知道，双向链表是由多个节点 (Node) 组成的。这个描述的意思是: quicklist的每个节点都是一个ziplist。ziplist我们已经在上一篇介绍过。

ziplist本身也是一个能维持数据项先后顺序的列表 (按插入位置) ，而且是一个内存紧缩的列表 (各个数据项在内存上前后相邻) 。比如，一个包含3个节点的quicklist，如果每个节点的ziplist又包含4个数据项，那么对外表现上，这个list就总共包含12个数据项。

quicklist的结构为什么这样设计呢？总结起来，大概又是一个空间和时间的折中: 

双向链表便于在表的两端进行push和pop操作，但是它的内存开销比较大。首先，它在每个节点上除了要保存数据之外，还要额外保存两个指针；其次，双向链表的各个节点是单独的内存块，地址不连续，节点多了容易产生内存碎片。
ziplist由于是一整块连续内存，所以存储效率很高。但是，它不利于修改操作，每次数据变动都会引发一次内存的realloc。特别是当ziplist长度很长的时候，一次realloc可能会导致大批量的数据拷贝，进一步降低性能。
于是，结合了双向链表和ziplist的优点，quicklist就应运而生了。

不过，这也带来了一个新问题: 到底一个quicklist节点包含多长的ziplist合适呢？比如，同样是存储12个数据项，既可以是一个quicklist包含3个节点，而每个节点的ziplist又包含4个数据项，也可以是一个quicklist包含6个节点，而每个节点的ziplist又包含2个数据项。

这又是一个需要找平衡点的难题。我们只从存储效率上分析一下: 

每个quicklist节点上的ziplist越短，则内存碎片越多。内存碎片多了，有可能在内存中产生很多无法被利用的小碎片，从而降低存储效率。这种情况的极端是每个quicklist节点上的ziplist只包含一个数据项，这就蜕化成一个普通的双向链表了。
每个quicklist节点上的ziplist越长，则为ziplist分配大块连续内存空间的难度就越大。有可能出现内存里有很多小块的空闲空间 (它们加起来很多) ，但却找不到一块足够大的空闲空间分配给ziplist的情况。这同样会降低存储效率。这种情况的极端是整个quicklist只有一个节点，所有的数据项都分配在这仅有的一个节点的ziplist里面。这其实蜕化成一个ziplist了。
可见，一个quicklist节点上的ziplist要保持一个合理的长度。那到底多长合理呢？这可能取决于具体应用场景。实际上，Redis提供了一个配置参数list-max-ziplist-size，就是为了让使用者可以来根据自己的情况进行调整。


https://www.cnblogs.com/chenchuxin/p/14199444.html

https://segmentfault.com/a/1190000027074753


http://zhangtielei.com/posts/blog-redis-quicklist.html

