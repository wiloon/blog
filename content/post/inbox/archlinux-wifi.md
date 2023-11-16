---
title: archlinux netctl wifi
author: "-"
date: 2016-04-25T06:39:09+00:00
url: /?p=8945
categories:
  - Inbox
tags:
  - reprint
---
## archlinux netctl wifi

Essay Address: [http://blog.csdn.net/sunnypotter/article/details/23201339](http://blog.csdn.net/sunnypotter/article/details/23201339)
  
    # 如果之前systemctl enable dhcpcd.service
 systemctl dhcpcd.service
 systemctl disable dhcpcd.service

然后

 cd /etc/netctl
 cp examples/wireless-wpa .    # A simple WPA encrypted wireless connection
 vim wireless-wpa    # Modify

+ Interface=wlp8s0 # iw dev查看, 或ip link 或ifconfig
+ Connection=wireless
+ Security=wpa
+
+ IP=dhcp
+ ESSID='wifi-name'
+ Key='wifi-passwd'

注意,必须先完成以上才能进行一下,否则有一系列问题

 netctl enable wireless-wpa
 netctl start wireless-wpa
 reboot
 (
 相关文件夹: /etc/netctl # 网络配置文件夹,假如配置名字叫 wireless-wpa
 /etc/systemd/system #
 /etc/systemd/system  # netctl@wireless-wpa.service
 /etc/systemd/system/multi-user.target.wants # netctl@wireless-wpa.service
 相关命令:
 journalctl -xn
 systemctl -failed
  
    ip link
 ifconfig wlp8s0 up  # start wireless adapter
 ifconfig eno1 up # start wire adapter
  
    # dhcpcd network-adapter 动态分配IP
 dhcpcd eno1
 dhcpcd wlp8s0
 )
  