---
author: "-"
date: 2026-05-05T14:02:11+08:00
lastmod: 2026-09-13T13:18:10+08:00
title: macos apps
url: macos-apps
categories:
  - Desktop
tags:
  - original
  - macos
  - AI-assisted
---

## macOS Apps

跨平台常用软件统一维护于 [my apps](../my-apps.md)，本文只记录 macOS 专属工具。

## 说明

- `brew` — `brew install <name>`
- `cask` — `brew install --cask <name>`

## Essentials

跨平台工具见 [my apps](../my-apps.md)，以下为 macOS 专属推荐：

| app           | install                   | notes                      |
| ------------- | ------------------------- | -------------------------- |
| iterm2        | cask:iterm2               | 功能强大的 terminal        |
| stats         | cask:stats                | 任务栏系统资源监控         |
| itsycal       | cask:itsycal              | 任务栏日历（显示周数）     |
| tunnelblick   | cask:tunnelblick          | OpenVPN GUI 客户端         |
| Logi Options+ | cask:logi-options-plus    | Logitech 键鼠配置工具      |
| Ice             | cask:jordanbaird-ice@beta | 菜单栏图标管理、隐藏与分组 |
| KeepingYouAwake | cask:keepingyouawake      | 菜单栏咖啡杯，防止系统休眠 |

## Input Method

| app                | install       | notes                                                          |
| ------------------ | ------------- | -------------------------------------------------------------- |
| 豆包输入法         | —             | AI 语音输入，详见 [豆包输入法](./doubao-ime.md)                |
| Squirrel（鼠须管） | cask:squirrel | RIME 引擎输入法，详见 [Squirrel（鼠须管）](./squirrel-rime.md) |

`brew install --cask doubao` 安装的是豆包 AI 聊天客户端，不是输入法。

## Productivity

| app            | install         | notes                   |
| -------------- | --------------- | ----------------------- |
| CleanMyMac X   | —               | 系统清理（官网购买）    |
| Bob            | cask:bob        | 翻译/词典               |
| Shottr         | cask:shottr     | 截图+标注+OCR，轻量快速 |
| Monosnap       | cask:monosnap   | 截图+标注               |
| RealVNC Viewer | cask:vnc-viewer | 远程桌面                |

## Screen Recording

| app      | install | notes                                      |
| -------- | ------- | ------------------------------------------ |
| Recordly | —       | 开源录屏与编辑器，适合演示视频；需 macOS 14+ |

官方 Homebrew 未收录 `recordly`。仓库里有 cask 文件，但公开 tap 尚未发布，`brew install --cask recordly` 不可用。从 [GitHub Releases](https://github.com/webadderallorg/Recordly/releases) 下载对应架构的 `.dmg` 安装。项目主页：[Recordly](https://github.com/webadderallorg/Recordly)。

## Terminal

| app    | install     | notes                   |
| ------ | ----------- | ----------------------- |
| iterm2 | cask:iterm2 | macOS 最流行的 terminal |

## Virtualization

Mac 上跑 Windows / Linux 虚拟机，三款常见软件的对比见 [macOS Virtual Machines](./macos-virtual-machines.md)。UTM 的具体操作见 [UTM](../other/utm.md)。

| app               | install            | notes                                      |
| ----------------- | ------------------ | ------------------------------------------ |
| Parallels Desktop | cask:parallels     | 付费；Windows 日常使用最省事                 |
| VMware Fusion Pro | —                  | Broadcom 门户下载；2025-03 起免费            |
| UTM               | cask:utm           | 开源；Apple Virtualization 或 QEMU 仿真     |

## VPN

| app         | install          | notes                   |
| ----------- | ---------------- | ----------------------- |
| Tunnelblick | cask:tunnelblick | OpenVPN GUI，macOS 专属 |

## Graphics / Design

| app    | install | notes                |
| ------ | ------- | -------------------- |
| Sketch | —       | 矢量绘图（官网购买） |

## References

- [Homebrew](https://brew.sh)

## 维护记录

| 时间       | 修改内容                                                                                                                                             | 原因                                           |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| 2026-07-09 | 新增 Squirrel（鼠须管）输入法条目及安装/五笔配置说明                                                                                                 | 补充 RIME 输入法方案，与豆包输入法并列         |
| 2026-07-10 | 豆包输入法、Squirrel（鼠须管）详细内容拆分至独立文档；移除 `Productivity` 中重复的 `Itsycal`、`Stats` 条目；将 `my apps` 站内链接改为相对 `.md` 路径 | 保持本文简短，避免重复推荐，并统一站内链接写法 |
| 2026-08-31 | 新增 Virtualization 小节，链到 Parallels / Fusion / UTM 对比文 | 补 macOS 虚拟机选型入口 |
| 2026-09-04 | Essentials 新增 KeepingYouAwake | 补菜单栏防休眠工具 |
| 2026-09-13 | 新增 Screen Recording 小节，记录 Recordly | 补充开源录屏/编辑器，并说明官方 brew 未收录 |
