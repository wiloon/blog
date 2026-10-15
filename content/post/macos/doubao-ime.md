---
author: "-"
date: 2026-07-10T11:11:06+08:00
lastmod: 2026-10-15T12:45:02+08:00
title: Doubao IME 豆包输入法
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
- Homebrew：`brew install --cask doubaoime`，安装到 `/Library/Input Methods/DoubaoIme.app`
- Ansible（w10n-config 仓库，内部同样用 Homebrew Cask；已有官网安装时首次加 `--force` 接管）：

  ```bash
  cd infra/homelab/workstation
  task install-doubao-ime
  ```

`brew install --cask doubao` 安装的是豆包 AI 聊天客户端，不是输入法。

装好后还需在系统设置中手动完成：

1. 键盘 → 输入法：添加「豆包输入法」
2. 隐私与安全性：为豆包输入法开启辅助功能；使用语音时需允许麦克风
3. 若菜单栏或切换异常，注销或重启后再试

## 语音输入后自动切回英文输入法

豆包的跨输入法语音输入结束后会停在豆包拼音上，不会切回原来的输入法。我用 Hammerspoon 监听麦克风状态补上了自动切回，见 [Doubao IME Voice Input: 语音输入后自动切回英文输入法](./doubao-voice-auto-restore.md)。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-15 | 标题加英文；安装方式改为 Homebrew Cask `doubaoime`；新增语音输入后自动切回输入法的链接 | 标题须含英文；playbook 已改用 Homebrew Cask；新增相关文章 |
