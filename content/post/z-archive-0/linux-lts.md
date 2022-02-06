---
title: archlinux 安装 linux-lts 内核
author: "-"
date: 2022-02-06 01:19:31
url: lts
categories:
  - Linux
tags:
  - remix

---
## archlinux 安装 linux-lts 内核

- 检查 /boot 目录是否已经挂载
- 挂载 /boot `mount /dev/sda1 /boot`
- 安装 linux-lts `pacman -S linux-lts`
- 把内核注册到 bootloader， `grub-mkconfig -o /boot/grub/grub.cfg`
- 重启 `reboot`
- 重启后 默认选项 "Arch Linux" 对应的内核应该已经是 linux-lts了， 也可以选择 Advanced options for Arch Linux, 能看到具体的内核列表。
- 使用 linux-lts 内核启动
- 确认一下当前使用的内核版本 `uname -r`
- 删除非lts 内核 `pacman -R linux`
- 更新 bootloader `grub-mkconfig -o /boot/grub/grub.cfg`

### LTS 内核的优点

- 稳定
新版本内核偶尔会有各种奇怪的问题，比如 5.16.5.arch1-1 `modprobe br_netfilter` 报错找不到模块。

<https://averagelinuxuser.com/the-lts-kernel-in-arch-linux/>
