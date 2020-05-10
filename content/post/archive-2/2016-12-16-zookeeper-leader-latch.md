---
title: zookeeper leader latch
author: wiloon
type: post
date: 2016-12-16T04:59:05+00:00
url: /?p=9564
categories:
  - Uncategorized

---
https://curator.apache.org/zk-compatibility.html
  
curator-framework 4.x 同时支持zookeeper 3.4.x, 3.5.x
  
curator4 默认依赖zookeeper 3.5
  
使用zookeeper3.4时,需要把zookeeper排除掉,再依赖zookeeper3.4<pre data-language=XML>

<code class="language-markup line-numbers">&lt;dependency&gt;
    &lt;groupId&gt;org.apache.curator&lt;/groupId&gt;
    &lt;artifactId&gt;curator-recipes&lt;/artifactId&gt;
    &lt;version&gt;${curator-version}&lt;/version&gt;
    &lt;exclusions&gt;
        &lt;exclusion&gt;
            &lt;groupId&gt;org.apache.zookeeper&lt;/groupId&gt;
            &lt;artifactId&gt;zookeeper&lt;/artifactId&gt;
        &lt;/exclusion&gt;
    &lt;/exclusions&gt;
&lt;/dependency&gt;
</code></pre> 

leader latch/leader election
  
在分布式计算中， leader election是很重要的一个功能， 这个选举过程是这样子的: 指派一个进程作为组织者，将任务分发给各节点。 在任务开始前， 哪个节点都不知道谁是leader或者coordinator. 当选举算法开始执行后，每个节点最终会得到一个唯一的节点作为任务leader.
  
除此之外， 选举还经常会发生在leader意外宕机的情况下，新的leader要被选举出来。

Curator 有两种选举recipe， 你可以根据你的需求选择合适的。

public LeaderLatch(CuratorFramework client, String latchPath)
  
public LeaderLatch(CuratorFramework client, String latchPath, String id)
  
必须启动LeaderLatch: leaderLatch.start();
  
一旦启动， LeaderLatch会和其它使用相同latch path的其它LeaderLatch交涉，然后随机的选择其中一个作为leader。 你可以随时查看一个给定的实例是否是leader:

public boolean hasLeadership()
  
类似JDK的CountDownLatch， LeaderLatch在请求成为leadership时有block方法：
  
public void await()
  
throws InterruptedException,
  
EOFException
  
Causes the current thread to wait until this instance acquires leadership
  
unless the thread is interrupted or closed.

public boolean await(long timeout,TimeUnit unit)throws InterruptedException
  
一旦不使用LeaderLatch了，必须调用close方法。 如果它是leader,会释放leadership， 其它的参与者将会选举一个leader。

异常处理
  
LeaderLatch实例可以增加ConnectionStateListener来监听网络连接问题。 当 SUSPENDED 或 LOST 时, leader不再认为自己还是leader.当LOST 连接重连后 RECONNECTED,LeaderLatch会删除先前的ZNode然后重新创建一个.
  
LeaderLatch用户必须考虑导致leadershi丢失的连接问题。 强烈推荐你使用ConnectionStateListener。<pre data-language=XML>

 <code class="language-markup line-numbers">&lt;dependency&gt;
            &lt;groupId&gt;org.apache.curator&lt;/groupId&gt;
            &lt;artifactId&gt;curator-recipes&lt;/artifactId&gt;
            &lt;version&gt;${curator.version}&lt;/version&gt;
            &lt;exclusions&gt;
                &lt;exclusion&gt;
                    &lt;artifactId&gt;log4j&lt;/artifactId&gt;
                    &lt;groupId&gt;log4j&lt;/groupId&gt;
                &lt;/exclusion&gt;
            &lt;/exclusions&gt;
        &lt;/dependency&gt;
</code></pre> 

<pre><code class="language-java line-numbers">RetryPolicy retryPolicy = new ExponentialBackoffRetry(1000, 3)
CuratorFramework client = CuratorFrameworkFactory.newClient(zookeeperConnectionString, retryPolicy);
client.getConnectionStateListenable().addListener(connectionStateListener);
client.start();

        leaderLatch = new LeaderLatch(client, zkLatchPath, leaderId);
        leaderLatch.start();
</code></pre>

http://colobu.com/2014/12/12/zookeeper-recipes-by-example-1/

<blockquote class="wp-embedded-content" data-secret="mwCqdwnDV0">
  <p>
    <a href="http://ifeve.com/zookeeper-leader/">跟着实例学习ZooKeeper的用法： Leader选举</a>
  </p>
</blockquote>

<iframe title="《跟着实例学习ZooKeeper的用法： Leader选举》—并发编程网 - ifeve.com" class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://ifeve.com/zookeeper-leader/embed/#?secret=mwCqdwnDV0" data-secret="mwCqdwnDV0" width="600" height="338" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>