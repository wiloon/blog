---
title: systemd-networkd, TAP
author: "-"
date: 2019-01-01T04:16:00+00:00
url: /?p=13281
categories:
  - inbox
tags:
  - reprint
---
## systemd-networkd, TAP

- 手动创建tap
- 开机自动创建tap

### 手动创建tap0

```bash
sudo ip tuntap add dev tap0 mode tap
# set ip
sudo ip addr add 192.168.60.1/24 dev tap0
# tap up
sudo ip link set tap0 up

# ---
## delete ip from tap0
sudo ip addr del 192.168.60.1/24 dev tap0
```

### 启动时由systemd自动创建tap0

```bash
sudo vim /etc/systemd/network/90-tap0.netdev
[NetDev]
Description=description0
Name=tap0
Kind=tap

sudo vim /etc/systemd/network/tap.network
[Match]
Name=tap0
[Link]
MACAddress=5a:70:70:48:7f:50
```

[https://www.freedesktop.org/software/systemd/man/systemd.netdev.html](https://www.freedesktop.org/software/systemd/man/systemd.netdev.html)
[https://www.freedesktop.org/software/systemd/man/systemd.network.html](https://www.freedesktop.org/software/systemd/man/systemd.network.html)
