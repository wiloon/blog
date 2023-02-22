---
title: free command
author: "-"
date: 2015-02-10T03:13:28+00:00
url: free
categories:
  - Linux
tags:
  - reprint
  - remix
---
## free command

free命令可以查看系统内存的使用情况,-m 参数表示按照兆字节展示。最后两列分别表示用于IO缓存的内存数, 和用于文件系统页缓存的内存数。需要注意的是, 第二行-/+ buffers/cache,看上去缓存占用了大量内存空间。

这是Linux系统的内存使用策略,尽可能的利用内存,如果应用程序需要内存,这部分内存会立即被回收并分配给应用程序。因此,这部分内存一般也被当成是可用内存。

如果可用内存非常少,系统可能会动用交换区 (如果配置了的话) ,这样会增加IO开销 (可以在iostat命令中提现) ,降低系统性能。

```bash
free -h
free -m
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
