---
title: "SCTP GRE"
author: "-"
date: ""
url: ""
categories:
  - "Network"
tags:
  - "Inbox"
  - "reprint"
---
## SCTP

sctp和tcp的区别
作为一个传输层协议，SCTP兼有TCP及UDP两者的特点。SCTP可以称为是TCP的改进协议，但他们之间仍然存在着较大的差别。首先SCTP和TCP之间的最大区别是SCTP的连接可以是多宿主连接的，TCP则一般是单地址连接的。在进行SCTP建立连接时，双方均可声明若干IP地址（IPv4，Ipv6或主机名）通知对方本端所有的地址。若当前连接失效，则协议可切换到另一个地址，而不需要重新建立连接。
其次SCTP是基于消息流，而TCP则是基于字节流。所谓基于消息流，是指发送数据和应答数据的最小单位是消息包(chunk)。一个SCTP连接（Association）同时可以支持多个流(stream)，每个流包含一系列用户所需的消息数据(chunk)。而TCP则只能支持一个流。在网络安全方面，SCTP增加了防止恶意攻击的措施。不同于TCP连接采用的三次握手机制，SCTP连接采用四次握手机制，有效的防止了类似于SYN Flooding的防范拒绝服务攻击。SCTP主要的贡献是对多重联外线路的支持，一个端点可以由多于一个IP地址组成，使得传输可在主机间或网卡间做到透明的网络容错备援。

[https://www.cnblogs.com/elleniou/p/3342140.html](https://www.cnblogs.com/elleniou/p/3342140.html)

## GRE

通用路由封装协议GRE 提供了将一种协议报文封装在另一种协议报文中的机制，是一种三层隧道封装技术；可以对IPv4协议的数据报文进行再封装，使这些被封装的数据报文能够在另一个网络层协议（如IPv4）中传输；报文通过GRE隧道透明的传输，可以解决外网主动访问内网的问题；GRE可以封装组播数据和路由选择协议，结合IP Sec使用，从而保证语音、视频等组播业务的安全。

GRE实现机制简单，对隧道两端的设备负担小；GRE隧道可以有效利用了原有的网络架构，降低成本；GRE隧道扩展了跳数受限网络协议的工作范围，支持企业灵活设计网络拓扑；GRE隧道支持MPLS LDP，使用GRE隧道承载MPLS LDP报文，建立LDP LSP，实现MPLS骨干网的互通；GRE隧道将不连续的子网连接起来，用于组建VPN，实现企业总部和分支间安全的连接。

[https://zhuanlan.zhihu.com/p/103214510](https://zhuanlan.zhihu.com/p/103214510)
