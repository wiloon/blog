---
title: 公有云安装 archlinux, Aliyun/阿里云 ecs, bwg KVM
author: "-"
date: 2012-09-16T07:11:34+00:00
url: archlinux/cloud
categories:
  - Linux
tags:
  - reprint
  - remix
---
## aliyun ecs, 阿里云安装 archlinux

aliyun  vm  安装 非 EFI 的镜像

```bash
cd /tmp
curl -O http://mirrors.163.com/archlinux/iso/2024.04.01/archlinux-bootstrap-2024.04.01-x86_64.tar.gz

tar zxvf archlinux-bootstrap-xxx.tar.gz

# 要用 mount --bind 把 RootFS 解包的目录自己与自己链接起来，不然 pacman 会装不了软件
sudo mount --bind /tmp/root.x86_64 /tmp/root.x86_64

# edit mirror list
vim /tmp/root.x86_64/etc/pacman.d/mirrorlist

# chroot
/tmp/root.x86_64/bin/arch-chroot /tmp/root.x86_64/

# 初始化 pacman 的密钥
pacman-key --init
pacman-key --populate archlinux

# 把 原系统的 根目录 / 挂载到  /mnt
# 先 df -h 看一下 根目录在哪个分区
mount /dev/vdaX /mnt

# 保留的目录  /dev /proc /run /sys /tmp , 这些目录都是存储到硬件的映射的，所以不能删
# boot 目录有可能会删除失败
rm -rf /mnt/boot
rm -rf /mnt/bin
rm -rf /mnt/data
rm -rf /mnt/etc
rm -rf /mnt/home
rm -rf /mnt/lib
rm -rf /mnt/lib32
rm -rf /mnt/lib64
rm -rf /mnt/libx32
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

echo 'aliyun0' > /etc/hostname
echo '127.0.0.1    localhost' >> /etc/hosts
echo '127.0.0.1    aliyun0' >> /etc/hosts

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
                   -`                    root@aliyun0 
                  .o+`                   ------------ 
                 `ooo/                   OS: Arch Linux x86_64 
                `+oooo:                  Host: Alibaba Cloud ECS pc-i440fx-2.1 
               `+oooooo:                 Kernel: 6.8.7-arch1-1 
               -+oooooo+:                Uptime: 6 mins 
             `/:-:++oooo+:               Packages: 254 (pacman) 
            `/++++/+++++++:              Shell: bash 5.2.26 
           `/++++++++++++++:             Resolution: 1024x768 
          `/+++ooooooooooooo/`           Terminal: /dev/pts/0 
         ./ooosssso++osssssso+`          CPU: Intel Xeon Platinum 8269CY (2) @ 2.500GHz 
        .oossssso-````/ossssss+`         GPU: 00:02.0 Cirrus Logic GD 5446 
       -osssssso.      :ssssssso.        Memory: 93MiB / 422MiB 
      :osssssss/        osssso+++.
     /ossssssss/        +ssssooo/-                               
   `/ossssso+/:-        -:/+osssso+-                             
  `+sso+:-`                 `.-/+oso:
 `++:.                           `-/+/
 .`                                 `/
```

[https://limelight.moe/t/topic/6007](https://limelight.moe/t/topic/6007)  
[https://www.scarletdrop.cn/archives/14](https://www.scarletdrop.cn/archives/14)

## DNS

```Bash
ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
```

## bwg intall archlinux

```bash
curl -O https://mirror.adectra.com/archlinux/iso/2025.02.01/archlinux-bootstrap-2025.02.01-x86_64.tar.zst
dnf install zstd
tar -I zstd -xvf archlinux-bootstrap-2025.02.01-x86_64.tar.zst
```