---
title: "Pixelbook: 用 MrChromebox 固件安装 Linux"
author: "-"
date: 2018-02-04T09:22:37+00:00
lastmod: 2026-08-09T11:43:16+08:00
url: pixelbook
categories:
  - Linux
tags:
  - chromeos
  - firmware
  - coreboot
  - remix
  - AI-assisted
aliases:
  - /p11818/
---

## 2018 年的旧方法已经过时

早年这篇文章记录的是开发者模式 + [crouton](https://github.com/dnschneid/crouton) 的方案，crouton 项目已经停止维护；后来 ChromeOS 自带的 Crostini 也只是容器化的 Linux，跑在 ChromeOS 内部，不算真正独立的系统。

2026 年推荐的做法是刷 [MrChromebox](https://mrchromebox.tech/) 提供的 coreboot 固件，把 Pixelbook（代号 `eve`）变成一台标准 UEFI x86_64 笔记本，然后像普通 PC 一样从 U 盘装发行版。下面记录完整流程。

## 进入开发者模式

同时按住 Esc、Refresh、电源键，直到出现 Recovery Mode（提示插入 U 盘的界面），这时按 Ctrl-D（不需要插 U 盘，插了反而会自动进入恢复模式）。

开启开发者模式会清空设备上的数据。

## MrChromebox 固件：两种模式

MrChromebox 固件有两种刷法：

- **RW_LEGACY**：保留 ChromeOS，做双系统引导
- **UEFI Full ROM**：彻底替换固件，刷完之后就是一台标准 UEFI 笔记本，可以直接用任意发行版的安装 U 盘

装 Linux 用，推荐直接选 **Full ROM**，体验最接近普通 PC，也省去后续维护 ChromeOS 的麻烦。

## 关闭硬件写保护

刷 Full ROM 之前必须先关闭主板的硬件写保护（Firmware Write Protect），Pixelbook 没有软件开关，只有两种办法：

1. **拆机**，断开主板上的电池排线
2. **用 SuzyQ 调试线**，走 CCD（Case-Closed Debugging，不拆机调试）流程

不想拆机的话，SuzyQ 线是更省心的方案。

### SuzyQ 调试线是什么

SuzyQ（也叫 SuzyQable）是 Google 设计的一种特制 USB-C 调试配件线。普通 USB-C 数据线两端都是"设备"角色，
SuzyQ 的其中一端在 CC1/CC2 引脚上接了 22kΩ 和 56kΩ 的识别电阻，让主机把它识别成 "debug accessory mode"，从而暴露出芯片内部的调试通道。

Pixelbook 内置了 Google 的安全芯片（Cr50），插上 SuzyQ 线之后，可以直接通过 `gsctool` 跟这颗芯片通讯，执行开关 CCD、读写权限等操作——包括不拆机关闭硬件写保护。

获取方式：

- **购买**：官方渠道基本停产，现在主要靠社区卖家出的仿制板/成品线（搜 "SuzyQable" 或 "USB-C debug cable" 能找到）
- **DIY**：用两根普通 USB-C 数据线 + 一块简单的转接板即可，核心就是在其中一端的 CC1/CC2 对 GND 各接一个 56kΩ/22kΩ 电阻。
- 社区有现成的开源打样文件，比如 [erichVK5/erichVK5-suzy-Q-cable-v1](https://github.com/erichVK5/erichVK5-suzy-Q-cable-v1)

使用流程：

```bash
# in crosh/shell, developer mode required

# 1. open CCD on the Cr50 chip
# takes a few minutes, press the power button when prompted
gsctool -a --ccd_open

# 2. plug in the SuzyQ cable to the debug port, then check capabilities
# OverrideWP / FlashAP should read "Always" instead of "IfOpened"
gsctool -a -I

# 3. confirm write protect is disabled
crossystem wpsw_cur
```

确认写保护关闭之后，就不需要拆机了，可以直接进入下一步刷固件。

## 刷 UEFI Full ROM 固件

```bash
# in crosh/shell, developer mode required
cd
curl -LO mrchromebox.tech/firmware-util.sh && sudo bash firmware-util.sh
```

脚本菜单里选 UEFI (Full ROM) 固件，刷完重启，看到 coreboot 的开机 logo 就说明成功了，接下来可以从 U 盘启动任意 Linux 发行版的安装介质。

## 装哪个发行版

刷完 Full ROM 之后硬件层面就是标准 x86_64 了，理论上什么发行版都能装，但 Pixelbook（2017 年的硬件）在触摸屏、键盘背光、待机唤醒、音频这些细节上，主流发行版的新内核比较容易开箱可用：

- **Fedora / Ubuntu**：内核新、上游驱动跟进快，推荐图省心的话选这两个
- **Arch**：细节需要自己动手调，装法见 [Pixelbook 上安装 Archlinux](./archlinux-on-pixelbook.md)

GalliumOS 这类专门给 Chromebook 做的发行版已经在 2022 年左右停止维护，不建议再用。

## 参考

- [MrChromebox Firmware Utility Script](https://docs.mrchromebox.tech/docs/fwscript.html)
- [MrChromebox: Disabling Firmware Write Protection](https://docs.mrchromebox.tech/docs/firmware/wp/disabling.html)
- [ArchWiki: Chrome OS devices/Custom firmware](https://wiki.archlinux.org/title/Chrome_OS_devices/Custom_firmware)
- [Chromium OS docs: Case Closed Debugging](https://chromium.googlesource.com/chromiumos/platform/ec/+/fe6ca90e/docs/case_closed_debugging_cr50.md)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-08-09 | 文件从 `content/post/cs/pixelbook.md` 移到 `content/post/linux/pixelbook.md`；分类由 `chrome` 改为 `Linux`；全文重写为 MrChromebox Full ROM 固件方案，新增 SuzyQ 调试线说明；删除已过时的 crouton 内容 | crouton 停止维护，2018 年方法已过时；2026 年推荐用 MrChromebox 刷固件后装标准 Linux |
