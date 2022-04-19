---
title: archlinux init
author: "-"
date: 2016-04-21T15:26:01+00:00
url: archlinux/init

categories:
  - inbox
tags:
  - reprint
---
## archlinux init

### before ansible script

   pacman -Syu && pacman -S git ansible

### clone ansible script

    git clone git@github.com:wiloon/ansible.git

### config network by systemd-networkd

<http://blog.wiloon.com/?p=9881>

### config pacman mirror

<https://blog.wiloon.com/?p=7501>
pacman -Syu

### create user and set password

yay 不能在root下执行, 需要新建个用户
<http://blog.wiloon.com/?p=911>

/etc/sudoer.d/wiloon.conf

    wiloon ALL=(ALL) NOPASSWD: ALL

ln -s /usr/bin/vim /usr/bin/vi
visudo

    wiloon ALL=(ALL) NOPASSWD: ALL

### install and enable sshd

pacman -S openssh
systemctl start sshd
systemctl enable sshd

# connect to new system with user0 via ssh

### ntp, chrony

<http://blog.wiloon.com/?p=10869>

- 监控, telegraf

### install app

- zsh, oh-my-zsh
    install and switch to zsh - oh-my-zsh
  
<http://blog.wiloon.com/zsh>

- 安装图形界面 kde 或 xfce4

#### install kde

<http://blog.wiloon.com/kde>

#### xfce4

```bash
# install xfce4

sudo pacman -S xorg-server
# sudo pacman -S xorg #includes Xorg server,  xorg-apps
sudo pacman -S xf86-video-vesa
sudo pacman -S xf86-video-intel # for intel GPU
sudo pacman -S xf86-video-fbdev #for hyper v
sudo pacman -S xfce4
sudo pacman -S xfce4-goodies

startxfce4
```

##### 登录后自动启动xfce4

登录shell后自动启动xfce4

<http://blog.wiloon.com/?p=8940>

### restart to desktop to continue

### wenquanyi 中文字体

sudo pacman -S wqy-microhei
# font for terminal
sudo pacman -S ttf-inconsolata
sudo pacman -S chromium
yay -S google-chrome

- yay
<http://blog.wiloon.com/?p=7953>

### 输入法

- fcitx
<http://blog.wiloon.com/?p=9650>

#### 输入法ibus

<http://www.wiloon.com/?p=7507>

#### for right click extrace package

pacman -S file-roller
  
# xfce4 date time plugin format #%b %d%n%V %a%n%R
<http://goodies.xfce.org/projects/panel-plugins/xfce4-datetime-plugin>

# for virtualbox

在virtual box 内安装的archlinux, 需要安装 virtualbox-guest-utils, 可以获得更流畅的图形界面,如virtual的无缝模式。
  
<https://wiki.archlinux.org/index.php/VirtualBox>
<https://bbs.archlinux.org/viewtopic.php?id=118986>

```

### sddm
    systemctl enable sddm

removed "SigLevel = RecquiredPackage" from /etc/pacman.conf and now it's O.K.

pacman -S binutils
  
pacman -S patch
xmarks
ntfs-3g
mount -t ntfs-3g /dev/sda5 /mnt

### 重启
    reboot
