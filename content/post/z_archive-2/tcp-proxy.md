---
title: tcp proxy
author: "-"
date: 2021-10-02T01:27:23+00:00
url: tcp/proxy
categories:
  - network
tags:
  - reprint
  - proxy
---
## tcp proxy

[https://github.com/jpillora/go-tcp-proxy](https://github.com/jpillora/go-tcp-proxy)

### TCP半开连接与半闭连接

[https://www.cnblogs.com/cangqinglang/p/9558236.html](https://www.cnblogs.com/cangqinglang/p/9558236.html)

## half-open connection, 半开连接

[https://bbs.huaweicloud.com/blogs/301407](https://bbs.huaweicloud.com/blogs/301407)

处于 establish 状态的服务端如果收到了客户端的 SYN 报文（注意此时的 SYN 报文其实是乱序的，因为 SYN 报文的初始化序列号其实是一个随机数），会回复一个携带了正确序列号和确认号的 ACK 报文，这个 ACK 被称之为 Challenge ACK。

接着，客户端收到这个 Challenge ACK，发现序列号并不是自己期望收到的，于是就会回 RST 报文，服务端收到后，就会释放掉该连接。

RFC 文档解释
rfc793 文档里的第 34 页里，有说到这个例子。

原文的解释我也贴出来给大家看看。

When the SYN arrives at line 3, TCP B, being in a synchronized state,
and the incoming segment outside the window, responds with an
acknowledgment indicating what sequence it next expects to hear (ACK
100).
TCP A sees that this segment does not acknowledge anything it
sent and, being unsynchronized, sends a reset (RST) because it has
detected a half-open connection.
TCP B aborts at line 5.
TCP A willcontinue to try to establish the connection;
