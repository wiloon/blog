---
title: archlinux ip forward, ip_forward
author: "-"
date: 2019-02-24T04:15:04+00:00
url: ip-forward
tags:
  - network
categories:
  - network

---
## archlinux ip forward, ip_forward

## 开启数据包转发

```bash
vim /etc/sysctl.d/30-ipforward.conf

net.ipv4.ip_forward=1
net.ipv6.conf.default.forwarding=1
net.ipv6.conf.all.forwarding=1
```

```Bash
sysctl -a |grep net.ipv4.ip_forward
```

## 配置 nftables 的转发规则

nftables 默认在 forward 链抛掉所有数据。
如果启用了 nftables, 一定修改一下 nftables 的默认配置文件。否则报文在 iptables 的 forward 链 accept之 后会被 nftables 规则抛掉。

[https://wiki.archlinux.org/index.php/Internet_sharing](https://wiki.archlinux.org/index.php/Internet_sharing)

## ip_forward 与路由转发

https://blog.51cto.com/u156838989/1880744
