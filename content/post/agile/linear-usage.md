---
title: Linear 使用笔记
author: "-"
date: 2026-06-21T06:45:22+08:00
lastmod: 2026-06-21T06:45:22+08:00
url: linear-usage
categories:
  - agile
tags:
  - linear
  - kanban
  - remix
  - AI-assisted
---

## 背景

选型结论见 [看板工具选型](./kanban-tool-selection.md)，最终选用 Linear。本文记录日常使用中的操作与快捷键，随用随补。

## 视图与布局

### 列表 / 看板切换

在 Issue 视图（Backlog、All issues 等支持布局切换的页面）：

- macOS：`⌘ B` 在列表与看板之间切换
- Windows / Linux：`Ctrl B`

若某个视图默认想用看板：先切到看板布局 → 右上角 **Display options** → **Set as default**。该设置只对当前视图生效，不能全局默认。

### Display options

- macOS：`⇧ V` 打开 Display options
- 看板可按 Status、Assignee、Project、Priority、Cycle 分组

## 导航

| 操作 | macOS | 说明 |
| ---- | ----- | ---- |
| 打开搜索 | `/` | 全局搜索 |
| 新建 Issue | `C` | 快速创建 |
| 我的 Issues | `G` `A` | Go → My issues |
| Backlog | `G` `B` | |
| 看板页 | `G` `D` | Go → Board |
| Inbox | `G` `I` | |

（`G` 开头的是组合键：先按 `G`，松手后再按第二个字母。）

## Issue 操作

| 操作 | macOS |
| ---- | ----- |
| 打开 Issue | `O` `I` |
| 编辑 | `E` |
| 改状态 | `S` |
| 改优先级 | `P` |
| 指派给自己 | `I` |
| 复制 Issue ID | `⌘ .` |
| 复制 git 分支名 | `⇧ ⌘ .` |

## 参考

- [Board layout – Linear Docs](https://linear.app/docs/board-layout)
- [Display options – Linear Docs](https://linear.app/docs/display-options)
