---
title: iw
author: "-"
date: 2011-12-05T13:44:32+00:00
url: /?p=1806
categories:
  - inbox
tags:
  - reprint
---
## iw

### Getting station statistics
    iw dev wlan1 station dump

---

https://wireless.wiki.kernel.org/en/users/documentation/iw
[http://www.linuxquestions.org/questions/linux-wireless-networking-41/ifconfig-vs-iwconfig-268525/](http://www.linuxquestions.org/questions/linux-wireless-networking-41/ifconfig-vs-iwconfig-268525/)

iwconfig only deals with the wireless elements of a wireless card: the ESSID, WEP keys, etc. All the normal attributes of the network card (IP address, subnet mask etc) are assigned through ifconfig. The two utilities don't overlap, and both are required to use the card (unless you're using dhclient, in which case you won't have to use ifconfig directly).