---
title: 网络唤醒, Wake On LAN, WAL
author: "-"
date: 2019-02-02T06:47:47+00:00
url: wol
categories:
  - network
tags:
  - reprint
  - remix
---
## 网络唤醒, Wake On LAN, WAL

### 华硕 BIOS 设置

```bash
Advanced> APM Configuration> Power on by PCI-E/PCI
```

### archlinux, wol

```bash
pacman -S wol
wol -i 192.168.50.255 -p 9  1c:b7:2c:af:9a:6a
# -i 192.168.50.255, 广播地址
# -p 9， 端口 9，大多数以太网卡都支持 9, 也可以尝试 7 或 0
# 1c:b7:2c:af:9a:6a， 被唤醒的 mac 地址
```

#### ubuntu

```bash
sudo apt-get install wakeonlan
wakeonlan 1c:b7:2c:af:9a:6a
```

### android client

TX ToolBox

Name: 填写一个别名就可以,例如: foo
Mac Address: 填写电脑网卡MAC地址 (注意是主板上有线网卡) ,这个要填写正确,如何获得? 进入命令行运行: ipconfig /all,然后查看对应的物理地址即可,共6组2字节十六进制字符；

Broadcast IP/Hostname/FQDN
Broadcast IP/Hostname 是电脑所在的局域网的广播地址: 如果你的电脑分配到 192.168.1.100 则填写 192.168.1.255,将唤醒包广播到1网段下面所有电脑, Hostname: 则是你电脑的主机名.
FQDN:是广域网唤醒, 例如你的手机在公网 (4g上网), 不在局域网,则需要填写路由器的DDNS域名, 如: <http://homepc.router.net>
Port 端口默认是9, 这里默认就可以

windows

BIOS打开唤醒设置
  
在BIOS电源相关选项寻找Resume By LAN,Enable Wake ON LAN 类似选项开启
  
网卡设置
  
找到对应的网卡,打开可唤醒选项

勾选
  
允许计算机关闭此设备发节约电源
  
允许此设备唤醒计算机

<https://sparkydogx.github.io/2019/01/16/ubuntu-wake-on-lan/>
