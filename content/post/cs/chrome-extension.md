---
title: Chrome Extension 开发笔记
author: "-"
date: 2019-04-21T16:09:22+00:00
lastmod: 2026-10-04T11:49:37+08:00
url: chrome/extension
categories:
  - Web
tags:
  - chrome-extension
  - manifest-v3
  - content-script
  - service-worker
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

## content script 与 service worker 的分工和通信

### 各自负责什么

| 对比项 | content script | service worker（background） |
| --- | --- | --- |
| 运行位置 | 注入到网页里，每个匹配的 tab（以及 `all_frames` 打开时的每个 frame）各一份 | 整个扩展只有一个，运行在扩展自己的后台 |
| DOM | 能读写所在页面的 DOM | 没有 DOM，也没有 `window`、`document`、`localStorage` |
| 页面的 JS 变量 | 访问不到，运行在 isolated world | 访问不到 |
| 可用的 chrome API | 只有一小部分：`chrome.runtime`（发消息、`getURL` 等）、`chrome.storage`、`chrome.i18n` | 按 manifest 里申请的 `permissions` 全部可用：`tabs`、`scripting`、`cookies`、`alarms`、`contextMenus` 等 |
| 网络请求 | `fetch()` 按所在页面的 origin 处理，受页面 CORS 限制 | 对 `host_permissions` 里的域名 `fetch()` 不受 CORS 限制 |
| 生命周期 | 跟着页面走，页面刷新或关闭就没了 | 事件驱动，空闲约 30 秒被回收，有事件再拉起（见下一节） |

一句话概括：content script 负责“页面里看得见的部分”，比如读取用户选中的文字、在页面上插入按钮或浮层；service worker 负责“页面之外的部分”，比如调用后端 API、保存登录 token、管理 tab、响应扩展图标点击和右键菜单。两边都做不了对方的事，所以绝大多数扩展功能都是两者配合完成的。

isolated world 的意思是：content script 和页面共享同一棵 DOM，但各自有独立的 JS 全局环境。页面定义的 `window.foo` 在 content script 里读不到，content script 定义的变量页面也读不到。如果确实需要拿页面 JS 里的数据，要往页面里注入一段脚本（文章开头提到的 Injected Script，或者 `chrome.scripting.executeScript` 指定 `world: "MAIN"`），再通过 `window.postMessage` 把数据传回 content script。

### 为什么这样设计

- **权限分离**：content script 跑在任意网页里，网页内容是不可信的。只给它最小的 API 集合，即使页面有办法影响 content script 的行为，也拿不到 `cookies`、`tabs` 这类高权限 API。高权限操作集中在 service worker，service worker 收到消息时要把它当成不可信输入来校验。
- **和页面互相隔离**：isolated world 让页面脚本无法篡改扩展的变量和函数，扩展也不会污染页面的全局变量，两边用到同名变量、不同版本的库都不会冲突。
- **节省资源**：开 50 个 tab 就有 50 份 content script，如果每份都自己维护登录状态、轮询后端，开销会很大。把这些集中到唯一的 service worker 里，并且空闲时回收，是 MV3 用 service worker 替换常驻 background page 的主要原因。

### 怎么通信

两者不在同一个 JS 环境里，不能互相调用函数，只能通过消息传递和共享存储交互。

#### 一次性消息：sendMessage / onMessage

适合“请求 → 响应”这类场景，最常用。content script 发给 service worker 用 `chrome.runtime.sendMessage`：

```javascript
// content.js
document.addEventListener("mouseup", async () => {
  const word = window.getSelection().toString().trim();
  if (!word) return;
  // In MV3, sendMessage returns a Promise when no callback is passed
  const resp = await chrome.runtime.sendMessage({ type: "LOOKUP", word });
  showTooltip(resp.definition);
});
```

```javascript
// service-worker.js
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type !== "LOOKUP") return;
  // sender.tab tells which tab the message came from
  lookup(msg.word).then((definition) => sendResponse({ definition }));
  // Return true to keep the channel open for an async sendResponse
  return true;
});

async function lookup(word) {
  const { token } = await chrome.storage.local.get("token");
  const r = await fetch(`https://api.example.com/dict?q=${encodeURIComponent(word)}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return (await r.json()).definition;
}
```

`onMessage` 的回调里如果要异步调用 `sendResponse`，必须同步 `return true`，否则通道会立刻关闭，content script 那边拿到的是 `undefined`。这是最常见的坑。

反方向，service worker 发给某个 tab 里的 content script，用 `chrome.tabs.sendMessage(tabId, msg)`，content script 那边同样用 `chrome.runtime.onMessage` 接收。如果目标 tab 里没有注入 content script（域名不在 `matches` 里、页面是安装扩展之前打开的、或者是 `chrome://` 页面），会报 `Could not establish connection. Receiving end does not exist.`。

#### 长连接：connect / Port

需要连续多次来回的场景（比如流式返回结果、持续同步状态），用 `chrome.runtime.connect` 建一个 `Port`：

```javascript
// content.js
const port = chrome.runtime.connect({ name: "stream" });
port.onMessage.addListener((msg) => appendChunk(msg.chunk));
port.postMessage({ type: "START", text: document.body.innerText });
```

```javascript
// service-worker.js
chrome.runtime.onConnect.addListener((port) => {
  if (port.name !== "stream") return;
  port.onMessage.addListener(async (msg) => {
    for await (const chunk of streamFromApi(msg.text)) {
      port.postMessage({ chunk });
    }
  });
});
```

service worker 被回收时 port 会断开，content script 要监听 `port.onDisconnect`，按需重连。

#### 共享存储：chrome.storage

`chrome.storage` 两边都能用，适合放配置、开关这类“状态”，而不是“请求”。一边写入，另一边用 `chrome.storage.onChanged` 监听变化，不需要显式发消息。例如在 popup 里切换开关，各个 tab 里的 content script 通过 `onChanged` 立即生效。

注意 `chrome.storage.session` 默认只有扩展自己的页面和 service worker 能访问，content script 要用的话，service worker 里需要先调用 `chrome.storage.session.setAccessLevel({ accessLevel: "TRUSTED_AND_UNTRUSTED_CONTEXTS" })`。token 这类敏感数据放在 service worker 侧，不建议开放给 content script。

### 一次完整的交互

以“选中单词显示释义”为例：

1. content script 监听 `mouseup`，拿到选中的文字（只有它能读 DOM）。
1. content script 用 `sendMessage` 把单词发给 service worker。
1. service worker 被唤醒（如果之前是 Inactive），从 `chrome.storage` 读 token，带着 token 请求后端 API（只有它能跨域请求、持有凭证）。
1. service worker 通过 `sendResponse` 把结果返回。
1. content script 在页面上渲染浮层（又回到只有它能做的 DOM 操作）。

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
- <https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts>
- <https://developer.chrome.com/docs/extensions/develop/concepts/messaging>

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-09-22 | 新增「host_permissions」章节，说明它和 `content_scripts.matches`、`activeTab` 的区别，并记录 enx-chrome 清理遗留 host_permissions 条目的真实案例 | 排查 enx-chrome 的 host_permissions 时把结论沉淀成笔记 |
| 2026-10-04 | 新增「content script 与 service worker 的分工和通信」章节，包括职责对比、设计原因、sendMessage / Port / chrome.storage 三种通信方式和完整交互示例；title 改为 `Chrome Extension 开发笔记`；补充参考链接 | 原文只有一句话的组成说明，缺少两者如何配合的说明 |
