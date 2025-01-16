---
title: dual boot windows and ubuntu
author: "-"
date: 2024-05-19T22:31:55+08:00
url: dual-boot
categories:
  - System
tags:
  - reprint
  - remix
---
## dual boot windows and ubuntu

https://askubuntu.com/questions/1506694/dual-boot-with-windows-11-and-bitlocker/1514161#1514161

Ubuntu 版本: 22.04

用 clonezill 备份硬盘

- 在硬盘上准备一块空闲的空间, 用 windows 的磁盘管理工具调整现有的分区

## 用 `balenaEtcher` 制作 ubuntu 安装盘 (U盘)

- 在 BIOS 里确认 Secure Boot 已经开启
- 用分区工具在 U 盘或移动硬盘上准备一个大于 100MB 的 FAT32 分区
- 从 U 盘引导, 安装 ubuntu, 选择 Try or install Ubuntu
  - Select Language: English
  - Install> Install Ubuntu
  - Keyboard: English(US)> English(US)
  - Wireless
  - What apps would you like to install to start with: Minimal installation
  - 勾选 Install third-party software for graphics and wi-fi hardware and additional media formats
  - 勾选 Configure Secure Boot, 设置 Secure boot 密码

## 备份 windows 的 EFI 分区 到 U 盘 (/dev/sda2)

open a terminal with ctrl+alt+t
- 切换到 root 用户: sudo -i
- `lsblk` to list all devices
- 挂载 FAT32 分区
    - `mkdir /mnt/persistent`
    - `mount /dev/sda2 /mnt/persistent`
    - `mkdir /mnt/persistent/efi-backup`
- Mount the Windows bootloader partition
  - `mkdir /mnt/efi`
  - `mount /dev/nvme0n1p1 /mnt/efi`
- Backup all the data on it, and make sure to correctly execute rsync as shown here (with trailing slashes):
  `rsync -av /mnt/efi/ /mnt/persistent/efi-backup/`
- Now we delete the content on the efi partition (don't be scared, we will copy it back later)
  `rm -rf /mnt/efi/*`
- Umount again the efi partition
  `umount /mnt/efi`
  `umount /mnt/persistent`

## 安装 Ubuntu

因为 Ubuntu 的安装程序如果选加密 (LUKS) 安装的话, 只能把 window 删掉. 所以我们的第一次安装硬盘是没有加密的, 
安装好之后再把 /root 分区的文件, 复制到加密的分区.

- 回到 Ubuntu 的图形化安装环境, 选择 something else, click continue
- 选择 free space, 一般在 /dev/nvme0n1p3 和 /dev/nvme0n1p4 之间
- 点击加号创建分区
  - 创建一个 512 MB 的分区 (/dev/nvme0n1p5), ubuntu 的 EFI 分区
    - Use as: EFI System Partition
  - 创建一个 2048MB 的分区 (/dev/nvme0n1p6), Ubuntu 的 /boot 分区
    - Use as: Ext4 journaling file system
    - Mount point: `/boot`
  - 创建一个 12000MB 的的分区  (/dev/nvme0n1p7), Ubuntu 的 /root 分区
    - Use as: Ext4 journaling file system
    - mount point: `/`
    - 之后会删掉, 这个分区不需要太大
- Device for bootloader installation: 选择新的 EFI 分区: /dev/nvme0n1p5, 点击 Install Now
    - 这里选择了 /dev/nvme0n1p5 但是 Ubuntu 还是会安装到 /dev/nvme0n1p1, (Ubuntu installer 的 bug, 这就是前面备份 windows EFI 分区的原因)安装完成之后再把备份的 windows boot loader 恢复回来
- 选择时区
- Who are you
    - Your name: xxx
    - Your computer's name: xxx
    - Pick a username: xxx
    - Choose a password: xxx
    - Confirm your password: xxx
    - 安装结束之后不要点击 Restart Now, 点击右上角的 `X` 关闭窗口, 系统会回到 Ubuntu live usb 的桌面

## 把 Ubuntu 的 EFI 分区复制到 /dev/nvme0n1p5

open a terminal with ctrl+alt+t, 切换到 root 用户: sudo -i
把 ubuntu installer 刚才安装的 /dev/nvme0n1p1 复制到 /dev/nvme0n1p5

```Bash
mount /dev/nvme0n1p1 /mnt/efi
mkdir /mnt/new-efi
mount /dev/nvme0n1p5 /mnt/new-efi
# with trailing slashes
rsync -av /mnt/efi/ /mnt/new-efi/ 
```

把之前备份的 windows boot loader 恢复到 /dev/nvme0n1p1

```Bash
mount /dev/sda2 /mnt/persistent
rm -rf /mnt/efi/*

# with trailing slashes
rsync -av /mnt/persistent/efi-backup/ /mnt/efi/
```

umount

```Bash
umount /mnt/efi
umount /mnt/new-efi
umount /mnt/persistent
```

## 把 Ubuntu 复制到加密分区 LVM on LUKS

在 terminal 运行 gparted 创建新分区 (/dev/nvme0n1p8)

- 选中 /dev/nvme0n1p7 后面的 unallocated 空间
- 创建分区
  - File system: cleared
  - click Add
- Apply All Operations

- 关掉 gparted, 回到 root terminal

## 加密分区 /dev/nvme0n1p8

LVM on LUKS, 管理起来更简单, 可以用一个密码解密所有的分区, 可以加密 swap 分区

```Bash
# Use the cryptsetup luksFormat command to set up the partition for encryption.
# are you sure: YES (一定要输入大写的 YES)
# 初始化/格式化一个加密分区
# /dev/nvme0n1p8 是前面创建的一个硬盘分区
cryptsetup luksFormat /dev/nvme0n1p8
# 打开一个 LUKS 设备, nvme0n1p8_crypt: 这是解密后设备在 /dev/mapper/ 目录下的名称。通过这个名称，可以访问解密后的分区。
# 打开之后会映射到 /dev/mapper/nvme0n1p8_crypt
cryptsetup open /dev/nvme0n1p8 nvme0n1p8_crypt
# 创建物理卷 (Physical Volume) PV, 在加密分区上 nvme0n1p8_crypt 创建 PV
# 直接在 LUKS 加密的分区上创建一个物理卷
pvcreate /dev/mapper/nvme0n1p8_crypt
# 创建卷组, volume group (VG), 卷组的名字: vgubuntu,  /dev/mapper/nvme0n1p8_crypt: 作为物理卷 (Physical Volume) 加入卷组的设备路径。
# 创建卷组, 卷组里只有一个物理卷
vgcreate vgubuntu /dev/mapper/nvme0n1p8_crypt
# 查看 卷组 信息
vgs -a # Check the available size and decide how big your partitions should be
# 在卷组上创建第一个逻辑卷, 作为 ubuntu 的 swap 分区
# 创建 LVM 逻辑卷 (分区)
# swap 分区
lvcreate --name swap_1 -L 16G vgubuntu
# 创建交换空间 (swap space)
mkswap /dev/vgubuntu/swap_1
# 在卷组上创建第二个逻辑卷, 作为 ubuntu 的 root 分区
# 创建逻辑卷, root 分区, 创建好之后会被映射到 /dev/vgubuntu/root
lvcreate --name root -L 67g vgubuntu
# 创建 ext4 文件系统
mkfs.ext4 /dev/vgubuntu/root
```

## 把之前安装的未加密的 Ubuntu 拷到新的加密分区

```Bash
mkdir /mnt/root-orig
mkdir /mnt/root-new

# /dev/nvme0n1p7, 在上一步安装的未加密的 ubuntu 的 /root 分区
mount /dev/nvme0n1p7 /mnt/root-orig/
# LUKS 加密的 root 分区 /dev/vgubuntu/root
mount /dev/vgubuntu/root /mnt/root-new/
# 复制分区数据
rsync -avhPAXHx --numeric-ids /mnt/root-orig/ /mnt/root-new/
umount /mnt/root-orig
umount /mnt/root-new
# 停用卷组/volume group: vgubuntu
# 停用卷组：-an 选项用于停用指定的卷组，这意味着该卷组及其逻辑卷将不可用。
vgchange -an vgubuntu
# 关闭 LUKS 分区
# 关闭之后 分区上创建的 LVM 分区都是不可见的了.
# 再打开的话得输入 密码
cryptsetup luksClose nvme0n1p8_crypt
# 准备删除分区和扩分区
```

## 删除旧的未加密的 ubuntu, 扩展加密分区

https://wiki.archlinux.org/title/Resizing_LVM-on-LUKS

open gparted, 在 gparted 里删除未加密的 ubuntu 分区, /dev/nvme0n1p7

```Bash
# resize /dev/nvme0n1p8 to use free space
# 重新打开 LUKS 设备: /dev/nvme0n1p8, 因为前面删分区 nvme0n1p7 之前 把 nvme0n1p8 关了, 这里重新打开加密的分区
cryptsetup open /dev/nvme0n1p8 nvme0n1p8_crypt
# 停用加密分区上的 LVM VG
# 停用 volume group: vgubuntu, todo: 为啥 需要停用呢, 有可能 上面一句会默认激活卷组?  下次用这个查看一下卷组状态 sudo vgdisplay vgubuntu
vgchange -an vgubuntu
# todo, cryptsetup resize 怎么知道是向前扩展还是向后扩展?
# 先扩展 LUKS 加密分区
cryptsetup resize nvme0n1p8_crypt
# 再扩展 加密分区上的 LVM 物理卷/PV
pvresize /dev/mapper/nvme0n1p8_crypt
# 激活卷组
vgchange -ay vgubuntu
# pvchange 命令用于更改物理卷（Physical Volume, PV）的属性。
# 修改物理卷的可扩展性：-x y 选项用于设置物理卷为可扩展（extendable）。这意味着可以在该物理卷上创建新的逻辑卷，或者扩展现有的逻辑卷。
# -x y：将物理卷设置为可扩展。即可以在该物理卷上创建新的逻辑卷或扩展现有的逻辑卷。
# -x n：将物理卷设置为不可扩展。即禁止在该物理卷上创建新的逻辑卷或扩展现有的逻辑卷。
pvchange -x y /dev/mapper/nvme0n1p8_crypt
# lvresize 命令用于调整逻辑卷（Logical Volume, LV）的大小。在 LVM（逻辑卷管理器）中，可以增加或减少逻辑卷的空间。
lvresize -L +11G vgubuntu/root
# 将物理卷设置为不可扩展。
pvchange -x n /dev/mapper/nvme0n1p8_crypt
# e2fsck 命令可以帮助确保文件系统的一致性，特别是在调整文件系统大小之前。
e2fsck -f /dev/mapper/vgubuntu-root
# resize2fs 命令用于调整 ext2/ext3/ext4 文件系统的大小
# 这个命令会自动调整文件系统的大小，使其占满整个逻辑卷（如果是扩展）或减少到逻辑卷的当前大小（如果是缩小）。
# p 选项用于在调整过程中显示进度，
resize2fs -p /dev/mapper/vgubuntu-root
```

## chroot to configure new installation

```Bash
mount /dev/vgubuntu/root /mnt/root-new/
mount /dev/nvme0n1p6 /mnt/root-new/boot/
mount /dev/nvme0n1p5 /mnt/root-new/boot/efi/
mount --bind /dev /mnt/root-new/dev/
mount --bind /proc /mnt/root-new/proc/
mount --bind /sys /mnt/root-new/sys/
mount --bind /run /mnt/root-new/run/
chroot /mnt/root-new/ /bin/bash
apt update
apt install lvm2 cryptsetup vim
blkid /dev/nvme0n1p8 # Copy the UUID
# /etc/crypttab 文件用于在 Linux 系统上管理加密设备的设置，特别是在系统启动时自动解密和挂载这些设备。它与 cryptsetup 工具一起使用，通常用于配置 LUKS（Linux Unified Key Setup）加密卷。这个文件的作用类似于 /etc/fstab，但专门用于加密设备。
vim /etc/crypttab
```

And now put in a new entry with your copied UUID

```Bash
# the content of /etc/crypttab
nvme0n1p8_crypt UUID=UUID none luks,discard
```

```Bash
blkid /dev/nvme0n1p5 # Get UUID of EFI
vim /etc/fstab
```

```Bash
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/... during installation
/dev/mapper/vgubuntu-root                 /               ext4    errors=remount-ro 0       1
# /boot was on /dev/nvme0n1p6 during installation
UUID=fd1eecf5-18b0-42fb-a3d4-5239c1465fc1 /boot           ext4    defaults        0       2
# /boot/efi was on /dev/nvme0n1p5 during installation
UUID=EF18-AD8F                            /boot/efi       vfat    umask=0077      0       1
/dev/mapper/vgubuntu-swap_1               none    swap    sw  0   0
```

Now apply update

```Bash
# 更新 initramfs：-u 选项表示更新现有的 initramfs 映像，而不是创建新的映像。
# 适用于所有内核版本：-k all 指定更新所有已安装内核版本的 initramfs 映像。
update-initramfs -u -k all
```

And lets also update grub
We will also make it detect Windows
vim /etc/default/grub

And add
GRUB_DISABLE_OS_PROBER=false
Now update
update-grub

And lets exit the chroot
exit

umount /mnt/root-new/dev/
umount /mnt/root-new/proc/
umount /mnt/root-new/sys
umount /mnt/root-new/run
umount /mnt/root-new/boot/efi
umount /mnt/root-new/boot
umount /mnt/root-new

UEFI boot order
As a last step we will check the boot order and create a new entry for our new EFI partition
# Check all entries
efibootmgr -v
# Locate the old Ubuntu entry, which was created for wrong EFI partiiton and delete it
efibootmgr -b 0001 -B
# Create new one for correct partition, here nvme0n1p5
efibootmgr --create --disk /dev/nvme0n1 --part 5 --label "Ubuntu" --loader /EFI/ubuntu/shimx64.efi
# Check if all fine
efibootmgr -v

- /dev/nvme0n1
  - /dev/nvme0n1p1: 100MB, window bootloader EFI
  - /dev/nvme0n1p2: 16MB, unknown, created by windows
  - /dev/nvme0n1p3: 378G, windows data NTFS (bitlocker)
  - /dev/nvme0n1p4: 890MB, windows recovery
  - /dev/nvme0n1p5: 487MB, ubuntu boot loader EFI
  - /dev/nvme0n1p6: 1.9G, ubuntu /boot
  - /dev/nvme0n1p7: 11.2G, ubuntu /root (original) (delete)
  - /dev/nvme0n1p8: 84.1G, ubuntu (LVM PV + LUKS)
    - nvme0n1p8_crypt
    - vgubuntu-swap_1 16G ubuntu swap
    - vgubuntu-root 67G ubuntu /root

- 获取和保存 BitLocker recovery key: https://account.microsoft.com/devices/recoverykey
- shrink your BitLocker encrypted partition
- create an Ubuntu live USB stick
- BACKUP device to image via Clonezilla https://blog.csdn.net/dqz1231/article/details/127947178
- create an Ubuntu live USB stick
- Create another partition in the free space of the USB stick at the end as FAT32
- 检查 secure boot 是否已经开启
- backup EFI partition

## create an Ubuntu live USB stick

- partition schema: GPT


## balenaEtcher

https://etcher.balena.io/#download-etcher

1. flash from file
2. select target
3. Flash!

## secure boot

https://www.cnblogs.com/dongxb/p/16717567.html

https://zhuanlan.zhihu.com/p/481696760



## initramfs

https://manpages.ubuntu.com/manpages/focal/en/man8/update-initramfs.8.html

update-initramfs - generate an initramfs image

https://help.ubuntu.com/community/ResizeEncryptedPartitions

## LVM + LUKS 磁盘扩容

