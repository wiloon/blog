---
title: archlinux grub
author: "-"
date: 2020-01-12T07:22:08+00:00
url: /?p=15345
categories:
  - inbox
tags:
  - reprint
---
## archlinux grub

### parted flag

For parted set/activate the flag bios_grub on the partition.

```bash
parted -a optimal /dev/sda
    set 1 bios_grub on

pacman -S grub
# where /dev/sdX is the disk (not a partition)
grub-install --target=i386-pc /dev/sdX

grub-mkconfig -o /boot/grub/grub.cfg

### exit arch-chroot
exit

# 重启
reboot
```
