---
title: chrome extension
author: "-"
date: 2019-04-21T16:09:22+00:00
lastmod: 2026-09-22T14:39:33+08:00
url: chrome/extension
categories:
  - Web
tags:
  - chrome-extension
  - manifest-v3
  - enx
  - remix
  - AI-assisted
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

## host_permissions

`manifest.json` 里 `host_permissions` 和 `content_scripts[].matches` 是两个独立字段，容易混为一谈：

- `content_scripts[].matches` 决定 content script **会不会在页面加载时自动注入**到某个域名。这是纯静态的注入开关，跟 `host_permissions` 无关。
- `host_permissions` 决定的是**扩展自己的代码（主要是 background/service worker）能不能对某个域名做编程访问**，具体是三件事：
  1. 跨域 `fetch()`：service worker 里 `fetch()` 一个 `host_permissions` 列出的域名，不受该域名 CORS 策略限制；没列出的域名照样要遵守普通的 CORS 规则。
  2. `chrome.cookies` API：读写某个域名下的 cookie，需要那个域名在 `host_permissions` 里。
  3. 不依赖用户手势、主动对某个 tab 调用 `chrome.scripting.executeScript` 注入脚本，也需要目标域名在 `host_permissions` 里。

反过来，**用户手势触发**（点扩展图标、按快捷键）之后调用 `chrome.scripting.executeScript`，只需要 `activeTab` 权限，不需要 `host_permissions`——`activeTab` 会在触发那一刻临时授予当前 tab 的权限，用完即失效。三者是正交的：

```json
{
  "permissions": ["activeTab", "scripting"],
  "host_permissions": ["https://api.example.com/*"],
  "content_scripts": [
    {
      "matches": ["https://www.example.com/*"],
      "js": ["content.js"]
    }
  ]
}
```

上面这份 manifest：`content.js` 只会自动注入到 `www.example.com`；service worker 能跨域 `fetch` `api.example.com`；用户点图标时可以往**任意**当前 tab 注入脚本（靠 `activeTab`，不受 `host_permissions` 列表限制）。三个字段各管一段，互不依赖。

Chrome Web Store 安装时"此扩展可以读取和更改您访问的所有网站的数据"这条警告，`content_scripts.matches` 和 `host_permissions` 里出现 `<all_urls>` / `http://*/*` / `https://*/*` 都会触发，文案不区分来源。

### 清理无用的 host_permissions

在 enx-chrome（`https://catglish.com` 的浏览器扩展）里查过一次真实案例：`host_permissions` 里躺着 `http://*/*`、`https://*/*`、`https://www.youdao.com/*`、`https://claude.com/blog/*` 四条，但代码里搜不到任何 `chrome.cookies` 或 `chrome.scripting.executeScript` 调用，唯一的跨域 `fetch()` 目标（后端 API）也不是靠这四条撑着的：

- 两条通配符是 2025-11-08 一次给 e2e 测试临时放宽 `content_scripts.matches` 时顺手加的，2026-01-03 收窄 `content_scripts` 时没同步收窄回去，纯属遗留。
- `youdao.com` 那条域名本身就对不上（代码里实际请求的是 `dict.youdao.com`，manifest 写的是 `www.youdao.com`），而且这段代码用的是 `new Audio(url)` 播放发音，浏览器媒体元素跨域加载播放本来就不受 `host_permissions` 限制（不像 `fetch()`）。
- `claude.com/blog` 在代码里零引用，是加这个文章站点到 `content_scripts.matches` 时顺手复制进 `host_permissions` 的，其余同批加入的站点都没有对应条目。

真正需要的后端 API、前端站点、认证服务几个域名，是构建脚本按部署环境（dev/homelab/production）在**构建时**动态拼进 `host_permissions` 的，跟这份写死在源文件里的静态清单完全独立。把这四条清空成 `[]` 后，跑了一遍完整测试（23 个 suite、246 个用例）+ 分别构建 homelab / production 两个 target，跨域 `fetch` 调用的域名在生成的 `dist/manifest.json` 里原样都在，功能没受影响，CWS 那条广泛权限警告的触发源却少了一个。

**经验**：`host_permissions` 里的每一条都要能对应到一个具体的 `fetch()` / `chrome.cookies` / 无 `activeTab` 的 `chrome.scripting.executeScript` 调用；对不上就大概率是加别的东西时顺手带进来的遗留项，可以直接删，删完跑一遍测试和构建产物核对就知道有没有踩到。

## 参考

- <https://developer.chrome.com/docs/extensions/develop/migrate/to-service-workers>
- <https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/basics>

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-09-22 | 新增「host_permissions」章节，说明它和 `content_scripts.matches`、`activeTab` 的区别，并记录 enx-chrome 清理遗留 host_permissions 条目的真实案例 | 排查 enx-chrome 的 host_permissions 时把结论沉淀成笔记 |
