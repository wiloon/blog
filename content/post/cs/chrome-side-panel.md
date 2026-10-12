---
title: "Chrome Side Panel 侧边栏"
author: "-"
date: 2026-10-12T10:04:10+08:00
lastmod: 2026-10-12T10:04:10+08:00
url: chrome-side-panel
categories:
  - Web
tags:
  - chrome-extension
  - side-panel
  - manifest-v3
  - enx
  - remix
  - AI-assisted
---
## Side Panel 是什么

Chrome 窗口右侧可以展开的一栏，和当前网页并排显示。Google 的说法是「a new companion surface that allows users to use tools alongside the content they are browsing」：一个伴随页面的界面，让用户一边看网页一边用工具。

它分两层：

- 浏览器自带的侧边栏：书签、阅读清单等 Chrome 自己的功能。
- 扩展的侧边栏：扩展通过 Side Panel API（`chrome.sidePanel`）在这一栏里显示自己的页面。

## 时间线

| 时间 | 版本 | 变化 |
| ---- | ---- | ---- |
| 2022-03 | Chrome 99 | 稳定版出现侧边栏，内容是书签和阅读清单（9to5Google 报道；Google 自己的博客写的是 2022 年 5 月加入） |
| 2023-05 | Chrome 114 | 扩展可用 Side Panel API，只支持 Manifest V3，需要 `sidePanel` 权限 |
| 2023-08 | Chrome 116 | 新增 `sidePanel.open()`，可以由扩展主动打开，但必须在用户操作（点击、快捷键、右键菜单等）里调用 |

## 为什么要有 Side Panel API

API 出现之前，扩展想做侧边栏，只能用 content script 往每个网页里注入一个 `<div>`。Google 在发布 API 时给的理由：

- 位置和布局统一：各个扩展的侧边栏出现在同一个地方，样子一致。
- 隐私：显示侧边栏不需要申请 host 权限，安装时的权限警告也更少。
- 不用往不受信任的网页里注入界面：注入的 UI 会和网页的样式、脚本互相干扰。

## 设计初衷和适用场景

官方给的唯一示例是词典：右键一个词，在侧边栏里显示释义（Dictionary side panel 示例）。翻译、查词这类「一边读一边查」的扩展，正是它设计时设想的用法。

Chrome Web Store 的政策对侧边栏也有要求：

- 单一用途政策同样适用于侧边栏，内容要和扩展本身的功能直接相关。
- 不相关的网站上不要显示，可以用 `setOptions` 只在特定网站启用。
- 不要放无关的干扰内容。

## ENX 的用法

[enX](../development/enx.md) 的侧边栏用来显示整句翻译和在句子里查的词。几个做法：

- 页面里的查词仍然靠 content script：要读网页文字、画下划线，侧边栏做不到这些。侧边栏只放「需要更大空间、和页面并排看」的内容。
- 按标签页打开（`setOptions({ tabId, path })`），关闭标签页时侧边栏跟着消失，不会把上一页的内容带到下一页。
- `open()` 必须在用户手势里调用，所以从网页浮层点按钮时，要在 background 收到消息后同步调用，中间不能有 `await`。

## 参考

- [chrome.sidePanel API](https://developer.chrome.com/docs/extensions/reference/api/sidePanel)
- [Design a superior user experience with the new Side Panel API](https://developer.chrome.com/blog/extension-side-panel-launch)
- [Create a side panel](https://developer.chrome.com/docs/extensions/develop/ui/create-a-side-panel)
- [Chrome 99 side panel（9to5Google）](https://9to5google.com/2022/03/25/google-chrome-side-panel/)
