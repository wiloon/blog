---
title: macos container
author: "-"
date: 2025-11-02T08:30:00+00:00
url: macos-container
categories:
  - container
tags:
  - reprint
  - remix
  - AI-assisted
---
## macos container

Apple 官方的容器化工具，专为 Apple Silicon Mac 设计，使用轻量级虚拟机运行 Linux 容器。

### 系统要求

- Apple Silicon Mac (M 系列芯片)
- macOS 26 或更高版本
- Xcode (从 App Store 安装)

### 安装

```bash
# 使用 Homebrew Cask 安装
brew install --cask container

# 启动 container 系统服务
container system start

# 检查系统状态
container system status

# 运行测试容器
container run --rm -it docker.io/library/hello-world:latest

# 列出容器 (注意: 使用 ls 而不是 ps)
container ls

# 查看所有可用命令
container --help
```

### 从源码编译

```bash
git clone https://github.com/apple/container.git
cd container
swift build
sudo cp .build/debug/container /usr/local/bin/container
```
