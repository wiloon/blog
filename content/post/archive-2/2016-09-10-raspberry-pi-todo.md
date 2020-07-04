---
title: raspberry pi install, init
author: wiloon
type: post
date: 2016-09-10T05:44:49+00:00
url: /?p=9199
categories:
  - Uncategorized

---
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

  * change pi password
  * network>hostname，wifi
  * localisation 
      * change locale
      * change timezone
      * change keyboard
      * Generic 101-key PC 
          * Other 
              * English(US) 
                  * English(US, alternative international)
  * interface 
      * ssh
  * advanced options>expand filesystem

finsh and reboot

config ssh public key
  
config source list
  
<http://blog.wiloon.com/?p=7566>

migrate from networking to systemd-networkd with dynamic failover
  
https://raspberrypi.stackexchange.com/questions/78787/howto-migrate-from-networking-to-systemd-networkd-with-dynamic-failover

openvpn
  
<http://www.wiloon.com/wordpress/?p=11072>

sudo apt-get update
  
sudo apt-get upgrade

sudo apt-get install omxplayer
  
sudo apt-get install emacs
  
sudo apt-get install xfonts-wqy
  
apt-get install git