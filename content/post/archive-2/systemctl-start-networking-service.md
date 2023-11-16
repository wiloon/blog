---
title: systemctl start networking.service
author: "-"
date: 2018-07-08T03:22:30+00:00
url: /?p=12409
categories:
  - inbox
tags:
  - reprint
---
## systemctl start networking.service

networking.service raises or downs the network interfaces configured in /etc/network/interfaces, that is, those network interfaces which are not managed by NetworkManager. If you look into /lib/systemd/system/networking.service you will see that all it does is ifup or ifdown depending on whether it is to be started or stopped.

[https://askubuntu.com/questions/850339/what-is-the-networking-service](https://askubuntu.com/questions/850339/what-is-the-networking-service)
