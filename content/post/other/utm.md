---
title: UTM
author: "-"
date: 2013-02-22T04:28:56+00:00
url: utm
categories:
  - Linux
tags:
  - reprint
  - remix
---

## UTM

browse utm gallery> archlinux arm> open in utm

archlinux arm default user/password: root/root

```bash
sudo mkdir -p /mnt/share
sudo mount -t 9p -o trans=virtio hostshare /mnt/share

```

---

## Use Apple Virtualization

使用 Apple 自家的 虚拟化框架（Apple Virtualization Framework） 来运行虚拟机，而不是使用传统的仿真（emulation）技术。
性能更高
资源占用更少

## boot from kernel image

勾选这个之后就不会出现 boot from iso image 的选项了

archlinux arm 不提供 iso

ARM 架构设备的安装方式与 PC 不同
x86_64 架构（标准 PC）：通常使用 Live ISO 镜像引导电脑，然后手动安装系统。

ARM 设备（如 Raspberry Pi、Pine64 等）：没有传统 BIOS/UEFI 通用引导机制，因此需要预制好系统镜像，直接刷写到 SD 卡或 eMMC 上。
