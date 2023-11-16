---
title: systemd-networkd MAC address spoofing
author: "-"
date: 2018-08-03T16:03:01+00:00
url: /?p=12491
categories:
  - inbox
tags:
  - reprint
---
## systemd-networkd MAC address spoofing

```bash
vim /etc/systemd/network/00-default.link

[Match]
MACAddress=old mac address

[Link]
MACAddress=new mac address
NamePolicy=kernel database onboard slot path
```

### NamePolicy
  
应该如何设置网卡的名称, 仅在未使用 "net.ifnames=0" 内核引导选项时有意义。 接受一个空格分隔的策略列表, 顺序尝试每个策略,并以第一个成功的策略为准。 所得的名字将被用于设置网卡的 "ID_NET_NAME" 属性。 注意,默认的udev规则会用 "ID_NET_NAME" 的值设置 "NAME" 属性(也就是网卡的名称)。 如果网卡已经被空户空间命名,那么将不会进行任何重命名操作。 可用的策略如下:
  
- kernel
如果内核已经为此网卡设置了固定的可预测名称, 那么不进行任何重命名操作。
- database
基于网卡的 "ID_NET_NAME_FROM_DATABASE" 属性值(来自于udev硬件数据库)设置网卡的名称。
- onboard
基于网卡的 "ID_NET_NAME_ONBOARD" 属性值(来自于板载网卡固件)设置网卡的名称。
- slot
基于网卡的 "ID_NET_NAME_SLOT" 属性值(来自于可插拔网卡固件)设置网卡的名称。
- path
基于网卡的 "ID_NET_NAME_PATH" 属性值(来自于网卡的总线位置)设置网卡的名称。
- mac
基于网卡的 "ID_NET_NAME_MAC" 属性值(来自于网卡的固定MAC地址)设置网卡的名称。

### windows mac address

windows 的无线网卡不支持直接修改 mac 地址，虽然可以通过修改注册表实现修改但是mac地址第二位只能修改为 2, 6, A, E 其中的一个， 改成其它值都不会生效。

[https://wiki.archlinux.org/index.php/MAC_address_spoofing](https://wiki.archlinux.org/index.php/MAC_address_spoofing)
[https://wiki.archlinux.org/index.php/MAC_address_spoofing_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87](https://wiki.archlinux.org/index.php/MAC_address_spoofing_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))  
[http://blog.lujun9972.win/blog/2018/06/01/linux%E5%A6%82%E4%BD%95%E6%9B%B4%E6%94%B9%E7%BD%91%E5%8D%A1mac%E5%9C%B0%E5%9D%80/index.html](http://blog.lujun9972.win/blog/2018/06/01/linux%E5%A6%82%E4%BD%95%E6%9B%B4%E6%94%B9%E7%BD%91%E5%8D%A1mac%E5%9C%B0%E5%9D%80/index.html)  
