---
title: archlinux install
author: wiloon
type: post
date: 2015-06-25T09:18:44+00:00
url: /?p=7821
categories:
  - Uncategorized
tags:
  - Archlinux

---
### Arch Linux Fast Installer
https://github.com/MatMoul/archfi

## 从U盘引导安装
download iso  
<http://mirrors.163.com/archlinux/iso/>

```bash
# 创建USB启动盘
#dd archlinux iso to usb
sudo dd bs=4M if=archlinux-2020.03.01-x86_64.iso of=/dev/sdx status=progress && sync

# boot with usb stick
```

### 设置网络
setup network with shell script https://gist.github.com/wiloon/xxxxxx

#### or  
<https://blog.wiloon.com/?p=9881>

```bash
# 给root设置密码
passwd

# 启动sshd
systemctl start sshd
# openssh  默认已安装, 没有的话 安装 一下 pacman -S openssh
# sshd已经配置允许root登录, 有问题的话, 去改一下配置文件/etc/ssh/sshd_config,  PermitRootLogin yes

# ssh to new system

# 查看当前的引导模式，uefi or bios
 ls /sys/firmware/efi/efivars
 # 如果提示文件不存在， 那么当前系统就不是efi引用的， 可能 是bios或CSM
```

### config pacman mirror
<https://blog.wiloon.com/?p=7501>

### pacman 更新， 不要用-Syu， -Syu有可能会把U盘写满。
```bash
pacman -Sy
```

## 分区并格式化硬盘
#### 用 parted 分区
<http://blog.wiloon.com/?p=8416>

#### 用 fdisk 分区
<http://blog.wiloon.com/?p=7609>

```bash
# Mount the partitions
mkdir /mnt/tmp
mount /dev/sdx3 /mnt/tmp
mkdir /mnt/tmp/boot
mount /dev/sdx1 /mnt/tmp/boot

pacstrap /mnt/tmp base linux linux-firmware
# if command not found, see http://www.wiloon.com/wordpress/?p=8443

# 建议使用UUID方式生成fstab和启动管理器配置
genfstab -p -U /mnt/tmp >> /mnt/tmp/etc/fstab
```
### 把网络配置文件复制到新系统
```bash
cp /etc/systemd/network/wifi.network  /mnt/tmp/etc/systemd/network/
```

```bash
arch-chroot /mnt/tmp

echo hostname0 > /etc/hostname

ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
pacman -S gvim
# Uncomment the needed locales(en_US.UTF-8, zh_CN.UTF-8) in /etc/locale.gen, then generate them with: locale-gen
vim /etc/locale.gen

en_US.UTF-8 UTF-8
zh_CN.UTF-8 UTF-8

locale-gen

# 文件设置全局有效的locale,没有的话新建一个文件。
vim /etc/locale.conf
LANG=en_US.UTF-8

## 如果是安装到U盘，需要修改mkinitcpio.conf
# 用 mkinitcpio -p linux创建 RAM Disk 前，在修改 /etc/mkinitcpio.conf，将 block 添加到紧挨 udev 的后面. 只有这样早期用户空间才能正确的装入模块。

# set root password
passwd

# install wpa_supplicant
pacman -S wpa_supplicant
```

### boot with UEFI

```bash
# boot with uefi
bootctl install
cd /boot/loader
pacman -S vim emacs
vim loader.conf

# loader.conf content
default arch
timeout 1

cd entries
vim arch.conf

# arch.conf content
title Archlinux
linux /vmlinuz-linux
initrd /initramfs-linux.img
# get PARTUUID via blkid, remove "" for PARTUUID
# 注意最后面的rw 不要漏掉!!!
options root=PARTUUID=xxx rw

:r !blkid
# uefi boot end
```

### boot with grub

<https://blog.wiloon.com/?p=15345>

```bash
useradd -m -s /bin/bash wiloon
passwd wiloon

pacman -S openssh sudo
systemctl enable sshd
chmod u+w /etc/sudoers
vim /etc/sudoers

wiloon ALL=(ALL) NOPASSWD: ALL

systemctl enable systemd-networkd
systemctl enable systemd-resolved.service

# 配置网络： https://blog.wiloon.com/?p=9881， /etc/systemd/network/eth.network， 否则有可能启动之后没有网络

systemctl enable fstrim.timer
# exit to iso
exit
cp /etc/wpa_supplicant/wpa_supplicant-*.conf /mnt/tmp/etc/wpa_supplicant
arch-chroot /mnt/tmp
systemctl enable wpa_supplicant@wlanx
exit
 poweroff
```

### 拔掉U盘开机

## archlinux init

<http://blog.wiloon.com/?p=8913>

* * *

https://wiki.archlinux.org/index.php/Install\_from\_existing_Linux
  
https://wiki.archlinux.org/index.php/Installation_guide
  
https://wiki.archlinux.org/index.php/Installing\_Arch\_Linux\_on\_a\_USB\_key
  
https://wiki.archlinux.org/index.php/Installing\_Arch\_Linux\_on\_a\_USB\_key_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)
  
http://www.linuxidc.com/Linux/2014-04/99749.htm
  
https://wiki.archlinux.org/index.php/Syslinux
  
https://wiki.archlinux.org/index.php/syslinux#Installation\_on\_BIOS

* * *

```bash
#uefi 可以直接启动archlinux, 不需要 bootloader
#Install a boot loader, e.g.syslinux
#check whather using mbr or gpt
blkid -s PTTYPE -o value /dev/sdx
mbr:dos

pacman -S syslinux
pacman -S gptfdisk

syslinux-install_update -i -a -m

#编辑/boot/syslinux/syslinux.cfg 把/dev/sdax 替换成uuid
使用UUID:
LABEL Arch
 MENU LABEL Arch Linux
 LINUX ../vmlinuz-linux
 APPEND root=UUID=3a9f8929-627b-4667-9db4-388c4eaaf9fa ro
 INITRD ../initramfs-linux.img</pre>

＃umount the usb disk and reboot

```