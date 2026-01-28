---
title: 硬盘扩容, PVE, Archlinux
author: "-"
date: 2025-09-13 15:33:33
url: disk/resize
categories:
  - OS
tags:
  - Reprint
  - Remix
  - Disk
  - PVE
---
## 硬盘扩容

## pve ext4 根分区磁盘扩容

虚拟机关机

在 pve 里给硬盘扩容: vm>hardware> Hard Disk> Disk Action> resize: 填写新增的容量

挂载 archlinux iso, 修改引导顺序, 让虚拟机从 iso 启动

启动虚拟机

```bash
lsblk

# 看到磁盘总大小增加了，但分区大小没变。
fdisk -l
# 调整分区表, 扩容, 用 fdisk 调整分区表一般不会丢数据，但是最好备份一下。
fdisk /dev/sda
# 如果不是从 iso 引导,直接在操作系统里执行, 会提示 This disk is currently in use - repartitioning is probably a bad idea. It's recommended to umount all file systems, nd swapoff all swap partitions on this disk.

# print the partition table
Command (m for help): p

Disk /dev/sda: 20 GiB, 21474836480 bytes, 41943040 sectors
Disk model: QEMU HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x1bc64ef0

Device     Boot   Start      End  Sectors Size Id Type
/dev/sda1  *       6144  2103295  2097152   1G  b W95 FAT32
/dev/sda2       2103296 20971519 18868224   9G 83 Linux

# delete partition 2
Command (m for help): d
Partition number (1,2, default 2): 2

Partition 2 has been deleted.

Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)

# 输入 p
Select (default p): p

# 使用默认值 2
Partition number (2-4, default 2): 

# 输入分区的起始扇区, 要和删除的分区起始扇区一样
First sector (2048-41943039, default 2048): 2103296

# 输入分区的结束扇区, 使用默认值, 即使用所有剩余空间
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2103296-41943039, default 41943039): 

Created a new partition 2 of type 'Linux' and of size 19 GiB.
Partition #2 contains a ext4 signature.

# 输入 y 确认删除 ext4 签名
Do you want to remove the signature? [Y]es/[N]o: Y

The signature will be removed by a write command.

# 再次打印分区表， 应该能看到分区 2 已经变大了
Command (m for help): p
Disk /dev/sda: 20 GiB, 21474836480 bytes, 41943040 sectors
Disk model: QEMU HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x1bc64ef0

Device     Boot   Start      End  Sectors Size Id Type
/dev/sda1  *       6144  2103295  2097152   1G  b W95 FAT32
/dev/sda2       2103296 41943039 39839744  19G 83 Linux

Filesystem/RAID signature on partition 2 will be wiped.

# 输入命令 w 保存分区表
Command (m for help): w
The partition table has been altered.
Syncing disks.

# ------
e2fsck -f /dev/sda2

# 有可能会询问是否优化，输入 y， 后面可能会有很多类似的提示，全部输入 y 即可， 还有可能提示输入 a: 确认全部
root@archiso ~ # e2fsck -f /dev/sda2
e2fsck 1.47.3 (8-Jul-2025)
ext2fs_open2: Bad magic number in super-block
e2fsck: Superblock invalid, trying backup blocks...
Pass 1: Checking inodes, blocks, and sizes

Inode 287507 extent tree (at level 1) could be narrower.  Optimize<y>? 

# resize the filesystem
resize2fs /dev/sda2

# 分区扩容完成，重启虚拟机
```

------

## PVE ext4 disk resize

[Online Lossless Expansion of EXT4 Partition](https://tech.he-sb.top/posts/online-lossless-expansion-of-ext4-partition/)

vm>hardware> Hard Disk> Disk Action> resize: 填写新增的容量

### 查看分区表类型

```bash
parted -l
```

回显有可能是以下其中一种

```bash
Partition Table: msdos
Partition Table: gpt
Partition Table: loop
```

msdos: MBR
gpt: GPT
loop: loop 设备（虚拟磁盘）

### 查看磁盘的分区信息

```bash
lsblk

# 回显
# sda2 挂载到了根目录 /
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda      8:0    0   13G  0 disk 
├─sda1   8:1    0  200M  0 part /boot
└─sda2   8:2    0  7.8G  0 part /
```

### 停掉写磁盘的服务

```bash
systemctl stop service0
```

### 非根分区扩容, 建议先卸载磁盘分区

```bash
umount /dev/sda2
```

#### 确认磁盘分区的卸载结果

```bash
lsblk

# 回显
# vdb 没有挂载
vdb    253:16   0  200G  0 disk
```

### 进入 parted

根分区卸载不掉, 直接进入 parted

```bash
# 进入 parted 分区工具, 参数要传整个硬盘(sda), 不要传某一个分区(sda2)
parted /dev/sda

# 输入"p" 然后回车，查看当前磁盘分区情况。
(parted) p

# 如果提示需要修复，执行Fix
Fix

# 扩容, 使用所有剩余空间
(parted) resizepart 2 100%

# 查看分区
(parted)  p

# 退出 parted
(parted)  q
```

### 检查磁盘分区文件系统的正确性, 文件系统扩容

```bash
# 执行以下命令，检查磁盘分区文件系统的正确性, 如果是要分区分显示正在使用, 检查不了
e2fsck -f /dev/sda2

#  其它分区如果回显 /dev/vdb is in use, 停掉读写硬盘的服务重试

# 执行以下命令，扩展磁盘分区文件系统的大小。
resize2fs /dev/sda2

# 查看分区容量
df -TH
```

## PVE archlinux xfs disk resize

1. 虚拟机关机
2. 在 PVE 控制台给虚拟机磁盘扩容：Hardware> Hard Disk> Disk Action> resize: 填写新增的容量
3. 启动虚拟机
4. SSH 登录之后 `sudo fdisk -l` 看到磁盘容量已经增加了，但是 `df -h` 容量没变
5. 执行以下命令

```bash
# cloud-guest-utils 提供了 growpart 命令
pacman -S cloud-guest-utils
growpart /dev/sda 2
xfs_growfs /dev/sda2
# 然后 df -h 应该能看到正确的磁盘容量了。
```

## KVM 虚拟磁盘扩容, qemu-img resize

### kvm 虚拟磁盘扩容

磁盘扩容分为 raw 和 qcow2 两种扩容方式, 命令相同, 区别是后缀名

```bash
# 查看磁盘信息
qemu-img info /data/daixuan1.qcow2
# 加 5G
qemu-img resize /data/daixuan1.qcow2 +5G
```

### windows 虚拟机需要用分区工具再调整一下

在 This PC 上点右键> 选择Manage>Storage>Disk Management>右键点击分区》选择extend volume

[http://blog.51cto.com/daixuan/1743047](http://blog.51cto.com/daixuan/1743047)

fdisk -l 列出系统中所有的磁盘设备和分区表,这里磁盘设备容量已经增加5G

[root@localhost ~]# fdisk -l

Disk /dev/vda: 16.1 GB, 16106127360 bytes

但是磁盘挂载的空间并没有增加,依然是8.3G

[root@localhost ~]# df -h //查看可用磁盘总容量和使用容量

Filesystem Size Used Avail Use% Mounted on

/dev/mapper/VolGroup-lv_root 8.3G 685M 7.2G 9% /

tmpfs 246M 0 246M 0% /dev/shm

/dev/vda1 477M 33M 419M 8% /boot

 (1) 因为新增加的空间还没有划分使用,所以要继续分区:

[root@localhost ~]# fdisk /dev/vda

WARNING: DOS-compatible mode is deprecated. It's strongly recommended to

switch off the mode (command 'c') and change display units to

sectors (command 'u').

Command (m for help): p

Disk /dev/vda: 16.1 GB, 16106127360 bytes

16 heads, 63 sectors/track, 31207 cylinders

Units = cylinders of 1008 * 512 = 516096 bytes

Sector size (logical/physical): 512 bytes / 512 bytes

I/O size (minimum/optimal): 512 bytes / 512 bytes

Disk identifier: 0x000dca27

Device Boot Start End Blocks Id System

/dev/vda1 * 3 1018 512000 83 Linux

Partition 1 does not end on cylinder boundary.

/dev/vda2 1018 20806 9972736 8e Linux LVM

Partition 2 does not end on cylinder boundary.

Command (m for help): n

Command action

e extended

p primary partition (1-4)

p

Partition number (1-4): 3

First cylinder (1-31207, default 1): 20807

Last cylinder, +cylinders or +size{K,M,G} (20807-31207, default 31207): 31207

Command (m for help): p

Disk /dev/vda: 16.1 GB, 16106127360 bytes

16 heads, 63 sectors/track, 31207 cylinders

Units = cylinders of 1008 * 512 = 516096 bytes

Sector size (logical/physical): 512 bytes / 512 bytes

I/O size (minimum/optimal): 512 bytes / 512 bytes

Disk identifier: 0x000dca27

Device Boot Start End Blocks Id System

/dev/vda1 * 3 1018 512000 83 Linux

Partition 1 does not end on cylinder boundary.

/dev/vda2 1018 20806 9972736 8e Linux LVM

Partition 2 does not end on cylinder boundary.

/dev/vda3 20807 31207 5242104 83 Linux

Command (m for help): w

The partition table has been altered!

Calling ioctl() to re-read partition table.

WARNING: Re-reading the partition table failed with error 16: Device or resource busy.

The kernel still uses the old table. The new table will be used at

the next reboot or after you run partprobe(8) or kpartx(8)

Syncing disks.

 (2) 然后再把这个/dev/vda3 加入到lvm里面去:

[root@localhost ~]# ls /dev/vda3 //如果没有这个分区,需要重启一下

[root@localhost ~]# reboot

```Bash
#创建物理卷
pvcreate /dev/vda3 
```

Physical volume "/dev/vda3" successfully created

[root@localhost ~]# pvs //查看卷

PV VG Fmt Attr PSize PFree

/dev/vda2 VolGroup lvm2 a- 9.51g 0

/dev/vda3 lvm2 - 5.00g 5.00g

[root@localhost ~]# vgextend VolGroup /dev/vda3 //VolGroup虚拟卷扩展,vda3加入到Vol

Volume group "VolGroup" successfully extended

[root@localhost ~]# pvs

PV VG Fmt Attr PSize PFree

/dev/vda2 VolGroup lvm2 a- 9.51g 0

/dev/vda3 VolGroup lvm2 a- 5.00g 0

```Bash
# //VFree中5G
vgs 
```

VG #PV #LV #SN Attr VSize VFree

VolGroup 2 2 0 wz-n- 14.50g 5.00g

如何把5G加入到lv_root中？

[root@localhost ~]# lvs //查看逻辑卷

LV VG Attr LSize Pool Origin Data% Meta% Move Log Cpy%Sync Convert

lv_root VolGroup -wi-ao-- 8.54g

lv_swap VolGroup -wi-ao-- 992.00m

[root@localhost ~]# lvextend -l +100%FREE /dev/VolGroup/lv_root //扩展卷

Size of logical volume VolGroup/lv_root changed from 8.54 GiB (2186 extents) to 13.54 GiB (3465 extents).

Logical volume lv_root successfully resized

[root@localhost ~]# df -h

Filesystem Size Used Avail Use% Mounted on

/dev/mapper/VolGroup-lv_root 8.3G 685M 7.2G 9% /

tmpfs 246M 0 246M 0% /dev/shm

/dev/vda1 477M 33M 419M 8% /boot

[root@localhost ~]# resize2fs /dev/VolGroup/lv_root

resize2fs 1.41.12 (17-May-2010)

Filesystem at /dev/VolGroup/lv_root is mounted on /; on-line resizing required

old desc_blocks = 1, new_desc_blocks = 1

Performing an on-line resize of /dev/VolGroup/lv_root to 3548160 (4k) blocks.

The filesystem on /dev/VolGroup/lv_root is now 3548160 blocks long.

[root@localhost ~]# df -h

Filesystem Size Used Avail Use% Mounted on

/dev/mapper/VolGroup-lv_root 14G 687M 12G 6% /

tmpfs 246M 0 246M 0% /dev/shm

/dev/vda1 477M 33M 419M 8% /boot

如果提示 This image format does not support resize, 检查一下你qemu-img create的时候,是否有加 preallocation=metadata 选项,如果有,就不能resize了。

 (3) 另外,如果是增加磁盘,思路是
  
创建磁盘:  qemu-img create -f qcow2 /data/daixuan1_2.qcow2 5G
  
关闭虚拟机:  virsh destroy daixuan1
  
编辑配置文件:  virsh edit daixuan1

复制增加如下: 注意是vdb,qcow2

```xml
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2' cache='none'/><source file='/data/daixuan1_2.qcow2'/><target dev='vdb' bus='virtio'/>
</disk>
```
  
开启虚拟机: virsh start daixuan1
  
进入虚拟机: virsh console daixuan1
  
分区:  fdisk /dev/vdb
  
格式化: mkfs.ext4 /dev/vdb

挂载: vim /etc/fstab, 添加一行: /dev/vdb /mnt ext4 defaults 0 0

mount -a 然后mnt就可以使用了

[root@localhost ~]# cd /mnt

[root@localhost mnt]# touch 23.txt

当然也可以按照上面的思路把 /dev/vdb 加入到 lvm里面去,测试成功,这里省略步骤

注:  raw格式
  
步骤基本上和qcow2一样。如果提示 This image format does not support resize, 检查一下你qemu-img create的时候,是否有加 preallocation=metadata 选项,如果有,就不能resize了。

## 华为云磁盘扩容

3 minute - manually

## 华为云帮助文档

[https://support.huaweicloud.com/usermanual-evs/evs_01_0109.html#evs_01_0109__section13346184710300](https://support.huaweicloud.com/usermanual-evs/evs_01_0109.html#evs_01_0109__section13346184710300)

### 查看分区表类型

```bash
parted -l
```

回显有可能是

```r
Partition Table: msdos
Partition Table: gpt
Partition Table: loop
```

msdos 对应华为云帮助中的 MBR.
gpt 对应华为云帮助中的 GPT.

### 查看磁盘的分区信息

```bash
lsblk

# 回显
# vdb 挂载到了 /foo
vdb    253:16   0  200G  0 disk /foo
```

### 停掉写磁盘的服务

```bash
systemctl stop service0
```

### 卸载磁盘分区

```bash
umount /dev/vdb1
```

如果提示:  umount: /foo: target is busy， 考虑强制卸载，参照后面的 ### 强制卸载

### 强制卸载

用 fuser 查看使用 /data 目录的进程

```bash
fuser -m /foo

# 杀掉进程, 或强制卸载
kill -9 xxxx
umount -l /foo
```

### 确认磁盘分区的卸载结果

```bash
lsblk

# 回显
# vdb 没有挂载
vdb    253:16   0  200G  0 disk
```

### 如果第 1 步查到的分区表类型是 gpt, 执行No.7，如果分区表类型是 loop 可以跳到 No.8

进入 parted 分区工具。

```bash
parted /dev/vdb
# 输入"unit s"，按"Enter"，设置磁盘的计量单位为磁柱。
(parted) unit s

# 输入"p"，按"Enter"，查看当前磁盘分区情况。
(parted) p

# 如果提示需要修复，执行Fix
Fix
# 记录待扩大分区 "/dev/vdb2" 的初始磁柱值 (start) 和截止磁柱值 (End) 
Number  Start  End         Size        File system  Flags
 1      0s     419430399s  419430400s  ext4

# 输入"rm"和分区编号，此处以"1"为例，按"Enter"。
(parted)  rm 1

# 重新划分分区，执行以下命令，按"Enter", xxxs 为上一步记录的初始磁柱值。
(parted)  mkpart ext4 xxxs 100%

# 查看分区
(parted)  p

# 退出parted
(parted)  q
```

### 退出 parted 后用lsblk再次检查挂载状态

```bash
lsblk
```

### 退出 parted 后分区有可能被自动挂载，再 umount 一次

```bash
umount /dev/vdb1
```

### 检查磁盘分区文件系统的正确性, 磁盘扩容

```bash
# 执行以下命令，检查磁盘分区文件系统的正确性,
e2fsck -f /dev/vdb1

#  如果回显 /dev/vdb is in use , vim /etc/fstab, 注释掉/data 的挂载, 重启

# 执行以下命令，扩展磁盘分区文件系统的大小。
resize2fs /dev/vdb1

# 挂载磁盘到目录 
mount /dev/vdb1 /data

# 查看分区容量
df -TH

```

### 启动写磁盘的服务

```bash
systemctl start service0
# 检查服务状态
systemctl status service0
```

### 系统盘扩容

```bash
growpart /dev/vda 1;resize2fs /dev/vda1
```

[https://support.huaweicloud.com/usermanual-evs/zh-cn_topic_0044524728.html#zh-cn_topic_0044524728__section31113372194023](https://support.huaweicloud.com/usermanual-evs/zh-cn_topic_0044524728.html#zh-cn_topic_0044524728__section31113372194023)
