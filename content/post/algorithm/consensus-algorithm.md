---
title: 共识算法,一致性算法, consensus algorithm
author: "-"
date: 2012-10-26T05:27:39+00:00
url: consensus
categories:
  - Algorithm
tags:
  - reprint
---
## 共识算法,一致性算法, consensus algorithm

PoW，PoS，DPoS，PBFT，Paxos，Raft 


分布式一致性算法-Paxos、Raft、ZAB、Gossip

>https://zhuanlan.zhihu.com/p/130332285

### ZAB算法

说明：ZAB也是对Multi Paxos算法的改进，大部分和raft相同
和raft算法的主要区别：
对于Leader的任期，raft叫做term，而ZAB叫做epoch
在状态复制的过程中，raft的心跳从Leader向Follower发送，而ZAB则相反。
