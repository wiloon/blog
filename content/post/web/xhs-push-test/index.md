---
title: 'XHS Push Test: 小红书推送测试页'
author: "-"
date: 2026-06-24T23:08:54+08:00
lastmod: 2026-06-24T23:08:54+08:00
url: xhs-push-test
description: wiloon.com 小红书推送联调用的固定测试页，用于校验标题、摘要与正文抓取。
categories:
  - development
tags:
  - hugo
  - remix
  - AI-assisted
---

## 说明

这是 wiloon.com 上的**测试页面**，用于验证「博客文章 → 小红书」推送流程。线上地址：`https://wiloon.com/xhs-push-test/`。

推送脚本或人工联调时，可用本页校验：

1. 能否正确抓取标题与 `description`
2. 正文 Markdown 转笔记文案是否正常
3. 部署后 URL 是否可公网访问

## 固定测试元数据

| 字段 | 值 |
| ---- | ---- |
| 站点 | wiloon.com |
| 路径 | `/xhs-push-test` |
| 创建日期 | 2026-06-24 |
| 用途 | 小红书推送联调 |

## 正文摘录（用于 diff）

下面这段文案故意写死，方便对比抓取结果是否与源站一致：

> 后端工程师的日常笔记站。技术栈：Java、Go、Kubernetes、Ansible。本段为 XHS 推送测试专用固定文本，请勿当作正式内容发布。

## 可选检查项

- 标题含英文：`XHS Push Test`
- 分类：`development`
- 标签：`hugo`

联调通过后，可删除本页或改为 `draft: true` 避免出现在站点列表中。
