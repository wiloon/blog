---
title: free
author: "-"
date: 2015-02-10T03:13:28+00:00
url: free
categories:
  - Linux
tags:$
  - reprint
---
## free

```bash
free -h
```

```bash
              total        used        free      shared  buff/cache   available
Mem:          8.7Gi       4.6Gi       437Mi       1.0Mi       3.8Gi       3.9Gi
Swap:            0B          0B          0B
```

- Mem：表示物理内存统计。
- total：表示物理内存总量( total = used + free + buff/cache )。
- used：total - free - buff/cache, 表示总计分配给缓存 (包含buffers 与cache ）使用的数量，但其中可能部分缓存并未实际使用。
- free：未被分配的内存。
- shared：共享内存。Memory used (mostly) by tmpfs (Shmem in /proc/meminfo)
- buffers：kernel buffers, 系统分配但未被使用的buffers数量。
- cached：page cache and slabs, 系统分配但未被使用的cache数量。
- available: 启动新的应用程序时可以使用的内存,
- buffers/cache：表示物理内存的缓存统计。
used2：也就是第一行中的used – buffers - cached也是实际使用的内存总量。 // used2为第二行
free2 = buffers1 + cached1 + free1 // free2为第二行，buffers1等为第一行
free2：未被使用的buffers与cache和未被分配的内存之和，这就是系统当前实际可用内存。
- Swap：表示硬盘上交换分区的使用情况。
- 