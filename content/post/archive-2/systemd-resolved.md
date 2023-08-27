---
title: resolv.conf, systemd-resolved, DNS
author: "-"
date: 2022-08-03 09:52:54
url: systemd-resolved
categories:
  - Network
tags:
  - reprint
---
## resolv.conf, systemd-resolved, DNS

```bash
# check systemd-resolved status
resolvectl status
resolvectl restart

# disable dns on 53 port
vim /etc/systemd/resolved.conf
#switch off binding to port 53
DNSStubListener=no

# disable LLMNR
LLMNR=false
```

---

<https://cloud-atlas.readthedocs.io/zh_CN/latest/linux/redhat_linux/systemd/systemd_resolved.html>

## 测试 域名解析

```bash
resolvectl query baidu.com
resolvectl query google.com
```

### 配置

```bash
vim /etc/systemd/resolved.conf
[Resolve]
# DNS: 上游的 dns 服务器, 可以配置多条, 用空格分隔
DNS=192.168.50.1
# FallbackDNS: 一个空格分隔的 IPv4 与 IPv6 地址列表。用作系统的替补 DNS 服务器。此选项所设置的 DNS 服务器仅在实在找不到可用 DNS 的情况下才会被使用。
FallbackDNS=223.5.5.5 223.6.6.6 114.114.114.114
#Domains=
#LLMNR=yes
#MulticastDNS=yes
#DNSSEC=allow-downgrade
#DNSOverTLS=no
#Cache=yes
#DNSStubListener=yes
#ReadEtcHosts=yes
```

### link

```bash
ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
```

archlinux
  
<https://wiki.archlinux.org/index.php/Systemd-resolved>

```bash
vim /etc/systemd/resolved.conf
[Resolve]
DNS=192.168.50.1

# link
ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

# restart systemd-resolved
sudo systemctl restart systemd-resolved

# check systemd-resolved status
resolvectl status
```

systemd-resolved
  
<https://blog.wiloon.com/?p=13243>

debian
  
<https://wiki.debian.org/resolv.conf>

```bash
vim /etc/dhcp/dhclient.conf

prepend domain-name-servers 223.5.5.5;
supersede domain-name-servers 223.5.5.5;
sudo dhclient -r
sudo dhclient
```

## Failed to get global data: Unit dbus-org.freedesktop.resolve1.service not found

```bash
# 重新连接服务
sudo ln -sf /lib/systemd/system/systemd-resolved.service /etc/systemd/system/dbus-org.freedesktop.resolve1.service
# 重启服务 
sudo systemctl restart systemd-resolved.service
# 确认状态
systemd-resolve --status
```

<http://www.jinbuguo.com/systemd/resolved.conf.html>
