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

## 竞品

以下是 macOS 上中文语音输入的几类选择，整理于 2026-10，产品和价格变化快，以各家官网为准。

### 中文输入法自带语音

和豆包用法一样，都是在一个输入法里带语音输入。

| 产品 | 说明 |
| ---- | ---- |
| 讯飞输入法 Mac 版 | 中文语音识别做得最久，方言、专业术语、长句的口碑好 |
| 微信输入法 Mac 版 | 免费、轻量，有语音输入 |
| 搜狗输入法 Mac 版 | 有语音输入，Mac 版的语音体验一般不如手机端 |
| 百度输入法 Mac 版 | 同上 |

豆包的优势在大模型带来的标点、断句和口语整理（去掉「嗯」「那个」等），并且免费。

### macOS 自带听写

系统设置 → 键盘 → 听写。支持普通话和英文，Apple Silicon 上可以离线识别，不用装任何东西。中文的准确率和标点不如豆包、讯飞，适合偶尔用。

### 跨输入法的 AI 听写工具

这类工具不是输入法，也不切换系统输入法：按快捷键说话，说完把文字直接粘贴到当前光标处，所以没有豆包那种「语音结束后停在中文输入法上」的问题。

| 产品 | 运行方式 | 说明 |
| ---- | -------- | ---- |
| superwhisper | 本地或云端 | 可选本地 Whisper / Parakeet 模型，完全离线；也提供云端模型和 AI 改写模式，选了云端模式音频会上传 |
| MacWhisper | 本地 | 本地 Whisper 模型，偏转录音频文件，也能听写 |
| VoiceInk | 本地 | 开源，本地运行 |
| Wispr Flow | 云端 | 英文听写里名气最大，带个人词典、语音片段（snippets）；会截取当前窗口作为上下文，有隐私争议；付费订阅 |
| Typeless | 云端 | 除了听写，还能选中文字后用语音指令改写、缩短；免费额度较多；付费订阅 |

Whisper 系模型识别中文偶尔会输出繁体，需要在设置或提示词里指定简体。

### 怎么选

- 中文：豆包或讯飞输入法
- 英文：要效果最好选 Wispr Flow 或 Typeless（云端）；在意隐私、想离线选 superwhisper 本地模式；只是偶尔用，macOS 自带听写的英文效果已经不错

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-15 | 标题加英文；安装方式改为 Homebrew Cask `doubaoime`；新增语音输入后自动切回输入法的链接 | 标题须含英文；playbook 已改用 Homebrew Cask；新增相关文章 |
