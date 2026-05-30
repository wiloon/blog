---
title: "网站访问统计：Umami + Cloudflare Web Analytics"
date: 2026-05-10T20:10:42+08:00
lastmod: 2026-05-30T07:03:28+08:00
url: web-analytics
tags: ["umami", "cloudflare", "analytics", "hugo", "papermod", "remix", "AI-assisted"]
categories: ["cs"]
---

## 背景

Hugo 博客（PaperMod 主题）默认没有访问统计。为了了解谁在访问、访问了哪些页面，选择同时接入两套统计：

- **Umami**：隐私友好，无 cookie，数据存储在 Umami 服务器
- **Cloudflare Web Analytics**：与 Cloudflare 基础设施集成，数据存储在 Cloudflare

两者不冲突，可以同时运行，便于对比数据。

## Umami

### 特点

- 无 cookie，无跨站追踪，不需要 GDPR 同意弹窗
- 免费 Hobby 计划：100K 事件/月，3 个站点，6 个月数据保留
- 地理位置精度：**国家级别**

### 统计维度

- 页面浏览量（PV）、独立访客数（UV）
- 每次会话浏览页数、跳出率、平均停留时间
- 引荐来源、UTM 参数
- 国家/地区、操作系统、浏览器、设备类型
- 各页面访问量排行

### Browsers：Chrome、Chrome (iOS) 与 iOS

Umami 在 **Environment → Browsers** 里根据访问请求的 **User-Agent（UA）** 解析浏览器名称，与 **Environment → OS** 里的操作系统是两套维度，不要混看。

| 显示名称 | 含义 |
| -------- | ---- |
| Chrome | 桌面端或 Android 等环境下的 Chrome；UA 不含 iOS 专用标记 |
| Chrome (iOS) | iPhone / iPad 上用 **Chrome App** 打开；UA 含 `CriOS/版本号` |
| iOS | 能判断是 iOS 上的浏览器或 WebView，但 **未识别** 为 Safari、Chrome、Firefox、Edge 等时的兜底分类 |

列表里 Chrome (iOS) 与 iOS 各计 1 个访客，通常表示 **两次不同访问**（不同人或不同设备 / 浏览器），不是同一次访问被记了两遍。

#### 为何 iOS 上还有单独的 Chrome (iOS)

Apple 要求 iOS 上所有浏览器共用 **WebKit** 引擎（与 Safari 相同），Chrome 无法在 UA 里伪装成桌面 Chrome。Chrome for iOS 在 UA 中用 `CriOS` 代替 Safari 的 `Version/`，例如：

```text
Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X)
AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/135.0.7049.83 Mobile/15E148 Safari/604.1
```

Umami 使用 [detect-browser](https://github.com/DamonOehlman/detect-browser) 解析 UA，识别到 `CriOS` 即归类为 **Chrome (iOS)**。

#### Browsers 里的「iOS」常见来源

这里的 **iOS 不是操作系统**（操作系统在 OS 面板，会显示 `iOS 18` 等版本）。常见落入该桶的访问包括：

- 应用内浏览器（微信、邮件、RSS 等 App 内置网页）
- 未带 `CriOS` / `FxiOS` / `EdgiOS` 等应用标记的 WebView 或第三方浏览器
- UA 被缩短、隐私模式或代理改写导致解析失败

系统 **Safari** 一般会单独显示为 **Safari**；若 Browsers 里只有 iOS 而没有 Safari，说明 iOS 流量很少，且该次访问未被归入 Safari。

#### 如何核对某次访问

在 Umami **Sessions** 中按 `browser` 筛选 `Chrome (iOS)` 或 `iOS`，对照引荐来源、页面与国家。若能查看原始 UA，含 `CriOS` 即为 Chrome App，否则多为未细分的 iOS WebView 或浏览器。

### 接入步骤

1. 注册 [cloud.umami.is](https://cloud.umami.is)
2. **Settings → Websites → Add website**，填入域名
3. 获取 `<script>` 标签

### Hugo PaperMod 接入方式

PaperMod 主题提供了 `extend_head.html` 扩展点，在项目根目录创建：

```
layouts/_partials/extend_head.html
```

内容：

```html
<script defer src="https://cloud.umami.is/script.js" data-website-id="YOUR_WEBSITE_ID"></script>
```

将 `YOUR_WEBSITE_ID` 替换为 Umami 后台生成的 ID。

## Cloudflare Web Analytics

### 特点

- 同样无 cookie，隐私友好
- 数据不设过期限制（免费）
- 地理位置精度：**城市级别**（比 Umami 更精细）

### Automatic setup vs Manual setup

| 方式            | 条件                                   | 操作                     |
| --------------- | -------------------------------------- | ------------------------ |
| Automatic setup | 域名 DNS 托管在 Cloudflare（橙云代理） | 后台开关，无需改代码     |
| Manual setup    | 任意域名                               | 手动添加 `<script>` 标签 |

如果域名 DNS **不在** Cloudflare 托管，只能用 Manual setup。

### 接入步骤

1. 登录 [dash.cloudflare.com](https://dash.cloudflare.com)
2. **Observe → Analytics → Web Analytics → Add a site**
3. 填入域名，选择 Manual setup
4. 获取 `<script>` 标签

### Hugo PaperMod 接入方式

将脚本追加到 `layouts/_partials/extend_head.html`：

```html
<script defer src="https://cloud.umami.is/script.js" data-website-id="YOUR_UMAMI_ID"></script>
<!-- Cloudflare Web Analytics -->
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "YOUR_CF_TOKEN"}'></script>
<!-- End Cloudflare Web Analytics -->
```

## 两者对比

|               | Umami (cloud)    | Cloudflare Web Analytics |
| ------------- | ---------------- | ------------------------ |
| 数据存储      | Umami 服务器     | Cloudflare               |
| 地理精度      | 国家             | 城市                     |
| 数据保留      | 6 个月（免费版） | 不限                     |
| Cookie        | 无               | 无                       |
| GDPR 同意弹窗 | 不需要           | 不需要                   |
| 自定义事件    | 支持             | 有限支持                 |
