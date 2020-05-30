---
title: archlinux hostapd
author: wiloon
type: post
date: 2016-10-31T06:32:26+00:00
url: /?p=9349
categories:
  - Uncategorized

---
system: archlinux
interface: eth*2, wlan*1

hostapd能够使得无线网卡切换为master模式，模拟AP（路由器）功能

### systemd-networkd config
```bash
cd /etc/systemd/network
vim 05-eth0.network
[Match]
Name=enp1s0
[Network]
DHCP=yes

vim 07-br0.netdev
[NetDev]
Name=br0
Kind=bridge

vim 10-eth1.network
[Match]
Name=enp3s0
[Network]
Bridge=br0

vim 15-wlan0.network
[Match]
Name=wlp2s0b1
[Network]
Bridge=br0

vim 20-br0.network
[Match]
Name=br0
[Network]
DNS=192.168.50.1
Address=192.168.97.1/24


```

### iptables
```bash
sudo iptables -t nat -A POSTROUTING -o enp1s0 -j MASQUERADE
```

### hostapd config

```bash
#edit /etc/hostapd/hostapd.conf

interface=wlp2s0b1
# if wlan0 already added to br0, uncomments this line
bridge=br0
driver=nl80211
logger_syslog=-1
logger_syslog_level=2
logger_stdout=-1
logger_stdout_level=2
ctrl_interface=/run/hostapd
ctrl_interface_group=0
hw_mode=g
channel=5
beacon_int=100
dtim_period=2
max_num_sta=5
rts_threshold=-1
fragm_threshold=-1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wmm_enabled=1
wmm_ac_bk_cwmin=4
wmm_ac_bk_cwmax=10
wmm_ac_bk_aifs=7
wmm_ac_bk_txop_limit=0
wmm_ac_bk_acm=0
wmm_ac_be_aifs=3
wmm_ac_be_cwmin=4
wmm_ac_be_cwmax=10
wmm_ac_be_txop_limit=0
wmm_ac_be_acm=0
wmm_ac_vi_aifs=2
wmm_ac_vi_cwmin=3
wmm_ac_vi_cwmax=4
wmm_ac_vi_txop_limit=94
wmm_ac_vi_acm=0
wmm_ac_vo_aifs=2
wmm_ac_vo_cwmin=2
wmm_ac_vo_cwmax=3
wmm_ac_vo_txop_limit=47
wmm_ac_vo_acm=0
eapol_key_index_workaround=0
eap_server=0
own_ip_addr=127.0.0.1
wpa=2
wpa_passphrase=hostapd0
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=test2

```

### dnsmasq
```bash
#vim /etc/dnsmasq.conf
interface=wlp2s0b1
listen-address=192.168.97.1
  
#no-dhcp-interface=
dhcp-range=192.168.97.10,192.168.97.20,12h
# route
dhcp-option=3,192.168.97.1
# dns
dhcp-option=6,192.168.97.1

#打开Linux主机网络数据转发功能
  
echo 1 > /proc/sys/net/ipv4/ip_forward 

sudo hostapd /etc/hostapd/hostapd.conf
```

### related command
```bash
sudo pacman -S iw
#check is support AP mode
iw list
ip link add name br0 type bridge
ip link set br0 up
ip link set eth0 up
ip link set eth0 master br0
# show bridge info
bridge link

sudo ip addr add 192.168.49.1/24 dev wlp3s0
sudo ip link set wlp3s0 up
sudo systemctl start dnsmasq.service
sudo nft add rule nat post ip saddr 192.168.49.0/24 oif enp2s0 snat 172.16.xxx.xxx
sudo hostapd /etc/hostapd/hostapd.conf
sudo hostapd -B /etc/hostapd/hostapd.conf
sudo systemctl start hostapd.service 
#设置无线接入点IP地址，命令模式如下：
  
sudo ip addr add 192.168.49.1/24 dev wlp3s0  
sudo ip link set wlp3s0 up

#启动 hostapd和dnsmasq
hostapd /etc/hostapd/hostapd.conf
hostapd -B /etc/hostapd/hostapd.conf

#or  
systemctl start hostapd.service
systemctl start dnsmasq.service 
```

https://wiki.archlinux.org/index.php/software\_access\_point#Wi-Fi\_device\_must\_support\_AP_mode
  
http://os.51cto.com/art/201311/415573.htm