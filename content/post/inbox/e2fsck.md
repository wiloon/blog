---
title: e2fsck
author: "-"
date: 2016-04-18T13:46:59+00:00
url: e2fsck
categories:
  - Inbox
tags:
  - reprint
  - remix
---
## e2fsck

linux下磁盘检查修复命令

```bash
# 注意, 是对分区进行检查, 如果参数只写磁盘 /dev/sda, 有可能会报分区表异常之类的... e2fsck: Bad magic number in super-block while trying to open /dev/vdb1
e2fsck -f /dev/sda2
```

e2fsck用于检查和修复ext3和ext2文件系统的硬盘分区,不过这个命令还有专有形式: fsck.ext3, fsck.ext2分别用于检测ext3和ext2。

使用方法:

1。首先在检查之前一定要卸载待检查的文件系统分区。

2。主要参数包括:

-a: 检查 partition,如发现问题会自动修复。

-b: 设定 superblock 位置。

-B size: 指定 size 作为区块大小。

-c: 检查 partition 是否有坏轨。

-C file: 将检查结果储存到 file。

-d: 输出 e2fsck debug 结果。

-f: e2fsck 预设只会对错误的档案系统检查,加上 -f 是强制检查。

-F: 在检查前将硬盘它的参数包括有:

-a:
