---
title: docker btrfs
author: "-"
date: 2019-04-14T04:09:04+00:00
url: /?p=14168
categories:
  - container
tags:
  - reprint
---
## docker btrfs
镜像分层与Btrfs共享
  
Docker利用Btrfs subvolumes和快照来管理镜像和容器数据层的硬盘组件(on-disk components)。Btrfs subvolumes看起来像一个正常的Unix文件系统。因此，他们可以有自己的内部目录结构，挂钩到更广泛的Unix文件系统。
  
subvolumes更新文件时涉及写时拷贝操作，写入新文件时涉及从一个底层存储池来按需分配空间的操作。它们既能嵌套也能做快照。下图显示了4个subvolumes。"subvolume 2″和"subvloume 3″是嵌套的，而"subvolume 4"显示它自己的内部目录树。
  
使用btrfs驱动的Docker主机创建镜像和容器的过程如下: 

1.镜像的基础数据层存储在/var/lib/docker/btrfs/subvolumes的Btrfs subvloume中。
  
2.后续的镜像数据层存储为subvolume或快照的父级数据层的一个Btrfs快照中。

https://www.centos.bz/2016/12/docker-and-btrfs-in-practice/