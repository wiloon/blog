---
title: 文件系统 Ext2, Ext3, Ext4, xfs, btrfs
author: "-"
date: 2011-12-03T08:27:03+00:00
url: file-system
categories:
  - filesystem
tags:
  - reprint
  - remix
---
## 文件系统 Ext2, Ext3, Ext4, xfs, btrfs

Linux kernel 自 2.6.28 开始正式支持新的文件系统 Ext4。 Ext4 是 Ext3 的改进版，修改了 Ext3 中部分重要的数据结构，而不仅仅像 Ext3 对 Ext2 那样，只是增加了一个日志功能而已。Ext4 可以提供更佳的性能和可靠性，还有更为丰富的功能:

1. 与 Ext3 兼容。执行若干条命令，就能从 Ext3 在线迁移到 Ext4，而无须重新格式化磁盘或重新安装系统。原有 Ext3 数据结构照样保留，Ext4 作用于新数据，当然，整个文件系统因此也就获得了 Ext4 所支持的更大容量。

2. 更大的文件系统和更大的文件。较之 Ext3 目前所支持的最大 16TB 文件系统和最大 2TB 文件，Ext4 分别支持 1EB (1,048,576TB， 1EB=1024PB， 1PB=1024TB) 的文件系统，以及 16TB 的文件。
FS
3. 无限数量的子目录。Ext3 目前只支持 32,000 个子目录，而 Ext4 支持无限数量的子目录。

4. Extents。Ext3 采用间接块映射，当操作大文件时，效率极其低下。比如一个 100MB 大小的文件，在 Ext3 中要建立 25,600 个数据块 (每个数据块大小为 4KB) 的映射表。而 Ext4 引入了现代文件系统中流行的 extents 概念，每个 extent 为一组连续的数据块，上述文件则表示为"该文件数据保存在接下来的 25,600 个数据块中"，提高了不少效率。

5. 多块分配。当写入数据到 Ext3 文件系统中时，Ext3 的数据块分配器每次只能分配一个 4KB 的块，写一个 100MB 文件就要调用 25,600 次数据块分配器，而 Ext4 的多块分配器"multiblock allocator" (mballoc)  支持一次调用分配多个数据块。

6. 延迟分配。Ext3 的数据块分配策略是尽快分配，而 Ext4 和其它现代文件操作系统的策略是尽可能地延迟分配，直到文件在 cache 中写完才开始分配数据块并写入磁盘，这样就能优化整个文件的数据块分配，与前两种特性搭配起来可以显著提升性能。

7. 快速 fsck。以前执行 fsck 第一步就会很慢，因为它要检查所有的 inode，现在 Ext4 给每个组的 inode 表中都添加了一份未使用 inode 的列表，今后 fsck Ext4 文件系统就可以跳过它们而只去检查那些在用的 inode 了。

8. 日志校验。日志是最常用的部分，也极易导致磁盘硬件故障，而从损坏的日志中恢复数据会导致更多的数据损坏。Ext4 的日志校验功能可以很方便地判断日志数据是否损坏，而且它将 Ext3 的两阶段日志机制合并成一个阶段，在增加安全性的同时提高了性能。

9. "无日志" (No Journaling) 模式。日志总归有一些开销，Ext4 允许关闭日志，以便某些有特殊需求的用户可以借此提升性能。

10. 在线碎片整理。尽管延迟分配、多块分配和 extents 能有效减少文件系统碎片，但碎片还是不可避免会产生。Ext4 支持在线碎片整理，并将提供 e4defrag 工具进行个别文件或整个文件系统的碎片整理。

11. inode 相关特性。Ext4 支持更大的 inode，较之 Ext3 默认的 inode 大小 128 字节，Ext4 为了在 inode 中容纳更多的扩展属性 (如纳秒时间戳或 inode 版本) ，默认 inode 大小为 256 字节。Ext4 还支持快速扩展属性 (fast extended attributes) 和 inode 保留 (inodes reservation) 。

12. 持久预分配 (Persistent preallocation) 。P2P 软件为了保证下载文件有足够的空间存放，常常会预先创建一个与所下载文件大小相同的空文件，以免未来的数小时或数天之内磁盘空间不足导致下载失败。 Ext4 在文件系统层面实现了持久预分配并提供相应的 API (libc 中的 posix_fallocate()) ，比应用软件自己实现更有效率。

13. 默认启用 barrier。磁盘上配有内部缓存，以便重新调整批量数据的写操作顺序，优化写入性能，因此文件系统必须在日志数据写入磁盘之后才能写 commit 记录，若 commit 记录写入在先，而日志有可能损坏，那么就会影响数据完整性。Ext4 默认启用 barrier，只有当 barrier 之前的数据全部写入磁盘，才能写 barrier 之后的数据。 (可通过 "mount -o barrier=0" 命令禁用该特性。)
  
Ext4 随 Linux kernel 2.6.28 正式发布已有数周，一直苦于找不到测试用的磁盘，正巧年前 Intel 送来几块 SSD 测试样品，这两天就顺带把 SSD 也测了。测试所使用的 Linux 内核版本为 2.6.28.2，测试工具为 IOzone 3.318。

IOzone 测试命令为:

time /opt/iozone/bin/iozone -a -s 4G -q 256 -y 4 >|/root/ext4-iozone-stdout.txt
  
上述命令的说明如下:

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
  
测试结果除了表明 Intel SSD 的读写速度快得令人咋舌之外，还可以说明 Ext4 的各方面性能都超过了上一代 Ext3，甚至在大多数情况下，比没有日志功能的 Ext2 还要快出不少:

### ext4, xfs

centos7.0 开始默认文件系统是xfs，centos6 是 ext4，centos5 是ext3

ext3 和 ext4 的最大区别在于，ext3 在 fsck 时需要耗费大量时间 (文件越多，时间越长) ，而 ext4 在 fsck 时用的时间会少非常多

fsck (file system check) 用来检查和维护不一致的文件系统。若系统掉电或磁盘发生问题，可利用 fsck 命令对文件系统进行检查

ext4 是第四代扩展文件系统 (英语: Fourth EXtended filesystem，缩写为 ext4) 是 linux 系统下的日志文件系统，是 ext3 文件系统的后继版本
ext4 的文件系统容量达到 1EB，而文件容量则达到 16TB，这是一个非常大的数字了。对一般的台式机和服务器而言，这可能并不重要，但对于大型磁盘阵列的用户而言，这就非常重要了。
ext3 目前只支持32000个子目录，而ext4取消了这一限制，理论上支持无限数量的子目录

xfs 是一种非常优秀的日志文件系统，它是 SGI 公司设计的。xfs 被称为业界最先进的、最具可升级性的文件系统技术

xfs 是一个64位文件系统，最大支持 8EB 减 1 字节的单个文件系统，实际部署时取决于宿主操作系统的最大块限制。对于一个 32 位 Linux 系统，文件和文件系统的大小会被限制在 16TB

xfs 在很多方面确实做的比 ext4 好，ext4 受限制于磁盘结构和兼容问题，可扩展性和 scalability 确实不如 xfs，另外 xfs 经过很多年发展，各种锁的细化做的也比较好。

Btrfs 性能太差，稳定性不行，提不上 prodcution use..3. 要知道 XFS 的 Mainainer Dave Chineer 是受雇于Redhat, 而 Ext4 的 Maintainer Ted 受雇于google

Ext4 作为传统的文件系统确实非常成熟稳定，但是随着存储需求的越来越大，Ext4 渐渐适应不了了。比如说现在虽然Ext4 目录索引采用了Hash Index Tree, 但是依然限制高度为2. 做过实际测试Ext4的单个目录文件超过200W个，性能下降的就比较厉害了。
由于历史磁盘结构原因Ext4 的inode 个数限制(32位数)最多只能有大概40多亿文件。而且Ext4的单个文件大小最大只能支持到16T(4K block size) 的话，这些至少对于目前来说已经是瓶颈了...而XFS使用64位管理空间，文件系统规模可以达到EB级别，可以说未来几年XFS彻底取代Ext4是早晚的事情！另外，我看了一下XFS 目前redhat 至少投入了5个Kernel developer 在上面，因为XFS 是基于B+Ttree 管理元数据，即将支持reflink, dedupe等高级特性(Oracle 开发者已经开发了patch)。综上所述，XFS 取代Ext4 已经成为必然。

作者: wangsl
链接: [https://www.zhihu.com/question/24413471/answer/38883787](https://www.zhihu.com/question/24413471/answer/38883787)
来源: 知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

更多对比
ext4不支持透明压缩、重复数据删除或者透明加密。技术上支持了快照，但该功能还处于实验性阶段。xfs也不能压缩，XFS 是基于B+ Ttree 管理元数据，即将支持reflink, dedupe等高级特性。
Ext4受限制于磁盘结构和兼容问题，可扩展性和scalability不如XFS。
虽然Ext4 目录索引采用了Hash Index Tree, 但是依然限制高度为2。
由于历史磁盘结构原因Ext4 的inode 个数限制(32位数)最多只能有大概40多亿文件。而且Ext4的单个文件大小最大只能支持到16T(4K block size) ，目前来说已经是瓶颈。XFS使用64位管理空间，文件系统规模可以达到EB级别。

XFS文件系统的卷无法被直接收缩，只能通过“备份->重灌->还原”的方式间接进行容量缩减 (这也是云端主机供应商会告知存储空间只能增加不能缩减的其中一个原因) ，在准备多一组存储卷的情况下，有工具可对XFS卷进行上述操作: xfsdump和xfsrestore。

[http://xiaqunfeng.cc/2017/07/06/XFS-vs-EXT4/](http://xiaqunfeng.cc/2017/07/06/XFS-vs-EXT4/)

### XFS vs EXT4

ceph 默认的文件系统是 XFS，centos7之前的版本默认文件系统是EXT4，现在是XFS，这里对比了一下，然后针对4k大小的随机读写进行了小小的测试。

前言
Linux操作系统有很多不同的文件系统选择，所有现有的默认文件系统都是ext4。 通常文件系统被用来处理当程序不再使用信息之后如何保存信息，如何管理信息的可访问性，其他信息 (元数据）与数据本身如何相关联等。

EXT4
Ext4是第四代扩展文件系统的缩写，它是2008年推出的。它是一个真正可靠的文件系统，它几乎在过去几年的大部分发行版中一直是默认选项，它是由比较老的代码生成的。它是一个日志文件系统，意味着它会对文件在磁盘中的位置以及任何其它对磁盘的更改做记录。如果系统崩溃，得益于journal技术，文件系统很少会损坏。

最大单个文件大小可以从16 GB到16 TB
最大文件系统大小为1EB (exabyte）
最大值包含64,000个子目录 (ext3中的32,000个）

XFS
XFS是由SGI为其IRIX平台设计的高性能64位日志文件系统。 XFS具有各种改进，使其能够在文件系统群体列表中脱颖而出，例如用于元数据操作的日志记录，可扩展/并行I / O，挂起/恢复I / O，在线碎片整理，延迟性能分配，等等

大概在2002年，XFS被合入Linux内核，2009年RHEL Linux版本5.4使用了XFS文件系统。 由于其高性能，架构可扩展性和鲁棒性，XFS一直是很多企业系统的首选，特别是拥有大量数据的企业系统。 现在，RHEL / CentOS 7和Oracle Linux使用XFS作为其默认文件系统。

最大单个文件大小可以是16 TB到16 Exabytes
最大文件系统大小为8EB (exabyte）
缺点：XFS文件系统不能缩小，当删除大量文件时会性能下降。

更多对比
ext4不支持透明压缩、重复数据删除或者透明加密。技术上支持了快照，但该功能还处于实验性阶段。xfs也不能压缩，XFS 是基于B+ Ttree 管理元数据，即将支持reflink, dedupe等高级特性。
Ext4受限制于磁盘结构和兼容问题，可扩展性和scalability不如XFS。
虽然Ext4 目录索引采用了Hash Index Tree, 但是依然限制高度为2。
由于历史磁盘结构原因Ext4 的inode 个数限制(32位数)最多只能有大概40多亿文件。而且Ext4的单个文件大小最大只能支持到16T(4K block size) ，目前来说已经是瓶颈。XFS使用64位管理空间，文件系统规模可以达到EB级别。

>[http://xiaqunfeng.cc/2017/07/06/XFS-vs-EXT4/](http://xiaqunfeng.cc/2017/07/06/XFS-vs-EXT4/)
