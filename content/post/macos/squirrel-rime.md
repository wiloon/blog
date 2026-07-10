---
author: "-"
date: 2026-07-10T11:11:06+08:00
lastmod: 2026-07-10T11:30:00+08:00
title: "Squirrel（鼠须管）"
url: squirrel-rime
categories:
  - Desktop
tags:
  - macos
  - remix
  - AI-assisted
---

## Squirrel（鼠须管）

macOS 上基于 RIME 输入法引擎的输入法，可自定义方案。参见 [macOS Apps](./macos-apps.md) 中的输入法列表。

**命名由来**

RIME 项目给各平台前端起的名字都是传统毛笔的名称，与输入法功能本身无关：Windows 端叫小狼毫（Weasel，狼毫笔），macOS 端叫鼠须管（Squirrel，鼠须笔，相传王羲之用它写《兰亭序》）。"鼠须"直译是"老鼠胡须"，英文若直译成 Rat 观感不好，于是取了同属啮齿类、形象更讨喜的 Squirrel（松鼠）作为意译名，因此 Squirrel 与"鼠须管"并非字面对应，而是保留"啮齿类"这个关联的近似翻译。

- 项目：[rime.im](https://rime.im)
- 安装：`brew install --cask squirrel`
- Ansible：

  ```bash
  cd homelab/workstation   # w10n-config 仓库
  task install-squirrel
  ```

Squirrel 本身只带基础拼音方案，**不包含五笔**，需另外安装 schema：

```bash
bash -c "$(curl -fsSL https://git.io/rime-install)" -- rime-wubi --using-mirror
```

或手动下载 rime-wubi（如 rime-wubi86-jidian）方案文件放入 `~/Library/Rime/`，在 `default.yaml` 的 `schema_list` 中加入五笔 schema，再右键菜单栏图标「重新部署」。

装好后需在系统设置中手动完成：

1. 键盘 → 输入法：添加「简体中文」→「鼠须管」
2. 安装五笔 schema（见上）
3. 点击菜单栏图标或自定义快捷键切换到五笔方案
