---
title: "UTM: Virtual Machines on macOS"
author: "-"
date: 2013-02-22T04:28:56+00:00
lastmod: 2026-08-31T16:47:52+08:00
url: utm
categories:
  - macOS
  - Desktop
tags:
  - macos
  - utm
  - qemu
  - remix
  - AI-assisted
---

## 简介

[UTM](https://mac.getutm.app/) 是 macOS / iOS 上的开源虚拟机，底层是 QEMU，也可以改用 Apple Virtualization Framework。

和 Parallels Desktop、VMware Fusion Pro 的对比见 [macOS Virtual Machines](../macos/macos-virtual-machines.md)。同架构 Linux 应优先开 Apple Virtualization，不要用 QEMU 仿真。

## Gallery 里开 Arch Linux ARM

browse UTM gallery > archlinux arm > open in UTM

默认用户 / 密码：`root` / `root`

## 共享目录（9p）

在 Linux 客户机里：

```bash
sudo mkdir -p /mnt/share
sudo mount -t 9p -o trans=virtio hostshare /mnt/share
```

## Use Apple Virtualization

用 Apple 自家的虚拟化框架（Apple Virtualization Framework）跑虚拟机，而不是 QEMU 仿真（emulation）：

- 性能更高
- 资源占用更少

适合 Apple Silicon 上的 ARM Linux / macOS。跨架构（例如在 M 系列上跑完整 x86 系统）仍然只能走 QEMU。

## boot from kernel image

勾选这个之后就不会出现 boot from iso image 的选项。

Arch Linux ARM 不提供 ISO。

ARM 架构设备的安装方式和 PC 不同：

- x86_64（标准 PC）：通常用 Live ISO 引导，再手动安装
- ARM 设备（如 Raspberry Pi、Pine64 等）：没有传统 BIOS/UEFI 通用引导机制，一般是预制系统镜像，直接刷到 SD 卡或 eMMC

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-08-31 | 标题改为含英文；分类改为 macOS / Desktop；补充与 Parallels / Fusion 对比文的链接；整理 Apple Virtualization 与 kernel 启动说明 | 原笔记过短，且站内缺少 macOS 虚拟机选型文档 |
