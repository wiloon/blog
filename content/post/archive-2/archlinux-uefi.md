---
title: archlinux UEFI
author: "-"
date: 2018-12-08T13:38:38+00:00
url: /?p=12981
categories:
  - Inbox
tags:
  - reprint
---
## archlinux UEFI
```bash
# boot with iso-usb
ls /sys/firmware/efi
dmesg |grep sdx
lsblk
gdisk /dev/sdx
o
y
n
EF00
n
w
y
/dev/sdx1 512M EFI
/dev/sdx2 xxxxM ext4

mkfs.vfat /dev/sdx1
mkfs.ext4 /dev/sdx2

mount /dev/sdx2 /mnt
mkdir /mnt/boot
mount/dev/sdx1 /mnt/boot
pacstrap /mnt
arch-chroot /mnt
bootctl install
cd /boot/loader
pacman -S vim
vim loader.conf
default arch
timeout 4
cd entries
vim arch.conf

title Archlinux
linux /vmlinuz-linux
initrd /initramfs-linux.img
options root=PARTUUID=xxx rw

r !blkid

reboot

```