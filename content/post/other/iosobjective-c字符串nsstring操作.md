---
title: jvm Warmup
author: "-"
date: 2014-12-03T06:18:35+00:00
url: /?p=7092
categories:
  - Uncategorized

tags:
  - reprint
---
## jvm Warmup

Warmup
  
Warmup 是指在实际进行 benchmark 前先进行预热的行为。为什么需要预热？因为 JVM 的 JIT 机制的存在,如果某个函数被调用多次之后,JVM 会尝试将其编译成为机器码从而提高执行速度。所以为了让 benchmark 的结果更加接近真实情况就需要进行预热。

<http://blog.dyngr.com/blog/2016/10/29/introduction-of-jmh/>
