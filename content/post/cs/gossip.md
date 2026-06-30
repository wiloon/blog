---
title: "Gossip Protocol 流言协议"
author: "-"
date: "2021-07-06 07:31:01"
lastmod: 2026-06-30T18:35:03+08:00
url: gossip
categories:
  - Algorithm
tags:
  - distributed-systems
  - gossip
  - remix
  - AI-assisted
aliases:
  - Gossip
---

Gossip（流言 / 八卦）协议是一种用于在分布式系统中传播消息的通信协议，灵感来自瘟疫扩散、社交网络这类「一传十、十传百」的过程。Redis Cluster、Consul、Apache Cassandra 等系统都用它来做节点间的信息同步。

## 基本思想

一个节点想把某条信息分享给网络中的其他节点时，并不会一次性广播给所有人，而是**周期性地随机挑选若干个节点**把消息发过去；收到消息的节点接下来做同样的事，再随机转发给另一些节点。如此一轮轮扩散，消息最终会传遍整个网络。

每次随机发送的目标节点数量记作 **fanout**（扇出）。比如 fanout = 4，就是每个被「感染」的节点每个周期向 4 个随机节点传播消息。

它的名字和「社交网络」的联想，背后是著名的「六度分隔」现象：1967 年哈佛大学 Stanley Milgram 通过连锁信实验发现，你和任意一个陌生人之间间隔的人通常不超过六个。若每人平均认识 260 人，理论上 260⁶ 已远超全球人口——这种指数级扩散正是 Gossip 的雏形。

## 用途

主要用于信息的传播与扩散，常见场景包括：数据库复制、配置 / 状态扩散、集群成员关系维护、故障探测等。典型系统有 Apache Cassandra、Redis（Cluster 模式）、Consul 等。

## 特点

- **可扩展（scalable）**：把消息传遍所有节点大约只需 O(log N) 个周期。发送时不需要等待对方确认（ack），即使个别消息丢失也不用补偿——节点会反复多次分享同一条消息，丢一两次不影响最终所有节点收到。在 fanout 固定时，节点数从 20 翻到 40、80、160，所需周期数也只是缓慢增长。
- **失败容错（fault-tolerant）**：网络故障等情况下依然能工作。即使暂时连不上某个节点，其他被「感染」的节点也会继续尝试向它传播。
- **健壮（robust）**：没有 leader 之类的特殊角色，任何节点随时上下线都不会破坏整体服务质量。

## 局限

Gossip 也有不完美的地方，比如难以应对[拜占庭问题](./byzantine-generals-problem.md)（Byzantine）：如果存在一个**恶意传播错误消息**的节点，普通 Gossip 协议的系统就会出问题——它假定节点只是可能失联，而不会主动作恶。

## 参考

- 阿飞的博客（简书）：<https://www.jianshu.com/p/54eab117e6ae>
- <https://cloud.tencent.com/developer/article/1662426>

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-30 | 给「拜占庭问题」加内链指向 [byzantine-generals-problem](./byzantine-generals-problem.md)；标签由 `Inbox` 改为 `distributed-systems`/`remix`/`AI-assisted`，新增 `lastmod` | 与拜占庭将军问题一文互链；规范标签 |
| 2026-06-30 | 从 `inbox/Gossip.md` 移到 `cs/gossip.md`；文件名改小写、title 改为「Gossip Protocol 流言协议」、url 改为 `gossip`（旧 `Gossip` 入 aliases）；分类 `inbox`→`Algorithm`、补 `gossip` 标签；重排为 `##` 小标题、清掉无图的残留图注、改写为自有表述 | 文件原在未分类 inbox、文件名大写、结构零散，整理归类 |
