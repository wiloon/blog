---
title: "Giscus：基于 GitHub Discussions 的评论系统"
author: "-"
date: 2026-06-16T09:11:22+08:00
lastmod: 2026-06-16T09:11:22+08:00
url: giscus
categories:
  - development
tags:
  - giscus
  - hugo
  - github
  - remix
  - AI-assisted
---

Giscus 是一个基于 GitHub Discussions 的评论系统，评论数据完全存储在 GitHub，无需额外的数据库或第三方平台。适合托管在 GitHub Pages、Cloudflare Pages 等静态站点。

## 工作原理

Giscus 把每篇页面的评论映射到 GitHub Discussions 中的一个 Discussion，通过在页面嵌入 `<script>` 标签加载评论组件。

页面与 Discussion 的映射方式：

| 映射方式 | 说明 |
| --- | --- |
| `pathname`（推荐） | 按页面 URL 路径匹配，最通用 |
| `title` | 按文章标题匹配 |
| `og:title` | 按 Open Graph 标题匹配 |

## 前置条件

- GitHub 仓库需开启 Discussions 功能：仓库 Settings → Features → Discussions ✓
- 安装 Giscus GitHub App：[github.com/apps/giscus](https://github.com/apps/giscus) → Install → 选择目标仓库

## 获取配置参数

访问 [giscus.app](https://giscus.app)，填写仓库名和配置选项，页面底部会生成完整的 `<script>` 标签，从中获取：

- `data-repo-id`（格式 `R_kgDO...`）：仓库 Node ID
- `data-category-id`（格式 `DIC_kwDO...`）：Discussion 分类 ID

Discussion 分类推荐选 `Announcements`：只有维护者能在 GitHub 网页直接新建 Discussion，普通用户只能通过 Giscus 组件留言，防止垃圾内容。

## 在 Hugo + PaperMod 中集成

PaperMod 主题已内置评论机制，`layouts/single.html` 中有：

```html
{{- if (.Param "comments") }}
{{- partial "comments.html" . }}
{{- end }}
```

需要做两步修改：

### 1. 创建 comments.html override

在 `layouts/_partials/` 目录创建 `comments.html`（会覆盖主题的空占位文件）：

```html
<div class="comments">
  <script src="https://giscus.app/client.js"
    data-repo="your-user/your-repo"
    data-repo-id="R_kgDO..."
    data-category="Announcements"
    data-category-id="DIC_kwDO..."
    data-mapping="pathname"
    data-strict="1"
    data-reactions-enabled="1"
    data-emit-metadata="0"
    data-input-position="bottom"
    data-theme="preferred_color_scheme"
    data-lang="zh-CN"
    crossorigin="anonymous"
    async>
  </script>
</div>
```

关键参数说明：

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `data-strict` | `1` | 严格匹配 pathname，URL 不变则评论不丢失 |
| `data-theme` | `preferred_color_scheme` | 跟随系统深色/浅色模式 |
| `data-input-position` | `bottom` | 输入框在评论列表下方 |
| `data-lang` | `zh-CN` | 界面语言中文 |

### 2. 开启评论

在 `config.toml` 中将 `comments = false` 改为 `comments = true`，全局开启所有文章的评论区。

如需对个别文章关闭，可在该文章 front matter 添加 `comments: false`。

## 回退

全局关闭：将 `config.toml` 中 `comments = true` 改回 `false`。评论数据保留在 GitHub Discussions，不会丢失。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-16 | 新建文章，记录 Giscus 集成方法 | 参考 TASK-SPEC-giscus-comments.md |
