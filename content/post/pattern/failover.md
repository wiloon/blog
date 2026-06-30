---
title: "Failover / Failfast / Failback / Failsafe: 四个故障处理术语"
author: "-"
date: "2021-07-06 06:44:36"
lastmod: 2026-06-30T16:49:21+08:00
url: "failover"
categories:
  - development
tags:
  - fault-tolerance
  - high-availability
  - Pattern
  - remix
  - AI-assisted
aliases:
  - /p14235/
---

这四个词长得像、也容易混，但讲的是「系统出故障时怎么应对」的不同侧面。下面把它们放在一起做个简单区分。

## Failover：失效转移 / 故障转移

当正在工作的主组件出现异常时，把它的职责切换到备用组件，让对外服务尽量不受影响。要点是**有主有备**，主故障时备能顶上、并被提升为新的主。

典型例子是数据库主从：正在使用的主库挂了，就把备库切为主库继续提供服务。理想情况下用户完全感知不到这次切换。衡量切换效果常用两个指标：

- RTO（Recovery Time Objective）：从故障到服务恢复需要多长时间。这段时间里服务通常是**不可用**的，用户感知到的是中断而不只是变慢，所以越接近 0 越好。
- RPO（Recovery Point Objective）：能恢复到故障前哪一刻，也就是最多会丢多少数据。它**不是一个固定的量级**，取决于数据保护方式：同步复制可做到 RPO ≈ 0（不丢数据，但成本高）；异步复制一般是秒级到分钟级；定期快照 / 备份则是分钟级到小时级（每天备一次，最坏丢近一天）。换句话说，秒级和小时级都可能，取决于你用哪种复制 / 备份策略以及业务能容忍丢多少。

## Failfast：快速失败

一旦检测到不该出现的状态，就**立即、显眼地失败**，把错误暴露在离源头最近的地方，而不是带着错误继续运行、之后在别处以奇怪的方式崩掉。它和 [fault-tolerant（容错）](./fault-tolerance.md)是相对的取向。

一个常见例子是 Java 集合的 fail-fast 迭代器：当一个线程在遍历集合时，集合内容被其他线程改动，遍历线程会立刻抛出 `ConcurrentModificationException`，而不是返回不可预期的结果。

fail-fast 作为一条通用的软件工程原则（不止集合迭代器），单独展开在 [Fail-Fast 快速失败](./fail-fast.md) 一文。

## Failback：失效自动恢复

failover 之后的「回切」。当原来的主组件修复、重新可用后，把网络资源和服务从备用系统切回原主系统的过程。常见于需要临时维护主机、把流量先转到备用系统、维护完再切回的场景。

## Failsafe：失效安全

即使发生故障，也尽量不造成伤害、或把伤害降到最低。一个形象的例子是红绿灯的冲突监测模块：当检测到错误或冲突的信号时，让整个路口进入闪烁警示模式，而不是把所有方向都显示为绿灯。

## 一句话区分

- failover：主挂了，备顶上，继续服务。
- failback：主修好了，再切回去。
- failfast：出错就立刻停下报错，别硬撑。
- failsafe：出错也要保证安全、把伤害降到最小。

failover / failback 关注的是「服务不中断」（可用性、容错），failfast / failsafe 关注的是「出错时的行为」——一个偏向尽早暴露，一个偏向兜底保护。

## 参考

- [失效转移、快速失败等概念（CSDN）](https://blog.csdn.net/u011305680/article/details/79730646)
- [https://blog.csdn.net/u013699827/article/details/73251649](https://blog.csdn.net/u013699827/article/details/73251649)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-30 | 从 `inbox/` 移到 `pattern/`；改写为自有表述、重排四个术语并加「一句话区分」；分类由 `inbox` 改为 `development`，标签更新为 `fault-tolerance`/`high-availability`/`Pattern`/`remix`/`AI-assisted`；新增到 [fail-fast](./fail-fast.md) 的内链 | 原在未分类 inbox、内容为转载片段，整理归类并提升可读性 |
| 2026-06-30 | RTO 说明改为强调「服务中断」而非延迟；RPO 补充其量级取决于复制 / 备份策略（同步 ≈0、异步秒/分钟级、备份分钟/小时级），不是固定小时级 | 澄清 RTO/RPO 含义，纠正「RPO 固定某量级」的误解 |
