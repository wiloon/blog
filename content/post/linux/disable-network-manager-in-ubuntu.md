---
title: Disable Network Manager In Ubuntu
author: "-"
date: 2012-03-13T05:03:15+00:00
url: /?p=2549
categories:
  - Linux
  - Network
tags:$
  - reprint
---
## Disable Network Manager In Ubuntu
This brief tutorial will show you how to quickly disable Network Manager in Ubuntu Lucid and configure a static or DHCP setting manually. This method will not remove or uninstall Network Manager, but makes it inactive every time you login to your computer. If Network Manager is misbehaving, this is also another way to disable it.
  
sudo apt-get purge network-manager network-manager-gnome
  
gedit /etc/network/interfaces
  
auto lo
  
iface lo inet loopback

auto eth0
  
iface eth0 inet static
  
address 3.242.170.149
  
netmask 255.255.255.0
  
gateway 3.242.170.1

If you chose a Static settings, you must also configure the DNS Servers. To do that, press Alt-F2 on your keyboard, then type the commands below and click Run:

gksu edit /etc/resolv.conf