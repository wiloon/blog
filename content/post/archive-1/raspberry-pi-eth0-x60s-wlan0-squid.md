---
title: raspberry pi eth0 x60s wlan0 squid
author: "-"
date: 2013-09-27T14:34:29+00:00
url: /?p=5828
categories:
  - Raspberry-Pi

tags:
  - reprint
  - Network
---
## raspberry pi eth0 x60s wlan0 squid
raspberry pi

eth0:192.168.0.59,

mask 255.255.255.0

->

x60s

eth0:192.168.0.1,

mask 255.255.255.0,

gateway:192.168.1.1,

dns:192.168.1.1

->

x60s

wlan0:192.168.1.119

mask:255.255.255.0

gateway:192.168.1.1

dns:192.168.1.1