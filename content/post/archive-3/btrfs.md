---
title: btrfs
author: "-"
date: 2019-03-30T00:11:19+00:00
url: /?p=14005
categories:
  - filesystem
tags:
  - reprint
---
## btrfs

### 禁用 COW

```bash
chattr +C /path/to/dir/
```

<https://typeblog.net/migrate-to-btrfs/>

数据一致性相关的特性

### COW 事务

理解 COW 事务，必须首先理解 COW 和事务这两个术语。

### 什么是 COW?

所谓 COW，即每次写磁盘数据时，先将更新数据写入一个新的 block，当新数据写入成功之后，再更新相关的数据结构指向新 block 。

### 什么是事务？

COW 只能保证单一数据更新的原子性。但文件系统中很多操作需要更新多个不同的元数据，比如创建文件需要修改以下这些元数据:

修改 extent tree，分配一段磁盘空间
  
创建一个新的 inode，并插入 FS Tree 中
  
增加一个目录项，插入到 FS Tree 中
  
任何一个步骤出错，文件便不能创建成功，因此可以定义为一个事务。

下面将演示一个 COW 事务。

A 是 FS Tree 的根节点，新的 inode 的信息将被插入节点 C 。首先，btrfs 将 inode 插入一个新分配的 block C '中，并修改上层节点 B，使其指向新的 block C '；修改 B 也将引发 COW，以此类推，引发一个连锁反应，直到最顶层的 Root A 。当整个过程结束后，新节点 A '变成了 FS Tree 的根。但此时事务并未结束，superblock 依然指向 A 。

## Checksum

## 多设备管理

## Subvolume

## 快照和克隆

## 软件 RAID

## Delay allocation

<https://blog.51cto.com/marvin89/2107489>

<https://www.ibm.com/developerworks/cn/linux/l-cn-btrfs/index.html>

<https://hedzr.com/devops/linux/btrfs-file-system-reviews/>
