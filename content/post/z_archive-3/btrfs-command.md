---
title: btrfs command
author: "-"
date: 2019-04-14T03:15:40+00:00
url: /?p=14150
categories:
  - Inbox
tags:
  - reprint
---
## btrfs command

```bash
# 安装 btrfs 的用户空间工具
pacman -S btrfs-progs

# 像 df 这样的用户空间工具可能不会准确的计算剩余空间 (因为并没有分别计算文件和元数据的使用情况) 。推荐使用 btrfs filesystem usage 来查看使用情况
btrfs filesystem usage /

#列出当前路径 (path) 下的子卷:
btrfs subvolume list -p path

# 碎片整理
btrfs filesystem defragment -r /
```
