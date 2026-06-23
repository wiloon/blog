---
title: Cursor
author: "-"
date: 2026-06-23T13:46:37+08:00
lastmod: 2026-06-23T13:46:37+08:00
url: cursor
categories:
  - Linux
  - AI
tags:
  - cursor
  - linux
  - archlinux
  - appimage
  - aur
  - remix
  - AI-assisted
---

## 背景

Arch Linux 工作站上我同时保留了两套 Cursor：**AUR 的 `cursor-bin`** 和 **官方 AppImage**。不是重复安装玩，而是两条更新通道各管一件事——AUR 省心，AppImage 跟官网更快。

## 为什么装两份

最初用 AUR 安装 `cursor-bin`，日常 `paru -Syu` 就能升级，和系统其他包一起维护。但 AUR 版本依赖上游维护者跟进官方发布，**往往比官网慢几天到一两周**。想试用新功能或修 bug 时，等 AUR 更新会比较被动。

Linux 版 Cursor 也有应用内自动更新（Help → Check for Updates），但我这边用起来不太稳，偶尔报错。所以另装了一份官方 AppImage，需要新版本时从官网拉，比等 AUR 或碰运气点内置更新更可控。

两套安装**共用** `~/.config/Cursor` 和 `~/.cursor`，配置、扩展、MCP 设置不用搬。约束是**同一时刻只开一个版本**——切换前先完全退出当前实例。

## stable 与 latest 发布通道

Cursor 官方下载 API 用 `releaseTrack` 区分通道（Linux AppImage 脚本安装靠这个接口）：

```text
https://www.cursor.com/api/download?platform=linux-x64&releaseTrack=stable|latest
```

返回 JSON，含 `downloadUrl`、`version` 等字段。论坛里也有人确认过这个接口。

| 通道 | 定位 | 说明 |
| ---- | ---- | ---- |
| **stable** | 保守、生产向 | 官方认为足够稳、适合大多数人默认用的构建；更新节奏较慢 |
| **latest** | 官网最新正式版 | 下载 CDN 上当前最新的正式发布，通常是比 stable 更新的 patch |

两者都是**正式发布构建**，不是每日实验版。差别在发布节奏：stable 更保守，latest 更快拿到新 patch。

实测时（2026-06-23）stable 为 `3.8.11`，latest 为 `3.8.22`，相差多个小版本。

应用内还有另一套更新设置（`Ctrl+Shift+J` → Beta）：**Default**、**Early Access**、**Nightly**。那是应用内自动更新通道；下载 API 的 `stable` / `latest` 主要给 **Linux 手动 / 脚本安装**用，和应用内三个名字**不是一一对应**。API 目前实测只有 `stable` 和 `latest` 可用。

查询示例：

```bash
# stable
curl -sSL "https://www.cursor.com/api/download?platform=linux-x64&releaseTrack=stable" | jq .

# latest
curl -sSL "https://www.cursor.com/api/download?platform=linux-x64&releaseTrack=latest" | jq .
```

我本地 Ansible playbook 默认走 `stable`；需要更快跟新时改 `releaseTrack=latest`，或手动从 latest 通道下载后更新软链。

## 双轨安装架构

```text
┌─────────────────────────────────────────────────────────────┐
│  AUR cursor-bin          │  官方 AppImage                    │
│  paru -Syu 升级          │  task upgrade-cursor-appimage     │
├──────────────────────────┼───────────────────────────────────┤
│  菜单: Cursor            │  菜单: Cursor (AppImage)          │
│  CLI:  cursor            │  CLI:  cursor-appimage            │
│  路径: /usr/bin/cursor   │  路径: ~/.local/bin/cursor-appimage│
└─────────────────────────────────────────────────────────────┘
         共用 ~/.config/Cursor 与 ~/.cursor
```

| 通道 | 安装 / 升级 | 入口 |
| ---- | ----------- | ---- |
| **AUR** `cursor-bin` | `paru -Syu` 或 `task install-cursor` | 菜单 **Cursor**；终端 `cursor` |
| **AppImage** | `task upgrade-cursor-appimage` | 菜单 **Cursor (AppImage)**；`cursor-appimage` |

Linux 上 chezmoi 管理的 zshrc **不**把 `~/.local/bin` 置于 PATH 最前，所以终端默认 `cursor` 解析为 AUR 的 `/usr/bin/cursor`，不会和 AppImage 抢名字。AppImage 通过别名 `cursor-appimage` 显式调用。

自动化在 homelab 仓库 `infra/homelab/workstation/`：Ansible 管安装与 AppImage 下载，chezmoi 管 PATH、别名和 `Cursor (AppImage)` 桌面项。

## 常用命令

```bash
cd infra/homelab/workstation

# 首次：AUR + AppImage 一起装
task install-cursor
chezmoi apply   # PATH、别名、AppImage 菜单项

# 仅升级 AppImage
task upgrade-cursor-appimage

# 升级 AUR 版（随系统更新）
paru -Syu
```

AppImage 文件放在 `~/.local/bin/Cursor-<version>-x86_64.AppImage`，`cursor-appimage` 软链指向当前版本。升级时旧文件会备份为 `*.zs-old`，可手动删除释放空间。

## 使用注意

1. **单实例**：AUR 和 AppImage 不要同时运行；切换版本前先 File → Exit 完全退出。
2. **配置共用**：两套共用同一套用户数据；若某版本导致配置损坏，再考虑隔离 `user-data-dir`（我目前没这么做）。
3. **通道选择**：日常稳定用 AUR + stable 即可；追新功能或等不及 AUR 时用 AppImage + latest。
4. **macOS**：双轨方案只针对 Arch 工作站；MacBook 上 Cursor 走 Homebrew Cask，不在本文范围。

## 相关

- 项目内 AI 文档布局（`.cursor/rules/`、`AGENTS.md` 等）：[项目里的 AI 文档怎么放](../AI/ai-docs-layout.md)
- AUR helper（paru / yay）：[archlinux AUR Helper, paru, yay](./aur-yay.md)
