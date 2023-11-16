---
title: "SkipList, 跳表, 跳跃表"
author: "-"
date: "2021-07-25 18:17:06"
url: "SkipList"
categories:
  - Data-Structure
tags:
  - inbox
---
## "SkipList, 跳表, 跳跃表"

SkipList

![](https://pic2.zhimg.com/80/v2-a78099a1347aa36d2599a6d78849a4ad_720w.jpg)

SkipList(跳表)这种数据结构是由 William Pugh 于1990年在在 Communications of the ACM June 1990, 33(6) 668-676 发表了Skip lists: a probabilistic alternative to balanced trees，在其中详细描述了他的工作。由论文标题可知，SkipList 的设计初衷是作为替换 平衡树 的一种选择。

我们都知道，AVL树有着严格的O(logN)的查询效率，但是由于插入过程中可能需要多次旋转，导致插入效率较低，因而才有了在工程界更加实用的红黑树。

但是红黑树有一个问题就是在并发环境下使用不方便，比如需要更新数据时，SkipList 需要更新的部分比较少，锁的东西也更少，而红黑树有个平衡的过程，在这个过程中会涉及到较多的节点，需要锁住更多的节点，从而降低了并发性能。

SkipList还有一个优势就是实现简单，SkipList的实现只花了2个小时，而红黑树，我可能得2天。

时隔将近三十多年，SkipList 这种数据结构仍在许多途径有用武之地，比如Redis, 还有Google的著名项目 Bigtable, leveldb

### 原理及实现

其实跳表就是在普通单向链表的基础上增加了一些索引，而且这些索引是**分层**的，从而可以快速地查的到数据。

比如我们要查找key为19的结点，那么我们不需要逐个遍历，而是按照如下步骤:

- 从header出发，从高到低的level进行查找，先索引到9这个结点，发现9 < 19,继续查找(然后在level==2这层)，查找到21这个节点，由于21 > 19, 所以结点不往前走，而是level由2降低到1
- 然后索引到17这个节点，由于17 < 19, 所以继续往后，索引到21这个结点，发现21>19, 所以level由1降低到0
- 在结点17上，level==0索引到19,查找完毕。
- 如果在level==0这层没有查找到，那么说明不存在key为19的节点，查找失败

[https://zhuanlan.zhihu.com/p/33674267](https://zhuanlan.zhihu.com/p/33674267)

### skiplist, 红黑树

skiplist 的复杂度和红黑树一样，而且实现起来更简单。
在并发环境下红黑树在插入和删除时需要 rebalance，性能不如跳表。

>[http://www.cnblogs.com/xuqiang/archive/2011/05/22/2053516.html](http://www.cnblogs.com/xuqiang/archive/2011/05/22/2053516.html)
