---
title: aliyun ecs, 阿里云安装 archlinux
author: "-"
date: 2012-09-16T07:11:34+00:00
url: archlinux/aliyun
categories:
  - Linux
tags:
  - reprint
---
## aliyun ecs, 阿里云安装 archlinux

```bash
curl -O http://mirrors.163.com/archlinux/iso/2022.02.01/archlinux-bootstrap-2022.02.01-x86_64.tar.gz
tar zxvf archlinux-bootstrap-2022.02.01-x86_64.tar.gz
sudo mount --bind /tmp/root.x86_64 /tmp/root.x86_64
/tmp/root.x86_64/bin/arch-chroot /tmp/root.x86_64/

pacman-key --init
pacman-key --populate archlinux

mount /dev/vda1 /mnt

# 保留的目录  /dev /proc /run /sys /tmp 
rm -rf /mnt/bin
rm -rf /mnt/boot
rm -rf /mnt/data
rm -rf /mnt/etc
rm -rf /mnt/home
rm -rf /mnt/lib
rm -rf /mnt/lib64
rm -rf /mnt/media
rm -rf /mnt/mnt
rm -rf /mnt/opt
rm -rf /mnt/root
rm -rf /mnt/sbin
rm -rf /mnt/srv
rm -rf /mnt/usr
rm -rf /mnt/var

pacstrap /mnt base linux linux-firmware
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
echo 'nameserver 114.114.114.114' >> resolv.conf

pacman -S gvim openssh grub sudo neofetch python

echo 'pingd0' > /etc/hostname
echo '127.0.0.1    localhost' >> /etc/hosts
echo '127.0.0.1    pingd0' >> /etc/hosts

systemctl enable systemd-networkd
systemctl enable systemd-resolved
systemctl enable sshd

vim /etc/systemd/network/eth.network

[Match]
Name=en*

[Network]
DHCP=ipv4

[DHCPv4]
UseHostname=false

useradd -m wiloon
passwd wiloon

passwd root

echo 'wiloon ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/wiloon.conf
grub-install --target=i386-pc /dev/vda
grub-mkconfig -o /boot/grub/grub.cfg

reboot

timedatectl set-ntp true

```

```bash
                   -`                    root@pingd0 
                  .o+`                   ----------- 
                 `ooo/                   OS: Arch Linux x86_64 
                `+oooo:                  Host: Alibaba Cloud ECS pc-i440fx-2.1 
               `+oooooo:                 Kernel: 5.16.8-arch1-1 
               -+oooooo+:                Uptime: 2 mins 
             `/:-:++oooo+:               Packages: 128 (pacman) 
            `/++++/+++++++:              Shell: bash 5.1.16 
           `/++++++++++++++:             Resolution: 1024x768 
          `/+++ooooooooooooo/`           CPU: Intel Xeon Platinum 8163 (1) @ 2.500GHz 
         ./ooosssso++osssssso+`          GPU: 00:02.0 Cirrus Logic GD 5446 
        .oossssso-````/ossssss+`         Memory: 76MiB / 466MiB 
       -osssssso.      :ssssssso.
      :osssssss/        osssso+++.                               
     /ossssssss/        +ssssooo/-                               
   `/ossssso+/:-        -:/+osssso+-
  `+sso+:-`                 `.-/+oso:
 `++:.                           `-/+/
 .`                                 `/
```
>https://limelight.moe/t/topic/6007
>https://www.scarletdrop.cn/archives/14


