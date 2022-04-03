---
title: hbase BufferedMutator
author: "-"
date: 2017-05-22T09:05:37+00:00
url: /?p=10336
categories:
  - Uncategorized

tags:
  - reprint
---
## hbase BufferedMutator

org.apache.hadoop.hbase.client.BufferedMutator主要用来对HBase的单个表进行操作。它和Put类的作用差不多,但是主要用来实现批量的异步写操作。

BufferedMutator替换了HTable的setAutoFlush(false)的作用。

可以从Connection的实例中获取BufferedMutator的实例。在使用完成后需要调用close()方法关闭连接。对BufferedMutator进行配置需要通过BufferedMutatorParams完成。

MapReduce Job的是BufferedMutator使用的典型场景。MapReduce作业需要批量写入,但是无法找到恰当的点执行flush。BufferedMutator接收MapReduce作业发送来的Put数据后,会根据某些因素 (比如接收的Put数据的总量) 启发式地执行Batch Put操作,且会异步的提交Batch Put请求,这样MapReduce作业的执行也不会被打断。

BufferedMutator也可以用在一些特殊的情况上。MapReduce作业的每个线程将会拥有一个独立的BufferedMutator对象。一个独立的BufferedMutator也可以用在大容量的在线系统上来执行批量Put操作,但是这时需要注意一些极端情况比如JVM异常或机器故障,此时有可能造成数据丢失。