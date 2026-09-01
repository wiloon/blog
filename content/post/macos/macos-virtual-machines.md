---
title: "macOS Virtual Machines: Parallels Desktop, Fusion Pro, UTM"
author: "-"
date: 2026-08-31T16:47:52+08:00
lastmod: 2026-08-31T16:47:52+08:00
url: macos-virtual-machines
categories:
  - macOS
  - Desktop
tags:
  - macos
  - virtualization
  - parallels
  - vmware
  - utm
  - qemu
  - remix
  - AI-assisted
---

## 背景

Apple Silicon（M 系列）之后，Mac 上不能再用 Boot Camp 装 Windows。日常要跑另一套操作系统，只能走虚拟机。

选型时先分清两件事：

1. 宿主机和客户机是不是同一套 CPU 架构。同架构（Apple Silicon 上跑 ARM Linux / Windows 11 ARM）走硬件虚拟化，接近本机速度。跨架构（在 M 系列上跑完整的 x86 Windows / Linux）要做指令仿真，会慢很多。
2. 要的是「每天用 Windows 应用」，还是「偶尔起一台 Linux / 旧系统 / 别的架构」。

下面三款是目前 macOS 上最常见的选择。软件列表里的入口见 [macos apps](./macos-apps.md)。UTM 的具体操作（Gallery、9p 共享目录、Apple Virtualization、从 kernel 启动）见 [UTM](../other/utm.md)。QEMU 本身见 [QEMU](../linux/qemu.md)。

## 怎么选

- 每天要在 Mac 上用 Windows 应用（Office 插件、Visio、部分工程软件）：Parallels Desktop。它是目前 Microsoft 授权在 Apple Silicon 上跑 Windows 11 Pro / Enterprise 的方案，Coherence、剪贴板、文件夹共享、显卡加速都更完整。
- 不想付钱、能接受自己下 ISO / 配网卡、偶尔用 Windows 或经常跑 Linux：VMware Fusion Pro。2025 年 3 月起对个人、教育和商业用途都免费。
- 要开源、要仿真 x86 / 旧系统 / RISC-V 等、或只是起一台 ARM Linux：UTM。

三款都不包含 Windows 许可证。Windows 要单独激活。

## 对比

| 维度 | Parallels Desktop | VMware Fusion Pro | UTM |
| ---- | ----------------- | ----------------- | --- |
| 许可 | 订阅为主（也有 Standard 买断）；Windows 另购 | 2025-03 起免费（个人 / 教育 / 商业） | 开源免费；Mac App Store 有付费版（方便更新） |
| 下载 | 官网或 `brew install --cask parallels` | Broadcom Support Portal（Homebrew cask 已因需登录而下架） | 官网 / GitHub 或 `brew install --cask utm` |
| 技术支持 | 官方支持 | 免费版无 Broadcom 工单，靠文档和社区 | 社区 |
| Apple Silicon 同架构虚拟化 | 有（Windows 11 ARM、Linux ARM、macOS） | 有（Windows 11 ARM、Linux ARM） | 有（Apple Virtualization：Linux、macOS） |
| Apple Silicon 上跑完整 x86 客户机 | Pro 等版本有实验性仿真（限制多、很慢） | 不支持 | QEMU 仿真，支持面最广，同样慢 |
| Windows 11 ARM 集成 | 最好：向导安装、Coherence、共享文件夹、DirectX | 能跑；Windows ARM 上共享文件夹、3D、Unity 等仍缺 | 能跑，集成弱 |
| Linux | 常用发行版；Pro 资源上限更高 | 常用 ARM 发行版 | Gallery 预制镜像；也可用 Apple VF |
| 图形 | 商务 / 部分 3D 软件方向最完整 | Apple Silicon 上 Windows ARM 图形偏基础 | 一般弱于前两款 |
| 快照 / 克隆 | 有 | 有 | 有 |
| 适合谁 | 把 Windows 当日常桌面的人 | 要免费专业虚拟机、能自己配的人 | 折腾、仿真、开源栈 |

数字和版本会变，上面按 2026-08 的公开说明整理，买之前以官网为准。

## 虚拟化还是仿真

Apple 的 Virtualization / Hypervisor 框架只虚拟化同架构客户机。M 系列 Mac 上，Windows 11 ARM、ARM64 Linux、Apple Silicon 版 macOS 可以接近本机速度。

跨架构是另一条路：在 ARM 宿主机上模拟一台 x86 PC。UTM 用 QEMU 做这件事；Parallels Desktop 从 20.2 起在 Pro / Business / Enterprise 里提供实验性 x86 仿真。Fusion 在 Apple Silicon 上不能跑 x86 客户机操作系统。

日常 Windows 软件通常不必开完整 x86 虚拟机。先装 Windows 11 ARM，再用 Windows 自带的 Prism 翻译层跑多数 x86/x64 应用。完整 x86 客户机留给：必须装 Intel 版 Windows、旧安装介质、或 Prism 过不了的环境。

Parallels 这份实验性仿真限制很死：1 个 vCPU、内存上限约 8 GB、无 USB 直通、无声卡、无嵌套虚拟化；启动可能要数分钟。Windows 11 较新的 build（官方曾写 26100 及更新）还不支持。UTM 的 QEMU 模式限制少一些，速度同样不是日常办公水平。

## Parallels Desktop

面向「在 Mac 上把 Windows 当常用环境」。

要点：

- Microsoft 授权在 Apple Silicon 上运行 Windows 11 Pro / Enterprise。虚拟机软件本身不含 Windows 许可证，仍要自己激活。
- 向导可从 Microsoft 拉取 Windows 11 ARM 镜像。
- Coherence：Windows 窗口混在 macOS 桌面上，剪贴板、拖放、共享目录默认能用。
- 2026 年的 Desktop 27 只支持 Apple Silicon；Intel Mac 继续用 26 及更早版本。
- Standard 虚拟硬件上限较低（公开对比里常见 8 GB vRAM / 4 vCPU）。开发、多虚拟机、重图形一般用 Pro（上限高得多，并带命令行和高级网络）。
- 订阅能跟新的 macOS / Windows；买断通常锁在购买时的大版本。

代价是每年费用，以及把工作流绑在商业产品上。只是偶尔开一台 Linux，这笔钱通常不值。

官网：[Parallels Desktop](https://www.parallels.com/products/desktop/)；Windows 11 ARM 授权说明见 [Microsoft-authorized solution](https://www.parallels.com/products/desktop/microsoft-authorized-solution-windows-11-arm/)。

## VMware Fusion Pro

Intel 时代和 Parallels 并列的商业虚拟机。Broadcom 收购 VMware 之后，桌面产品线改过几次授权。

2025 年 3 月起，当前 Fusion Pro / Workstation Pro 对个人、教育和商业用途免费，不需要许可证密钥。官方 FAQ：[VMware Desktop Hypervisor FAQs](https://www.vmware.com/docs/desktop-hypervisor-faqs)。

实际使用要注意：

- 安装包从 Broadcom Support Portal 下，要注册账号并填出口合规信息。站内自动更新曾被关掉，新版本往往要手动下。
- 免费版没有 Broadcom 官方工单，问题走知识库和社区。
- 版本号改成半年一轮，例如 25H2、26H1。
- Apple Silicon 上只跑 ARM 客户机。Windows 11 ARM、常见 ARM Linux 可以；x86 客户机不行。
- Windows 11 ARM 的 VMware Tools 不完整：共享文件夹官方写明不支持，3D / Unity / 窗口自适应也缺。文件交换多用 SMB、拖放或拷贝粘贴。
- 嵌套虚拟化（例如 Windows 里的 WSL2）在 Apple Silicon 上不可用。

和 vSphere / Workstation 共用 VMDK、习惯 VMware 网络和快照的人，Fusion 仍然顺手。要的是「Windows 窗口嵌进 macOS、共享盘开箱即用」，它现在不如 Parallels。

## UTM

开源，包了一层 QEMU，并可选 Apple Virtualization Framework。官网：[UTM](https://mac.getutm.app/)。

两种后端差别很大：

- Apple Virtualization：同架构 Linux / macOS，速度快、占用低。Arch Linux ARM 这类场景应开这个，而不是 QEMU 仿真。
- QEMU：仿真多种 CPU（x86_64、ARM32、MIPS、PPC、RISC-V 等）。能在 M 系列上起完整 x86 系统，也适合旧系统或非主流架构；CPU 和磁盘都会慢一截。

Gallery 提供预制虚拟机（包括 Arch Linux ARM）。ARM 发行版常常是磁盘镜像而不是 Live ISO，创建时可能要「从 kernel / 镜像启动」，而不是「从 ISO 引导」。共享目录在 Linux 客户机里常见做法是 9p。这些步骤写在 [UTM](../other/utm.md)。

Windows 能装，但没有 Parallels 那种 Coherence 和显卡栈，不适合把 Windows 当主力桌面。Mac App Store 上的 UTM 收费，功能与官网免费版接近，钱主要换自动更新。

## 和 VirtualBox 的关系

[VirtualBox](../linux/virtualbox.md) 在 Intel Mac / Windows / Linux 上仍常见。Apple Silicon 上的支持长期落后于上面三款，日常选 Mac 虚拟机时一般不再把它和 Parallels / Fusion / UTM 放在同一优先级。

Linux 开发如果主要是容器而不是完整桌面，还可以看 OrbStack、Lima 这类工具，它们不是通用 Type-2 虚拟机，这里不展开。

## 参考

- [UTM 官网](https://mac.getutm.app/)
- [VMware Desktop Hypervisor FAQs](https://www.vmware.com/docs/desktop-hypervisor-faqs)（Fusion 免费范围、下载与支持）
- [Download and license VMware Desktop Hypervisor](https://knowledge.broadcom.com/external/article/368667/download-and-license-information-for-vmw.html)
- [Compatibility considerations for Arm guests in Fusion](https://knowledge.broadcom.com/external/article/315602)
- [Parallels：Microsoft-authorized Windows 11 on Apple silicon](https://www.parallels.com/products/desktop/microsoft-authorized-solution-windows-11-arm/)
- [Parallels KB：Apple Silicon 上的 x86 仿真](https://kb.parallels.com/en/130217)
