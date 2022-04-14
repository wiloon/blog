---
title: gentoo
author: "-"
date: 2015-09-12T06:09:48+00:00
url: /?p=8243
categories:
  - Uncategorized

tags:
  - reprint
---
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