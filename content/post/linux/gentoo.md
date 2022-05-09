---
title: Gentoo
author: "-"
date: 2011-11-26T06:40:52+00:00
url: /?p=1607
categories:
  - Linux

tags:
  - reprint
---
## Gentoo
#  Gentoo是一个基于Linux的自由操作系统，它能为几乎任何应用程序或需求自动地作出优化和定制。追求极限的配置、性能，以及顶尖的用户和开发者社区，都是Gentoo体验的标志特点。 Gentoo的哲学是自由和选择。得益于一种称为Portage的技术，Gentoo能成为理想的安全服务器、开发工作站、专业桌面、游戏系统、嵌入式解决方案或者别的东西——你想让它成为什么，它就可以成为什么。由于它近乎无限的适应性，可把Gentoo称作元发行版。

# 简介


  Gentoo已经停止发布新的编译版，最近一次发布的是10.0，之所以发行是为了纪念发行十周年。之所以不发行编译版，是因为没有这个必要，Gentoo不提供传统意义的安装程序，他的安装CD只是提供一个Linux环境，从分区，挂载硬盘，下载编译内核，书写Grub等等都需要手动命令行一步步来。复杂的安装过程往往会让很多新手觉得沮丧，但是它确实能更好的帮你了解Linux的构建。 
  
  
  
    当然，Gentoo的意义不仅仅在于它所提供的软件。它是围绕着一个发行版建立起来的社区，由300多名开发人员和数以千记的用户共同驱动。发行版项目为用户提供各种途径来享用Gentoo: 文档、基础设施 (邮件列表、站点、论坛……) 、版本发布工程、软件移植、质量保证、安全跟进、强化等等。
  
  
  
    为了商讨和协助Gentoo的全局开发，每年推选出一个7人议会，对Gentoo项目中的全局性问题、方针政策和发展进步做出决定。
  
  
  
  
    核心
  
  
    Portage是Gentoo的核心，履行许多关键的职责。其一，Portage是Gentoo的软件发行系统。Gentoo
 下要获取最新的软件，打一个命令: emerge-sync。这个命令告诉Portage从网上更新你本地的"Portage树"。本地Portage树包含一份完整的脚本集合，Portage以之创建和安装最新的Gentoo软件包。当前，我们的Portage树中拥有超过10000个软件包，软件包更新和新软件包每时每刻都在加入中。Portage也是一个软件包构建和安装系统。当你想安装一个软件包时，你输入"emerge 软件包名"，此时Portage按照你作的具体配置自动构建一个软件包的定制版本。请根据自己的硬件优化配置，确保启用了软件包中你想要的一些可选特性——同时确保未启用那些你不想要的。
  
  
  
    Portage还使系统保持在持续更新状态。输入emerge -uDN world——一个命令——能确保系统中你想要的所有软件包得到自动更新。
  
  
  
  
    优点
  
  
    与大多数GNU/Linux发行版本不同，Gentoo Linux为用户提供了大量的应用程序源代码。Gentoo Linux的每一部分都可以在最终用户的系统上重新编译建造，甚至包括最基本的系统库和编译器自身。 通过依赖关系描述和源代码镜像的形式提供软件，Gentoo Linux提供了大量软件供用户选择。 标准的源代码镜像包括30G的数据。 选择不仅在软件整体方面，也存在于软件的内部。由于可以在本地编译软件，参数和变量的选择可以由用户自己指定。
  
  
  
    指定参数的优势不仅在于用户了解了设置，更多是增加了针对硬件进行性能提升的余地。 而且用户可以使用自己喜欢的补丁或插件对软件功能进行调整，比如当前的Gentoo Linux内核发布包括35种。
  
  
  
    由于系统及应用软件的安装方法差异显著，Gentoo Linux社区对安装内容的探讨相当深入。即便不使用 Gentoo Linux的用户也可以通过了解参数选择明白软件内部的设定。应用软件的配置设定都记录在ebuild文件中，由ebuild、emerge命令管理。

## gentoo
```bash
  
mount /dev/sda3 /mnt/gentoo
  
mount /dev/sda1 /mnt/gentoo/boot
  
chmod 1777 /mnt/gentoo/tmp

mount -t proc proc /mnt/gentoo/proc
  
mount -rbind /sys /mnt/gentoo/sys
  
mount -make-rslave /mnt/gentoo/sys
  
mount -rbind /dev /mnt/gentoo/dev
  
mount -make-rslave /mnt/gentoo/dev
  
mount -t tmpfs -o nosuid,nodev,noexec shm /dev/shm
  
chmod 1777 /dev/shm

chroot /mnt/gentoo /bin/bash
  
source /etc/profile
  
export PS1="(chroot) $PS1"
  
```

the minimal install cds have the ability to run isohybrid on them and then you can dd that image to a removable device.



  
    
      Code:
    
  
  
  
    
      # isohybrid image.iso && dd if=image.iso of=/dev/sdb bs=8192k
    
  



dmesg

lspci -k

```bash

gentoo dosshd

passwd

#wireless
  
#http://www.wiloon.com/?p=6008
  
#start sshd

parted -a optimal /dev/sda
  
mklabel gpt
  
unit mib
  
mkpart primary 1 129
  
name 1 boot
  
mkpart primary 129 17536
  
name 2 swap
  
mkpart primary  17536 -1
  
name 3 rootfs
  
set 1 boot on
  
quit

#mkfs.vfat /dev/sda1
  
mkfs.msdos -F 32 /dev/sda1
  
mkfs.ext4 /dev/sda3
      
Filesystem UUID: d10a8895-80c5-44ef-be41-edc0bca71c5b
  
mkswap /dev/sda2
      
UUID=4d2d7b5c-0d27-4b1d-8e2e-826a3ebb12f4

mount /dev/sda3 /mnt/gentoo
  
mkdir /mnt/gentoo/boot
  
mount /dev/sda1 /mnt/gentoo/boot
  
mkdir /mnt/gentoo/tmp
  
chmod 1777 /mnt/gentoo/tmp
  
date
  
cd /mnt/gentoo
  
#download stage tarball
  
tar xvjpf stage3-*.tar.bz2 -xattrs

#Configuring compile options
  
mirrorselect -i -o >> /mnt/gentoo/etc/portage/make.conf
  
cp -L /etc/resolv.conf /mnt/gentoo/etc/

mount -t proc proc /mnt/gentoo/proc
  
mount -rbind /sys /mnt/gentoo/sys
  
mount -make-rslave /mnt/gentoo/sys
  
mount -rbind /dev /mnt/gentoo/dev
  
mount -make-rslave /mnt/gentoo/dev
  
mount -t tmpfs -o nosuid,nodev,noexec shm /dev/shm
  
chmod 1777 /dev/shm

chroot /mnt/gentoo /bin/bash
  
source /etc/profile
  
export PS1=&quot;(chroot) $PS1&quot;

emerge-webrsync
  
emerge -sync
  
eselect profile list
  
eselect profile set 3

nano -w /etc/portage/make.conf
  
echo &quot;Asia/Shanghai&quot; >/etc/timezone
  
emerge -config sys-libs/timezone-data
  
nano -w /etc/locale.gen
  
locale-gen
  
eselect locale list
  
eselect locale set 5
  
env-update &amp;&amp; source /etc/profile

emerge -ask sys-kernel/gentoo-sources
  
ls -l /usr/src/linux
  
emerge genkernel
  
genkernel -install initramfs
  
ls /boot/initramfs*

nano -w /etc/fstab
  
emerge -ask sys-kernel/genkernel
  
genkernel all
  
ls /boot/kernel\* /boot/initramfs\*
  
find /lib/modules/4.0.5-gentoo/ -type f -iname '\*.o' -or -iname '\*.ko' | less
  
emerge -ask sys-kernel/linux-firmware
  
nano -w /etc/fstab
  
nano -w /etc/conf.d/hostname
  
emerge -ask -noreplace net-misc/netifrc
  
passwd
  
emerge -ask app-admin/syslog-ng
  
emerge -ask sys-process/cronie
  
crontab /etc/crontab
  
emerge -ask sys-apps/mlocate
  
nano -w /etc/inittab
  
emerge -ask net-misc/dhcpcd
  
nano -w /etc/portage/make.conf
  
Enable the systemd USE flag globally (in make.conf).
  
eselect profile list
  
emerge -avDN @world

#syslinux
  
#efi
  
echo sys-boot/syslinux >> /etc/portage/package.keywords
  
emerge -ask sys-boot/syslinux
  
mkdir -p /boot/efi/EFI/syslinux
  
cd /usr/share/syslinux/efi64
  
cp syslinux.efi ldlinux.e64 menu.c32 libcom32.c32 libutil.c32 /boot/efi/EFI/syslinux

#syslinux, bios
  
dd bs=440 conv=notrunc count=1 if=/usr/share/syslinux/gptmbr.bin of=/dev/sda
  
emerge sys-apps/gptfdisk
  
gdisk /dev/sda
  
x
  
a
  
w

mkdir /boot/extlinux
  
extlinux -install /boot/extlinux
  
ln -snf . /boot/boot
  
cd /usr/share/syslinux
  
cp menu.c32 memdisk libcom32.c32 libutil.c32 /boot/extlinux
  
```