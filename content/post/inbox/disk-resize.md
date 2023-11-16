---
title: 磁盘扩容, PVE, Archlinux
author: "-"
date: 2022-06-21 08:19:27
url: disk/resize
categories:
  - OS
tags:
  - Reprint
  - Disk
  - PVE
  - Archlinux
---
## 磁盘扩容

## PVE ext4

## virtualbox ext4 disk resize

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

磁盘扩容分为 raw和 qcow2 两种扩容方式, 命令相同, 区别是后缀名

```bash
# 查看磁盘信息
qemu-img info /data/daixuan1.qcow2
# 加5G
qemu-img resize /data/daixuan1.qcow2 +5G
```

### windows 虚拟机需要用分区工具再调整一下

在 This PC 上点右键》选择Manage>Storage>Disk Management>右键点击分区》选择extend volume

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

[root@localhost ~]# pvcreate /dev/vda3 //创建物理卷

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

[root@localhost ~]# vgs //VFree中5G

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
