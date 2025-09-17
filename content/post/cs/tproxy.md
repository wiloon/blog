---
title: TProxy
author: "-"
date: 2019-04-10T05:30:05+00:00
url: tproxy
categories:
  - Network
tags:
  - reprint
---
## TProxy

## net.ipv4.ip_forward

这条命令的作用是开启 Linux 系统的 IPv4 协议栈的数据包转发功能。

```bash
sudo sysctl net.ipv4.ip_forward = 1
```

ip_forward = 0

如果目标 IP 地址是本机拥有的某个 IP 地址，系统就会接收并处理这个数据包（例如，交给某个正在监听端口的应用程序）。

如果目标 IP 地址不是本机的，系统会默认将该数据包丢弃。这是普通主机（Host）的正常行为。

ip_forward = 1

如果目标 IP 地址是本机的，处理方式不变。

如果目标 IP 地址不是本机的，系统不会丢弃它。而是会查询自己的路由表，根据路由规则将这个数据包从合适的网络接口转发出去，发送给下一个路由器或者目标主机。这时，这台机器就扮演了路由器（Router）的角色。

### TPROXY 的作用

TPROXY（Transparent Proxy）用来做 透明代理，可以拦截特定的流量，并强制把它交给本地某个 socket（通常是代理进程），而 不改变包的目标地址/端口（和 REDIRECT 不一样，REDIRECT 会改成本机 IP）。

TPROXY 依赖内核的 nf_tproxy_core 模块，它会在路由决策阶段之前决定：这个包是否交给本地 socket

### TPROXY 能拦截哪些流量

来自外部的流量
在 mangle/PREROUTING 链，TPROXY 可以截获所有进入本机的包 ——
不论目标 IP 是本机，还是本来应该转发出去的其它主机，都可以“强行”转给本地代理进程。
这就是它相比 REDIRECT 的强大之处：

REDIRECT 只能改成本机 IP，所以只适合本机为目标的流量；

TPROXY 不改变目标 IP，能“假装”这个包还是发往原地址，同时又让本地代理进程接收。

本地产生的流量
在 mangle/OUTPUT 链，TPROXY 可以截获本机应用发出的连接，再转交给代理进程。

### 哪些流量不能被 TPROXY 拦截？

内核绕过 Netfilter 的流量：例如某些特殊协议或 raw socket 直接发出的包。

已经路由转发后的包：如果流量没有在 PREROUTING 被标记，到了 FORWARD 就已经“太晚”，TPROXY 无法再劫持。

非 TCP/UDP：TPROXY 主要针对 TCP、UDP，像 ICMP、GRE、ESP 等协议并不能用它透明劫持。

### Netfilter 的钩子点顺序

Linux 内核收包时，Netfilter 的主要钩子顺序是：

PREROUTING（刚进来，路由前）

INPUT（路由后，目标是本机）

FORWARD（路由后，目标是别的主机）

OUTPUT（本地产生的数据包）

POSTROUTING（即将发出）

iptables 将不同的功能划分到不同的“表”（table）中，以保持逻辑清晰。

TPROXY 要修改的是 路由决策，因为它要把本来可能转发的包强行交给本地 socket。
所以必须在 路由前（PREROUTING） 或 本地发出（OUTPUT） 的阶段下手。

NAT 表的 PREROUTING 是做 DNAT 的，改变的是 目的 IP/端口，和 TPROXY 的目标不同。nat 表在设计上是为了做地址转换，比如不能在 nat 表 用 drop 或者 reject 来拒绝连接, iptables 会报错

filter 表主要是 允许/拒绝，没有改变路由的能力。

mangle 表才允许 标记数据包/修改 TTL 等参数，并且是 TPROXY 实现所需的表。  mangle 表专门负责修改数据包的元数据，例如修改 TTL、TOS/DSCP 字段等，用于流量整形或高级路由。

-j TPROXY --tproxy-mark 1 会为匹配的数据包（TCP 或 UDP）设置一个标记值（mark）为 1。这个标记是 Linux 内核中的一种元数据，附加在数据包的 sk_buff（socket buffer）结构上。

在 Linux 内核的网络协议栈中，每个 TCP/IP 数据包在内核处理过程中都会被封装在一个 sk_buff（socket buffer）结构中。

当网络接口（如网卡）接收到一个数据包时，内核会为其分配一个 sk_buff 结构，用于存储数据包的原始数据（包括以太网头部、IP 头部、TCP/UDP 头部和有效载荷）。
在数据包从物理层向上通过协议栈（如链路层、网络层、传输层）处理的过程中，sk_buff 会携带数据包的元数据，并在各层之间传递。
同样，当系统发送数据包时，内核会为待发送的数据分配一个 sk_buff，并在协议栈向下处理后通过网卡发送出去。

TPROXY 只能在 mangle 表的 PREROUTING 链上工作

- TPROXY 需要在路由决策之前处理数据包
- mangle 表的 PREROUTING 链是数据包进入系统后最早的处理点
- 这个位置可以在路由决策前修改数据包的目标地址和端口

Linux 透明代理并不是一个独立的功能模块，而是一个功能特性。在使用 Linux 透明代理的时候，需要 iptables, ip-rule, ip-route 和应用程序一起协同工作。

tproxy 即 transparent（透明） proxy。这里的 transparent（透明）有两层含义：

代理对于 client 是透明的，client 端无需进行任何配置。即无需修改请求地址，也无需采用代理协议和代理服务器进行协商。与之相对比的是 socks 代理或者 http 代理，需要在 client 端设置代理的地址，在发起请求时也需要通过代理协议告知代理服务器其需要访问的真实地址。
代理对于 server 是透明的，server 端看到的是 client 端的地址，而不是 proxy 的地址。

tproxy 是 Linux 的内核模块（自 Linux 2.2 版本开始引入），用于实现透明代理，其名称中的字母 t 即代表透明（transparent）。

要使用透明代理首先需要把指定的数据包使用 iptables 拦截到指定的网卡上，然后在该网卡监听并转发数据包。

使用 tproxy 实现透明代理的步骤如下：

首先需要实现流量拦截：在 iptables 的 PREROUTING 链的 mangle 表中创建一个规则，拦截流量发送给 tproxy 处理，
例如: `iptables -t mangle -A PREROUTING -p tcp -dport 9080 -j TPROXY --on-port 15001 --on-ip 127.0.0.1 --tproxy-mark 0x1/0x1`

--on-ip 127.0.0.1 代理进程监听的 IP.
--on-port 12345 是代理进程的监听端口。

--tproxy-mark 1/1 为 IP 数据包打上一个标记，以应用上面创建的策略路由。

```Bash
# iptables -j TPROXY -h

TPROXY target options:
  --on-port port                    Redirect connection to port, or the original port if 0
  --on-ip ip                        Optionally redirect to the given IP
  --tproxy-mark value[/mask]        Mark packets with the given value/mask

```

给所有目的地为 9080 端口的 TCP 数据包打上标记 1，你还可以指定来源 IP 地址或者 IP 集 ，进一步缩小标记范围，tproxy 监听在 15001 端口；
创建一个路由规则，将所有带有标记 1 的数据包查找特定的路由表：例如 `ip rule add fwmark 1 lookup 100`，让所有 fwmark 为 1 的数据包查找 100 路由表；
将数据包映射到特定的本地地址：例如

`ip route add local default dev lo table 100`，

local 是一个路由类型，指将网络包发给系统本地协议栈。

在 100 路由表中将所有 IPv4 地址声明为本地，当然这只是一个例子，实际使用时需要请将特定的 IP 的数据包转发到本地的 lo 回环网卡；
在路由表100 中添加了一条路由规则，将所有数据包的下一跳都指向 loopback，这样数据包才能被本地代理进程的 listener 看到。

至此流量已被拦截到 tproxy 的监听端口 15001（从 Linux 内核空间进入用户空间），你可以编写网络应用处理数据包或使用 Squid 或 Envoy 等支持 tproxy 的软件来处理数据包；
透明代理的优点
透明代理具有以下优点：

透明代理提供更高的带宽并减少传输延迟，从而提高服务质量；

用户无需配置网络和主机；

企业可以控制对其网络服务的访问；

用户可以通过透明代理连接互联网以绕过一些监管；

透明代理的缺点
透明代理有以下缺点：

如果透明代理配置不当，可能导致用户无法连接互联网，而对于不知情的用户来说，他们无法排查和修改透明代理中的错误；
透明代理的安全性无法得到保证，因为被拦截的用户流量可能被透明代理篡改；
透明代理可能缓存用户信息，导致用户隐私泄露的风险；
总结
透明代理作为代理中的一类重要类型，它的用途广泛，不论是 代理软件，还是 Istio 服务网格中得使用了应用。了解它的原理和工作方式有助于我们科学正确的使用代理，而是否使用透明代理取决于你对它的信任和了解程度。

参考
tproxy-example - github.com
Linux transparent proxy support - powerdns.org
Feature: TPROXY version 4.1+ Support - wiki.squid-cache.org

TProxy 不会修改报文头，但却可以将报文转发。

It redirects the packet to a local socket without changing the packet header in any way.

它会将数据包重定向到一个本地的 socket 上，而不会以任何形式修改包的头部。

TProxy 模块工作在 mangle 表上，支持对数据包进行标记和重定向。

使用 TProxy 有两个前提条件：

启用了 nf_defrag_ipv4。
协议为 TCP 或 UDP。

https://www.kernel.org/doc/Documentation/networking/tproxy.txt

https://jimmysong.io/blog/what-is-tproxy/

https://www.zhaohuabing.com/learning-linux/docs/tproxy/

https://www.kernel.org/doc/html/latest/networking/tproxy.html

https://asphaltt.github.io/post/linux-solve-policy-routing-problem/

https://people.apache.org/~amc/tiphares/router-inline.html

https://www.brendangregg.com/bpf-performance-tools-book.html

————————————————
版权声明：本文为CSDN博主「redwingz」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/sinat_20184565/article/details/125473975
