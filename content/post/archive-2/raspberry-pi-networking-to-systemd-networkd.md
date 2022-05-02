---
title: raspberry pi networking to systemd-networkd
author: "-"
date: 2018-12-26T14:35:39+00:00
url: /?p=13214
categories:
  - Raspberry-Pi
tags:
  - reprint
---
## raspberry pi networking to systemd-networkd
https://raspberrypi.stackexchange.com/questions/78787/howto-migrate-from-networking-to-systemd-networkd-with-dynamic-failover

```bash
vim /etc/resolvconf.conf
# Set to NO to disable resolvconf from running any subscribers. Defaults to YES.
resolvconf=NO
systemctl disable networking
systemctl disable dhcpcd
systemctl enable systemd-networkd
systemctl enable systemd-resolved
ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf

vim /etc/systemd/network/eth0.network
[Match]
Name=eth0
[Network]
DHCP=yes

apt install deborphan
apt --autoremove purge openresolv
apt --autoremove purge ifupdown
apt --autoremove purge dhcpcd5
apt --autoremove purge isc-dhcp-client isc-dhcp-common
apt --autoremove purge $(deborphan)
apt --autoremove purge $(deborphan) #two times

```
