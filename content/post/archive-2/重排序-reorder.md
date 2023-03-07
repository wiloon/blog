---
title: 重排序 Reorder
author: "-"
date: 2017-03-26T05:25:39+00:00
url: /?p=9961
categories:
  - Inbox
tags:
  - reprint
---
## 重排序 Reorder

编译器和处理器可能会对操作做重排序。编译器和处理器在重排序时,会遵守数据依赖性,编译器和处理器不会改变存在数据依赖关系的两个操作的执行顺序。

注意,这里所说的数据依赖性仅针对单个处理器中执行的指令序列和单个线程中执行的操作,不同处理器之间和不同线程之间的数据依赖性不被编译器和处理器考虑。

<http://www.infoq.com/cn/articles/java-memory-model-2>

<http://tech.meituan.com/java-memory-reordering.html>
