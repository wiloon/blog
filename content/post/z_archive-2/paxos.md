---
title: Paxos
author: "-"
date: 2015-12-23T02:48:43+00:00
url: /?p=8592
categories:
  - Inbox
tags:
  - reprint
---
## Paxos
# paxos
  Paxos (Greek: Παξοί, pronounced Paksi in English ) 又名Paxi是希腊西南部一个风景如画的小岛。而Paxos算法则是现在很火的分布式一致性算法,为何以一个希腊小岛名字算法？Lamport这样解释道: 

I thought, and still think, that Paxos is an important algorithm.  Inspired by my success at popularizing the consensus problem by describing it with Byzantine generals, I decided to cast the algorithm in terms of a parliament on an ancient Greek island.  Leo Guibas suggested the name Paxos for the island.

为描述 Paxos 算法,Lamport 虚拟了一个叫做 Paxos 的希腊城邦,这个岛按照议会民主制的政治模式制订法律,但是没有人愿意将自己的全部时间和精力放在这种事情上。所以无论是议员,议长或者传递纸条的服务员都不能承诺别人需要时一定会出现,也无法承诺批准决议或者传递消息的时间。但是这里假设没有拜占庭将军问题 (Byzantine failure,即虽然有可能一个消息被传递了两次,但是绝对不会出现错误的消息) ；只要等待足够的时间,消息就会被传到。另外,Paxos 岛上的议员是不会反对其他议员提出的决议的[1]。

**http://www.cnblogs.com/endsock/p/3480093.html**

Paxos分析
  
最近研究paxos算法,看了许多相关的文章,概念还是很模糊,觉得还是没有掌握paxos算法的精髓,所以花了3天时间分析了libpaxos3的所有代码,此代码可以从https://bitbucket.org/sciascid/libpaxos 下载。对paxos算法有初步了解之后,再看此文的效果会更好；如果你也想分析libpaxos3的话,此文应该会对你有不小帮助；关于paxos的历史这里不多做介绍,关于描述paxos算法写的最好的一篇文章应该就是维基百科了,地址戳这里: http://zh.wikipedia.org/zh-cn/Paxos%E7%AE%97%E6%B3%95


在paxos算法中,分为4种角色: 

Proposer : 提议者

Acceptor: 决策者

Client: 产生议题者

Learner: 最终决策学习者

上面4种角色中,提议者和决策者是很重要的,其他的2个角色在整个算法中应该算做打酱油的,Proposer就像Client的使者,由Proposer使者拿着Client的议题去向Acceptor提议,让Acceptor来决策。这里上面出现了个新名词: 最终决策。现在来系统的介绍一下paxos算法中所有的行为: 

Proposer提出议题
  
Acceptor初步接受 或者 Acceptor初步不接受
  
如果上一步Acceptor初步接受则Proposer再次向Acceptor确认是否最终接受
  
Acceptor 最终接受 或者Acceptor 最终不接受

>https://www.cnblogs.com/ychellboy/archive/2009/12/29/1634685.html