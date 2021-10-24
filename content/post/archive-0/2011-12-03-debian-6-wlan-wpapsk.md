---
title: debian 6 wlan wpa/psk
author: "-"
type: post
date: 2011-12-03T15:02:24+00:00
url: /?p=1728
bot_views:
  - 2
categories:
  - Linux
  - Network

---
## debian 6 wlan wpa/psk
我的Debian 6 安装后在/etc/network/interfaces 里没有wlan0的配置项，默认是由"network connections"管理的。

在/etc/network/interfaces 中增加wlan0配置

auto wlan0
iface wlan0 inet dhcp
	wpa-ssid "xxxx"
	wpa-psk "xxxxxx"