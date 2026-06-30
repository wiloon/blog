---
title: "Byzantine Generals Problem 拜占庭将军问题"
author: "-"
date: "2021-07-06 23:01:13"
lastmod: 2026-06-30T17:26:51+08:00
url: byzantine-generals-problem
categories:
  - Algorithm
tags:
  - distributed-systems
  - consensus
  - blockchain
  - remix
  - AI-assisted
aliases:
  - 拜占庭将军问题
---

接触区块链，多少会听到「某某算法解决了拜占庭将军问题」。它其实是分布式系统一致性（distributed consensus）领域一个很经典的抽象问题，由 [Leslie Lamport](https://en.wikipedia.org/wiki/Leslie_Lamport)（2013 年图灵奖得主，分布式系统领域奠基人之一，逻辑时钟、Paxos、LaTeX 的作者）与 Robert Shostak、Marshall Pease 在 1982 年的论文 [《The Byzantine Generals Problem》](https://lamport.azurewebsites.net/pubs/byz.pdf) 中提出。

## 什么是拜占庭将军问题

它也被叫作「拜占庭容错问题」。用一个比喻来描述：

拜占庭帝国派出 10 支军队去包围一个敌人。这个敌人能抵御 5 支常规军队的同时袭击，所以至少要有 6 支军队（过半）同时进攻才能取胜。这些军队分散在敌国四周，只能靠通信兵骑马互相传递消息来约定「进攻意向」和「进攻时间」。

麻烦在于：将军中可能有**叛徒**。叛徒会擅自篡改进攻意向或时间。那么，在可能存在叛徒的情况下，忠诚的将军们要如何达成一致、保证有多于 6 支军队在同一时间发起进攻？

需要注意，这个问题里**假定信道本身是可靠的**（消息不会丢失、不会被截获）。至于「在可能丢消息的不可靠信道上，靠消息传递达成一致是不可能的」，那是另一个经典结论——[两将军问题（Two Generals' Problem）](https://en.wikipedia.org/wiki/Two_Generals%27_Problem)，由 Akkoyunlu 等人在 1975 年提出并证明无解、Jim Gray 1978 年将其命名，是第一个被证明无解的计算机通信问题。它常被误记为 Lamport 的成果，其实和拜占庭将军问题是两回事：前者讲「信道不可靠」，后者讲「节点会作恶」。所以拜占庭将军问题把信道问题排除在外，焦点放在「节点（将军）本身可能作恶」上。

## 问题分析

先看没有叛徒的情况：将军 A 提一个进攻提议（「明天下午 1 点进攻，你加入吗？」），通过通信兵告诉其他将军。如果他收到 6 个以上将军的同意，就能发起进攻。但如果其他将军同时也在发不同的提议（2 点、3 点……），由于消息到达有时间差，不同将军收到并认可的提议可能不一样，于是出现 A 提议 3 票、B 提议 4 票、C 提议 2 票这种分裂局面。

再加入叛徒就更复杂了：一个叛徒会**向不同的将军发出不同的提议**（告诉 A 是 1 点、告诉 B 是 2 点），也可能同时同意多个互相冲突的提议。

叛徒发送的这种前后不一致、互相矛盾的信息，就叫「拜占庭错误（Byzantine fault）」。

## 正式定义与关键结论

上面是流传最广的「对等版」讲法（将军平等、谁都能提议），直观但不完整。Lamport 等人原始论文里**正式求解**的其实是一个非对称形式：一个「司令」发命令、其余「副官」执行，要求所有忠诚副官执行同一命令、且司令忠诚时执行的就是他发的命令；多将军的全体一致再由「轮流当司令」推广得到。关键在于：**不能假定任何单点（包括司令）诚实**。

两个常被引用的结论：

- 口头消息（oral messages，可被篡改但不能冒名）：要容忍 m 个叛徒，至少需要 3m + 1 个将军，即忠诚者必须超过 2/3。三个将军时一个叛徒就无解。
- 签名消息（signed messages，带不可伪造签名）：叛徒无法谎报「别人说了什么」，于是可以容忍任意数量的叛徒，不再受 3m + 1 限制。

工程上的后代是各种 BFT 共识：如 PBFT（Practical Byzantine Fault Tolerance，1999），以及区块链里的 Tendermint、HotStuff 等。需要注意，常见的 [Paxos](./paxos.md)、[Raft](./raft.md) 只解决「节点崩溃」而不解决「节点作恶」，不属于 BFT。

## 拜占庭容错（BFT）

能够在部分节点出现「拜占庭错误」（任意行为，包括发送错误甚至恶意信息）时仍让系统达成一致的容错能力，称为 **Byzantine Fault Tolerance（BFT）**，是 [容错（fault tolerance）](../pattern/fault-tolerance.md) 里要求最强的一类——它要应对的不只是「节点宕机/失联」，还有「节点说谎」。

BFT 是区块链等去中心化系统的核心诉求之一。相比之下，常见的分布式共识算法如 [Paxos](./paxos.md)、[Raft](./raft.md) 通常假定节点只会崩溃、不会作恶（即所谓 non-Byzantine / crash fault），因此不解决拜占庭错误。

## 参考

- Lamport、Shostak、Pease，《The Byzantine Generals Problem》（1982）原文 PDF：<https://lamport.azurewebsites.net/pubs/byz.pdf>
- [Leslie Lamport（Wikipedia）](https://en.wikipedia.org/wiki/Leslie_Lamport)、[2013 图灵奖介绍](https://amturing.acm.org/award_winners/lamport_1205376.cfm)
- [两将军问题 Two Generals' Problem（Wikipedia）](https://en.wikipedia.org/wiki/Two_Generals%27_Problem)
- [比特币与拜占庭将军问题](https://learnblockchain.cn/2018/02/05/bitcoin-byzantine/)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-30 | 文件由 `inbox/拜占庭将军问题.md` 重命名并移到 `cs/byzantine-generals-problem.md`；title 改为英中混写、url 改为 `byzantine-generals-problem`（旧中文 url 加入 aliases）；分类 `inbox`→`Algorithm`，标签更新为 `distributed-systems`/`consensus`/`blockchain`/`remix`/`AI-assisted`；重排小标题、改写为自有表述并补 BFT 与 Paxos/Raft、fault-tolerance 内链 | 文件名为中文、内容在未分类 inbox，整理归类、规范文件名与 URL |
| 2026-06-30 | 纠正出处：原文把「不可靠信道无法达成一致」误记为 Lamport 的结论，改为指明这是「两将军问题」（Akkoyunlu 1975 / Jim Gray 1978）；补 Lamport 简介与链接、Byzantine Generals 原始论文 PDF、Two Generals' Problem 等参考链接 | 修正张冠李戴的事实错误，补一手出处 |
| 2026-06-30 | 新增「正式定义与关键结论」一节：通俗版 vs 司令/副官正式版的区别、口头消息 3m+1（>2/3）与签名消息可破除该限制、工程后代 PBFT/区块链 BFT，并点明 Paxos/Raft 非 BFT | 补全正式结论，避免读者把通俗故事当作全部 |
