---
title: debian network command
author: w1100n
type: post
date: 2012-01-01T04:04:36+00:00
url: /?p=2059
categories:
  - Linux

---
#restart

sudo /etc/init.d/networking restart

****#获取地址

sudo dhclient eth0

#wlan

iwlist wlan0 scan

iwconfig wlan0 essid

iwconfig wlan0 key open

iwconfig