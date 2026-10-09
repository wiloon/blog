---
title: 'reveal.js, markdown > PPT'
author: "-"
date: 2019-04-16T16:03:17+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: reveal-js-markdown-ppt
categories:
  - Tools
tags:
  - reveal-js
  - markdown
  - remix
  - AI-assisted
aliases:
  - /p14189/
---
## 'reveal.js, markdown > PPT'

### 快捷键

全屏 f , 退出全屏 Esc
上一页 p, 下一页 n/空格
首页 Home, 末页 End
缩略图 Esc 或 o
黑屏 b
演讲提示模式 s
vi导航键: h, j, k, l
  
帮助页面: ?

### 字号

reveal.js的markdown支持4种字号#，##，###，####

### 安装

```bash
# install nodejs
sudo pacman -S nodejs
# install npm
sudo pacman -S npm
# git clone reveal.js
git clone https://github.com/hakimel/reveal.js.git
cd reveal.js
npm install
mv index.html index.html.bak
ln -s scrum/index.html index.html
npm start
npm start -- --port=8001
```

```html
<section data-markdown="example.md" data-separator-notes="^Note:" data-charset="UTF-8">
</section>
```

### 内容左对齐

```html
<style>
    .reveal .slides {
        text-align: left;
    }
    .reveal .slides section>* {
        margin-left: 0;
        margin-right: 0;
    }
</style>
```

### 插入图片并控制样式

路径是相对于 index.html 的路径

```markdown
![An image](scrum/scrum.png)  <!-- .element height="50%" width="50%" -->
```

### 设备字号

```html
<br>
```

https://github.com/hakimel/reveal.js/issues/1349

https://github.com/hakimel/reveal.js#markdown

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Tools | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
