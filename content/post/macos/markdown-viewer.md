---
title: "Markdown Viewer: 轻量 Markdown 预览工具"
author: "-"
date: 2026-10-20T06:24:00+08:00
lastmod: 2026-10-20T06:24:00+08:00
url: markdown-viewer
categories:
  - Desktop
tags:
  - markdown
  - macos
  - glow
  - claude-code
  - remix
  - AI-assisted
---

## 背景

在 Claude Code 会话里经常会生成一些 Markdown 文档，想快速看一下渲染效果。VS Code、Cursor 能预览，但启动慢，只为看一篇文档不值得。这里记录几个轻量的方案，以 macOS 为主。

Markdown 语法本身见 [Markdown 语法](../cs/markdown.md)。

## 方案对比

| 工具 | 类型 | 价格 | 适合场景 |
| ---- | ---- | ---- | -------- |
| QuickLook + QLMarkdown | Finder 预览插件 | 免费 | 只看不改，按空格即出 |
| MarkEdit | 原生 macOS 编辑器 | 免费 | 边看边改 |
| glow | 终端 TUI | 免费 | 留在终端里读，跨平台 |
| mdcat | 终端渲染 | 免费 | kitty / iTerm2 下能显示图片 |
| Typora | 所见即所得编辑器 | 付费 | 长文写作 |
| Marked 2 | 预览器 | 付费 | 配合任意编辑器实时预览 |

日常用 QuickLook 看、MarkEdit 改就够了，两个都是原生应用，启动不到一秒。

## QuickLook + QLMarkdown

QLMarkdown 给 macOS 的 QuickLook 加上 Markdown 渲染，支持 GFM、表格、代码高亮、mermaid。

```bash
brew install --cask qlmarkdown
```

装完后首次需要打开一次 QLMarkdown.app，让系统注册扩展。之后在 Finder 选中 `.md` 文件按空格就是渲染后的效果。

命令行也能直接弹出预览窗口：

```bash
# open a QuickLook preview window from terminal
qlmanage -p README.md >/dev/null 2>&1
```

使用中遇到的问题：在预览页面里双击，预览窗口会直接关掉。我有时习惯双击选中一个词，结果窗口意外关闭，体验不太好。还不确定这是 QuickLook 本身的设计（双击预览内容通常会用默认应用打开文件并关闭预览）还是 QLMarkdown 的 bug。需要选词、复制内容时，改用鼠标拖选，或者直接用下面的 MarkEdit 打开。

## MarkEdit

MarkEdit 是 Swift 写的原生 Markdown 编辑器，体积小，启动速度接近系统自带的 TextEdit，带预览。

```bash
brew install --cask markedit

# open a file with MarkEdit
open -a MarkEdit README.md
```

## glow

glow 是 Go 写的终端 Markdown 渲染器，macOS 和 Linux 都能用，Linux 下的安装记录见 [Linux Apps](../linux/linux-apps.md)。

```bash
brew install glow

# read with pager
glow -p README.md

# browse markdown files in current directory
glow
```

## mdcat

mdcat 把 Markdown 渲染输出到终端，在 kitty、iTerm2、WezTerm 下能直接显示文中的图片。

```bash
brew install mdcat

mdcat README.md
```

## 在 Claude Code 会话中打开

Claude Code 没有内置的 Markdown 预览命令。在会话里可以用 `!` 前缀执行 shell 命令，也可以直接让 Claude 去打开文件（它知道刚生成的文件路径）。

需要注意的是，`!` 命令的输出会写进会话上下文：

- 不要用 `! glow file.md`：渲染结果整篇进上下文，浪费 token；`!` 也不是交互式终端，分页器翻不了页
- 用只弹窗口、几乎没有输出的命令

```bash
# open GUI viewer, nothing printed back into the session
! qlmanage -p docs/foo.md >/dev/null 2>&1
! open -a MarkEdit docs/foo.md
```

用 kitty 的话，可以在 overlay 或新窗口里跑 glow，不影响 Claude Code 的界面。需要先在 `kitty.conf` 里打开远程控制：

```conf
# kitty.conf
allow_remote_control yes
```

```bash
# run glow in a kitty overlay window
! kitty @ launch --type=overlay glow -p docs/foo.md
```
