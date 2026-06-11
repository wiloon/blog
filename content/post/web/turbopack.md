---
title: "Turbopack"
author: "-"
date: 2026-06-10T18:58:06+08:00
lastmod: 2026-06-10T18:58:06+08:00
url: turbopack
categories:
  - web
tags:
  - turbopack
  - bundler
  - webpack
  - nextjs
  - remix
  - AI-assisted
---

Turbopack 是由 Vercel 开发的下一代 JavaScript/TypeScript 打包工具（bundler），使用 Rust 编写，定位为 Webpack 的继任者。

## 背景

Webpack 在前端工程化领域统治了十余年，但随着项目规模增大，其构建速度逐渐成为开发体验的瓶颈。Vercel 团队（同时也是 Next.js 的维护者）在 2022 年发布了 Turbopack，目标是在保持兼容性的前提下，大幅提升打包速度。

Turbopack 的核心作者之一 Tobias Koppers，正是 Webpack 的原作者。

## 核心特性

### 极速增量编译

Turbopack 采用**增量计算引擎**（基于 Turbo 引擎），对每个函数的计算结果进行细粒度缓存。只有发生变化的模块才会被重新编译，未变化的部分直接复用缓存结果。

官方数据对比（大型应用）：

| 场景          | Webpack | Turbopack |
| ------------- | ------- | --------- |
| 冷启动（dev） | ~30s    | ~3s       |
| HMR（热更新） | ~3s     | <100ms    |

### Rust 实现

使用 Rust 编写，相比 JavaScript/Node.js 实现的工具，在 CPU 密集型任务（如 AST 解析、代码转换）上有显著的性能优势，并且可以充分利用多核并行。

### 原生支持 TypeScript 和 JSX

无需额外配置，开箱即用地支持 TypeScript、JSX/TSX、CSS Modules 等现代前端常用格式。

### 与 Next.js 深度集成

从 Next.js 13 开始，Turbopack 作为实验性 dev server 引入；Next.js 15 正式将其设为默认开发服务器（`next dev --turbopack`）。

## 与 Vite 的区别

Vite 在开发模式下使用原生 ES Modules（ESM），利用浏览器按需加载，无需打包全部模块；Turbopack 则在开发模式下仍进行打包，但通过增量缓存做到极低的增量编译延迟。

| 对比维度       | Vite               | Turbopack           |
| -------------- | ------------------ | ------------------- |
| 开发模式原理   | 原生 ESM，按需加载 | 增量打包 + 缓存     |
| 实现语言       | Go (esbuild) + JS  | Rust                |
| 生产构建       | Rollup             | Turbopack（开发中） |
| 框架绑定       | 框架无关           | 与 Next.js 深度集成 |
| 冷启动速度     | 极快（无需打包）   | 快，但略逊于 Vite   |
| HMR 规模敏感性 | 模块多时变慢       | 大规模下更稳定      |

## 当前状态（2026）

- **开发服务器**：稳定，Next.js 15 默认启用
- **生产构建**：仍在开发中，尚未正式发布
- **独立使用**：目前主要通过 Next.js 使用，独立 CLI 工具尚不完善

## 使用方式

在 Next.js 项目中启用 Turbopack dev server：

```bash
next dev --turbopack
```

或在 `package.json` 中配置：

```json
{
  "scripts": {
    "dev": "next dev --turbopack"
  }
}
```

## 参考

- [Turbopack 官网](https://turbo.build/pack)
- [Next.js Turbopack 文档](https://nextjs.org/docs/app/api-reference/turbopack)
- [Turbopack GitHub](https://github.com/vercel/turbo)
