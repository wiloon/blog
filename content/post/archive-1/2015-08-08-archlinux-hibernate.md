---
title: archlinux hibernate
author: wiloon
type: post
date: 2015-08-08T05:44:49+00:00
url: /?p=8082
categories:
  - Uncategorized
tags:
  - Arch Linux

---
edit config file  /etc/mkinitcpio.conf

Configure the initramfs

When an initramfs with the base hook is used, which is the default, the resume hook is required in /etc/mkinitcpio.conf. Whether by label or by UUID, the swap partition is referred to with a udev device node, so the resume hook must go after the udev hook. This example was made starting from the default hook configuration:
  
HOOKS=&#8221;base udev resume autodetect modconf block filesystems keyboard fsck&#8221;
  
Remember to rebuild the initramfs for these changes to take effect.
  
run mkinitcpio -p linux to rebuild the initramfs

```bash&lt;br />mkinitcpio -p linux
```

```bashvim /boot/loader/entries/arch.conf
# add line
options resume=UUID=edf3ac02-8e07-4625-a831-a6d19dab9c3c
```

edit /boot/syslinux/syslinux.cfg

Required kernel parameters
  
resume=_swap_partition_

```bash&lt;br />LABEL arch
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

https://wiki.archlinux.org/index.php/Power\_management/Suspend\_and_hibernate