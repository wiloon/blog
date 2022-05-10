---
title: systemd-networkd
author: "-"
date: 2017-02-28T09:08:28+00:00
url: systemd-networkd
categories:
  - inbox
tags:
  - reprint
---
## systemd-networkd

### dhcp

networkd内置了dhcp client。如果需要更新resolv.conf,则需要启动 systemd-resolved.service

配置文件存放在 /usr/lib/systemd/network (上游提供的配置), /run/systemd/network (运行时配置), 以及 /etc/systemd/network (本地配置). 其中 /etc/systemd/network 有着最高的优先级.

### 有三类配置文件

- .link 文件: 当一个网络设备出现时, udev 会寻找第一个匹配到的 .link 文件.
- .network 文件: 给匹配到的设备应用一个网络配置
- .netdev 文件: 给匹配到的环境创建一个虚拟的网络设备

他们都遵循一些相同的规则:

如果 [Match] 部分满足了条件, 在接下来的段落中的配置会被应用  
[Match] 部分可以接受不止一项条目. 在这种情况下, 只有当每一个条目都被满足时, 这个配置才会被启用  
空白的 [Match] 部分表示这个配置在任何情况下都会被应用  
每一项条目都是 KEY=VALUE 格式的键值对  
所有的配置文件会被收集并按字典序排序后再处理, 无论它们在哪个目录  
相同名字的配置文件会相互替代

### .network 配置

    [Match]
    Name= 设备名 (比如Br0, enp4s0, 也可以用通配符, 比如 en*)
    Host= 匹配的 hostname
    Virtualization= 一个布尔值, 检测你的系统是否运行在一个虚拟化环境中. 也就是说, Virtualization=no 只会在宿主机上满足, 而 Virtualization=yes 会应用到任何虚拟机或 container.

    [Network]
    DHCP= 一个布尔值. 设为 true 的时候, 会启用 systemd-networkd 自带的基础 DHCPv4 支持.
    DNS= DNS 服务器地址.
    Bridge= 如果要将这个连接加入网桥, 在这里写入目标网桥的名字
    Address= 静态的 IPv4 或者 IPv6 地址, 以及相应的用/<数字>方式表示的掩码(如 192.168.1.90/24).
    Gateway= 网关地址.

如果需要指定多个 DNS, Address 或者 Gateway, 你可以多次指定相应的键值对. (也就是说, 多写几行 DNS=xxx, DNS=yyy…)

```bash
pacman -S wpa_supplicant

# start systemd-networkd and systemd-resolved service
systemctl enable systemd-networkd
systemctl start systemd-networkd
systemctl enable systemd-resolved.service
systemctl start systemd-resolved.service

# for wifi
vim  /etc/systemd/network/wifi.network

[Match]
Name=wlp3s0
[Network]
DHCP=yes

cat /etc/wpa_supplicant/wpa_supplicant-wlp3s0.conf
network={
 ssid="w1100n"
 psk="xxxxxxxx"
}

sudo systemctl start wpa_supplicant@wlp2s0


```

### DHCP

for eth0, vim  /etc/systemd/network/eth.network

    [Match]
    Name=en*
    [Network]
    DHCP=yes

### 配置静态 IP, 网关

```bash
vim /etc/systemd/network/eth.network
```

文件内容:

```bash
[Match]
Name=ens3

[Network]
Address=192.168.50.10/24
Gateway=192.168.50.1
DNS=192.168.50.1
```

### 把网卡加入网桥 /etc/systemd/network/10-eth1.network

    [Match]
    Name=enp3s0

    [Network]
    Bridge=br0

### check network config

```bash
   networkctl status -a
```

---

在吃掉 udev 和谋划收编 dbus 后, systemd 又将它的魔爪伸向了网络管理方面. 虽然这已经是 systemd 209 时候的旧闻, 不过因为整个功能太过不完善 (被吐槽有超多 bug, 以及各种基本功能缺失) 以及没有文档, 上游一直没有大力推广.

本文仅就最为简单普通的有线网络连接介绍 systemd-networkd 的打开方式. (wifi 呀, ppp 呀, vpn 呀之类的复杂配置现在都不支持哦) (大部分信息翻译自 ArchWiki)

---

<https://blog.felixc.at/2014/04/try-new-network-configuration-tool-systemd-networkd/>  
<https://blog.felixc.at/2014/04/try-new-network-configuration-tool-systemd-networkd/embed/#?secret=GLctgxboIR>
<https://zhuanlan.zhihu.com/p/19770401>  
<https://linux.cn/article-6629-1.html>  
