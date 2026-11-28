---
title: "Long Polling and HTTP Keep-Alive: 长轮询与连接复用"
author: "-"
date: 2026-10-20T06:57:24+08:00
lastmod: 2026-10-20T06:57:24+08:00
url: long-polling
categories:
  - Web
tags:
  - http
  - long-polling
  - keep-alive
  - tls
  - github-actions
  - remix
  - AI-assisted
---

客户端想"一有新消息就知道"，但只能由客户端主动发请求（比如它在内网里，服务端连不进来），常用的办法是长轮询。这篇记录长轮询怎么工作，以及它底下的 HTTP 连接复用（keep-alive）是怎么回事。起因是给 homelab 配 GitHub Actions 自托管 runner 时，想弄清楚 runner 在内网里是怎么及时拿到任务的。

## 短轮询和长轮询

**短轮询**：客户端每隔固定时间问一次"有没有新消息"，服务端立刻回答，有就给，没有就回空。

- 间隔设短了，大部分请求都是空跑，浪费流量和服务端资源
- 间隔设长了，消息要等到下一次轮询才能拿到，延迟最多一个间隔

**长轮询**：客户端发出请求后，服务端**先不回答**，把请求挂住：

- 挂住期间来了消息，立刻在这个请求上返回
- 一直没有消息，等到约定的时间（比如 50 秒）返回一个空响应
- 客户端收到响应（不管有没有消息）后马上发下一个请求

```text
client                                   server
  |---- GET /messages (wait up to 50s) ---->|
  |                                         |  no message yet, hold the request
  |                                         |  ... 12s later a message arrives
  |<--------- 200 [message] ----------------|
  |---- GET /messages (wait up to 50s) ---->|  sent again immediately
  |                                         |  nothing for 50s
  |<--------- 200 [] (empty) ---------------|
  |---- GET /messages (wait up to 50s) ---->|
```

所以长轮询几乎任何时候都有一个请求挂在服务端，消息一到就能送出去，延迟接近实时；没有消息时每 50 秒才一个请求，空跑也很少。消息在两次请求之间到达也不会丢：服务端先把它放进队列，下一个请求一到就取走。

## 超时为什么是几十秒，而不是无限长

一个请求挂得太久，路上的设备会把它当成死连接切掉：

- 服务端、反向代理、负载均衡器都有空闲或读超时，比如 nginx 的 `proxy_read_timeout` 默认 60 秒
- 家用路由器和运营商的 NAT 会清理长时间没有数据的连接表项
- 客户端自己的 HTTP 库也可能有请求超时

被切掉的请求客户端不一定能及时发现，可能干等很久。所以长轮询的超时通常设得比路径上最短的那个超时还短，让服务端在被切之前主动返回，客户端再发下一个。常见的取值：

| 例子 | 长轮询超时 |
| --- | --- |
| GitHub Actions 自托管 runner 向 GitHub 取任务 | 约 50 秒 |
| AWS SQS `ReceiveMessage` 的 `WaitTimeSeconds` | 最长 20 秒 |
| Telegram Bot API `getUpdates` 的 `timeout` 参数 | 由客户端指定 |

## 每次重发请求，要重新握手吗

一般不用，这就是 HTTP keep-alive（持久连接）的作用。先理清楚分层：

```text
HTTP request / response   <- many of these, one after another
TLS (encryption)          <- handshake once per connection
TCP connection            <- 3-way handshake once per connection
```

- 建立连接时做两次握手：先是 TCP 三次握手，然后在这条 TCP 连接上做 TLS 握手，协商出加密用的密钥
- 一个 HTTP 请求结束后，**TCP 连接和 TLS 会话都不关**。下一个请求直接用已经协商好的密钥加密，在同一条连接上发出去
- 所以长轮询每 50 秒发一个新请求，是"新的 HTTP 请求"，不是"新的连接"。TCP 和 TLS 都不用重新握手

HTTP/1.1 默认就是持久连接，除非某一方发了 `Connection: close`。HTTP/1.1 的一条连接同一时间只跑一个请求，下一个要等上一个的响应结束；HTTP/2 可以在一条连接上同时跑多个请求（多路复用）。

连接并不是永远不断。下面几种情况连接会关掉，下一个请求就要重新握手：

- 服务端或客户端的空闲超时到了，比如 Go 的 `http.Transport` 默认空闲 90 秒关闭连接
- 中间的 NAT 或代理清掉了连接
- 网络断了，或者任意一端重启

重新连接时 TCP 三次握手照常要做，TLS 可以用会话恢复（session resumption）：凭上次连接留下的票据跳过证书交换，比完整握手快。TLS 1.3 的完整握手需要 1 个往返（RTT），恢复时还可以用 0-RTT，在第一个包里就带上请求数据。

长轮询正好让连接一直有流量（每次请求和响应之间最多空闲几十秒），一般不会触发空闲超时，同一条连接能复用很久。

## 和 SSE、WebSocket 的区别

| 方式 | 连接 | 方向 | 说明 |
| --- | --- | --- | --- |
| 短轮询 | 普通 HTTP 请求 | 客户端拉 | 最简单，延迟和空跑二选一 |
| 长轮询 | 普通 HTTP 请求，挂住再返回 | 客户端拉 | 几乎实时，穿过任何代理和防火墙都没问题，每条消息后要重发请求 |
| SSE（Server-Sent Events） | 一个不结束的 HTTP 响应 | 服务端推 | 服务端在同一个响应里不断写事件，只能单向 |
| WebSocket | 从 HTTP 升级成独立的双向协议 | 双向 | 最实时，但有的代理和负载均衡器要专门配置才能放行 |

长轮询的好处是它就是普通的 HTTP 请求，任何能访问 HTTPS 的环境都能用，代理和防火墙不需要任何特殊配置。GitHub runner、SQS、Telegram Bot 都选它，主要就是这个原因。

## 例子：GitHub Actions 自托管 runner

自托管 runner 跑在内网里，GitHub 连不进来，所以由 runner 主动向 GitHub 长轮询：

1. 代码 push 到 GitHub，GitHub 根据 workflow 创建 job，放进这个 runner 的队列
2. runner 一直有一个挂着的请求，job 一进队列，GitHub 就在这个请求上返回
3. runner 领到 job 开始执行，同时再发一个新请求继续等

内网只需要能访问 GitHub 的 HTTPS，路由器上不用开任何入站端口。从 push 到开始执行的延迟主要是 GitHub 创建 job 的时间，轮询本身几乎不增加延迟。

## 参考

- [GitHub Docs: Communicating with self-hosted runners](https://docs.github.com/en/enterprise-server@3.13/actions/concepts/runners/communicating-with-self-hosted-runners)
- [RFC 9112: HTTP/1.1, Persistent Connections](https://www.rfc-editor.org/rfc/rfc9112#name-persistence)
- [Amazon SQS short and long polling](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html)
- [Telegram Bot API: getUpdates](https://core.telegram.org/bots/api#getupdates)
