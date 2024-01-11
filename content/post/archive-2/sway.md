---
title: sway
author: "-"
date: 2016-02-26T18:51:16+00:00
url: sway
categories:
  - Linux
tags:
  - reprint
  - remix
---
## sway

virtualbox 里的 sway

virtualbox 窗口在不同分辨率的显示器之间切换时花屏, 剪贴板不好用, 窗口不能自动缩放 2024-01-08T08:17:03+08:00

## fedora sway

1. download Fedora Sway Spin iso
2. virtualbox 配置显存128, 3D加速
3. 用 iso 启动后 win + enter 打开 terminal
4. 用 text mode 安装 liveinst --text

fedora disable firewall

```Bash
sudo systemctl stop firewalld
# replace dnf mirror with 163
dnf upgrade --refresh
dnf install kernel-headers
```

--

## archlinux + sway

virtualbox guest addition failed to start

```Bash
sudo pacman -S sway
sudo pacman -S swaylock swayidle swaybg
sudo pacman -S dmenu
# install yay
yay -S wmenu

sudo pacman -S foot
sudo pacman -S polkit

```

virtualbox 虚拟机要打开 3D 加速

```Bash
# 配置环境变量
vim .bashrc
export WLR_NO_HARDWARE_CURSORS=1

# 登录后直接执行 sway
sway
```

