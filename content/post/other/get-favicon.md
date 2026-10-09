---
title: favicon
author: "-"
date: 2014-03-19T07:03:48+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: get-favicon
categories:
  - Web
tags:
  - html
  - remix
  - AI-assisted
aliases:
  - /获取网站favicon/
---
## favicon
获取网站favicon

http://www.google.com/s2/favicons?domain=google.com

home.html 代码如下: 

```html
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>home page</title>
</head>
<body>
home page
</body>
</html>
```

下面两行代码就可以告诉浏览器使用wangyi.ico 作为home.html的图标了: 

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `get-favicon.md`；url 改为 `get-favicon`；旧 url 加入 aliases；categories 改为 Web | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
