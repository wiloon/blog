---
title: obsidian
author: "-"
date: 2013-01-12T06:56:46+00:00
url: obsidian
categories:
  - Inbox
tags:
  - reprint
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
- ak: <check in bitwarden>
- sk: <check in bitwarden>
- bucket name: obsidian-w10n

## 调整页边距

解决编辑区域过窄的问题

Obsidian> settings> Editor> Readable line length: diable
