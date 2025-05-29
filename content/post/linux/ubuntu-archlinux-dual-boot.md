---
title: ubuntu archlinux dual boot
author: "-"
date: 2014-11-30T01:40:15+00:00
url: ubuntu-archlinux-dual-boot
categories:
  - Linux
tags:
  - reprint
---
## ubuntu archlinux dual boot

因为某种原因, ubuntu 安装的时候选了 luks + lvm, 只能格掉整个硬盘安装 ubuntu

ubuntu 安装之后再手动的给分区缩容, 然后再安装 archlinux

分区缩容的过程在这里 wiloon.com/disk/resize

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

# 用 parted 分区
# 有 32G 内存, 所以没有建 swap 分区
# 跟 ubuntu 共享 EFI 分区, 也就是 /boot/efi
parted -a optimal /dev/nvme0n1
# 查看分区情况, 空闲空间也打印出来
(parted) print free
(parted) mkpart primary ext4 615GB 1000GB
(parted) quit

# 格式化分区为 ext4
mkfs.ext4 /dev/nvme0n1p4

# Mount the file systems
mount /dev/nvme0n1p4 /mnt

# config mirror
vim /etc/pacman.d/mirrorlist

# add line
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch

# Install essential packages
# amd cpu 所以需要 amd-ucode
pacstrap -K /mnt base linux linux-firmware amd-ucode vim
# Generate an fstab file
genfstab -U /mnt >> /mnt/etc/fstab

# Change root into the new system
arch-chroot /mnt

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
Gateway=192.168.50.21
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
