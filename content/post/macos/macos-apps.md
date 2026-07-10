---
author: "-"
date: 2026-05-05T14:02:11+08:00
lastmod: 2026-07-10T11:11:06+08:00
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

跨平台常用软件统一维护于 [my apps](my-apps)，本文只记录 macOS 专属工具。

## 说明

- `brew` — `brew install <name>`
- `cask` — `brew install --cask <name>`

## Essentials

跨平台工具见 [my apps](my-apps)，以下为 macOS 专属推荐：

| app | install | notes |
| --- | --- | --- |
| iterm2 | cask:iterm2 | 功能强大的 terminal |
| stats | cask:stats | 任务栏系统资源监控 |
| itsycal | cask:itsycal | 任务栏日历（显示周数） |
| tunnelblick | cask:tunnelblick | OpenVPN GUI 客户端 |
| Logi Options+ | cask:logi-options-plus | Logitech 键鼠配置工具 |
| Ice | cask:jordanbaird-ice@beta | 菜单栏图标管理、隐藏与分组 |

## Input Method

| app | install | notes |
| --- | --- | --- |
| 豆包输入法 | — | AI 语音输入，详见 [豆包输入法](./doubao-ime.md) |
| Squirrel（鼠须管） | cask:squirrel | RIME 引擎输入法，详见 [Squirrel（鼠须管）](./squirrel-rime.md) |

`brew install --cask doubao` 安装的是豆包 AI 聊天客户端，不是输入法。

## Productivity

| app | install | notes |
| --- | --- | --- |
| CleanMyMac X | — | 系统清理（官网购买） |
| Bob | cask:bob | 翻译/词典 |
| Itsycal | cask:itsycal | 任务栏日历，显示周数 |
| Stats | cask:stats | 任务栏 CPU/内存/网络监控 |
| Shottr | cask:shottr | 截图+标注+OCR，轻量快速 |
| Monosnap | cask:monosnap | 截图+标注 |
| RealVNC Viewer | cask:vnc-viewer | 远程桌面 |

## Terminal

| app | install | notes |
| --- | --- | --- |
| iterm2 | cask:iterm2 | macOS 最流行的 terminal |

## VPN

| app | install | notes |
| --- | --- | --- |
| Tunnelblick | cask:tunnelblick | OpenVPN GUI，macOS 专属 |

## Graphics / Design

| app | install | notes |
| --- | --- | --- |
| Sketch | — | 矢量绘图（官网购买） |

## References

- [Homebrew](https://brew.sh)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-09 | 新增 Squirrel（鼠须管）输入法条目及安装/五笔配置说明 | 补充 RIME 输入法方案，与豆包输入法并列 |
| 2026-07-10 | 豆包输入法、Squirrel（鼠须管）详细内容拆分至独立文档 [豆包输入法](./doubao-ime.md)、[Squirrel（鼠须管）](./squirrel-rime.md)，本文仅保留简介 | 保持本文简短，详细内容按 App 独立成文 |
