---
title: obsidian
author: "-"
date: 2013-01-12T06:56:46+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: obsidian
categories:
  - Tools
tags:
  - obsidian
  - remix
  - AI-assisted
---
## obsidian

```bash
# archlinux
pacman -S obsidian
```

[https://forum-zh.obsidian.md/](https://forum-zh.obsidian.md/)

```bash
flatpak install flathub md.obsidian.Obsidian
flatpak run md.obsidian.Obsidian
```

[https://decoge.medium.com/how-to-install-obsidian-on-a-chromebook-53e379217adf](https://decoge.medium.com/how-to-install-obsidian-on-a-chromebook-53e379217adf)

## install plugin: remotely save

Obsidian> settings> community plugins> turn on community plugins> browse

search remotely save and install and enable

config s3 storage:

setting> community plugins> remotely save

- Choose A Remote Service: S3 or compatible
- endpoint: s3.ap-southeast-1.amazonaws.com
- region: ap-southeast-1
- ak: `<check in bitwarden>`
- sk: `<check in bitwarden>`
- bucket name: obsidian-w10n

## 调整页边距

解决编辑区域过窄的问题

Obsidian> settings> Editor> Readable line length: diable

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Tools | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
