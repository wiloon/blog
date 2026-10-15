---
title: "WCAG: Web 内容无障碍指南"
author: "-"
date: 2026-10-15T17:41:14+08:00
lastmod: 2026-10-15T17:41:14+08:00
url: wcag
categories:
  - web
tags:
  - wcag
  - accessibility
  - a11y
  - css
  - remix
  - AI-assisted
---

WCAG 全称 Web Content Accessibility Guidelines，中文一般译作「Web 内容无障碍指南」，是 W3C 发布的一套规范，规定网页要做到什么程度，才能让视力、听力、行动或认知有障碍的人也能正常使用。这里的「障碍」范围比想象中宽：色弱、老花、在强光下看手机、手腕受伤只能用键盘，都算在内。

我第一次认真对照它，是给自己的项目调灰色辅助文字的颜色：原来的灰字在白底上对比度 4.7:1，刚好过线；在浅灰背景上只有 4.3:1，没过线。下面是我整理的要点。

## 版本

| 版本 | 发布时间 | 说明 |
| ---- | -------- | ---- |
| WCAG 2.0 | 2008-12 | 后来被采纳为国际标准 ISO/IEC 40500:2012 |
| WCAG 2.1 | 2018-06 | 在 2.0 上增加移动端、低视力、认知相关的条款 |
| WCAG 2.2 | 2023-10 | 再增加 9 条（如焦点不能被遮挡、点击目标最小尺寸），删除了过时的 4.1.1 Parsing |
| WCAG 3.0 | 草案 | 打算换一套评分模型，还没定稿，不能拿来做合规依据 |

2.x 各版本向后兼容：满足 2.2 就自动满足 2.1 和 2.0。现在各国法规引用最多的是 2.1 AA，新项目直接按 2.2 AA 做就行。

## 四个原则：POUR

所有条款归在四个原则下：

- **Perceivable（可感知）**：信息要能被感知到。图片有替代文字，视频有字幕，文字和背景有足够对比度，不能只靠颜色传达信息。
- **Operable（可操作）**：界面要能被操作。所有功能都能用键盘完成，焦点位置看得见，不设置让人来不及反应的时间限制。
- **Understandable（可理解）**：内容和操作方式要能看懂。页面声明语言，表单出错时说明错在哪、怎么改，同样的控件在不同页面行为一致。
- **Robust（健壮）**：能被各种浏览器和辅助技术（如读屏软件）正确解析。主要靠语义化 HTML 和正确使用 ARIA。

## 三个等级：A、AA、AAA

每条「成功标准」（success criterion）都标了等级：

- **A**：最低要求，做不到会让一部分人完全用不了。例如 2.1.1 键盘可操作。
- **AA**：通行的合规目标，法规和公司规范基本都要求到这一级。例如 1.4.3 文字对比度 4.5:1。
- **AAA**：最高要求，W3C 自己也说不建议把整站 AAA 作为目标，因为有些内容做不到。例如 1.4.6 文字对比度 7:1。

说「符合 WCAG 2.2 AA」，意思是 A 级和 AA 级的条款全部满足。

## 常用条款

做前端时最常碰到的几条：

| 编号 | 名称 | 等级 | 要求 |
| ---- | ---- | ---- | ---- |
| 1.1.1 | Non-text Content | A | 图片、图标按钮要有文字替代（`alt`、`aria-label`） |
| 1.4.1 | Use of Color | A | 不能只用颜色区分信息，比如表单错误不能只把边框变红 |
| 1.4.3 | Contrast (Minimum) | AA | 正文对比度至少 4.5:1，大字至少 3:1 |
| 1.4.11 | Non-text Contrast | AA | 输入框边框、图标、焦点框等界面元素和相邻颜色对比度至少 3:1 |
| 2.1.1 | Keyboard | A | 所有功能都能只用键盘操作 |
| 2.4.7 | Focus Visible | AA | 键盘焦点所在的元素要看得出来 |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | 获得焦点的元素不能被吸顶栏、浮层完全挡住（2.2 新增） |
| 2.5.8 | Target Size (Minimum) | AA | 点击目标至少 24×24 CSS 像素，或者周围留够间距（2.2 新增） |
| 3.3.1 | Error Identification | A | 表单出错时用文字指出哪里错了 |

一个常见的坑：只在鼠标悬停时才显示的按钮，如果键盘聚焦时不显示，就违反了 2.4.7。写 CSS 时，`:hover` 显示的东西，`:focus-visible` 也要显示。

## 对比度怎么算

1.4.3 是最容易量化、也最常被违反的一条。对比度公式：

```text
contrast = (L1 + 0.05) / (L2 + 0.05)
```

L1 是较亮颜色的相对亮度（relative luminance），L2 是较暗颜色的。结果在 1:1（同色）到 21:1（黑白）之间。

相对亮度的算法：把 sRGB 的每个通道换算成线性值，再按人眼对红绿蓝的敏感度加权：

```js
// Relative luminance of an sRGB colour, per WCAG 2.x
function luminance(r, g, b) {
  const linear = (c) => {
    c /= 255
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
  }
  return 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b)
}

function contrast(a, b) {
  const [hi, lo] = [luminance(...a), luminance(...b)].sort((x, y) => y - x)
  return (hi + 0.05) / (lo + 0.05)
}

contrast([0x73, 0x73, 0x73], [0xff, 0xff, 0xff]) // ~4.7, passes AA for body text
contrast([0x73, 0x73, 0x73], [0xf5, 0xf5, 0xf5]) // ~4.3, fails AA
```

几个要点：

- 「大字」指 18pt（约 24px）及以上，或 14pt（约 18.7px）及以上的粗体。大字的门槛是 3:1。
- 禁用状态的控件、纯装饰的文字、logo 不受这条约束。
- 只算前景和直接背景这两个颜色。灰字放在浅灰卡片上，要和卡片的颜色比，不是和页面的白色比。我那次的问题就出在这里：灰字在白底上合格，放进浅灰背景就不合格了。
- 如果用 OKLCH 定义灰色，有个方便的性质：中性灰的 L 值的三次方就是相对亮度。L=0.556 的灰，亮度约 0.172，对白底 (1+0.05)/(0.172+0.05) ≈ 4.7。把 L 降到 0.5，就是 6.0:1。

## 怎么检查

- **Chrome DevTools**：在 Elements 面板里点颜色值打开取色器，会直接显示对比度，以及 AA、AAA 是否达标。
- **Lighthouse**：DevTools 里的 Lighthouse 有 Accessibility 一项，能扫出对比度不足、缺 `alt`、缺表单标签等问题。
- **axe DevTools**：Deque 出的浏览器扩展，规则比 Lighthouse 全，也能在 Playwright、Jest 里跑（`@axe-core/playwright`、`jest-axe`）。
- **WebAIM Contrast Checker**：网页版对比度计算器，输入两个颜色就出结果。
- **只用键盘走一遍**：拔掉鼠标，用 Tab、Shift+Tab、Enter、Esc 把主要流程走完，看焦点在哪、能不能操作。自动工具只能查出一部分问题，这一步查不出来的要靠人。

## 和法规的关系

WCAG 本身只是 W3C 的建议，没有强制力，但很多法规直接引用它：

- **美国**：ADA 相关诉讼和和解里普遍以 WCAG 2.1 AA 为标准；Section 508（联邦政府采购）引用 WCAG 2.0 AA。2024 年美国司法部的新规要求州和地方政府的网站达到 WCAG 2.1 AA。
- **欧盟**：《欧洲无障碍法案》（European Accessibility Act）从 2025-06-28 起适用，覆盖电商、银行等面向消费者的数字服务，配套标准 EN 301 549 引用 WCAG 2.1 AA。
- **中国**：有推荐性国标 GB/T 37668-2019《信息技术 互联网内容无障碍可访问性技术要求与测试方法》，内容和 WCAG 2.0 基本对应。

个人项目一般不会被强制要求，但做到 AA 并不难，大部分条款本来就是好的设计习惯。

## 参考

- [WCAG 2.2（W3C Recommendation）](https://www.w3.org/TR/WCAG22/)
- [How to Meet WCAG（快速参考，可按等级和技术筛选）](https://www.w3.org/WAI/WCAG22/quickref/)
- [Understanding SC 1.4.3: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
