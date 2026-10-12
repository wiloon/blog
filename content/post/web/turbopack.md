---
title: "Turbopack"
author: "-"
date: 2026-06-10T18:58:06+08:00
lastmod: 2026-10-12T13:36:22+08:00
url: turbopack
categories:
  - web
tags:
  - turbopack
  - bundler
  - webpack
  - nextjs
  - pnpm
  - rust
  - remix
  - AI-assisted
---

Turbopack 是 Vercel 开发的 JavaScript/TypeScript 打包工具（bundler），用 Rust 编写，定位是 Webpack 的继任者。它目前主要通过 Next.js 使用：从 Next.js 16 开始，`next dev` 和 `next build` 默认都用 Turbopack。

## 打包工具做什么

浏览器不能直接运行一个现代前端项目的源码：TypeScript 和 JSX 要编译成 JavaScript，`import` 了上百个 npm 包的模块图要合并、拆分成若干个文件，CSS、图片要处理，生产环境还要压缩、去掉没用到的代码（tree shaking）。打包工具做的就是这件事：从入口文件出发，沿着 `import` 建出完整的模块图，再按规则输出浏览器和 Node.js 能直接加载的文件。

Next.js 这类同时有服务端和客户端代码的框架，还要求打包工具同时产出两套结果：服务端渲染用的代码，和发给浏览器的代码。

常见的打包工具：

| 工具      | 实现语言 | 说明                                                     |
| --------- | -------- | -------------------------------------------------------- |
| Webpack   | JS       | 2012 年起的事实标准，插件和 loader 生态最大              |
| Rollup    | JS       | 偏库打包，Vite 的生产构建原先基于它                      |
| esbuild   | Go       | 速度快，常被其他工具当作底层编译器                       |
| Vite      | JS       | 开发模式基于浏览器原生 ESM，正在把底层换成 Rust 实现     |
| Turbopack | Rust     | Vercel 出品，与 Next.js 绑定                             |

## 背景

Webpack 统治前端工程化十余年，但它用 JavaScript 实现，项目一大，冷启动和热更新都慢。Vercel 在 2022 年随 Next.js 13 发布了 Turbopack 的 alpha 版。Webpack 的原作者 Tobias Koppers 是 Turbopack 的核心作者之一。

## 发展时间线

| 时间           | 版本                 | 状态                                                     |
| -------------- | -------------------- | -------------------------------------------------------- |
| 2022-10        | Next.js 13           | alpha，`next dev --turbo` 试用                           |
| 2024-10        | Next.js 15           | 开发模式（`next dev --turbopack`）稳定                   |
| 2025-08        | Next.js 15.5         | 生产构建（`next build --turbopack`）进入 beta            |
| 2025-10        | Next.js 16           | 开发和生产构建都默认使用 Turbopack，Webpack 改为可选     |
| 2026-10        | Next.js 16.4         | 新增实验性配置 `experimental.turbopackAdditionalRoots`   |

所以我在这篇文章最初版本里写的「生产构建仍在开发中」已经过时。现在一个 Next.js 16 项目跑 `next build`，日志第一行就会显示：

```text
▲ Next.js 16.4.0 (Turbopack)
```

想退回 Webpack，要显式加参数：

```bash
next build --webpack
```

## 为什么快

- **Rust 实现**：解析 AST、代码转换这类 CPU 密集的工作用 Rust 做，并且能用满多核。
- **增量计算引擎**：Turbopack 底层是 Turbo 引擎，它把构建过程拆成大量函数，按函数缓存计算结果。改了一个文件，只有依赖它的那部分函数需要重新执行。开发模式下热更新（HMR）的耗时因此基本不随项目规模增长。
- **按需编译**：开发模式只编译当前打开的页面实际用到的模块。

## 项目根目录（root）

这是我在实际项目里踩到的一点，值得单独说。

Turbopack 只解析**项目根目录以内**的文件。根目录默认是从 `next.config` 所在目录往上找到的第一个 lockfile（`pnpm-lock.yaml`、`package-lock.json`、`yarn.lock` 等）所在的目录。这样做是为了缓存校验更可靠、文件监听开销更小，构建结果也和机器上的其他目录无关。

问题出在依赖不在项目里的情况。pnpm 的 `node_modules` 本来就大量使用符号链接；如果虚拟 store 被放到了项目目录之外，`node_modules/next` 就是一个指向项目外的链接，Turbopack 不会跟过去，`next build` 直接失败：

```text
Error: Turbopack build failed with 1 error:
./src/app
Error: Could not find the Next.js package (next/package.json)
```

会遇到这种情况的场景：

- 开启了 pnpm 的全局虚拟 store（`enableGlobalVirtualStore`）
- `npm link` 了项目外的包
- 用 Heroku 的 Cloud Native Buildpack 构建：它把 pnpm 的虚拟 store 放在单独的 layer `/layers/heroku_nodejs/virtual` 里

同一个项目用 `next build --webpack` 能构建通过，因为 Webpack 会照常跟随符号链接。

解决办法有两个：

1. 把 `turbopack.root` 设成能同时包含项目和依赖的上级目录。官方文档提醒不要设得太大（比如家目录），否则 Turbopack 会监听大量无关文件。
1. Next.js 16.4 起，用实验性配置 `experimental.turbopackAdditionalRoots` 声明额外的根目录。Turbopack 只会在符号链接处跨进这些目录；使用 `output: 'standalone'` 时，这些目录里被用到的文件也会复制进 standalone 输出：

```ts
// next.config.ts
const nextConfig = {
  experimental: {
    turbopackAdditionalRoots: {
      // Root name: 1-40 chars of letters, digits, "_" or "-"
      cnbPnpmVirtualStore: {
        path: '/layers/heroku_nodejs/virtual',
        // Skip silently where the directory does not exist (local dev)
        ignoreIfMissing: true,
      },
    },
  },
}

export default nextConfig
```

## 和 Vite 的区别

| 对比项       | Vite                                   | Turbopack                    |
| ------------ | -------------------------------------- | ---------------------------- |
| 开发模式     | 浏览器原生 ESM，按需加载，不预先打包   | 增量打包 + 函数级缓存        |
| 实现语言     | JS，底层正在换成 Rust 实现的 Rolldown  | Rust                         |
| 生产构建     | 有                                     | 有（Next.js 16 起默认）      |
| 框架         | 与框架无关（Vue、React、Svelte 等）    | 目前基本只用于 Next.js       |
| 插件生态     | Rollup/Vite 插件                       | 兼容部分 Webpack loader      |

如果项目用 Next.js，Turbopack 已经是默认选项，一般不需要再考虑别的；不用 Next.js 的项目，Vite 是更常见的选择。

## 和 Webpack 的兼容性

Turbopack 能运行一部分 Webpack loader（如 `@svgr/webpack`、`sass-loader`、`raw-loader`），通过 `turbopack.rules` 配置。只返回 JavaScript 的 loader 基本可用；依赖 `this.emitFile`、`this.loadModule` 等 API 的 loader 不支持。Webpack 插件（plugin）不能直接使用。

## 参考

- [Next.js：Turbopack API reference](https://nextjs.org/docs/app/api-reference/turbopack)
- [Next.js：next.config.js turbopack 配置（含 root 与 Additional roots）](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack)
- [pnpm #14972：Global virtual store 下 Next.js 16 + Turbopack 构建失败](https://github.com/pnpm/pnpm/issues/14972)
- [next.js #93556：Turbopack fails to resolve next/package.json with pnpm v11 enableGlobalVirtualStore](https://github.com/vercel/next.js/issues/93556)

## 维护记录

| 时间       | 修改内容                                                                                                    | 原因                                               |
| ---------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| 2026-10-12 | 补充打包工具的作用、发展时间线、项目根目录与符号链接问题、`turbopackAdditionalRoots`；删除未注明来源的性能数据；更新参考链接 | 原文「生产构建仍在开发中」已过时；记录 enx-ui 用 CNB 构建时遇到的问题 |
