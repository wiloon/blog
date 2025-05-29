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
  - linux
  - remix
---
## LVM

## commands

```bash
# lvreduce, 用于减小 LVM 逻辑卷（Logical Volume）的大小
# -r, 同时调整（resize）文件系统的大小（调用 resize2fs xfs_growfs 等）
# -L -40G 减小逻辑卷的大小 40GB（注意 - 表示减小）
# /dev/ubuntu-vg/root 要调整的逻辑卷路径（通常是根分区）
sudo lvreduce -r -L -40G /dev/ubuntu-vg/root
```

## LVM 的基本概念

通过 LVM 技术，可以屏蔽掉磁盘分区的底层差异，在逻辑上给文件系统提供了一个卷的概念，然后在这些卷上建立相应的文件系统。下面是 LVM 中主要涉及的一些概念。
PM 物理存储设备 (Physical Media): 指系统的存储设备文件，比如 某一块硬盘, /dev/sda、/dev/sdb 等。 或者 设备映射器（Device Mapper）管理的加密分区. /dev/mapper/nvme0n1p8_crypt
PV (物理卷 Physical Volume)： PV 可以看做是硬盘上的分区, 指硬盘分区或者从逻辑上看起来和硬盘分区类似的设备 (比如 RAID 设备)。
PE (Physical Extent)：PV(物理卷)中可以分配的最小存储单元称为 PE，PE 的大小是可以指定的。

VG (卷组, Volume Group)： 卷组: 物理卷的组合. 类似于非 LVM 系统中的**物理硬盘**，一个 LVM 卷组由一个或者多个 PV(物理卷) 组成。 
                         卷组是 LVM 的中间层，VG 将多个物理卷（Physical Volumes, PV）组合在一起，
                         以便在其上创建逻辑卷（Logical Volumes, LV）。

LV (逻辑卷 Logical Volume)：类似于非 LVM 系统上的**硬盘分区**，LV 建立在 VG 上，可以在 LV 上建立文件系统。
LE (Logical Extent)：LV(逻辑卷)中可以分配的最小存储单元称为 LE，在同一个卷组中，LE 的大小和 PE 的大小是一样的，并且一一对应。
可以这么理解，LVM 是把硬盘的分区分成了更小的单位(PE)，再用这些单元拼成更大的看上去像分区的东西(PV)，进而用 PV 拼成看上去像硬盘的东西(VG)，最后在这个新的硬盘上创建分区(LV)。文件系统则建立在 LV 之上，这样就在物理硬盘和文件系统中间添加了一层抽象(LVM)。下图大致描述了这些概念之间的关系：


```Bash
# 扫描系统中连接的所有硬盘，列出找到的物理卷列表。使用 pvscan 命令的 -n 选项可以显示硬盘中的不属于任何卷组的物理卷，这些物理卷是未被使用的。
# -d：调试模式；
# -e：仅显示属于输出卷组的物理卷；
# -n：仅显示不属于任何卷组的物理卷；
# -s：短格式输出；
# -u：显示UUID。
sudo pvscan
# 输出格式化的物理卷信息报表。使用 pvs 命令仅能得到物理卷的概要信息，如果要得到更加详细的信息可以使用 pvdisplay 命令。
# --noheadings：不输出标题头；
# --nosuffix：不输出空间大小的单位。

sudo pvs

# 显示物理卷的属性。pvdisplay 命令显示的物理卷信息包括：物理卷名称、所属的卷组、物理卷大小、PE 大小、总 PE 数、可用 PE 数、已分配的 PE 数和 UUID
sudo pvdisplay

# 查找系统中存在的 LVM 卷组，并显示找到的卷组列表。vgscan 命令仅显示找到的卷组的名称和 LVM 元数据类型，
# 要得到卷组的详细信息需要使用 vgdisplay 命令。
sudo vgscan

# 查看卷组状态, VG Status            有可能是 resizable, available, inactive
sudo vgdisplay

# 扫描当前系统中存在的所有的LVM逻辑卷。使用lvscan指令可以发现系统中的所有逻辑卷，及其对应的设备文件。
sudo lvscan
# 报告有关逻辑卷的信息
sudo lvs
# lvdisplay命令用于显示LVM逻辑卷空间大小、读写状态和快照信息等属性。如果省略”逻辑卷”参数，则lvdisplay命令显示所有的逻辑卷属性。
# 否则，仅显示指定的逻辑卷属性。
sudo lvdisplay

# 将物理卷添加到已经存在的卷组
vgextend vg_data /dev/sde1 /dev/sdf1 /dev/sdg1
```

## pvcreate

LVM 逻辑卷管理器技术由物理卷、卷组和逻辑卷组成, 其中 pvcreate 命令的工作属于第一个环节 - 创建物理卷设备。

pvcreate 命令 用于将物理硬盘分区初始化为物理卷 (Physical Volume) ，供 LVM 使用。
使用这个命令之前，请确保在该设备上的数据已经备份，因为 pvcreate 会覆盖设备上的分区表信息，从而导致数据丢失。

-f：强制创建物理卷，不需要用户确认；
-u：指定设备的UUID；
-y：所有的问题都回答“yes”；
-Z：是否利用前4个扇区。

```Bash
pvcreate /dev/mapper/nvme0n1p8_crypt
```

## vgcreate

指令用于创建 LVM 卷组 (Volume Group)。

```Bash
# the name of new volume group: vgubuntu
vgcreate vgubuntu /dev/mapper/nvme0n1p8_crypt
# /dev/mapper/nvme0n1p8_crypt 是将被包含在卷组 vgubuntu 中的物理卷。这通常是通过之前的 pvcreate 命令初始化的设备。
```

https://www.cnblogs.com/sparkdev/p/10130934.html

https://linux.cn/article-5117-1.html

LVM 是 Logical Volume Manager 的缩写，中文一般翻译为 "逻辑卷管理"，它是 Linux 下对磁盘分区进行管理的一种机制。
LVM 是建立在磁盘分区和文件系统之间的一个逻辑层，系统管理员可以利用 LVM 在不重新对磁盘分区的情况下动态的调整分区的大小。
如果系统新增了一块硬盘，通过 LVM 就可以将新增的硬盘空间直接扩展到原来的磁盘分区上。

LVM 的优点如下：

文件系统可以跨多个磁盘，因此大小不再受物理磁盘的限制。
可以在系统运行状态下动态地扩展文件系统大小。
可以以镜像的方式冗余重要数据到多个物理磁盘上。
可以很方便地导出整个卷组，并导入到另外一台机器上。
LVM 也有一些缺点：

在从卷组中移除一个磁盘的时候必须使用 reducevg 命令(这个命令要求 root 权限，并且不允许在快照卷组中使用)。
当卷组中的一个磁盘损坏时，整个卷组都会受影响。
因为增加了一个逻辑层，存储的性能会受影响。
LVM 的优点对服务器的管理非常有用，但对于桌面系统的帮助则没有那么显著，所以需要我们根据使用的场景来决定是否应用 LVM。

## commands

### vgs

列出所有的卷组

vgs 命令来自英文词组 “volume groups display” 的缩写，其功能是用于显示逻辑卷的卷组信息。

LVM 逻辑卷管理器中 vg 卷组是由一个或多个 pv 物理卷组成的设备，使用 vgs 命令能够查看到其基本信息，如若想要看到更详细的参数信息则需要使用 vgdisplay 命令。
原文链接：https://www.linuxcool.com/vgs

```Bash
sudo vgs -a
# 显示卷组属性
# -a|--all
# -A 仅显示活动卷组的属性
# -s 使用短格式输出信息
```

### lvcreate

在卷组中创建逻辑卷 (Logical Volume)
LVM 系统中的分区

```Bash
# -L 16G 指定逻辑卷的大小为 16 GB。
# vgubuntu 是逻辑卷所基于的卷组名称。该卷组应该已经通过 vgcreate 命令创建并包含一个或多个物理卷。
lvcreate --name swap_1 -L 16G vgubuntu
lvcreate --name root -L 67g vgubuntu
```

```Bash
# list logical volume
lvs

# remove logical volume
lvremove /dev/vgubuntu/swap_1

# 在名为 vgubuntu 的卷组中创建 32G 大小的逻辑卷
lvcreate --name swap_1 -L 32G vgubuntu

# vgchange 指令用于修改卷组的属性，经常被用来设置卷组是处于活动状态或者非活动状态。
# -a 设置卷组的活动状态, 指定是否激活或停用逻辑卷：a 表示 activate（激活）
# 将 vgubuntu 卷组激活
# y 表示 “yes”，即 激活逻辑卷（n 则表示停用）
vgchange -ay vgubuntu

# 参数里不放卷组名字,激活系统中的所有分区
sudo vgchange -ay

# 将 vgubuntu 停用（deactivate）
vgchange -an vgubuntu
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
创建物理卷 (PV): 按照 LVM 的规则，把每个硬盘分区创建为一个物理卷 (physical volume)。 
物理卷 Physical volume (PV)：可以在上面建立卷组的媒介，可以是硬盘分区，也可以是硬盘本身或者回环文件（loopback file）。
物理卷包括一个特殊的 header，其余部分被切割为一块块物理区域（physical extents）。 
Think of physical volumes as big building blocks which can be used to build your hard drive.
要创建物理卷必须首先对硬盘进行分区，并且将硬盘分区的类型设置为 `8e` 后，
才能使用 pvcreate 指令将分区初始化为物理卷。
创建卷池 (VG): 新建的物理卷就像一桶矿泉水，把它们加入到一个VG大池子里面，这样池子里的水 (硬件空间)就会变多。卷组Volume group (VG)：将一组物理卷收集为一个管理单元。Group of physical volumes that are used as storage volume (as one disk). They contain logical volumes. Think of volume groups as hard drives.
创建逻辑卷 (LV): 想要划分一块硬盘空间拿来使用，只需要从 VG 里面取一瓢水出来即可，这个划分出来的硬盘空间叫做一个 LV (logical volume)。逻辑卷Logical volume (LV)：虚拟分区，由物理区域（physical extents）组成。A "virtual/logical partition" that resides in a volume group and is composed of physical extents. Think of logical volumes as normal partitions.

物理区域 Physical extent (PE)：硬盘可供指派给逻辑卷的最小单位（通常为4MB）。A small part of a disk (usually 4MB) that can be assigned to a logical Volume. Think of physical extents as parts of disks that can be allocated to any partition.

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