---
title: OverlayFS
author: "-"
date: 2018-04-05T10:26:43+00:00
url: /?p=12109
categories:
  - inbox
tags:
  - reprint
---
## OverlayFS
https://blog.csdn.net/styshoo/article/details/60715942

Docker存储驱动之OverlayFS简介

简介
  
OverlayFS是一种和AUFS很类似的文件系统,与AUFS相比,OverlayFS有以下特性: 
  
1) 更简单地设计；
  
2) 从3.18开始,就进入了Linux内核主线；
  
3) 可能更快一些。
  
因此,OverlayFS在Docker社区关注度提高很快,被很多人认为是AUFS的继承者。就像宣称的一样,OverlayFS还很年轻。所以,在生成环境使用它时,还是需要更加当心。
  
Docker的overlay存储驱动利用了很多OverlayFS特性来构建和管理镜像与容器的磁盘结构。
  
自从Docker1.12起,Docker也支持overlay2存储驱动,相比于overlay来说,overlay2在inode优化上更加高效。但overlay2驱动只兼容Linux kernel4.0以上的版本。
  
注意: 自从OverlayFS加入kernel主线后,它在kernel模块中的名称就被从overlayfs改为overlay了。但是为了在本文中区别,我们使用OverlayFS代表整个文件系统,而overlay/overlay2表示Docker的存储驱动

### overlay和overlay2
  
OverlayFS (overlay) 的镜像分层与共享
  
OverlayFS使用两个目录,把一个目录置放于另一个之上,并且对外提供单个统一的视角。这两个目录通常被称作层,这个分层的技术被称作union mount。术语上,下层的目录叫做lowerdir,上层的叫做upperdir。对外展示的统一视图称作merged。
  
下图展示了Docker镜像和Docker容器是如何分层的。镜像层就是lowerdir,容器层是upperdir。暴露在外的统一视图就是所谓的merged。


OverlayFS 是类似 AUFS 的现代联合文件系统 (union filesystem) ,但是速度更快,实现更简单。针对 OverlayFS 提供了两个存储驱动: 最初的 overlay,以及更新更稳定的 overlay2。
Note: 如果你使用 OverlayFS,使用 overlay2 而不是 overlay 驱动,因为 overlay2 在 inode 利用率上更高效。要使用新的驱动,你需要系统内核版本 4.0 或者更高版本,除非你是使用 RHEL 或者 CentOS 用户,此时需要内核版本在 3.10.0-514 或更高版本。

先决条件
除了上述的系统内核版本,使用 OverlayFS 还需要以下条件: 
因为 inode 以及后续的 Docker 版本兼容问题,不推荐使用 overlay,满足条件下优先使用 overlay2
以下文件系统支持: 
ext4 (只支持 RHEL 7.1) 
xfs (RHEL 7.2 或更高版本) ,d_type=true 必须开启。使用 xfs_info 验证 ftype 选项是否为 1。
修改 Docker 存储驱动会使已存在的容器和镜像不可访问,可以提前使用 docker save 保存镜像或推送到 Docker Hub (也可以是内部私有镜像仓库) ,防止镜像丢失
mkfs -t xfs -n ftype=1 /PATH/TO/DEVICE  # 开启 d_type 选项
xfs_info /PATH/TO/DEVICE | grep ftype   # 验证是否已支持
配置 overlay 或 overlay2 驱动
满足使用 OverlayFS 的条件后,通过 /etc/docker/daemon.json 加入 overlay2 存储配置项, 重启 docker daemon 即可生效。
{
  "storage-driver": "overlay2"
}
overlay2 驱动是如何工作的
OverlayFS 层 (layers)  在单个 Linux 主机上分为两个目录,并且将它们呈现为单个目录。这些目录统称为层 (layers) ,统一过程称为联合挂载 (union mount) 。OverlayFS 把下层目录称为 lowerdir,上层目录称为 upperdir,统一视图通过称为 merged 自身目录暴露。
overlay 驱动仅适用单个 lower OverlayFS 层,因此需要通过硬链接来实现多层镜像,overlay2 驱动原生支持 128 个 lower OverlayFS 层。这个功能为与层相关的命令如 docker build 和 docker commit 提供了更好的性能,并且在后备文件系统上消耗更少的 inode。

OverlayFS 和 Docker 性能
overlay2 和 overlay 驱动比 aufs 和 devicemapper 拥有更好的性能。在某些情况下,overlay2 的性能表现可能比 btrfs 还要好。不过要注意以下几点: 
Page Caching:  OverlayFS 支持页级别的缓存共享。多个容器访问同样的文件共享此文件的同一个页缓存。这个特性使得 overlay 和 overlay2 驱动高效利用内存以及高密度使用案例的优先选择如 PaaS。
copy_up:  同 AUFS 一样,容器第一次写入文件时,OverlayFS 会有一个 copy-up 的操作。这会增加写入操作的延迟,特别是大文件操作。不过,一旦文件已经被复制,后续文件的写操作都是发生在上层的,不再会有 copy-up 的操作。OverlayFS 的 copy_up 比 AUFS 同样的操作要更快,因为 AUFS 比 OverlayFS 拥有更多的层级,如果在多个 AUFS 层级搜索可能会造成大的延迟。overlay2 也支持多层,但通过缓存减轻了性能损失。
Inode limits: 使用 overlay 存储驱动会导致过多的 inode 损耗。特别是 Docker 主机上存在大量的镜像和容器时尤为明显。格式化文件系统增加可用的 inode 数量是唯一的解决方式。为了避免这个问题,因此建议尽可能的使用 overlay2。
性能最佳实践
以下通用性能最佳实践也适用于 OverlayFS。
使用更快的存储: 使用 SSD
针对写频繁工作负载使用 volumes 功能: Volumes 为写入频繁的工作负载提供了最佳和最可预测的性能。这是因为它们绕过存储驱动,并且避免 thin provisioning 和写时复制的任何潜在开销。Volumes 还有其它好处,如允许容器间共享数据以及持久化数据存储等。

---

https://wiki.opskumu.com/docker/jing-xiang-cun-chu/docker-overlayfs

### kernel does not support overlay fs: 'overlay' is not supported over xfs

```bash
[storage.options]
# Storage options to be passed to underlying storage drivers
mount_program = "/usr/bin/fuse-overlayfs"

```