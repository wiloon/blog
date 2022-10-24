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

QUIC (Quick UDP Internet Connection）

Quic 是一个通用的基于UDP的传输层网络协议, 其目的是为了在网络层代替 TCP。 QUIC旨在提供几乎等同于TCP连接的可靠性，但延迟大大减少, 提供与TLS/SSL相当的安全性

QUIC 是 Google 制定的一种互联网传输层协议，它基于UDP传输层协议，同时兼具TCP、TLS、HTTP/2等协议的可靠性与安全性，可以有效减少连接与传输延迟，更好地应对当前传输层与应用层的挑战。目前阿里云 CDN 线上提供 QUIC 版本服务，已经有 Tbps 级别的流量承载，并对客户来带了显著的延迟收益。本文将由低向上分层讨论 QUIC 协议的特点。

QUIC协议在当前Chrome版本中被默认开启，活跃的会话可以用 chrome://net-export/ 导出, 再导入分析工具 <https://netlog-viewer.appspot.com/> 查看。

HTTP/3就是基于QUIC协议的

chrome dev tool 里 “h3-29”表示是QUIC请求
目前常见的实现有Google的quiche，微软的msquic，mozilla的neqo，以及基于go语言的quic-go等。

什么是QUIC
QUIC (Quick UDP Internet Connections）是一种实验性传输层网络协议，提供与TLS/SSL相当的安全性，同时具有更低的连接和传输延迟。QUIC基于UDP，因此拥有极佳的弱网性能，在丢包和网络延迟严重的情况下仍可提供可用的服务。QUIC在应用程序层面就能实现不同的拥塞控制算法，不需要操作系统和内核支持，这相比于传统的TCP协议，拥有了更好的改造灵活性，非常适合在TCP协议优化遇到瓶颈的业务。

Quic 相比现在广泛应用的 http2+tcp+tls 协议有如下优势：

- 减少了握手的延迟 (1-RTT 或 0-RTT）, 连接创建期间大大减少开销, 减少了 TCP 三次握手及 TLS 握手时间。
- 改进的拥塞控制 -- 拥塞控制移到了用户空间

在QUIC级别而不是UDP级别重传丢失的数据

- 避免**队头阻塞**的多路复用。
QUIC与HTTP/2的多路复用连接协同工作，允许多个数据流独立到达所有端点，因此不受涉及其他数据流的丢包影响。相反，HTTP/2创建在传输控制协议 (TCP）上，如果任何一个TCP数据包延迟或丢失，所有多路数据流都会遭受队头阻塞延迟。
- 连接迁移 (Connection Migration）

QUIC包含一个连接标识符，该标识符唯一地标识客户端与服务器之间的连接，而无论源IP地址是什么。这样只需发送一个包含此ID的数据包即可重新创建连接，因为即使用户的IP地址发生变化，原始连接ID仍然有效。

QUIC连接未严格绑定到单个网络路径上。连接迁移使用连接标识符来允许连接转移到新的网络路径。在这个版本的QUIC中，只有客户端能够进行迁移。此设计还允许在网络拓扑或地址映射发生变化 (如NAT重新绑定可能引起的变化）后继续连接。

><https://github.com/alibaba/xquic/blob/main/docs/translation/draft-ietf-quic-transport-34-zh.md>
><https://zhuanlan.zhihu.com/p/311221111>

- 前向冗余纠错。
- stream mode

每个数据包是单独加密的，因此加密数据时不需要等待部分数据包。

QUIC包含一个连接标识符，该标识符唯一地标识客户端与服务器之间的连接，而无论源IP地址是什么。这样只需发送一个包含此ID的数据包即可重新创建连接，因为即使用户的IP地址发生变化，原始连接ID仍然有效。

QUIC 具备“0RTT 建联”、“支持连接迁移”等诸多优势，并将成为下一代互联网协议：HTTP3.0 的底层传输协议

QUIC 是一种基于 UDP 封装的安全 可靠传输协议，他的目标是取代 TCP 并自包含 TLS 成为标准的安全传输协议。

在 QUIC 出现之前，TCP 承载了 90% 多的互联网流量， 发展了几十年的 TCP 面临 “协议僵化问题”

网络设备支持 TCP 时的僵化，表现在：对于一些防火墙或者 NAT 等设备，如果 TCP 引入了新的特性，比如增加了某些 TCP OPTION 等，可能会被认为是攻击而丢包，导致新特性在老的网络设备上无法工作。
网络操作系统升级困难导致的 TCP 僵化，一些 TCP 的特性无法快速的被演进
除此之外，当应用层协议优化到 TLS1.3、 HTTP2.0 后， 传输层的优化也提上了议程

### HTTP/3

2018年10月，IETF的HTTP工作组和QUIC工作组共同决定将QUIC上的HTTP映射称为 "HTTP/3"  
当IETF正式标准化HTTP/2时，Google正在独立构建一个新的传输协议，名为gQUIC。它后来成为新互联网草案，并被命名为QUIC。gQUIC最初的实验证明，在网络条件较差的情况下，gQUIC在增强网页浏览体验方面的效果非常好。因此，gQUIC的发展势头越来越好，IETF的大多数成员赞成建立一个在QUIC上运行的HTTP新规范。这个新的倡议被称为HTTP/3，以区别于当前的HTTP/2标准。

### quic-go

```bash
#increase the maximum buffer size by running:

sysctl -w net.core.rmem_max=2500000
```

><https://www.cnblogs.com/weijunji/p/quic-study.html>

### quic-go
<https://github.com/lucas-clemente/quic-go>
><https://datatracker.ietf.org/doc/html/rfc9000>

><https://fangqiuhang.github.io/RFC9000_Chinese_Translation/>

><https://zhuanlan.zhihu.com/p/32553477>
><https://zhuanlan.zhihu.com/p/151639428>
<http://www.infoq.com/cn/news/2018/03/weibo-quic?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global>

<https://www.bennythink.com/quic.html>

<https://devsisters.github.io/goquic/>
  
<https://github.com/mholt/caddy>
><https://datatracker.ietf.org/doc/html/rfc9000>
><https://datatracker.ietf.org/doc/html/draft-ietf-quic-transport-29>

### Tunneling TCP inside QUIC
<https://datatracker.ietf.org/doc/html/draft-piraux-quic-tunnel-tcp-00>
><https://pkg.go.dev/github.com/lucas-clemente/quic-go#Session>

><https://github.com/10cella/awesome-quic>
><https://github.com/alibaba/xquic/blob/main/docs/docs-zh/README-zh.md>
><https://datatracker.ietf.org/wg/quic/about/>
><https://kiosk007.top/2021/07/24/QUIC-%E5%8F%91%E7%94%9F%E4%BA%86%E4%BB%80%E4%B9%88/#QUIC-%E4%BB%8E%E5%93%AA%E6%9D%A5>
><https://interop.seemann.io/>
