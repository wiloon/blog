---
title: "etcd"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "etcd"

### etcd

etcd是CoreOS团队于2013年6月发起的开源项目，它的目标是构建一个高可用的分布式键值(key-value)数据库。etcd内部采用`raft`协议作为一致性算法，etcd基于Go语言实现。

本文的主角是 etcd。名称 “etcd” 源自两个想法，即 unix “/etc” 文件夹 和 “d” 分布式系统。“/etc” 文件夹是用于存储单个系统的配置数据的位置，而 etcd 用于存储大规模分布式的配置信息。因此，分配了 “d” 的 “/etc” 就是 “etcd”。
etcd 被设计为大型分布式系统的通用基板。这些大型系统需要避免裂脑操作，并且愿意牺牲可用性来实现此目的。 etcd 以一致且容错的方式存储元数据。 etcd 集群旨在提供具有稳定性、可靠性、可伸缩性和性能的键值存储。
分布式系统将 etcd 用作配置管理、服务发现和协调分布式工作的一致键值存储组件。许多组织在生产系统上使用 etcd，例如容器调度程序、服务发现服务和分布式数据存储。使用 etcd 的常见分布式模式包括领导者选举、分布式锁和监视机器活动状态等。
此外，etcd 开箱即用地支持多种语言和框架。Zookeeper 拥有自己的自定义Jute RPC 协议，该协议对于 Zookeeper 而言是完全唯一的，并限制了其受支持的语言绑定，而 etcd 的客户端协议则是基于 gRPC 构建的，gRP 是一种流行的 RPC 框架，具有 go，C ++，Java 等语言支持。同样，gRPC 可以通过 HTTP 序列化为 JSON，因此即使是通用命令行实用程序 (例如curl) 也可以与之通信。由于系统可以从多种选择中进行选择，因此它们是基于具有本机工具的 etcd 构建的，而不是基于一组固定的技术围绕 etcd 构建的。
在考虑功能，支持和稳定性时，etcd 相比于 Zookeeper，更加适合用作一致性的键值存储的组件。

## etcd的特点

* 简单: 安装配置简单，而且提供了HTTP API进行交互，使用也很简单
* 安全: 支持SSL证书验证
* 快速: 根据官方提供的benchmark数据，单实例支持每秒2k+读操作
* 可靠: 采用raft算法，实现分布式系统数据的可用性和一致性

## 概念术语

* Raft: etcd 所采用的保证分布式系统强一致性的算法。
* Node: 一个Raft状态机实例。
* Member:  一个etcd实例。它管理着一个Node，并且可以为客户端请求提供服务。
* Cluster: 由多个Member构成可以协同工作的etcd集群。
* Peer: 对同一个etcd集群中另外一个Member的称呼。
* Client:  向etcd集群发送HTTP请求的客户端。
* WAL: 预写式日志，etcd用于持久化存储的日志格式。
* snapshot: etcd防止WAL文件过多而设置的快照，存储etcd数据状态。
* Proxy: etcd的一种模式，为etcd集群提供反向代理服务。
* Leader: Raft算法中通过竞选而产生的处理所有数据提交的节点。
* Follower: 竞选失败的节点作为Raft中的从属节点，为算法提供强一致性保证。
* Candidate: 当Follower超过一定时间接收不到Leader的心跳时转变为Candidate开始竞选。
* Term: 某个节点成为Leader到下一次竞选时间，称为一个Term。
* Index: 数据项编号。Raft中通过Term和Index来定位数据。

## 数据读写顺序

为了保证数据的强一致性，etcd集群中所有的数据流向都是一个方向，从 Leader  (主节点) 流向 Follower，也就是所有 Follower 的数据必须与 Leader 保持一致，如果不一致会被覆盖。

用户对于etcd集群所有节点进行读写

* 读取: 由于集群所有节点数据是强一致性的，读取可以从集群中随便哪个节点进行读取数据
* 写入: etcd集群有leader，如果写入往leader写入，可以直接写入，然后然后Leader节点会把写入分发给所有Follower，如果往follower写入，然后Leader节点会把写入分发给所有Follower

## leader选举

假设三个节点的集群，三个节点上均运行Timer (每个Timer持续时间是随机的) ，Raft算法使用随机Timer来初始化Leader选举流程，第一个节点率先完成了Timer，随后它就会向其他两个节点发送成为Leader的请求，其他节点接收到请求后会以投票回应然后第一个节点被选举为Leader。

成为Leader后，该节点会以固定时间间隔向其他节点发送通知，确保自己仍是Leader。有些情况下当Follower们收不到Leader的通知后，比如说Leader节点宕机或者失去了连接，其他节点会重复之前选举过程选举出新的Leader。

## 判断数据是否写入

etcd认为写入请求被Leader节点处理并分发给了多数节点后，就是一个成功的写入。那么多少节点如何判定呢，假设总结点数是N，那么多数节点 `Quorum=N/2+1`。关于如何确定etcd集群应该有多少个节点的问题，上图的左侧的图表给出了集群中节点总数(Instances)对应的Quorum数量，用Instances减去Quorom就是集群中容错节点 (允许出故障的节点) 的数量。

所以在集群中推荐的最少节点数量是3个，因为1和2个节点的容错节点数都是0，一旦有一个节点宕掉整个集群就不能正常工作了。

## 架构解析

从 etcd 的架构图中我们可以看到，etcd 主要分为四个部分。

* HTTP Server: 用于处理用户发送的 API 请求以及其它 etcd 节点的同步与心跳信息请求。
* Store: 用于处理 etcd 支持的各类功能的事务，包括数据索引、节点状态变更、监控与反馈、事件处理与执行等等，是 etcd 对用户提供的大多数 API 功能的具体实现。
* Raft: Raft 强一致性算法的具体实现，是 etcd 的核心。
* WAL: Write Ahead Log (预写式日志) ，是 etcd 的数据存储方式。除了在内存中存有所有数据的状态以及节点的索引以外，etcd 就通过 WAL 进行持久化存储。WAL 中，所有的数据提交前都会事先记录日志。
  * Snapshot 是为了防止数据过多而进行的状态快照；
  * Entry 表示存储的具体日志内容。

通常，一个用户的请求发送过来，会经由 HTTP Server 转发给 Store 进行具体的事务处理，如果涉及到节点的修改，则交给 Raft 模块进行状态的变更、日志的记录，然后再同步给别的 etcd 节点以确认数据提交，最后进行数据的提交，再次同步。

### etcd vs zookeeper

#### 对 Zookeeper 进行的 etcd 改进包括

动态重新配置集群成员
高负载下稳定的读写
多版本并发控制数据模型
可靠的键值监控
租期原语将 session 中的连接解耦
用于分布式共享锁的 API

zookeeper 使用 ZAB 协议作为其一致性协议。 zookeeper 通过团队的形式工作，一组 node 一起工作，来提供分布式能力，这组 node 的数量需要是奇数。

第一个节点与其他节点沟通，选举出一个 leader，获取多数票数的成为 leader，这就是为什么需要奇数个 node，其他节点被称为follower。

client 连接 zookeeper 时可以连接任何一个，client 的读请求可以被任何一个节点处理，写请求只能被 leader 处理。所以，添加新节点可以提高读的速度，但不会提高写的速度。

对于 CAP 模型，zookeeper 保障的是 CP。

优点
非阻塞全部快照 (达成最终一致)
高效的内存管理
高可靠
API 简单
连接管理可以自动重试
ZooKeeper recipes 的实现是经过完整良好的测试的。
有一套框架使得写新的 ZooKeeper recipes 非常简单。
支持监听事件
发生网络分区时，各个区都会开始选举 leader，那么节点数少的那个分区将会停止运行。
缺点
zookeeper 是 java 写的，那么自然就会继承 java 的缺点，例如 GC 暂停。
如果开启了快照，数据会写入磁盘，此时 zookeeper 的读写操作会有一个暂时的停顿。
对于每个 watch 请求，zookeeper 都会打开一个新的 socket 连接，这样 zookeeper 就需要实时管理很多 socket 连接，比较复杂。

etcd 使用 RAFT 算法实现的一致性，比 zookeeper 的 ZAB 算法更简单。

etcd 没有使用 zookeeper 的树形结构，而是提供了一个分布式的 key-value 存储。

优点
支持增量快照，避免了 zookeeper 的快照暂停问题
堆外存储，没有垃圾回收暂停问题
无需像 zookeeper 那样为每个 watch 都做个 socket 连接，可以复用
zookeeper 每个 watch 只能收到一次事件通知，etcd 可以持续监控，在一次 watch 触发之后无需再次设置一次 watch
zookeeper 会丢弃事件，etcd3 持有一个事件窗口，在 client 断开连接后不会丢失所有事件
缺点
如果超时，或者 client 与 etcd 网络中断，client 不会明确的知道当前操作的状态
在 leader 选举时，etcd 会放弃操作，并且不会给 client 发送放弃响应
在网络分区时，当 leader 处于小分区时，读请求会继续被处理
总结
zookeeper 是用 java 开发的，被 Apache 很多项目采用。

etcd 是用 go 开发的，主要是被 Kubernetes 采用。
zookeeper 非常稳定，是一个著名的分布式协调系统，etcd 是后起之秀，前景广阔。

>[https://medium.com/@Imesha94/apache-curator-vs-etcd3-9c1362600b26](https://medium.com/@Imesha94/apache-curator-vs-etcd3-9c1362600b26)
>[https://juejin.im/post/5e02fb1f518825123b1aa341](https://juejin.im/post/5e02fb1f518825123b1aa341)
>[https://juejin.cn/post/6844904147779600391](https://juejin.cn/post/6844904147779600391)
