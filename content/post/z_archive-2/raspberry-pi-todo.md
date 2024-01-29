---
title: raspberry pi basic, install, init
author: "-"
date: 2016-09-10T05:44:49+00:00
url: /?p=9199
categories:
  - Raspberry-Pi
tags:
  - reprint
---
## raspberry pi basic, install, init

```bash
#download  image
http://director.downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip

# unzip image
unzip 2018-11-13-raspbian-stretch-lite.zip

# burn the system
sudo dd bs=4M if=2017-08-16-raspbian-stretch.img of=/dev/sdX conv=fsync

```

### config

login with pi/raspberry

sudo raspi-config

* Localisation Options
  * L3 Keyboard
    * Generic 101-key PC
      * Other
        * English(US)
          * English(US) - English (US, alt. intl.)
  * change locale
  * change timezone
  * change keyboard

* change pi password
* network>hostname,wifi

* interface
  * ssh
* advanced options>expand filesystem

finsh and reboot

config ssh public key
  
config source list
  
[http://blog.wiloon.com/?p=7566](http://blog.wiloon.com/?p=7566)

migrate from networking to systemd-networkd with dynamic failover
  
[https://raspberrypi.stackexchange.com/questions/78787/howto-migrate-from-networking-to-systemd-networkd-with-dynamic-failover](https://raspberrypi.stackexchange.com/questions/78787/howto-migrate-from-networking-to-systemd-networkd-with-dynamic-failover)

openvpn
  
[http://www.wiloon.com/?p=11072](http://www.wiloon.com/?p=11072)

sudo apt-get update
  
sudo apt-get upgrade

sudo apt-get install omxplayer
  
sudo apt-get install emacs
  
sudo apt-get install xfonts-wqy
  
apt-get install git

### mirror

```bash
# 编辑 `/etc/apt/sources.list` 文件,删除原文件所有内容,用以下内容取代: 
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib rpi
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib rpi

# 编辑 `/etc/apt/sources.list.d/raspi.list` 文件,删除原文件所有内容,用以下内容取代: 
deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui
```

### mirror backup

deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi

### dhcp server

apt install dnsmasq
