---
title: zookeeper client zkCli.sh
author: "-"
date: 2016-12-29T00:12:42+00:00
url: /?p=9633
categories:
  - Uncategorized

tags:
  - reprint
---
## zookeeper client zkCli.sh
```bash
#zkCli.sh
#连接zookeeper
bin/zkCli.sh -server localhost:2181

#键入help查看所有支持的命令
help

#查看根节点列表
ls /

#创建节点
create /k0 v0

#创建Ephemeral节点
create -e /test

#创建sequential节点
create -s /test

#设置节点数据
set /test "111111"

#查看节点数据
get /test 

#删除节点
delete /test
```

zookeeper提供了很多方便的功能,方便我们查看服务器的状态,增加,修改,删除数据 (入口是zkServer.sh和zkCli.sh) 。
  
还提供了一系列四字命令,方便我们跟服务器进行各种交互,来确认服务器当前的工作情况 (这也是服务器监控告警的基础) 。
  
本文所讲的zkCli.sh和zkServer.sh均位于以下目录中: 
  
/usr/local/zookeeper-server1
  
目录分布情况请参考我的另一篇文章: 
  
zookeeper集群搭建 - http://www.cnblogs.com/linuxbug/p/4840137.html
  
zkServer.sh
  
提供的主要功能如下: 

1. 查看服务器状态

[root@rocket zookeeper-server1]# bin/zkServer.sh status

JMX enabled by default

Using config: /usr/local/zookeeper-server1/bin/../conf/zoo.cfg

Mode: leader

2. 启停服务器

[root@rocket zookeeper-server1]# bin/zkServer.sh help

JMX enabled by default

Using config: /usr/local/zookeeper-server1/bin/../conf/zoo.cfg

Usage: bin/zkServer.sh {start|start-foreground|stop|restart|status|upgrade|print-cmd}

四字命令
  
功能描述
  
conf
  
输出相关服务配置的详细信息。
  
cons
  
列出所有连接到服务器的客户端的完全的连接 /会话的详细信息。包括"接受 / 发送"的包数量、会话 id 、操作延迟、最后的操作执行等等信息。
  
dump
  
列出未经处理的会话和临时节点。
  
envi
  
输出关于服务环境的详细信息 (区别于 conf命令) 。
  
reqs
  
列出未经处理的请求
  
ruok
  
测试服务是否处于正确状态。如果确实如此,那么服务返回"imok ",否则不做任何相应。
  
stat
  
输出关于性能和连接的客户端的列表。
  
wchs
  
列出服务器 watch的详细信息。
  
wchc
  
通过 session列出服务器 watch的详细信息,它的输出是一个与watch相关的会话的列表。
  
wchp
  
通过路径列出服务器 watch的详细信息。它输出一个与 session相关的路径。
  
查看连接到结点上所有的client信息,被选作leader还是follower

[root@rocket zookeeper-server1]# echo stat|nc 127.0.0.1 2181

Zookeeper version: 3.4.6-1569965, built on 02/20/2014 09:09 GMT

Clients:

/127.0.0.1:52547[][1]

/0:0:0:0:0:0:0:1:53913[1][2]

 

Latency min/avg/max: 0/3/9

Received: 13

Sent: 12

Connections: 2

Outstanding: 0

Zxid: 0x300000005

Mode: leader

Node count: 4

 

测试是否启动了该Server,若回复imok表示已经启动

[root@rocket zookeeper-server1]# echo ruok|nc 127.0.0.1 2181

Imok

查看连接到服务器的所有客户端的会话信息

[root@rocket zookeeper-server1]# echo cons|nc 127.0.0.1 2181

/127.0.0.1:52552[][1]

/0:0:0:0:0:0:0:1:53913[1][3]

http://izualzhy.cn/c/cpp/2016/09/24/zkcli-introduction

 [1]: queued=0,recved=1,sent=0
 [2]: queued=0,recved=4,sent=4
 [3]: queued=0,recved=88,sent=88,sid=0x14ffe63e9ce0001,lop=PING,est=1443098949817,to=30000,lcxid=0x2,lzxid=0x30000000a,lresp=1443099814079,llat=0,minlat=0,avglat=0,maxlat=3