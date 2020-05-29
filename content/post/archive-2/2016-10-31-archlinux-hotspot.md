---
title: archlinux hostapd
author: wiloon
type: post
date: 2016-10-31T06:32:26+00:00
url: /?p=9349
categories:
  - Uncategorized

---
```bash
sudo ip addr add 192.168.49.1/24 dev wlp3s0
sudo ip link set wlp3s0 up
sudo systemctl start dnsmasq.service
sudo nft add rule nat post ip saddr 192.168.49.0/24 oif enp2s0 snat 172.16.xxx.xxx
sudo hostapd /etc/hostapd/hostapd.conf
sudo hostapd -B /etc/hostapd/hostapd.conf
sudo systemctl start hostapd.service 
```

https://wiki.archlinux.org/index.php/software\_access\_point#Wi-Fi\_device\_must\_support\_AP_mode
  
http://os.51cto.com/art/201311/415573.htm

[shell]

sudo pacman -S iw

#check is support AP mode
  
iw list

#edit /etc/hostapd/hostapd.conf

ctrl_interface=/var/run/hostapd
  
ctrl\_interface\_group=wheel
  
\# Some usable default settings&#8230;
  
macaddr_acl=0
  
auth_algs=1
  
ignore\_broadcast\_ssid=0
  
\# Uncomment these for base WPA &amp;amp;amp;amp; WPA2 support with a pre-shared key
  
wpa=2
  
wpa\_key\_mgmt=WPA-PSK
  
wpa_pairwise=TKIP
  
rsn_pairwise=CCMP
  
\# DO NOT FORGET TO SET A WPA PASSPHRASE!!
  
wpa_passphrase=\***\*****
  
\# Most modern wireless drivers in the kernel need driver=nl80211
  
#ieee80211n=1
  
\# Customize these for your local configuration&#8230;
  
interface=wlp3s0
  
hw_mode=g
  
channel=7
  
ssid=20160621
  
logger_stdout=-1
  
logger\_stdout\_level=2
  
max\_num\_sta=5
  
driver=nl80211

#edit/etc/dnsmasq.conf

interface=wlp3s0
  
listen-address=192.168.0.1
  
#no-dhcp-interface=
  
dhcp-range=192.168.49.50,192.168.49.150,12h
  
dhcp-option=3,192.168.49.1
  
dhcp-option=6,192.168.1.100

#打开Linux主机网络数据转发功能
  
echo 1 &amp;amp;gt;/proc/sys/net/ipv4/ip_forward 

#设置无线接入点IP地址，命令模式如下：
  
sudo ip addr add 192.168.49.1/24 dev wlp3s0
  
sudo ip link set wlp3s0 up

#启动 hostapd和dnsmasq
  
hostapd -B /etc/hostapd/hostapd.conf
  
#or
  
systemctl start hostapd.service
  
systemctl start dnsmasq.service 

[/shell]