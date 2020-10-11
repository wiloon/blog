---
title: Linux文件系统Ext2,Ext3,Ext4
author: wiloon
type: post
date: 2011-12-03T08:27:03+00:00
url: /?p=1687
bot_views:
  - 1
categories:
  - Linux

---
Linux kernel 自 2.6.28 开始正式支持新的文件系统 Ext4。 Ext4 是 Ext3 的改进版，修改了 Ext3 中部分重要的数据结构，而不仅仅像 Ext3 对 Ext2 那样，只是增加了一个日志功能而已。Ext4 可以提供更佳的性能和可靠性，还有更为丰富的功能：

1. 与 Ext3 兼容。执行若干条命令，就能从 Ext3 在线迁移到 Ext4，而无须重新格式化磁盘或重新安装系统。原有 Ext3 数据结构照样保留，Ext4 作用于新数据，当然，整个文件系统因此也就获得了 Ext4 所支持的更大容量。

2. 更大的文件系统和更大的文件。较之 Ext3 目前所支持的最大 16TB 文件系统和最大 2TB 文件，Ext4 分别支持 1EB（1,048,576TB， 1EB=1024PB， 1PB=1024TB）的文件系统，以及 16TB 的文件。

3. 无限数量的子目录。Ext3 目前只支持 32,000 个子目录，而 Ext4 支持无限数量的子目录。

4. Extents。Ext3 采用间接块映射，当操作大文件时，效率极其低下。比如一个 100MB 大小的文件，在 Ext3 中要建立 25,600 个数据块（每个数据块大小为 4KB）的映射表。而 Ext4 引入了现代文件系统中流行的 extents 概念，每个 extent 为一组连续的数据块，上述文件则表示为"该文件数据保存在接下来的 25,600 个数据块中"，提高了不少效率。

5. 多块分配。当写入数据到 Ext3 文件系统中时，Ext3 的数据块分配器每次只能分配一个 4KB 的块，写一个 100MB 文件就要调用 25,600 次数据块分配器，而 Ext4 的多块分配器"multiblock allocator"（mballoc） 支持一次调用分配多个数据块。

6. 延迟分配。Ext3 的数据块分配策略是尽快分配，而 Ext4 和其它现代文件操作系统的策略是尽可能地延迟分配，直到文件在 cache 中写完才开始分配数据块并写入磁盘，这样就能优化整个文件的数据块分配，与前两种特性搭配起来可以显著提升性能。

7. 快速 fsck。以前执行 fsck 第一步就会很慢，因为它要检查所有的 inode，现在 Ext4 给每个组的 inode 表中都添加了一份未使用 inode 的列表，今后 fsck Ext4 文件系统就可以跳过它们而只去检查那些在用的 inode 了。

8. 日志校验。日志是最常用的部分，也极易导致磁盘硬件故障，而从损坏的日志中恢复数据会导致更多的数据损坏。Ext4 的日志校验功能可以很方便地判断日志数据是否损坏，而且它将 Ext3 的两阶段日志机制合并成一个阶段，在增加安全性的同时提高了性能。

9. "无日志"（No Journaling）模式。日志总归有一些开销，Ext4 允许关闭日志，以便某些有特殊需求的用户可以借此提升性能。

10. 在线碎片整理。尽管延迟分配、多块分配和 extents 能有效减少文件系统碎片，但碎片还是不可避免会产生。Ext4 支持在线碎片整理，并将提供 e4defrag 工具进行个别文件或整个文件系统的碎片整理。

11. inode 相关特性。Ext4 支持更大的 inode，较之 Ext3 默认的 inode 大小 128 字节，Ext4 为了在 inode 中容纳更多的扩展属性（如纳秒时间戳或 inode 版本），默认 inode 大小为 256 字节。Ext4 还支持快速扩展属性（fast extended attributes）和 inode 保留（inodes reservation）。

12. 持久预分配（Persistent preallocation）。P2P 软件为了保证下载文件有足够的空间存放，常常会预先创建一个与所下载文件大小相同的空文件，以免未来的数小时或数天之内磁盘空间不足导致下载失败。 Ext4 在文件系统层面实现了持久预分配并提供相应的 API（libc 中的 posix_fallocate()），比应用软件自己实现更有效率。

13. 默认启用 barrier。磁盘上配有内部缓存，以便重新调整批量数据的写操作顺序，优化写入性能，因此文件系统必须在日志数据写入磁盘之后才能写 commit 记录，若 commit 记录写入在先，而日志有可能损坏，那么就会影响数据完整性。Ext4 默认启用 barrier，只有当 barrier 之前的数据全部写入磁盘，才能写 barrier 之后的数据。（可通过 "mount -o barrier=0" 命令禁用该特性。）
  
Ext4 随 Linux kernel 2.6.28 正式发布已有数周，一直苦于找不到测试用的磁盘，正巧年前 Intel 送来几块 SSD 测试样品，这两天就顺带把 SSD 也测了。测试所使用的 Linux 内核版本为 2.6.28.2，测试工具为 IOzone 3.318。

IOzone 测试命令为：

time /opt/iozone/bin/iozone -a -s 4G -q 256 -y 4 >|/root/ext4-iozone-stdout.txt
  
上述命令的说明如下：

Auto Mode
  
File size set to 4194304 KB
  
Using Maximum Record Size 256 KB
  
Using Minimum Record Size 4 KB
  
Command line used: /opt/iozone/bin/iozone -a -s 4G -q 256 -y 4
  
Output is in Kbytes/sec
  
Time Resolution = 0.000001 seconds.
  
Processor cache size set to 1024 Kbytes.
  
Processor cache line size set to 32 bytes.
  
File stride size set to 17 * record size.
  
测试结果除了表明 Intel SSD 的读写速度快得令人咋舌之外，还可以说明 Ext4 的各方面性能都超过了上一代 Ext3，甚至在大多数情况下，比没有日志功能的 Ext2 还要快出不少：