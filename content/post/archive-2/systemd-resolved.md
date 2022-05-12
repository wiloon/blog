---
title: resolv.conf, systemd-resolved
author: "-"
date: 2018-12-30T09:59:49+00:00
url: systemd-resolved
categories:
  - Network
tags:
  - reprint
---
## resolv.conf, systemd-resolved

```bash
# check systemd-resolved status
resolvectl status

# disable dns on 53 port
vim /etc/systemd/resolved.conf
#switch off binding to port 53
DNSStubListener=no

#disable LLMNR
LLMNR=false
```

---

<https://cloud-atlas.readthedocs.io/zh_CN/latest/linux/redhat_linux/systemd/systemd_resolved.html>

## resolv.conf, systemd-resolved

```bash
### check status
resolvectl status
### 测试 域名解析
resolvectl query baidu.com
resolvectl query google.com
```

### 配置

```bash
vim /etc/systemd/resolved.conf
[Resolve]
# 上游的dns服务器,可以配置多条
DNS=192.168.50.1
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
