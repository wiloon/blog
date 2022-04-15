---
author: "-"
date: "2020-09-29 10:05:41" 
title: "Service Worker"
categories:
  - Web
tags:
  - reprint
---
## "Service Worker"

Service Worker 是浏览器在后台独立于网页运行的脚本
Service workers 本质上充当 Web 应用程序、浏览器与网络 (可用时) 之间的代理服务器。这个 API 旨在创建有效的离线体验，它会拦截网络请求并根据网络是否可用采取来适当的动作、更新来自服务器的的资源。它还提供入口以推送通知和访问后台同步 API。
推送消息,背景后台同步geofencing (地理围栏定位) 
它是一种 JavaScript Worker，无法直接访问 DOM。 Service Worker 通过响应 postMessage 接口发送的消息来与其控制的页面通信，页面可在必要时对 DOM 执行操作。
Service Worker 是一种可编程网络代理，让您能够控制页面所发送网络请求的处理方式。
Service Worker 在不用时会被中止，并在下次有需要时重启，因此，您不能依赖 Service Worker onfetch 和 onmessage 处理程序中的全局状态。 如果存在您需要持续保存并在重启后加以重用的信息，Service Worker 可以访问 IndexedDB API。
Service Worker 广泛地利用了 promise，因此如果您不熟悉 promise，则应停下阅读此内容，看一看 Promise 简介。

Service Worker 是一个浏览器中的进程而不是浏览器内核下的线程，因此它在被注册安装之后，能够被在多个页面中使用，也不会因为页面的关闭而被销毁。因此，Service Worker 很适合被用与多个页面需要使用的复杂数据的计算

### chrome
    # 检查是否已经启用service workers
    chrome://inspect/#service-workers 
    chrome://serviceworker-internals

https://juejin.im/post/6844903613270081543
