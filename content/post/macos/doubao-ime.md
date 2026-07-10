---
author: "-"
date: 2026-07-10T11:11:06+08:00
lastmod: 2026-07-10T11:11:06+08:00
title: 豆包输入法
url: doubao-ime
categories:
  - Desktop
tags:
  - macos
  - remix
  - AI-assisted
---

## 豆包输入法

macOS 上的 AI 语音输入法，来自字节跳动。参见 [macOS Apps](./macos-apps.md) 中的输入法列表。

- 官网：[shurufa.doubao.com](https://shurufa.doubao.com)
- 手动安装：官网下载 `DoubaoImeInstaller_*.zip`，双击安装器按 GUI 引导完成
- Ansible 静默安装（写入 `/Library/Input Methods/`，不弹 GUI 安装器）：

  ```bash
  cd homelab/workstation   # w10n-config 仓库
  task install-doubao-ime  # 需输入 sudo 密码
  ```

  Playbook 从官网 API 拉取最新包并执行包内 `install.sh`。

`brew install --cask doubao` 安装的是豆包 AI 聊天客户端，不是输入法。

装好后还需在系统设置中手动完成：

1. 键盘 → 输入法：添加「豆包输入法」
2. 隐私与安全性：为豆包输入法开启辅助功能；使用语音时需允许麦克风
3. 若菜单栏或切换异常，注销或重启后再试
