---
title: parted
author: "-"
date: 2015-10-22T09:55:38+00:00
url: parted
categories:
  - inbox
tags:
  - reprint
---
## parted
```bash
# 查看磁盘信息
lsblk

# list disk and partitions
# -l, --list
sudo parted -l

# -a 分区对齐, 对齐类型
# -a, --align
sudo parted -a optimal /dev/sdx

# 查看磁盘分区
(parted) p
# set disk label
(parted) mklabel gpt
#or mklabel msdos

# 设置 单位为 s, MiB, GiB, MB,GB
unit mib

# 查看parted 命令帮助
help mkpart
# mkpart part-type fs-type start end
# fs-type 是文件系统类型,支持的类型列表可以通过 help mkpart 查看。 
# mkpart 并不会实际创建文件系统, fs-type 参数仅是让 parted 设置一个 1-byte 编码,让启动管理器可以提前知道分区中有什么格式的数据。

# 按比例分区, 可以不设置 unit xxx

mkpart 磁盘分区名称 起始磁柱值 截止磁柱值

# fs-type: ext4,fat32
mkpart primary ext4 0% 100%

# 指定分区名和起止位置,起点会自动设置成2048s
mkpart data 0% 100%

# 创建efi分区建议550M, linux的efi分区用fat32,系统分区不能用fat,fat会有各种问题,比如不允许使用冒号作文件名
(parted) mkpart primary fat32 1 551

# 设置efi分区标记
(parted) set 1 esp on

# 设置常规bios引导, esp is an alias for boot on GPT
(parted) set 1 boot on
# grub引导
(parted) set 1 bios_grub on


# 给分区取个名字, msdos disk label do not support partition names.
name 1 boot

# 创建swap分区 16G+
mkpart primary 551 17536
name 2 swap

mkpart primary 17536 -1
name 3 rootfs

#检查是否分区对齐
align-check optimal 1

# 退出parted
(parted) q

# 查看磁盘信息
lsblk

# format partition, 格式化分区,把x替换成实际分区
# if mkfs.msdos command not found, pacman -S dosfstools
# 格式化efi分区
sudo mkfs.msdos -F 32 /dev/sdx1
#mkfs.vfat /dev/sdx1

sudo mkfs.ntfs /dev/sddx
# mkfs.ntfs command not found, sudo pacman -S ntfsprogs

# mkswap
sudo mkswap /dev/sdx2
swapon /dev/sdx2

# 格式化
sudo mkfs.ext4 /dev/sdx3
sudo mkfs -t ext4 /dev/vdb1
sudo mkfs.btrfs -L data0 /dev/sdx3

# 查看磁盘分区UUID, 没有root权限时, blkid没有输出, 要加sudo.
# sudo blkid

#genfstab -p -U /mnt > /mnt/etc/fstab
```

>https://www.gnu.org/software/parted/manual/html_chapter/parted_2.html
>https://www.gnu.org/software/parted/manual/html_node/mklabel.html
>https://linux.cn/article-3167-1.html


### parted分区NTFS文件系统

```bash
sudo pacman -S ntfs-3g
# 不安装ntfs-3g 会提示 mkfs.ntfs: command not found
```

parted /dev/sdb                                      
1
分区表选择gpt，文件系统选ntfs，起始点和结束点分别为0%和100%，你也可以按照需要的磁盘量来选择。

(parted) mklabel gpt
(parted) mkpart 
分区名称？  []? LyData2
文件系统类型？  [ext2]? ntfs                                              
起始点？ 0%                                                               
结束点？ 100%                                                             
(parted) print
Model: ATA TOSHIBA MG04ACA4 (scsi)
磁盘 /dev/sdb: 4001GB
Sector size (logical/physical): 512B/512B
分区表：gpt
Disk Flags: 

数字  开始：  End     大小    文件系统  Name     标志
 1    1049kB  4001GB  4001GB  ntfs      LyData2

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
然后就可以退出了

(parted) quit
信息: You may need to update /etc/fstab.
1
2
磁盘格式化
然后就要对这块磁盘进行格式化

ls /dev/sd*
/dev/sda  /dev/sda1  /dev/sdb  /dev/sdb1  /dev/sdc
1
2
可以看到多了一个/dev/sdb1，就是刚才分好区的那块硬盘。

mkfs.ntfs -f /dev/sdb1 
————————————————
版权声明：本文为CSDN博主「Litedg」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/Litedg/article/details/111504305
