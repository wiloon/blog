---
title: archlinux wireless
author: "-"
date: 2015-04-26T08:29:37+00:00
url: /?p=7520
tags:
  - Arch Linux
categories:
  - inbox
---
## archlinux wireless
    https://wiki.archlinux.org/index.php/Wireless_network_configuration
    
    ip link set wlp3s0 up
    
    
    
    wifi-menu -o
    

netctl start <i>profile</i>

netctl enable <i>profile</i>

 netctl start wlp0s26f7u5-w1100n

------deleted
sudo wpa_supplicant -i wlp0s26f7u5 -c /etc/wpa_supplicant/wpa_supplicant.conf -d sudo dhcpcd wlp0s26f7u5