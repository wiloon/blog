---
title: "tsrs: 在 ENX 项目里试用 Rust 版 TypeScript 类型检查器"
author: "-"
date: 2026-10-21T09:50:35+08:00
lastmod: 2026-10-21T09:50:35+08:00
url: tsrs
categories:
  - web
tags:
  - typescript
  - tsrs
  - rust
  - oxc
  - enx
  - remix
  - AI-assisted
---

## 起因

先是在微信公众号上看到一篇介绍 tsrs 的文章，又读了 Cloudflare 的公告 [Porting TypeScript to Rust](https://blog.cloudflare.com/typescript-rust-port/)。tsrs 在 Oxc 项目下孵化，Oxc 属于尤雨溪的 VoidZero。我一直关注尤雨溪的动向，早年也用过 Vue，对他团队出的东西比较信任，所以想在自己的项目 ENX 上试一下。

ENX 有两个 TypeScript 前端：enx-ui（Next.js）和 enx-chrome（Chrome 扩展，Vite 构建）。两边现在都用 TypeScript 6.0.3。

## tsrs 是什么

- 把 TypeScript 7 的 Go 版编译器（tsgo）逐个函数移植到 Rust，命令行用法和 `tsc` 一样，许可证是 Apache-2.0。
- 由 Owner.com 的 Max Schwenk 发起，Cloudflare 和 VoidZero 参与，和 TypeScript 团队有合作。它不是 fork，语言方向仍由 TypeScript 团队决定。
- 对齐的是 TypeScript 7.1 开发版（`microsoft/TypeScript@b85298b6a81f`）。官方一致性测试的 13,462 条错误基线通过了 13,458 条，作者说剩下 4 条是测试工具本身的问题。
- Cloudflare 的数据：同样数量的检查线程下，tsrs 比 TypeScript 7.0 快最多 8 倍，内存少约 70%。
- 仓库 2026-10-01 才建，到我试的时候已经发到 0.18.0。仓库不接受 PR。不支持 `--init` 和 `--showConfig`，没有 Intel Mac 二进制，Windows 包还没发布。

## 试用过程

为了不动项目依赖，我把 tsrs 装在一个临时目录里，再用它的二进制去检查两个前端：

```sh
# install outside the project
pnpm add -D tsrs@0.18.0-ts7.1.0-dev.20260929

# run against the project's own tsconfig
tsrs -p tsconfig.app.json --noEmit
```

有个小坑：npm 上的版本号带后缀，`tsrs@0.18.0` 解析不到，要写完整的 `0.18.0-ts7.1.0-dev.20260929`。想临时跑一下，也可以用 `pnpm dlx` 加完整版本号。

### 速度和内存

机器是 Apple Silicon Mac。每项跑 3 次，取大致的值：

| 项目 | tsc 6.0.3 | tsrs 0.18.0 |
| --- | --- | --- |
| enx-chrome（`tsconfig.app.json`，2630 个文件） | 约 2.3 秒，峰值内存 584 MB | 约 0.16 秒 |
| enx-ui（关掉 incremental，约 2245 个文件） | 约 3.0 秒，峰值内存 685 MB | 约 0.16 秒，峰值内存 185 MB |
| 当前代码的报错数 | 0 | 0 |

注意这里比的是 TypeScript 6 的 JS 版 `tsc`，不是官方的 TypeScript 7（tsgo）。所以这组数字比 Cloudflare 公布的倍数大很多。

### 报错是否一致

跑这么快，我担心它是不是根本没在检查。于是复制了一份 enx-chrome，加了一个故意写错的文件：引用不存在的模块、把字符串赋给 number、调用 string 上不存在的方法、参数没用到、`chrome.tabs.query` 传错类型。

两边报出的 7 个错误完全一样，只差一个列号：没用到的 import，`tsc` 报在第 1 列，tsrs 报在第 10 列。这属于 TypeScript 7 的行为变化。

两个前端的 tsconfig 也没用 TypeScript 7 删掉的选项（`baseUrl`、ES5、AMD 等），不用改配置就能直接跑。

## 为什么暂时不用

结论是现在不把 tsrs 放进 ENX 的生产工具链，原因有四条：

1. 收益不大。现在一次类型检查也就两三秒，CI 的时间主要花在装依赖、跑测试和构建镜像上。
2. 替换不了 `typescript` 包。`next build` 自带的类型检查和 typescript-eslint 都依赖 TypeScript 的 JS API。加了 tsrs 只是多一个检查器，`typescript` 包还得留着。
3. 版本对不上。tsrs 按 TypeScript 7.1 的规则检查，而项目、编辑器和 `next build` 用的都是 TypeScript 6。两套规则并存，容易出现一边报错、另一边不报的情况。
4. 项目太新。三周发了十几个版本，npm scope 还从 `@ts-rs` 改成了 `@tsrs`。进生产构建链路的东西，我希望它先稳定下来。

## 以后怎么用

等 ENX 升级到 TypeScript 7 时再评估：在官方 tsgo 和 tsrs 之间选一个。到那时如果 tsrs 已经发了对齐 TypeScript 7.1 的稳定版，包名也不再变，第一步可以先替换 enx-chrome 构建脚本里的 `tsc -p tsconfig.app.json`。这一步只做类型检查，不产出文件，换起来风险最小。

后续进展在 ENX 的 GitHub issue [#247](https://github.com/wiloon/enx/issues/247) 里跟踪。

## 相关

- [TypeScript](./typescript.md)
- [oxc-project/tsrs](https://github.com/oxc-project/tsrs)
- [tsrs compatibility](https://github.com/oxc-project/tsrs/blob/main/docs/COMPATIBILITY.md)
