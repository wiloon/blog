---
author: "-"
date: 2026-05-05T14:02:11+08:00
lastmod: 2026-06-04T20:53:59+08:00
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
| 豆包输入法 | — | AI 语音输入；无 brew cask，安装见下文 |

`brew install --cask doubao` 安装的是豆包 AI 聊天客户端，不是输入法。

### 豆包输入法

- 官网：[shurufa.doubao.com](https://shurufa.doubao.com)
- 手动安装：官网下载 `DoubaoImeInstaller_*.zip`，双击安装器按 GUI 引导完成
- Ansible 静默安装（写入 `/Library/Input Methods/`，不弹 GUI 安装器）：

  ```bash
  cd homelab/workstation   # w10n-config 仓库
  task install-doubao-ime  # 需输入 sudo 密码
  ```

  Playbook 从官网 API 拉取最新包并执行包内 `install.sh`。

装好后还需在系统设置中手动完成：

1. 键盘 → 输入法：添加「豆包输入法」
2. 隐私与安全性：为豆包输入法开启辅助功能；使用语音时需允许麦克风
3. 若菜单栏或切换异常，注销或重启后再试

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
