---
title: debian 6 wlan wpa/psk
author: wiloon
type: post
date: 2011-12-03T15:02:24+00:00
url: /?p=1728
bot_views:
  - 2
categories:
  - Linux
  - Network

---
我的Debian 6 安装后在/etc/network/interfaces 里没有wlan0的配置项，默认是由&#8221;network connections&#8221;管理的。

在/etc/network/interfaces 中增加wlan0配置

<pre>auto wlan0
iface wlan0 inet dhcp
	wpa-ssid "xxxx"
	wpa-psk "xxxxxx"</pre>