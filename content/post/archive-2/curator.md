---
title: Curator
author: "-"
date: 2015-12-23T02:55:41+00:00
url: /?p=8594
categories:
  - Uncategorized

tags:
  - reprint
---
## Curator

http://macrochen.iteye.com/blog/1366136

Curator是Netflix开源的一套ZooKeeper客户端框架. Netflix在使用ZooKeeper的过程中发现ZooKeeper自带的客户端太底层, 应用方在使用的时候需要自己处理很多事情, 于是在它的基础上包装了一下, 提供了一套更好用的客户端框架. Netflix在用ZooKeeper的过程中遇到的问题, 我们也遇到了, 所以开始研究一下, 首先从他在github上的源码, wiki文档以及Netflix的技术blog入手.

看完官方的文档之后, 发现Curator主要解决了三类问题:

- 封装ZooKeeper client与ZooKeeper server之间的连接处理;
- 提供了一套Fluent风格的操作API;
- 提供ZooKeeper各种应用场景(recipe, 比如共享锁服务, 集群领导选举机制)的抽象封装.

Curator列举的ZooKeeper使用过程中的几个问题
  
初始化连接的问题: 在client与server之间握手建立连接的过程中, 如果握手失败, 执行所有的同步方法(比如create, getData等)将抛出异常
  
自动恢复(failover)的问题: 当client与一台server的连接丢失,并试图去连接另外一台server时, client将回到初始连接模式
  
session过期的问题: 在极端情况下, 出现ZooKeeper session过期, 客户端需要自己去监听该状态并重新创建ZooKeeper实例 .
  
对可恢复异常的处理:当在server端创建一个有序ZNode, 而在将节点名返回给客户端时崩溃, 此时client端抛出可恢复的异常, 用户需要自己捕获这些异常并进行重试
  
使用场景的问题:Zookeeper提供了一些标准的使用场景支持, 但是ZooKeeper对这些功能的使用说明文档很少, 而且很容易用错. 在一些极端场景下如何处理, zk并没有给出详细的文档说明. 比如共享锁服务, 当服务器端创建临时顺序节点成功, 但是在客户端接收到节点名之前挂掉了, 如果不能很好的处理这种情况, 将导致死锁.

Curator主要从以下几个方面降低了zk使用的复杂性:
  
重试机制:提供可插拔的重试机制, 它将给捕获所有可恢复的异常配置一个重试策略, 并且内部也提供了几种标准的重试策略(比如指数补偿).
  
连接状态监控: Curator初始化之后会一直的对zk连接进行监听, 一旦发现连接状态发生变化, 将作出相应的处理.
  
zk客户端实例管理:Curator对zk客户端到server集群连接进行管理. 并在需要的情况, 重建zk实例, 保证与zk集群的可靠连接
  
各种使用场景支持:Curator实现zk支持的大部分使用场景支持(甚至包括zk自身不支持的场景), 这些实现都遵循了zk的最佳实践, 并考虑了各种极端情况.

Curator通过以上的处理, 让用户专注于自身的业务本身, 而无需花费更多的精力在zk本身.

Curator声称的一些亮点:

日志工具
  
内部采用SLF4J 来输出日志
  
采用驱动器(driver)机制, 允许扩展和定制日志和跟踪处理
  
提供了一个TracerDriver接口, 通过实现addTrace()和addCount()接口来集成用户自己的跟踪框架

和Curator相比, 另一个ZooKeeper客户端——zkClient(https://github.com/sgroschupf/zkclient)的不足之处:
  
文档几乎没有
  
异常处理弱爆了(简单的抛出RuntimeException)
  
重试处理太难用了
  
没有提供各种使用场景的实现

对ZooKeeper自带客户端(ZooKeeper类)的"抱怨":
  
只是一个底层实现
  
要用需要自己写大量的代码
  
很容易误用
  
需要自己处理连接丢失, 重试等

Curator几个组成部分

  * Client: 是ZooKeeper客户端的一个替代品, 提供了一些底层处理和相关的工具方法.
  * Framework: 用来简化ZooKeeper高级功能的使用, 并增加了一些新的功能, 比如管理到ZooKeeper集群的连接, 重试处理
  * Recipes: 实现了通用ZooKeeper的recipe, 该组件建立在Framework的基础之上
  * Utilities:各种ZooKeeper的工具类
  * Errors: 异常处理, 连接, 恢复等.
  * Extensions: recipe扩展

Client
  
这是一个底层的API, 应用方基本对这个可以无视, 最好直接从Curator Framework入手
  
主要包括三部分:
  
不间断连接管理
  
连接重试处理

Retry Loop(循环重试)
  
一种典型的用法:


  
    
      Java代码 
      
      <embed src="http://macrochen.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://macrochen.iteye.com/images/icon_star.png" alt="收藏代码" />
  
  
  
    
      RetryLoop retryLoop = client.newRetryLoop();
    
    
      while ( retryLoop.shouldContinue() )
    
    
      {
    
    
         try
    
    
         {
    
    
             // perform your work
    
    
             ...
    
    
             // it's important to re-get the ZK instance as there may have been an error and the instance was re-created
    
    
             ZooKeeper      zk = client.getZookeeper();
    
    
    
    
             retryLoop.markComplete();
    
    
         }
    
    
         catch ( Exception e )
    
    
         {
    
    
             retryLoop.takeException(e);
    
    
         }
    
    
      }
    
  

如果在操作过程中失败, 且这种失败是可重试的, 而且在允许的次数内, Curator将保证操作的最终完成.

另一种使用Callable接口的重试做法:


  
    
      Java代码 
      
      <embed src="http://macrochen.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://macrochen.iteye.com/images/icon_star.png" alt="收藏代码" />
  
  
  
    
      RetryLoop.callWithRetry(client, new Callable()
    
    
      {
    
    
            @Override
    
    
            public Void call() throws Exception
    
    
            {
    
    
                // do your work here - it will get retried if needed
    
    
                return null;
    
    
            }
    
    
      });
    
  

重试策略
  
RetryPolicy接口只有一个方法(以前版本有两个方法):
  
public boolean allowRetry(int retryCount, long elapsedTimeMs);
  
在开始重试之前, allowRetry方法被调用, 其参数将指定当前重试次数, 和操作已消耗时间. 如果允许, 将继续重试, 否则抛出异常.

Curator内部实现的几种重试策略:

  * ExponentialBackoffRetry:重试指定的次数, 且每一次重试之间停顿的时间逐渐增加.
  * RetryNTimes:指定最大重试次数的重试策略
  * RetryOneTime:仅重试一次
  * RetryUntilElapsed:一直重试直到达到规定的时间

Framework
  
是ZooKeeper Client更高的抽象API
  
自动连接管理: 当ZooKeeper客户端内部出现异常, 将自动进行重连或重试, 该过程对外几乎完全透明
  
更清晰的API: 简化了ZooKeeper原生的方法, 事件等, 提供流程的接口

CuratorFrameworkFactory类提供了两个方法, 一个工厂方法newClient, 一个构建方法build. 使用工厂方法newClient可以创建一个默认的实例, 而build构建方法可以对实例进行定制. 当CuratorFramework实例构建完成, 紧接着调用start()方法, 在应用结束的时候, 需要调用close()方法.  CuratorFramework是线程安全的. 在一个应用中可以共享同一个zk集群的CuratorFramework.

CuratorFramework API采用了连贯风格的接口(Fluent Interface). 所有的操作一律返回构建器, 当所有元素加在一起之后, 整个方法看起来就像一个完整的句子. 比如下面的操作:


  
    
      Java代码 
      
      <embed src="http://macrochen.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://macrochen.iteye.com/images/icon_star.png" alt="收藏代码" />
  
  
  
    
      client.create().forPath("/head", new byte[]);
    
    
      client.delete().inBackground().forPath("/head");
    
    
      client.create().withMode(CreateMode.EPHEMERAL_SEQUENTIAL).forPath("/head/child", new byte[]);
    
    
      client.getData().watched().inBackground().forPath("/test");
    
  

方法说明:

  * create(): 发起一个create操作. 可以组合其他方法 (比如mode 或background) 最后以forPath()方法结尾
  * delete(): 发起一个删除操作. 可以组合其他方法(version 或background) 最后以forPath()方法结尾
  * checkExists(): 发起一个检查ZNode 是否存在的操作. 可以组合其他方法(watch 或background) 最后以forPath()方法结尾
  * getData(): 发起一个获取ZNode数据的操作. 可以组合其他方法(watch, background 或get stat) 最后以forPath()方法结尾
  * setData(): 发起一个设置ZNode数据的操作. 可以组合其他方法(version 或background) 最后以forPath()方法结尾
  * getChildren(): 发起一个获取ZNode子节点的操作. 可以组合其他方法(watch, background 或get stat) 最后以forPath()方法结尾
  * inTransaction(): 发起一个ZooKeeper事务. 可以组合create, setData, check, 和/或delete 为一个操作, 然后commit() 提交

.

通知(Notification)
  
Curator的相关代码已经更新了, 里面的接口已经由ClientListener改成CuratorListener了, 而且接口中去掉了clientCloseDueToError方法. 只有一个方法:
  
eventReceived()            当一个后台操作完成或者指定的watch被触发时该方法被调用

UnhandledErrorListener接口用来对异常进行处理.

CuratorEvent(在以前版本为ClientEvent)是对各种操作触发相关事件对象(POJO)的一个完整封装, 而事件对象的内容跟事件类型相关, 下面是对应关系:


  
    
      CREATE
    
    
    
      getResultCode() and getPath()
    
  
  
  
    
      DELETE
    
    
    
      getResultCode() and getPath()
    
  
  
  
    
      EXISTS
    
    
    
      getResultCode(), getPath() and getStat()
    
  
  
  
    
      GET_DATA
    
    
    
      getResultCode(), getPath(), getStat() and getData()
    
  
  
  
    
      SET_DATA
    
    
    
      getResultCode(), getPath() and getStat()
    
  
  
  
    
      CHILDREN
    
    
    
      getResultCode(), getPath(), getStat(), getChildren()
    
  
  
  
    
      WATCHED
    
    
    
      getWatchedEvent()
    
  


名称空间(Namespace)
  
因为一个zk集群会被多个应用共享, 为了避免各个应用的zk patch冲突, Curator Framework内部会给每一个Curator Framework实例分配一个namespace(可选). 这样你在create ZNode的时候都会自动加上这个namespace作为这个node path的root. 使用代码如下:


  
    
      Java代码 
      
      <embed src="http://macrochen.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://macrochen.iteye.com/images/icon_star.png" alt="收藏代码" />
  
  
  
    
      CuratorFramework    client = CuratorFrameworkFactory.builder().namespace("MyApp") ... build();
    
    
       …
    
    
      client.create().forPath("/test", data);
    
    
      // node was actually written to: "/MyApp/test"
    
  

Recipe

Curator实现ZooKeeper的所有recipe(除了两段提交)
  
选举
  
集群领导选举(leader election)

锁服务
  
共享锁: 全局同步分布式锁, 同一时间两台机器只有一台能获得同一把锁.
  
共享读写锁: 用于分布式的读写互斥处理, 同时生成两个锁:一个读锁, 一个写锁, 读锁能被多个应用持有, 而写锁只能一个独占, 当写锁未被持有时, 多个读锁持有者可以同时进行读操作
  
共享信号量: 在分布式系统中的各个JVM使用同一个zk lock path, 该path将跟一个给定数量的租约(lease)相关联, 然后各个应用根据请求顺序获得对应的lease, 相对来说, 这是最公平的锁服务使用方式.
  
多共享锁:内部构件多个共享锁(会跟一个znode path关联), 在acquire()过程中, 执行所有共享锁的acquire()方法, 如果中间出现一个失败, 则将释放所有已require的共享锁; 执行release()方法时, 则执行内部多个共享锁的release方法(如果出现失败将忽略)

队列(Queue)
  
分布式队列:采用持久顺序zk node来实现FIFO队列, 如果有多个消费者, 可以使用LeaderSelector来保证队列的消费者顺序
  
分布式优先队列: 优先队列的分布式版本
  
BlockingQueueConsumer: JDK阻塞队列的分布式版本

关卡(Barrier)
  
分布式关卡:一堆客户端去处理一堆任务, 只有所有的客户端都执行完, 所有客户端才能继续往下处理
  
双分布式关卡:同时开始, 同时结束

计数器(Counter)
  
共享计数器:所有客户端监听同一个znode path, 并共享一个最新的integer计数值
  
分布式AtomicLong(AtomicInteger): AtomicXxx的分布式版本, 先采用乐观锁更新, 若失败再采用互斥锁更新, 可以配置重试策略来处理重试

工具类

Path Cache
  
Path Cache用于监听ZNode的子节点的变化, 当add, update, remove子节点时将改变Path Cache state, 同时返回所有子节点的data和state.
  
Curator中采用了PathChildrenCache类来处理Path Cache, 状态的变化则采用PathChildrenCacheListener来监听.
  
相关用法参见TestPathChildrenCache测试类

注意: 当zk server的数据发生变化, zk client会出现不一致, 这个需要通过版本号来识别这种状态的变化

Test Server
  
用来在测试中模拟一个本地进程内ZooKeeper Server.

Test Cluster
  
用来在测试中模拟一个ZooKeeper Server集群

ZKPaths工具类
  
提供了和ZNode相关的path处理工具方法:

  * getNodeFromPath: 根据给定path获取node name. i.e. "/one/two/three" -> "three"
  *     mkdirs: 根据给定路径递归创建所有node
  *     getSortedChildren: 根据给定路径, 返回一个按序列号排序的子节点列表
  *     makePath: 根据给定的path和子节点名, 创建一个完整path

EnsurePath工具类

直接看例子, 具体的说就是调用多次, 只会执行一次创建节点操作.


  
    
      Java代码 
      
      <embed src="http://macrochen.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://macrochen.iteye.com/images/icon_star.png" alt="收藏代码" />
  
  
  
    
      EnsurePath       ensurePath = new EnsurePath(aFullPathToEnsure);
    
    
      ...
    
    
      String           nodePath = aFullPathToEnsure + "/foo";
    
    
      ensurePath.ensure(zk);   // first time syncs and creates if needed
    
    
      zk.create(nodePath, ...);
    
    
      ...
    
    
      ensurePath.ensure(zk);   // subsequent times are NOPs
    
    
      zk.create(nodePath, ...);
    
  

Notification事件处理
  
Curator对ZooKeeper的事件Watcher进行了封装处理, 然后实现了一套监听机制. 提供了几个监听接口用来处理ZooKeeper连接状态的变化
  
当连接出现异常, 将通过ConnectionStateListener接口进行监听, 并进行相应的处理, 这些状态变化包括:

  * 暂停(SUSPENDED): 当连接丢失, 将暂停所有操作, 直到连接重新建立, 如果在规定时间内无法建立连接, 将触发LOST通知
  * 重连(RECONNECTED): 连接丢失, 执行重连时, 将触发该通知
  * 丢失(LOST): 连接超时时, 将触发该通知

从com.netflix.curator.framework.imps.CuratorFrameworkImpl.validateConnection(CuratorEvent)方法中我们可以知道, Curator分别将ZooKeeper的Disconnected, Expired, SyncConnected三种状态转换成上面三种状态.

参考

  * https://github.com/Netflix/curator
  * https://github.com/sgroschupf/zkclient
  * http://en.wikipedia.org/wiki/Fluent_interface
  * http://huidian.iteye.com/blog/426664 fluent interface中文版
  * http://techblog.netflix.com/2011/11/introducing-curator-netflix-zookeeper.html
  * http://www.ibm.com/developerworks/cn/opensource/os-cn-zookeeper/ 分布式服务框架 Zookeeper - 管理分布式环境中的数据
  * Netflix Curator 使用

### zookeeper curator watcher/listener
http://blog.csdn.net/collonn/article/details/43969045

