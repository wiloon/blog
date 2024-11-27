---
title: iptables nat
author: "-"
date: 2018-11-22T13:58:38+00:00
url: iptables/nat
categories:
  - network
tags:
  - reprint
---
## iptables nat

```bash
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 10.10.10.0/24 -o eth0 -j MASQUERADE
```

nat 表需要的三个链:

1. PREROUTING:可以在这里定义进行目的NAT的规则,因为路由器进行路由时只检查数据包的目的ip地址,所以为了使数据包得以正确路由,我们必须在路由之前就进行目的NAT;
2. POSTROUTING:可以在这里定义进行源NAT的规则,系统在决定了数据包的路由以后在执行该链中的规则。
3. OUTPUT:定义对本地产生的数据包的目的NAT规则。

需要用到的几个动作选项:  (真实环境中用大写)

redirect 将数据包重定向到另一台主机的某个端口,通常用实现透明代理和对外开放内网某些服务。

snat 源地址转换,改变数据包的源地址

dnat 目的地址转换,改变数据包的目的地址

masquerade IP伪装,只适用于ADSL等动态拨号上网的IP伪装,如果主机IP是静态分配的,就用snat

### ip 包大致的流向 DNAT, podman

* nat表prerouting链 - nat替换目标地址
* 路由判断
* filter表forward链
* nat表postrouting链 accept
* 路由判断, 流入虚拟网卡 cni-podman0

[https://www.cnblogs.com/highstar/p/3256813.html](https://www.cnblogs.com/highstar/p/3256813.html)
