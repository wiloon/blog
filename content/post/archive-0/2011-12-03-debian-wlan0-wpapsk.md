---
title: debian wlan0 wpa/psk
author: wiloon
type: post
date: 2011-12-03T14:18:27+00:00
url: /?p=1723
bot_views:
  - 1
views:
  - 2
categories:
  - Linux
  - Network

---
1.添加wpa-psk支持，在debian下是这个插件wpasupplicant
  
apt-get install wpasupplicant

可查看debian wiki
  
[code]
   
http://wiki.debian.org/WiFi/HowToUse#wpa_supplicant
   
[/code]

2.修改/etc/network/interfaces项，如下：

[code]
  
iface wlan0 inet dhcp
  
wpa-driver wext
  
wpa-ssid DFERG
  
wpa-proto WPA
  
wpa-pairwise TKIP
  
wpa-group TKIP
  
wpa-key-mgmt WPA-PSK
  
wpa-psk fcb3717c5f66e893d9010a6872436b34686618a3e8fa2833d56bb98b41be5c8d
  
[/code]

3.最关键的WPA－PSK项，之前一直无法连接，经google，原来此处不能写入明文密码，需要通过wpa-passphrase转换的，如下：

[code]
  
wpa\_passphrase <your\_essid> <your\_assic\_key>
  
[/code]

例如:

[shell]
  
wpa_passphrase DFERG 100200300b
  
network={
  
ssid="DFERG"
  
#psk="100200300b"
  
psk=fcb3717c5f66e893d9010a6872436b34686618a3e8fa2833d56bb98b41be5c8d
  
}
  
[/shell]

原文地址：<http://hi.baidu.com/tanmeng_sino/blog/item/8b3526f5781d65e77709d735.html>