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

Ubuntu: 22.04

1. 在硬盘上准备一块空闲的空间
    - 用 windows 的磁盘管理工具调整现有的分区
2. 用 balenaEtcher 制作 ubuntu 安装盘 (U盘)
2. 在 BIOS 里确认 Secure Boot 已经开启
3. 用分区工具在U盘或移动硬盘上准备一个大于 100MB 的 FAT32 分区
4. 从 U 盘引导,安装 ubuntu, 选择 Try or install Ubuntu
5. Select Language: English
6. Install> Install Ubuntu
7. Keyboard: English(US)> English(US)
8. Wireless
9. What apps would you like to install to start with: Minimal installation
10. 勾选 Install third-party software for graphics and wi-fi hardware and additional media formats
11. 勾选 Configure Secure Boot, 设置 Secure boot 密码
12. open a terminal with ctrl+alt+t
13. 切换到 root 用户: sudo -i
14. lsblk to list all devices
15. 挂载 FAT32 分区
    - mkdir /mnt/persistent
    - mount /dev/sda2 /mnt/persistent
    - mkdir /mnt/persistent/efi-backup
16. Mount the Windows bootloader partition
    - mkdir /mnt/efi
    - mount /dev/nvme0n1p1 /mnt/efi
17. Backup all the data on it, and make sure to correctly execute rsync as shown here (with trailing slashes):
    rsync -av /mnt/efi/ /mnt/persistent/efi-backup/
18. Now we delete the content on the efi partition (don't be scared, we will copy it back later)
    rm -rf /mnt/efi/*
19. Umount again the efi partition
    umount /mnt/efi
    umount /mnt/persistent
20. 回到 Ubuntu 的图形化安装环境 选择 something else, click continue
21. 选择 free space, 一般在 /dev/nvme0n1p3 和 /dev/nvme0n1p4 之间
22. 点击加号创建分区
    - 创建一个512MB 的分区
      - Use as: EFI System Partition
    - 创建一个 2048MB 的分区
      - Use as: Ext4 journaling file system
      - Mount point: `/boot`
    - 创建一个 12000MB 的的分区
      - Use as: Ext4 journaling file system
      - mount point: `/`
      - 之后会删掉, 这个分区不需要太大
23. Device for boot loader installation: 选择新的 EFI 分区: /dev/nvme0n1p5, 点击 Install Now
    - 选择了 /dev/nvme0n1p5 但是 Ubuntu 还是会安装到 /dev/nvme0n1p1
    - 安装完成之后再把备份的 windows boot loader 恢复回来
24. 选择时区
25. Who are you
    - Your name: xxx
    - Your computer's name: xxx
    - Pick a username: xxx
    - Choose a password: xxx
    - Confirm your password: xxx
26. 安装结束之后不要点击 Restart Now, 点击右上角的 `X` 关闭窗口, 系统会回到 Ubuntu live usb 状态 
27. open a terminal with ctrl+alt+t, 切换到 root 用户: sudo -i
28. 把 ubuntu installer 刚才安装的 /dev/nvme0n1p1 拷到 /dev/nvme0n1p5
    - mount /dev/nvme0n1p1 /mnt/efi
    - mkdir /mnt/new-efi && mount /dev/nvme0n1p5 /mnt/new-efi
    - rsync -av /mnt/efi/ /mnt/new-efi/ (with trailing slashes)
29. 把之前备份的 windows boot loader 恢复到 /dev/nvme0n1p1
    - mount /dev/sda2 /mnt/persistent
    - rm -rf /mnt/efi/*
    - rsync -av /mnt/persistent/efi-backup/ /mnt/efi/ (with trailing slashes)
30. umount
    - umount /mnt/efi
    - umount /mnt/new-efi
    - umount /mnt/persistent
31. 在 terminal 运行 gparted
    - 选中 /dev/nvme0n1p7 后面的 unallocated 空间
    - 创建分区
      - File system: cleared
      - click Add
    - Appy All Operations
32. 关掉 gparted, 回到 root terminal
33. 加密分区
    - cryptsetup luksFormat /dev/nvme0n1p8
      - are you sure: YES (一定要输入大写的 YES)
    - cryptsetup open /dev/nvme0n1p8 nvme0n1p8_crypt
    - pvcreate /dev/mapper/nvme0n1p8_crypt
    - vgcreate vgubuntu /dev/mapper/nvme0n1p8_crypt
    - vgs -a # Check the available size and decide how big your partitions hould be
    - lvcreate --name swap_1 -L 16G vgubuntu
    - lvcreate --name root -L 67g vgubuntu
    - mkfs.ext4 /dev/vgubuntu/root
    - mkswap /dev/vgubuntu/swap_1
34. 把之前安装的未加密的 ubuntu 拷到新的加密分区
    - mkdir /mnt/root-orig
    - mkdir /mnt/root-new
        mount /dev/nvme0n1p7 /mnt/root-orig/
        mount /dev/vgubuntu/root /mnt/root-new/
        rsync -avhPAXHx --numeric-ids /mnt/root-orig/ /mnt/root-new/
    - umount /mnt/root-orig
    - umount /mnt/root-new
    - vgchange -an vgubuntu
    - cryptsetup luksClose nvme0n1p8_crypt
      - (准备删除分区和扩分区)
35. 删除旧的未加密的 ubuntu, 扩展加密分区
    - open gparted
    - remove /dev/nvme0n1p7
    - resize /dev/nvme0n1p8 to use free space
    - cryptsetup open /dev/nvme0n1p8 nvme0n1p8_crypt
    - vgchange -an vgubuntu
    - cryptsetup resize nvme0n1p8_crypt
    - pvresize /dev/mapper/nvme0n1p8_crypt
    - vgchange -ay vgubuntu
    - pvchange -x y /dev/mapper/nvme0n1p8_crypt
    - lvresize -L +11G vgubuntu/root
    - pvchange -x n /dev/mapper/nvme0n1p8_crypt
    - e2fsck -f /dev/mapper/vgubuntu-root
    - resize2fs -p /dev/mapper/vgubuntu-root
36. chroot to configure new installation
    - mount /dev/vgubuntu/root /mnt/root-new/
    - mount /dev/nvme0n1p6 /mnt/root-new/boot/
    - mount /dev/nvme0n1p5 /mnt/root-new/boot/efi/
    - mount --bind /dev /mnt/root-new/dev/
    - mount --bind /proc /mnt/root-new/proc/
    - mount --bind /sys /mnt/root-new/sys/
    - mount --bind /run /mnt/root-new/run/
    - chroot /mnt/root-new/ /bin/bash
    - apt update
    - apt install lvm2 cryptsetup vim
    - blkid /dev/nvme0n1p8 # Copy the UUID
    - vim /etc/crypttab

And now put in a new entry with your copied UUID

```Bash
nvme0n1p8_crypt UUID=UUID none luks,discard
```

blkid /dev/nvme0n1p5 # Get UUID of EFI
vim /etc/fstab

```Bash
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/... during installation
/dev/mapper/vgubuntu-root /               ext4    errors=remount-ro 0       1
# /boot was on /dev/nvme0n1p6 during installation
UUID=fd1eecf5-18b0-42fb-a3d4-5239c1465fc1 /boot           ext4    defaults        0       2
# /boot/efi was on /dev/nvme0n1p5 during installation
UUID=EF18-AD8F  /boot/efi       vfat    umask=0077      0       1
/dev/mapper/vgubuntu-swap_1 none    swap    sw  0   0
```

Now apply update

update-initramfs -u -k all


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
  - /dev/nvme0n1p1: 100MB, window boot loader EFI
  - /dev/nvme0n1p2: 16MB, unknow, created by windows
  - /dev/nvme0n1p3: 378G, windows data NTFS (bitlocker)
  - /dev/nvme0n1p4: 890MB, windows recovery
  - /dev/nvme0n1p5: 487MB, ubuntu boot loader EFI
  - /dev/nvme0n1p6: 1.9G, ubuntu /boot
  - /dev/nvme0n1p7: 11.2G, ubuntu /root (original) (delete)
  - /dev/nvme0n1p8: 84.1G, ubuntu (LVM PV + LUKS)
    - nvme0n1p8_crypt
    - vgubuntu-swap_1 16G ubuntu swap
    - vgubuntu-root 67G ubuntu /root

https://askubuntu.com/questions/1506694/dual-boot-with-windows-11-and-bitlocker/1514161#1514161

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

## `clonezill`

https://clonezilla.org/

https://clonezilla.org/liveusb.php#macos-setup

1. Download the `Clonezilla` Live iso file.
2. Insert a USB flash drive on the Mac machine.
3. Erase it using the standard Mac Disk Utility (exFAT works fine).
4. Download `balenaEtcher` for macOS, then follow its document to burn the image to the USB flash drive.
5. Eject the USB drive.

Thanks to Hans Palm for providing this info.

### 备份硬盘

https://minipc.netlify.app/posts/3390c071/

1. Clonezilla GNU GRUB
2. Clonezilla live (VGA 800*600)
3. zh_CN.UTF8 Chinese
4. keyboard: Keep
5. start clonezilla
6. device-image
7. local_dev
8. 插入移动硬盘
9. 屏幕上会打印出当前连接的存储设备, 能看到系统盘 nvme01和移动硬盘
10. ctrl-c
11. 选择保存镜像文件的分区, 选移动硬盘上的空闲分区 sdb1
12. 检查文件系统, 因为要备份的是windows所以选择 no-fsck
13. 选择保存镜像的目录, 默认选中的是根目录, 选好之后选择 Done
14. 看一下屏幕上打印的挂载状态, 没有问题的话按回车
15. 模式选择: Beginner
16. savedisk: 备份整个目标硬盘
17. 输入镜像名
18. 选择要备份的硬盘: nvme0n1
19. 压缩方式: z9p (默认)
20. 因为目标盘是 windows, 所以跳过 fsdk: -sfsck
21. 检查保存的镜像
22. 不加密 -senc
23. 操作完成要执行的动作 -p choose
24. 按 y 执行


## balenaEtcher

https://etcher.balena.io/#download-etcher

1. flash from file
2. select target
3. Flash!

## secure boot

https://www.cnblogs.com/dongxb/p/16717567.html

https://zhuanlan.zhihu.com/p/481696760

## pvcreate

pvcreate 命令的功能是用于创建物理卷设备。LVM逻辑卷管理器技术由物理卷、卷组和逻辑卷组成，其中pvcreate命令的工作属于第一个环节——创建物理卷设备。

```Bash
pvcreate /dev/mapper/nvme0n1p8_crypt
```

vgcreate 指令用于创建LVM卷组。

```Bash
vgcreate vgubuntu /dev/mapper/nvme0n1p8_crypt
```

## initramfs

https://manpages.ubuntu.com/manpages/focal/en/man8/update-initramfs.8.html

update-initramfs - generate an initramfs image

https://help.ubuntu.com/community/ResizeEncryptedPartitions
