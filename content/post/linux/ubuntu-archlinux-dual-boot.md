---
title: ubuntu archlinux dual boot
author: "-"
date: 2025-12-03T16:00:00+08:00
url: ubuntu-archlinux-dual-boot
categories:
  - Linux
tags:
  - reprint
  - remix
  - AI-assisted
---
## ubuntu archlinux dual boot

因为某种原因, ubuntu 安装的时候选了 luks + lvm, 只能格掉整个硬盘安装 ubuntu

ubuntu 安装之后再手动的给分区缩容, 然后再安装 archlinux

分区缩容的过程在这里 wiloon.com/disk/resize

## 双系统分区配置

主硬盘 nvme0n1 的完整分区布局（四个分区）：

### 1. nvme0n1p1 - EFI 分区（共享）

- 文件系统：vfat (FAT32)
- 大小：1.1GB
- 挂载点：
  - Ubuntu: `/boot/efi`
  - Archlinux: `/efi`
- 使用率：1%
- UUID：`FF07-C6C8`
- 说明：双系统共享的 UEFI 引导分区

### 2. nvme0n1p2 - Ubuntu Boot 分区

- 文件系统：ext4
- 大小：2.0GB
- 挂载点：`/boot` (Ubuntu)
- 使用率：12%
- UUID：`a45ac700-f127-447d-880d-8a8d51d37f49`
- 说明：Ubuntu 的 boot 分区，存储内核和 initramfs

### 3. nvme0n1p3 - Ubuntu 加密根分区

- 类型：crypto_LUKS (LUKS2 加密)
- 加密 UUID：`4bb8683a-8706-44e1-ad3b-0388d44759cb`
- 内含 LVM 配置：
  - 卷组：`ubuntu-vg`
  - 逻辑卷：`ubuntu-lv` (492GB, ext4)
  - 挂载点：`/` (Ubuntu 根目录)
  - 使用情况：198GB 已用 / 269GB 可用 (43%)
  - 文件系统 UUID：`e3ad7c01-acec-4afc-9915-2203badc5e11`
- 说明：Ubuntu 的加密根分区，使用 LUKS + LVM

### 4. nvme0n1p4 - Archlinux 根分区

- 文件系统：ext4
- 大小：约 353GB
- 挂载点：`/` (Archlinux 根目录)
- 使用情况：90GB 已用 / 245GB 可用 (27%)
- UUID：`63c2c764-83b9-4b1b-99f3-db52c03f0109`
- 说明：Archlinux 的根分区，无加密

### 查看分区信息的命令

```bash
# 查看所有块设备及其文件系统类型
lsblk -f

# 查看磁盘空间使用情况
df -h

# 查看详细分区信息
sudo parted /dev/nvme0n1 print

# 查看文件系统挂载配置
cat /etc/fstab
```

又因为要开 secure boot, 需要在 ubuntu 的 grub 里引导 archlinux 的内核, 所以不能用 archinstall, 因为 archinstall 会安装自己的 grub

所以只能手动安装 archlinux, archlinux 不加密

https://wiki.archlinux.org/title/Installation_guide

```bash
# Verify the boot mode
cat /sys/firmware/efi/fw_platform_size
# 64, the system is booted in UEFI mode and has a 64-bit x64 UEFI.

# Update the system clock
timedatectl

# 查看磁盘信息
lsblk

# 用 parted 分区（首次安装时执行，重装时跳过）
# 有 32G 内存, 所以没有建 swap 分区
# 跟 ubuntu 共享 EFI 分区, 也就是 /boot/efi
# 注意：如果 nvme0n1p4 分区已经存在，跳过分区步骤，直接格式化
parted -a optimal /dev/nvme0n1
# 查看分区情况, 空闲空间也打印出来
(parted) print free
(parted) mkpart primary ext4 615GB 1000GB
(parted) quit

# 格式化分区为 ext4（会清除分区上的所有数据）
mkfs.ext4 /dev/nvme0n1p4

# Mount the file systems
mount /dev/nvme0n1p4 /mnt

# config mirror
vim /etc/pacman.d/mirrorlist

# add line
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch

# Install essential packages
# amd cpu 所以需要 amd-ucode
mkdir -p /mnt/etc && touch /mnt/etc/vconsole.conf
pacstrap -K /mnt base linux linux-firmware amd-ucode vim
# 注意：安装过程中可能会出现 "ERROR: file not found: '/etc/vconsole.conf'" 错误
# 这是正常的，因为是全新安装，该文件尚不存在，可以忽略继续
# 如果想避免这个错误，可以在 pacstrap 前创建空文件：
# mkdir -p /mnt/etc && touch /mnt/etc/vconsole.conf

# Generate an fstab file
genfstab -U /mnt >> /mnt/etc/fstab

# Change root into the new system
arch-chroot /mnt
```

## 继续安装 Archlinux

```bash

#Set the time zone:
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# Run hwclock(8) to generate /etc/adjtime:
hwclock --systohc

# Localization
# Uncomment the needed locales(en_US.UTF-8, zh_CN.UTF-8) in /etc/locale.gen, then generate them with: locale-gen
vim /etc/locale.gen

en_US.UTF-8 UTF-8
zh_CN.UTF-8 UTF-8

locale-gen

# Create the locale.conf(5) file, and set the LANG variable accordingly:
# 文件设置全局有效的locale,没有的话新建一个文件。
/etc/locale.conf
LANG=en_US.UTF-8

# Network configuration
# Create the hostname file
vim /etc/hostname

# config eth
vim /etc/systemd/network/eth.network

[Match]
Name=en*

[Network]
Address=192.168.50.19/24
Gateway=192.168.50.61
DNS=192.168.50.1

# Set the root password:
passwd

# install wpa_supplicant
pacman -S wpa_supplicant
pacman -S openssh
systemctl enable sshd
systemctl enable systemd-networkd
systemctl enable systemd-resolved.service
vim /etc/ssh/sshd_config # PermitRootLogin yes

# Boot loader
# use ubuntu's grub to boot archlinux, do not install grub here

# Reboot
# Exit the chroot environment by typing exit or pressing Ctrl+d.
```

## ubuntu grub 配置 archlinux

从 Ubuntu 20.04.3 / 21.04 开始，出于安全原因，os-prober 默认被禁用。

```Bash
vim /etc/default/grub
# Uncomment the following line to enable os-prober
GRUB_DISABLE_OS_PROBER=false
# 从 hidden 改为 menu, 否则 grub 只会显示 ubuntu
GRUB_TIMEOUT_STYLE=menu
# Set the timeout, 0 means no timeout, -1 means wait indefinitely
GRUB_TIMEOUT=5

# Update grub
sudo update-grub

# 这时你应该能看到类似输出：
# Found Arch Linux on /dev/nvme0n1p4

# 查看 grub.cfg 中是否包含 archlinux 的 menuentry
cat /boot/grub/grub.cfg

reboot
```
