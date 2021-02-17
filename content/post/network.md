+++
author = "w1100n"
date = "2021-02-17 13:32:57" 
title = "network"

+++
### Dnat VS Redirect VS Tproxy
Dnat:通过iptable nat表变更目标IP和PORT，需要修改数据包，走IPTABLE需要过内核。

Redirect:REDIRECT其实是 DNAT 的一种特殊形式,只变更目标端口，这种场景下只有两台机器通讯。
REDIRECT其实是 DNAT 的一种特殊形式，特殊在其把数据包的目标 IP 改成了 127.0.0.1，端口改成了--to-ports 参数指定的本地端口，这样本机的透明代理程序就能处理这个包，应用能通过内核的状态信息拿到被改写之前的目标 IP 和端口号，具体参考https://unix.stackexchange.com/questions/166692/how-does-a-transparent-socks-proxy-know-which-destination-ip-to-use


TPROXY：开启TCP/IP IP_TRANSPARENT标志，数据在两个SOCKTS间复制, 这种场景不走kernel,不需要开启ip_forward,不需要开启connection_tracking。

TPROXY比REDIRECT新的特性，它能做到不修改数据包，应用只需一点改动就能实现REDIRECT所有的功能，内核文档里有如下说明：

TPROXY (Transparent proxying) often involves "intercepting" traffic on a router. This is
usually done with the iptables REDIRECT target; however, there are serious
limitations of that method. One of the major issues is that it actually
modifies the packets to change the destination address -- which might not be
acceptable in certain situations. (Think of proxying UDP for example: you won't
be able to find out the original destination address. Even in case of TCP
getting the original destination address is racy.)
从这段说明里似乎 UDP 并没有内核状态来记录更改前的 IP 地址，这与这篇博客所说所说的有些矛盾，我目前的理解还是 UDP 在内核没有状态记录。TPROXY得以实现归结为三个要点：

将流量重定向到本地路由
路由规则定义去向
代理程序监听，通过特殊的参数可以响应非本机的 IP(因为包的目的地址没改嘛)

### 策略路由
```bash
    # 创建链 chain0
    iptables -t mangle -N chain0
    # 端口12345的tcp数据打标记 1
    iptables -t mangle -A chain0 -p tcp -j TPROXY --on-port 12345 --tproxy-mark 1
    # 端口12345的udp数据打标记 1
    iptables -t mangle -A chain0 -p udp -j TPROXY --on-port 12345 --tproxy-mark 1
    iptables -t mangle -A PREROUTING -j chain0

    ip rule add fwmark 1 table 100
    ip route add local 0.0.0.0/0 dev lo table 100
```
---

https://www.jianshu.com/p/91a084e91ed2