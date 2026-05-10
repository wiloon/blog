---
title: debian network command
author: "-"
date: 2012-01-01T04:04:36+00:00
url: debian-network-command
categories:
  - Linux
tags:
  - reprint
---
## debian network command

# restart

sudo /etc/init.d/networking restart

****#获取地址

sudo dhclient eth0

# wlan

iwlist wlan0 scan

iwconfig wlan0 essid

iwconfig wlan0 key open

iwconfig
