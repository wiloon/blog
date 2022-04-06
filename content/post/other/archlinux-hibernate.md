---
title: archlinux hibernate
author: "-"
date: 2015-08-08T05:44:49+00:00
url: archlinux/hibernate
categories:
  - linux
tags:
  - archlinux

---
## archlinux hibernate

### edit config file  /etc/mkinitcpio.conf add resume field
```bash
sudo vim /etc/mkinitcpio.conf
HOOKS=(base udev resume autodetect modconf block filesystems keyboard fsck)
```
Configure the initramfs

When an initramfs with the base hook is used, which is the default, the resume hook is required in /etc/mkinitcpio.conf. Whether by label or by UUID, the swap partition is referred to with a udev device node, so the resume hook must go after the udev hook. This example was made starting from the default hook configuration:

Remember to rebuild the initramfs for these changes to take effect.
  
run mkinitcpio -p linux to rebuild the initramfs

### rebuild initramfs
```bash
sudo mkinitcpio -p linux
```

### for uefi
```bash
vim /boot/loader/entries/arch.conf
# add line
options resume=UUID=ed325732-b768-4680-a4ff-24dd0da24509
```

### for syslinux
edit /boot/syslinux/syslinux.cfg

Required kernel parameters
  
resume=_swap_partition_

```bash

LABEL arch
TEXT HELP
Boot Arch Linux
ENDTEXT
MENU LABEL Arch Linux
LINUX /boot/vmlinuz-linux
APPEND root=PARTUUID=1af9c78c-0c07-42fb-9e8c-201235183fd5 rootfstype=ext4 rw rootflags=rw,noatime,discard,data=ordered cgroup_disable=memory resume=/dev/sda1
INITRD /boot/intel-ucode.img,/boot/initramfs-linux.img

systemctl hibernate
```

hibernate and re start the system.

https://wiki.archlinux.org/index.php/Power_management/Suspend_and_hibernate