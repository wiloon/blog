---
title: 硬盘扩容, PVE, Archlinux
author: "-"
date: 2025-05-20 09:17:42
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

## PVE ext4 disk resize

[Online Lossless Expansion of EXT4 Partition](https://tech.he-sb.top/posts/online-lossless-expansion-of-ext4-partition/)

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

## lVM on LUKS 分区缩容

https://linux-blog.anracom.com/2018/11/09/shrinking-an-encrypted-partition-with-lvm-on-luks/
https://starbeamrainbowlabs.com/blog/article.php?article=posts%2F441-resize-luks-lvm.html
https://wiki.archlinux.org/title/Resizing_LVM-on-LUKS

```bash
# Step 1: Get an overview over your block devices
lsblk
# Step 2: Open the encrypted partition
sudo cryptsetup open /dev/nvme0n1p3 cr-ext
ls -la /dev/mapper

# Step 3: Get an overview on LVM structure
pvdisplay
vgdisplay
lvdisplay

# Step 4: Check the integrity of the filesystem
fsck /dev/mapper/ubuntu--vg-ubuntu--lv
# Step 5: Check the physical block size of the filesystem and the used space within the filesystem
fdisk -l
# 能看到 /dev/mapper/ubuntu--vg-ubuntu--lv 的 sectors 数量, 每个 sector 512 bytes

## Use tunefs to get some block information:
tune2fs -l /dev/mapper/ubuntu--vg-ubuntu--lv

# Step 6: Plan the reduced volume and filesystem sizes ahead – perform safety and limit considerations

# 因为接下来使用的工具用的单位不一样 有的是 GB, 有的是 GiB, 所以, 假设计划缩容之后 的分区是500G, 那么 在做文件系统缩容的时候,把文件系统缩容到450G是比较安全的
# 500G * 0.9 = 450G

#Step 7: Shrink the filesystem
resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv 450G
e2fsck -f /dev/mapper/vg1-lvroot
# 有可能 会提示 inode 35131705 extent tree (at level 1) could be shorter. optimize<y>?
#这通常不是错误，而是一种结构上的优化建议，可以减少元数据开销，提高效率。

# Step 8: Shrink the logical volume
lvreduce -L 500G /dev/mapper/ubuntu--vg-ubuntu--lv
resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv

sudo vgs
sudo vgchange -ay
sudo e2fsck -f /dev/ubuntu-vg/root
# 缩小 EXT4 文件系统
# 尝试将文件系统的大小调整为 500GB
sudo resize2fs /dev/ubuntu-vg/root 500G
sudo lvreduce -L 500G /dev/ubuntu-vg/root
# 或者
# -r 自动同时调整（resize）文件系统大小
# -L 把逻辑卷大小调整为 500GB
sudo lvreduce -r -L 500G /dev/ubuntu-vg/root
# 查看物理卷
sudo pvs
sudo pvresize --setphysicalvolumesize 505G /dev/mapper/cryptroot
sudo vgchange -an
sudo cryptsetup close cryptroot

# 修改分区表
sudo parted /dev/nvme0n1
print
resizepart 3 510GB
quit
```