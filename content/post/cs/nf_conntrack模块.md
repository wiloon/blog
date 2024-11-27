---
title: nf_conntrack模块
author: "-"
date: 2019-07-02T09:43:51+00:00
url: /?p=14622
categories:
  - Inbox
tags:
  - reprint
---
## nf_conntrack模块

nf_conntrack(在老版本的 Linux 内核中叫 ip_conntrack)是一个内核模块,用于跟踪一个连接的状态的。连接状态跟踪可以供其他模块使用,最常见的两个使用场景是 iptables 的 nat 的 state 模块。 iptables 的 nat 通过规则来修改目的/源地址,但光修改地址不行,我们还需要能让回来的包能路由到最初的来源主机。这就需要借助 nf_conntrack 来找到原来那个连接的记录才行。而 state 模块则是直接使用 nf_conntrack 里记录的连接的状态来匹配用户定义的相关规则。例如下面这条 INPUT 规则用于放行 80 端口上的状态为 NEW 的连接上的包。

iptables -A INPUT -p tcp -m state -state NEW -m tcp -dport 80 -j ACCEPT。

iptables中的状态检测功能是由state选项来实现iptable的。对这个选项，在iptables的手册页中有以下描述: 

state

这个模块能够跟踪分组的连接状态(即状态检测)。

格式: -state XXXXX

这里，state是一个用逗号分割的列表，表示要匹配的连接状态。

在iptables中有四种状态: NEW，ESTABLISHED，RELATED，INVALID。

NEW，表示这个分组需要发起一个连接，或者说，分组对应的连接在两个方向上都没有进行过分组传输。NEW说明 这个包是我们看到的第一个包。意思就是，这是conntrack模块看到的某个连接第一个包，它即将被匹配了。比如，我们看到一个SYN包，是我们所留意 的连接的第一个包，就要匹配它。第一个包也可能不是SYN包，但它仍会被认为是NEW状态。比如一个特意发出的探测包，可能只有RST位，但仍然是 NEW。

ESTABLISHED，表示分组对应的连接已经进行了双向的分组传输，也就是说连接已经建立，而且会继续匹配 这个连接的包。处于ESTABLISHED状态的连接是非常容易理解的。只要发送并接到应答，连接就是ESTABLISHED的了。一个连接要从NEW变 为ESTABLISHED，只需要接到应答包即可，不管这个包是发往防火墙的，还是要由防火墙转发的。ICMP的错误和重定向等信息包也被看作是 ESTABLISHED，只要它们是我们所发出的信息的应答。

RELATED，表示分组要发起一个新的连接，但是这个连接和一个现有的连接有关，例如: FTP的数据传输连接 和控制连接之间就是RELATED关系。RELATED是个比较麻烦的状态。当一个连接和某个已处于ESTABLISHED状态的连接有关系时，就被认为 是RELATED的了。换句话说，一个连接要想是RELATED的，首先要有一个ESTABLISHED的连接。这个ESTABLISHED连接再产生一 个主连接之外的连接，这个新的连接就是RELATED的了，当然前提是conntrack模块要能理解RELATED。ftp是个很好的例子，FTP- data连接就是和FTP-control有RELATED的。还有其他的例子，

INVAILD，表示分组对应的连接是未知的，说明数据包不能被识别属于哪个连接或没有任何状态。有几个原因可以产生这种情况，比如，内存溢出，收到不知属于哪个连接的ICMP错误信息。一般地，我们DROP这个状态的任何东西。

https://clodfisher.github.io/2018/09/nf_conntrack/

## 连接跟踪（conntrack）

>https://arthurchiao.art/blog/conntrack-design-and-implementation-zh/
