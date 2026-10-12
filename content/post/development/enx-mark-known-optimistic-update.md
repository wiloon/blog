---
title: "ENX Mark Known: 从等待接口改为乐观更新"
author: "-"
date: 2026-10-12T10:04:10+08:00
lastmod: 2026-10-12T10:04:10+08:00
url: enx-mark-known-optimistic-update
categories:
  - Projects
tags:
  - enx
  - chrome-extension
  - optimistic-update
  - original
  - AI-assisted
---
## 背景

[enX](./enx.md) 的 Chrome 扩展会给查过的生词画下划线。主窗口点一个词会弹出浮层，浮层里有 Mark Known（标为已认识）按钮，点了之后这个词的下划线消失。

后来侧边栏的整句翻译也加上了同样的下划线（ADR-053），于是有了一个新问题：在主窗口标为已认识之后，侧边栏里这个词的下划线也应该一起消失。

## 原来的做法

```text
content script → background → POST /api/mark → enx-api 写库
                                   ↓ 成功
content script 收到回复 → 去掉主窗口下划线
```

主窗口要等接口成功才去掉下划线，侧边栏完全不知道这件事。

## 改成什么样

```text
content script：先去掉主窗口下划线
  └─ runtime.sendMessage({ type: 'markAcquainted', word })
        ├─ 侧边栏：收到后立即去掉下划线，不回复
        └─ background：调 enx-api，完成后回复 content script
```

两点变化：

- 主窗口先改界面，再让 background 在后台调接口，也就是常说的乐观更新（optimistic update），和它相对的是原来那种等服务端确认再改界面的做法。
- 侧边栏不需要新的通道。`chrome.runtime.sendMessage` 从 content script 发出时，会投递给扩展里所有监听 `runtime.onMessage` 的页面，background 和侧边栏都能收到。侧边栏只需要多注册一个监听。

## 为什么可以先改界面

标为已认识失败的代价很低：服务端没记上，用户下次读别的文章时这个词还会带下划线，再标一次就行。为了这个小概率的失败让用户每次都等一个网络往返，不划算。

如果改成「background 调接口成功后再通知侧边栏」，状态会更严格一致，但侧边栏要多等一个接口的时间。对这个操作来说，一致性没有那么重要。

## 多个接收方只能有一个回复

`runtime.sendMessage` 允许多个页面监听，但发送方只会收到**第一个**调用 `sendResponse` 的回复，其余的被忽略。侧边栏如果也回复，会抢在 background 前面，content script 就看不到接口的真实结果了。

所以约定：侧边栏只监听、不回复（不调用 `sendResponse`，也不 `return true`），只有 background 回复。

## 顺带发现的问题：接口不能重试

原来的 `/api/mark` 是切换：每调用一次，已认识和未认识互相翻转。服务端已经写入、但回复丢了的时候，如果客户端重试，这个词就被翻回了未认识。所以这次改动先不做重试，另开了一个 issue：把接口拆成两个幂等的操作，`PUT /api/me/words/:word/known` 和 `DELETE /api/me/words/:word/known`，之后再给 background 加重试。

## 参考

- [Message passing（Chrome for Developers）](https://developer.chrome.com/docs/extensions/develop/concepts/messaging)
- [useOptimistic（React）](https://react.dev/reference/react/useOptimistic)
- [Optimistic Updates（TanStack Query）](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates)
