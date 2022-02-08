---
title: QUIC
author: "-"
date: 2017-12-16T03:35:36+00:00
url: quic
categories:
  - network

tags:
  - reprint
---
## QUIC
读作 "quick"
Quic 全称 quick udp internet connection, 是一个基于UDP的传输层协议, 其目的是为了代替TCP。

QUIC（Quick UDP Internet Connection）是谷歌制定的一种互联网传输层协议，它基于UDP传输层协议，同时兼具TCP、TLS、HTTP/2等协议的可靠性与安全性，可以有效减少连接与传输延迟，更好地应对当前传输层与应用层的挑战。目前阿里云CDN线上提供GQUIC版本服务，已经有Tbps级别的流量承载，并对客户来带了显著的延迟收益。本文将由低向上分层讨论QUIC协议的特点。

Quic 相比现在广泛应用的 http2+tcp+tls 协议有如下优势 [2]：

- 减少了 TCP 三次握手及 TLS 握手时间。
- 改进的拥塞控制 -- 拥塞控制移到了用户空间
- 避免队头阻塞的多路复用。
- 连接迁移（Connection Migration）
- 前向冗余纠错。
- stream mode

QUIC 具备“0RTT 建联”、“支持连接迁移”等诸多优势，并将成为下一代互联网协议：HTTP3.0 的底层传输协议

QUIC (Quick UDP Internet Connections) 是一种基于 UDP 封装的安全 可靠传输协议，他的目标是取代 TCP 并自包含 TLS 成为标准的安全传输协议。

在 QUIC 出现之前，TCP 承载了 90% 多的互联网流量， 发展了几十年的 TCP 面临 “协议僵化问题”

网络设备支持 TCP 时的僵化，表现在：对于一些防火墙或者 NAT 等设备，如果 TCP 引入了新的特性，比如增加了某些 TCP OPTION 等，可能会被认为是攻击而丢包，导致新特性在老的网络设备上无法工作。
网络操作系统升级困难导致的 TCP 僵化，一些 TCP 的特性无法快速的被演进
除此之外，当应用层协议优化到 TLS1.3、 HTTP2.0 后， 传输层的优化也提上了议程

### HTTP/3
2018年10月，IETF的HTTP工作组和QUIC工作组共同决定将QUIC上的HTTP映射称为 "HTTP/3"  
当IETF正式标准化HTTP/2时，Google正在独立构建一个新的传输协议，名为gQUIC。它后来成为新互联网草案，并被命名为QUIC。gQUIC最初的实验证明，在网络条件较差的情况下，gQUIC在增强网页浏览体验方面的效果非常好。因此，gQUIC的发展势头越来越好，IETF的大多数成员赞成建立一个在QUIC上运行的HTTP新规范。这个新的倡议被称为HTTP/3，以区别于当前的HTTP/2标准。

>https://zhuanlan.zhihu.com/p/32553477
>https://zhuanlan.zhihu.com/p/151639428
http://www.infoq.com/cn/news/2018/03/weibo-quic?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global

https://www.bennythink.com/quic.html

https://github.com/lucas-clemente/quic-go
  
https://devsisters.github.io/goquic/
  
https://github.com/mholt/caddy
>https://datatracker.ietf.org/doc/html/rfc9000
>https://datatracker.ietf.org/doc/html/draft-ietf-quic-transport-29
### Tunneling TCP inside QUIC
https://datatracker.ietf.org/doc/html/draft-piraux-quic-tunnel-tcp-00
>https://pkg.go.dev/github.com/lucas-clemente/quic-go#Session
