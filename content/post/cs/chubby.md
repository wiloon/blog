---
title: Chubby
author: "-"
date: 2021-11-11T02:46:23+00:00
url: Chubby
categories:
  - Inbox
tags:
  - reprint
---
## Chubby

分布式锁管理系统,也可理解为一个小型强一致性文件系统
http://www.cnblogs.com/linhaohong/archive/2012/11/26/2789394.html

随着云计算的推广,云平台的设计和实现越来越复杂,很多系统属性如一致性和可靠性往往是在系统迭代开发时才被考虑到。如果在原生的系统上重复的实现复杂的一致性算法,这样不仅会破坏原有设计的结构,而且还带来很多开发上的负担。因此很多系统开发人员和架构师努力地进行系统划分,将系统分割成很多组件,分层设计,模块调用,从而最大限度地提高软件复用能力,降低系统设计和开发的难度。

Google在系统的可靠性方面提出了中心化的组件Chubby—粗粒度锁服务,通过锁原语为其他系统实现更高级的服务,比如组成员、域名服务和leader选举等等。Chubby本身也是一个小型的cell (通常由5个chubby结点组成) ,cell内部采用类似于状态机副本形式实现可靠容错。Google的Chubby论文在OSDI上发表后引起了很大的反响,原因很多,主要有两个: 第一,chubby很好的解决了分布式开发的一致性问题；
第二,Google Chubby采用Leslie Lamport提出的paxos算法来实现可靠容错,这是业界关于paxos第一个完整可行的实现。正因为Google Chubby,paxos这个一直沉淀在学术研究的协议,终于曝光在工业界中,之后很快地推广开去。

然而, Google Chubby 并不是开源的, 我们只能通过其论文和其他相关的文档中了解具体的细节。值得庆幸的是,Yahoo！借鉴 Chubby 的设计思想开发了 Zookeeper, 并将其开源。
和 Chubby 相比, Zookeeper 做了很多突破。不像 Chubby 的单点服务的结构, zookeeper 采用多个 server 同时处理客户端的请求, 异步读同步写, 
通过 primary 节点来同步数据的 update, 这一点大大改善了读服务的性能, 当然弱化了客户端与服务器之间的一致性。另外, zookeeper 采用 block free 的服务接口, 
采用 watch 机制的方式异步处理请求结果和指定数据的变更。Zookeeper 对外提供了更加低级的原语 primitive, 基于此可以实现更多更加复杂的分布式算法, 如 queue、barrier 和 lock 等等。
如今很多云计算系统或者平台都使用 Zookeeper 来做可靠容错, 进行订阅分发服务, 或者其他应用。

和Chubby一样,zookeeper采用paxos的变种来实现消息传输的一致性。Zookeeper开发了原子多播协议 Zab 来实现数据的一致性传输。Zookeeper采用的是primary-backup的结构,primary节点产生non- commutative 事务,通过协议按序的广播到其他backup节点上。在节点无错的情况下,这是非常简单的事情,然而,面对复杂的网络环境,多变的软硬件条件,节点挂掉,重启,数据重复发送,这些异常很常见。Zookeeper如何做到即便是系统出现异常,也能够保证整个系统状态是一致？paxos的变种,Zookeeper的Zab协议很好的保证了这一点。

Zab 协议以epoch的方式执行 (相当与序列号) ,在每个epoch最多只有一个进程多播数据。如果某个进程执行了协议的的第一阶段,那么进程将不再接受之前还没确定提交的epoch的数据。这样一来就保证了在进程在recovery阶段不会出现丢失已提交的数据的情况。在某个epoch下,所有参加这个epoch的进程必须此epoch之前所有已经提交的数据镜像。为了保证一致性,进程在完全恢复之前必须不能广播新的事务。Zab协议的这几个特点处理了primary异常、新旧primary以及backup节点异常的情况,的确保证了primary进程原子多播的order特性。

整个Zab协议的内容分成三个阶段: Discovery、Synchronization和Broadcast阶段。

Discovery阶段其实是选举leader或者发现leader。在这个阶段里,follower会给 (可能是) leader的进程 (这里的进程可以是多个) 发送当前自己epoch的信息CEPOCH；如果 (可能是) leader进程收到大多数的follower的CEPOCH消息,那么leader就会产生一个新epoch的消息NEWEPOCH,其中包含新的leader,并发送给follower；当follower f收到NEWEPOCH时,f会判断其中epoch是否比当前的大,如果是则反馈信息ACK-E,其中包含f所接受的最大事务编号和历史数据；leader会从这些ACK-E中选出最新的历史数据来初始化它当前的系统状态。这个阶段其实就是paxos的执行过程,由于两个大多数集合的交集肯定不为空,所以不可能一个epoch下会选出两个不同的leader。因此Discovery阶段最后的结果肯定只有一个新leader。在整个系统初始的时候,每个节点当前的epoch都为0,这样会给其它节点发送请求,这样有可能会导致paxos死锁,对此,每个zookeeper节点会通过配置获得唯一的id,并根据id的大则优先的原则来推选leader。

Synchronization阶段其实就会状态同步,新leader会将其最新状态通知给所有的follower；follower的到leader的状态后,会和自己的进行比较,从中提前还未提交的数据T,并反馈给leader；leader收到大多数确认反馈时,则发送提交命令commit给这些follower；follower收到commit后提交T中的所有数据。

Broadcast阶段和Synchronization阶段相似,只是这个阶段是对一个请求的提交而不是一个集合的提交。

Zab这三个阶段保证了前面提到的协议的几个特性,其正确性无非就是从integrity、total order 和 casual order三个方面去证明。从实际应用看,Discovery和synchronization阶段在系统状态出现不一致时,这两个阶段保证了系统即便出问题也能恢复到一致的状态；Broadcast阶段主要保证了事务执行的顺序性。

总而言之,paxos算法是Zookeeper的核心。Google Chubby架构师曾说,一切一致性协议都是paxos的变种。仔细分析,想gossip、viewstamp或者virtual synchronization其实是对relax paxos的某些条件。即便是Chubby或者Zookeeper其中采取的算法也是变种中的其中之一。Chubby和Zookeeper现有版本都是采取中心化的思想,在扩展性和性能之间的折中表现还不是很好。随着系统规模的变大和新环境的出现,如何对其去中心化并能保证可靠容错,这将是个很有趣的问题。
