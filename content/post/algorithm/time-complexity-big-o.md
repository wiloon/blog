---
title: "时间复杂度与大 O 表示法 Big O Notation"
author: "-"
date: 2015-06-28T07:44:24+00:00
lastmod: 2026-07-04T17:10:13+08:00
url: time-complexity-big-o
categories:
  - Algorithm
tags:
  - algorithm
  - remix
  - AI-assisted
---
## 大 O 表示法（Big O Notation）

大 O 符号用来描述算法的时间复杂度：输入规模增长时，算法运行时间的增长趋势。

最直观的两种复杂度是：

- `O(1)`：一次操作即可直接取得目标元素，例如字典（哈希表）的查找
- `O(n)`：需要逐一检查 n 个元素才能找到目标，例如遍历数组查找

那么 `O(log n)` 是什么意思？

## O(log n) 的由来：二分查找

`O(log n)` 最常见的例子是二分查找。二分查找最好情况下复杂度是 `O(1)`（第一次就命中中间元素），最坏情况下是 `O(log n)`。下面从最坏情况推导这个结论。

假设有 16 个元素的有序数组，要查找的目标值小于数组中间的元素。每比较一次中间元素，搜索范围就减半：

1. 16 个元素 → 取中间元素比较，目标在前一半 → 剩余 8 个元素
1. 8 个元素 → 剩余 4 个元素
1. 4 个元素 → 剩余 2 个元素
1. 2 个元素 → 剩余 1 个元素，查找结束

也就是说，从 16 个元素中定位目标，最多需要将数组对半分割 4 次：

$$
\frac{16}{2^4} = 1
$$

推广到 n 个元素，设需要分割 k 次才能剩下 1 个元素：

$$
\frac{n}{2^k} = 1 \implies n = 2^k \implies k = \log_2 n
$$

所以二分查找最坏情况下的比较次数是 $\log_2 n$，这就是 `O(log n)` 的来源。

## 对数的定义

对数（logarithm）回答的是这样一个问题：底数取多少次幂，才能等于给定的数。写成公式：

$$
\log_b x = y \iff b^y = x
$$

例如 $\log_2 16 = 4$，因为 $2^4 = 16$。这也解释了为什么二分查找每次让规模减半时，需要的步数正好是 $\log_2 n$。

---

参考：[What does the time complexity O(log n) actually mean?](https://github.com)（原文作者 Maaz，中文译文见[掘金翻译计划](https://juejin.cn/post/6844903481191432206)，译者 cdpath，校对 zaraguo、whatbeg）

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-04 | 文件重命名为 `time-complexity-big-o.md`；url 由 `时间复杂度` 改为 `time-complexity-big-o`；标题改为「时间复杂度与大 O 表示法 Big O Notation」；categories 由 `Inbox` 改为 `Algorithm`；目录由 `other` 移动到 `algorithm`；重写正文，去除重复标题和失效的图片说明文字，补充公式推导；添加 `remix`、`AI-assisted`、`algorithm` 标签，去除 `reprint` | 原文件名为中文且不规范；正文格式混乱，含多处重复标题与残留的图片描述文字，无法正常阅读；`other` 目录不能反映文章的算法主题 |