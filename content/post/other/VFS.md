---
title: VFS
author: "-"
date: 2012-02-25T15:08:30+00:00
url: VFS
categories:
  - Linux
tags:
  - file

---
## VFS
Linux 采用 Virtual Filesystem（VFS）的概念，通过内核在物理存储介质上的文件系统和用户之间建立起一个虚拟文件系统的软件抽象层，使得 Linux 能够支持目前绝大多数的文件系统，不论它是 windows、unix 还是其他一些系统的文件系统，都可以挂载在 Linux 上供用户使用。

VFS 在 Linux 中是一个处理所有 unix 文件系统调用的软件层，同时给不同类型的文件系统提供一个统一的接口。VFS 支持以下归类的三种类型的文件系统：

磁盘文件系统，存储在本地磁盘、U盘、CD等的文件系统，它包含各种不同的文件系统格式，比如 windows NTFS、VFAT，BSD 的 UFS，CD的 CD-ROM 等
网络文件系统，它们存储在网络中的其他主机上，通过网络进行访问，例如 NFS
特殊文件系统，例如 /proc、sysfs 等
VFS 背后的思想就是建立一个通用的文件模型，使得它能兼容所有的文件系统，这个通用的文件模型是以 Linux 的文件系统 EXT 系列为模版构建的。每个特定的文件系统都需要将它物理结构转换为通用文件模型。例如，通用文件模型中，所有的目录都是文件，它包含文件和目录；而在其他的文件类型中，比如 FAT，它的目录就不属于文件，这时，内核就会在内存中生成这样的目录文件，以满足通用文件模型的要求。同时，VFS 在处理实际的文件操作时，通过指针指向特定文件的操作函数。可以认为通用文件模型是面向对象的设计，它实现了几个文件通用模型的对象定义，而具体的文件系统就是对这些对象的实例化。通用文件模型包含下面几个对象：

superblock 存储挂载的文件系统的相关信息
inode 存储一个特定文件的相关信息
file 存储进程中一个打开的文件的交互相关的信息
dentry 存储目录和文件的链接信息


>https://wushifublog.com/2020/05/22/%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3Linux%E5%86%85%E6%A0%B8%E2%80%94%E2%80%94VFS/



VFS并不是一种实际的文件系统，它只存在于内存中，不存在任何外存空间，VFS在系统启动时建立，在系统关闭时消亡。

VFS由超级块、inode、dentry、vfsmount等结构来组成。
