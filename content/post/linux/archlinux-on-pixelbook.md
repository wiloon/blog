---
title: "Pixelbook 上安装 Archlinux (MrChromebox Full ROM)"
author: "-"
date: 2018-09-08T04:24:14+00:00
lastmod: 2026-08-09T11:43:16+08:00
url: archlinux-on-pixelbook
categories:
  - Linux
tags:
  - archlinux
  - chromeos
  - firmware
  - remix
  - AI-assisted
aliases:
  - /p12641/
---

## 前提：先刷好 Full ROM 固件

这篇文章原本记录的是 Crostini 容器里跑 Archlinux 的方法，Crostini 只是 ChromeOS 内部的容器化 Linux，性能和硬件访问都受限。2026 年推荐先按 [Pixelbook: 用 MrChromebox 固件安装 Linux](./pixelbook.md) 完成开发者模式、关闭硬件写保护（拆机或用 SuzyQ 调试线）、刷入 MrChromebox 的 Full ROM UEFI 固件。刷完之后 Pixelbook（代号 `eve`）就是一台标准 UEFI x86_64 笔记本，可以直接从 U 盘装 Archlinux，不再依赖 ChromeOS。

## 通用安装步骤

分区、`pacstrap`、bootloader 这些通用步骤跟普通 PC 装 Arch 完全一样，参考 [archlinux install](./archlinux-install.md)，这篇只记录 Pixelbook 硬件相关、跟通用步骤不一样的地方。

## Pixelbook 硬件专属问题

Pixelbook 是 2017 年的硬件，装上主流发行版的新内核（参考 [pixelbook.md](./pixelbook.md) 里 Fedora / Ubuntu 优先的建议）大多能直接工作，但自己装 Arch 用较老的内核配置时，以下几个点容易遇到问题，遇到时优先查这些方向：

- **触摸屏 / 触控板**：老款 Chromebook 常用的触控芯片在原厂内核之外的社区补丁里支持更全，可以参考 [tsowell/linux-samus](https://github.com/tsowell/linux-samus) 和 [yusefnapora/pixelbook-linux](https://github.com/yusefnapora/pixelbook-linux) 这两个针对 Chromebook 硬件整理的内核补丁/配置仓库
- **音频**：ChromeOS 自己用的是 cras（Chromium Audio Server）驱动这套硬件，标准 ALSA/PulseAudio 在部分型号上需要额外配置才能出声，同样可以参考上面两个仓库里的音频配置部分
- **键盘背光 / 待机唤醒**：偶发问题，社区论坛（如 [chrultrabook 论坛](https://forum.chrultrabook.com/)）能搜到具体机型的报告和修复办法

这些细节变化比较快，遇到问题建议直接搜对应内核版本 + `eve` 关键字，而不是死抠某一份补丁。

## 旧方法（Crostini，仅在保留 ChromeOS 时用）

如果不想动固件、想继续用 ChromeOS，也可以用它自带的 Crostini（设置 > Linux > 启用）跑一个基于容器的 Archlinux 环境，但那不是独立系统，性能和硬件访问都有限，遇到 GPU、USB 外设之类的需求会比较麻烦，这里不再展开，只在维护记录里存档旧方法已废弃这件事。

## 参考

- [ArchWiki: Installation guide](https://wiki.archlinux.org/index.php/Installation_guide)
- [ArchWiki: Chrome OS devices/Custom firmware](https://wiki.archlinux.org/title/Chrome_OS_devices/Custom_firmware)
- [tsowell/linux-samus](https://github.com/tsowell/linux-samus)
- [yusefnapora/pixelbook-linux](https://github.com/yusefnapora/pixelbook-linux)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-08-09 | 文件从 `content/post/inbox/archlinux-on-pixelbook.md` 移到 `content/post/linux/archlinux-on-pixelbook.md`；分类由 `Inbox` 改为 `Linux`；全文重写为 MrChromebox Full ROM 固件之后的原生安装方案；删除已过时的 Crostini 容器操作细节 | Crostini 容器方案功能受限，2026 年推荐刷固件后装原生 Arch |
