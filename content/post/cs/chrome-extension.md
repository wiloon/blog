---
title: chrome extension
author: "-"
date: 2019-04-21T16:09:22+00:00
url: chrome/extension
categories:
  - Web
tags:
  - reprint
---
## chrome extension

- content script, 只能访问 dom, 不能访问页面 js 变量和函数
- Injected Script, 被插入到页面里的 js 代码

chrome://extensions

puzzle button: chrome extension 图标后面的拼图按钮

## develop

## chrome extension doc

[https://developer.chrome.com/docs/extensions/mv3/](https://developer.chrome.com/docs/extensions/mv3/)

- javascript web api: [https://developer.mozilla.org/en-US/docs/Web/API](https://developer.mozilla.org/en-US/docs/Web/API)
- chrome api: [https://developer.mozilla.org/en-US/docs/Web/API](https://developer.mozilla.org/en-US/docs/Web/API)
- html: [https://web.dev/learn/html/](https://web.dev/learn/html/)
- css: [https://web.dev/learn/css/](https://web.dev/learn/css/)
- javascript: [https://developer.mozilla.org/en-US/docs/Learn/JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript)
- chrome extension development overview: [https://developer.chrome.com/docs/extensions/mv3/devguide/](https://developer.chrome.com/docs/extensions/mv3/devguide/)

## chrome extension 的构成

- The manifest, manifest.json, 唯一一个必须要存在于 extension 根目录的文件
- The service worker, service worker 监听 chrome 的各种事件, 可以调用 Chrome api, 但是不能直接操作页面内容
- Content scripts: content script 可以直接在页面中执行 js 代码, 可以直接操作 DOM, 还可以跟 service worker 通信
- The popup and other pages

## crxjs, react

[https://crxjs.dev/vite-plugin](https://crxjs.dev/vite-plugin)

[https://www.freecodecamp.org/news/chrome-extension-message-passing-essentials/](https://www.freecodecamp.org/news/chrome-extension-message-passing-essentials/)

## background.js

不能直接访问页面的内容, 只能发消息给 content.js

## service worker 的 Inactive 状态 (Manifest V3)

`chrome://extensions` 里 "Inspect views" 后面经常显示 `service worker (Inactive)`, 这是 MV3 的正常行为, 不是报错.

- MV3 把 background 脚本做成事件驱动的 service worker, 空闲约 30 秒左右没有任务 (没有消息/网络请求/定时器) 就会被 Chrome 卸载, 回收内存, 页面上显示为 Inactive
- 有新事件触发时 (点击扩展图标, popup/content script 发消息 `chrome.runtime.onMessage`, `chrome.alarms`, 收到通知点击等), Chrome 会自动重新拉起 service worker, 从头执行一遍顶层代码, 这个过程对用户透明, 只是首次唤醒有零点几秒延迟
- **不能依赖 service worker 内存里的全局变量长期存活**, 每次被唤醒都是一次全新的执行上下文, 之前保存在内存变量里的状态 (比如 token, 计数器) 会丢失
  - 需要跨生命周期保留的状态必须持久化到 `chrome.storage.local` / `chrome.storage.session`, 并在顶层初始化逻辑里主动读回内存
  - 依赖内存去重的逻辑 (比如"合并并发请求, 只发一次" 的 in-flight Promise) 只在同一次 SW 存活期间有效, SW 重启会重置, 设计时要接受这种边界情况
- 调试时点 "service worker (Inactive)" 链接会强制唤醒并打开对应的 DevTools

## 参考

- <https://developer.chrome.com/docs/extensions/develop/migrate/to-service-workers>
- <https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/basics>
