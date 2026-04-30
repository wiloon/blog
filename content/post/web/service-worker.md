---
author: "-"
date: 2026-04-30T16:58:02+08:00
title: "Service Worker"
url: service-worker
categories:
  - web
tags:
  - service-worker
  - remix
  - AI-assisted
---

## 解决的问题

**1. 离线体验**

传统 Web 应用断网即不可用。Service Worker 可拦截网络请求，从缓存中返回资源，让应用在无网络时仍能运行。

**2. 网络性能**

可缓存静态资源（HTML、CSS、JS、图片），后续请求直接走缓存，减少网络延迟，加快页面加载速度。

**3. 推送通知（Push Notifications）**

即使页面未打开，Service Worker 也能在后台接收服务器推送的消息并展示通知。

**4. 后台同步（Background Sync）**

当用户在离线状态下提交表单或操作时，Service Worker 可在网络恢复后自动重试，保证数据最终被发送到服务器。

**5. 独立于页面生命周期**

它是独立于页面的后台进程，页面关闭后仍可运行，适合处理跨页面共享的复杂逻辑。

**核心本质**：Service Worker 是一个可编程的网络代理，让开发者能完全控制"请求如何被响应"，这是 Web 平台此前缺失的能力。

## 概述

Service Worker 是浏览器在后台独立于网页运行的脚本，本质上充当 Web 应用程序、浏览器与网络之间的代理服务器。

- 是一种 JavaScript Worker，无法直接访问 DOM
- 通过响应 `postMessage` 接口发送的消息与页面通信
- 不用时会被中止，下次有需要时重启——不能依赖全局状态，持久数据应使用 IndexedDB
- 广泛使用 Promise
- 是浏览器中的独立进程（非内核线程），注册后可被多个页面共用，页面关闭后不会销毁

## Chrome 调试

```text
chrome://inspect/#service-workers
chrome://serviceworker-internals
```

## 参考

- <https://juejin.im/post/6844903613270081543>
