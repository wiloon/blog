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

- openssh
- ssh key
- neovim
- ln -s ... vi... vim to nvim
- sudo nopassword for wiloon
- python for ansible
- pacman -Syu
- yay for telegraf

after install mesa, to confirm it works 被正确加载

```bash
glxinfo | grep "OpenGL renderer"
# OpenGL renderer string: AMD Radeon Graphics (radeonsi, phoenix, LLVM 19.1.7, DRM 3.61, 6.14.9-arch1-1)
# 看内核模块是否加载成功
lsmod | grep amdgpu
vulkaninfo | grep "deviceName"
```

after install vkcube

```bash
# 测试 vulkan
su - wiloon
echo $WAYLAND_DISPLAY
# wayland-0
# vkcube 默认会尝试用 xlib（X11）作为窗口系统接口, 如果你想要使用 Wayland, 需要指定 --wsi wayland
vkcube --wsi wayland
```

### before ansible script

```bash
pacman -Syu && pacman -S git ansible
```

### clone ansible script

```bash
git clone git@github.com:wiloon/ansible.git
```

### config network by systemd-networkd

[http://blog.wiloon.com/?p=9881](http://blog.wiloon.com/?p=9881)

pacman -Syu

### create user and set password

yay 不能在root下执行, 需要新建个用户
[http://blog.wiloon.com/?p=911](http://blog.wiloon.com/?p=911)

ln -s /usr/bin/vim /usr/bin/vi
visudo

/etc/sudoer.d/wiloon.conf

```bash
wiloon ALL=(ALL) NOPASSWD: ALL
```

```bash
# install and enable sshd

pacman -S openssh
systemctl start sshd
systemctl enable sshd
```

connect to new system with user0 via ssh

- ntp, chrony

[http://blog.wiloon.com/ntp](http://blog.wiloon.com/ntp)

- 监控, telegraf

### install app

- zsh, oh-my-zsh
    install and switch to zsh - oh-my-zsh
  
[http://blog.wiloon.com/zsh](http://blog.wiloon.com/zsh)

- 安装图形界面 kde 或 xfce4

#### install kde

[http://blog.wiloon.com/kde](http://blog.wiloon.com/kde)

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

[http://blog.wiloon.com/?p=8940](http://blog.wiloon.com/?p=8940)

### restart to desktop to continue

### wenquanyi 中文字体

sudo pacman -S wqy-microhei

## font for terminal

sudo pacman -S ttf-inconsolata
sudo pacman -S chromium
yay -S google-chrome

- yay
[http://blog.wiloon.com/?p=7953](http://blog.wiloon.com/?p=7953)

### 输入法

- fcitx
[http://blog.wiloon.com/?p=9650](http://blog.wiloon.com/?p=9650)

#### 输入法ibus

[http://www.wiloon.com/?p=7507](http://www.wiloon.com/?p=7507)

#### for right click extrace package

pacman -S file-roller
  
xfce4 date time plugin format

Date Format: Custom Format

```r
%b %d%n%V %a%n%R
```

Time Format: Custom Format

```r
%a %R
```

[http://goodies.xfce.org/projects/panel-plugins/xfce4-datetime-plugin](http://goodies.xfce.org/projects/panel-plugins/xfce4-datetime-plugin)

### sddm

```bash
systemctl enable sddm
```

removed "SigLevel = RecquiredPackage" from /etc/pacman.conf and now it's O.K.

pacman -S binutils
  
pacman -S patch
xmarks
ntfs-3g
mount -t ntfs-3g /dev/sda5 /mnt

### 重启

```bash
reboot
```

## archlinux 中文支持

```bash
vim /etc/locale.gen
en_US.UTF-8 UTF-8
zh_CN.UTF-8 UTF-8

locale-gen

/etc/locale.conf文件设置全局有效的locale
LANG=en_US.UTF-8

# 中文字体 
sudo pacman -S wqy-microhei

locale -a 来显示当前Linux系统支持的所有的语言环境。

```
## amd driver

```bash
sudo pacman -S xf86-video-amdgpu
sudo pacman -S vulkan-radeon
```