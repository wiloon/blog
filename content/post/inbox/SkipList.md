---
title: "SkipList, 跳表, 跳跃表"
author: "-"
date: "2021-07-25 18:17:06"
url: "SkipList"
categories:
  - inbox
tags:
  - inbox
---
SkipList(跳表)这种数据结构是由William Pugh于1990年在在 Communications of the ACM June 1990, 33(6) 668-676 发表了Skip lists: a probabilistic alternative to balanced trees，在其中详细描述了他的工作。由论文标题可知，SkipList的设计初衷是作为替换平衡树的一种选择。

我们都知道，AVL树有着严格的O(logN)的查询效率，但是由于插入过程中可能需要多次旋转，导致插入效率较低，因而才有了在工程界更加实用的红黑树。

但是红黑树有一个问题就是在并发环境下使用不方便，比如需要更新数据时，Skip需要更新的部分比较少，锁的东西也更少，而红黑树有个平衡的过程，在这个过程中会涉及到较多的节点，需要锁住更多的节点，从而降低了并发性能。

SkipList还有一个优势就是实现简单，SkipList的实现只花了2个小时，而红黑树，我可能得2天。

时隔将近三十多年，SkipList这种数据结构仍在许多途径有用武之地，比如Redis, 还有Google的著名项目Bigtable.



https://zhuanlan.zhihu.com/p/33674267


### skiplist, 红黑树
skiplist 的复杂度和红黑树一样，而且实现起来更简单。
在并发环境下红黑树在插入和删除时需要rebalance，性能不如跳表。

