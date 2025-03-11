---
title: jsdom
author: "-"
date: 2015-02-09T02:18:35+00:00
url: jsdom
categories:
  - Web
tags:
  - reprint
  - remix
---
## jsdom

jsdom 是一个纯粹由 JavaScript 实现的一系列 Web 标准，特别是 WHATWG 组织制定的 DOM 和 HTML 标准，用于在 Node.js 中使用。
大体上来说，该项目的目标是模拟足够的 Web 浏览器子集，以便用于测试和挖掘真实世界的 Web 应用程序。

```js
import {JSDOM} from "jsdom"

test('infoQ test', () => {
    const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
    console.log("foo test:", dom.window.document.querySelector("p").textContent); // "Hello world"

});
```

作者：0D0A
链接：https://juejin.cn/post/7151065517569081380
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
