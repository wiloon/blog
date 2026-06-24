---
title: 'Hugo Static Site Search: Fuse.js 与 Pagefind'
author: "-"
date: 2026-06-24T18:24:33+08:00
lastmod: 2026-06-24T18:24:33+08:00
url: hugo-static-site-search
categories:
  - development
tags:
  - hugo
  - pagefind
  - remix
  - AI-assisted
---

## 背景

本站使用 Hugo + PaperMod，通过 `Containerfile` 构建为 Nginx 静态站点镜像。文章约 2800+ 篇（Pagefind 实测索引 **2779** 页）。本文记录站内搜索方案调研与当前 Pagefind 接入方式。

## PaperMod 内置搜索（Fuse.js，已弃用）

PaperMod 主题自带基于 **Fuse.js** 的客户端搜索：Hugo 构建时生成 `index.json`，搜索页在浏览器里加载全文索引并做模糊匹配。零后端依赖，但本站实测 `index.json` 约 **13MB**，需一次下载全部正文，首访慢，中文分词也一般。现已移除 Fuse 相关配置，改用 Pagefind。

## Hugo 静态站搜索方案对比

| 方案 | 原理 | 适合规模 | 优点 | 缺点 |
| ---- | ---- | -------- | ---- | ---- |
| PaperMod Fuse.js | 浏览器加载完整 JSON | 小站（约 500 篇以内） | 零配置、纯静态 | 大站索引体积大、首访慢；中文分词弱 |
| Pagefind | 构建时生成索引，搜索时按查询加载分片 | 中大型站 | 首访不必下完全部正文；extended 支持 CJK | 需加构建步骤；索引目录总体积未必更小 |
| Lunr.js | 类似 Fuse，浏览器建倒排索引 | 小中型 | 多主题支持 | 与 Fuse 同类局限 |
| Algolia DocSearch | 构建时推送到 Algolia 云端 | 文档站 / 开源项目 | 搜索体验好 | 需申请、依赖第三方 |
| Meilisearch / Typesense | 自托管搜索引擎 | 大型站 | 功能强 | 需跑服务，个人博客偏重 |

## 本站实现：Pagefind

采用 **Pagefind extended**（v1.5.2，支持中文分词）。搜索 UI 使用 **Default UI**（`pagefind-ui.js` / `PagefindUI`），不是 1.5 新推荐的 Component UI。

### 构建流程

```mermaid
flowchart LR
    A[hugo --minify] --> B[public/*.html]
    B --> C[pagefind --site public]
    C --> D[public/pagefind/]
    D --> E[/search/ 搜索页]
```

统一入口：`scripts/build-site.sh`（`task site:build`）。

- 本地：脚本内 `npx -y pagefind@1.5.2`（npm 包默认带 extended）
- Cloudflare Pages：`build.sh` → `scripts/build-site.sh`（OpenTofu `build_command = "bash build.sh"`）
- 容器：`Containerfile` 安装 `pagefind_extended` 二进制，执行 `hugo --minify && pagefind --site public`

### 索引范围

文章 URL 在站点根路径（front matter 自定义 `url`），不在 `/post/` 下，因此**不能**用 `post/**/*.html` 这类 glob 限定范围。

实际做法：

1. `pagefind.yml` 只指定 `site: public`
2. `layouts/single.html` 在 `<article>` 上加 `data-pagefind-body`
3. Pagefind 检测到该属性后，**自动忽略**不含它的页面（标签页、分类列表、首页等）
4. `post-footer` 等区域加 `data-pagefind-ignore`，避免标签链接等进入正文索引

### 关键文件

| 文件 | 作用 |
| ---- | ---- |
| `content/search.md` | 搜索页内容，`layout: search` |
| `pagefind.yml` | 指定索引源目录 `public` |
| `layouts/single.html` | 文章页 `data-pagefind-body`；页脚 `data-pagefind-ignore` |
| `layouts/search.html` | 搜索页挂载 `PagefindUI` |
| `layouts/_partials/head.html` | 移除 PaperMod Fuse.js 脚本 |
| `assets/css/extended/pagefind.css` | 搜索框样式适配 PaperMod 主题色 |
| `scripts/build-site.sh` | `hugo` + `pagefind`，版本由 `PAGEFIND_VERSION` 控制 |
| `build.sh` | Cloudflare Pages 入口：生成 `stats.json` 后调用 `scripts/build-site.sh` |
| `Containerfile` | 多阶段构建：Hugo → Pagefind → Nginx |
| `config.toml` | 启用「搜索」菜单；`outputs.home` 仅保留 HTML（不再生成 `index.json`） |

### 本地预览

| 命令 | 说明 |
| ---- | ---- |
| `task preview` | `hugo server` 热更新（`:1313`），**无**搜索索引 |
| `task preview:search` | 先 `build-site.sh` 构建索引，再 `pagefind --serve` 静态服务（`:1414`）；非热更新 |
| `task site:build` | 仅构建到 `public/`，不启动服务 |

访问搜索页：`http://localhost:1414/search/`（preview:search）或部署后的 `/search/`。导航栏「搜索」、`Alt + /` 快捷键可用。

### 与 Fuse 方案的区别

| | Fuse.js（旧） | Pagefind（当前） |
| --- | --- | --- |
| 索引产物 | `index.json`（约 13MB 全文） | `public/pagefind/`（约 27MB，压缩分片） |
| 加载方式 | 打开搜索页一次下载全部 | 按查询按需加载相关分片 |
| 构建步骤 | 仅 `hugo` | `hugo` + `pagefind` |
| 收录范围 | `index.json` 遍历 RegularPages | 仅含 `data-pagefind-body` 的 HTML（实测 2779 页） |
| 中文 | 字符级模糊匹配 | extended 版 CJK 分词 |

索引目录总体积未必小于 Fuse 的单文件 JSON，优势在于搜索时不必首屏拉取全部正文。
