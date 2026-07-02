---
title: enX
author: "-"
date: 2024-10-17T07:46:51+08:00
lastmod: 2026-07-01T18:10:41+08:00
url: enX
categories:
  - Projects
tags:
  - original
  - AI-assisted
---
## enX

GitHub 仓库：[wiloon/enx](https://github.com/wiloon/enx)

## 开发环境

vscode

## 本地测试

1. 在 Chrome 里打开 Manage Extensions: chrome://extensions/
2. Reload enX
3. 在 Chrome 里打开 InfoQ 里任意一篇文章
4. 点击扩展栏里的 enX
5. enX 会标记文章正文部分的英文词

## unit test

```Bash
cd /Users/wiloon/workspace/projects/enx/chrome-enx
npm run test -- infoq.test.js
```
## deploy api to local vm

1. commit and push enx to GitHub
2. go to jenkins run deploy

## env

DNS: 192.168.50.1:53, dnsmasq
Nginx: 192.168.50.130
api: 192.168.50.36:8080

[https://github.com/wiloon/enx/blob/main/enx-api/deploy.sh](https://github.com/wiloon/enx/blob/main/enx-api/deploy.sh)

## 维护记录

| 时间       | 修改内容               | 原因                                                                                                                  |
| ---------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 2026-07-01 | 顶部加 GitHub 仓库链接 | 供 [open-source-dictionaries.md](../english/open-source-dictionaries.md) 站内链接跳转到本文后，能继续跳到 GitHub 仓库 |
