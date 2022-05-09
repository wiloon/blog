---
title: redis info
author: "-"
date: 2018-02-12T08:53:11+00:00
url: /?p=11876
categories:
  - Inbox
tags:
  - reprint
---
## redis info

instantaneous_input_kbps 每秒读字节数
instantaneous_ops_per_sec 每秒处理指令数
instantaneous_output_kbps 每秒写字节数
keyspace_hitrate Rate of successful lookup of keys in the main dictionary
keyspace_hits : 查找数据库键成功的次数。
  
keyspace_misses : 查找数据库键失败的次数。
  
latest_fork_usec : 最近一次 fork() 操作耗费的毫秒数。

lru_clock : 以分钟为单位进行自增的时钟,用于 LRU 管理
  
master_repl_offset The replication offset of master (in ms)
  
mem_fragmentation_ratio : used_memory_rss 和 used_memory 之间的比率
  
migrate_cached_sockets Current amount of cached sockets
  
rdb_changes_since_last_save : 距离最近一次成功创建持久化文件之后,经过了多少秒。