---
title: zookeeper leader latch
author: "-"
date: 2016-12-16T04:59:05+00:00
url: /?p=9564
categories:
  - Uncategorized

tags:
  - reprint
---
## zookeeper leader latch
# zookeeper leader latch, leader election

https://curator.apache.org/zk-compatibility.html
  
curator-framework 4.x 同时支持zookeeper 3.4.x, 3.5.x
  
curator4 默认依赖zookeeper 3.5
  
使用zookeeper3.4时,需要把zookeeper排除掉,再依赖zookeeper3.4

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

leader latch/leader election
  
在分布式计算中, leader election是很重要的一个功能, 这个选举过程是这样子的: 指派一个进程作为组织者,将任务分发给各节点。 在任务开始前, 哪个节点都不知道谁是leader或者coordinator. 当选举算法开始执行后,每个节点最终会得到一个唯一的节点作为任务leader.
  
除此之外, 选举还经常会发生在leader意外宕机的情况下,新的leader要被选举出来。

Curator 有两种选举recipe, 你可以根据你的需求选择合适的。

public LeaderLatch(CuratorFramework client, String latchPath)
  
public LeaderLatch(CuratorFramework client, String latchPath, String id)
  
必须启动LeaderLatch: leaderLatch.start();
  
一旦启动, LeaderLatch会和其它使用相同latch path的其它LeaderLatch交涉,然后随机的选择其中一个作为leader。 你可以随时查看一个给定的实例是否是leader:

public boolean hasLeadership()
  
类似JDK的CountDownLatch, LeaderLatch在请求成为leadership时有block方法: 
  
public void await()
  
throws InterruptedException,
  
EOFException
  
Causes the current thread to wait until this instance acquires leadership
  
unless the thread is interrupted or closed.

public boolean await(long timeout,TimeUnit unit)throws InterruptedException
  
一旦不使用LeaderLatch了,必须调用close方法。 如果它是leader,会释放leadership, 其它的参与者将会选举一个leader。

异常处理
  
LeaderLatch实例可以增加ConnectionStateListener来监听网络连接问题。 当 SUSPENDED 或 LOST 时, leader不再认为自己还是leader.当LOST 连接重连后 RECONNECTED,LeaderLatch会删除先前的ZNode然后重新创建一个.
  
LeaderLatch用户必须考虑导致leadershi丢失的连接问题。 强烈推荐你使用ConnectionStateListener。

 ```xml
<dependency>
            <groupId>org.apache.curator</groupId>
            curator-recipes</artifactId>
            <version>${curator.version}</version>
            <exclusions>
                <exclusion>
                    log4j</artifactId>
                    <groupId>log4j</groupId>
                </exclusion>
            </exclusions>
        </dependency>
``` 

```javaRetryPolicy retryPolicy = new ExponentialBackoffRetry(1000, 3)
CuratorFramework client = CuratorFrameworkFactory.newClient(zookeeperConnectionString, retryPolicy);
client.getConnectionStateListenable().addListener(connectionStateListener);
client.start();

        leaderLatch = new LeaderLatch(client, zkLatchPath, leaderId);
        leaderLatch.start();
```

http://colobu.com/2014/12/12/zookeeper-recipes-by-example-1/


  
    跟着实例学习ZooKeeper的用法:  Leader选举
  


http://ifeve.com/zookeeper-leader/embed/#?secret=mwCqdwnDV0


### Leader Election
zookeeper 通过 Zab (Zookeeper Atomic Broadcast)  协议保持集群间的数据一致性。
Zab 协议包括两个阶段: Leader Election 和 Atomic Broadcast 。

Leader Election
此阶段集群内会选举出一个 leader,余下机器则会成为 follower。leader 会通过 broadcast 通知所有 follower ,当大部分机 (> 1/2) 器完成了与 leader 的状态同步后,Leader Election 阶段结束。

当 leader 失去大多数 follower 时,集群会再次进入 Leader Election 阶段并选举出新的 leader ,使集群回到正确的状态。

Atomic Broadcast
此阶段 leader 会通过 broadcast 与 follower 通讯,保证 leader 与 follower 具有相同的系统状态。

作者: jaren
链接: https://www.jianshu.com/p/30bcaf55f451
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

