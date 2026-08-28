---
title: "WeChat QR to PDF: 微信扫码查看与下载 PDF"
author: "-"
date: 2026-08-28T20:27:31+08:00
lastmod: 2026-08-28T20:27:31+08:00
url: wechat-qr-pdf-cloudflare-pages
categories:
  - web
tags:
  - cloudflare
  - github
  - pdf
  - wechat
  - qrcode
  - remix
  - AI-assisted
---

设计目标：用户用微信扫事先印好的二维码，在手机里查看 PDF，并能下载。技术栈固定为自购域名、GitHub 私有仓库、Cloudflare Pages、离线生成二维码。不使用 Hugo，也不需要后端。

域名购买、DNS 切到 Cloudflare、Pages 绑自定义域名的操作步骤，与本站博客相同，见 [Hugo + Cloudflare Pages 搭建个人博客](./hugo-cloudflare-pages-blog-setup.md)。本文只写和「微信扫码 + PDF」有关的设计选择。

## 目标与非目标

**目标**

- 微信扫码打开 HTTPS 页面，能预览 PDF
- 页面上提供下载
- PDF 源文件放在 GitHub 私有仓库里，不在 GitHub 网页上公开浏览
- 更新 PDF 时尽量不换二维码（同一 URL 覆盖文件即可）

**非目标**

- 不做登录、不做按人授权。知道链接的人都能打开
- 不接入微信公众号、JS-SDK、微信支付
- 不在微信里做「仅好友可见」之类的权限
- 单文件超过 Cloudflare Pages 限制（25 MiB）时，本方案不够，需改对象存储

## 整体结构

二维码里只放一个 URL，不放 PDF 本身。扫码等于用微信内置浏览器打开这个地址。

```text
Printed QR  -->  https://files.example.com/catalog/
                    |
                    +-- index.html     landing page
                    +-- catalog.pdf    the file
```

| 组件 | 作用 |
| ---- | ---- |
| 自购域名 | 二维码里的长期地址，例如 `files.example.com` |
| GitHub 私有仓库 | 存放 HTML 和 PDF，只有仓库成员能在 GitHub 上看到 |
| Cloudflare Pages | 从私有仓库拉取并托管静态文件，对外提供 HTTPS |
| 二维码图片 | 事先生成、打印或贴到物料上，内容是落地页 URL |

仓库私有只挡住 GitHub 上的浏览和 clone。部署到 Pages 之后，站点是公开的。这是预期行为：扫码的人没有 GitHub 账号，也必须能打开。

不要把二维码写成 `github.com/.../blob/...` 或 `raw.githubusercontent.com/...`。私有仓库的这类链接会跳登录页，扫码的人打不开。

## 为什么二维码指向页面而不是 PDF

微信内置浏览器对直接打开 `.pdf` 链接不友好：iOS 上经常空白或提示无法预览；Android 上表现不稳定。`<a download>` 在微信里也常常不触发系统下载。

因此二维码指向 **HTML 落地页**，由页面负责预览和下载引导，而不是 `https://files.example.com/catalog.pdf`。

落地页要做三件事：

1. 用 PDF.js 把 PDF 画到 canvas 上，在微信 WebView 里预览（不依赖浏览器自带的 PDF 插件）
2. 提供「下载」按钮；若当前是微信内置浏览器，同时提示「点右上角 · 在浏览器打开」
3. 非微信环境（Safari / Chrome）下，下载按钮按普通文件链接处理即可

检测微信内置浏览器用 User-Agent 中的 `MicroMessenger` 即可，不需要微信开放平台。

## 仓库内容

没有构建步骤。Cloudflare Pages 的 Build command 留空，Output directory 填仓库根目录（或约定的 `public/`）。

```text
repo/
  catalog/
    index.html
    catalog.pdf
  assets/
    pdf.min.js
    pdf.worker.min.js
  index.html
```

`assets/` 里放 PDF.js 的本地副本，不要运行时去拉国外 CDN。微信里外链 JS 失败时，预览会整页挂掉。

多份 PDF 就多几个目录，每个目录一个落地页，二维码一对一：

| 物料 | 二维码内容 | 仓库路径 |
| ---- | ---------- | -------- |
| 产品手册 | `https://files.example.com/catalog/` | `catalog/` |
| 价目表 | `https://files.example.com/price/` | `price/` |

根路径 `index.html` 可以只是一份文件列表，也可以做成 404 式的空白页，避免目录被随便翻。需要防遍历时，把路径做成无含义的短码（例如 `/d/a8f3c2/`），仍然只是隐藏，不是权限控制。

落地页的核心结构如下。样式和文案按实际品牌改；预览容器要给一个明确高度，否则微信里容易是空白。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>产品手册</title>
</head>
<body>
  <p id="wechat-tip" hidden>
    预览若无法显示，请点右上角 · 在浏览器打开
  </p>
  <p>
    <a id="download" href="./catalog.pdf">下载 PDF</a>
  </p>
  <canvas id="pdf-canvas"></canvas>
  <script src="/assets/pdf.min.js"></script>
  <script>
    (function () {
      var inWeChat = /MicroMessenger/i.test(navigator.userAgent);
      if (inWeChat) {
        document.getElementById("wechat-tip").hidden = false;
      }
      pdfjsLib.GlobalWorkerOptions.workerSrc = "/assets/pdf.worker.min.js";
      pdfjsLib.getDocument("./catalog.pdf").promise.then(function (pdf) {
        return pdf.getPage(1);
      }).then(function (page) {
        var canvas = document.getElementById("pdf-canvas");
        var ctx = canvas.getContext("2d");
        var viewport = page.getViewport({ scale: 1.2 });
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        return page.render({ canvasContext: ctx, viewport: viewport }).promise;
      });
    })();
  </script>
</body>
</html>
```

上面只渲染第一页，作为设计示意。多页需要按页循环渲染，或接入 PDF.js 自带的 viewer。第一页能出来，就说明文件地址、MIME、JS 都通了。

## 域名与 Pages

1. 购买域名（任意注册商）。二维码会印到实物上，选短、好念、长期能续费的。
2. 把域名的 Nameserver 改成 Cloudflare 分配的两个，DNS 由 Cloudflare 托管。
3. GitHub 建 **private** 仓库，放入上一节的目录。
4. Cloudflare Pages → Connect to Git → 授权该私有仓库（Cloudflare 用 OAuth 拉取，仓库对外仍是私有）。
5. 构建设置：Framework 选 None；Build command 空；Output directory `/`。
6. 绑定自定义域名，例如 `files.example.com`。证书由 Cloudflare 签发。

二维码必须写自定义域名，不要写 `*.pages.dev`。`pages.dev` 以后换项目会变；印出去的码很难收回。

路径一旦印到物料上就不要改。更新 PDF：覆盖同路径文件，`git push`，Pages 自动发布。旧码继续有效。

## 二维码

内容是落地页的绝对 URL，带 `https://`，末尾建议带 `/`，和 Pages 的目录约定一致：

```text
https://files.example.com/catalog/
```

生成方式不限：本地 `qrencode`、设计软件、或任意二维码生成器。产物是一张图，用于印刷、贴纸、展架。生成一次即可，不需要服务端动态出码。

打印前用微信扫自己的测试码，确认走的是落地页而不是 PDF 直链。微信识码会把 URL 交给内置浏览器，和系统相机扫码的差异主要在后续预览，不在解码。

## 约束

| 项 | 说明 |
| -- | ---- |
| 单文件大小 | Cloudflare Pages 单个静态文件上限 25 MiB。超过需改 Cloudflare R2，Pages 只留落地页 |
| 仓库体积 | PDF 是二进制，git 历史会变肥。文件少、更新不频繁可以接受；频繁大文件更适合 R2 |
| 公开性 | Pages URL 无鉴权。链接被转发、被拍照，效果和扫官方码一样 |
| 微信下载 | 内置浏览器里「下载」经常只是再次打开预览。可靠下载路径是「在浏览器打开」后由 Safari / Chrome 保存 |
| 大陆访问 | Cloudflare 在部分网络下延迟较高。若扫码现场网络差，预览会慢。这是本方案的已知风险，不是配置错误 |
| 备案 | 只做扫码打开网页，不接微信公众号接口，不强制 ICP。若以后要在公众号菜单里放同样的链接，再按微信侧规则补备案和 JS 安全域名 |

## 实施顺序

1. 买域名，DNS 切到 Cloudflare。
2. 建 GitHub 私有仓库，放入一份测试 PDF 和落地页。
3. Pages 连接仓库，先用分配的 `*.pages.dev` 在微信里扫码自测预览和下载提示。
4. 绑定自定义域名，再用最终 URL 生成正式二维码。
5. 印刷前保留一枚测试码；上线后用覆盖同路径的方式更新 PDF。

自测清单：

- 微信 iOS、微信 Android 各扫一次，第一页能出来
- 非微信浏览器能直接下载
- 未登录 GitHub 的账号打不开仓库，但能打开 Pages URL
- 换一版 PDF 后旧码仍指向新文件

## 和博客那套的差别

本站博客用 Hugo 把 Markdown 编成 HTML，再交给 Pages，见 [Hugo + Cloudflare Pages 搭建个人博客](./hugo-cloudflare-pages-blog-setup.md)。本方案没有编译步骤：仓库里的 HTML 和 PDF 就是线上文件。GitHub 私有、Cloudflare 拉仓、自定义域名这三段是一样的。
