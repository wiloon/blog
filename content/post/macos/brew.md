---
title: Homebrew (brew) 使用指南
author: "-"
date: 2026-06-11T11:18:29+08:00
lastmod: 2026-06-11T14:20:33+08:00
url: brew
categories:
  - macOS
tags:
  - brew
  - macOS
  - remix
  - AI-assisted
---

## 简介

[Homebrew](https://brew.sh/) 是 macOS 上最流行的包管理器，用于安装和管理命令行工具及应用程序。

- brew 会把软件安装在用户主目录里，不需要 sudo
- brew（formula）装的主要是命令行工具
- brew cask 装的大多是有 GUI 界面的 app 以及驱动

## Formula 与 Cask 的区别

两者的本质区别是**安装方式**，不是有没有 GUI：

- **formula**：需要从源码编译或解压二进制的工具，brew 完全管理其生命周期
- **cask**：处理 `.dmg`、`.pkg`、`.zip`（含 `.app`）这类"分发包"，安装时需要复制到 `/Applications`、注册 UTI、处理系统权限等，安装/卸载逻辑与 formula 完全不同

两套安装逻辑分开，互不干扰，也便于用户区分"这是个 CLI 工具"还是"这是个桌面 App"。

实际使用中的经验规律：

| 类型 | 典型情况 | 例外 |
| --- | --- | --- |
| formula（不加 `--cask`）| 命令行工具、库 | 极少数带 GUI |
| cask（`--cask`）| GUI 桌面 App | `google-cloud-sdk`、`android-platform-tools` 等纯 CLI |

官方说法是：cask 用于安装"macOS native apps and large binaries"，重点是**分发形式**（预编译的大型安装包），而不是有没有界面。

### Homebrew 术语表（酿酒比喻）

Homebrew 整个项目名叫"家酿啤酒"，术语全部来自酿酒场景：

| 术语 | 酿酒含义 | 对应概念 |
| --- | --- | --- |
| formula | 配方 | 软件的安装脚本 |
| keg | 酒桶 | 安装后的目录（`/usr/local/Cellar/<pkg>`）|
| cellar | 酒窖 | 所有已安装包的存放处 |
| tap | 水龙头（接上一个新酒桶）| 接入一个新的软件仓库 |
| cask | 大木桶（装整瓶酒）| 完整的 macOS App |
| bottle | 预先装好的瓶子 | 预编译的二进制包 |

## 安装与卸载 brew

```bash
# 安装
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 卸载
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
```

## 常用命令

```bash
# 搜索
brew search foo

# 安装
brew install ansible
brew install --cask obsidian

# 卸载
brew uninstall packageName

# 列出已安装的包
brew list

# 查看所有需要更新的包
brew outdated

# 更新某一个包
brew upgrade package0

# 更新所有包
brew upgrade

# 配置信息
brew config

# 检查系统问题
brew doctor
```

## Tap（第三方仓库）

### 什么是 tap

brew 默认只包含官方维护的 formula（`homebrew/core`）和 cask（`homebrew/cask`）。**tap** 是第三方维护的额外软件仓库，本质上是一个 GitHub 仓库，遵循 brew 的目录结构约定。

通过 tap，软件作者可以自己发布和维护 brew 安装包，用户不需要等官方收录。

名字来自酿酒比喻："tap"（水龙头）的语义是把一个新的啤酒桶"接上"（tap into）系统，之后就能从里面"倒出"软件来。

### tap 命令

```bash
# 添加一个 tap
brew tap <user>/<repo>

# 列出已添加的 tap
brew tap

# 移除 tap
brew untap <user>/<repo>

# 直接从 tap 安装（会自动 tap）
brew install --cask <user>/<tap>/<cask>
```

### 示例：通过 tap 安装 netbird-ui

netbird 没有进入 homebrew 官方仓库，官方维护了自己的 tap `netbirdio/tap`：

```bash
# 方式一：先 tap，再安装
brew tap netbirdio/tap
brew install --cask netbird-ui

# 方式二：直接指定完整路径（推荐，自动 tap）
brew install --cask netbirdio/tap/netbird-ui
```

**背景**：netbird 原本通过官网 `.pkg` 安装包安装。迁移到 brew 管理后，可以通过 `brew upgrade --cask netbird-ui` 统一升级，不再需要手动下载安装包。`/var/lib/netbird/` 中的配置文件（私钥、管理服务器地址）在迁移过程中完整保留，连接配置不受影响。

### 升级 netbird

```bash
brew upgrade --cask netbird-ui
```

## 换国内源（网络慢时）

```bash
# 步骤一：更换 brew 主仓库
cd "$(brew --repo)"
git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git

# 步骤二：更换 homebrew-core
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git

# 步骤三
brew update
```

### 恢复默认源

```bash
cd "$(brew --repo)"
git remote set-url origin https://github.com/Homebrew/brew.git

cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://github.com/Homebrew/homebrew-core

brew update
```

## 所有 cask 包

<https://formulae.brew.sh/cask/>
