---
title: LVM
author: "-"
date: 2015-10-12T10:32:47+00:00
url: lvm
categories:
  - filesystem
tags:
  - reprint
  - LVM
---
## LVM

https://linux.cn/article-5117-1.html

## commands

vgs命令来自英文词组“volume groups display”的缩写，其功能是用于显示逻辑卷的卷组信息。LVM逻辑卷管理器中vg卷组是由一个或多个pv物理卷组成的设备，使用vgs命令能够查看到其基本信息，如若想要看到更详细的参数信息则需要使用vgdisplay命令。
原文链接：https://www.linuxcool.com/vgs

```Bash
vgs -a

# list logical volume
lvs

# remove logical volume
lvremove /dev/vgubuntu/swap_1

# 在名为 vgubuntu 的卷组中创建 32G 大小的逻辑卷
lvcreate --name swap_1 -L 32G vgubuntu

# vgchange 指令用于修改卷组的属性，经常被用来设置卷组是处于活动状态或者非活动状态。
# -a 设置卷组的活动状态
vgchange -an vgubuntu

vgchange -ay vgubuntu  # 将 vgubuntu 卷组激活
vgchange -an vgubuntu  # 将 vgubuntu 卷组去激活

# pvresize命令的作用是调整一个卷组中的物理卷的大小。pvresize命令可以调整可能已经在卷组中的物理卷的大小，并在其中分配活动的逻辑卷。
# https://linuxcommand.p2hp.com/pvresize
pvresize /dev/mapper/nvme0n1p8_crypt
```

https://blog.51cto.com/livestreaming/6037245

PVE 虚拟机 – 如何扩容虚拟机磁盘空间？

最近遇到一点困扰，就是我创建的虚拟机磁盘空间在使用过程中不足了，该如何动态扩容呢？没想到这里面也藏着不少 linux 基础知识，下面我就来说说。

了解 LVM
每个虚拟机都是需要一块硬盘的，实际是从宿主机划分出来的给虚拟机使用的。

PVE 虚拟机是基于 linux 的，它使用 LVM 管理宿主机磁盘，所以每个虚拟机仅仅是从 LVM 的 VG (volume group卷组)中新建一个固定大小的 LV (logical volume)，
提供给特定的一个虚拟机实例作为虚拟化的硬盘使用。

想实现虚拟机硬盘动态扩容，我们必须明白 linux 的 LVM 硬盘管理，因为只有 LVM 可以实现对一个已有的硬盘分区扩容。

为了说 LVM，我们先得搞明白传统的硬盘管理，传统的硬盘管理包含 4 步: 

块设备: 插在机器上的一块硬盘。
硬盘分区: 把块设备分成多个分区，每个分区固定大小。
文件系统: 如果想要使用硬盘某分区，需要在这个分区上制作文件系统，比如: ext4 格式。
挂载目录: 最终把做好的文件系统通过 mount 命令挂载到某个目录下，就可以读写分区内的数据了。
传统硬盘分区方案的问题是，一旦我们把操作系统安装到某个分区内，那么这个分区大小就无法改变了，随着数据变多硬盘就塞满了。
想要扩容的话，我们只能选定某个目录挂载一块新的硬盘，然后把一些较大的数据手动迁移进去，总之我们会因为容量问题严重影响到使用体验。

LVM 则可以对一个已有的文件系统 (当然对应一个硬盘分区)进行扩容，这就是它厉害的地方。

LVM 的使用过程是这样的: 

块设备: 给机器插上新的硬盘。
硬盘分区: 把块设备分成多个分区 (1个分区用尽整块磁盘也可以，无所谓)，每个分区的大小也是固定的。
创建物理卷 (PV): 按照 LVM 的规则，把每个硬盘分区创建为一个物理卷 (physical volume)。 物理卷Physical volume (PV)：可以在上面建立卷组的媒介，可以是硬盘分区，也可以是硬盘本身或者回环文件（loopback file）。物理卷包括一个特殊的header，其余部分被切割为一块块物理区域（physical extents）。 Think of physical volumes as big building blocks which can be used to build your hard drive.要创建物理卷必须首先对硬盘进行分区，并且将硬盘分区的类型设置为"8e"后，才能使用pvcreate指令将分区初始化为物理卷。
创建卷池 (VG): 新建的物理卷就像一桶矿泉水，把它们加入到一个VG大池子里面，这样池子里的水 (硬件空间)就会变多。卷组Volume group (VG)：将一组物理卷收集为一个管理单元。Group of physical volumes that are used as storage volume (as one disk). They contain logical volumes. Think of volume groups as hard drives.
创建逻辑卷 (LV): 想要划分一块硬盘空间拿来使用，只需要从 VG 里面取一瓢水出来即可，这个划分出来的硬盘空间叫做一个 LV (logical volume)。逻辑卷Logical volume (LV)：虚拟分区，由物理区域（physical extents）组成。A "virtual/logical partition" that resides in a volume group and is composed of physical extents. Think of logical volumes as normal partitions.

物理区域Physical extent (PE)：硬盘可供指派给逻辑卷的最小单位（通常为4MB）。A small part of a disk (usually 4MB) that can be assigned to a logical Volume. Think of physical extents as parts of disks that can be allocated to any partition.

文件系统: 现在可以对 LV 制作文件系统，比如: ext4 格式。
挂载目录: 现在可以把在做好文件系统的 LV 挂载到某个目录，就可以访问了。
我们在安装操作系统的时候可以选择基于 LVM 管理硬盘，安装程序默认会把整个硬盘作为1个分区，创建分区对应的 PV，创建1个 VG并把该 PV加入到 VG中，
然后从 VG 中划出1个 LV格式化 ext4 文件系统，然后把整个操作系统安装到这个 LV里。

大家可以看一下 LVM的一个简明教程，了解从一块裸硬盘到一个LV的全过程命令。

LVM 与虚拟机的关系
首先，PVE本身是把宿主机硬盘做成了LVM，新建虚拟机则划分一个LV给它作为虚拟化的硬盘使用。

所以，我们很容易给虚拟机新增更多虚拟化硬盘，只需要在宿主机上划分更多LV挂给KVM即可。

通过宿主机划分更多的LV，可以全部虚拟化成硬盘提供给某个虚拟机，这样可以让虚拟机中识别的硬盘越来越多。

虚拟机内其实并不知道宿主机上的LVM，它看到的只是若干硬盘对应的块设备，所以它自身也需要使用LVM，才能将更多的块设备加入到VG中，并且对已有的LV进行扩容。

>https://yuerblog.cc/2020/02/09/pve%E8%99%9A%E6%8B%9F%E6%9C%BA-%E5%A6%82%E4%BD%95%E6%89%A9%E5%AE%B9%E8%99%9A%E6%8B%9F%E6%9C%BA%E7%A3%81%E7%9B%98%E7%A9%BA%E9%97%B4%EF%BC%9F/
>https://linux.cn/article-3218-1.html