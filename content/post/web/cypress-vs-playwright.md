---
author: "-"
date: 2026-05-11T10:27:14+08:00
lastmod: 2026-05-11T10:27:14+08:00
title: "Cypress vs Playwright: E2E 测试框架对比"
url: cypress-vs-playwright
categories:
  - web
tags:
  - cypress
  - playwright
  - testing
  - e2e
  - remix
  - AI-assisted
---

## 概述

Cypress 和 Playwright 是目前最主流的两个 E2E（端到端）测试框架。两者都能模拟真实用户操作来测试 Web 应用，但在架构、能力和适用场景上有明显差异。

## 核心对比

| 维度         | Cypress                         | Playwright                             |
| ------------ | ------------------------------- | -------------------------------------- |
| 开发商       | Cypress.io                      | Microsoft                              |
| 首发年份     | 2017                            | 2020                                   |
| 语言支持     | JS / TS                         | JS / TS / Python / Java / C#           |
| 浏览器支持   | Chrome、Firefox、Edge、Electron | Chrome、Firefox、Safari (WebKit)、Edge |
| 移动端浏览器 | 不支持                          | 支持（模拟移动设备）                   |
| 多标签页     | 有限支持                        | 原生支持                               |
| iframe 支持  | 受限                            | 完整支持                               |
| 并发执行     | 收费云服务 / 第三方插件         | 内置，免费                             |
| API 测试     | 支持                            | 支持（更完整）                         |
| 组件测试     | 成熟                            | 实验性                                 |

## 架构差异

### Cypress

Cypress 运行在**浏览器内部**，测试代码与应用代码共享同一个 JavaScript 运行时。这一设计带来了极低的延迟和实时调试能力，但也造成了一些限制：

- 历史上不支持跨域（cross-origin）场景（v12 起已大幅改善）
- 同一时间只能操作一个标签页
- 不支持 Safari / WebKit

### Playwright

Playwright 运行在**浏览器外部**，通过 Chrome DevTools Protocol（Chrome/Edge）和各浏览器原生协议（Firefox、WebKit）远程控制浏览器。这种架构更接近真实用户操作，且：

- 原生支持多标签页、多窗口
- 原生支持跨域场景
- 覆盖所有主流浏览器，包括 Safari

## 安装与初始化

### Cypress

```bash
npm install --save-dev cypress
npx cypress open
```

### Playwright

```bash
npm init playwright@latest
npx playwright test
```

## 编写测试用例

### Cypress 示例

```javascript
describe('登录页', () => {
  it('用户名密码正确时应跳转到首页', () => {
    cy.visit('/login')
    cy.get('[data-cy=username]').type('admin')
    cy.get('[data-cy=password]').type('secret')
    cy.get('[data-cy=submit]').click()
    cy.url().should('include', '/dashboard')
  })
})
```

### Playwright 示例

```typescript
import { test, expect } from '@playwright/test'

test('用户名密码正确时应跳转到首页', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[data-cy=username]', 'admin')
  await page.fill('[data-cy=password]', 'secret')
  await page.click('[data-cy=submit]')
  await expect(page).toHaveURL(/dashboard/)
})
```

## 自动等待（Auto-waiting）

两个框架都内置了自动等待机制，无需手动 `sleep`。

- **Cypress**：命令链式调用，每个命令自动重试直到超时
- **Playwright**：`await` 语法，等待元素可操作后再执行，并内置网络请求拦截

## 并发与 CI/CD

- **Cypress**：并发测试需要 [Cypress Cloud](https://www.cypress.io/cloud)（收费），开源方案可用 `cypress-parallel` 插件
- **Playwright**：`playwright.config.ts` 中一行配置即可开启 worker 并发，完全免费

```typescript
// playwright.config.ts
export default {
  workers: 4,  // 同时运行 4 个 worker
}
```

## 调试体验

| 功能         | Cypress             | Playwright        |
| ------------ | ------------------- | ----------------- |
| 可视化 UI    | Cypress App（内置） | `--ui` 模式       |
| 时间旅行截图 | ✅                   | ✅（trace viewer） |
| VS Code 插件 | ✅                   | ✅（官方插件）     |
| 断点调试     | 有限                | 完整支持          |
| 网络请求拦截 | `cy.intercept()`    | `page.route()`    |

Playwright 的 **Trace Viewer** 可以录制完整的测试过程（截图、DOM 快照、网络日志），是排查 CI 失败问题的利器。

## 适用场景建议

**选 Cypress，如果：**

- 团队只使用 JavaScript / TypeScript
- 项目以 Chrome 为主要目标浏览器
- 重视组件测试（Component Testing）
- 希望有更平缓的学习曲线和更活跃的社区生态

**选 Playwright，如果：**

- 需要跨浏览器测试（尤其是 Safari）
- 后端团队（Python / Java / C#）也需要参与编写测试
- 需要多标签页、iframe、文件下载等复杂场景
- 在意并发执行成本（Playwright 并发免费）
- 需要移动端浏览器模拟

## 参考

- [Cypress 官方文档](https://docs.cypress.io)
- [Playwright 官方文档](https://playwright.dev)
- [Playwright vs Cypress - Microsoft Blog](https://playwright.dev/docs/why-playwright)
