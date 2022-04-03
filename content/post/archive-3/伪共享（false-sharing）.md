---
title: 伪共享 (false sharing) 
author: "-"
date: 2020-01-13T08:31:31+00:00
url: /?p=15356
categories:
  - Uncategorized

tags:
  - reprint
---
## 伪共享 (false sharing)
伪共享的非标准定义为: 缓存系统中是以缓存行 (cache line) 为单位存储的，当多线程修改互相独立的变量时，如果这些变量共享同一个缓存行，就会无意中影响彼此的性能，这就是伪共享。
  
https://www.cnblogs.com/cyfonly/p/5800758.html