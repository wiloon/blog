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

<https://developer.chrome.com/docs/extensions/mv3/>

- javascript web api: <https://developer.mozilla.org/en-US/docs/Web/API>
- chrome api: <https://developer.mozilla.org/en-US/docs/Web/API>
- html: <https://web.dev/learn/html/>
- css: <https://web.dev/learn/css/>
- javascript: <https://developer.mozilla.org/en-US/docs/Learn/JavaScript>
- chrome extension development overview: <https://developer.chrome.com/docs/extensions/mv3/devguide/>

## chrome extension 的构成

- The manifest, manifest.json, 唯一一个必须要存在于 extension 根目录的文件
- The service worker, service worker 监听 chrome 的各种事件, 可以调用 Chrome api, 但是不能直接操作页面内容
- Content scripts: content script 可以直接在页面中执行 js 代码, 可以直接操作 DOM, 还可以跟 service worker 通信
- The popup and other pages

## crxjs, react

<https://crxjs.dev/vite-plugin>

<https://www.freecodecamp.org/news/chrome-extension-message-passing-essentials/>
