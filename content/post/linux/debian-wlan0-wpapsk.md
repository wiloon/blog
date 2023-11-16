---
title: debian wlan0 wpa/psk
author: "-"
date: 2011-12-03T14:18:27+00:00
url: /?p=1723
categories:
  - Linux
  - Network
tags:
  - reprint
---
## debian wlan0 wpa/psk
1.添加wpa-psk支持，在debian下是这个插件wpasupplicant
  
apt-get install wpasupplicant

可查看debian wiki
  
[code]
   
http://wiki.debian.org/WiFi/HowToUse#wpa_supplicant
   
```

2.修改/etc/network/interfaces项，如下: 

[code]
  
iface wlan0 inet dhcp
  
wpa-driver wext
  
wpa-ssid DFERG
  
wpa-proto WPA
  
wpa-pairwise TKIP
  
wpa-group TKIP
  
wpa-key-mgmt WPA-PSK
  
wpa-psk fcb3717c5f66e893d9010a6872436b34686618a3e8fa2833d56bb98b41be5c8d
  
```

3.最关键的WPA－PSK项，之前一直无法连接，经google，原来此处不能写入明文密码，需要通过wpa-passphrase转换的，如下: 

[code]
  
wpa_passphrase <your_essid> <your_assic_key>
  
```

例如:

```bash
  
wpa_passphrase DFERG 100200300b
  
network={
  
ssid="DFERG"
  
#psk="100200300b"
  
psk=fcb3717c5f66e893d9010a6872436b34686618a3e8fa2833d56bb98b41be5c8d
  
}
  
```

原文地址: [http://hi.baidu.com/tanmeng_sino/blog/item/8b3526f5781d65e77709d735.html](http://hi.baidu.com/tanmeng_sino/blog/item/8b3526f5781d65e77709d735.html)