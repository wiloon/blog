---
title: angular material
author: "-"
date: 2019-06-08T08:38:12+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: angular-material
categories:
  - Web
tags:
  - angular
  - remix
  - AI-assisted
aliases:
  - /p14477/
---
## angular material

```bash
yarn add @angular/material @angular/cdk @angular/animations

app.module.ts

import { MatSliderModule } from '@angular/material/slider';
  
import 'hammerjs';
  
…
  
@NgModule ({....

imports: [...,

MatSliderModule,
  
…]
  
})
```

app.component.html
  
```html
<mat-slider min="1" max="100" step="1" value="1"></mat-slider>
```

styles.css

```css
@import '@angular/material/prebuilt-themes/deeppurple-amber.css';
```

[https://material.angular.io/](https://material.angular.io/)
  
[https://material.angular.cn/guides](https://material.angular.cn/guides)
  
[https://github.com/stbui/angular-material-app/tree/master/src/app](https://github.com/stbui/angular-material-app/tree/master/src/app)
  
[https://material.io/](https://material.io/)
  
[https://material.angular.io/components/categories](https://material.angular.io/components/categories)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Web | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
