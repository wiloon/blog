---
title: 加密分区缩容, LVM on LUKS
author: "-"
date: 2025-05-20 21:43:13
url: shrink-lvm-on-luks
categories:
  - Linux
tags:
  - reprint
  - remix
---
## 加密分区缩容, LVM on LUKS

https://linux-blog.anracom.com/2018/11/09/shrinking-an-encrypted-partition-with-lvm-on-luks/

https://wiki.archlinux.org/title/Resizing_LVM-on-LUKS

https://wiki.archlinux.org/title/LVM#Resizing_the_logical_volume_and_file_system_in_one_go

https://starbeamrainbowlabs.com/blog/article.php?article=posts%2F441-resize-luks-lvm.html

Step 1: Get an overview over your block devices

```bash
lsblk
```

加密分区在 /dev/nvme0n1p3 上

Step 2: Open the encrypted partition

```bash
cryptsetup open /dev/nvme0n1p3 cr-ext
# 打开过程中会要求输入密码

# 检查一下设备映射
ls -la /dev/mapper
```

能看到 PV: /dev/mapper/cr-ext
还有 LVM-volumes: /dev/mapper/ubuntu--vg-ubuntu--lv

Step 3: Get an overview on LVM structure

```bash
pvdisplay
vgdisplay
lvdisplay
```

```bash
# 查看 lv 是否激活
lvs -o lv_name,lv_attr
```

输出

```bash
# 第五位 a 表示 LV 是 active（已激活）
LV          Attr
ubuntu-lv   -wi-ao----
```

一般情况打开 luks 加密的设备之后 lvm 的 vg, lv 会自动 激活
如果没有激活的话, 手动激活 vg

```bash
# 手动激活 vg
vgchange -ay ubuntu-vg
vgchange -ay ubuntu-vg --verbose
```

Step 4: Check the integrity of the filesystem

```bash
fsck /dev/mapper/ubuntu--vg-ubuntu--lv
# 如果检查结果有问题执行 fsck -f
```

Step 5: Check the physical block size of the filesystem and the used space within the filesystem

```bash
fdisk -l
tune2fs -l /dev/mapper/ubuntu--vg-ubuntu--lv
```

Step 6: Plan the reduced volume and filesystem sizes ahead – perform safety and limit considerations

1000G 缩容到 500G
安全系数 0.9
500*0.9 = 450G
文件系统至少要比逻辑卷小 10%, 因为后面用到的工具使用的单位不一样, 有的是 GB, 有的是 GiB

Step 7: Shrink the filesystem

```bash
# 先执行 fsck, 再执行 resize2fs, 否则会提示先执行 fsck
fsck -f /dev/mapper/ubuntu--vg-ubuntu--lv
resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv 450G
```

Step 8: Shrink the logical volume

```bash
# lvreduce works in GiB
lvreduce -L 500G /dev/mapper/ubuntu--vg-ubuntu--lv
```

Step 9: Extend the fs to the volume size again

```bash
resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```

Step 10: Check for gaps between the volumes of your LVM volume group

ubuntu 24.04 默认不会有 swap 分区, 有个swap 文件 在 /root 分区

Step 11: Resize/reduce the physical LVM

```bash
# pvresize works in GiB
pvresize --setphysicalvolumesize 550G /dev/mapper/cr-ext
pvdisplay
```

Step 12: Set new size of the encrypted region

```bash
cryptsetup status cr-ext
# 1258291200 = 600G*1024*1024*1024/512
cryptsetup -b 1258291200 resize cr-ext
cryptsetup status cr-ext
```

Step 13: Reduce the size of the physical partition – a pretty scary step!

```bash
parted /dev/nvme0n1
(parted) print
(parted) resizepart 
Partition number? 3                                                       
End?  [112GB]? 614GB
(parted) print
(parted) q 
```

Step 14: Set new size of the encrypted region

```bash
cryptsetup resize cr-ext
cryptsetup status cr-ext
```

Step 15: Reset the PV size to the full partition size

```bash
pvresize  /dev/mapper/cr-ext
pvdisplay
vgdisplay
lvdisplay
pvs -v --segments /dev/mapper/cr-ext
```

Step 16: Closing and leaving the encrypted device

```bash
vgchange -an ubuntu-vg
cryptsetup close cr-ext
# ubuntu 24.04, 在执行 vgchange -an 之后, 有某种未知的机制 ubuntu-vg 马上又被激活了
# 所以... 可以这样
# 解除激活之后, 趁系统还没反应过来, 马上 cryptsetup close
vgchange -an ubuntu-vg && cryptsetup close cr-ext
```
