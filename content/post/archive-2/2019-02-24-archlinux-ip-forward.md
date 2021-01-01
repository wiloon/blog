---
title: archlinux ip forward
author: w1100n
type: post
date: 2019-02-24T04:15:04+00:00
url: /?p=13701
categories:
  - Uncategorized

---
### 开启数据包转发
```bash
vim /etc/sysctl.d/30-ipforward.conf
net.ipv4.ip_forward=1
net.ipv6.conf.default.forwarding=1
net.ipv6.conf.all.forwarding=1
```

### 配置nftables的转发规则
nftables默认在forward链抛掉所有数据。
如果启用了nftables, 一定修改一下nftables的默认配置文件。否则报文在iptables 的forward链accept之后会被nftables规则抛掉。

https://wiki.archlinux.org/index.php/Internet_sharing