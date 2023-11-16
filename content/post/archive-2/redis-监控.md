---
title: redis 监控
author: "-"
date: 2016-12-29T00:06:42+00:00
url: /?p=9631
categories:
  - Inbox
tags:
  - reprint
---
## redis 监控

[http://ghoulich.xninja.org/2016/12/08/how-to-use-latency-monitor-in-redis/](http://ghoulich.xninja.org/2016/12/08/how-to-use-latency-monitor-in-redis/)

Redis 2.8.13引入了一个新特性,叫做延迟监控 (Latency Monitoring) ,它可以帮助用户检查和定位可能的延迟问题。延迟监控由下面的几个组件构成:

延迟挂钩: 这个组件会对延迟敏感的各种代码路径进行采样。
时间序列: 这个组件会记录由各种事件造成的延迟飙升。
报告引擎: 这个组件会从时间序列中取出原始数据。
分析引擎: 这个组件会根据测量方法向用户提供易读的报告和提示信息。
本文只会详细描述延迟监控子系统的各项功能。如果想要了解如何检查和定位Redis的延迟问题,请参考《Redis延迟问题的排查方法》。

[http://www.jianshu.com/p/68485d5c7fb9](http://www.jianshu.com/p/68485d5c7fb9)

Redis Server监控数据采集
  
ping,info all, slowlog get/len/reset/cluster info/config get
  
Redis存活监控
  
redis存活监控 (redis_alive):redis本地监控agent使用ping,如果指定时间返回PONG表示存活,否则redis不能响应请求,可能阻塞或死亡。当返回值不为1时,redis挂了,告警
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 ping | grep -c PONG
  
连接个数 (connected_clients): 客户端连接个数,如果连接数过高,影响redis吞吐量。>5000 时告警
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w "connected_clients" | awk -F":" '{print $2}'
  
连接数使用率(connected_clients_pct): 连接数使用百分比,通过(connected_clients/maxclients)计算；如果达到1,redis开始拒绝新连接创建,告警
  
拒绝的连接个数(rejected_connections): redis连接个数达到maxclients限制,拒绝新连接的个数。告警
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w rejected_connections
  
rejected_connections:0
  
新创建连接个数 (total_connections_received): 如果新创建连接过多,过度地创建和销毁连接对性能有影响,说明短连接严重或连接池使用有问题,告警。
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w total_connections_received
  
total_connections_received:217
  
list阻塞调用被阻塞的连接个数 (blocked_clients): 如果监控数据大于0,告警
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w blocked_clients
  
blocked_clients:0
  
redis分配的内存大小 (used_memory): redis真实使用内存,不包含内存碎片
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w used_memory
  
used_memory:2513656
  
redis进程使用内存大小(used_memory_rss): 进程实际使用的物理内存大小,包含内存碎片；如果rss过大导致内部碎片大,内存资源浪费,和fork的耗时和cow内存都会增大。
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w used_memory_rss
  
used_memory_rss:9728000
  
redis内存碎片率 (mem_fragmentation_ratio): 表示(used_memory_rss/used_memory),碎片率过大,导致内存资源浪费,不设置告警。小于1,表示redis已使用swap分区,则告警
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w mem_fragmentation_ratio
  
mem_fragmentation_ratio:3.89
  
键个数 (keys): redis实例包含的键个数。单实例键个数过大,可能导致过期键的回收不及时。
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w keys | awk -F':' '{print $2}' | awk -F',' '{print $1}' | awk -F'=' '{print $2}'
  
redis处理的命令数 (total_commands_processed): 监控采集周期内的平均qps
  
./redis-cli -c -p 7000 info | grep -w total_commands_processed| awk -F':' '{print $2}'
  
redis当前的qps (instantaneous_ops_per_sec): redis内部较实时的每秒执行的命令数
  
./redis-cli -c -p 7000 info | grep -w instantaneous_ops_per_sec | awk -F':' '{print $2}'
  
请求键被命中次数 (keyspace_hits): redis请求键被命中的次数
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w keyspace_hits | awk -F':' '{print $2}'
  
请求键未被命中次数 (keyspace_misses): redis请求键未被命中的次数
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w keyspace_misses
  
keyspace_misses:122
  
请求键的命中率 (keyspace_hit_ratio):使用keyspace_hits/(keyspace_hits+keyspace_misses)计算所得,命中率低于50%告警
  
最近一次fork阻塞的微秒数 (latest_fork_usec): 最近一次Fork操作阻塞redis进程的耗时数,单位微秒。
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w latest_fork_usec
  
latest_fork_usec:315
  
三、Redis集群监控
  
cluster info 、info
  
实例是否启用集群模式 (cluster_enabled): 通过info的cluster_enabled监控是否启用集群模式。不等于1则告警
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 info | grep -w cluster_enabled
  
cluster_enabled:1
  
集群健康状态  (clusster_state):cluster_state不为OK则告警
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 cluster info
  
cluster_state:ok
  
集群数据槽slots分配情况 (cluster_slots_assigned):集群正常运行时,默认16384个slots
  
不等于16384则告警[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 cluster info | grep -w cluster_slots_ok
  
cluster_slots_ok:16384
  
检测下线的数据槽slots个数 (cluster_slots_fail):集群正常运行时,应该为0. 如果大于0说明集群有slot存在故障。
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 cluster info | grep -w cluster_slots_fail
  
cluster_slots_fail:0
  
集群的节点数  (cluster_known_nodes) : 集群中redis节点的个数
  
[root@tzgdevapp10 bin]# ./redis-cli -c -p 7000 cluster info | grep -w cluster_known_nodes
  
cluster_known_nodes:6
  
文/疲马羁禽 (简书作者)
  
原文链接: [http://www.jianshu.com/p/68485d5c7fb9](http://www.jianshu.com/p/68485d5c7fb9)
  
著作权归作者所有,转载请联系作者获得授权,并标注"简书作者"。
