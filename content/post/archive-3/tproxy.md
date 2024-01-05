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
透明代理作为代理中的一类重要类型，它的用途广泛，不论是 xray、clash 等代理软件，还是 Istio 服务网格中得使用了应用。了解它的原理和工作方式有助于我们科学正确的使用代理，而是否使用透明代理取决于你对它的信任和了解程度。

参考
tproxy-example - github.com
Linux transparent proxy support - powerdns.org
Feature: TPROXY version 4.1+ Support - wiki.squid-cache.org

TProxy 不会修改报文头，但却可以将报文转发。

It redirects the packet to a local socket without changing the packet header in any way.

它会将数据包重定向到一个本地的 socket 上，而不会以任何形式修改包的头部。

TProxy 模块工作在 mangle 表上，

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
