---
title: ZooKeeper Leader Latch 与 Leader Election
author: "-"
date: 2026-04-28T12:13:10+08:00
url: zookeeper-leader-latch
categories:
  - cloud
tags:
  - zookeeper
  - curator
  - distributed
  - remix
  - AI-assisted
---
## ZooKeeper 节点类型

ZooKeeper 的节点（ZNode）类型是两个维度的组合：

**生命周期维度：**

- 持久（Persistent）：客户端断开后节点依然存在，需要显式删除
- 临时（Ephemeral）：与创建它的客户端 Session 绑定，Session 结束节点自动删除

**命名维度：**

- 普通：你指定什么路径就创建什么路径，路径已存在则报错
- 顺序（Sequential）：路径作为前缀，ZooKeeper 自动追加 10 位单调递增序号

两两组合，实际有四种节点类型：

| 类型 | 说明 |
| --- | --- |
| 持久节点 | 最普通的节点，手动删除才消失 |
| 持久顺序节点 | 名称自动追加递增序号，永久存在 |
| 临时节点 | Session 结束自动删除 |
| 临时顺序节点 | Session 结束自动删除 + 名称追加序号 |

**各场景适用类型：**

| 场景 | 用哪种 |
| --- | --- |
| 分布式锁（抢占式）| 普通临时节点，谁先创建谁得锁 |
| 分布式锁（公平排队）| 顺序临时节点，序号最小的得锁 |
| Leader 选举 | 顺序临时节点，序号最小的是 leader |
| 配置中心、服务注册 | 普通持久节点 |

## 临时节点原理

ZooKeeper 客户端连接服务端后会建立一个 Session，并维持心跳（默认每隔 tickTime 发一次）。服务端为每个 Session 设置超时时间（`sessionTimeout`），超时内未收到心跳则判定 Session 过期，自动删除该 Session 创建的所有临时节点，其他 watch 了这些节点的客户端会收到删除通知。

| 状态 | 临时节点是否消失 |
| --- | --- |
| 网络抖动（短暂断开） | 不消失，等待重连，Session 未过期 |
| 断开超过 sessionTimeout | 消失，Session 过期 |
| 客户端主动 close() | 立即消失 |

临时节点不能有子节点，因为它的生命周期是不确定的。

## Leader Latch 底层原理

Leader Latch 使用**临时顺序节点**实现，流程如下：

1. 每个客户端在同一路径下创建临时顺序节点：

   ```
   /latch/lock-0000000001
   /latch/lock-0000000002
   /latch/lock-0000000003
   ```

2. 每个客户端查询该路径下所有子节点，**序号最小的即为 leader**

3. 非 leader 客户端只 watch 自己的**前一个节点**（避免惊群效应）

4. leader 宕机或主动关闭时，临时节点自动消失，下一个节点收到通知，发现自己变成最小节点，成为新 leader

**关键设计点：**

- 用**临时节点**：客户端断线后节点自动删除，不会出现僵尸 leader
- 用**顺序节点**：保证公平性，先到先得，有明确排队顺序
- **只 watch 前一个节点**：把广播变成链式单播，每次只有一个客户端被唤醒，避免惊群

## Watch 机制与惊群问题

**错误做法（Watch 父节点）：**

```
/latch/lock-001  ← leader，宕机消失
/latch/lock-002  ← watch /latch（父节点）
/latch/lock-003  ← watch /latch（父节点）
/latch/lock-004  ← watch /latch（父节点）
```

lock-001 消失时，所有客户端同时收到通知，全部涌去查询"我是不是最小节点"——这就是惊群（Herd Effect）。

**正确做法（只 Watch 前一个节点）：**

```
/latch/lock-001  ← leader，宕机消失
/latch/lock-002  ← watch lock-001
/latch/lock-003  ← watch lock-002
/latch/lock-004  ← watch lock-003
```

lock-001 消失时，只有 lock-002 收到通知，成为新 leader，lock-003、lock-004 完全感知不到。

ZooKeeper 的 watch 是**一次性的**，触发后自动失效，需要重新注册。Curator 会自动处理重新注册，避免漏通知。

## ZooKeeper 内部 Leader Election（Zab 协议）

ZooKeeper 通过 Zab（ZooKeeper Atomic Broadcast）协议保持集群间数据一致性，包括两个阶段：

**Leader Election 阶段：**
集群内选举出一个 leader，余下机器成为 follower。leader 通过 broadcast 通知所有 follower，当超过半数机器（> 1/2）完成与 leader 的状态同步后，此阶段结束。当 leader 失去大多数 follower 时，集群会再次进入此阶段。

**Atomic Broadcast 阶段：**
leader 通过 broadcast 与 follower 通讯，保证 leader 与 follower 具有相同的系统状态。

## Curator Leader Latch 使用

curator-framework 4.x 同时支持 zookeeper 3.4.x 和 3.5.x，默认依赖 zookeeper 3.5。使用 zookeeper 3.4 时需排除默认依赖：

```xml
<dependency>
    <groupId>org.apache.curator</groupId>
    <artifactId>curator-recipes</artifactId>
    <version>${curator-version}</version>
    <exclusions>
        <exclusion>
            <groupId>org.apache.zookeeper</groupId>
            <artifactId>zookeeper</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

**基本用法：**

```java
RetryPolicy retryPolicy = new ExponentialBackoffRetry(1000, 3);
CuratorFramework client = CuratorFrameworkFactory.newClient(zookeeperConnectionString, retryPolicy);
client.getConnectionStateListenable().addListener(connectionStateListener);
client.start();

leaderLatch = new LeaderLatch(client, zkLatchPath, leaderId);
leaderLatch.start();
```

- `hasLeadership()`：查询当前实例是否为 leader
- `await()`：阻塞直到获得 leadership
- `await(long timeout, TimeUnit unit)`：带超时的阻塞等待
- `close()`：释放 leadership，必须调用

**异常处理：**

建议添加 `ConnectionStateListener` 监听网络状态：

- `SUSPENDED`：网络抖动，leader 不再认为自己是 leader，但临时节点尚未消失
- `LOST`：Session 过期，临时节点已消失
- `RECONNECTED`：重连后，Curator 会删除旧 ZNode 并重新创建
