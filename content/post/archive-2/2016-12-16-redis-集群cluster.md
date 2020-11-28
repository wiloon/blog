---
title: redis 集群/cluster
author: w1100n
type: post
date: 2016-12-16T02:55:44+00:00
url: /?p=9561
categories:
  - Uncategorized

---
```bash
#centos
sudo yum install epel-release
yum install redis

```

mkdir redis-cluster
  
cd redis-cluster
  
mkdir 7000 7001 7002 7003 7004 7005

在文件夹 7000 至 7005 中， 各创建一个 redis.conf 文件， 文件的内容可以使用上面的示例配置文件， 但记得将配置中的端口号从 7000 改为与文件夹名字相同的号码。

port 7000
  
cluster-enabled yes
  
cluster-config-file nodes.conf
  
cluster-node-timeout 5000
  
appendonly yes

cd 7000
  
../redis-server ./redis.conf

搭建集群
  
现在我们已经有了六个正在运行中的 Redis 实例， 接下来我们需要使用这些实例来创建集群， 并为每个节点编写配置文件。

通过使用 Redis 集群命令行工具 redis-trib ， 编写节点配置文件的工作可以非常容易地完成： redis-trib 位于 Redis 源码的 src 文件夹中， 它是一个 Ruby 程序， 这个程序通过向实例发送特殊命令来完成创建新集群， 检查集群， 或者对集群进行重新分片（reshared）等工作。

```bash./redis-trib.rb create --replicas 1 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005
```

redis requires Ruby version >= 2.2.2
  
https://blog.csdn.net/FengYe_YuLu/article/details/77628094

这个命令在这里用于创建一个新的集群, 选项–replicas 1 表示我们希望为集群中的每个主节点创建一个从节点。

之后跟着的其他参数则是这个集群实例的地址列表,3个master3个slave redis-trib 会打印出一份预想中的配置给你看， 如果你觉得没问题的话， 就可以输入 yes ， redis-trib 就会将这份配置应用到集群当中,让各个节点开始互相通讯,最后可以得到如下信息：

[OK] All 16384 slots covered

/System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/rubygems/core\_ext/kernel\_require.rb:55:in `require': cannot load such file — redis (LoadError)

注意 ：kernel_require.rb:55:in`require': cannot load such file — redis
  
这里就是缺什么，安装什么

我这里用命令：
  
gem intall redis
  
http://greemranqq.iteye.com/blog/2229640

http://redis.cn/topics/cluster-tutorial.html