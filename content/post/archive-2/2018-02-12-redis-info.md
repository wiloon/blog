---
title: redis info
author: w1100n
type: post
date: 2018-02-12T08:53:11+00:00
url: /?p=11876
categories:
  - Uncategorized

---

instantaneous\_input\_kbps 每秒读字节数
instantaneous\_ops\_per_sec 每秒处理指令数
instantaneous\_output\_kbps 每秒写字节数
keyspace_hitrate Rate of successful lookup of keys in the main dictionary
keyspace_hits : 查找数据库键成功的次数。
  
keyspace_misses : 查找数据库键失败的次数。
  
latest\_fork\_usec : 最近一次 fork() 操作耗费的毫秒数。

lru_clock : 以分钟为单位进行自增的时钟，用于 LRU 管理
  
master\_repl\_offset The replication offset of master (in ms)
  
mem\_fragmentation\_ratio : used\_memory\_rss 和 used_memory 之间的比率
  
migrate\_cached\_sockets Current amount of cached sockets
  
rdb\_changes\_since\_last\_save : 距离最近一次成功创建持久化文件之后，经过了多少秒。