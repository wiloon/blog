---
title: archlinux kvm qemu gentoo
author: "-"
date: 2015-12-07T14:37:48+00:00
url: /?p=8534
categories:
  - Inbox
tags:
  - reprint
---
## archlinux kvm qemu gentoo

```bash
pacman -Syu
pacman -S qemu
pacman -S qemu-launcher
qemu-img create -f raw gentoo.img 20G
qemu-img create -f qcow2 gentoo 20G

exec qemu-system-x86_64 -enable-kvm -cpu host -cdrom install-amd64-minimal-20150924.iso -boot order=d -drive file=gentooVM.img,if=virtio -netdev user,id=vmnic,hostname=gentoovm -device virtio-net,netdev=vmnic -m 2048M -monitor stdio -name "Gentoo VM"

pacman -S linux-atm
pacman -S bridge-utils

在主机上创建桥
创建桥的原因是虚拟机间,虚拟机与主机间的互联
$ sudo brctl addbr br0
ip tuntap

#start gentoo with sshd
gentoo dosshd
#or /etc/init.d/sshd start

#prepare partition

#mounting
mount /dev/sda4 /mnt/gentoo
mkdir /mnt/gentoo/boot
mount /dev/sda2 /mnt/gentoo/boot
chmod 1777 /mnt/gentoo/tmp
#Downloading the stage tarball
```

<https://bbs.archlinux.org/viewtopic.php?id=164461>
  
<https://wiki.archlinux.org/index.php/Network_bridge_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87>)
  
<https://www.ibm.com/developerworks/community/blogs/5144904d-5d75-45ed-9d2b-cf1754ee936a/entry/%25e6%2589%258b%25e5%258a%25a8%25e5%2588%259b%25e5%25bb%25banat%25e7%25bd%2591%25e7%25bb%259c?lang=en>
